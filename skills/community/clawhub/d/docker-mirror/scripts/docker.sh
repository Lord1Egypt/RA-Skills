#!/bin/bash
# Docker wrapper with automatic mirror failover
# Usage: docker.sh pull <image>[:tag]
# If pull fails, automatically try alternative mirrors

command -v sg >/dev/null 2>&1 || { echo "sg required"; exit 1; }

# If not a pull command, just run directly
if [[ "$1" != "pull" ]]; then
    sg docker -c "docker $*"
    exit $?
fi

IMAGE="$2"
if [[ -z "$IMAGE" ]]; then
    echo "Usage: docker.sh pull <image>[:tag]"
    exit 1
fi

# Mirrors: each entry is "host/namespace" for that mirror
# For official images (no "/" in name), namespace="library"
# For user images (contains "/"), namespace is stripped (user/image passed as-is)
#
# Verified 2026-03-29:
#   docker.1ms.run        →  ✅ 可用，支持 library/ 前缀
#   docker.m.daocloud.io →  ✅ 可用

MIRRORS=(
    "docker.1ms.run:library"               # official images → library/<image>
    "docker.m.daocloud.io:library"         # official images → library/<image>
)

# First try official docker.io (no mirror)
echo "Trying: docker pull $IMAGE"
if sg docker -c "docker pull $IMAGE" 2>&1; then
    echo "Done!"
    exit 0
fi
echo "Failed, trying mirrors..."

# Then try mirrors
for ENTRY in "${MIRRORS[@]}"; do
    HOST="${ENTRY%%:*}"
    NS="${ENTRY#*:}"

    # If image already contains a "/" (user/image format), use image as-is
    # Otherwise prepend namespace (library) for official images
    if [[ "$IMAGE" == *"/"* ]]; then
        MIRROR_PATH="${HOST}/${IMAGE}"
    else
        MIRROR_PATH="${HOST}/${NS}/${IMAGE}"
    fi

    echo "Trying: docker pull $MIRROR_PATH"
    if sg docker -c "docker pull $MIRROR_PATH" 2>&1; then
        # Success — tag back to original image name and clean up
        echo "Tagging $MIRROR_PATH -> $IMAGE"
        sg docker -c "docker tag '$MIRROR_PATH' '$IMAGE'" 2>/dev/null
        echo "Cleaning up"
        sg docker -c "docker rmi '$MIRROR_PATH'" 2>/dev/null
        echo "Done!"
        exit 0
    fi
    echo "Failed, trying next..."
done

echo "All mirrors failed"
exit 1
