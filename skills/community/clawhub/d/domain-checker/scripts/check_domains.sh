#!/usr/bin/env bash
# Domain availability checker — cross-verifies whois + DNS NS records
# Usage: check_domains.sh domain1.com domain2.com ...
# Or:    echo "domain1.com domain2.com" | check_domains.sh
# Output: one line per domain: ✅ AVAILABLE / ❌ TAKEN / ❓ UNKNOWN

set -uo pipefail

# Colors (disabled if not a terminal)
if [ -t 1 ]; then
  GREEN='\033[0;32m'; RED='\033[0;31m'; YELLOW='\033[0;33m'; NC='\033[0m'
else
  GREEN=''; RED=''; YELLOW=''; NC=''
fi

check_one() {
  local domain="$1"
  local tld="${domain##*.}"
  
  # --- Method 1: whois ---
  local whois_out
  whois_out=$(whois "$domain" 2>/dev/null || true)
  
  local created=""
  local not_found=""
  
  # Different TLDs use different "not found" strings
  case "$tld" in
    com|net)
      not_found=$(echo "$whois_out" | grep -iE "No match for|NOT FOUND" | head -1) ;;
    org)
      not_found=$(echo "$whois_out" | grep -iE "NOT FOUND|No match" | head -1) ;;
    io)
      not_found=$(echo "$whois_out" | grep -iE "NOT FOUND|is available|No match" | head -1) ;;
    ai)
      not_found=$(echo "$whois_out" | grep -iE "NOT FOUND|No Data Found|No Object Found" | head -1) ;;
    so)
      not_found=$(echo "$whois_out" | grep -iE "NOT FOUND|No Object Found|AVAILABLE" | head -1) ;;
    *)
      not_found=$(echo "$whois_out" | grep -iE "No match|NOT FOUND|No Data Found|No entries found|AVAILABLE|No Object Found" | head -1) ;;
  esac
  
  created=$(echo "$whois_out" | grep -iE "^[[:space:]]*(Creation Date|created|Registration Time):" | head -1 | sed 's/^[[:space:]]*//')
  
  # --- Method 2: DNS NS records ---
  local ns=""
  ns=$(dig +short "$domain" NS 2>/dev/null | head -1)
  
  # --- Method 3: DNS A record (fallback signal) ---
  local a_record=""
  a_record=$(dig +short "$domain" A 2>/dev/null | head -1)
  
  # --- Cross-verify and decide ---
  if [ -n "$created" ]; then
    # whois shows creation date = definitely taken
    printf "${RED}❌ %-30s TAKEN    %s${NC}\n" "$domain" "$created"
  elif [ -n "$not_found" ] && [ -z "$ns" ]; then
    # whois says not found AND no NS records = very likely available
    printf "${GREEN}✅ %-30s AVAILABLE${NC}\n" "$domain"
  elif [ -n "$not_found" ] && [ -n "$ns" ]; then
    # whois says not found but has NS = conflicting signals, likely taken
    printf "${YELLOW}⚠️  %-30s LIKELY TAKEN (has NS: %s)${NC}\n" "$domain" "$ns"
  elif [ -n "$ns" ] || [ -n "$a_record" ]; then
    # No whois creation date but has DNS records = likely taken
    printf "${YELLOW}⚠️  %-30s LIKELY TAKEN (has DNS records)${NC}\n" "$domain"
  else
    # No whois data, no DNS = unknown (whois may have failed)
    printf "${YELLOW}❓ %-30s UNKNOWN  (whois returned no data — check manually)${NC}\n" "$domain"
  fi
}

# Read domains from args or stdin
domains=()
if [ $# -gt 0 ]; then
  domains=("$@")
else
  while IFS= read -r line; do
    for word in $line; do
      domains+=("$word")
    done
  done
fi

if [ ${#domains[@]} -eq 0 ]; then
  echo "Usage: check_domains.sh domain1.com domain2.com ..."
  echo "   or: echo 'domain1.com domain2.com' | check_domains.sh"
  exit 1
fi

echo "Checking ${#domains[@]} domain(s)..."
echo "Method: whois + DNS NS + DNS A cross-verification"
echo "────────────────────────────────────────────────────"

available=0
taken=0
unknown=0

for d in "${domains[@]}"; do
  result=$(check_one "$d")
  echo -e "$result"
  if echo "$result" | grep -q "AVAILABLE"; then
    ((available++))
  elif echo "$result" | grep -q "TAKEN"; then
    ((taken++))
  else
    ((unknown++))
  fi
  # Rate limit: avoid whois server throttling
  sleep 1
done

echo "────────────────────────────────────────────────────"
echo "Summary: ${#domains[@]} checked — ✅ $available available, ❌ $taken taken, ❓ $unknown unknown"
