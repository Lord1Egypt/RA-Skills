#!/usr/bin/env bash
# bring.sh — CLI for the Bring! Shopping Lists API
# Requires: curl, jq
# Auth: temporary BRING_EMAIL + BRING_PASSWORD env vars for login only; profile
# preferences and tokens use protected local files, never a stored password.
set -euo pipefail
# Every credential, token, and temporary file created by this process starts
# owner-only. Individual writes below also use atomic same-directory renames.
umask 077

###############################################################################
# Constants
###############################################################################
API_BASE="https://api.getbring.com/rest"
CATALOG_BASE="https://web.getbring.com/locale"
# Public Bring! app client identifier — NOT a user secret. Bring clients use
# this shared value to identify the application, while user auth uses tokens.
BRING_APP_CLIENT_ID="cof4Nc6D8saplXjE3h3HXqHH8m7VU2i1Gs0g85Sp"
TOKEN_FILE="${BRING_TOKEN_FILE:-${HOME}/.cache/bring/token.json}"
CRED_FILE="${BRING_CREDENTIALS_FILE:-${HOME}/.config/bring/credentials.json}"
# Country code for Bring API (affects item catalog language). Override in credentials.json.
BRING_COUNTRY="${BRING_COUNTRY:-DE}"
BRING_LOCALE="${BRING_LOCALE:-}"
DRY_RUN=0

###############################################################################
# Helpers
###############################################################################
die()  { echo "ERROR: $*" >&2; exit 1; }
info() { echo "$*" >&2; }

ensure_private_dir() {
  local dir="$1"
  [[ ! -L "$dir" ]] || die "Refusing symlinked secret directory: $dir"
  mkdir -p -m 700 -- "$dir"
  [[ -d "$dir" && -O "$dir" && ! -L "$dir" ]] || die "Secret directory must be an owner-controlled directory: $dir"
  chmod 700 -- "$dir"
}

# Read stdin into a private file in the destination directory, then atomically
# replace the destination. Refuse special files and symlinks rather than
# following them while handling credentials or tokens.
atomic_secret_write() {
  local target="$1" dir base tmp
  dir="$(dirname "$target")"
  base="$(basename "$target")"
  ensure_private_dir "$dir"

  if [[ -L "$target" || ( -e "$target" && ( ! -f "$target" || ! -O "$target" ) ) ]]; then
    die "Refusing unsafe secret file: $target"
  fi

  tmp="$(mktemp "${dir}/.${base}.tmp.XXXXXX")" || die "Could not create private temporary file"
  chmod 600 -- "$tmp"
  if ! cat > "$tmp"; then
    rm -f -- "$tmp"
    die "Could not write private temporary file"
  fi
  mv -f -- "$tmp" "$target"
  chmod 600 -- "$target"
}

sanitize_profile() {
  [[ -f "$CRED_FILE" ]] || return 0
  jq -e 'type == "object"' "$CRED_FILE" >/dev/null 2>&1 \
    || die "Invalid profile JSON: $CRED_FILE"

  if jq -e 'has("email") or has("password")' "$CRED_FILE" >/dev/null 2>&1; then
    jq 'del(.email, .password)' "$CRED_FILE" | atomic_secret_write "$CRED_FILE"
    info "Removed legacy email/password fields from $CRED_FILE"
  fi
}

write_default_list() {
  local list_name="$1"
  if [[ -f "$CRED_FILE" ]]; then
    jq --arg list "$list_name" '. + {default_list: $list}' "$CRED_FILE"
  else
    jq -n --arg list "$list_name" '{default_list: $list}'
  fi | atomic_secret_write "$CRED_FILE"
}

require_cmd() {
  for cmd in "$@"; do
    command -v "$cmd" >/dev/null 2>&1 || die "Required command '$cmd' not found. Install it first."
  done
}

# URL-encode a string (handles special chars like #, &, =, spaces, etc.)
# Uses jq (required dep) as primary encoder; falls back to python3 (optional) then sed.
urlencode() {
  printf '%s' "$1" | jq -sRr @uri 2>/dev/null \
    || python3 -c "import urllib.parse,sys; print(urllib.parse.quote(sys.stdin.read().rstrip('\n'), safe=''))" <<< "$1" 2>/dev/null \
    || printf '%s' "$1" | sed 's/%/%25/g; s/ /%20/g; s/!/%21/g; s/#/%23/g; s/\$/%24/g; s/&/%26/g; s/'\''/%27/g; s/(/%28/g; s/)/%29/g; s/\*/%2A/g; s/+/%2B/g; s/,/%2C/g; s|/|%2F|g; s/:/%3A/g; s/;/%3B/g; s/=/%3D/g; s/?/%3F/g; s/@/%40/g; s/\[/%5B/g; s/\]/%5D/g'
}

require_cmd curl jq

###############################################################################
# Credentials
###############################################################################
load_profile() {
  # The profile is non-secret. Passwords are never loaded from disk; an
  # interactive setup or explicitly supplied environment variables are needed
  # only when the refresh token has expired.
  sanitize_profile
  if [[ -z "${BRING_DEFAULT_LIST:-}" && -f "$CRED_FILE" ]]; then
    BRING_DEFAULT_LIST="$(jq -r '.default_list // empty' "$CRED_FILE" 2>/dev/null)" || true
  fi

  # Load country override if configured
  if [[ -f "$CRED_FILE" ]]; then
    local cfg_country cfg_locale
    cfg_country="$(jq -r '.country // empty' "$CRED_FILE" 2>/dev/null)" || true
    if [[ -n "$cfg_country" ]]; then
      BRING_COUNTRY="$cfg_country"
    fi
    cfg_locale="$(jq -r '.locale // empty' "$CRED_FILE" 2>/dev/null)" || true
    if [[ -z "$BRING_LOCALE" && -n "$cfg_locale" ]]; then
      BRING_LOCALE="$cfg_locale"
    fi
  fi
}

load_login_credentials() {
  if [[ -z "${BRING_EMAIL:-}" || -z "${BRING_PASSWORD:-}" ]]; then
    die "No login credentials in this session. Run 'bring.sh setup' in your own terminal; passwords are never stored on disk."
  fi
}

# Resolve list argument: use provided value or fall back to default
resolve_list_arg() {
  local input="${1:-}"
  if [[ -z "$input" ]]; then
    if [[ -n "${BRING_DEFAULT_LIST:-}" ]]; then
      echo "$BRING_DEFAULT_LIST"
    else
      die "No list specified and no default_list configured. Set \"default_list\" in $CRED_FILE or pass a list name."
    fi
  else
    echo "$input"
  fi
}

###############################################################################
# Token management
###############################################################################
save_token() {
  atomic_secret_write "$TOKEN_FILE"
}

load_token() {
  [[ -f "$TOKEN_FILE" ]] || return 1
  # Check expiry — token file stores expires_at (unix timestamp)
  local expires_at
  expires_at="$(jq -r '.expires_at // 0' "$TOKEN_FILE" 2>/dev/null)" || return 1
  local now
  now="$(date +%s)"
  if (( now >= expires_at - 60 )); then
    # Try refresh
    local refresh_token
    refresh_token="$(jq -r '.refresh_token // empty' "$TOKEN_FILE" 2>/dev/null)" || return 1
    if [[ -n "$refresh_token" ]]; then
      refresh_access_token "$refresh_token" && return 0
    fi
    return 1
  fi
  return 0
}

get_header() {
  local field="$1"
  jq -r ".$field // empty" "$TOKEN_FILE" 2>/dev/null
}

authenticated_curl() {
  local method="$1" url="$2"
  shift 2
  local token_type access_token uuid public_uuid curl_config status
  token_type="$(get_header token_type)"
  access_token="$(get_header access_token)"
  uuid="$(get_header uuid)"
  public_uuid="$(get_header publicUuid)"

  [[ "$BRING_COUNTRY" =~ ^[A-Za-z]{2}$ ]] || die "Invalid country code"
  ensure_private_dir "$(dirname "$TOKEN_FILE")"
  curl_config="$(mktemp "$(dirname "$TOKEN_FILE")/.bring-curl.XXXXXX")" || die "Could not create private curl config"
  chmod 600 -- "$curl_config"
  {
    printf 'header = "Authorization: %s %s"\n' "$token_type" "$access_token"
    printf 'header = "X-BRING-API-KEY: %s"\n' "$BRING_APP_CLIENT_ID"
    printf 'header = "X-BRING-CLIENT: android"\n'
    printf 'header = "X-BRING-APPLICATION: bring"\n'
    printf 'header = "X-BRING-COUNTRY: %s"\n' "$BRING_COUNTRY"
    printf 'header = "X-BRING-USER-UUID: %s"\n' "$uuid"
    printf 'header = "X-BRING-PUBLIC-USER-UUID: %s"\n' "$public_uuid"
  } > "$curl_config"

  if curl -s -w "\n%{http_code}" --config "$curl_config" -X "$method" "$url" "$@"; then
    status=0
  else
    status=$?
  fi
  rm -f -- "$curl_config"
  return "$status"
}

api_call() {
  local method="$1" url="$2"
  shift 2

  local response http_code
  response=$(authenticated_curl "$method" "$url" "$@")

  http_code=$(echo "$response" | tail -1)
  local body
  body=$(echo "$response" | sed '$d')

  case "$http_code" in
    200|204|207) echo "$body" ;;
    401) die "Authentication failed (401). Token may be expired. Run: bring.sh login" ;;
    404) die "Not found (404). Check list UUID or item name." ;;
    *)   die "API error (HTTP $http_code): $body" ;;
  esac
}

###############################################################################
# Auth commands
###############################################################################
do_login() {
  local email="${1:-${BRING_EMAIL:-}}"
  local password="${2:-${BRING_PASSWORD:-}}"
  if [[ -z "$email" || -z "$password" ]]; then
    load_login_credentials
    email="$BRING_EMAIL"
    password="$BRING_PASSWORD"
  fi
  local enc_email enc_pass
  enc_email="$(urlencode "$email")"
  enc_pass="$(urlencode "$password")"
  local response http_code
  response=$(printf 'email=%s&password=%s' "$enc_email" "$enc_pass" | curl -s -w "\n%{http_code}" -X POST "${API_BASE}/v2/bringauth" \
    -H "X-BRING-API-KEY: ${BRING_APP_CLIENT_ID}" \
    -H "X-BRING-CLIENT: android" \
    -H "X-BRING-APPLICATION: bring" \
    --data-binary @-)

  http_code=$(echo "$response" | tail -1)
  local body
  body=$(echo "$response" | sed '$d')

  case "$http_code" in
    200) ;;
    400) die "Login failed (400 Bad Request). Check your email address." ;;
    401) die "Login failed (401 Unauthorized). Check your email and password." ;;
    *)   die "Login failed (HTTP $http_code): $body" ;;
  esac

  # Calculate absolute expiry timestamp
  local expires_in now expires_at
  expires_in=$(echo "$body" | jq -r '.expires_in // 0')
  now=$(date +%s)
  expires_at=$(( now + expires_in ))

  # Save token with absolute expiry
  echo "$body" | jq --argjson ea "$expires_at" '. + {expires_at: $ea}' | save_token
  info "Login successful. Token cached at $TOKEN_FILE"
}

refresh_access_token() {
  local refresh_token="$1"

  local response http_code
  response=$(printf 'grant_type=refresh_token&refresh_token=%s' "$refresh_token" | \
    authenticated_curl POST "${API_BASE}/v2/bringauth/token" --data-binary @-)

  http_code=$(echo "$response" | tail -1)
  local body
  body=$(echo "$response" | sed '$d')

  if [[ "$http_code" != "200" ]]; then
    info "Token refresh failed (HTTP $http_code). Re-login required."
    return 1
  fi

  # Merge new token data into existing token file
  local new_expires_in now new_expires_at
  new_expires_in=$(echo "$body" | jq -r '.expires_in // 0')
  now=$(date +%s)
  new_expires_at=$(( now + new_expires_in ))

  jq -s --argjson ea "$new_expires_at" '.[0] * .[1] + {expires_at: $ea}' "$TOKEN_FILE" <(echo "$body") | save_token
  info "Token refreshed successfully."
  return 0
}

ensure_auth() {
  load_profile
  if ! load_token; then
    info "No valid token found. Logging in..."
    do_login
  fi
}

###############################################################################
# API commands
###############################################################################

# Get user UUID from token
get_uuid() {
  get_header uuid
}

# List all shopping lists
do_lists() {
  ensure_auth
  local uuid
  uuid="$(get_uuid)"
  local result
  result=$(api_call GET "${API_BASE}/bringusers/${uuid}/lists")
  echo "$result" | jq -r '.lists[] | select(.name != null and .name != "null") | "\(.listUuid)\t\(.name)\t\(.theme)"' | \
    while IFS=$'\t' read -r id name theme; do
      echo "${id}  ${name}  (theme: ${theme})"
    done
}

do_lists_json() {
  ensure_auth
  local uuid
  uuid="$(get_uuid)"
  api_call GET "${API_BASE}/bringusers/${uuid}/lists"
}

# Resolve list: by UUID or name (partial match)
resolve_list() {
  local input="$1"
  # If it looks like a UUID, use as-is
  if [[ "$input" =~ ^[0-9a-f-]{36}$ ]]; then
    echo "$input"
    return 0
  fi
  # Otherwise search by name
  ensure_auth
  local uuid
  uuid="$(get_uuid)"
  local lists_json
  lists_json=$(api_call GET "${API_BASE}/bringusers/${uuid}/lists")

  local list_uuid
  # Try exact match first (case-insensitive)
  list_uuid=$(echo "$lists_json" | jq -r --arg name "$input" \
    '.lists[] | select(.name | ascii_downcase == ($name | ascii_downcase)) | .listUuid' | head -1)

  if [[ -z "$list_uuid" ]]; then
    # Try partial match
    list_uuid=$(echo "$lists_json" | jq -r --arg name "$input" \
      '.lists[] | select(.name | ascii_downcase | contains($name | ascii_downcase)) | .listUuid' | head -1)
  fi

  if [[ -z "$list_uuid" ]]; then
    die "List not found: '$input'. Use 'bring.sh lists' to see available lists."
  fi
  echo "$list_uuid"
}

# Show items on a list
do_show() {
  local list_id="$1"
  ensure_auth
  local list_uuid
  list_uuid=$(resolve_list "$list_id")

  local result
  result=$(api_call GET "${API_BASE}/v2/bringlists/${list_uuid}")
  result=$(apply_catalog_display_names "$result")

  local purchase_count recently_count
  purchase_count=$(echo "$result" | jq '.items.purchase | length')
  recently_count=$(echo "$result" | jq '.items.recently | length')

  echo "🛒 Shopping List (${purchase_count} items to buy, ${recently_count} recently completed)"
  echo ""

  if (( purchase_count > 0 )); then
    echo "📋 TO BUY:"
    echo "$result" | jq -r '.items.purchase[] | "  • \(.displayName)\(if .specification != "" then " (\(.specification))" else "" end)"'
  else
    echo "📋 TO BUY: (empty)"
  fi

  echo ""

  if (( recently_count > 0 )); then
    echo "✅ RECENTLY COMPLETED:"
    echo "$result" | jq -r '.items.recently[] | "  ✓ \(.displayName)\(if .specification != "" then " (\(.specification))" else "" end)"'
  fi
}

do_show_json() {
  local list_id="$1"
  ensure_auth
  local list_uuid
  list_uuid=$(resolve_list "$list_id")
  api_call GET "${API_BASE}/v2/bringlists/${list_uuid}"
}

# Generate a UUID
gen_uuid() {
  cat /proc/sys/kernel/random/uuid 2>/dev/null || uuidgen 2>/dev/null || python3 -c "import uuid; print(uuid.uuid4())" 2>/dev/null || echo ""
}

# Build a single change entry as JSON (safe for any characters in item/spec)
build_change() {
  local item_name="$1" spec="$2" operation="$3" uuid="${4:-}"
  jq -n --arg item "$item_name" --arg spec "$spec" --arg op "$operation" --arg uuid "$uuid" \
    '{itemId: $item, spec: $spec, uuid: (if $uuid == "" then null else $uuid end), operation: $op, accuracy: "0.0", altitude: "0.0", latitude: "0.0", longitude: "0.0"}'
}

resolve_catalog_locale() {
  if [[ -n "$BRING_LOCALE" ]]; then
    [[ "$BRING_LOCALE" =~ ^[a-z]{2}-[A-Z]{2}$ ]] || die "Invalid Bring catalog locale: '$BRING_LOCALE'"
    echo "$BRING_LOCALE"
    return 0
  fi

  case "${BRING_COUNTRY^^}" in
    DE|AT|CH) echo "de-DE" ;;
    FR|BE|LU) echo "fr-FR" ;;
    IT) echo "it-IT" ;;
    ES) echo "es-ES" ;;
    *) echo "en-US" ;;
  esac
}

# Return the catalog's internal itemId and display name as a tab-separated row.
# Bring sometimes uses different values (for example, itemId Peperoni is shown
# as Paprika in the German catalog); sending itemId is what preserves icons.
match_catalog_item() {
  local query="$1" locale catalog matches count suggestions
  locale="$(resolve_catalog_locale)"
  catalog=$(curl -fsS "${CATALOG_BASE}/catalog.${locale}.json") \
    || die "Could not load Bring catalog for locale '$locale'"

  echo "$catalog" | jq -e '.catalog.sections | type == "array"' >/dev/null 2>&1 \
    || die "Invalid Bring catalog response for locale '$locale'"

  matches=$(echo "$catalog" | jq -c --arg query "$query" '
    [.catalog.sections[].items[]
      | select((.itemId | ascii_downcase) == ($query | ascii_downcase)
            or (.name | ascii_downcase) == ($query | ascii_downcase))]
    | unique_by(.itemId)')
  count=$(echo "$matches" | jq 'length')

  if (( count == 0 )); then
    matches=$(echo "$catalog" | jq -c --arg query "$query" '
      [.catalog.sections[].items[]
        | select((.itemId | ascii_downcase | contains($query | ascii_downcase))
              or (.name | ascii_downcase | contains($query | ascii_downcase)))]
      | unique_by(.itemId)')
    count=$(echo "$matches" | jq 'length')
  fi

  if (( count == 0 )); then
    die "No catalog match for '$query' in locale '$locale'. Use 'add' for a custom item."
  fi
  if (( count > 1 )); then
    suggestions=$(echo "$matches" | jq -r '.[0:8] | map(.name) | join(", ")')
    die "Catalog match for '$query' is ambiguous: $suggestions. Use a more specific name."
  fi

  echo "$matches" | jq -r '.[0] | [.itemId, .name] | @tsv'
}

apply_catalog_display_names() {
  local list_json="$1" locale catalog
  locale="$(resolve_catalog_locale)"
  if ! catalog=$(curl -fsS "${CATALOG_BASE}/catalog.${locale}.json" 2>/dev/null); then
    echo "$list_json"
    return 0
  fi

  printf '%s\n%s\n' "$list_json" "$catalog" | jq -s '
    (reduce (.[1].catalog.sections[].items[]) as $item
      ({}; . + {($item.itemId): $item.name})) as $names
    | .[0]
    | .items.purchase |= map(. + {displayName: ($names[.itemId] // .itemId)})
    | .items.recently |= map(. + {displayName: ($names[.itemId] // .itemId)})'
}

find_list_item() {
  local list_json="$1" input="$2" scope="$3" filter row catalog_id
  case "$scope" in
    purchase) filter='.items.purchase[]' ;;
    recently) filter='.items.recently[]' ;;
    all) filter='(.items.purchase + .items.recently)[]' ;;
    *) die "Invalid item lookup scope: $scope" ;;
  esac

  row=$(echo "$list_json" | jq -c --arg name "$input" "$filter | select(.itemId == \$name)" | head -1)
  if [[ -z "$row" ]]; then
    catalog_id=$(match_catalog_item "$input" 2>/dev/null | cut -f1) || true
    if [[ -n "$catalog_id" ]]; then
      row=$(echo "$list_json" | jq -c --arg name "$catalog_id" "$filter | select(.itemId == \$name)" | head -1)
    fi
  fi
  echo "$row"
}

read_stdin_items() {
  local line
  STDIN_ITEMS=()
  while IFS= read -r line || [[ -n "$line" ]]; do
    line="${line%$'\r'}"
    [[ -n "${line//[[:space:]]/}" ]] || continue
    STDIN_ITEMS+=("$line")
  done
  (( ${#STDIN_ITEMS[@]} > 0 )) || die "No items received on stdin"
}

# Add an item to a list
do_add() {
  local list_id="$1"
  local item_name="$2"
  local spec="${3:-}"
  local display_name="${4:-$item_name}"
  ensure_auth
  local list_uuid
  list_uuid=$(resolve_list "$list_id")

  if (( DRY_RUN )); then
    if [[ -n "$spec" ]]; then
      echo "DRY-RUN: Would add '${display_name}' (${spec}) to list '${list_id}'."
    else
      echo "DRY-RUN: Would add '${display_name}' to list '${list_id}'."
    fi
    return 0
  fi

  local item_uuid
  item_uuid=$(gen_uuid)

  local json_data
  json_data=$(jq -n --argjson change "$(build_change "$item_name" "$spec" "TO_PURCHASE" "$item_uuid")" \
    '{changes: [$change], sender: ""}')

  api_call PUT "${API_BASE}/v2/bringlists/${list_uuid}/items" \
    -H "Content-Type: application/json" \
    -d "$json_data" > /dev/null

  if [[ -n "$spec" ]]; then
    echo "Added '${display_name}' (${spec}) to list."
  else
    echo "Added '${display_name}' to list."
  fi
}

do_smart_add() {
  local list_id="$1" query="$2" spec="${3:-}"
  local match item_id display_name locale
  locale="$(resolve_catalog_locale)"
  match="$(match_catalog_item "$query")"
  IFS=$'\t' read -r item_id display_name <<< "$match"
  info "Catalog match (${locale}): '${query}' -> '${display_name}' [${item_id}]"
  do_add "$list_id" "$item_id" "$spec" "$display_name"
}

# Remove an item from a list
do_remove() {
  local list_id="$1"
  local item_name="$2"
  local requested_name="$item_name"
  ensure_auth
  local list_uuid
  list_uuid=$(resolve_list "$list_id")

  # Find the item's UUID from the list for precise removal
  local list_data item_data item_uuid
  list_data=$(api_call GET "${API_BASE}/v2/bringlists/${list_uuid}")
  item_data=$(find_list_item "$list_data" "$item_name" all)
  item_uuid=$(echo "$item_data" | jq -r '.uuid // empty')

  if [[ -z "$item_uuid" ]]; then
    die "Item '${item_name}' not found on the list. Use 'bring.sh show' to see current items."
  fi
  item_name=$(echo "$item_data" | jq -r '.itemId')

  if (( DRY_RUN )); then
    echo "DRY-RUN: Would permanently remove '${requested_name}' from list '${list_id}'."
    return 0
  fi

  local json_data
  json_data=$(jq -n --argjson change "$(build_change "$item_name" "" "REMOVE" "$item_uuid")" \
    '{changes: [$change], sender: ""}')

  api_call PUT "${API_BASE}/v2/bringlists/${list_uuid}/items" \
    -H "Content-Type: application/json" \
    -d "$json_data" > /dev/null

  echo "Removed '${requested_name}' from list."
}

# Complete (check off) an item
do_complete() {
  local list_id="$1"
  local item_name="$2"
  local requested_name="$item_name"
  ensure_auth
  local list_uuid
  list_uuid=$(resolve_list "$list_id")

  # Find the item's UUID for precise completion
  local list_data item_data item_uuid spec
  list_data=$(api_call GET "${API_BASE}/v2/bringlists/${list_uuid}")
  item_data=$(find_list_item "$list_data" "$item_name" purchase)
  item_uuid=$(echo "$item_data" | jq -r '.uuid // empty')
  spec=$(echo "$item_data" | jq -r '.specification // empty')

  if [[ -z "$item_uuid" ]]; then
    die "Item '${item_name}' not found on the purchase list. It may already be completed."
  fi
  item_name=$(echo "$item_data" | jq -r '.itemId')

  if (( DRY_RUN )); then
    echo "DRY-RUN: Would complete '${requested_name}' on list '${list_id}'."
    return 0
  fi

  local json_data
  json_data=$(jq -n --argjson change "$(build_change "$item_name" "${spec:-}" "TO_RECENTLY" "$item_uuid")" \
    '{changes: [$change], sender: ""}')

  api_call PUT "${API_BASE}/v2/bringlists/${list_uuid}/items" \
    -H "Content-Type: application/json" \
    -d "$json_data" > /dev/null

  echo "Completed '${requested_name}' (moved to recently)."
}

# Uncomplete — move item from recently back to purchase list
do_uncomplete() {
  local list_id="$1"
  local item_name="$2"
  local requested_name="$item_name"
  ensure_auth
  local list_uuid
  list_uuid=$(resolve_list "$list_id")

  # Find item in recently list
  local list_data item_data item_uuid spec
  list_data=$(api_call GET "${API_BASE}/v2/bringlists/${list_uuid}")
  item_data=$(find_list_item "$list_data" "$item_name" recently)
  item_uuid=$(echo "$item_data" | jq -r '.uuid // empty')
  spec=$(echo "$item_data" | jq -r '.specification // empty')

  if [[ -z "$item_uuid" ]]; then
    die "Item '${item_name}' not found in recently completed items."
  fi
  item_name=$(echo "$item_data" | jq -r '.itemId')

  if (( DRY_RUN )); then
    echo "DRY-RUN: Would move '${requested_name}' back to purchase on list '${list_id}'."
    return 0
  fi

  local json_data
  json_data=$(jq -n --argjson change "$(build_change "$item_name" "${spec:-}" "TO_PURCHASE" "$item_uuid")" \
    '{changes: [$change], sender: ""}')

  api_call PUT "${API_BASE}/v2/bringlists/${list_uuid}/items" \
    -H "Content-Type: application/json" \
    -d "$json_data" > /dev/null

  echo "Moved '${requested_name}' back to purchase list."
}

# Add multiple items at once
do_add_multi() {
  local list_id="$1"
  shift
  ensure_auth
  local list_uuid
  list_uuid=$(resolve_list "$list_id")

  if (( DRY_RUN )); then
    for item_spec in "$@"; do
      local item_name spec
      item_name="${item_spec%%|*}"
      if [[ "$item_spec" == *"|"* ]]; then
        spec="${item_spec#*|}"
        echo "DRY-RUN: Would add '${item_name}' (${spec}) to list '${list_id}'."
      else
        echo "DRY-RUN: Would add '${item_name}' to list '${list_id}'."
      fi
    done
    return 0
  fi

  local changes="[]"
  for item_spec in "$@"; do
    local item_name spec item_uuid
    # Support "item|spec" format
    item_name="${item_spec%%|*}"
    if [[ "$item_spec" == *"|"* ]]; then
      spec="${item_spec#*|}"
    else
      spec=""
    fi
    item_uuid=$(gen_uuid)

    changes=$(echo "$changes" | jq --argjson entry "$(build_change "$item_name" "$spec" "TO_PURCHASE" "$item_uuid")" '. + [$entry]')
  done

  local json_data
  json_data=$(jq -n --argjson changes "$changes" '{"changes": $changes, "sender": ""}')

  api_call PUT "${API_BASE}/v2/bringlists/${list_uuid}/items" \
    -H "Content-Type: application/json" \
    -d "$json_data" > /dev/null

  echo "Added $# item(s) to list."
}

# Remove multiple items at once
do_remove_multi() {
  local list_id="$1"
  shift
  ensure_auth
  local list_uuid
  list_uuid=$(resolve_list "$list_id")

  local list_data
  list_data=$(api_call GET "${API_BASE}/v2/bringlists/${list_uuid}")

  local changes="[]" count=0
  for item_name in "$@"; do
    local item_data item_uuid requested_name="$item_name"
    item_data=$(find_list_item "$list_data" "$item_name" all)
    item_uuid=$(echo "$item_data" | jq -r '.uuid // empty')
    if [[ -z "$item_uuid" ]]; then
      info "Warning: '${requested_name}' not found, skipping."
      continue
    fi
    item_name=$(echo "$item_data" | jq -r '.itemId')
    if (( DRY_RUN )); then
      echo "DRY-RUN: Would permanently remove '${requested_name}' from list '${list_id}'."
    else
      changes=$(echo "$changes" | jq --argjson entry "$(build_change "$item_name" "" "REMOVE" "$item_uuid")" '. + [$entry]')
    fi
    (( count++ )) || true
  done

  if (( DRY_RUN )); then
    echo "DRY-RUN: ${count} item(s) would be removed."
    return 0
  fi

  (( count > 0 )) || die "No matching items found to remove"

  local json_data
  json_data=$(jq -n --argjson changes "$changes" '{"changes": $changes, "sender": ""}')

  api_call PUT "${API_BASE}/v2/bringlists/${list_uuid}/items" \
    -H "Content-Type: application/json" \
    -d "$json_data" > /dev/null

  echo "Removed ${count} item(s) from list."
}

# Complete multiple items at once
do_complete_multi() {
  local list_id="$1"
  shift
  ensure_auth
  local list_uuid
  list_uuid=$(resolve_list "$list_id")

  local list_data
  list_data=$(api_call GET "${API_BASE}/v2/bringlists/${list_uuid}")

  local changes="[]"
  local count=0
  for item_name in "$@"; do
    local item_data item_uuid spec requested_name="$item_name"
    item_data=$(find_list_item "$list_data" "$item_name" purchase)
    item_uuid=$(echo "$item_data" | jq -r '.uuid // empty')
    spec=$(echo "$item_data" | jq -r '.specification // empty')
    if [[ -n "$item_uuid" ]]; then
      item_name=$(echo "$item_data" | jq -r '.itemId')
      changes=$(echo "$changes" | jq --argjson entry "$(build_change "$item_name" "${spec:-}" "TO_RECENTLY" "$item_uuid")" '. + [$entry]')
      (( count++ )) || true
    else
      info "Warning: '${requested_name}' not found on purchase list, skipping."
    fi
  done

  if (( count > 0 )); then
    if (( DRY_RUN )); then
      echo "DRY-RUN: ${count} item(s) would be completed on list '${list_id}'."
      return 0
    fi
    local json_data
    json_data=$(jq -n --argjson changes "$changes" '{"changes": $changes, "sender": ""}')
    api_call PUT "${API_BASE}/v2/bringlists/${list_uuid}/items" \
      -H "Content-Type: application/json" \
      -d "$json_data" > /dev/null
  fi

  echo "Completed ${count} item(s)."
}

do_setup() {
  echo "Bring! Credentials Setup"
  echo "========================"
  echo ""
  echo "Only optional list and country preferences are stored in: $CRED_FILE"
  echo "Your password is used only for this login and is never written to disk."
  echo ""
  sanitize_profile
  read -rp "Bring! Email: " email
  read -rsp "Bring! Password: " password
  echo ""

  echo "Testing login..."
  do_login "$email" "$password"
  unset password

  # Show lists and ask for default
  echo ""
  echo "Your Bring! lists:"
  local uuid
  uuid="$(get_uuid)"
  local lists_json
  lists_json=$(api_call GET "${API_BASE}/bringusers/${uuid}/lists")
  local list_count
  list_count=$(echo "$lists_json" | jq '.lists | length')

  local i=1
  echo "$lists_json" | jq -r '.lists[] | .name' | while read -r name; do
    echo "  ${i}. ${name}"
    (( i++ )) || true
  done

  echo ""
  if (( list_count == 1 )); then
    local single_name
    single_name=$(echo "$lists_json" | jq -r '.lists[0].name')
    echo "Only one list found — setting '${single_name}' as default."
    write_default_list "$single_name"
  elif (( list_count > 1 )); then
    read -rp "Which list should be the default? (name or number, Enter to skip): " choice
    if [[ -n "$choice" ]]; then
      local chosen_name
      if [[ "$choice" =~ ^[0-9]+$ ]] && (( choice >= 1 && choice <= list_count )); then
        chosen_name=$(echo "$lists_json" | jq -r --argjson idx "$(( choice - 1 ))" '.lists[$idx].name')
      else
        chosen_name="$choice"
      fi
      write_default_list "$chosen_name"
      echo "Default list set to '${chosen_name}'."
    fi
  fi

  echo ""
  echo "Setup complete! Try: bring.sh show"
}

###############################################################################
# Usage
###############################################################################
usage() {
  cat <<EOF
bring.sh — Bring! Shopping Lists CLI

USAGE:
  bring.sh <command> [arguments]

COMMANDS:
  setup                                Interactive credentials setup
  login                                Login and cache auth token
  lists [--json]                       List all shopping lists
  show [list] [--json]                 Show items on a list
  add [list] <item> [spec]             Add an item (with optional description)
  smart-add [list] <item> [spec]       Add using Bring's catalog for icon matching
  add-multi [list] <items...|->        Add arguments or newline-separated stdin
  remove [list] <item>                 Remove an item from a list
  remove-multi [list] <items...>       Remove multiple items at once
  complete [list] <item>               Check off an item (move to recently)
  complete-multi [list] <items...>     Check off multiple items at once
  uncomplete [list] <item>             Move item back to purchase list

OPTIONS:
  --dry-run                             Validate and preview any modifying command

LIST ARGUMENT:
  Can be a list UUID, a list name (partial match), or omitted if
  "default_list" is set in credentials.json.

DEFAULT LIST:
  Add "default_list" to ~/.config/bring/credentials.json to skip
  specifying the list name every time:
  {"default_list": "Einkaufsliste", "country": "DE", "locale": "de-DE"}

AUTHENTICATION:
  Run 'bring.sh setup' in your own terminal to log in. The password is never
  stored; only a protected refresh token and non-secret profile are kept.

EXAMPLES:
  bring.sh setup
  bring.sh lists
  bring.sh show                        # uses default list
  bring.sh show "Einkaufsliste"
  bring.sh add "Milch" "fettarm, 1L"   # uses default list
  bring.sh smart-add "Paprika" "2 Stück"
  bring.sh add --dry-run "Milch" "1L"
  bring.sh add "Einkaufsliste" "Milch" "fettarm, 1L"
  bring.sh add-multi "Brot" "Käse|Gouda" "Butter|irische"
  printf '%s\n' "Milch|1L" "Brot" | bring.sh add-multi -
  bring.sh complete "Milch"
  bring.sh complete-multi "Milch" "Brot" "Käse"
  bring.sh remove-multi "Milch" "Brot"
EOF
}

###############################################################################
# Main
###############################################################################
main() {
  local filtered_args=() arg
  for arg in "$@"; do
    if [[ "$arg" == "--dry-run" ]]; then
      DRY_RUN=1
    else
      filtered_args+=("$arg")
    fi
  done
  set -- "${filtered_args[@]}"

  local cmd="${1:-help}"
  shift || true

  case "$cmd" in
    add|smart-add|add-multi|remove|remove-multi|complete|complete-multi|uncomplete) ;;
    *) (( DRY_RUN == 0 )) || die "--dry-run is only valid for modifying commands" ;;
  esac

  case "$cmd" in
    setup)
      do_setup
      ;;
    login)
      load_profile
      do_login
      ;;
    lists)
      if [[ "${1:-}" == "--json" ]]; then
        do_lists_json
      else
        do_lists
      fi
      ;;
    create-list|delete-list)
      die "The Bring! API does not reliably support creating or deleting lists. Please manage lists in the Bring! app."
      ;;
    show)
      load_profile
      local show_list
      if [[ "${1:-}" == "--json" ]]; then
        show_list="$(resolve_list_arg "")"
        do_show_json "$show_list"
      elif [[ "${2:-}" == "--json" ]]; then
        do_show_json "$1"
      else
        show_list="$(resolve_list_arg "${1:-}")"
        do_show "$show_list"
      fi
      ;;
    add)
      load_profile
      [[ $# -ge 1 ]] || die "Usage: bring.sh add [list] <item> [specification]"
      local add_list add_item add_spec
      local _try_list=""
      if [[ $# -ge 2 ]]; then _try_list=$(resolve_list "$1" 2>/dev/null) || true; fi
      if [[ $# -ge 2 && -n "$_try_list" ]]; then
        # First arg is a valid list name
        add_list="$1"
        add_item="$2"
        add_spec="${3:-}"
      elif [[ $# -ge 2 ]] && [[ -n "${BRING_DEFAULT_LIST:-}" ]]; then
        # First arg is not a list — use default, treat args as item + spec
        add_list="$BRING_DEFAULT_LIST"
        add_item="$1"
        add_spec="${2:-}"
      elif [[ $# -eq 1 ]]; then
        add_list="$(resolve_list_arg "")"
        add_item="$1"
        add_spec=""
      else
        add_list="$(resolve_list_arg "$1")"
        add_item="$2"
        add_spec="${3:-}"
      fi
      do_add "$add_list" "$add_item" "$add_spec"
      ;;
    smart-add)
      load_profile
      [[ $# -ge 1 ]] || die "Usage: bring.sh smart-add [list] <item> [specification]"
      local smart_list smart_item smart_spec
      local _try_smart=""
      if [[ $# -ge 2 ]]; then _try_smart=$(resolve_list "$1" 2>/dev/null) || true; fi
      if [[ $# -ge 2 && -n "$_try_smart" ]]; then
        smart_list="$1"
        smart_item="$2"
        smart_spec="${3:-}"
      elif [[ $# -ge 2 && -n "${BRING_DEFAULT_LIST:-}" ]]; then
        smart_list="$BRING_DEFAULT_LIST"
        smart_item="$1"
        smart_spec="${2:-}"
      elif [[ $# -eq 1 ]]; then
        smart_list="$(resolve_list_arg "")"
        smart_item="$1"
        smart_spec=""
      else
        smart_list="$(resolve_list_arg "$1")"
        smart_item="$2"
        smart_spec="${3:-}"
      fi
      do_smart_add "$smart_list" "$smart_item" "$smart_spec"
      ;;
    add-multi)
      load_profile
      [[ $# -ge 1 ]] || die "Usage: bring.sh add-multi [list] <item1> [item2|spec] ..."
      local aml _try_aml=""
      _try_aml=$(resolve_list "$1" 2>/dev/null) || true
      if [[ -n "$_try_aml" ]]; then
        aml="$1"; shift
      else
        aml="$(resolve_list_arg "")"
      fi
      if [[ $# -eq 1 && "$1" == "-" ]]; then
        read_stdin_items
        do_add_multi "$aml" "${STDIN_ITEMS[@]}"
      else
        [[ $# -ge 1 ]] || die "No items specified for add-multi"
        do_add_multi "$aml" "$@"
      fi
      ;;
    remove)
      load_profile
      [[ $# -ge 1 ]] || die "Usage: bring.sh remove [list] <item>"
      local rm_list rm_item _try_rm=""
      if [[ $# -ge 2 ]]; then _try_rm=$(resolve_list "$1" 2>/dev/null) || true; fi
      if [[ $# -ge 2 && -n "$_try_rm" ]]; then
        rm_list="$1"; rm_item="$2"
      elif [[ -n "${BRING_DEFAULT_LIST:-}" ]]; then
        rm_list="$BRING_DEFAULT_LIST"; rm_item="$1"
      else
        rm_list="$(resolve_list_arg "$1")"; rm_item="$2"
      fi
      do_remove "$rm_list" "$rm_item"
      ;;
    remove-multi)
      load_profile
      [[ $# -ge 1 ]] || die "Usage: bring.sh remove-multi [list] <item1> [item2] ..."
      local rml _try_rml=""
      _try_rml=$(resolve_list "$1" 2>/dev/null) || true
      if [[ -n "$_try_rml" ]]; then
        rml="$1"; shift
      else
        rml="$(resolve_list_arg "")"
      fi
      do_remove_multi "$rml" "$@"
      ;;
    complete)
      load_profile
      [[ $# -ge 1 ]] || die "Usage: bring.sh complete [list] <item>"
      local comp_list comp_item _try_comp=""
      if [[ $# -ge 2 ]]; then _try_comp=$(resolve_list "$1" 2>/dev/null) || true; fi
      if [[ $# -ge 2 && -n "$_try_comp" ]]; then
        comp_list="$1"; comp_item="$2"
      elif [[ -n "${BRING_DEFAULT_LIST:-}" ]]; then
        comp_list="$BRING_DEFAULT_LIST"; comp_item="$1"
      else
        comp_list="$(resolve_list_arg "$1")"; comp_item="$2"
      fi
      do_complete "$comp_list" "$comp_item"
      ;;
    complete-multi)
      load_profile
      [[ $# -ge 1 ]] || die "Usage: bring.sh complete-multi [list] <item1> [item2] ..."
      local cml _try_cml=""
      _try_cml=$(resolve_list "$1" 2>/dev/null) || true
      if [[ -n "$_try_cml" ]]; then
        cml="$1"; shift
      else
        cml="$(resolve_list_arg "")"
      fi
      do_complete_multi "$cml" "$@"
      ;;
    uncomplete)
      load_profile
      [[ $# -ge 1 ]] || die "Usage: bring.sh uncomplete [list] <item>"
      local unc_list unc_item _try_unc=""
      if [[ $# -ge 2 ]]; then _try_unc=$(resolve_list "$1" 2>/dev/null) || true; fi
      if [[ $# -ge 2 && -n "$_try_unc" ]]; then
        unc_list="$1"; unc_item="$2"
      elif [[ -n "${BRING_DEFAULT_LIST:-}" ]]; then
        unc_list="$BRING_DEFAULT_LIST"; unc_item="$1"
      else
        unc_list="$(resolve_list_arg "$1")"; unc_item="$2"
      fi
      do_uncomplete "$unc_list" "$unc_item"
      ;;
    help|--help|-h)
      usage
      ;;
    *)
      die "Unknown command: $cmd. Run 'bring.sh help' for usage."
      ;;
  esac
}

main "$@"
