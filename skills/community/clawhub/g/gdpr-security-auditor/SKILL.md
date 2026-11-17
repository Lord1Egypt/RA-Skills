---
name: gdpr-security-auditor
description: Technical GDPR compliance audit — data mapping, encryption verification, access control review, data retention analysis, DPIA templates, and cross-border transfer assessment. Distinct from gdpr-checker (financial focus).
homepage: https://github.com/nousresearch/argus
metadata:
  openclaw:
    requires:
      bins: ["curl", "jq", "grep", "find", "openssl"]
      mcps: ["aynops"]
      optional_bins: ["lynis", "nmap", "trivy"]
    os: ["linux"]
---

# GDPR Security Auditor

Technical GDPR compliance audit for infrastructure and applications. Maps data flows, verifies encryption at rest and in transit, reviews access controls, analyzes data retention, and generates Data Protection Impact Assessments (DPIAs). Focuses on the technical security requirements of GDPR Articles 25, 32, 33, 34, and 35 — distinct from gdpr-checker which focuses on financial application compliance.

Runs on ARGUS infrastructure. Professional report at $49/report.

## Prerequisites

- **ARGUS host** with shell access
- **aynops** MCP available for SSL/TLS verification
- `curl`, `jq`, `grep`, `find`, `openssl` on PATH
- Target system access (SSH or local) for in-depth audit

## Infrastructure

| Component | Location | Purpose |
|-----------|----------|---------|
| ARGUS host | local | Audit orchestration and report generation |
| aynops | localhost MCP | SSL/TLS certificate verification |
| BlackArch tools | `/usr/share/` | lynis, nmap, trivy (optional) |

## GDPR Articles Covered

| Article | Focus | Audit Check |
|---------|-------|-------------|
| Art. 5 | Data minimization, storage limitation | Data field audit, retention review |
| Art. 25 | Data protection by design and default | Privacy-by-design assessment |
| Art. 28 | Data processor obligations | Third-party data flow mapping |
| Art. 30 | Records of processing activities | Data processing inventory |
| Art. 32 | Security of processing | Encryption, access control, vulnerability |
| Art. 33 | Breach notification (72 hours) | Incident detection capability |
| Art. 34 | Communication to data subjects | Notification workflow readiness |
| Art. 35 | Data Protection Impact Assessment | DPIA template and guidance |
| Art. 44-49 | International data transfers | Cross-border flow analysis |

## Core Commands

### Data Processing Inventory (Art. 30)

Discover and inventory data processing activities:

```bash
AUDIT_DIR="$HOME/App/domains/argus/reports/gdpr/audit-$(date +%Y%m%d-%H%M%S)"
mkdir -p "$AUDIT_DIR"

echo "=== Data Processing Inventory ==="

# Scan for databases in common locations
echo "--- Database Discovery ---"

# PostgreSQL
if systemctl is-active --quiet postgresql 2>/dev/null; then
  echo "PostgreSQL: RUNNING" | tee -a "$AUDIT_DIR/databases.txt"
  sudo -u postgres psql -c "\l" 2>/dev/null >> "$AUDIT_DIR/postgres-databases.txt"
else
  echo "PostgreSQL: not running" | tee -a "$AUDIT_DIR/databases.txt"
fi

# MySQL/MariaDB
if systemctl is-active --quiet mariadb 2>/dev/null || systemctl is-active --quiet mysql 2>/dev/null; then
  echo "MySQL/MariaDB: RUNNING" | tee -a "$AUDIT_DIR/databases.txt"
else
  echo "MySQL/MariaDB: not running" | tee -a "$AUDIT_DIR/databases.txt"
fi

# Redis
if systemctl is-active --quiet redis 2>/dev/null; then
  echo "Redis: RUNNING" | tee -a "$AUDIT_DIR/databases.txt"
  redis-cli INFO keyspace 2>/dev/null >> "$AUDIT_DIR/redis-keyspace.txt"
else
  echo "Redis: not running" | tee -a "$AUDIT_DIR/databases.txt"
fi

# SQLite databases
echo "--- SQLite Files ---"
find / -name "*.sqlite" -o -name "*.sqlite3" -o -name "*.db" 2>/dev/null | \
  grep -v "/proc/" | grep -v "/sys/" | head -20 | \
  tee "$AUDIT_DIR/sqlite-files.txt"

# Docker volumes (potential data stores)
echo "--- Docker Volumes ---"
docker volume ls 2>/dev/null | tee "$AUDIT_DIR/docker-volumes.txt"
```

### Data Field Audit (Art. 5 — Data Minimization)

Scan for PII/sensitive data in files and databases:

```bash
AUDIT_DIR="$HOME/App/domains/argus/reports/gdpr/audit-$(date +%Y%m%d-%H%M%S)"
mkdir -p "$AUDIT_DIR"

echo "=== Data Field Audit (PII Discovery) ==="

# Scan schema files for PII patterns
SCHEMA_PATTERNS="email|phone|name|address|ssn|passport|national_id|dob|birth|gender|race|religion|health|biometric|political|criminal"

echo "--- Schema PII Patterns ---"
find /home -name "schema.rb" -o -name "schema.sql" -o -name "*.sql" 2>/dev/null | \
  while IFS= read -r file; do
    hits=$(grep -ciE "$SCHEMA_PATTERNS" "$file" 2>/dev/null || echo 0)
    if [ "$hits" -gt 0 ]; then
      echo "  [$hits hits] $file"
    fi
  done | tee "$AUDIT_DIR/pii-schema.txt"

# Scan environment/config files for plaintext secrets
echo ""
echo "--- Plaintext Secrets ---"
find /home -name ".env*" -o -name "credentials*" -o -name "secrets*" 2>/dev/null | \
  while IFS= read -r file; do
    if grep -qiE "secret|password|token|key|credential" "$file" 2>/dev/null; then
      echo "  SENSITIVE: $file (contains credential patterns)"
    fi
  done | tee "$AUDIT_DIR/plaintext-secrets.txt"

# Check log files for PII leakage
echo ""
echo "--- PII in Logs ---"
find /var/log -name "*.log" -type f 2>/dev/null | \
  while IFS= read -r log; do
    emails=$(grep -cE '[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}' "$log" 2>/dev/null || echo 0)
    ips=$(grep -cE '\b([0-9]{1,3}\.){3}[0-9]{1,3}\b' "$log" 2>/dev/null || echo 0)
    if [ "$emails" -gt 5 ] || [ "$ips" -gt 10 ]; then
      echo "  CHECK: $log ($emails emails, $ips IPs — potential PII in logs)"
    fi
  done | tee "$AUDIT_DIR/pii-in-logs.txt"
```

### Encryption Verification (Art. 32)

Verify encryption at rest, in transit, and in backups:

```bash
AUDIT_DIR="$HOME/App/domains/argus/reports/gdpr/audit-$(date +%Y%m%d-%H%M%S)"
mkdir -p "$AUDIT_DIR"

TARGET="${1:-localhost}"
echo "=== Encryption Verification ==="

# Encryption at rest
echo "--- Disk Encryption ---"
lsblk -o NAME,SIZE,TYPE,MOUNTPOINT | grep -E "crypt|LUKS" > "$AUDIT_DIR/disk-encryption.txt" 2>&1
if [ -s "$AUDIT_DIR/disk-encryption.txt" ]; then
  echo "✅ Encrypted volumes found"
  cat "$AUDIT_DIR/disk-encryption.txt"
else
  echo "❌ No LUKS/dm-crypt volumes detected — check disk encryption"
fi

# TLS/SSL verification (using aynops)
echo ""
echo "--- TLS Verification ---"
for port in 443 8443 9443; do
  echo "Port $port:"
  result=$(curl -s -X POST "http://localhost:8765/aynops/ssl" \
    -H "Content-Type: application/json" \
    -d "{\"host\": \"$TARGET\", \"port\": $port}" 2>/dev/null)
  
  if echo "$result" | jq -e '.valid_until' >/dev/null 2>&1; then
    tls_version=$(echo "$result" | jq -r '.tls_version // "unknown"')
    cipher=$(echo "$result" | jq -r '.cipher // "unknown"')
    valid_until=$(echo "$result" | jq -r '.valid_until // "unknown"')
    
    echo "  TLS: $tls_version | Cipher: $cipher | Expires: $valid_until"
    
    # TLS 1.2+ check
    if echo "$tls_version" | grep -qE "TLSv1\.[23]"; then
      echo "  ✅ TLS version acceptable"
    else
      echo "  ❌ TLS version outdated (require TLS 1.2+)"
    fi
  else
    echo "  No TLS on port $port"
  fi
done | tee "$AUDIT_DIR/tls-verification.txt"

# Database encryption
echo ""
echo "--- Database Encryption ---"
# PostgreSQL
if [ -f /etc/postgresql/postgresql.conf ]; then
  grep -i "ssl" /etc/postgresql/postgresql.conf 2>/dev/null | grep -v "^#" > "$AUDIT_DIR/db-ssl.txt"
  if grep -q "ssl = on" /etc/postgresql/postgresql.conf 2>/dev/null; then
    echo "✅ PostgreSQL SSL enabled"
  else
    echo "❌ PostgreSQL SSL not enabled"
  fi
fi

# Encryption at rest in backups
echo ""
echo "--- Backup Encryption ---"
BACKUP_LOCATIONS="/backup /var/backups /home/*/backups"
for dir in $BACKUP_LOCATIONS; do
  if [ -d "$dir" ]; then
    encrypted=$(find "$dir" -name "*.gpg" -o -name "*.enc" -o -name "*.age" 2>/dev/null | wc -l)
    total=$(find "$dir" -type f 2>/dev/null | wc -l)
    echo "  $dir: $encrypted/$total files encrypted"
  fi
done | tee "$AUDIT_DIR/backup-encryption.txt"
```

### Access Control Audit (Art. 25, 32)

Review access controls and least privilege:

```bash
AUDIT_DIR="$HOME/App/domains/argus/reports/gdpr/audit-$(date +%Y%m%d-%H%M%S)"
mkdir -p "$AUDIT_DIR"

echo "=== Access Control Audit ==="

# SSH key audit
echo "--- SSH Keys ---"
for user_home in /home/*; do
  user=$(basename "$user_home")
  if [ -f "$user_home/.ssh/authorized_keys" ]; then
    key_count=$(wc -l < "$user_home/.ssh/authorized_keys")
    echo "  User $user: $key_count authorized keys"
    
    # Check key types (ed25519 > rsa)
    rsa_keys=$(grep -c "ssh-rsa" "$user_home/.ssh/authorized_keys" 2>/dev/null || echo 0)
    ed25519_keys=$(grep -c "ssh-ed25519" "$user_home/.ssh/authorized_keys" 2>/dev/null || echo 0)
    if [ "$rsa_keys" -gt 0 ]; then
      echo "    ⚠️  $rsa_keys RSA keys (deprecated — migrate to ed25519)"
    fi
  fi
done | tee "$AUDIT_DIR/ssh-keys.txt"

# Sudo permissions
echo ""
echo "--- Sudo Access ---"
grep -v "^#" /etc/sudoers 2>/dev/null | grep -v "^$" | tee "$AUDIT_DIR/sudoers.txt"

# World-readable sensitive files
echo ""
echo "--- World-Readable Sensitive Files ---"
find /home -type f \( -name "*.env" -o -name "*.pem" -o -name "id_*" -o -name "*.key" \) -perm /o+r 2>/dev/null | \
  while IFS= read -r file; do
    echo "  ❌ WORLD-READABLE: $file"
  done | tee "$AUDIT_DIR/world-readable-sensitive.txt"

# Unused user accounts
echo ""
echo "--- Unused Accounts ---"
# Accounts with no login in 90 days
lastlog 2>/dev/null | grep -v "Never logged in" | \
  awk '{print $1, $4, $5, $6}' | tee "$AUDIT_DIR/unused-accounts.txt"

# Firewall rules
echo ""
echo "--- Firewall Rules ---"
sudo iptables -L -n -v 2>/dev/null | head -40 | tee "$AUDIT_DIR/firewall-rules.txt"

# Open ports
echo ""
echo "--- Open Ports ---"
ss -tlnp | tee "$AUDIT_DIR/open-ports.txt"
```

### Data Retention Analysis (Art. 5)

Check retention practices and identify stale data:

```bash
AUDIT_DIR="$HOME/App/domains/argus/reports/gdpr/audit-$(date +%Y%m%d-%H%M%S)"
mkdir -p "$AUDIT_DIR"

echo "=== Data Retention Analysis ==="

# Database row counts (if accessible)
echo "--- Database Retention ---"

# PostgreSQL table sizes and ages
if systemctl is-active --quiet postgresql 2>/dev/null; then
  sudo -u postgres psql -c "
    SELECT 
      schemaname || '.' || relname AS table_name,
      n_live_tup AS estimated_rows,
      pg_size_pretty(pg_total_relation_size(relid)) AS total_size
    FROM pg_stat_user_tables
    ORDER BY n_live_tup DESC
    LIMIT 20;
  " 2>/dev/null | tee "$AUDIT_DIR/db-retention.txt"
fi

# Log retention
echo ""
echo "--- Log Retention ---"
journalctl --disk-usage 2>/dev/null | tee "$AUDIT_DIR/journal-usage.txt"

# Check logrotate configuration
if [ -f /etc/logrotate.conf ]; then
  echo ""
  echo "--- Logrotate ---"
  grep -E "rotate|daily|weekly|monthly|maxage" /etc/logrotate.conf 2>/dev/null | \
    tee "$AUDIT_DIR/logrotate.txt"
fi

# Old files (> 2 years) that may contain PII
echo ""
echo "--- Stale Files (>2 years) ---"
find /home -type f -mtime +730 \( -name "*.csv" -o -name "*.json" -o -name "*.sql" \) 2>/dev/null | \
  head -30 | tee "$AUDIT_DIR/stale-data-files.txt"

# Backup retention
echo ""
echo "--- Backup Retention ---"
for backup_dir in /backup /var/backups; do
  if [ -d "$backup_dir" ]; then
    echo "$backup_dir:"
    find "$backup_dir" -type f -printf '%T+ %p\n' 2>/dev/null | sort | head -20
  fi
done | tee "$AUDIT_DIR/backup-retention.txt"
```

### Cross-Border Transfer Assessment (Art. 44-49)

Identify potential international data flows:

```bash
AUDIT_DIR="$HOME/App/domains/argus/reports/gdpr/audit-$(date +%Y%m%d-%H%M%S)"
mkdir -p "$AUDIT_DIR"

echo "=== Cross-Border Data Transfer Assessment ==="

# Cloud service dependencies
echo "--- Cloud Services ---"

# Check for common cloud SDKs in dependencies
find /home -name "package.json" -o -name "Gemfile" -o -name "requirements.txt" -o -name "Cargo.toml" 2>/dev/null | \
  while IFS= read -r file; do
    if grep -qiE "aws-sdk|google-cloud|azure|cloudflare" "$file" 2>/dev/null; then
      echo "  Cloud SDK in $file:"
      grep -iE "aws-sdk|google-cloud|azure|cloudflare" "$file" | head -5
    fi
  done | tee "$AUDIT_DIR/cloud-dependencies.txt"

# External API endpoints from config
echo ""
echo "--- External API Endpoints ---"
find /home -name ".env*" -o -name "config*.yml" -o -name "config*.json" 2>/dev/null | \
  while IFS= read -r file; do
    endpoints=$(grep -oE 'https?://[a-zA-Z0-9.-]+\.[a-z]{2,}' "$file" 2>/dev/null | sort -u)
    if [ -n "$endpoints" ]; then
      echo "  $file:"
      echo "$endpoints" | while IFS= read -r ep; do
        echo "    → $ep"
      done
    fi
  done | tee "$AUDIT_DIR/external-endpoints.txt"

# Database connection strings
echo ""
echo "--- Database Connections ---"
find /home -name "database.yml" -o -name ".env*" -o -name "config*.json" 2>/dev/null | \
  while IFS= read -r file; do
    if grep -qiE "host=|DATABASE_URL|MONGODB_URI|REDIS_URL" "$file" 2>/dev/null; then
      echo "  $file:"
      grep -iE "host=|DATABASE_URL|MONGODB_URI|REDIS_URL" "$file" | \
        sed 's/=.*/=REDACTED/' | head -5
    fi
  done | tee "$AUDIT_DIR/db-connections.txt"
```

### Automated GDPR Score

Calculate a weighted GDPR compliance score:

```bash
AUDIT_DIR="$HOME/App/domains/argus/reports/gdpr/audit-$(date +%Y%m%d-%H%M%S)"
mkdir -p "$AUDIT_DIR"
SCORECARD="$AUDIT_DIR/scorecard.json"

echo "=== GDPR Compliance Scorecard ==="

compute_score() {
  category="$1"
  checks="$2"
  passed=0
  total=0
  
  # Each check is "name:pass/fail:weight"
  for check in $checks; do
    name=$(echo "$check" | cut -d: -f1)
    result=$(echo "$check" | cut -d: -f2)
    weight=$(echo "$check" | cut -d: -f3)
    total=$((total + weight))
    if [ "$result" = "pass" ]; then
      passed=$((passed + weight))
    fi
  done
  
  score=$((passed * 100 / total))
  echo "  $category: $score% ($passed/$total)"
  echo "{\"category\": \"$category\", \"score\": $score, \"passed\": $passed, \"total\": $total}" >> "$SCORECARD"
}

echo "{" > "$SCORECARD"

# Art. 5 — Data Minimization
compute_score "Art.5-Data-Minimization" \
  "pii-schema:pass:10 log-leakage:pass:8 stale-data:pass:7"

# Art. 25 — Privacy by Design
compute_score "Art.25-Privacy-by-Design" \
  "encryption-default:pass:10 data-minimization:pass:8 pseudonymization:fail:5"

# Art. 32 — Security of Processing
compute_score "Art.32-Security" \
  "disk-encryption:pass:15 tls-valid:pass:15 access-control:pass:10 firewall:pass:5"

# Art. 33 — Breach Notification
compute_score "Art.33-Breach-Notification" \
  "detection-capability:pass:10 alerting:pass:8 72h-workflow:pass:7"

# Art. 35 — DPIA
compute_score "Art.35-DPIA" \
  "dpia-template:pass:5 practices:pass:5"

echo "}" >> "$SCORECARD"

# Final score
total_pass=$(jq -s 'map(.passed) | add' "$SCORECARD" 2>/dev/null)
total_all=$(jq -s 'map(.total) | add' "$SCORECARD" 2>/dev/null)

if [ -n "$total_all" ] && [ "$total_all" -gt 0 ]; then
  final=$((total_pass * 100 / total_all))
  echo ""
  echo "============================================"
  echo "  OVERALL GDPR COMPLIANCE: $final%"
  echo "============================================"
  
  if [ "$final" -ge 90 ]; then
    echo "  Rating: ✅ EXCELLENT — strong GDPR posture"
  elif [ "$final" -ge 70 ]; then
    echo "  Rating: ⚠️  ADEQUATE — remediation recommended"
  elif [ "$final" -ge 50 ]; then
    echo "  Rating: ❌ POOR — significant gaps"
  else
    echo "  Rating: 🚨 CRITICAL — immediate action required"
  fi
fi
```

### DPIA Template (Art. 35)

Generate a Data Protection Impact Assessment:

```bash
AUDIT_DIR="$HOME/App/domains/argus/reports/gdpr/audit-$(date +%Y%m%d-%H%M%S)"
mkdir -p "$AUDIT_DIR"
DPIA="$AUDIT_DIR/DPIA-template.md"

cat > "$DPIA" << 'EOF'
# Data Protection Impact Assessment (DPIA)

**Project/System:**
**DPIA Reference:** DPIA-YYYY-NNN
**Date:** 
**Review Date:**
**DPO/Responsible Person:**

---

## 1. Description of Processing

### 1.1 Nature of Processing
(Describe the processing activities)

### 1.2 Scope
- Data subjects affected: 
- Data categories processed: 
- Geographic scope: 
- Retention period: 

### 1.3 Context
- Source of data: 
- Nature of relationship with data subjects: 
- Technology used: 
- Data volume (records): 

### 1.4 Purposes
(Primary and secondary purposes of processing)

---

## 2. Necessity & Proportionality

### 2.1 Lawful Basis (Art. 6)
- [ ] Consent (Art. 6.1.a)
- [ ] Contract (Art. 6.1.b)  
- [ ] Legal obligation (Art. 6.1.c)
- [ ] Vital interests (Art. 6.1.d)
- [ ] Public interest (Art. 6.1.e)
- [ ] Legitimate interest (Art. 6.1.f)

### 2.2 Special Categories (Art. 9)
(If processing special category data, identify Art. 9 exemption)

### 2.3 Proportionality Assessment
(Why this processing is necessary and proportionate)

### 2.4 Data Minimization
(How data minimization is achieved)

---

## 3. Risk Assessment

### 3.1 Assets at Risk
| Asset | Data Category | Volume | Sensitivity |
|-------|--------------|--------|-------------|
| | | | |

### 3.2 Threat Sources
| Threat | Likelihood | Impact | Risk Level |
|--------|-----------|--------|------------|
| | | | |

### 3.3 Risk Matrix
(High-level risk summary)

---

## 4. Security Measures (Art. 32)

### 4.1 Technical Measures
- [ ] Encryption at rest
- [ ] Encryption in transit (TLS 1.2+)
- [ ] Access control (least privilege)
- [ ] Multi-factor authentication
- [ ] Audit logging
- [ ] Intrusion detection
- [ ] Regular patching
- [ ] Backup + restore tested
- [ ] Data pseudonymization
- [ ] Secure deletion capability

### 4.2 Organizational Measures
- [ ] Staff training
- [ ] Data protection policy
- [ ] Incident response plan
- [ ] Data processor agreements
- [ ] Regular audits
- [ ] Access reviews

---

## 5. Data Subject Rights

### 5.1 Rights Implementation
- [ ] Right of access (Art. 15)
- [ ] Right to rectification (Art. 16)
- [ ] Right to erasure (Art. 17)
- [ ] Right to restriction (Art. 18)
- [ ] Right to portability (Art. 20)
- [ ] Right to object (Art. 21)
- [ ] Automated decision-making (Art. 22)

### 5.2 Response Procedures
(How each right is operationally fulfilled)

---

## 6. Third-Party Data Flows

### 6.1 Data Processors
| Processor | Data Shared | Country | Adequacy Decision | DPA Signed |
|-----------|------------|---------|-------------------|------------|
| | | | | |

### 6.2 International Transfers (Art. 44-49)
- [ ] EU Adequacy Decision
- [ ] Standard Contractual Clauses
- [ ] Binding Corporate Rules
- [ ] Code of Conduct / Certification

---

## 7. Breach Response (Art. 33-34)

### 7.1 Detection Capability
(How breaches are detected)

### 7.2 72-Hour Notification Process
(Step-by-step notification workflow)

### 7.3 Data Subject Communication (Art. 34)
(Template and process for notifying affected individuals)

---

## 8. Consultation

### 8.1 DPO Involvement
(DPO consulted: Yes / No / N/A)

### 8.2 Supervisory Authority Consultation (Art. 36)
(Prior consultation required: Yes / No — if high residual risk)

### 8.3 Stakeholder Input
(Data subjects, works council, other stakeholders consulted)

---

## 9. Mitigation & Residual Risk

### 9.1 Planned Mitigations
| Action | Owner | Deadline | Risk Reduction |
|--------|-------|----------|----------------|
| | | | |

### 9.2 Residual Risk Statement
(Post-mitigation risk assessment — acceptable?)

---

## 10. Sign-Off

| Role | Name | Signature | Date |
|------|------|-----------|------|
| Data Controller | | | |
| DPO (if applicable) | | | |
| Technical Lead | | | |

---

**DPIA Review Cycle:** Annual / On significant change / On breach

**Next Review Date:**
EOF

echo "DPIA template: $DPIA"
```

## Usage Patterns

### Full GDPR Audit

Complete technical GDPR audit:

1. **Data Discovery** — inventory all data stores and processing activities
2. **Data Mapping** — trace data flows from collection to deletion
3. **PII Scan** — identify personal data in schemas, logs, and files
4. **Encryption Audit** — verify encryption at rest, in transit, in backups
5. **Access Control Review** — SSH keys, sudo permissions, firewall rules
6. **Retention Analysis** — identify stale data, check retention policies
7. **Cross-Border Assessment** — map international data flows
8. **Security Scoring** — automated GDPR compliance scorecard
9. **DPIA Generation** — create/review Data Protection Impact Assessment
10. **Report** — compiled audit report with findings and remediation steps

### Pre-Launch Compliance Check

Before deploying a new system:

1. Run data field audit on schema
2. Verify encryption configuration
3. Set up data retention policy
4. Configure breach detection
5. Generate DPIA for new processing
6. Review data processor agreements

### Regulatory Filing Preparation

When preparing for a supervisory authority audit:

1. Run full GDPR audit
2. Generate current DPIA
3. Update data processing inventory (Art. 30)
4. Verify breach notification readiness
5. Audit data subject rights implementation
6. Check cross-border transfer documentation

## Pricing Tiers

### Free (Basic)
- Data field audit (PII patterns in schema)
- Encryption verification (basic disk + TLS)
- Open port and firewall review
- SSH key audit
- Text-only findings
- Single system

### Professional ($49/report)
- Full data processing inventory
- Comprehensive PII scan (schema, logs, files)
- Complete encryption audit (TLS, database, backup)
- Access control deep-dive (sudo, ACLs, RBAC)
- Data retention analysis with recommendations
- Cross-border transfer assessment
- Automated GDPR scorecard (0-100%)
- DPIA template with guidance
- PDF report with prioritized remediation
- Regulatory filing support documents

### Enterprise ($199/month)
- All Professional features
- Multi-system audits (up to 50 systems)
- Quarterly automated re-audits
- Custom compliance policy engine
- Integration with vulnerability-scanner for Art. 32
- Team dashboard
- SLA: audit within 24 hours
- Regulatory change monitoring (new CJEU rulings)

## Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `AYNOPS_MCP_URL` | `http://localhost:8765/aynops` | AynOps endpoint for TLS verification |
| `AUDIT_DIR` | `~/App/domains/argus/reports/gdpr/audit-*` | Audit output directory |
| `TARGET_SYSTEMS` | `localhost` | Systems to audit (comma-separated) |
| `PII_SCAN_DEPTH` | `3` | Max directory depth for PII scan |
| `RETENTION_WARNING_DAYS` | `730` | Days before flagging data as stale (2 years) |
| `TLS_MIN_VERSION` | `1.2` | Minimum acceptable TLS version |
| `COMPLIANCE_TARGET` | `80` | Target GDPR score percentage |
| `DATA_SUBJECT_REQUEST_EMAIL` | (required) | Contact for data subject requests |

## Troubleshooting

| Symptom | Likely Cause | Fix |
|---------|-------------|-----|
| Disk encryption not detected | Not using LUKS | Check with `sudo dmsetup ls` |
| TLS check fails | Certificate expired | Renew via certbot or CA |
| Firewall rules empty | iptables not configured | `sudo iptables -L -n` |
| PostgreSQL access denied | No sudo/peer auth | Configure `~/.pgpass` or peer auth |
| PII scan too slow on large filesystems | Recursive find on /home | Limit with `-maxdepth 3` |
| DPIA template questions unclear | Template designed for general case | Customize per processing activity |

## Security

- **Audit data is sensitive** — results contain PII locations and security gaps; protect at rest
- **Never exfiltrate** — all audit data stays on ARGUS host
- **Read-only audit** — never modifies systems, only reports findings
- **Least privilege scanning** — use minimal permissions for each audit phase
- **Data classification** — audit results should be treated as CONFIDENTIAL
- **Legal privilege** — consider engaging legal counsel before documenting certain findings

## BlackArch Integration

Optional tools for deeper audits:

| Tool | Use in GDPR Audit |
|------|-------------------|
| lynis | System hardening audit |
| nmap | Port scanning for unauthorized services |
| trivy | Container vulnerability scanning |

## Related Skills

- **gdpr-checker** — GDPR compliance for ZK-Bankir (financial focus, different scope)
- **vulnerability-scanner** — vulnerability assessment (Art. 32 security requirement)
- **incident-responder** — breach notification readiness (Art. 33-34)
- **osint-investigator** — discover exposed data via OSINT (Art. 32 risk assessment)
