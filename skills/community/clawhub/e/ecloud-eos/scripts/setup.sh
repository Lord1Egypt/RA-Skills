#!/bin/bash
# Mobile Cloud EOS Skill Auto Setup Script
# Usage:
#   setup.sh --check-only                    Check environment status only
#   setup.sh --access-key <ID> --secret-key <KEY> --region <REGION> --bucket <BUCKET> --endpoint <ENDPOINT>
#   setup.sh --config-file <path>            Use config file (properties format)

set -e

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

log_info()   { echo -e "${GREEN}✓${NC} $1"; }
log_error() { echo -e "${RED}✗${NC} $1"; }
log_warn() { echo -e "${YELLOW}!${NC} $1"; }

# Get script directory (skill baseDir)
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
BASE_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

# ========== Check Functions ==========

check_node() {
  if command -v node &>/dev/null; then
    log_info "Node.js $(node --version)"
    return 0
  else
    log_error "Node.js not installed"
    return 1
  fi
}

check_npm() {
  if command -v npm &>/dev/null; then
    log_info "npm $(npm --version)"
    return 0
  else
    log_error "npm not installed"
    return 1
  fi
}

check_eos_sdk() {
  if node -e "require('@aws-sdk/client-s3') && require('@aws-sdk/s3-request-presigner') && require('@smithy/hash-node') && require('@smithy/protocol-http')" &>/dev/null 2>&1; then
    log_info "Node.js SDK installed"
    return 0
  else
    log_error "Node.js SDK not installed"
    return 1
  fi
}

check_env_vars() {
  local all_set=true
  local bucket_missing=false

  # 检查必要的环境变量
  for key in EOS_ACCESS_KEY EOS_SECRET_KEY EOS_REGION EOS_ENDPOINT; do
    local value="${!key}"
    if [ -n "$value" ]; then
      log_info "$key is set"
    else
      log_error "$key not set"
      all_set=false
    fi
  done

  # 检查桶名环境变量（允许缺失，但会提示）
  if [ -n "$EOS_BUCKET" ]; then
    log_info "EOS_BUCKET is set"
  else
    log_warn "EOS_BUCKET not set (但可以执行 list-buckets/create-bucket/delete-bucket 操作)"
    bucket_missing=true
  fi

  $all_set
}

# ========== Check Mode ==========

do_check() {
  echo "=== Mobile Cloud EOS Skill Environment Check ==="
  echo ""
  echo "--- Basic Environment ---"
  check_node || true
  check_npm || true
  echo ""
  echo "--- Node.js SDK ---"
  check_eos_sdk || true
  echo ""
  echo "--- Environment Variables ---"
  if check_env_vars; then
    log_info "EOS环境变量配置完成"
  else
    log_error "缺少必要的EOS环境变量"
  fi
  echo ""
  echo "--- Skill Files ---"
  [ -f "$BASE_DIR/SKILL.md" ] && log_info "SKILL.md" || log_error "SKILL.md not found"
  [ -f "$BASE_DIR/scripts/eos_node.mjs" ] && log_info "scripts/eos_node.mjs" || log_error "scripts/eos_node.mjs not found"
  echo ""
}

# ========== Setup Mode ==========

do_setup() {
  local ACCESS_KEY=""
  local SECRET_KEY=""
  local REGION=""
  local BUCKET=""
  local ENDPOINT=""
  local CONFIG_FILE=""
  local COPY_CONFIG_FILE=""

  while [[ $# -gt 0 ]]; do
    case "$1" in
      --access-key)  ACCESS_KEY="$2"; shift 2;;
      --secret-key) SECRET_KEY="$2"; shift 2;;
      --region)     REGION="$2"; shift 2;;
      --bucket)     BUCKET="$2"; shift 2;;
      --endpoint)    ENDPOINT="$2"; shift 2;;
      --config-file) CONFIG_FILE="$2"; shift 2;;
      --copy-config-file) COPY_CONFIG_FILE="$2"; shift 2;;
      *) shift;;
    esac
  done

  # If config file provided, read credentials from it
  if [ -n "$CONFIG_FILE" ]; then
    if [ ! -f "$CONFIG_FILE" ]; then
      echo "Error: Config file not found: $CONFIG_FILE"
      exit 1
    fi

    # Parse properties format config file
    ACCESS_KEY=$(grep "^accessKey=" "$CONFIG_FILE" | cut -d'=' -f2- | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')
    SECRET_KEY=$(grep "^secretKey=" "$CONFIG_FILE" | cut -d'=' -f2- | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')
    REGION=$(grep "^region=" "$CONFIG_FILE" | cut -d'=' -f2- | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')
    BUCKET=$(grep "^bucket=" "$CONFIG_FILE" | cut -d'=' -f2- | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')
    ENDPOINT=$(grep "^endpoint=" "$CONFIG_FILE" | cut -d'=' -f2- | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')

    if [ -z "$ACCESS_KEY" ] || [ -z "$SECRET_KEY" ] || [ -z "$REGION" ] || [ -z "$BUCKET" ] || [ -z "$ENDPOINT" ]; then
      echo "Error: Config file is missing required fields"
      exit 1
    fi

    log_info "Credentials loaded from config file: $CONFIG_FILE"
  fi

  if [ -z "$ACCESS_KEY" ] || [ -z "$SECRET_KEY" ] || [ -z "$REGION" ] || [ -z "$BUCKET" ] || [ -z "$ENDPOINT" ]; then
    echo "Error: Missing required parameters"
    echo "Usage: setup.sh --access-key <ID> --secret-key <KEY> --region <REGION> --bucket <BUCKET> --endpoint <ENDPOINT>"
    echo "Or: setup.sh --config-file <path>"
    exit 1
  fi

  # If copy config file requested, load it directly first
  if [ -n "$COPY_CONFIG_FILE" ]; then
    if [ ! -f "$COPY_CONFIG_FILE" ]; then
      echo "Error: Config file not found: $COPY_CONFIG_FILE"
      exit 1
    fi

    echo "=== Load Config File ==="
    echo "Source: $COPY_CONFIG_FILE"
    
    # Verify file contains required keys
    local required_keys=("accessKey" "secretKey" "region" "bucket" "endpoint")
    local missing_keys=()
    
    for key in "${required_keys[@]}"; do
      if ! grep -q "^${key}=" "$COPY_CONFIG_FILE"; then
        missing_keys+=("$key")
      fi
    done
    
    if [ ${#missing_keys[@]} -gt 0 ]; then
      echo "Error: Config file is missing required keys: ${missing_keys[*]}" 
      echo "Required keys: ${required_keys[*]}"
      exit 1
    fi
    
    # Read credentials from config file
    ACCESS_KEY=$(grep "^accessKey=" "$COPY_CONFIG_FILE" | cut -d'=' -f2- | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')
    SECRET_KEY=$(grep "^secretKey=" "$COPY_CONFIG_FILE" | cut -d'=' -f2- | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')
    REGION=$(grep "^region=" "$COPY_CONFIG_FILE" | cut -d'=' -f2- | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')
    BUCKET=$(grep "^bucket=" "$COPY_CONFIG_FILE" | cut -d'=' -f2- | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')
    ENDPOINT=$(grep "^endpoint=" "$COPY_CONFIG_FILE" | cut -d'=' -f2- | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')

    if [ -z "$ACCESS_KEY" ] || [ -z "$SECRET_KEY" ] || [ -z "$REGION" ] || [ -z "$BUCKET" ] || [ -z "$ENDPOINT" ]; then
      echo "Error: Config file is missing required fields"
      exit 1
    fi

    echo ""
    echo "Credentials loaded from config file:"
    echo "  accessKey: $ACCESS_KEY"
    echo "  region: $REGION"
    echo "  bucket: $BUCKET"
    echo "  endpoint: $ENDPOINT"
    echo ""
    echo "=== Load Complete ==="
    # Don't exit here, continue with setup process
  fi

  echo "=== Mobile Cloud EOS Skill Auto Setup ==="
  echo ""

  # 1. Check Node.js
  echo "--- Step 1: Check Node.js ---"
  if ! check_node; then
    log_error "Please install Node.js first: https://nodejs.org/"
    exit 1
  fi

  # 2. Ensure package.json exists
  echo ""
  echo "--- Step 2: Initialize Project ---"
  if [ ! -f "$BASE_DIR/package.json" ]; then
    (cd "$BASE_DIR" && npm init -y &>/dev/null)
    log_info "Created package.json"
  else
    log_info "package.json already exists"
  fi

  # 3. Install Dependencies
  echo ""
  echo "--- Step 3: Install Dependencies ---"
  (cd "$BASE_DIR" && npm install @aws-sdk/client-s3 @aws-sdk/s3-request-presigner @smithy/hash-node @smithy/protocol-http --no-progress 2>&1 | tail -3)
  log_info "Dependencies installation completed"

  # 4. Set Environment Variables
  echo ""
  echo "--- Step 4: Set Environment Variables ---"
  
  # Set environment variables for current session
  export EOS_ACCESS_KEY="$ACCESS_KEY"
  export EOS_SECRET_KEY="$SECRET_KEY"
  export EOS_REGION="$REGION"
  export EOS_BUCKET="$BUCKET"
  export EOS_ENDPOINT="$ENDPOINT"
  
  # Determine shell config file
  SHELL_CONFIG=""
  if [ -n "$ZSH_VERSION" ]; then
    SHELL_CONFIG="$HOME/.zshrc"
  elif [ -n "$BASH_VERSION" ]; then
    SHELL_CONFIG="$HOME/.bashrc"
  else
    # Default to .bashrc
    SHELL_CONFIG="$HOME/.bashrc"
  fi
  
  # Remove old EOS environment variables from shell config
  sed -i.tmp '/^export EOS_ACCESS_KEY=/d; /^export EOS_SECRET_KEY=/d; /^export EOS_REGION=/d; /^export EOS_BUCKET=/d; /^export EOS_ENDPOINT=/d' "$SHELL_CONFIG" 2>/dev/null || true
  rm -f "${SHELL_CONFIG}.tmp" 2>/dev/null || true
  
  # Add new EOS environment variables to shell config
  {
    echo ""
    echo "# Mobile Cloud EOS Environment Variables"
    echo "export EOS_ACCESS_KEY='$ACCESS_KEY'"
    echo "export EOS_SECRET_KEY='$SECRET_KEY'"
    echo "export EOS_REGION='$REGION'"
    echo "export EOS_BUCKET='$BUCKET'"
    echo "export EOS_ENDPOINT='$ENDPOINT'"
  } >> "$SHELL_CONFIG"
  
  log_info "Environment variables set (current session and $SHELL_CONFIG)"
  echo "  EOS_ACCESS_KEY = $ACCESS_KEY"
  echo "  EOS_SECRET_KEY = ***"
  echo "  EOS_REGION = $REGION"
  echo "  EOS_BUCKET = $BUCKET"
  echo "  EOS_ENDPOINT = $ENDPOINT"
  echo ""
  echo "Note: Environment variables are set in $SHELL_CONFIG and will persist across sessions." 
  echo "      Run 'source $SHELL_CONFIG' to load them in the current session, or start a new terminal."

  # 5. Verify
  echo ""
  echo "--- Step 5: Verify Connection ---"
  if (cd "$BASE_DIR" && node scripts/eos_node.mjs list --max-keys 1 2>/dev/null | grep -q '"success": true'); then
    log_info "EOS connection verified successfully"
  else
    log_warn "EOS connection verification failed, please check credentials and network"
  fi

  echo ""
  echo "=== Setup Complete ==="
  echo "You can now use EOS with the following methods:"
  echo "  node $BASE_DIR/scripts/eos_node.mjs <action>"
  echo ""
  echo "Environment variables set for current session and $SHELL_CONFIG:"
  echo "  EOS_ACCESS_KEY"
  echo "  EOS_SECRET_KEY"
  echo "  EOS_REGION"
  echo "  EOS_BUCKET"
  echo "  EOS_ENDPOINT"
  echo ""
  echo "Note: Run 'source $SHELL_CONFIG' to load them in the current session, or start a new terminal."
}

# ========== Set Bucket ==========

do_set_bucket() {
  local BUCKET="$1"

  if [ -z "$BUCKET" ]; then
    echo "Error: Missing bucket name"
    echo "Usage: $0 --set-bucket <bucket>"
    exit 1
  fi

  echo "=== Update Bucket Name ==="
  echo "Updating bucket to: $BUCKET"

  # Update environment variable for current session
  export EOS_BUCKET="$BUCKET"
  
  # Determine shell config file
  SHELL_CONFIG=""
  if [ -n "$ZSH_VERSION" ]; then
    SHELL_CONFIG="$HOME/.zshrc"
  elif [ -n "$BASH_VERSION" ]; then
    SHELL_CONFIG="$HOME/.bashrc"
  else
    # Default to .bashrc
    SHELL_CONFIG="$HOME/.bashrc"
  fi
  
  # Update EOS_BUCKET in shell config
  if [ -f "$SHELL_CONFIG" ]; then
    # Remove old EOS_BUCKET and add new one
    sed -i.tmp '/^export EOS_BUCKET=/d' "$SHELL_CONFIG" 2>/dev/null || true
    rm -f "${SHELL_CONFIG}.tmp" 2>/dev/null || true
    echo "export EOS_BUCKET='$BUCKET'" >> "$SHELL_CONFIG"
  else
    echo "Warning: $SHELL_CONFIG not found, only updating current session"
  fi
  
  log_info "EOS_BUCKET environment variable updated (current session and $SHELL_CONFIG)"
  
  # Verify new bucket is accessible
  echo ""
  echo "--- Verify Bucket Access ---"
  if (cd "$BASE_DIR" && node scripts/eos_node.mjs list --max-keys 1 2>/dev/null | grep -q '"success": true'); then
    log_info "Bucket access verified successfully"
  else
    log_warn "Bucket access verification failed, bucket may not exist or no permission"
  fi

  echo ""
  echo "=== Bucket Update Complete ==="
  echo "New bucket: $BUCKET"
  echo ""
  echo "Note: Bucket name is set in $SHELL_CONFIG and will persist across sessions."
  echo "      Run 'source $SHELL_CONFIG' to load it in the current session, or start a new terminal."
}

# ========== Main Entry ==========

case "$1" in
  --check-only)
    do_check
    ;;
  --set-bucket)
    do_set_bucket "$2"
    ;;
  --copy-config-file)
    do_setup "$@"
    ;;
  --access-key|--secret-key|--region|--bucket|--config-file)
    do_setup "$@"
    ;;
  *)
    echo "Mobile Cloud EOS Skill Setup Tool"
    echo ""
    echo "Usage:"
    echo "  $0 --check-only"
    echo "    Check environment status only"
    echo ""
    echo "  $0 --set-bucket <bucket>"
    echo "    Update bucket name in environment variables (keep other settings)"
    echo ""
    echo "  $0 --access-key <ID> --secret-key <KEY> --region <REGION> --bucket <BUCKET> --endpoint <ENDPOINT>"
    echo "    Auto setup environment (install dependencies + set environment variables + verify connection)"
    echo ""
    echo "  $0 --config-file <path>"
    echo "    Use config file for credentials (properties format)"
    echo "    Config file template: references/config_template.properties"
    echo ""
    echo "  $0 --copy-config-file <path>"
    echo "    Load credentials from config file and set environment variables"
    ;;
esac
