#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Install a weekly cron job that renews ESA-managed ACME certificates.

Required:
  --domains "example.com,*.example.com"
  --ak YOUR_ACCESS_KEY_ID
  --sk YOUR_ACCESS_KEY_SECRET

Optional:
  --region cn-hangzhou            ESA region hint
  --env-file /root/.config/esa-acme.env
  --wrapper /usr/local/sbin/esa-acme-renew
  --log-file /var/log/esa-acme-renew.log
  --schedule "17 3 * * 0"         cron expression (default: weekly Sunday 03:17)
  --dns-timeout 600               passed to esa_acme_issue.py
  --lang en                       passed to esa_acme_issue.py
  --site-id 1234567890            optional ESA SiteId
  --cert-path /etc/nginx/ssl/example.crt
  --key-path /etc/nginx/ssl/example.key
  --reload-cmd "systemctl reload nginx"
  --with-nginx-reload             run nginx -t && reload after renewal (default off)
  --wrapper-name dogeow           convenience suffix for default env/wrapper/log names

Example:
  bash scripts/install_cron.sh \
    --wrapper-name dogeow \
    --domains "dogeow.com,*.dogeow.com" \
    --ak YOUR_AK \
    --sk YOUR_SK \
    --region cn-hangzhou \
    --with-nginx-reload
EOF
}

require_root() {
  if [[ ${EUID:-$(id -u)} -ne 0 ]]; then
    echo "[ERR] run as root" >&2
    exit 1
  fi
}

shell_quote() {
  printf "%q" "$1"
}

WRAPPER_NAME=""
DOMAINS=""
AK=""
SK=""
STS_TOKEN=""
REGION=""
SITE_ID=""
ENV_FILE=""
WRAPPER=""
LOG_FILE=""
SCHEDULE="17 3 * * 0"
DNS_TIMEOUT="600"
LANGUAGE="en"
CERT_PATH=""
KEY_PATH=""
RELOAD_CMD="systemctl reload nginx"
WITH_NGINX_RELOAD="0"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --domains) DOMAINS="$2"; shift 2 ;;
    --ak) AK="$2"; shift 2 ;;
    --sk) SK="$2"; shift 2 ;;
    --sts-token) STS_TOKEN="$2"; shift 2 ;;
    --region) REGION="$2"; shift 2 ;;
    --site-id) SITE_ID="$2"; shift 2 ;;
    --env-file) ENV_FILE="$2"; shift 2 ;;
    --wrapper) WRAPPER="$2"; shift 2 ;;
    --log-file) LOG_FILE="$2"; shift 2 ;;
    --schedule) SCHEDULE="$2"; shift 2 ;;
    --dns-timeout) DNS_TIMEOUT="$2"; shift 2 ;;
    --lang) LANGUAGE="$2"; shift 2 ;;
    --cert-path) CERT_PATH="$2"; shift 2 ;;
    --key-path) KEY_PATH="$2"; shift 2 ;;
    --reload-cmd) RELOAD_CMD="$2"; shift 2 ;;
    --with-nginx-reload) WITH_NGINX_RELOAD="1"; shift ;;
    --wrapper-name) WRAPPER_NAME="$2"; shift 2 ;;
    -h|--help) usage; exit 0 ;;
    *) echo "[ERR] unknown argument: $1" >&2; usage; exit 2 ;;
  esac
done

require_root

if [[ -z "$DOMAINS" || -z "$AK" || -z "$SK" ]]; then
  echo "[ERR] --domains, --ak, and --sk are required" >&2
  usage
  exit 2
fi

if [[ -z "$WRAPPER_NAME" ]]; then
  primary_domain="${DOMAINS%%,*}"
  WRAPPER_NAME="${primary_domain//\*/wildcard}"
  WRAPPER_NAME="${WRAPPER_NAME//@/root}"
  WRAPPER_NAME="${WRAPPER_NAME//./-}"
fi

if [[ -z "$ENV_FILE" ]]; then
  ENV_FILE="/root/.config/esa-acme-${WRAPPER_NAME}.env"
fi
if [[ -z "$WRAPPER" ]]; then
  WRAPPER="/usr/local/sbin/esa-acme-${WRAPPER_NAME}-renew"
fi
if [[ -z "$LOG_FILE" ]]; then
  LOG_FILE="/var/log/esa-acme-${WRAPPER_NAME}.log"
fi

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_SCRIPT="$SCRIPT_DIR/esa_acme_issue.py"
if [[ ! -f "$SKILL_SCRIPT" ]]; then
  echo "[ERR] could not find esa_acme_issue.py at $SKILL_SCRIPT" >&2
  exit 1
fi

mkdir -p "$(dirname "$ENV_FILE")"
umask 077
cat > "$ENV_FILE" <<EOF
ALIYUN_AK=$(shell_quote "$AK")
ALIYUN_SK=$(shell_quote "$SK")
EOF
if [[ -n "$STS_TOKEN" ]]; then
  printf 'ALIYUN_SECURITY_TOKEN=%s\n' "$(shell_quote "$STS_TOKEN")" >> "$ENV_FILE"
fi
if [[ -n "$REGION" ]]; then
  printf 'ALIYUN_ESA_REGION=%s\n' "$(shell_quote "$REGION")" >> "$ENV_FILE"
fi
chmod 600 "$ENV_FILE"

IFS=',' read -r -a domain_items <<< "$DOMAINS"
if [[ ${#domain_items[@]} -eq 0 ]]; then
  echo "[ERR] no domains parsed from --domains" >&2
  exit 2
fi

domain_args=()
for domain in "${domain_items[@]}"; do
  domain="${domain#${domain%%[![:space:]]*}}"
  domain="${domain%${domain##*[![:space:]]}}"
  if [[ -n "$domain" ]]; then
    domain_args+=("-d" "$domain")
  fi
done
if [[ ${#domain_args[@]} -eq 0 ]]; then
  echo "[ERR] no non-empty domains parsed from --domains" >&2
  exit 2
fi

{
  echo '#!/usr/bin/env bash'
  echo 'set -euo pipefail'
  echo 'export PATH="/root/.hermes/node/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"'
  printf 'source %s\n' "$(shell_quote "$ENV_FILE")"
  printf 'exec 9>%s\n' "$(shell_quote "/tmp/esa-acme-${WRAPPER_NAME}.lock")"
  echo 'flock -n 9 || exit 0'
  echo 'cd /root'
  printf 'python3 %s \\\n' "$(shell_quote "$SKILL_SCRIPT")"
  for ((i=0; i<${#domain_args[@]}; i+=2)); do
    printf '  -d %s \\\n' "$(shell_quote "${domain_args[i+1]}")"
  done
  printf '  --ak "$ALIYUN_AK" \\\n'
  printf '  --sk "$ALIYUN_SK" \\\n'
  if [[ -n "$STS_TOKEN" ]]; then
    printf '  --sts-token "$ALIYUN_SECURITY_TOKEN" \\\n'
  fi
  if [[ -n "$REGION" ]]; then
    printf '  --region "$ALIYUN_ESA_REGION" \\\n'
  fi
  if [[ -n "$SITE_ID" ]]; then
    printf '  --site-id %s \\\n' "$(shell_quote "$SITE_ID")"
  fi
  printf '  --dns-timeout %s \\\n' "$(shell_quote "$DNS_TIMEOUT")"
  printf '  --lang %s' "$(shell_quote "$LANGUAGE")"
  if [[ -n "$CERT_PATH" ]]; then
    printf ' \\\n  --install-cert \\\n  --cert-path %s' "$(shell_quote "$CERT_PATH")"
    if [[ -n "$KEY_PATH" ]]; then
      printf ' \\\n  --key-path %s' "$(shell_quote "$KEY_PATH")"
    fi
    if [[ -n "$RELOAD_CMD" ]]; then
      printf ' \\\n  --reload-cmd %s' "$(shell_quote "$RELOAD_CMD")"
    fi
  elif [[ -n "$KEY_PATH" ]]; then
    echo
    echo 'echo "[ERR] --key-path requires --cert-path" >&2'
    echo 'exit 2'
    chmod 700 "$WRAPPER"
    exit 2
  fi
  echo
  if [[ "$WITH_NGINX_RELOAD" == "1" && -z "$CERT_PATH" ]]; then
    echo 'nginx -t'
    echo 'systemctl reload nginx'
  fi
} > "$WRAPPER"
chmod 700 "$WRAPPER"

existing=$(mktemp)
newtab=$(mktemp)
crontab -l 2>/dev/null > "$existing" || true
grep -vF "$WRAPPER" "$existing" > "$newtab" || true
printf '%s %s >> %s 2>&1\n' "$SCHEDULE" "$WRAPPER" "$LOG_FILE" >> "$newtab"
crontab "$newtab"
rm -f "$existing" "$newtab"

bash -n "$WRAPPER"

echo "[OK] installed env file: $ENV_FILE"
echo "[OK] installed wrapper: $WRAPPER"
echo "[OK] installed cron: $(crontab -l | grep -F "$WRAPPER")"
echo "[OK] log file: $LOG_FILE"
