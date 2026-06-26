#!/usr/bin/env bash
# 将视频从远程 URL 下载到本地文件。
# 支持 MP4（curl 直接下载）和 HLS（ffmpeg 转封装为 MP4）。
# 下载前校验 URL 来源：必须属于 config.json 的 trusted_media_origins，
# 或由环境变量 WENLV_API_ORIGIN 指定的站点根（两者取并集）。
#
# 用法: bash scripts/download_video.sh "<video_url>" "<output_path>" [HLS|MP4]
#
# 参数:
#   video_url   - 远程视频地址（MP4 直链或 HLS m3u8）
#   output_path - 本地保存路径（如 downloads/Commodity-xxx.mp4）
#   type        - 可选，HLS 或 MP4；未指定时自动判定
#
# 退出码:
#   0 - 下载成功
#   1 - 参数错误
#   2 - 下载失败
#   3 - ffmpeg 未安装（HLS 场景）
#   4 - URL 来源不在 trusted_media_origins 中

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
CONFIG_FILE="$SKILL_ROOT/config.json"

URL="${1:-}"
OUTPUT="${2:-}"
TYPE="${3:-}"

if [[ -z "$URL" || -z "$OUTPUT" ]]; then
  echo "用法: $0 <video_url> <output_path> [HLS|MP4]" >&2
  exit 1
fi

# ── URL 来源校验 ──────────────────────────────────────────────
# 可信来源 = config.json trusted_media_origins ∪ WENLV_API_ORIGIN（若设置）
URL_TRUSTED=false

if [[ ! -f "$CONFIG_FILE" ]]; then
  echo "[download] 错误: 未找到 $CONFIG_FILE，无法加载 trusted_media_origins，拒绝下载" >&2
  exit 4
fi

# 用 python3（macOS 自带）解析 JSON，避免依赖 jq
ORIGINS=$(python3 -c "
import json, sys
with open('$CONFIG_FILE') as f:
    cfg = json.load(f)
origins = cfg.get('trusted_media_origins', [])
if not origins:
    print('__EMPTY__', file=sys.stderr)
    sys.exit(1)
for o in origins:
    print(o)
" 2>/dev/null) || {
  echo "[download] 错误: 无法解析 $CONFIG_FILE 或 trusted_media_origins 为空，拒绝下载" >&2
  exit 4
}

# 若 WENLV_API_ORIGIN 环境变量已设置，追加到可信来源（去掉末尾 /）
if [[ -n "${WENLV_API_ORIGIN:-}" ]]; then
  EXTRA_ORIGIN="${WENLV_API_ORIGIN%/}"
  ORIGINS="${ORIGINS}"$'\n'"${EXTRA_ORIGIN}"
fi

while IFS= read -r origin; do
  if [[ -n "$origin" && "$URL" == "$origin"* ]]; then
    URL_TRUSTED=true
    break
  fi
done <<< "$ORIGINS"

if [[ "$URL_TRUSTED" != "true" ]]; then
  echo "[download] 错误: URL 来源不在可信列表中，拒绝下载" >&2
  echo "[download] URL: $URL" >&2
  echo "[download] 可信来源 (trusted_media_origins + WENLV_API_ORIGIN): $ORIGINS" >&2
  exit 4
fi

# ── 自动判定流类型 ────────────────────────────────────────────
if [[ -z "$TYPE" ]]; then
  if [[ "$URL" == *"/hls/"* ]] || [[ "$URL" == *.m3u8 ]]; then
    TYPE=HLS
  else
    TYPE=MP4
  fi
fi

# ── 确保输出目录存在 ──────────────────────────────────────────
OUTPUT_DIR="$(dirname "$OUTPUT")"
mkdir -p "$OUTPUT_DIR"

# ── 执行下载 ──────────────────────────────────────────────────
case "$TYPE" in
  MP4|mp4)
    echo "[download] MP4 直接下载: $URL" >&2
    echo "[download] 保存到: $OUTPUT" >&2
    if curl -fSL --progress-bar -o "$OUTPUT" "$URL"; then
      echo "[download] 完成: $OUTPUT ($(du -h "$OUTPUT" | cut -f1))" >&2
      echo "$OUTPUT"
      exit 0
    else
      echo "[download] 下载失败" >&2
      exit 2
    fi
    ;;
  HLS|hls)
    if ! command -v ffmpeg &>/dev/null; then
      echo "[download] 错误: HLS 下载需要 ffmpeg，请先安装: brew install ffmpeg" >&2
      exit 3
    fi
    echo "[download] HLS 转封装下载: $URL" >&2
    echo "[download] 保存到: $OUTPUT" >&2
    if ffmpeg -y -i "$URL" -c copy -bsf:a aac_adtstoasc "$OUTPUT" -loglevel warning; then
      echo "[download] 完成: $OUTPUT ($(du -h "$OUTPUT" | cut -f1))" >&2
      echo "$OUTPUT"
      exit 0
    else
      echo "[download] ffmpeg 转封装失败" >&2
      exit 2
    fi
    ;;
  *)
    echo "[download] 未知类型: $TYPE（支持 HLS 或 MP4）" >&2
    exit 1
    ;;
esac
