#!/bin/bash
# Generate a new AIOZ Pin API key
# Usage: ./generate_api_key.sh JWT_TOKEN KEY_NAME [admin] [pinList] [nftList] [unpin] [pinByHash] [pinFileToIPFS] [unpinNFT] [pinNFTToIPFS]

JWT_TOKEN="$1"
KEY_NAME="$2"
ADMIN="${3:-false}"
PIN_LIST="${4:-false}"
NFT_LIST="${5:-false}"
UNPIN="${6:-false}"
PIN_BY_HASH="${7:-false}"
PIN_FILE_TO_IPFS="${8:-false}"
UNPIN_NFT="${9:-false}"
PIN_NFT_TO_IPFS="${10:-false}"

if [ -z "$JWT_TOKEN" ] || [ -z "$KEY_NAME" ]; then
    echo "Usage: $0 JWT_TOKEN KEY_NAME [admin] [pinList] [nftList] [unpin] [pinByHash] [pinFileToIPFS] [unpinNFT] [pinNFTToIPFS]"
    exit 1
fi

# Normalize bool input to true/false so JSON payload stays valid.
to_bool() {
    case "${1,,}" in
        true|1|yes|y) echo "true" ;;
        *) echo "false" ;;
    esac
}

ADMIN="$(to_bool "$ADMIN")"
PIN_LIST="$(to_bool "$PIN_LIST")"
NFT_LIST="$(to_bool "$NFT_LIST")"
UNPIN="$(to_bool "$UNPIN")"
PIN_BY_HASH="$(to_bool "$PIN_BY_HASH")"
PIN_FILE_TO_IPFS="$(to_bool "$PIN_FILE_TO_IPFS")"
UNPIN_NFT="$(to_bool "$UNPIN_NFT")"
PIN_NFT_TO_IPFS="$(to_bool "$PIN_NFT_TO_IPFS")"

REQUEST_URL="https://api.aiozpin.network/api/apiKeys/"
REQUEST_BODY=$(cat <<EOF
{
  "name": "$KEY_NAME",
  "scopes": {
    "admin": $ADMIN,
    "data": {
      "pin_list": $PIN_LIST,
      "nft_list": $NFT_LIST
    },
    "pinning": {
      "unpin": $UNPIN,
      "pin_by_hash": $PIN_BY_HASH,
      "pin_file_to_ipfs": $PIN_FILE_TO_IPFS
    },
    "pin_nft": {
      "unpin_nft": $UNPIN_NFT,
      "pin_nft_to_ipfs": $PIN_NFT_TO_IPFS
    }
  }
}
EOF
)

# Print request URL before calling API
echo "Request URL: $REQUEST_URL"

# Send request to generate API key
RESPONSE=$(curl -s --location --request POST "$REQUEST_URL" \
  -H "Authorization: Bearer $JWT_TOKEN" \
  -H "Content-Type: application/json" \
  --data-raw "$REQUEST_BODY")

echo "$RESPONSE" | jq . || echo "$RESPONSE"
