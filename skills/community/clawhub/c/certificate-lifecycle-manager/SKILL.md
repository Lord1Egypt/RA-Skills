---
name: certificate-lifecycle-manager
description: Manage TLS/SSL certificate lifecycle — discovery, monitoring, renewal planning, and rotation. Track certificates across services, alert before expiry, automate renewal with ACME/Let's Encrypt, and verify deployment after rotation.
---

# Certificate Lifecycle Manager

Stop getting paged at 3 AM about expired certificates. Discover all certificates across your infrastructure, track expiry dates, plan renewals, automate with ACME/Let's Encrypt, and verify deployment — so certificates rotate smoothly before anyone notices.

Use when: "certificate expiring", "find all certificates", "SSL renewal", "cert management", "certificate inventory", "Let's Encrypt automation", "cert rotation", or when an expired certificate causes an outage.

## Commands

### 1. `discover` — Find All Certificates

#### Step 1: Scan Network Endpoints

```bash
# Scan known hosts for certificates
for host in $HOSTS; do
  for port in 443 8443 9443; do
    cert_info=$(echo | openssl s_client -connect "$host:$port" -servername "$host" 2>/dev/null | \
      openssl x509 -noout -subject -enddate -issuer 2>/dev/null)
    if [ -n "$cert_info" ]; then
      echo "=== $host:$port ==="
      echo "$cert_info"
      # Days until expiry
      expiry=$(echo | openssl s_client -connect "$host:$port" -servername "$host" 2>/dev/null | \
        openssl x509 -noout -enddate 2>/dev/null | cut -d= -f2)
      days=$(( ($(date -d "$expiry" +%s) - $(date +%s)) / 86400 ))
      echo "Days until expiry: $days"
      echo
    fi
  done
done
```

#### Step 2: Scan Kubernetes Secrets

```bash
kubectl get secrets -A -o json | python3 -c "
import json, sys, base64, subprocess
secrets = json.load(sys.stdin)['items']
for s in secrets:
    if s['type'] == 'kubernetes.io/tls':
        ns = s['metadata']['namespace']
        name = s['metadata']['name']
        cert_b64 = s['data'].get('tls.crt', '')
        if cert_b64:
            cert_pem = base64.b64decode(cert_b64).decode()
            result = subprocess.run(
                ['openssl', 'x509', '-noout', '-subject', '-enddate'],
                input=cert_pem, capture_output=True, text=True
            )
            print(f'{ns}/{name}: {result.stdout.strip()}')
"
```

#### Step 3: Scan Local Certificate Files

```bash
# Find certificate files
find / -maxdepth 5 \( -name "*.pem" -o -name "*.crt" -o -name "*.cert" -o -name "*.cer" \) \
  -not -path "*/proc/*" -not -path "*/sys/*" 2>/dev/null | while read cert; do
  info=$(openssl x509 -in "$cert" -noout -subject -enddate 2>/dev/null)
  if [ -n "$info" ]; then
    echo "=== $cert ==="
    echo "$info"
  fi
done
```

#### Step 4: Generate Inventory

```markdown
# Certificate Inventory

## Summary
- Certificates found: 23
- Expiring within 30 days: 2 🔴
- Expiring within 90 days: 5 🟡
- Healthy (>90 days): 16 🟢

## Critical (renew immediately)
| Host | CN/SAN | Issuer | Expires | Days Left |
|------|--------|--------|---------|-----------|
| api.example.com:443 | *.example.com | Let's Encrypt R3 | 2026-05-10 | 11 🔴 |
| internal.corp:8443 | internal.corp | Corp CA | 2026-05-15 | 16 🔴 |

## Warning (renew within 30 days)
| Host | CN/SAN | Issuer | Expires | Days Left |
|------|--------|--------|---------|-----------|
| staging.example.com | *.staging.example.com | Let's Encrypt | 2026-06-15 | 47 🟡 |

## Auto-Renewed (managed)
| Host | Provider | Auto-Renew | Last Renewed |
|------|----------|-----------|-------------|
| www.example.com | CloudFlare | ✅ | 2026-04-01 |
| app.example.com | AWS ACM | ✅ | 2026-03-15 |

## Manual Renewal Required
| Host | Reason |
|------|--------|
| internal.corp | Internal CA, no ACME support |
| vpn.example.com | Client certificate, manual CSR process |
```

### 2. `renew` — Automate Certificate Renewal

**Let's Encrypt / ACME:**
```bash
# Certbot renewal
certbot renew --dry-run 2>&1
certbot renew 2>&1

# Check renewal hooks
cat /etc/letsencrypt/renewal-hooks/deploy/*.sh 2>/dev/null
```

**Manual renewal runbook:**
1. Generate new CSR: `openssl req -new -key server.key -out server.csr`
2. Submit CSR to CA
3. Download new certificate
4. Verify chain: `openssl verify -CAfile ca-bundle.crt server.crt`
5. Deploy: update server config, restart service
6. Verify: `openssl s_client -connect host:443`

### 3. `monitor` — Set Up Expiry Alerts

```bash
# Prometheus blackbox exporter config
# Alerts at 30, 14, 7, 1 days before expiry
cat <<'YAML'
groups:
  - name: certificate-expiry
    rules:
      - alert: CertExpiringIn30Days
        expr: probe_ssl_earliest_cert_expiry - time() < 86400 * 30
        labels: { severity: warning }
      - alert: CertExpiringIn7Days
        expr: probe_ssl_earliest_cert_expiry - time() < 86400 * 7
        labels: { severity: critical }
      - alert: CertExpired
        expr: probe_ssl_earliest_cert_expiry - time() < 0
        labels: { severity: page }
YAML
```

### 4. `verify` — Post-Renewal Verification

After deploying new certificate:
```bash
# Verify certificate is deployed correctly
echo | openssl s_client -connect "$HOST:443" -servername "$HOST" 2>/dev/null | \
  openssl x509 -noout -subject -issuer -dates -fingerprint

# Check chain completeness
echo | openssl s_client -connect "$HOST:443" -servername "$HOST" -showcerts 2>/dev/null | \
  grep -c "BEGIN CERTIFICATE"
# Should be 2-3 (leaf + intermediate(s))

# Verify no mixed content or pinning issues
curl -sI "https://$HOST" | grep -i "strict-transport\|public-key-pins"
```
