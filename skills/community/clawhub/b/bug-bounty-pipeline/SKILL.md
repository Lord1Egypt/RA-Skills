---
name: bug-bounty-pipeline
description: Automated Hunter-Killer pipeline — BlackArch recon + CVE-MCP enrichment → human-verified exploits → bug bounty payouts. Orchestrates the full vulnerability discovery-to-payout workflow.
homepage: https://github.com/nousresearch/argus
metadata:
  openclaw:
    requires:
      bins: ["nmap", "curl", "jq", "python3"]
      mcps: ["cve-mcp", "pentester-mcp", "aynops"]
      optional_bins: ["openvas", "zap", "nikto", "wapiti", "nuclei", "sqlmap", "theHarvester", "subfinder", "amass"]
    os: ["linux"]
---

# Bug Bounty Pipeline

Automated Hunter-Killer Loop for vulnerability discovery and bug bounty payouts. Runs BlackArch reconnaissance and scanning tools against in-scope targets, enriches findings with CVE-MCP data, and triages candidates for manual exploitation. Designed for the ARGUS platform — 2800+ BlackArch tools + CVE-MCP + pentester-mcp + aynops + netmcp.

**Macro thesis:** The global AI arms race (US vs China), EU AI Act enforcement (Aug 2026), NIS2 mandates, and explosive AI agent adoption create a target-rich environment. Every corporate AI deployment is a potential bounty. This pipeline turns that chaos into income.

## Hunter-Killer Architecture

```
┌─────────────────────────────────────────────────────┐
│              HUNTER-KILLER LOOP                      │
│                                                     │
│  TIER 1: Recon        theHarvester, amass, subfinder│
│     ↓  (auto)         5-10 min/target               │
│  TIER 2: Scan         Nmap, OpenVAS, Nikto          │
│     ↓  (auto)         15-45 min/target               │
│  TIER 3: Web App      ZAP, nuclei, Wapiti           │
│     ↓  (auto)         30-120 min/target              │
│  TIER 4: Enrich       CVE-MCP, pentester-mcp        │
│     ↓  (auto)         <1 min/finding                 │
│  TIER 5: EXPLOIT      MANUAL (human creativity)      │
│     ↓                 30min-8h/finding               │
│  TIER 6: SUBMIT       Report → Platform → $$$        │
│                                                     │
│  Auto finds targets → Human exploits → Payout        │
└─────────────────────────────────────────────────────┘
```

## Prerequisites

- ARGUS host with BlackArch tools installed
- CVE-MCP, pentester-mcp, aynops MCP servers running
- Registered on at least one bug bounty platform (Intigriti recommended)
- Python 3.9+ with `requests`, `jinja2` installed

## Platforms

| Platform | Competition | Best For | Min Bounty | Region |
|----------|------------|----------|------------|--------|
| **Intigriti** ⭐ | Low (100K) | Start here | €50-150 | EU |
| YesWeHack | Low (150K) | EU programs | €50-200 | EU |
| HackerOne | High (2M) | Broadest scope | $50-150 | Global |
| Bugcrowd | Medium (500K) | Enterprise | $100-500 | Global |

**Start with Intigriti** — lowest competition, EU data residency, Swedish/EU programs.

## Tier 1: Recon (Automated)

Discover targets and subdomains:

```bash
#!/bin/bash
# tier1-recon.sh — Target discovery
# Usage: ./tier1-recon.sh example.com

TARGET="${1:?Usage: $0 <domain>}"
OUTDIR="$HOME/App/domains/argus/reports/bounty/$(date +%Y%m%d-%H%M%S)-$TARGET"
mkdir -p "$OUTDIR"

echo "=== TIER 1: Reconnaissance ==="
echo "Target: $TARGET"
echo "Output: $OUTDIR"
echo ""

# Subdomain enumeration
echo "[1/4] Subdomain discovery (amass + subfinder)..."
amass enum -passive -d "$TARGET" -o "$OUTDIR/subdomains-amass.txt" 2>/dev/null
subfinder -d "$TARGET" -o "$OUTDIR/subdomains-subfinder.txt" 2>/dev/null
cat "$OUTDIR/subdomains-amass.txt" "$OUTDIR/subdomains-subfinder.txt" 2>/dev/null | sort -u > "$OUTDIR/subdomains-all.txt"
echo "  Found: $(wc -l < "$OUTDIR/subdomains-all.txt" 2>/dev/null || echo 0) subdomains"

# DNS enumeration
echo "[2/4] DNS records..."
for sub in $(head -50 "$OUTDIR/subdomains-all.txt" 2>/dev/null); do
  dig +short A "$sub" 2>/dev/null
  dig +short AAAA "$sub" 2>/dev/null
done | sort -u > "$OUTDIR/dns-records.txt"
echo "  Found: $(wc -l < "$OUTDIR/dns-records.txt" 2>/dev/null || echo 0) DNS records"

# WHOIS lookup
echo "[3/4] WHOIS..."
whois "$TARGET" > "$OUTDIR/whois.txt" 2>/dev/null

# Technology stack detection
echo "[4/4] Technology stack..."
whatweb "$TARGET" --log-json="$OUTDIR/tech-stack.json" 2>/dev/null

echo ""
echo "=== Tier 1 Complete ==="
echo "Subdomains: $(wc -l < "$OUTDIR/subdomains-all.txt")"
echo "DNS records: $(wc -l < "$OUTDIR/dns-records.txt")"
echo "Tech stack: $OUTDIR/tech-stack.json"
```

## Tier 2: Network Scan (Automated)

Port and service discovery on live targets:

```bash
#!/bin/bash
# tier2-scan.sh — Network vulnerability scanning
# Usage: ./tier2-scan.sh targets.txt

TARGETS_FILE="${1:?Usage: $0 <targets.txt>}"
OUTDIR="$HOME/App/domains/argus/reports/bounty/$(date +%Y%m%d-%H%M%S)-scan"
mkdir -p "$OUTDIR"

echo "=== TIER 2: Network Scanning ==="
echo "Targets: $(wc -l < "$TARGETS_FILE")"
echo "Output: $OUTDIR"
echo ""

# Nmap — quick port scan
echo "[1/4] Nmap port scan..."
while IFS= read -r target; do
  [ -z "$target" ] && continue
  echo "  Scanning: $target"
  nmap -sV -sC -T4 -p- --min-rate 1000 "$target" -oN "$OUTDIR/nmap-$target.txt" 2>/dev/null
done < "$TARGETS_FILE"

# Nmap — vulnerability scripts
echo "[2/4] Nmap vuln scripts..."
while IFS= read -r target; do
  [ -z "$target" ] && continue
  nmap --script vuln "$target" -oN "$OUTDIR/nmap-vuln-$target.txt" 2>/dev/null
done < "$TARGETS_FILE"

# OpenVAS (if installed)
echo "[3/4] OpenVAS scan..."
if command -v gvm-cli &>/dev/null; then
  while IFS= read -r target; do
    [ -z "$target" ] && continue
    gvm-cli socket --xml "<create_task>...</create_task>" 2>/dev/null
  done < "$TARGETS_FILE"
else
  echo "  OpenVAS not installed — skipping"
fi

# Nikto web server scan
echo "[4/4] Nikto web server scan..."
while IFS= read -r target; do
  [ -z "$target" ] && continue
  nikto -h "$target" -Format txt -o "$OUTDIR/nikto-$target.txt" 2>/dev/null
done < "$TARGETS_FILE"

echo ""
echo "=== Tier 2 Complete ==="
```

## Tier 3: Web Application Scan (Automated)

Deep web app vulnerability scanning:

```bash
#!/bin/bash
# tier3-webapp.sh — Web application scanning
# Usage: ./tier3-webapp.sh urls.txt

URLS_FILE="${1:?Usage: $0 <urls.txt>}"
OUTDIR="$HOME/App/domains/argus/reports/bounty/$(date +%Y%m%d-%H%M%S)-webapp"
mkdir -p "$OUTDIR"

echo "=== TIER 3: Web Application Scanning ==="
echo "URLs: $(wc -l < "$URLS_FILE")"
echo "Output: $OUTDIR"
echo ""

# ZAP baseline scan (fast)
echo "[1/5] ZAP baseline scan..."
while IFS= read -r url; do
  [ -z "$url" ] && continue
  echo "  Scanning: $url"
  zap-baseline.py -t "$url" -r "$OUTDIR/zap-baseline-$(echo "$url" | md5sum | cut -c1-8).html" 2>/dev/null
done < "$URLS_FILE"

# Nuclei templates
echo "[2/5] Nuclei template scan..."
while IFS= read -r url; do
  [ -z "$url" ] && continue
  echo "  Scanning: $url"
  nuclei -u "$url" -o "$OUTDIR/nuclei-$(echo "$url" | md5sum | cut -c1-8).txt" 2>/dev/null
done < "$URLS_FILE"

# Wapiti
echo "[3/5] Wapiti scan..."
while IFS= read -r url; do
  [ -z "$url" ] && continue
  echo "  Scanning: $url"
  wapiti -u "$url" -f txt -o "$OUTDIR/wapiti-$(echo "$url" | md5sum | cut -c1-8)" 2>/dev/null
done < "$URLS_FILE"

# Technology fingerprinting
echo "[4/5] Technology fingerprinting..."
while IFS= read -r url; do
  [ -z "$url" ] && continue
  echo "  Fingerprinting: $url"
  whatweb "$url" --log-json="$OUTDIR/whatweb-$(echo "$url" | md5sum | cut -c1-8).json" 2>/dev/null
done < "$URLS_FILE"

# Wayback machine URLs
echo "[5/5] Historical URL discovery..."
while IFS= read -r url; do
  [ -z "$url" ] && continue
  domain=$(echo "$url" | sed 's|https\?://||' | cut -d/ -f1)
  curl -s "https://web.archive.org/cdx/search/cdx?url=*.$domain/*&output=text&fl=original&collapse=urlkey" 2>/dev/null | \
    head -200 > "$OUTDIR/wayback-$domain.txt"
  echo "  $domain: $(wc -l < "$OUTDIR/wayback-$domain.txt") historical URLs"
done < "$URLS_FILE"

echo ""
echo "=== Tier 3 Complete ==="
```

## Tier 4: CVE Enrichment (Automated)

Enrich findings with vulnerability intelligence:

```bash
#!/bin/bash
# tier4-enrich.sh — CVE enrichment
# Usage: ./tier4-enrich.sh findings-dir/

FINDINGS_DIR="${1:?Usage: $0 <findings-directory>}"
OUTDIR="$FINDINGS_DIR/enriched"
mkdir -p "$OUTDIR"

echo "=== TIER 4: CVE Enrichment ==="

# Extract CVE IDs from all scan outputs
echo "[1/3] Extracting CVE references..."
grep -rohE 'CVE-[0-9]{4}-[0-9]+' "$FINDINGS_DIR" 2>/dev/null | sort -u > "$OUTDIR/cve-ids.txt"
echo "  Found: $(wc -l < "$OUTDIR/cve-ids.txt") unique CVEs"

# Enrich with CVE-MCP
echo "[2/3] CVE-MCP enrichment..."
while IFS= read -r cve_id; do
  [ -z "$cve_id" ] && continue

  result=$(curl -s -X POST "http://localhost:8765/cve-mcp/lookup" \
    -H "Content-Type: application/json" \
    -d "{\"cve_id\": \"$cve_id\"}" 2>/dev/null)

  if echo "$result" | jq -e '.cvss_score' >/dev/null 2>&1; then
    score=$(echo "$result" | jq -r '.cvss_score')
    severity=$(echo "$result" | jq -r '.severity')
    description=$(echo "$result" | jq -r '.description // "N/A"')

    echo "$cve_id | CVSS $score | $severity | $description" >> "$OUTDIR/cve-enriched.txt"

    # Flag critical/high for immediate attention
    if echo "$score" | awk '{exit !($1 >= 7.0)}'; then
      echo "  🔴 $cve_id (CVSS $score — $severity)" >> "$OUTDIR/CRITICAL.txt"
    fi
  fi
done < "$OUTDIR/cve-ids.txt"

# EPSS enrichment
echo "[3/3] EPSS exploitation probability..."
python3 - "$OUTDIR/cve-ids.txt" "$OUTDIR" << 'PYEOF'
import sys, json, urllib.request

cve_file = sys.argv[1]
outdir = sys.argv[2]

with open(cve_file) as f:
    cves = [line.strip() for line in f if line.strip()]

if cves:
    cve_list = ",".join(cves[:50])  # EPSS API limit
    url = f"https://api.first.org/data/v1/epss?cve={cve_list}"
    try:
        with urllib.request.urlopen(url, timeout=10) as resp:
            data = json.loads(resp.read())
            with open(f"{outdir}/epss-scores.json", "w") as out:
                json.dump(data, out, indent=2)

            for item in data.get("data", []):
                epss = float(item.get("epss", 0))
                percentile = float(item.get("percentile", 0))
                if epss > 0.01:  # >1% exploitation probability
                    print(f"  ⚡ {item['cve']} — EPSS {epss:.4f} (top {percentile:.1f}%)")
    except Exception as e:
        print(f"  EPSS API error: {e}")
PYEOF

echo ""
echo "=== Tier 4 Complete ==="
echo "Critical findings: $(wc -l < "$OUTDIR/CRITICAL.txt" 2>/dev/null || echo 0)"
```

## Tier 5: Manual Exploitation (Human)

This is where the money is. Automation finds candidates — human creativity exploits them.

```bash
#!/bin/bash
# tier5-triage.sh — Candidate triage for manual review
# Sorts findings by estimated bounty value

FINDINGS_DIR="${1:-$HOME/App/domains/argus/reports/bounty/latest}"
OUTDIR="$FINDINGS_DIR/triage"
mkdir -p "$OUTDIR"

echo "=== TIER 5: Candidate Triage ==="

# Priority 1: RCE / Auth Bypass (highest payout)
echo "--- PRIORITY 1: RCE / Auth Bypass ---"
grep -riE "remote.code.execution|RCE|auth.bypass|privilege.escalation" "$FINDINGS_DIR" 2>/dev/null | \
  head -20 > "$OUTDIR/p1-critical.txt"

# Priority 2: SQLi / SSRF ($1K-$5K)
echo "--- PRIORITY 2: SQLi / SSRF ---"
grep -riE "SQL.injection|SSRF|server.side.request.forgery" "$FINDINGS_DIR" 2>/dev/null | \
  head -20 > "$OUTDIR/p2-high.txt"

# Priority 3: XSS / CSRF ($50-$500)
echo "--- PRIORITY 3: XSS / CSRF ---"
grep -riE "XSS|cross.site.scripting|CSRF" "$FINDINGS_DIR" 2>/dev/null | \
  head -20 > "$OUTDIR/p3-medium.txt"

# Priority 4: Info Disclosure / Misconfig ($50-$300)
echo "--- PRIORITY 4: Info Disclosure ---"
grep -riE "information.disclosure|misconfig|default.credentials" "$FINDINGS_DIR" 2>/dev/null | \
  head -20 > "$OUTDIR/p4-low.txt"

echo ""
echo "=== Triage Summary ==="
echo "P1 (RCE/Auth): $(wc -l < "$OUTDIR/p1-critical.txt")"
echo "P2 (SQLi/SSRF): $(wc -l < "$OUTDIR/p2-high.txt")"
echo "P3 (XSS/CSRF): $(wc -l < "$OUTDIR/p3-medium.txt")"
echo "P4 (Info/Misconfig): $(wc -l < "$OUTDIR/p4-low.txt")"
echo ""
echo "Next: Review P1 candidates first → manual exploit → submit report"
```

## Tier 6: Report & Submit

Generate professional vulnerability reports and submit to platforms:

```bash
#!/bin/bash
# tier6-submit.sh — Generate report and submit
# Usage: ./tier6-submit.sh finding-detail.txt target.com "RCE via Unvalidated Input"

FINDING_FILE="${1:?Usage: $0 <finding.txt> <target> <title>}"
TARGET="${2:?}"
TITLE="${3:?}"
OUTDIR="$HOME/App/domains/argus/reports/bounty/submitted/$(date +%Y%m%d-%H%M%S)"
mkdir -p "$OUTDIR"

REPORT="$OUTDIR/report.md"

cat > "$REPORT" << 'EOF'
# Vulnerability Report

**Title:** TITLE_PLACEHOLDER
**Target:** TARGET_PLACEHOLDER
**Date:** DATE_PLACEHOLDER
**Severity:** SEVERITY_PLACEHOLDER
**CVSS Score:** CVSS_PLACEHOLDER

---

## Summary
(One-paragraph summary of the vulnerability and its impact)

## Steps to Reproduce

1. 
2. 
3. 

## Proof of Concept

```

(Include curl commands, screenshots, or code snippets)

```

## Impact
(What can an attacker achieve? Data access? Code execution? Privilege escalation?)

## Remediation
(Suggested fix — be specific)

## References
- CVE-XXXX-XXXXX
- OWASP: 

---

**Discovered by:** 1Beekeeper
**Disclosure:** Responsible disclosure per platform policy
EOF

# Replace placeholders
sed -i "s/TITLE_PLACEHOLDER/$TITLE/g" "$REPORT"
sed -i "s/TARGET_PLACEHOLDER/$TARGET/g" "$REPORT"
sed -i "s/DATE_PLACEHOLDER/$(date -u +%Y-%m-%dT%H:%M:%SZ)/g" "$REPORT"

echo "Report generated: $REPORT"
echo ""
echo "=== Submission Checklist ==="
echo "☐ Report follows platform template"
echo "☐ PoC is reproducible"
echo "☐ No data exfiltration during testing"
echo "☐ All requests within scope"
echo "☐ Rate limits respected"
echo "☐ Screenshots attached"
echo "☐ CVE references included"
echo ""
echo "Submit on your bug bounty platform dashboard."
```

## Full Pipeline Orchestrator

Run the complete Hunter-Killer Loop:

```bash
#!/bin/bash
# hunter-killer.sh — Full pipeline orchestrator
# Usage: ./hunter-killer.sh targets.txt

TARGETS_FILE="${1:?Usage: $0 <targets.txt>}"
PIPELINE_DIR="$HOME/App/domains/argus/reports/bounty"
RUN_ID="hk-$(date +%Y%m%d-%H%M%S)"
RUN_DIR="$PIPELINE_DIR/$RUN_ID"
mkdir -p "$RUN_DIR"

echo "╔══════════════════════════════════════════╗"
echo "║   HUNTER-KILLER PIPELINE — $RUN_ID  ║"
echo "╚══════════════════════════════════════════╝"
echo ""

# Extract URLs from targets file
grep -E '^https?://' "$TARGETS_FILE" > "$RUN_DIR/urls.txt" 2>/dev/null

# Tier 1: Recon
echo "▶ Tier 1: Reconnaissance"
bash tier1-recon.sh "$(head -1 "$TARGETS_FILE" | sed 's|https\?://||' | cut -d/ -f1)" 2>&1 | tail -1

# Tier 2: Network Scan
echo "▶ Tier 2: Network Scanning"
bash tier2-scan.sh "$TARGETS_FILE" 2>&1 | tail -1

# Tier 3: Web App Scan
echo "▶ Tier 3: Web Application Scanning"
bash tier3-webapp.sh "$RUN_DIR/urls.txt" 2>&1 | tail -1

# Tier 4: CVE Enrichment
echo "▶ Tier 4: CVE Enrichment"
bash tier4-enrich.sh "$RUN_DIR" 2>&1 | tail -1

# Tier 5: Triage
echo "▶ Tier 5: Candidate Triage"
bash tier5-triage.sh "$RUN_DIR" 2>&1 | tail -5

echo ""
echo "╔══════════════════════════════════════════╗"
echo "║   PIPELINE COMPLETE                      ║"
echo "║   Review candidates in: $RUN_DIR     ║"
echo "║   Start manual exploitation on P1 hits   ║"
echo "╚══════════════════════════════════════════╝"
```

## Integration with Ash (OpenClaw)

Ash monitors the pipeline and flags opportunities:

```bash
# Add to Ash's HEARTBEAT.md or cron jobs:

# Check pipeline output for high-value findings
PIPELINE_DIR="$HOME/App/domains/argus/reports/bounty"
LATEST=$(ls -t "$PIPELINE_DIR" | head -1)
CRITICAL_COUNT=$(wc -l < "$PIPELINE_DIR/$LATEST/triage/p1-critical.txt" 2>/dev/null || echo 0)
HIGH_COUNT=$(wc -l < "$PIPELINE_DIR/$LATEST/triage/p2-high.txt" 2>/dev/null || echo 0)

if [ "$CRITICAL_COUNT" -gt 0 ]; then
  echo "🚨 $CRITICAL_COUNT CRITICAL findings ready for manual review in $LATEST"
fi
if [ "$HIGH_COUNT" -gt 0 ]; then
  echo "⚡ $HIGH_COUNT HIGH-priority findings in $LATEST"
fi
```

## Usage Patterns

### Daily Hunter-Killer Run

1. **Morning:** Run Tier 1-2 on new targets (15 min)
2. **Midday:** Run Tier 3-4 on promising targets (30 min)
3. **Evening:** Run Tier 5 triage — review P1 candidates (30 min)
4. **Weekly:** Manual exploitation on top candidates (2-4h)

### Target Discovery

- **Platform scope pages:** Download program scope files from Intigriti/HackerOne
- **Shodan/Censys:** Search for specific tech stacks "nginx 1.18" → find targets
- **Google dorks:** `site:example.com inurl:admin` → find juicy endpoints
- **Wayback Machine:** Historical URLs often reveal old/debug endpoints
- **GitHub dorking:** `org:target "API_KEY" "secret"` → find leaked credentials

### Continuous Monitoring

- **New program alerts:** Ash monitors for new bug bounty programs
- **New CVE alerts:** When critical CVEs drop, immediately scan targets for that vuln
- **Tech stack changes:** Monitor targets for new deployments = new attack surface

## Pricing Tiers

### Free (DIY Pipeline)

- All shell scripts and pipeline code
- Basic CVE enrichment
- Manual triage only
- Community support

### Pro ($29/month)

- Auto-triage with ML scoring
- Historical finding correlation ("this target had XSS last month → likely still vulnerable")
- Custom exploit templates per vuln type
- Priority CVE-MCP enrichment
- Monthly target discovery pack

### Enterprise ($99/month)

- All Pro features
- Automated target discovery (Shodan, Censys, Google dorks)
- Continuous monitoring for new programs and CVEs
- Team dashboard with finding-to-payout tracking
- ZK-Bankir integration: auto-track bounty income

## Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `BOUNTY_PLATFORM` | `intigriti` | Primary platform (intigriti, hackerone, bugcrowd, yeswehack) |
| `PIPELINE_DIR` | `~/App/domains/argus/reports/bounty` | Pipeline output directory |
| `MAX_TARGETS_PER_RUN` | `10` | Max targets per pipeline execution |
| `SCAN_RATE_LIMIT` | `3` | Requests per second |
| `CVE_MCP_URL` | `http://localhost:8765/cve-mcp` | CVE-MCP endpoint |
| `PENTEST_MCP_URL` | `http://localhost:8765/pentest-mcp` | Pentest-MCP endpoint |
| `ZKBANKIR_API` | `http://localhost:3000/api/v1` | ZK-Bankir API for tracking payouts |

## Security & Legal

- **Scope whitelist is absolute.** Never scan outside program scope.
- **Rate limiting mandatory.** Max 2-5 req/s per target.
- **No destructive testing.** Never run sqlmap without `--batch --level=1 --risk=1`.
- **No data exfiltration.** Even from vulnerable systems.
- **Audit trail.** All requests logged for responsible disclosure.
- **Platform ToS compliance.** Each platform has unique rules — read them.

## BlackArch Tools Used

| Tool | Tier | Purpose |
|------|------|---------|
| amass | 1 | Subdomain enumeration |
| subfinder | 1 | Passive subdomain discovery |
| theHarvester | 1 | OSINT email/subdomain |
| nmap | 2 | Port + service discovery |
| nikto | 2 | Web server scanning |
| OpenVAS | 2 | Full vulnerability assessment |
| ZAP | 3 | Web app scanning |
| nuclei | 3 | Template-based scanning |
| Wapiti | 3 | Web app vulnerability scanning |
| whatweb | 1,3 | Technology fingerprinting |
| CVE-MCP | 4 | CVE lookup + severity scoring |

## Related Skills

- **vulnerability-scanner** — Full vulnerability assessment (use with this pipeline)
- **cve-tracker** — CVE intelligence (enrichment source)
- **osint-investigator** — Target discovery and OSINT
- **incident-responder** — If a finding escalates to incident
- **zk-bankir-monitor** — Track bounty payouts in ZK-Bankir

---

_Generated: 2026-07-04 | ARGUS Domain | Hunter-Killer Pipeline v1.0_
