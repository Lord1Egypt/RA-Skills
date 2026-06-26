#!/usr/bin/env bash
set -euo pipefail

detect_image_arch() {
  case "$(uname -m)" in
    x86_64|amd64)
      echo "x64"
      ;;
    aarch64|arm64)
      echo "arm64"
      ;;
    *)
      echo "Unsupported host architecture: $(uname -m)" >&2
      exit 1
      ;;
  esac
}

if [ "$#" -lt 2 ] || [ "$1" != "file" ]; then
  echo "usage: $0 file <path> [args...]" >&2
  exit 2
fi

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
IMAGE_ARCH="${IMAGE_ARCH:-$(detect_image_arch)}"
IMAGE_VERSION="${IMAGE_VERSION:-0.0.1}"
IMAGE_REGISTRY="${IMAGE_REGISTRY:-crpi-4auaoyyj6r36p6lb.cn-hangzhou.personal.cr.aliyuncs.com/huozige_lab}"
IMAGE_BASENAME="convert-document-to-markdown-${IMAGE_ARCH}"
ENV_FILE="${ROOT_DIR}/.env"
DOCKER_ARGS=(run --rm)

case "${IMAGE_ARCH}" in
  x64|arm64)
    ;;
  *)
    echo "Unsupported image architecture: ${IMAGE_ARCH}" >&2
    exit 1
    ;;
esac

if [ -z "${IMAGE_NAME:-}" ] && [ -n "${IMAGE_REGISTRY}" ]; then
  IMAGE_NAME="${IMAGE_REGISTRY}/${IMAGE_BASENAME}:${IMAGE_VERSION}"
elif [ -z "${IMAGE_NAME:-}" ]; then
  IMAGE_NAME="${IMAGE_BASENAME}:${IMAGE_VERSION}"
fi

if [ -f "${ENV_FILE}" ]; then
  DOCKER_ARGS+=(--env-file "${ENV_FILE}")
fi

for env_name in VL_BASE_URL VL_API_KEY VL_MODEL VL_API_TIMEOUT VL_PAGE_TARGET_WIDTH VL_PAGE_MIN_ZOOM VL_PAGE_MAX_ZOOM; do
  if [ -n "${!env_name:-}" ]; then
    DOCKER_ARGS+=(-e "${env_name}=${!env_name}")
  fi
done

if ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
  docker pull "${IMAGE_NAME}" >/dev/null
fi

shift

input_path="$1"
input_dir="$(cd "$(dirname "${input_path}")" && pwd -P)"
input_name="$(basename "${input_path}")"
input_path="${input_dir}/${input_name}"
input_dir="$(dirname "${input_path}")"
shift

exec docker "${DOCKER_ARGS[@]}" \
  -v "${input_dir}:/input:ro" \
  "${IMAGE_NAME}" \
  file "/input/${input_name}" "$@"
