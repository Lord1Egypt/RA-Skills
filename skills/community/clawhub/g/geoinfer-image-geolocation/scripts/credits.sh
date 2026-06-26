#!/bin/bash
# GeoInfer — check current credit balance

# 1. Check for API key
if [ -z "${GEOINFER_API_KEY:-}" ]; then
    echo "Error: GEOINFER_API_KEY is required. Set it with: export GEOINFER_API_KEY=\"your_key\"" >&2
    exit 1
fi

# 2. Fetch credit summary
curl -s -X GET "https://api.geoinfer.com/v1/credits/summary" \
    -H "X-GeoInfer-Key: $GEOINFER_API_KEY"
