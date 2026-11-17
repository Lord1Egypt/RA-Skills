#!/bin/bash
#
# API Cockpit - Key Encryption Utility
# Encrypts/decrypts API keys using openssl AES-256-CBC
#

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_DIR="${SCRIPT_DIR}/config"
KEY_FILE="${CONFIG_DIR}/.key"  # Master encryption key

# Generate a random master key if not exists
generate_key() {
    if [ ! -f "${KEY_FILE}" ]; then
        openssl rand -base64 32 > "${KEY_FILE}"
        chmod 600 "${KEY_FILE}"
        echo "Master key generated at ${KEY_FILE}"
    fi
}

# Encrypt a value
encrypt() {
    local value="$1"
    if [ -f "${KEY_FILE}" ]; then
        echo "${value}" | openssl enc -aes-256-cbc -salt -pbkdf2 -pass file:"${KEY_FILE}" -base64
    else
        echo "${value}"  # Fallback: no encryption if key missing
    fi
}

# Decrypt a value
decrypt() {
    local encrypted="$1"
    if [ -f "${KEY_FILE}" ]; then
        echo "${encrypted}" | openssl enc -aes-256-cbc -d -pbkdf2 -pass file:"${KEY_FILE}" -base64
    else
        echo "${encrypted}"  # Fallback: assume plain text
    fi
}

# Encrypt .env file
encrypt_env() {
    local input="$1"
    local output="${input}.enc"
    
    if [ ! -f "${input}" ]; then
        echo "Error: ${input} not found"
        exit 1
    fi
    
    generate_key
    openssl enc -aes-256-cbc -salt -pbkdf2 -pass file:"${KEY_FILE}" -in "${input}" -out "${output}"
    rm "${input}"
    echo "Encrypted ${input} -> ${output}"
}

# Decrypt .env file
decrypt_env() {
    local input="$1"
    local output="${input%.enc}"
    
    if [ ! -f "${input}" ]; then
        echo "Error: ${input} not found"
        exit 1
    fi
    
    openssl enc -aes-256-cbc -d -pbkdf2 -pass file:"${KEY_FILE}" -in "${input}" -out "${output}"
    echo "Decrypted ${input} -> ${output}"
}

# Main
case "${1:-}" in
    encrypt)
        encrypt_env "${2:-config/.env}"
        ;;
    decrypt)
        decrypt_env "${2:-config/.env.enc}"
        ;;
    generate)
        generate_key
        ;;
    *)
        echo "Usage: $0 {encrypt|decrypt|generate} [file]"
        ;;
esac
