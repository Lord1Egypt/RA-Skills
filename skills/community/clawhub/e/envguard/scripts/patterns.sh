#!/usr/bin/env bash
# EnvGuard — Secret Pattern Definitions
# Each pattern: REGEX | SEVERITY | SERVICE | DESCRIPTION
#
# Severity levels:
#   critical — Immediate credential exposure risk
#   high     — Likely valid secret or token
#   medium   — Possible secret, needs verification
#   low      — Generic pattern, higher false positive rate
#
# IMPORTANT: All regexes must use POSIX ERE syntax (grep -E compatible).
# - Use [[:space:]] instead of \s
# - Use literal quotes instead of \x27
# - Avoid Perl-only features (\d, \w, etc.)

set -euo pipefail

# ─── Pattern registry ──────────────────────────────────────────────────────
#
# Format: "regex|severity|service|description"
# Patterns use POSIX extended grep regex (ERE) syntax.
# Order: critical first, then high, medium, low.

declare -a ENVGUARD_PATTERNS=()

# ─── 1. AWS Credentials (Critical) ────────────────────────────────────────

ENVGUARD_PATTERNS+=(
  'AKIA[0-9A-Z]{16}|critical|AWS|AWS Access Key ID'
  'aws_secret_access_key[[:space:]]*[=:][[:space:]]*[A-Za-z0-9/+=]{40}|critical|AWS|AWS Secret Access Key'
  'ASIA[0-9A-Z]{16}|critical|AWS|AWS Temporary Access Key (STS)'
)

# ─── 2. Stripe Keys (Critical) ────────────────────────────────────────────

ENVGUARD_PATTERNS+=(
  'sk_live_[0-9a-zA-Z]{24,}|critical|Stripe|Stripe Live Secret Key'
  'sk_test_[0-9a-zA-Z]{24,}|high|Stripe|Stripe Test Secret Key'
  'rk_live_[0-9a-zA-Z]{24,}|critical|Stripe|Stripe Live Restricted Key'
  'rk_test_[0-9a-zA-Z]{24,}|high|Stripe|Stripe Test Restricted Key'
  'whsec_[0-9a-zA-Z]{24,}|critical|Stripe|Stripe Webhook Signing Secret'
  'pk_live_[0-9a-zA-Z]{24,}|medium|Stripe|Stripe Live Publishable Key'
)

# ─── 3. GitHub Tokens (Critical) ──────────────────────────────────────────

ENVGUARD_PATTERNS+=(
  'ghp_[0-9a-zA-Z]{36,}|critical|GitHub|GitHub Personal Access Token'
  'gho_[0-9a-zA-Z]{36,}|critical|GitHub|GitHub OAuth Access Token'
  'ghu_[0-9a-zA-Z]{36,}|critical|GitHub|GitHub User-to-Server Token'
  'ghs_[0-9a-zA-Z]{36,}|critical|GitHub|GitHub Server-to-Server Token'
  'ghr_[0-9a-zA-Z]{36,}|critical|GitHub|GitHub Refresh Token'
  'github_pat_[0-9a-zA-Z_]{22,}|critical|GitHub|GitHub Fine-Grained Personal Access Token'
)

# ─── 4. GitLab Tokens (Critical) ──────────────────────────────────────────

ENVGUARD_PATTERNS+=(
  'glpat-[0-9a-zA-Z_-]{20,}|critical|GitLab|GitLab Personal Access Token'
  'gloas-[0-9a-zA-Z_-]{20,}|critical|GitLab|GitLab OAuth Application Secret'
  'glrt-[0-9a-zA-Z_-]{20,}|critical|GitLab|GitLab Runner Registration Token'
)

# ─── 5. Slack Tokens (High) ───────────────────────────────────────────────

ENVGUARD_PATTERNS+=(
  'xoxb-[0-9]{10,}-[0-9a-zA-Z]{24,}|high|Slack|Slack Bot Token'
  'xoxp-[0-9]{10,}-[0-9a-zA-Z]{24,}|high|Slack|Slack User OAuth Token'
  'xoxo-[0-9]{10,}-[0-9a-zA-Z]{24,}|high|Slack|Slack OAuth Token'
  'xapp-[0-9]+-[A-Za-z0-9]{10,}-[0-9]{10,}-[a-z0-9]{64}|high|Slack|Slack App-Level Token'
  'xoxs-[0-9a-zA-Z-]{50,}|high|Slack|Slack Session Token'
)

# ─── 6. Google API Keys (High) ────────────────────────────────────────────

ENVGUARD_PATTERNS+=(
  'AIza[0-9A-Za-z_-]{35}|high|Google|Google API Key'
  '[0-9]+-[0-9A-Za-z_]{32}\.apps\.googleusercontent\.com|high|Google|Google OAuth Client ID'
)

# ─── 7. JWT Tokens (High) ─────────────────────────────────────────────────

ENVGUARD_PATTERNS+=(
  'eyJ[A-Za-z0-9_-]{20,}\.eyJ[A-Za-z0-9_-]{20,}\.[A-Za-z0-9_-]{20,}|high|JWT|JSON Web Token'
)

# ─── 8. Generic API Keys and Secrets (Low) ────────────────────────────────

ENVGUARD_PATTERNS+=(
  '[Aa][Pp][Ii]_?[Kk][Ee][Yy][[:space:]]*[=:][[:space:]]*"[0-9a-zA-Z_-]{16,}"|low|Generic|Generic API Key assignment'
  "[Aa][Pp][Ii]_?[Kk][Ee][Yy][[:space:]]*[=:][[:space:]]*'[0-9a-zA-Z_-]{16,}'|low|Generic|Generic API Key assignment (single-quoted)"
  '[Aa][Pp][Ii][-_]?[Kk][Ee][Yy][[:space:]]*[=:][[:space:]]*[0-9a-zA-Z_-]{20,}|low|Generic|Generic API Key assignment (unquoted)'
  '[Ss][Ee][Cc][Rr][Ee][Tt][[:space:]]*[=:][[:space:]]*"[^ "]{8,}"|low|Generic|Generic secret assignment'
  '[Pp][Aa][Ss][Ss][Ww][Oo][Rr][Dd][[:space:]]*[=:][[:space:]]*"[^ "]{8,}"|low|Generic|Generic password assignment'
  '[Tt][Oo][Kk][Ee][Nn][[:space:]]*[=:][[:space:]]*"[0-9a-zA-Z_-]{16,}"|low|Generic|Generic token assignment'
  'auth[_-]?token[[:space:]]*[=:][[:space:]]*"[^ "]{8,}"|low|Generic|Auth token assignment'
  'access[_-]?token[[:space:]]*[=:][[:space:]]*"[^ "]{8,}"|low|Generic|Access token assignment'
)

# ─── 9. Private Keys (Critical) ───────────────────────────────────────────

ENVGUARD_PATTERNS+=(
  'BEGIN RSA PRIVATE KEY|critical|PrivateKey|RSA Private Key'
  'BEGIN OPENSSH PRIVATE KEY|critical|PrivateKey|OpenSSH Private Key'
  'BEGIN DSA PRIVATE KEY|critical|PrivateKey|DSA Private Key'
  'BEGIN EC PRIVATE KEY|critical|PrivateKey|EC Private Key'
  'BEGIN PGP PRIVATE KEY BLOCK|critical|PrivateKey|PGP Private Key Block'
  'BEGIN PRIVATE KEY|critical|PrivateKey|Generic Private Key (PKCS8)'
  'BEGIN ENCRYPTED PRIVATE KEY|high|PrivateKey|Encrypted Private Key'
)

# ─── 10. .env File Contents (Low) ─────────────────────────────────────────
# Detects KEY=value patterns that look like env vars in non-.env files

ENVGUARD_PATTERNS+=(
  '^[A-Z][A-Z0-9_]{2,}=[[:space:]]*"?[^ "]{8,}"?|low|DotEnv|Environment variable pattern (potential .env leak)'
)

# ─── 11. Database Connection Strings (High) ───────────────────────────────

ENVGUARD_PATTERNS+=(
  'postgres(ql)?://[^ "<>]{10,}|high|Database|PostgreSQL Connection String'
  'mysql://[^ "<>]{10,}|high|Database|MySQL Connection String'
  'mongodb(\+srv)?://[^ "<>]{10,}|high|Database|MongoDB Connection String'
  'redis://[^ "<>]{10,}|high|Database|Redis Connection String'
  'amqp://[^ "<>]{10,}|high|Database|AMQP/RabbitMQ Connection String'
  'mssql://[^ "<>]{10,}|high|Database|MSSQL Connection String'
)

# ─── 12. SSH Keys / PEM Files (Medium) ────────────────────────────────────

ENVGUARD_PATTERNS+=(
  'BEGIN CERTIFICATE|medium|Certificate|X.509 Certificate'
  'ssh-rsa[[:space:]]+AAAA[0-9A-Za-z+/]{50,}|medium|SSH|SSH RSA Public Key (check for private key nearby)'
  'ssh-ed25519[[:space:]]+AAAA[0-9A-Za-z+/]{50,}|medium|SSH|SSH Ed25519 Public Key'
)

# ─── 13. Twilio, SendGrid, Mailgun, Postmark (High) ──────────────────────

ENVGUARD_PATTERNS+=(
  'SK[0-9a-fA-F]{32}|high|Twilio|Twilio API Key'
  'AC[0-9a-fA-F]{32}|medium|Twilio|Twilio Account SID'
  'SG\.[0-9A-Za-z_-]{22}\.[0-9A-Za-z_-]{43}|high|SendGrid|SendGrid API Key'
  'key-[0-9a-zA-Z]{32}|medium|Mailgun|Mailgun API Key'
  '[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}|low|Postmark|Postmark Server Token (UUID pattern)'
)

# ─── 14. Firebase / Supabase / Vercel (High) ──────────────────────────────

ENVGUARD_PATTERNS+=(
  'firebase[_-]?api[_-]?key[[:space:]]*[=:][[:space:]]*"?AIza[0-9A-Za-z_-]{35}|high|Firebase|Firebase API Key'
  'FIREBASE_[A-Z_]*[[:space:]]*[=:][[:space:]]*"[^ "]{10,}"|medium|Firebase|Firebase Configuration Value'
  'sbp_[0-9a-f]{40}|high|Supabase|Supabase Service Role Key'
  'vercel_[0-9a-zA-Z_]{24,}|high|Vercel|Vercel Token'
  'VERCEL_[A-Z_]*[[:space:]]*[=:][[:space:]]*"[^ "]{10,}"|medium|Vercel|Vercel Environment Variable'
)

# ─── 15. npm Tokens (High) ────────────────────────────────────────────────

ENVGUARD_PATTERNS+=(
  'npm_[0-9a-zA-Z]{36,}|high|npm|npm Access Token'
  '//registry\.npmjs\.org/:_authToken=[0-9a-zA-Z_-]{36,}|high|npm|npm Registry Auth Token'
)

# ─── 16. Docker Hub Tokens (Medium) ───────────────────────────────────────

ENVGUARD_PATTERNS+=(
  'dckr_pat_[0-9a-zA-Z_-]{24,}|medium|Docker|Docker Hub Personal Access Token'
  'DOCKER_[A-Z_]*PASSWORD[[:space:]]*[=:][[:space:]]*"[^ "]{8,}"|medium|Docker|Docker Password in Config'
)

# ─── 17. Heroku API Keys (Medium) ─────────────────────────────────────────

ENVGUARD_PATTERNS+=(
  'heroku[_-]?api[_-]?key[[:space:]]*[=:][[:space:]]*"?[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}|medium|Heroku|Heroku API Key'
  'HEROKU_API_KEY[[:space:]]*[=:][[:space:]]*"?[0-9a-fA-F-]{36}|medium|Heroku|Heroku API Key (env var)'
)

# ─── 18. DigitalOcean Tokens (Medium) ─────────────────────────────────────

ENVGUARD_PATTERNS+=(
  'dop_v1_[0-9a-fA-F]{64}|medium|DigitalOcean|DigitalOcean Personal Access Token'
  'doo_v1_[0-9a-fA-F]{64}|medium|DigitalOcean|DigitalOcean OAuth Token'
)

# ─── 19. Azure Keys (Medium) ──────────────────────────────────────────────

ENVGUARD_PATTERNS+=(
  'AccountKey=[0-9A-Za-z+/=]{44,}|medium|Azure|Azure Storage Account Key'
  'azure[_-]?client[_-]?secret[[:space:]]*[=:][[:space:]]*"[^ "]{8,}"|medium|Azure|Azure Client Secret'
  'AZURE_[A-Z_]*KEY[[:space:]]*[=:][[:space:]]*"[^ "]{10,}"|medium|Azure|Azure API Key'
  'SharedAccessSignature=sv=[^ &]{20,}|medium|Azure|Azure Shared Access Signature'
)

# ─── 20. Cloudflare API Tokens (Medium) ───────────────────────────────────

ENVGUARD_PATTERNS+=(
  'cloudflare[_-]?api[_-]?token[[:space:]]*[=:][[:space:]]*"?[0-9a-zA-Z_-]{40}|medium|Cloudflare|Cloudflare API Token'
  'CF_API_TOKEN[[:space:]]*[=:][[:space:]]*"?[0-9a-zA-Z_-]{40}|medium|Cloudflare|Cloudflare API Token (env var)'
  'CF_API_KEY[[:space:]]*[=:][[:space:]]*"?[0-9a-fA-F]{37}|medium|Cloudflare|Cloudflare Global API Key'
)

# ─── Utility: get pattern count ────────────────────────────────────────────

envguard_pattern_count() {
  echo "${#ENVGUARD_PATTERNS[@]}"
}

# ─── Utility: list patterns by severity ────────────────────────────────────

envguard_list_patterns() {
  local filter_severity="${1:-all}"

  for entry in "${ENVGUARD_PATTERNS[@]}"; do
    IFS='|' read -r regex severity service description <<< "$entry"
    if [[ "$filter_severity" == "all" || "$filter_severity" == "$severity" ]]; then
      printf "%-10s %-15s %s\n" "$severity" "$service" "$description"
    fi
  done
}

# ─── Utility: severity to numeric level ────────────────────────────────────

severity_to_level() {
  case "$1" in
    critical) echo 4 ;;
    high)     echo 3 ;;
    medium)   echo 2 ;;
    low)      echo 1 ;;
    *)        echo 0 ;;
  esac
}

# ─── Default exclude directories ───────────────────────────────────────────

ENVGUARD_EXCLUDE_DIRS=(
  ".git"
  "node_modules"
  "dist"
  "build"
  "vendor"
  "__pycache__"
  ".venv"
  "venv"
  ".tox"
  ".mypy_cache"
  ".pytest_cache"
  "target"
  ".next"
  ".nuxt"
  "coverage"
  ".terraform"
)

# ─── Default binary extensions to skip ─────────────────────────────────────

ENVGUARD_BINARY_EXTENSIONS=(
  "png" "jpg" "jpeg" "gif" "bmp" "ico" "svg"
  "woff" "woff2" "ttf" "eot" "otf"
  "pdf" "zip" "tar" "gz" "bz2" "xz" "7z" "rar"
  "exe" "dll" "so" "dylib" "bin"
  "mp3" "mp4" "avi" "mov" "mkv" "wav" "flac"
  "pyc" "pyo" "class" "o" "obj"
  "wasm" "map"
)
