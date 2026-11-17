# FreshBooks token helper — source this, then use `fb_curl`.
#
#   . references/fb-token.sh
#   fb_curl /auth/api/v1/users/me | jq .
#
# Requires: curl, jq, and FRESHBOOKS_CLIENT_ID / FRESHBOOKS_CLIENT_SECRET in the
# environment (e.g. `set -a; . ~/.secrets; set +a`).
#
# ── Why this is more than a header wrapper ────────────────────────────────────
# FreshBooks refresh tokens are SINGLE-USE and rotate on every refresh: the token
# you just spent is dead, and if the replacement is not written to disk the account
# is locked out with no way back except re-running the browser authorize flow.
# So the helper caches the access token (to avoid burning refreshes) and persists
# the rotated refresh token immediately.
#
# This uses its OWN state file, deliberately separate from the freshbooks-mcp
# server's store — two writers on one rotating-token file will spend each other's
# tokens and lock the account out of both.

FB_STATE="${FB_STATE:-$HOME/.freshbooks-curl/session.json}"
FB_REDIRECT_URI="${FRESHBOOKS_REDIRECT_URI:-https://localhost}"

fb_state_init() {
  [ -f "$FB_STATE" ] && return 0
  if [ -z "$FRESHBOOKS_REFRESH_TOKEN" ]; then
    echo "fb: no state at $FB_STATE and FRESHBOOKS_REFRESH_TOKEN unset — run the bootstrap in SKILL.md" >&2
    return 1
  fi
  mkdir -p "$(dirname "$FB_STATE")" && chmod 700 "$(dirname "$FB_STATE")"
  # umask in a subshell so the file is owner-only from creation, not after.
  (umask 077; printf '{"refresh_token":"%s","access_token":"","expires_at":0}\n' "$FRESHBOOKS_REFRESH_TOKEN" > "$FB_STATE")
  chmod 600 "$FB_STATE"
}

# Echo a valid access token, refreshing (and persisting the rotation) when stale.
fb_access_token() {
  fb_state_init || return 1
  local now exp tok
  now=$(date +%s)
  exp=$(jq -r '.expires_at // 0' "$FB_STATE")
  tok=$(jq -r '.access_token // ""' "$FB_STATE")

  # 120s of slack so a token cannot expire mid-request.
  if [ -n "$tok" ] && [ "$tok" != "null" ] && [ "$exp" -gt $((now + 120)) ]; then
    printf '%s' "$tok"
    return 0
  fi

  local rt resp new_rt new_at expires_in created_at
  rt=$(jq -r '.refresh_token' "$FB_STATE")
  resp=$(curl -sS -X POST https://api.freshbooks.com/auth/oauth/token \
    -H 'Content-Type: application/x-www-form-urlencoded' \
    --data-urlencode "client_id=$FRESHBOOKS_CLIENT_ID" \
    --data-urlencode "client_secret=$FRESHBOOKS_CLIENT_SECRET" \
    --data-urlencode 'grant_type=refresh_token' \
    --data-urlencode "redirect_uri=$FB_REDIRECT_URI" \
    --data-urlencode "refresh_token=$rt")

  new_at=$(printf '%s' "$resp" | jq -r '.access_token // ""')
  if [ -z "$new_at" ] || [ "$new_at" = "null" ]; then
    echo "fb: refresh failed: $(printf '%s' "$resp" | jq -r '.error_description // .error // .')" >&2
    echo "fb: FreshBooks refresh tokens are single-use. If this one was spent, re-run the bootstrap." >&2
    return 1
  fi

  new_rt=$(printf '%s' "$resp" | jq -r '.refresh_token // ""')
  expires_in=$(printf '%s' "$resp" | jq -r '.expires_in // 0 | numbers')
  created_at=$(printf '%s' "$resp" | jq -r '.created_at // empty | numbers')
  [ -n "$created_at" ] || created_at=$now
  # Writing a missing token as the string "null" would replace the only copy
  # of a usable credential with garbage — refuse instead, keeping the old state.
  if [ -z "$new_rt" ] || [ "$new_rt" = "null" ] || [ -z "$expires_in" ] || [ "$expires_in" -le 0 ]; then
    echo "fb: refresh response carried no refresh token or expiry; state left unchanged." >&2
    echo "fb: The old token may now be spent. If the next call fails, re-run the bootstrap." >&2
    return 1
  fi

  # Persist BEFORE returning: the old token is already dead upstream. umask in
  # a subshell so the temp file holding the tokens is never group/world-readable.
  (umask 077; jq -n --arg rt "$new_rt" --arg at "$new_at" --argjson exp "$((created_at + expires_in))" \
    '{refresh_token:$rt, access_token:$at, expires_at:$exp}' > "$FB_STATE.tmp") \
    && chmod 600 "$FB_STATE.tmp" && mv "$FB_STATE.tmp" "$FB_STATE" || {
      echo "fb: REFRESHED BUT COULD NOT PERSIST — the old token is spent. Fix $FB_STATE and re-bootstrap." >&2
      return 1
    }
  printf '%s' "$new_at"
}

# curl against the FreshBooks API with auth attached. Args after the path are
# passed through to curl, so: fb_curl /path -X POST -d '{...}'
fb_curl() {
  local path="$1"; shift
  local token; token=$(fb_access_token) || return 1
  curl -sS "https://api.freshbooks.com$path" \
    -H "Authorization: Bearer $token" \
    -H 'Api-Version: alpha' \
    -H 'Accept: application/json' \
    "$@"
}

# Resolve the three non-interchangeable identifiers. accountId for
# /accounting/account + /payments/account; businessId for /projects/business +
# /timetracking/business; businessUuid for /accounting/businesses.
#
# business.account_id is observed live as null on real owner accounts, with the
# usable accountId at roles[].accountid — fall back to it, as the server does.
fb_ids() {
  fb_curl /auth/api/v1/users/me \
    | jq '.response as $r
          | ([$r.roles[]?.accountid | select(. != null)][0]) as $roleAcct
          | $r.business_memberships[0].business
          | {accountId: (.account_id // $roleAcct), businessId: .id, businessUuid: .business_uuid, name}'
}

fb_account_id() { fb_ids | jq -r '.accountId'; }
