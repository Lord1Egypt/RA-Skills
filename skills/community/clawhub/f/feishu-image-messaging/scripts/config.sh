#!/bin/bash
# Feishu API Configuration
# Credentials are read from environment variables for security

# Check if required environment variables are set
if [[ -z "${FEISHU_APP_ID:-}" || -z "${FEISHU_APP_SECRET:-}" ]]; then
  echo "Error: FEISHU_APP_ID and FEISHU_APP_SECRET must be set in environment" >&2
  echo "Example:" >&2
  echo "  export FEISHU_APP_ID='cli_xxxxxx'" >&2
  echo "  export FEISHU_APP_SECRET='xxxxxx'" >&2
  exit 1
fi

# Export credentials from environment
export FEISHU_APP_ID
export FEISHU_APP_SECRET

# API Endpoints
export FEISHU_API_BASE="https://open.larksuite.com/open-apis"
export FEISHU_AUTH_ENDPOINT="${FEISHU_API_BASE}/auth/v3/tenant_access_token/internal"
export FEISHU_IMAGE_UPLOAD_ENDPOINT="${FEISHU_API_BASE}/im/v1/images"
export FEISHU_MESSAGE_ENDPOINT="${FEISHU_API_BASE}/im/v1/messages"
