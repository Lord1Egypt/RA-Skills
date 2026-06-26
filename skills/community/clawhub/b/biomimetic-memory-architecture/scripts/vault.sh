#!/bin/bash
# BMA Vault — encrypted key-value store for sensitive data.
# Derived from OpenCortex (MIT License). Namespace renamed OPENCORTEX_* → BMA_*.
# Uses GPG symmetric encryption (AES-256).
#
# Usage:
#   vault.sh init              Set up vault
#   vault.sh set <key> <value> Store a secret
#   vault.sh get <key>         Retrieve a secret
#   vault.sh list              List stored keys, not values
#   vault.sh delete <key>      Remove a secret
#   vault.sh rotate            Rotate passphrase and re-encrypt secrets
#   vault.sh backend           Show passphrase backend
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
WORKSPACE="${CLAWD_WORKSPACE:-$(cd "$SCRIPT_DIR/../../.." && pwd)}"
VAULT_DIR="$WORKSPACE/.vault"
VAULT_FILE="$VAULT_DIR/secrets.gpg"
VAULT_PASS_FILE="$VAULT_DIR/.passphrase"
KEYRING_LABEL="bma-vault"

_keyring_backend() {
  if [ -n "${BMA_VAULT_PASS:-}" ]; then
    echo "env"
  elif command -v secret-tool >/dev/null 2>&1; then
    echo "secret-tool"
  elif command -v security >/dev/null 2>&1 && [[ "${OSTYPE:-}" == darwin* ]]; then
    echo "keychain"
  elif command -v keyctl >/dev/null 2>&1; then
    echo "keyctl"
  elif [ -f "$VAULT_PASS_FILE" ]; then
    echo "file"
  else
    echo "none"
  fi
}

_store_passphrase() {
  local pass="$1"
  if command -v secret-tool >/dev/null 2>&1; then
    echo "$pass" | secret-tool store --label="$KEYRING_LABEL" service bma key vault-passphrase 2>/dev/null
    echo "   🔐 Passphrase stored in system keyring (secret-tool)"
  elif command -v security >/dev/null 2>&1 && [[ "${OSTYPE:-}" == darwin* ]]; then
    security add-generic-password -a bma -s "$KEYRING_LABEL" -w "$pass" 2>/dev/null || {
      security delete-generic-password -a bma -s "$KEYRING_LABEL" 2>/dev/null || true
      security add-generic-password -a bma -s "$KEYRING_LABEL" -w "$pass" >/dev/null
    }
    echo "   🔐 Passphrase stored in macOS Keychain"
  elif command -v keyctl >/dev/null 2>&1; then
    local ring
    ring=$(keyctl newring bma @u 2>/dev/null || keyctl search @u keyring bma 2>/dev/null)
    echo "$pass" | keyctl padd user vault-passphrase "$ring" >/dev/null 2>&1
    echo "   🔐 Passphrase stored in kernel keyring (keyctl)"
  elif [ "${BMA_ALLOW_FILE_PASSPHRASE:-0}" = "1" ]; then
    mkdir -p "$VAULT_DIR"
    echo "$pass" > "$VAULT_PASS_FILE"
    chmod 600 "$VAULT_PASS_FILE"
    echo "   📁 Passphrase stored in $VAULT_PASS_FILE (mode 600)"
    echo "   ⚠️  File-based storage is less secure than a system keyring"
  else
    echo "❌ No system keyring available."
    echo "   Install secret-tool, use macOS Keychain, install keyctl, set BMA_VAULT_PASS,"
    echo "   or set BMA_ALLOW_FILE_PASSPHRASE=1 to allow file-based storage."
    return 1
  fi
}

_get_passphrase() {
  case "$(_keyring_backend)" in
    secret-tool) secret-tool lookup service bma key vault-passphrase 2>/dev/null ;;
    keychain) security find-generic-password -a bma -s "$KEYRING_LABEL" -w 2>/dev/null ;;
    keyctl)
      local ring key
      ring=$(keyctl search @u keyring bma 2>/dev/null) || return 1
      key=$(keyctl search "$ring" user vault-passphrase 2>/dev/null) || return 1
      keyctl print "$key" 2>/dev/null
      ;;
    env) echo "${BMA_VAULT_PASS:-}" ;;
    file) cat "$VAULT_PASS_FILE" 2>/dev/null ;;
    *) return 1 ;;
  esac
}

_ensure_vault() {
  if [ ! -f "$VAULT_FILE" ]; then
    echo "Vault not initialized. Run: $0 init" >&2
    exit 1
  fi
  if [ -z "$(_get_passphrase 2>/dev/null || true)" ]; then
    echo "❌ Cannot retrieve vault passphrase." >&2
    echo "   Checked system keyring, BMA_VAULT_PASS, and $VAULT_PASS_FILE" >&2
    exit 1
  fi
}

_encrypt() {
  local content="$1" pass tmpfile
  pass=$(_get_passphrase)
  tmpfile=$(mktemp)
  printf '%s\n' "$content" > "$tmpfile"
  gpg --batch --yes --passphrase-fd 3 --quiet --symmetric --cipher-algo AES256 --output "$VAULT_FILE" "$tmpfile" 3<<< "$pass" 2>/dev/null
  rm -f "$tmpfile"
  chmod 600 "$VAULT_FILE"
}

_decrypt() {
  local pass
  pass=$(_get_passphrase)
  gpg --batch --yes --passphrase-fd 3 --quiet --decrypt "$VAULT_FILE" 3<<< "$pass" 2>/dev/null
}

_validate_key() {
  local key="$1"
  if ! printf '%s' "$key" | grep -qE '^[A-Za-z_][A-Za-z0-9_]*$'; then
    echo "❌ Invalid key name: $key" >&2
    echo "   Key must start with a letter or underscore and contain only letters, digits, and underscores." >&2
    exit 1
  fi
}

case "${1:-help}" in
  init)
    mkdir -p "$VAULT_DIR"
    chmod 700 "$VAULT_DIR"
    if [ -f "$VAULT_FILE" ] && [ -n "$(_get_passphrase 2>/dev/null || true)" ]; then
      echo "Vault already initialized at $VAULT_DIR"
      echo "   Backend: $(_keyring_backend)"
      exit 0
    fi
    command -v gpg >/dev/null 2>&1 || { echo "❌ gpg is required" >&2; exit 1; }
    command -v openssl >/dev/null 2>&1 || { echo "❌ openssl is required" >&2; exit 1; }
    pass=$(openssl rand -base64 32)
    _store_passphrase "$pass"
    # Ensure initial encryption can run even before keyring backend is re-detected.
    if [ ! -f "$VAULT_PASS_FILE" ]; then
      printf '%s\n' "$pass" > "$VAULT_PASS_FILE"
      chmod 600 "$VAULT_PASS_FILE"
    fi
    _encrypt ""
    if [ "$(_keyring_backend)" != "file" ] && [ -f "$VAULT_PASS_FILE" ] && [ "${BMA_ALLOW_FILE_PASSPHRASE:-0}" != "1" ]; then
      rm -f "$VAULT_PASS_FILE"
    fi
    echo "✅ Vault initialized at $VAULT_DIR"
    ;;
  set)
    _ensure_vault
    key="${2:-}"; value="${3:-}"
    [ -n "$key" ] && [ -n "$value" ] || { echo "Usage: vault.sh set <key> <value>" >&2; exit 1; }
    _validate_key "$key"
    content=$(_decrypt | grep -v "^${key}=" || true)
    content="${content}
${key}=${value}"
    _encrypt "$content"
    echo "✅ Stored: $key"
    ;;
  get)
    _ensure_vault
    key="${2:-}"
    [ -n "$key" ] || { echo "Usage: vault.sh get <key>" >&2; exit 1; }
    _validate_key "$key"
    value=$(_decrypt | grep "^${key}=" | head -1 | cut -d= -f2- || true)
    [ -n "$value" ] || { echo "Key not found: $key" >&2; exit 1; }
    printf '%s\n' "$value"
    ;;
  list)
    _ensure_vault
    _decrypt | grep -v '^$' | cut -d= -f1 | sort
    ;;
  delete)
    _ensure_vault
    key="${2:-}"
    [ -n "$key" ] || { echo "Usage: vault.sh delete <key>" >&2; exit 1; }
    _validate_key "$key"
    content=$(_decrypt | grep -v "^${key}=" || true)
    _encrypt "$content"
    echo "✅ Deleted: $key"
    ;;
  rotate)
    _ensure_vault
    command -v openssl >/dev/null 2>&1 || { echo "❌ openssl is required" >&2; exit 1; }
    content=$(_decrypt)
    new_pass=$(openssl rand -base64 32)
    backend=$(_keyring_backend)
    case "$backend" in
      env)
        # env backend: cannot persist new passphrase.
        echo "❌ Cannot rotate passphrase when using BMA_VAULT_PASS (env backend)."
        echo "   Unset BMA_VAULT_PASS, run 'vault.sh rotate' to store a new passphrase in your keyring,"
        echo "   then re-set BMA_VAULT_PASS if needed."
        exit 1
        ;;
      secret-tool|keychain|keyctl)
        _store_passphrase "$new_pass"
        ;;
      file)
        mkdir -p "$VAULT_DIR"
        printf '%s\n' "$new_pass" > "$VAULT_PASS_FILE"
        chmod 600 "$VAULT_PASS_FILE"
        ;;
      *)
        echo "❌ No passphrase backend available for rotation." >&2
        exit 1
        ;;
    esac
    tmpfile=$(mktemp)
    printf '%s\n' "$content" > "$tmpfile"
    gpg --batch --yes --passphrase-fd 3 --quiet --symmetric --cipher-algo AES256 --output "$VAULT_FILE" "$tmpfile" 3<<< "$new_pass" 2>/dev/null
    rm -f "$tmpfile"
    chmod 600 "$VAULT_FILE"
    echo "✅ Passphrase rotated. Backend: $(_keyring_backend)"
    ;;
  backend)
    echo "Passphrase backend: $(_keyring_backend)"
    [ -f "$VAULT_PASS_FILE" ] && echo "⚠️  File passphrase exists at $VAULT_PASS_FILE"
    ;;
  help|*)
    sed -n '1,14p' "$0"
    ;;
esac
