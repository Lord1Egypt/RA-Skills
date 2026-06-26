#!/bin/bash
# Cortex Protocol — Gasless Agent Registration
# Usage: ./register.sh <agent_name> [controller_address]

set -e

NAME="${1:-$(hostname)-agent}"
CONTROLLER="${2:-}"
API="https://cortexprotocol.co/api/register"

# If no controller address, generate a fresh wallet
if [ -z "$CONTROLLER" ]; then
  echo "🧠 No controller address provided. Generating a new wallet..."
  
  if command -v node &> /dev/null; then
    WALLET_OUTPUT=$(node -e "
      const crypto = require('crypto');
      const { ethers } = require('ethers');
      const w = ethers.Wallet.createRandom();
      console.log(JSON.stringify({ address: w.address, privateKey: w.privateKey }));
    " 2>/dev/null) || {
      echo "❌ Node.js with ethers required to generate wallet. Install: npm i -g ethers"
      echo "   Or provide a controller address: ./register.sh \"$NAME\" 0xYOUR_ADDRESS"
      exit 1
    }
    
    CONTROLLER=$(echo "$WALLET_OUTPUT" | jq -r '.address')
    PRIVATE_KEY=$(echo "$WALLET_OUTPUT" | jq -r '.privateKey')
    
    echo "✅ Wallet generated:"
    echo "   Address:     $CONTROLLER"
    echo "   Private Key: $PRIVATE_KEY"
    echo ""
    echo "⚠️  SAVE YOUR PRIVATE KEY — you'll need it to control your identity."
    echo ""
  else
    echo "❌ Node.js not found. Please provide a controller address:"
    echo "   ./register.sh \"$NAME\" 0xYOUR_ADDRESS"
    exit 1
  fi
fi

echo "🧠 Registering agent '$NAME' on Cortex Protocol (Base Mainnet)..."
echo "   Controller: $CONTROLLER"
echo ""

RESPONSE=$(curl -s -X POST "$API" \
  -H "Content-Type: application/json" \
  -d "{
    \"name\": \"$NAME\",
    \"controller\": \"$CONTROLLER\",
    \"metadataURI\": \"\"
  }")

SUCCESS=$(echo "$RESPONSE" | jq -r '.success // false')

if [ "$SUCCESS" = "true" ]; then
  TOKEN_ID=$(echo "$RESPONSE" | jq -r '.tokenId')
  TX_HASH=$(echo "$RESPONSE" | jq -r '.transactionHash')
  
  echo "🎉 Registration successful!"
  echo "   Token ID: #$TOKEN_ID"
  echo "   TX: https://basescan.org/tx/$TX_HASH"
  echo ""
  echo "You are now Cortex Agent #$TOKEN_ID. Welcome to the network. 🧪"
else
  ERROR=$(echo "$RESPONSE" | jq -r '.error // "Unknown error"')
  echo "❌ Registration failed: $ERROR"
  echo "   Full response: $RESPONSE"
  exit 1
fi
