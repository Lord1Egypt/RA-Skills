#!/bin/bash
# GeoInfer — predict image location

IMAGE_PATH="$1"
MODEL_ID="${2:-global_v0_1}"
TOP_N="${3:-5}"

# 1. Check for image path
if [ -z "$IMAGE_PATH" ]; then
    echo "Usage: $0 <image_path> [model_id] [top_n]" >&2
    echo "" >&2
    echo "  image_path  Path to image file (JPEG, PNG, WebP, max 10MB)" >&2
    echo "  model_id    Model to use (default: GLOBAL_V0_1)" >&2
    echo "  top_n       Number of predictions to return, 1-15 (default: 5)" >&2
    exit 1
fi

# 2. Check file exists
if [ ! -f "$IMAGE_PATH" ]; then
    echo "Error: File not found: $IMAGE_PATH" >&2
    exit 1
fi

# 3. Check for API key
if [ -z "${GEOINFER_API_KEY:-}" ]; then
    echo "Error: GEOINFER_API_KEY is required. Set it with: export GEOINFER_API_KEY=\"your_key\"" >&2
    exit 1
fi

# 4. Validate top_n range
if [ "$TOP_N" -lt 1 ] || [ "$TOP_N" -gt 15 ] 2>/dev/null; then
    echo "Error: top_n must be between 1 and 15." >&2
    exit 1
fi

# 5. Run prediction
curl -s -X POST "https://api.geoinfer.com/v1/prediction/predict?model_id=${MODEL_ID}&top_n=${TOP_N}" \
    -H "X-GeoInfer-Key: $GEOINFER_API_KEY" \
    -F "file=@${IMAGE_PATH}"
