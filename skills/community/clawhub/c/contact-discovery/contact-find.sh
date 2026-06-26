#!/usr/bin/env bash
set -euo pipefail

API_URL="${PRISMFY_API_URL:-https://api.prismfy.io/v1/search}"
API_URL="${API_URL%/}"
API_ROOT="${PRISMFY_API_ROOT:-}"
API_ROOT="${API_ROOT%/}"
ME_URL="${PRISMFY_ME_URL:-}"
ME_URL="${ME_URL%/}"
SKILL_VERSION="1.0.0"

die() { echo "ERROR: $*" >&2; exit 1; }
need() { command -v "$1" >/dev/null 2>&1 || die "missing dependency: $1"; }

need curl
need jq

company=""
domain=""
person=""
role=""
geo=""
query_family="all"
quota=0
raw=0
engine=""
engines=""
out_file=""

usage() {
  cat <<'EOF'
Contact Discovery helper

Usage:
  contact-find.sh --company "Company" [--domain example.com] [--query-family all]
  contact-find.sh --person "Person" --company "Company" [--domain example.com] [--role "Title"] [--query-family all]
  contact-find.sh --person "Person" [--query-family identity|direct|company|pattern|all]
  contact-find.sh --quota

Options:
  --company NAME
  --domain DOMAIN
  --person NAME
  --role TITLE
  --geo GEO
  --query-family NAME
  --engine NAME
  --engines CSV
  --out FILE
  --raw
  --quota

Query families:
  identity | direct | company | pattern | all

Notes:
  - This helper looks for public contact details and contact-path evidence.
  - It does not invent private emails or guarantee deliverability.
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --company) shift; company="${1:-}" ;;
    --domain) shift; domain="${1:-}" ;;
    --person) shift; person="${1:-}" ;;
    --role) shift; role="${1:-}" ;;
    --geo) shift; geo="${1:-}" ;;
    --query-family) shift; query_family="${1:-all}" ;;
    --engine) shift; engine="${1:-}" ;;
    --engines) shift; engines="${1:-}" ;;
    --out) shift; out_file="${1:-}" ;;
    --raw) raw=1 ;;
    --quota) quota=1 ;;
    --help|-h) usage; exit 0 ;;
    *) die "unknown arg: $1" ;;
  esac
  shift
done

if [[ "$quota" -eq 1 ]]; then
  [[ -n "${PRISMFY_API_KEY:-}" ]] || die "PRISMFY_API_KEY is not set"
  if [[ -z "$ME_URL" ]]; then
    if [[ -n "$API_ROOT" ]]; then
      ME_URL="${API_ROOT}/user/me"
    elif [[ "$API_URL" == */search ]]; then
      ME_URL="${API_URL%/search}/user/me"
    else
      die "cannot derive quota endpoint from PRISMFY_API_URL; set PRISMFY_API_ROOT or PRISMFY_ME_URL"
    fi
  fi
  curl -fsS -H "Authorization: Bearer $PRISMFY_API_KEY" "$ME_URL"
  exit 0
fi

[[ -n "${PRISMFY_API_KEY:-}" ]] || die "PRISMFY_API_KEY is not set"
[[ -n "$company" || -n "$domain" || -n "$person" ]] || { usage; die "provide --company, --domain, or --person"; }

tmp_queries="$(mktemp)"
tmp_runs="$(mktemp)"
tmp_report="$(mktemp)"
trap 'rm -f "$tmp_queries" "$tmp_runs" "$tmp_report"' EXIT
printf '' > "$tmp_queries"
echo "[]" > "$tmp_runs"

add_query() {
  local family="$1"
  local hypothesis="$2"
  local text="$3"
  [[ -n "$text" ]] || return 0
  jq -cn --arg family "$family" --arg hypothesis "$hypothesis" --arg text "$text" \
    '{family:$family,hypothesis:$hypothesis,query:$text}' >> "$tmp_queries"
  printf '\n' >> "$tmp_queries"
}

build_identity_queries() {
  if [[ -n "$domain" ]]; then
    add_query identity support "site:$domain contact"
    add_query identity support "site:$domain about"
    add_query identity support "site:$domain team"
  elif [[ -n "$company" ]]; then
    add_query identity support "\"$company\" official site"
    add_query identity support "\"$company\" contact"
    add_query identity support "\"$company\" team"
  fi
  if [[ -n "$person" ]]; then
    if [[ -n "$company" ]]; then
      add_query identity support "\"$person\" \"$company\""
      add_query identity support "\"$person\" \"$company\" ${role:-role}"
    else
      add_query identity support "\"$person\" contact"
      add_query identity support "\"$person\" bio"
    fi
  fi
}

build_direct_queries() {
  if [[ -n "$person" && -n "$company" ]]; then
    add_query direct support "\"$person\" \"$company\" email"
    add_query direct support "\"$person\" \"$company\" contact"
    add_query direct support "\"$person\" \"$company\" author"
    add_query direct support "\"$person\" \"$company\" press"
    [[ -n "$domain" ]] && add_query direct support "\"$person\" @$domain"
  elif [[ -n "$person" ]]; then
    add_query direct support "\"$person\" email"
    add_query direct support "\"$person\" contact"
  fi
}

build_company_queries() {
  if [[ -n "$domain" ]]; then
    add_query company support "site:$domain contact"
    add_query company support "site:$domain press"
    add_query company support "site:$domain author"
    add_query company support "site:$domain support"
  elif [[ -n "$company" ]]; then
    add_query company support "\"$company\" contact email"
    add_query company support "\"$company\" press email"
    add_query company support "\"$company\" support email"
  elif [[ -n "$person" ]]; then
    add_query company support "\"$person\" contact"
    add_query company support "\"$person\" author"
    add_query company support "\"$person\" website"
  fi
}

build_pattern_queries() {
  if [[ -n "$company" ]]; then
    add_query pattern support "\"$company\" email format"
    add_query pattern support "\"$company\" contact email"
  fi
  if [[ -n "$domain" ]]; then
    add_query pattern support "\"@$domain\""
    add_query pattern support "\"$domain\" email format"
  fi
  if [[ -n "$person" && -n "$company" ]]; then
    add_query pattern support "\"$person\" \"$company\" email format"
  elif [[ -n "$person" ]]; then
    add_query pattern support "\"$person\" email"
    add_query pattern support "\"$person\" contact"
  fi
}

case "$query_family" in
  identity) build_identity_queries ;;
  direct) build_direct_queries ;;
  company) build_company_queries ;;
  pattern) build_pattern_queries ;;
  all)
    build_identity_queries
    build_direct_queries
    build_company_queries
    build_pattern_queries
    ;;
  *) die "unsupported query family: $query_family" ;;
esac

mapfile -t query_lines < <(jq -cs 'unique_by(.query) | .[]' "$tmp_queries")
[[ "${#query_lines[@]}" -gt 0 ]] || die "no queries generated"

api_search() {
  local query="$1"
  local payload
  payload="$(jq -n \
    --arg q "$query" \
    --arg engine "$engine" \
    --arg engines "$engines" \
    --arg geo "$geo" \
    '{
      query: $q
    }
    + (if $engine != "" then {engine: $engine} else {} end)
    + (if $engines != "" then {engines: ($engines | split(","))} else {} end)
    + (if $geo != "" then {geo: $geo} else {} end)')"

  local attempt=0
  local max_attempts=2
  local response
  local err
  while (( attempt < max_attempts )); do
    attempt=$((attempt + 1))
    err="$(mktemp)"
    if response="$(curl -m 20 -fsS "$API_URL" \
      -H "Authorization: Bearer $PRISMFY_API_KEY" \
      -H "Content-Type: application/json" \
      -d "$payload" 2>"$err")"; then
      rm -f "$err"
      printf '%s' "$response"
      return 0
    fi
    local msg
    msg="$(cat "$err" 2>/dev/null || true)"
    rm -f "$err"
    if (( attempt >= max_attempts )); then
      printf '%s' "$msg"
      return 1
    fi
    sleep 1
  done
}

for line in "${query_lines[@]}"; do
  family="$(echo "$line" | jq -r '.family')"
  hypothesis="$(echo "$line" | jq -r '.hypothesis')"
  query="$(echo "$line" | jq -r '.query')"
  if response="$(api_search "$query")"; then
    if printf '%s' "$response" | jq -e 'type == "object" and ((has("results") | not) or (.results | type == "array"))' >/dev/null 2>&1; then
      trimmed_response="$(printf '%s' "$response" | jq -c 'if (.results? | type) == "array" then .results |= .[:5] else . end')"
      jq --arg family "$family" \
         --arg hypothesis "$hypothesis" \
         --arg query "$query" \
         --argjson response "$trimmed_response" \
         '. + [{
           family:$family,
           hypothesis:$hypothesis,
           query:$query,
           status:"ok",
           response:$response
         }]' "$tmp_runs" > "${tmp_runs}.new"
    else
      jq --arg family "$family" \
         --arg hypothesis "$hypothesis" \
         --arg query "$query" \
         --arg error "invalid_response_schema" \
         '. + [{
           family:$family,
           hypothesis:$hypothesis,
           query:$query,
           status:"error",
           error:$error
         }]' "$tmp_runs" > "${tmp_runs}.new"
    fi
  else
    jq --arg family "$family" \
       --arg hypothesis "$hypothesis" \
       --arg query "$query" \
       --arg error "$response" \
       '. + [{
         family:$family,
         hypothesis:$hypothesis,
         query:$query,
         status:"error",
         error:$error
       }]' "$tmp_runs" > "${tmp_runs}.new"
  fi
  mv "${tmp_runs}.new" "$tmp_runs"
done

jq -n \
  --arg timestamp_utc "$(date -u +"%Y-%m-%dT%H:%M:%SZ")" \
  --arg skill_version "$SKILL_VERSION" \
  --arg company "$company" \
  --arg domain "$domain" \
  --arg person "$person" \
  --arg role "$role" \
  --arg query_family "$query_family" \
  --argjson runs "$(cat "$tmp_runs")" \
'
def host_from_url:
  (. // "") | sub("^https?://";"") | split("/")[0] | sub("^www\\."; "");
def combined_text:
  ((.title // "") + " " + (.snippet // "") + " " + (.url // ""));
def normalized_text:
  (combined_text | ascii_downcase);
def extract_emails:
  [combined_text | scan("[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}")];
def is_directory_domain:
  (.domain | test("rocketreach\\.|zoominfo\\.|apollo\\.|lusha\\.|signalhire\\.|contactout\\.|leadiq\\.|hunter\\.|snov\\.|crunchbase\\."));
def source_type($provided_domain; $candidate_domain):
  if .domain == "" then "unknown"
  elif $provided_domain != "" and .domain == $provided_domain then "official"
  elif $candidate_domain != "" and .domain == $candidate_domain then "candidate"
  elif is_directory_domain then "directory"
  elif (.domain | test("linkedin\\.com$|x\\.com$|twitter\\.com$")) then "profile"
  elif (.domain | test("github\\.com$")) then "code"
  else "web"
  end;
def looks_like_pattern:
  normalized_text | test("email format|firstname|first.last|first_last|f.lastname|contact email|press email");
def public_emails_only:
  [ .emails[]?
    | select((ascii_downcase | test("^firstname|^first\\.last|^first_last|^f\\.lastname|^name")) | not)
  ];
def stance($provided_domain; $candidate_domain):
  . as $row
  | if $row.family == "pattern" and ($row | looks_like_pattern) then "pattern"
    elif (($row | public_emails_only | length) > 0)
         and ($row.source_type == "official" or $row.family == "direct" or $row.family == "company")
         then "support"
    elif $row.family == "company" and ($row | normalized_text | test("contact|support|press|help")) then "support"
    elif $row.family == "direct" and ($row | normalized_text | test("email|contact|author|press")) then "support"
    elif $row.family == "identity" and ($row.source_type == "official" or $row.source_type == "candidate") and ($row | normalized_text | test("contact|support|press|team|about|official|company")) then "support"
    else "neutral"
    end;
def evidence_rows($provided_domain; $candidate_domain):
  [ .runs[]
    | select(.status=="ok")
    | .family as $family
    | .query as $query
    | (.response.results // [])[]
    | {
        family: $family,
        query: $query,
        title: (.title // ""),
        url: (.url // ""),
        snippet: (.snippet // ""),
        domain: ((.url // "") | host_from_url)
      }
    | .source_type = (source_type($provided_domain; $candidate_domain))
    | .emails = extract_emails
    | .stance = (stance($provided_domain; $candidate_domain))
  ] | unique_by(.url + "|" + .title);
def canonical_domain($provided_domain):
  if $provided_domain != "" then $provided_domain
  else
    (
      ($company | ascii_downcase | gsub("[^a-z0-9 ]";"") | split(" ") | map(select(length >= 4))) as $company_tokens
      | [ .runs[]
          | select(.status=="ok" and .family=="identity")
          | (.response.results // [])[]
          | {
              domain: (.url // "" | host_from_url),
              text: (((.title // "") + " " + (.snippet // "")) | ascii_downcase)
            }
          | select(.text | test("official|about|company|team|contact|support|press"))
          | . as $row
          | select(($company_tokens | length) == 0 or ($company_tokens | map(. as $t | ($row.domain | contains($t))) | any))
          | .domain
          | select(. != "")
          | select(test("linkedin\\.com$|x\\.com$|twitter\\.com$|github\\.com$|rocketreach\\.|zoominfo\\.|apollo\\.|lusha\\.|signalhire\\.|contactout\\.|leadiq\\.|hunter\\.|snov\\.|crunchbase\\.") | not)
        ]
      | group_by(.)
      | sort_by(length)
      | reverse
      | .[0][0]
    ) // ""
  end;
{
  runs: $runs,
  timestamp_utc: $timestamp_utc,
  skill_version: $skill_version,
  company: $company,
  domain: $domain,
  person: $person,
  role: $role,
  query_family: $query_family
} as $root
| $root
| (canonical_domain($domain)) as $canonical_domain
| (evidence_rows($domain; $canonical_domain)) as $evidence
| ([ $evidence[]
     | select(.stance=="support" and ((.family=="direct" or .family=="company") or .source_type=="official" or (.source_type=="candidate" and .family=="identity")))
     | public_emails_only[]?
   ] | unique) as $emails
| ($evidence | map(select(.family=="pattern" and .stance=="pattern")) | length) as $pattern_hits
| ($evidence | map(select(.family=="company" and .stance=="support")) | length) as $company_contact_hits
| ($evidence | map(select(.family=="direct" and .stance=="support")) | length) as $direct_hits
| ($evidence | map(select(.stance=="support" and ((.family=="direct" or .family=="company") or .source_type=="official" or (.source_type=="candidate" and .family=="identity")) and (.emails | length) > 0)) | length) as $verified_email_hits
| ($evidence | map(select(.stance=="support" and (((.title + " " + .snippet + " " + .url) | ascii_downcase | test("contact|support|press|help|team|author")))) | .url) | unique | length) as $contact_path_hits
| ($evidence | map(select(.stance=="support" and (.source_type=="official" or .source_type=="candidate") and (((.title + " " + .snippet + " " + .url) | ascii_downcase | test("contact|support|press|help|team|author")))) | .url) | unique | length) as $trusted_contact_path_hits
| ($evidence | map(select((.source_type=="official" or .source_type=="candidate") and .stance=="support")) | length) as $identity_support_hits
| ($evidence | map(select(.source_type=="official" and .stance=="support")) | length) as $official_hits
| ($root.runs | map(select(.status=="error")) | length) as $error_count
| ($root.runs | length) as $run_count
| ($root.runs | map(select(.status=="error") | .error) | join(" | ")) as $error_text
| (
    if $person != "" and $company == "" and $domain == "" then
      (if $verified_email_hits > 0 then "partial" else "unclear" end)
    elif $domain != "" then "resolved"
    elif $canonical_domain != "" and $identity_support_hits >= 2 then "resolved"
    elif $canonical_domain != "" and $identity_support_hits >= 1 then "partial"
    elif ($official_hits + $company_contact_hits + $direct_hits) > 0 then "partial"
    else "unclear"
    end
  ) as $identity_status
| (
    if $verified_email_hits > 0 and $identity_status != "unclear" then "public_email_found"
    elif $person != "" and ($company != "" or $domain != "") and $direct_hits >= 1 and $identity_status != "unclear" then "contact_path_found"
    elif $trusted_contact_path_hits >= 1 and $identity_status != "unclear" then "company_contact_found"
    elif $company_contact_hits >= 1 and ($official_hits >= 1 or $identity_status == "resolved") then "company_contact_found"
    elif $pattern_hits >= 1 and ($company != "" or $domain != "") then "company_email_pattern_found"
    elif $person != "" and $company == "" and $domain == "" and $identity_status == "unclear" then "ambiguous"
    elif $error_count == $run_count then "ambiguous"
    elif ($evidence | length) > 0 then "not_found"
    else "ambiguous"
    end
  ) as $contact_verdict
| (
    if ($error_text | test("timed out|timeout|429|rate")) then "RATE_LIMIT_OR_TIMEOUT"
    elif ($error_text | test("invalid_json_response|invalid_response_schema")) then "PRISMFY_INVALID_RESPONSE"
    elif $error_count == $run_count then "PRISMFY_UNAVAILABLE"
    elif $identity_status == "unclear" and ($evidence | length) == 0 then "IDENTITY_UNCLEAR"
    elif ($evidence | length) == 0 then "NO_PUBLIC_EVIDENCE"
    else null
    end
  ) as $run_failure_code
| {
    timestamp_utc: $timestamp_utc,
    skill_version: $skill_version,
    entity: {
      company_name: $company,
      domain: $canonical_domain,
      person_name: $person,
      role: $role
    },
    entity_type:
      (if $person != "" and $company != "" then "person+company"
       elif $person != "" then "person"
       else "company"
       end),
    query_family: $query_family,
    identity_status: $identity_status,
    contact_verdict: $contact_verdict,
    summary:
      ("emails=" + (($emails|length)|tostring)
       + ", direct_hits=" + ($direct_hits|tostring)
       + ", company_hits=" + ($company_contact_hits|tostring)
       + ", pattern_hits=" + ($pattern_hits|tostring)
       + ", official_hits=" + ($official_hits|tostring)),
    public_emails: $emails,
    contact_paths:
      ($evidence
       | map(select(.family=="direct" or .family=="company" or .family=="identity")
             | {title, url, family, source_type})
       | unique_by(.url)
       | .[:8]),
    email_pattern_clues:
      ($evidence
       | map(select(.family=="pattern" and .stance=="pattern")
             | {title, url, snippet})
       | unique_by(.url)
       | .[:5]),
    source_urls: ($evidence | map(.url) | unique | .[:10]),
    evidence: ($evidence | .[:20]),
    query_runs: $root.runs,
    run_failure_code: $run_failure_code
  }
' > "$tmp_report"

if [[ -n "$out_file" ]]; then
  cp "$tmp_report" "$out_file"
fi

if [[ "$raw" -eq 1 ]]; then
  cat "$tmp_report"
  exit 0
fi

jq -r '
  [
    (
      if .contact_verdict == "public_email_found" then "Public email found."
      elif .contact_verdict == "contact_path_found" then "Contact path found."
      elif .contact_verdict == "company_contact_found" then "Company contact found."
      elif .contact_verdict == "company_email_pattern_found" then "Email pattern clue found."
      elif .contact_verdict == "not_found" then "No strong public contact found."
      else "Ambiguous."
      end
    ),
    (
      if (.public_emails | length) > 0 then
        "1. Public email: " + .public_emails[0]
      elif (.entity.domain != "") then
        "1. Identity: canonical domain = " + .entity.domain
      else
        "1. Identity: not fully resolved from public evidence"
      end
    ),
    (
      "2. Evidence: " + .summary
    ),
    (
      if (.contact_paths | length) > 0 then
        "3. Path: " + .contact_paths[0].url
      elif (.email_pattern_clues | length) > 0 then
        "3. Pattern clue: " + (.email_pattern_clues[0].title // "public pattern clue")
      else
        "3. Caution: do not infer a private email from weak public signals"
      end
    ),
    (
      if (.source_urls | length) > 0 then
        "4. Source: " + .source_urls[0]
      else
        "4. Source: no strong source URL surfaced"
      end
    )
  ] | join("\n")
' "$tmp_report"
