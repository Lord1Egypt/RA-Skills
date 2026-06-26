---
name: ali-esa-acme-ssl-skill
description: Automatically issue/renew HTTPS certificates using Alibaba Cloud ESA DNS + acme.sh (including wildcard *.example.com + example.com), with optional installation to Nginx. Trigger this skill when the user mentions ESA, ATrustDNS, _acme-challenge, acme.sh, Let's Encrypt, No TXT record found, InvalidRecordNameSuffix, wildcard certificate, or Nginx certificate configuration.
homepage: https://github.com/dogeow/ali-esa-acme-ssl-skill
metadata: {"openclaw":{"homepage":"https://github.com/dogeow/ali-esa-acme-ssl-skill","os":["linux"],"requires":{"bins":["python3","dig","acme.sh"],"env":["ALIYUN_AK","ALIYUN_SK","ALIBABACLOUD_ACCESS_KEY_ID","ALIBABACLOUD_ACCESS_KEY_SECRET"]},"primaryEnv":"ALIYUN_AK"}}
---

# ESA DNS + ACME Certificate Automation

## Design Decision (Important)
This skill **combines acme.sh + ESA DNS** into a single integrated flow, not split into two skills.

Reasons:
1. The two steps are tightly coupled: ACME challenge tokens must be written to ESA DNS immediately.
2. The most common user errors are "validation failed / record written to the wrong panel" — an integrated flow minimizes mistakes.
3. Wildcard scenarios often produce multiple TXT values for the same FQDN; splitting would increase manual synchronization cost.

> If there is significant demand for "DNS-only operations" in the future, a separate `esa-dns-records` helper skill can be extracted.

---

## When to Trigger
Trigger when any of the following apply:
- Domain NS records are on `*.atrustdns.com` (ESA-hosted DNS)
- User says "issue certificate with acme.sh", "Let's Encrypt", "DNS-01"
- Error: `No TXT record found at _acme-challenge...`
- Need to issue `example.com + *.example.com` together
- Need to auto-write ESA DNS records and install to Nginx

---

## Supported Environment

- Linux hosts (recommended: Ubuntu tested)
- System-level Nginx (LNMP tested)
- Docker/containerized environments are not supported
- Not tested on Windows/macOS

## Prerequisites

Install `acme.sh` from the official project before using this skill, and review the installation method you choose instead of piping remote scripts directly to a shell:

- https://github.com/acmesh-official/acme.sh

This skill expects `acme.sh` to be available on `PATH`. The script also falls back to `~/.acme.sh/acme.sh` if present.

Requirements:

- Credentials via `ALIYUN_AK` / `ALIYUN_SK` or `ALIBABACLOUD_ACCESS_KEY_ID` / `ALIBABACLOUD_ACCESS_KEY_SECRET`
- Optional ESA region hint via `ALIYUN_ESA_REGION` / `ALIBABACLOUD_ESA_REGION` / `ESA_REGION` or `--region`
- STS token is supported via `ALIYUN_SECURITY_TOKEN`, `ALIBABACLOUD_SECURITY_TOKEN`, or `--sts-token`
- If the user provides credentials directly in OpenClaw chat/TUI as plain `id` / `secret` / `token` values without env names, treat them as generic Alibaba Cloud `AccessKeyId` / `AccessKeySecret` / `SecurityToken` and pass them to `--ak` / `--sk` / `--sts-token`. Do not block on whether the user said `Aliyun` or `Alibaba Cloud`; let the script auto-detect the ESA region/site.

---

## Running the Script

Script path: `scripts/esa_acme_issue.py`

Default behavior (optimized):

- Certificate installation to Nginx is disabled by default; opt in with `--install-cert`
- `--dns-timeout` defaults to 600 seconds
- Region auto-discovery is best-effort; if ESA does not expose `DescribeRegions`, pass `--region` to seed site discovery and the script will probe a fallback region list
- Optional IPv4/IPv6 record management: `--ensure-a-record host=ip` (with authoritative NS propagation check)
- Overwrite protection: existing A value is NOT overwritten unless `--confirm-overwrite` is passed
- `--lang` selects output language (default: `en`; available languages auto-discovered from `scripts/i18n/`)
- If `--install-cert` is used, run on a controlled Linux host with permission to write the target cert paths and reload Nginx

## Installing automatic renewal cron

Use `scripts/install_cron.sh` when the user wants this workflow to keep renewing automatically on the host.

What it installs:
- a root-owned env file containing AK/SK (and optional STS token / region hint)
- a wrapper script under `/usr/local/sbin/`
- a cron entry that runs the wrapper on the requested schedule and logs to `/var/log/`

Example:

```bash
sudo bash scripts/install_cron.sh \
  --wrapper-name dogeow \
  --domains "dogeow.com,*.dogeow.com" \
  --ak YOUR_AK \
  --sk YOUR_SK \
  --region cn-hangzhou \
  --with-nginx-reload
```

Important:
- This is the recommended way to automate renewal for ESA zones, because default `acme.sh --cron` does not know how to create ESA DNS TXT records by itself.
- If the user wants installed nginx cert paths, also pass `--cert-path` / `--key-path` and optionally `--reload-cmd`.

### Single domain

```bash
export ALIYUN_AK='YOUR_AK'
export ALIYUN_SK='YOUR_SK'
export ALIYUN_SECURITY_TOKEN='YOUR_STS_TOKEN'   # optional but recommended
python3 scripts/esa_acme_issue.py \
  -d test.example.com
```

Equivalent Alibaba Cloud env names are also accepted:

```bash
export ALIBABACLOUD_ACCESS_KEY_ID='YOUR_AK'
export ALIBABACLOUD_ACCESS_KEY_SECRET='YOUR_SK'
export ALIBABACLOUD_SECURITY_TOKEN='YOUR_STS_TOKEN'   # optional
```

### Apex + wildcard (recommended order)

```bash
export ALIYUN_AK='YOUR_AK'
export ALIYUN_SK='YOUR_SK'
python3 scripts/esa_acme_issue.py \
  -d example.com \
  -d '*.example.com'
```

### Wildcard only

```bash
python3 scripts/esa_acme_issue.py \
  -d '*.example.com'
```

---

## Correct Nginx Configuration

```nginx
ssl_certificate     /etc/nginx/ssl/example.com.crt;
ssl_certificate_key /etc/nginx/ssl/example.com.key;
```

---

## Completion Criteria (Anti False-Positive)
Before reporting "record created / DNS ready", both conditions must be met:

1) `ListRecords` returns the target `RecordName + Type + Value`;
2) Authoritative NS `dig @ns TXT` returns the expected token.

If only the CreateRecord API returned success (RequestId/RecordId only) without passing both checks above, report "request accepted", not "completed".

## Troubleshooting Quick Reference

1. `InvalidRecordNameSuffix`
   - Domain suffix does not belong to the current ESA site (common typo).

2. `No TXT record found at _acme-challenge...`
   - TXT not yet propagated to all authoritative NS; increase `--dns-timeout` to 300–600.

3. Permission / signature errors after setting AccessKey IP whitelist
   - Check current public egress IP: `curl -s ifconfig.me`
   - Whitelist the actual egress NAT IP (not LAN IP)
   - If behind proxy/gateway, whitelist the proxy egress IP
   - Wait briefly after whitelist update before retrying

---

## Security Guidelines

Before each execution, remind the user:
1) Use a RAM sub-account with minimal permissions. Do NOT use the primary account long-term AK.
2) Prefer STS temporary credentials to reduce leak risk.
3) Enable AccessKey IP whitelist, allowing only the actual egress NAT IP.
