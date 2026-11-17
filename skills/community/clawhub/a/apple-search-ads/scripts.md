# Scripts & Automation — Apple Search Ads

Ready-to-use scripts for automating Apple Search Ads operations. Every mutation script respects `confirm_before_push` (SKILL.md Configuration): list the change, confirm, then run.

Contents: Prerequisites · Authentication · Campaign Management · Keywords · Reports · Automation · Setup Scripts · Usage Examples

## Prerequisites

All scripts require:
- `curl` and `jq` installed
- Environment variables set (see `memory-template.md`)
- OAuth token generation working

## Authentication

### get-token.sh

Generate OAuth access token.

```bash
#!/usr/bin/env bash
set -euo pipefail

# SECURITY MANIFEST:
# Environment variables accessed: ASA_CLIENT_ID, ASA_TEAM_ID, ASA_KEY_ID, ASA_PRIVATE_KEY_FILE
# External endpoints called: https://appleid.apple.com/auth/oauth2/token
# Local files read: Private key file (ASA_PRIVATE_KEY_FILE)
# Local files written: none (outputs to stdout)

# Required environment variables
: "${ASA_CLIENT_ID:?Set ASA_CLIENT_ID}"
: "${ASA_TEAM_ID:?Set ASA_TEAM_ID}"
: "${ASA_KEY_ID:?Set ASA_KEY_ID}"
: "${ASA_PRIVATE_KEY_FILE:?Set ASA_PRIVATE_KEY_FILE}"

# Create JWT header (base64url encoded)
header=$(echo -n '{"alg":"ES256","kid":"'"$ASA_KEY_ID"'"}' | openssl base64 -e | tr -d '=' | tr '/+' '_-' | tr -d '\n')

# Create JWT payload
now=$(date +%s)
exp=$((now + 15552000))  # 180 days
payload=$(echo -n '{"sub":"'"$ASA_CLIENT_ID"'","aud":"https://appleid.apple.com","iat":'"$now"',"exp":'"$exp"',"iss":"'"$ASA_TEAM_ID"'"}' | openssl base64 -e | tr -d '=' | tr '/+' '_-' | tr -d '\n')

# Sign with ES256
signature=$(echo -n "$header.$payload" | openssl dgst -sha256 -sign "$ASA_PRIVATE_KEY_FILE" | openssl base64 -e | tr -d '=' | tr '/+' '_-' | tr -d '\n')

client_secret="$header.$payload.$signature"

# Exchange for access token
response=$(curl -s -X POST "https://appleid.apple.com/auth/oauth2/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=client_credentials" \
  -d "client_id=$ASA_CLIENT_ID" \
  -d "client_secret=$client_secret" \
  -d "scope=searchadsorg")

# Output token
echo "$response" | jq -r '.access_token'
```

### Usage

```bash
export ASA_CLIENT_ID="your-client-id"
export ASA_TEAM_ID="your-team-id"
export ASA_KEY_ID="your-key-id"
export ASA_PRIVATE_KEY_FILE="$HOME/.secrets/asa-private-key.p8"

# Get token
export ASA_ACCESS_TOKEN=$(./get-token.sh)
```

## Campaign Management

### list-campaigns.sh

List all campaigns with key metrics.

```bash
#!/usr/bin/env bash
set -euo pipefail

# SECURITY MANIFEST:
# Environment variables accessed: ASA_ACCESS_TOKEN, ASA_ORG_ID
# External endpoints called: https://api.searchads.apple.com/api/v5/campaigns
# Local files read: none
# Local files written: none (outputs to stdout)

: "${ASA_ACCESS_TOKEN:?Set ASA_ACCESS_TOKEN}"
: "${ASA_ORG_ID:?Set ASA_ORG_ID}"

curl -s "https://api.searchads.apple.com/api/v5/campaigns" \
  -H "Authorization: Bearer $ASA_ACCESS_TOKEN" \
  -H "X-AP-Context: orgId=$ASA_ORG_ID" \
  | jq '.data[] | {
    id: .id,
    name: .name,
    status: .status,
    budget: .budgetAmount.amount,
    dailyBudget: .dailyBudgetAmount.amount,
    countries: .countriesOrRegions
  }'
```

### create-campaign.sh

Create a new campaign.

```bash
#!/usr/bin/env bash
set -euo pipefail

# SECURITY MANIFEST:
# Environment variables accessed: ASA_ACCESS_TOKEN, ASA_ORG_ID
# External endpoints called: https://api.searchads.apple.com/api/v5/campaigns
# Local files read: none
# Local files written: none

: "${ASA_ACCESS_TOKEN:?Set ASA_ACCESS_TOKEN}"
: "${ASA_ORG_ID:?Set ASA_ORG_ID}"

# Arguments
NAME="${1:?Usage: $0 <name> <adam_id> <country> <daily_budget>}"
ADAM_ID="${2:?Missing adam_id}"
COUNTRY="${3:?Missing country}"
DAILY_BUDGET="${4:?Missing daily_budget}"

curl -s -X POST "https://api.searchads.apple.com/api/v5/campaigns" \
  -H "Authorization: Bearer $ASA_ACCESS_TOKEN" \
  -H "X-AP-Context: orgId=$ASA_ORG_ID" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "'"$NAME"'",
    "adamId": '"$ADAM_ID"',
    "countriesOrRegions": ["'"$COUNTRY"'"],
    "budgetAmount": {"amount": "10000", "currency": "USD"},
    "dailyBudgetAmount": {"amount": "'"$DAILY_BUDGET"'", "currency": "USD"},
    "supplySources": ["APPSTORE_SEARCH_RESULTS"],
    "billingEvent": "TAPS",
    "status": "ENABLED"
  }' | jq
```

### pause-campaign.sh

Pause a campaign.

```bash
#!/usr/bin/env bash
set -euo pipefail

# SECURITY MANIFEST:
# Environment variables accessed: ASA_ACCESS_TOKEN, ASA_ORG_ID
# External endpoints called: https://api.searchads.apple.com/api/v5/campaigns/{id}
# Local files read: none
# Local files written: none

: "${ASA_ACCESS_TOKEN:?Set ASA_ACCESS_TOKEN}"
: "${ASA_ORG_ID:?Set ASA_ORG_ID}"

CAMPAIGN_ID="${1:?Usage: $0 <campaign_id>}"

curl -s -X PUT "https://api.searchads.apple.com/api/v5/campaigns/$CAMPAIGN_ID" \
  -H "Authorization: Bearer $ASA_ACCESS_TOKEN" \
  -H "X-AP-Context: orgId=$ASA_ORG_ID" \
  -H "Content-Type: application/json" \
  -d '{"status": "PAUSED"}' | jq
```

## Keywords

### add-keywords.sh

Add keywords to an ad group.

```bash
#!/usr/bin/env bash
set -euo pipefail

# SECURITY MANIFEST:
# Environment variables accessed: ASA_ACCESS_TOKEN, ASA_ORG_ID
# External endpoints called: https://api.searchads.apple.com/api/v5/campaigns/{cId}/adgroups/{agId}/targetingkeywords/bulk
# Local files read: none
# Local files written: none

: "${ASA_ACCESS_TOKEN:?Set ASA_ACCESS_TOKEN}"
: "${ASA_ORG_ID:?Set ASA_ORG_ID}"

CAMPAIGN_ID="${1:?Usage: $0 <campaign_id> <adgroup_id> <keyword> <match_type> <bid>}"
ADGROUP_ID="${2:?Missing adgroup_id}"
KEYWORD="${3:?Missing keyword}"
MATCH_TYPE="${4:-EXACT}"  # EXACT, BROAD
BID="${5:-1.00}"

curl -s -X POST "https://api.searchads.apple.com/api/v5/campaigns/$CAMPAIGN_ID/adgroups/$ADGROUP_ID/targetingkeywords/bulk" \
  -H "Authorization: Bearer $ASA_ACCESS_TOKEN" \
  -H "X-AP-Context: orgId=$ASA_ORG_ID" \
  -H "Content-Type: application/json" \
  -d '[{
    "text": "'"$KEYWORD"'",
    "matchType": "'"$MATCH_TYPE"'",
    "bidAmount": {"amount": "'"$BID"'", "currency": "USD"},
    "status": "ACTIVE"
  }]' | jq
```

### add-negatives.sh

Add negative keywords.

```bash
#!/usr/bin/env bash
set -euo pipefail

# SECURITY MANIFEST:
# Environment variables accessed: ASA_ACCESS_TOKEN, ASA_ORG_ID
# External endpoints called: https://api.searchads.apple.com/api/v5/campaigns/{cId}/negativekeywords/bulk
# Local files read: none
# Local files written: none

: "${ASA_ACCESS_TOKEN:?Set ASA_ACCESS_TOKEN}"
: "${ASA_ORG_ID:?Set ASA_ORG_ID}"

CAMPAIGN_ID="${1:?Usage: $0 <campaign_id> <keyword> [match_type]}"
KEYWORD="${2:?Missing keyword}"
MATCH_TYPE="${3:-EXACT}"

curl -s -X POST "https://api.searchads.apple.com/api/v5/campaigns/$CAMPAIGN_ID/negativekeywords/bulk" \
  -H "Authorization: Bearer $ASA_ACCESS_TOKEN" \
  -H "X-AP-Context: orgId=$ASA_ORG_ID" \
  -H "Content-Type: application/json" \
  -d '[{
    "text": "'"$KEYWORD"'",
    "matchType": "'"$MATCH_TYPE"'"
  }]' | jq
```

## Reports

### daily-report.sh

Get yesterday's performance summary. Spend is final same-day; install and CPA columns for windows newer than 2 days are provisional (`measurement.md`) — use this for spend monitoring and the spend gate, not for bid decisions.

```bash
#!/usr/bin/env bash
set -euo pipefail

# SECURITY MANIFEST:
# Environment variables accessed: ASA_ACCESS_TOKEN, ASA_ORG_ID
# External endpoints called: https://api.searchads.apple.com/api/v5/reports/campaigns
# Local files read: none
# Local files written: none

: "${ASA_ACCESS_TOKEN:?Set ASA_ACCESS_TOKEN}"
: "${ASA_ORG_ID:?Set ASA_ORG_ID}"

# Get yesterday's date
if [[ "$OSTYPE" == "darwin"* ]]; then
  YESTERDAY=$(date -v-1d +%Y-%m-%d)
  TODAY=$(date +%Y-%m-%d)
else
  YESTERDAY=$(date -d "yesterday" +%Y-%m-%d)
  TODAY=$(date +%Y-%m-%d)
fi

curl -s -X POST "https://api.searchads.apple.com/api/v5/reports/campaigns" \
  -H "Authorization: Bearer $ASA_ACCESS_TOKEN" \
  -H "X-AP-Context: orgId=$ASA_ORG_ID" \
  -H "Content-Type: application/json" \
  -d '{
    "startTime": "'"$YESTERDAY"'",
    "endTime": "'"$TODAY"'",
    "granularity": "DAILY",
    "returnRowTotals": true,
    "returnGrandTotals": true
  }' | jq '{
    date: "'"$YESTERDAY"'",
    campaigns: [.data.reportingDataResponse.row[] | {
      name: .metadata.campaignName,
      spend: .total.localSpend.amount,
      impressions: .total.impressions,
      taps: .total.taps,
      installs: .total.installs,
      cpa: (if .total.installs > 0 then ((.total.localSpend.amount | tonumber) / .total.installs | . * 100 | round / 100) else null end)
    }],
    totals: {
      spend: .data.reportingDataResponse.grandTotals.total.localSpend.amount,
      impressions: .data.reportingDataResponse.grandTotals.total.impressions,
      taps: .data.reportingDataResponse.grandTotals.total.taps,
      installs: .data.reportingDataResponse.grandTotals.total.installs
    }
  }'
```

### search-terms-report.sh

Get search terms for a campaign. For decisions, request windows ending ≥2 days back (`measurement.md`); `weekly-optimization.sh` below does this automatically.

```bash
#!/usr/bin/env bash
set -euo pipefail

# SECURITY MANIFEST:
# Environment variables accessed: ASA_ACCESS_TOKEN, ASA_ORG_ID
# External endpoints called: https://api.searchads.apple.com/api/v5/reports/campaigns/{id}/searchterms
# Local files read: none
# Local files written: none

: "${ASA_ACCESS_TOKEN:?Set ASA_ACCESS_TOKEN}"
: "${ASA_ORG_ID:?Set ASA_ORG_ID}"

CAMPAIGN_ID="${1:?Usage: $0 <campaign_id> [days]}"
DAYS="${2:-7}"

# Date range
if [[ "$OSTYPE" == "darwin"* ]]; then
  START=$(date -v-${DAYS}d +%Y-%m-%d)
  END=$(date +%Y-%m-%d)
else
  START=$(date -d "$DAYS days ago" +%Y-%m-%d)
  END=$(date +%Y-%m-%d)
fi

curl -s -X POST "https://api.searchads.apple.com/api/v5/reports/campaigns/$CAMPAIGN_ID/searchterms" \
  -H "Authorization: Bearer $ASA_ACCESS_TOKEN" \
  -H "X-AP-Context: orgId=$ASA_ORG_ID" \
  -H "Content-Type: application/json" \
  -d '{
    "startTime": "'"$START"'",
    "endTime": "'"$END"'",
    "selector": {
      "conditions": [
        {"field": "impressions", "operator": "GREATER_THAN", "values": ["5"]}
      ],
      "orderBy": [{"field": "impressions", "sortOrder": "DESCENDING"}],
      "pagination": {"offset": 0, "limit": 100}
    },
    "returnRowTotals": true
  }' | jq '.data.reportingDataResponse.row[] | {
    term: .metadata.searchTermText,
    matchType: .metadata.matchType,
    impressions: .total.impressions,
    taps: .total.taps,
    installs: .total.installs,
    spend: .total.localSpend.amount,
    cpa: (if .total.installs > 0 then ((.total.localSpend.amount | tonumber) / .total.installs | . * 100 | round / 100) else null end)
  }'
```

### keyword-report.sh

Get keyword performance for an ad group.

```bash
#!/usr/bin/env bash
set -euo pipefail

# SECURITY MANIFEST:
# Environment variables accessed: ASA_ACCESS_TOKEN, ASA_ORG_ID
# External endpoints called: https://api.searchads.apple.com/api/v5/reports/campaigns/{cId}/adgroups/{agId}/keywords
# Local files read: none
# Local files written: none

: "${ASA_ACCESS_TOKEN:?Set ASA_ACCESS_TOKEN}"
: "${ASA_ORG_ID:?Set ASA_ORG_ID}"

CAMPAIGN_ID="${1:?Usage: $0 <campaign_id> <adgroup_id> [days]}"
ADGROUP_ID="${2:?Missing adgroup_id}"
DAYS="${3:-7}"

if [[ "$OSTYPE" == "darwin"* ]]; then
  START=$(date -v-${DAYS}d +%Y-%m-%d)
  END=$(date +%Y-%m-%d)
else
  START=$(date -d "$DAYS days ago" +%Y-%m-%d)
  END=$(date +%Y-%m-%d)
fi

curl -s -X POST "https://api.searchads.apple.com/api/v5/reports/campaigns/$CAMPAIGN_ID/adgroups/$ADGROUP_ID/keywords" \
  -H "Authorization: Bearer $ASA_ACCESS_TOKEN" \
  -H "X-AP-Context: orgId=$ASA_ORG_ID" \
  -H "Content-Type: application/json" \
  -d '{
    "startTime": "'"$START"'",
    "endTime": "'"$END"'",
    "selector": {
      "orderBy": [{"field": "impressions", "sortOrder": "DESCENDING"}],
      "pagination": {"offset": 0, "limit": 100}
    },
    "returnRowTotals": true
  }' | jq '.data.reportingDataResponse.row[] | {
    keyword: .metadata.keyword,
    matchType: .metadata.matchType,
    bid: .metadata.bidAmount.amount,
    impressions: .total.impressions,
    taps: .total.taps,
    installs: .total.installs,
    spend: .total.localSpend.amount,
    cpa: (if .total.installs > 0 then ((.total.localSpend.amount | tonumber) / .total.installs | . * 100 | round / 100) else null end)
  }'
```

## Automation

### weekly-optimization.sh

The graduate-and-negate cycle (SKILL.md Rules 4 and 7) as a script. Surfaces candidates; pushing them is a separate, confirmed step (`confirm_before_push`).

```bash
#!/usr/bin/env bash
set -euo pipefail

# SECURITY MANIFEST:
# Environment variables accessed: ASA_ACCESS_TOKEN, ASA_ORG_ID
# External endpoints called: https://api.searchads.apple.com/api/v5/campaigns, /reports/campaigns/{id}/searchterms
# Local files read: none
# Local files written: ~/Clawic/data/apple-search-ads/reports/weekly-{date}.txt

: "${ASA_ACCESS_TOKEN:?Set ASA_ACCESS_TOKEN}"
: "${ASA_ORG_ID:?Set ASA_ORG_ID}"

TARGET_CPA="${1:?Usage: $0 <target_cpa>}"   # target CPA in account currency; gates below derive from it

OUTPUT_DIR="${HOME}/Clawic/data/apple-search-ads/reports"
mkdir -p "$OUTPUT_DIR"

DATE=$(date +%Y-%m-%d)
OUTPUT_FILE="$OUTPUT_DIR/weekly-$DATE.txt"

# 7-day window ending 2 days back — newer rows are provisional (measurement.md)
if [[ "$OSTYPE" == "darwin"* ]]; then
  START=$(date -v-9d +%Y-%m-%d)
  END=$(date -v-2d +%Y-%m-%d)
else
  START=$(date -d "9 days ago" +%Y-%m-%d)
  END=$(date -d "2 days ago" +%Y-%m-%d)
fi

{
echo "Apple Search Ads weekly optimization — $DATE (window $START..$END, target CPA $TARGET_CPA)"

CAMPAIGNS=$(curl -s "https://api.searchads.apple.com/api/v5/campaigns" \
  -H "Authorization: Bearer $ASA_ACCESS_TOKEN" \
  -H "X-AP-Context: orgId=$ASA_ORG_ID" \
  | jq -r '.data[] | select(.status == "ENABLED") | "\(.id)\t\(.name)"')

while IFS=$'\t' read -r CAMPAIGN_ID CAMPAIGN_NAME; do
  [ -n "$CAMPAIGN_ID" ] || continue
  echo ""
  echo "Campaign: $CAMPAIGN_NAME ($CAMPAIGN_ID)"

  SEARCH_TERMS=$(curl -s -X POST "https://api.searchads.apple.com/api/v5/reports/campaigns/$CAMPAIGN_ID/searchterms" \
    -H "Authorization: Bearer $ASA_ACCESS_TOKEN" \
    -H "X-AP-Context: orgId=$ASA_ORG_ID" \
    -H "Content-Type: application/json" \
    -d '{
      "startTime": "'"$START"'",
      "endTime": "'"$END"'",
      "selector": {
        "conditions": [{"field": "impressions", "operator": "GREATER_THAN", "values": ["10"]}],
        "orderBy": [{"field": "impressions", "sortOrder": "DESCENDING"}],
        "pagination": {"offset": 0, "limit": 200}
      }
    }')

  # Graduates — Rule 4: >=2 installs AND CPA <= target
  echo "  Graduate to exact (and negate at the source):"
  echo "$SEARCH_TERMS" | jq -r --argjson t "$TARGET_CPA" '.data.reportingDataResponse.row[] |
    select(.total.installs >= 2) |
    select((.total.localSpend.amount | tonumber) / .total.installs <= $t) |
    "    - \(.metadata.searchTermText) (CPA: \((.total.localSpend.amount | tonumber) / .total.installs * 100 | round / 100), installs: \(.total.installs))"'

  # Spend gate — Rule 7: spend >= 2x target CPA with 0 installs
  echo "  Spend-gate breaches (cut bid 30-50% or pause, negate if off-intent):"
  echo "$SEARCH_TERMS" | jq -r --argjson t "$TARGET_CPA" '.data.reportingDataResponse.row[] |
    select(.total.installs == 0) |
    select((.total.localSpend.amount | tonumber) >= 2 * $t) |
    "    - \(.metadata.searchTermText) (spend: \(.total.localSpend.amount), 0 installs)"'
done <<< "$CAMPAIGNS"
} | tee "$OUTPUT_FILE"

echo "Report saved to: $OUTPUT_FILE"
```

## Setup Scripts

### init-workspace.sh

Initialize the workspace structure.

```bash
#!/usr/bin/env bash
set -euo pipefail

# SECURITY MANIFEST:
# Environment variables accessed: none
# External endpoints called: none
# Local files read: none
# Local files written: ~/Clawic/data/apple-search-ads/*

BASE_DIR="${HOME}/Clawic/data/apple-search-ads"

mkdir -p "$BASE_DIR"/{campaigns,reports,scripts}

# One-time migration hint from pre-namespace locations
for OLD in "${HOME}/apple-search-ads" "${HOME}/clawic/apple-search-ads"; do
  if [[ -d "$OLD" ]]; then
    echo "Found data at old location $OLD — move its contents to $BASE_DIR"
  fi
done

# Create initial memory file (full format: memory-template.md)
if [[ ! -f "$BASE_DIR/memory.md" ]]; then
  cat > "$BASE_DIR/memory.md" << EOF
# Apple Search Ads Memory

## Status
status: ongoing
last: $(date +%Y-%m-%d)
integration: pending

## Apps
<!-- Add your apps here -->

## Active Campaigns
<!-- Track your campaigns here -->

## Learnings
<!-- What's working, what's not -->

---
*Updated: $(date +%Y-%m-%d)*
EOF
fi

echo "Workspace initialized at $BASE_DIR"
echo ""
echo "Next steps:"
echo "1. Set environment variables (ASA_CLIENT_ID, etc.)"
echo "2. Run ./scripts/get-token.sh to test authentication"
echo "3. Run ./scripts/list-campaigns.sh to see your campaigns"
```

## Usage Examples

```bash
# Setup
export ASA_CLIENT_ID="..."
export ASA_TEAM_ID="..."
export ASA_KEY_ID="..."
export ASA_ORG_ID="..."
export ASA_PRIVATE_KEY_FILE="$HOME/.secrets/asa.p8"
export ASA_ACCESS_TOKEN=$(./get-token.sh)

# List campaigns
./list-campaigns.sh

# Get yesterday's report
./daily-report.sh

# Get search terms for campaign 12345
./search-terms-report.sh 12345 7

# Add keyword to campaign 12345, adgroup 67890
./add-keywords.sh 12345 67890 "meditation app" EXACT 2.00

# Add negative keyword
./add-negatives.sh 12345 "free meditation"

# Run weekly optimization (target CPA $6 — yours comes from LTV / ltv_divisor)
./weekly-optimization.sh 6
```
