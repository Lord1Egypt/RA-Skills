#!/usr/bin/env bash
set -euo pipefail

: "${CLOUDFLARE_GLOBAL_API_KEY:?Set CLOUDFLARE_GLOBAL_API_KEY}"
: "${CLOUDFLARE_EMAIL:?Set CLOUDFLARE_EMAIL}"

CF_API="https://api.cloudflare.com/client/v4"
AUTH=(-H "X-Auth-Email: ${CLOUDFLARE_EMAIL}" -H "X-Auth-Key: ${CLOUDFLARE_GLOBAL_API_KEY}" -H "Content-Type: application/json")

cf_request() {
  local method="$1" path="$2" data="${3:-}"
  if [[ -n "$data" ]]; then
    curl -fsS -X "$method" "${AUTH[@]}" -d "$data" "$CF_API$path"
  else
    curl -fsS -X "$method" "${AUTH[@]}" "$CF_API$path"
  fi
}

cf_get() { cf_request GET "$1"; }
cf_post() { cf_request POST "$1" "$2"; }
cf_put() { cf_request PUT "$1" "$2"; }
cf_patch() { cf_request PATCH "$1" "$2"; }
cf_delete() { cf_request DELETE "$1"; }

need_jq() { command -v jq >/dev/null || { echo "jq is required" >&2; exit 1; }; }
need_jq

case "${1:-}" in
  verify)
    cf_get /user/tokens/verify | jq '.result'
    ;;
  zones|zones-list)
    name="${2:-}"
    qs='?per_page=50'
    [[ -n "$name" ]] && qs+="&name=$name"
    cf_get "/zones${qs}" | jq '.result[] | {id, name, status, name_servers}'
    ;;
  zone-get)
    zone_id="${2:?Usage: cf-global.sh zone-get <zone_id>}"
    cf_get "/zones/${zone_id}" | jq '.result | {id, name, status, name_servers, plan: .plan.name}'
    ;;
  zone-id)
    domain="${2:?Usage: cf-global.sh zone-id <domain>}"
    cf_get "/zones?name=${domain}" | jq -r '.result[0].id // empty'
    ;;
  dns-list)
    zone_id="${2:?Usage: cf-global.sh dns-list <zone_id> [type] [name]}"
    type="${3:-}"
    name="${4:-}"
    qs='?per_page=100'
    [[ -n "$type" ]] && qs+="&type=$type"
    [[ -n "$name" ]] && qs+="&name=$name"
    cf_get "/zones/${zone_id}/dns_records${qs}" | jq '.result[] | {id, type, name, content, proxied, ttl}'
    ;;
  dns-create)
    zone_id="${2:?Usage: cf-global.sh dns-create <zone_id> <type> <name> <content> [proxied] [ttl]}"
    type="${3:?}"; name="${4:?}"; content="${5:?}"
    proxied="${6:-false}"; ttl="${7:-1}"
    data=$(jq -n --arg t "$type" --arg n "$name" --arg c "$content" --argjson p "$proxied" --argjson ttl "$ttl" '{type:$t,name:$n,content:$c,proxied:$p,ttl:$ttl}')
    cf_post "/zones/${zone_id}/dns_records" "$data" | jq '.result | {id, type, name, content, proxied, ttl}'
    ;;
  dns-update)
    zone_id="${2:?Usage: cf-global.sh dns-update <zone_id> <record_id> <type> <name> <content> [proxied] [ttl]}"
    record_id="${3:?}"; type="${4:?}"; name="${5:?}"; content="${6:?}"
    proxied="${7:-false}"; ttl="${8:-1}"
    data=$(jq -n --arg t "$type" --arg n "$name" --arg c "$content" --argjson p "$proxied" --argjson ttl "$ttl" '{type:$t,name:$n,content:$c,proxied:$p,ttl:$ttl}')
    cf_put "/zones/${zone_id}/dns_records/${record_id}" "$data" | jq '.result | {id, type, name, content, proxied, ttl}'
    ;;
  dns-delete)
    zone_id="${2:?Usage: cf-global.sh dns-delete <zone_id> <record_id>}"
    record_id="${3:?}"
    cf_delete "/zones/${zone_id}/dns_records/${record_id}" | jq '.'
    ;;
  dns-export)
    zone_id="${2:?Usage: cf-global.sh dns-export <zone_id>}"
    cf_get "/zones/${zone_id}/dns_records?per_page=500" | jq '[.result[] | {type, name, content, proxied, ttl, priority}]'
    ;;
  dns-import)
    zone_id="${2:?Usage: cf-global.sh dns-import <zone_id> <file.json>}"
    file="${3:?}"
    jq -c '.[]' "$file" | while IFS= read -r rec; do
      cf_post "/zones/${zone_id}/dns_records" "$rec" | jq '.result | {id, type, name, content}'
    done
    ;;
  settings-list)
    zone_id="${2:?Usage: cf-global.sh settings-list <zone_id>}"
    cf_get "/zones/${zone_id}/settings" | jq '.result[] | {id, value}'
    ;;
  setting-get)
    zone_id="${2:?Usage: cf-global.sh setting-get <zone_id> <setting_id>}"
    setting="${3:?}"
    cf_get "/zones/${zone_id}/settings/${setting}" | jq '.result | {id, value}'
    ;;
  setting-set)
    zone_id="${2:?Usage: cf-global.sh setting-set <zone_id> <setting_id> <value>}"
    setting="${3:?}"; value="${4:?}"
    data=$(jq -n --arg v "$value" '{value:$v}')
    cf_patch "/zones/${zone_id}/settings/${setting}" "$data" | jq '.result | {id, value}'
    ;;
  ssl-get)
    zone_id="${2:?Usage: cf-global.sh ssl-get <zone_id>}"
    cf_get "/zones/${zone_id}/settings/ssl" | jq '.result | {id, value}'
    ;;
  ssl-set)
    zone_id="${2:?Usage: cf-global.sh ssl-set <zone_id> <off|flexible|full|strict>}"
    mode="${3:?}"
    data=$(jq -n --arg v "$mode" '{value:$v}')
    cf_patch "/zones/${zone_id}/settings/ssl" "$data" | jq '.result | {id, value}'
    ;;
  cache-purge)
    zone_id="${2:?Usage: cf-global.sh cache-purge <zone_id> [url1 url2 ...]}"
    shift 2
    if [[ $# -eq 0 ]]; then
      data='{"purge_everything":true}'
    else
      data=$(printf '%s\n' "$@" | jq -R . | jq -sc '{files:.}')
    fi
    cf_post "/zones/${zone_id}/purge_cache" "$data" | jq '.result'
    ;;
  pagerules-list)
    zone_id="${2:?Usage: cf-global.sh pagerules-list <zone_id>}"
    cf_get "/zones/${zone_id}/pagerules" | jq '.result[] | {id, status, targets, actions}'
    ;;
  firewall-list)
    zone_id="${2:?Usage: cf-global.sh firewall-list <zone_id>}"
    cf_get "/zones/${zone_id}/firewall/rules" | jq '.result[] | {id, description, action, filter: .filter.expression}'
    ;;
  tunnels-list)
    acct="${CLOUDFLARE_ACCOUNT_ID:?Set CLOUDFLARE_ACCOUNT_ID for tunnel ops}"
    cf_get "/accounts/${acct}/cfd_tunnel" | jq '.result[] | {id, name, status, created_at}'
    ;;
  tunnel-get)
    acct="${CLOUDFLARE_ACCOUNT_ID:?Set CLOUDFLARE_ACCOUNT_ID}"
    tunnel_id="${2:?Usage: cf-global.sh tunnel-get <tunnel_id>}"
    cf_get "/accounts/${acct}/cfd_tunnel/${tunnel_id}" | jq '.result'
    ;;
  tunnel-create)
    acct="${CLOUDFLARE_ACCOUNT_ID:?Set CLOUDFLARE_ACCOUNT_ID}"
    name="${2:?Usage: cf-global.sh tunnel-create <name>}"
    secret=$(openssl rand -base64 32)
    data=$(jq -n --arg n "$name" --arg s "$secret" '{name:$n, tunnel_secret:$s, config_src:"cloudflare"}')
    cf_post "/accounts/${acct}/cfd_tunnel" "$data" | jq '.result | {id, name, status, created_at}'
    ;;
  tunnel-delete)
    acct="${CLOUDFLARE_ACCOUNT_ID:?Set CLOUDFLARE_ACCOUNT_ID}"
    tunnel_id="${2:?Usage: cf-global.sh tunnel-delete <tunnel_id>}"
    cf_delete "/accounts/${acct}/cfd_tunnel/${tunnel_id}" | jq '.'
    ;;
  analytics)
    zone_id="${2:?Usage: cf-global.sh analytics <zone_id> [since]}"
    since="${3:--1440}"
    cf_get "/zones/${zone_id}/analytics/dashboard?since=${since}" | jq '.result.totals'
    ;;
  *)
    echo "Usage: $0 {verify|zones|zones-list|zone-get|zone-id|dns-list|dns-create|dns-update|dns-delete|dns-export|dns-import|settings-list|setting-get|setting-set|ssl-get|ssl-set|cache-purge|pagerules-list|firewall-list|tunnels-list|tunnel-get|tunnel-create|tunnel-delete|analytics}" >&2
    exit 1
    ;;
esac
