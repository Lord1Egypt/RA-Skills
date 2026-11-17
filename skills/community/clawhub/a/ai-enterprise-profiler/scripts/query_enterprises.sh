#!/usr/bin/env bash
set -euo pipefail

BASE_URL="${BASE_URL:-https://mcp.applications.jiqizhixin.com}"
API_TOKEN_FROM_ENV="${JQZX_API_TOKEN:-}"

QUERY=""
COMPANY=""
REGION=""
FOUNDED_AFTER=""
FOUNDED_BEFORE=""
INVESTOR=""
TAG=""
MODEL_KEYWORD=""
PRODUCT_KEYWORD=""
TEAM_KEYWORD=""
TEAM_ROLE=""
TEAM_BACKGROUND=""
LISTED=""
HAS_FOUNDER=""
LIMIT=""
CURSOR=""
SORT_BY=""
SORT_ORDER=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --query)
      QUERY="${2:-}"
      shift 2
      ;;
    --company)
      COMPANY="${2:-}"
      shift 2
      ;;
    --region)
      REGION="${2:-}"
      shift 2
      ;;
    --founded-after)
      FOUNDED_AFTER="${2:-}"
      shift 2
      ;;
    --founded-before)
      FOUNDED_BEFORE="${2:-}"
      shift 2
      ;;
    --investor)
      INVESTOR="${2:-}"
      shift 2
      ;;
    --tag)
      TAG="${2:-}"
      shift 2
      ;;
    --model-keyword)
      MODEL_KEYWORD="${2:-}"
      shift 2
      ;;
    --product-keyword)
      PRODUCT_KEYWORD="${2:-}"
      shift 2
      ;;
    --team-keyword)
      TEAM_KEYWORD="${2:-}"
      shift 2
      ;;
    --team-role)
      TEAM_ROLE="${2:-}"
      shift 2
      ;;
    --team-background)
      TEAM_BACKGROUND="${2:-}"
      shift 2
      ;;
    --listed)
      LISTED="${2:-}"
      shift 2
      ;;
    --has-founder)
      HAS_FOUNDER="${2:-}"
      shift 2
      ;;
    --limit)
      LIMIT="${2:-}"
      shift 2
      ;;
    --cursor)
      CURSOR="${2:-}"
      shift 2
      ;;
    --sort-by)
      SORT_BY="${2:-}"
      shift 2
      ;;
    --sort-order)
      SORT_ORDER="${2:-}"
      shift 2
      ;;
    *)
      echo "未知参数: $1"
      exit 1
      ;;
  esac
done

if [[ -z "$API_TOKEN_FROM_ENV" ]]; then
  echo "未检测到环境变量 JQZX_API_TOKEN，请先执行 export JQZX_API_TOKEN=你的Token"
  exit 1
fi

if [[ -z "$QUERY" && -z "$COMPANY" && -z "$REGION" && -z "$INVESTOR" && -z "$TAG" && -z "$MODEL_KEYWORD" && -z "$PRODUCT_KEYWORD" && -z "$TEAM_KEYWORD" && -z "$TEAM_ROLE" && -z "$TEAM_BACKGROUND" && -z "$FOUNDED_AFTER" && -z "$FOUNDED_BEFORE" && -z "$LISTED" && -z "$HAS_FOUNDER" ]]; then
  echo "至少需要提供一个查询条件，例如 --query、--company、--region、--investor"
  exit 1
fi

BODY="$(jq -n \
  --arg query "$QUERY" \
  --arg company "$COMPANY" \
  --arg region "$REGION" \
  --arg foundedAfter "$FOUNDED_AFTER" \
  --arg foundedBefore "$FOUNDED_BEFORE" \
  --arg investor "$INVESTOR" \
  --arg tag "$TAG" \
  --arg modelKeyword "$MODEL_KEYWORD" \
  --arg productKeyword "$PRODUCT_KEYWORD" \
  --arg teamKeyword "$TEAM_KEYWORD" \
  --arg teamRole "$TEAM_ROLE" \
  --arg teamBackground "$TEAM_BACKGROUND" \
  --arg listed "$LISTED" \
  --arg hasFounder "$HAS_FOUNDER" \
  --arg limit "$LIMIT" \
  --arg cursor "$CURSOR" \
  --arg sortBy "$SORT_BY" \
  --arg sortOrder "$SORT_ORDER" \
  '
  {}
  | if $query == "" then . else .query = $query end
  | if $company == "" then . else .company = $company end
  | if $region == "" then . else .regions = [$region] end
  | if $foundedAfter == "" then . else .founded_after = $foundedAfter end
  | if $foundedBefore == "" then . else .founded_before = $foundedBefore end
  | if $investor == "" then . else .investors_any = [$investor] end
  | if $tag == "" then . else .tags_any = [$tag] end
  | if $modelKeyword == "" then . else .model_keywords = [$modelKeyword] end
  | if $productKeyword == "" then . else .product_keywords = [$productKeyword] end
  | if $teamKeyword == "" then . else .team_keywords = [$teamKeyword] end
  | if $teamRole == "" then . else .team_roles_any = [$teamRole] end
  | if $teamBackground == "" then . else .team_background_keywords = [$teamBackground] end
  | if $listed == "" then . elif $listed == "true" then .listed = true elif $listed == "false" then .listed = false else .listed = $listed end
  | if $hasFounder == "" then . elif $hasFounder == "true" then .has_founder = true elif $hasFounder == "false" then .has_founder = false else .has_founder = $hasFounder end
  | if $limit == "" then . else .limit = ($limit | tonumber) end
  | if $cursor == "" then . else .cursor = $cursor end
  | if $sortBy == "" then . else .sort_by = $sortBy end
  | if $sortOrder == "" then . else .sort_order = $sortOrder end
  ')"

curl -sS --location --request POST "${BASE_URL%/}/api/v1/enterprises" \
  --header "X-MCP-TOKEN: ${API_TOKEN_FROM_ENV}" \
  --header "Content-Type: application/json" \
  --data "${BODY}"
