# ali-esa-acme-ssl-skill

[Chinese Documentation](README_zh.md)

OpenClaw skill for **automatic HTTPS certificate issuance/renewal** using **Alibaba Cloud ESA DNS + acme.sh**, with optional installation to Nginx.

## What this skill solves

AI models often resolve to the wrong place: they write records to traditional AliDNS, while the correct target should be ESA DNS. These two DNS systems are independent.

In other words, when a domain is hosted on ESA (`*.atrustdns.com`), DNS-01 validation records must be written to ESA DNS, not traditional AliDNS.

## Environment compatibility

- ✅ Linux hosts (Ubuntu tested)
- ✅ System-level Nginx deployments (LNMP tested)
- ❌ Containerized environments (Docker not supported)
- ❌ Windows/macOS not tested

## Project structure

- `SKILL.md` – Trigger rules and usage guidance for the agent
- `scripts/esa_acme_issue.py` – Automation script
- `scripts/i18n/` – Language files (en.json, zh.json, …) for script output
- `evals/evals.json` – Basic evaluation prompts

## acme.sh prerequisite

Install `acme.sh` from the official project before using this skill, and review the installation method you choose instead of piping remote scripts directly to a shell:

- https://github.com/acmesh-official/acme.sh

This skill expects `acme.sh` to be available on `PATH`. The script also falls back to `~/.acme.sh/acme.sh` if present.

## Quick start

### 1) Export credentials

```bash
export ALIYUN_AK='YOUR_AK'
export ALIYUN_SK='YOUR_SK'
export ALIYUN_SECURITY_TOKEN='YOUR_STS_TOKEN'  # optional but recommended
```

The script also accepts Alibaba Cloud style aliases:

```bash
export ALIBABACLOUD_ACCESS_KEY_ID='YOUR_AK'
export ALIBABACLOUD_ACCESS_KEY_SECRET='YOUR_SK'
export ALIBABACLOUD_SECURITY_TOKEN='YOUR_STS_TOKEN'  # optional
```

### 2) Single domain

```bash
python3 scripts/esa_acme_issue.py -d test.example.com
```

### 3) Apex + wildcard

```bash
python3 scripts/esa_acme_issue.py -d example.com -d '*.example.com'
```

### 3.1) Wildcard only

```bash
python3 scripts/esa_acme_issue.py -d '*.example.com'
```

The script keeps wildcard-only requests as wildcard-only. It no longer adds `example.com` implicitly.

### 4) With Chinese output

```bash
python3 scripts/esa_acme_issue.py -d example.com --lang zh
```

## Defaults

- Certificate installation to Nginx is disabled by default; opt in with `--install-cert`
- `--dns-timeout` defaults to 600 seconds
- Region auto-discovery is best-effort; if ESA does not expose `DescribeRegions`, pass `--region` to seed site discovery and the script will probe a fallback region list
- Optional IPv4/IPv6 record management: `--ensure-a-record host=ip` (with authoritative NS propagation check)

- If you use `--install-cert`, run on a controlled Linux host with permission to write target cert paths and reload Nginx

## Install automatic renewal cron

Use `scripts/install_cron.sh` to install a root-owned env file, wrapper script, and cron entry.

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

What it creates:
- env file under `/root/.config/`
- wrapper under `/usr/local/sbin/`
- cron entry that writes logs to `/var/log/`

You can customize the schedule with `--schedule`, for example:

```bash
sudo bash scripts/install_cron.sh \
  --domains "example.com,*.example.com" \
  --ak YOUR_AK \
  --sk YOUR_SK \
  --schedule "17 3 * * 0"
```

If you want acme.sh to install the renewed certificate into nginx-managed paths, pass `--cert-path`, `--key-path`, and optionally `--reload-cmd`.

Example:

```bash
python3 scripts/esa_acme_issue.py \
  -d test.example.com \
  --ensure-a-record test.example.com=1.2.3.4
```

Install to Nginx explicitly:

```bash
python3 scripts/esa_acme_issue.py \
  -d test.example.com \
  --install-cert
```

## Completion criteria (anti false-positive)

Do not say "DNS record is done" unless both checks pass:

1. ESA `ListRecords` confirms the exact `RecordName + Type + Value`
2. Authoritative NS query (`dig @ns TXT`) returns the expected token

If only CreateRecord API returned success, report it as "request accepted" (not completed).

## Common troubleshooting

- `No TXT record found`: increase `--dns-timeout`, verify authoritative NS propagation
- `InvalidRecordNameSuffix`: domain does not belong to current ESA site suffix

## FAQ

### Q: I set an IP whitelist on AccessKey. What should I check?

A: This is a common cause of "permission"-like failures.

- Ensure the **current egress public IP** of the server is in the whitelist
- If using proxy/NAT, whitelist the **actual outbound NAT IP**, not LAN IP
- Verify IP first:

  ```bash
  curl -s ifconfig.me
  ```

- If whitelist is strict, API calls may fail even when AK/SK and RAM policy are correct
- After changing whitelist, wait a short propagation window and retry

## Security notes

Always remind users of these 1/2/3 before execution:

1. Use least-privilege RAM sub-account keys instead of long-term root keys
2. Prefer STS temporary credentials whenever possible
3. Enable AccessKey IP allowlist for actual outbound NAT IP

- Never hardcode AK/SK in script
- Prefer env vars
- Rotate keys immediately if exposed in chat/logs
