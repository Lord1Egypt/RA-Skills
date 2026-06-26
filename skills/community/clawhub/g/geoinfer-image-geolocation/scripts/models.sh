#!/bin/bash
# GeoInfer — list available prediction models

# 1. Check for API key
if [ -z "${GEOINFER_API_KEY:-}" ]; then
    echo "Error: GEOINFER_API_KEY is required. Set it with: export GEOINFER_API_KEY=\"your_key\"" >&2
    exit 1
fi

# 2. Fetch models
curl -s -X GET "https://api.geoinfer.com/v1/prediction/models" \
    -H "X-GeoInfer-Key: $GEOINFER_API_KEY"
