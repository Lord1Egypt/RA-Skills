#!/usr/bin/env bash
#
# 抖音视频工作流：下载 → OSS上传 → 飞书多维表格写入
#
# 用法:
#   ./douyin-workflow.sh <抖音链接> [--dry-run] [--skip-feishu] [--skip-oss]
#
# 环境变量 (必需):
#   ALIYUN_OSS_ACCESS_KEY_ID, ALIYUN_OSS_ACCESS_KEY_SECRET
#   ALIYUN_OSS_ENDPOINT, ALIYUN_OSS_BUCKET
#   FEISHU_APP_ID, FEISHU_APP_SECRET
#
# 环境变量 (可选):
#   FEISHU_BITABLE_APP_TOKEN  - 多维表格 app_token (设置后跳过wiki查询)
#   FEISHU_BITABLE_TABLE_ID   - 表格ID
#   FEISHU_WIKI_TOKEN         - Wiki节点token (当表格在wiki中时需要)
#   DOUYIN_DOWNLOAD_DIR       - 下载目录 (默认: /tmp/douyin-download)
#   OSS_PREFIX                - OSS路径前缀 (默认: douyin)
#

set -euo pipefail

# ============================================================
# 颜色输出
# ============================================================
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; BLUE='\033[0;34m'; NC='\033[0m'
info()  { echo -e "${BLUE}[INFO]${NC}  $*"; }
ok()    { echo -e "${GREEN}[OK]${NC}    $*"; }
warn()  { echo -e "${YELLOW}[WARN]${NC}  $*"; }
err()   { echo -e "${RED}[ERROR]${NC} $*" >&2; }
die()   { err "$*"; exit 1; }

# ============================================================
# 自动探测 skill 路径
# ============================================================
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
SKILLS_ROOT="$(dirname "$SKILL_DIR")"

DOUYIN_SCRIPT="${SKILLS_ROOT}/douyin-download/douyin.js"
OSS_SCRIPT="${SKILLS_ROOT}/aliyun-oss-upload/scripts/oss-upload.py"

# ============================================================
# 默认配置
# ============================================================
DOWNLOAD_DIR="${DOUYIN_DOWNLOAD_DIR:-/tmp/douyin-download}"
OSS_PREFIX="${OSS_PREFIX:-douyin}"

DRY_RUN=false
SKIP_FEISHU=false
SKIP_OSS=false

# ============================================================
# 参数解析
# ============================================================
DOUYIN_URL=""
for arg in "$@"; do
  case "$arg" in
    --dry-run)     DRY_RUN=true ;;
    --skip-feishu) SKIP_FEISHU=true ;;
    --skip-oss)    SKIP_OSS=true ;;
    --help|-h)
      echo "用法: $0 <抖音链接> [--dry-run] [--skip-feishu] [--skip-oss]"
      exit 0
      ;;
    *)
      if [[ -z "$DOUYIN_URL" ]]; then
        DOUYIN_URL="$arg"
      fi
      ;;
  esac
done

[[ -z "$DOUYIN_URL" ]] && die "请提供抖音视频链接"

# ============================================================
# 从分享文本中提取URL
# ============================================================
EXTRACTED_URL=$(echo "$DOUYIN_URL" | grep -oE 'https?://[^ ]+' | head -1)
if [[ -n "$EXTRACTED_URL" ]]; then
  DOUYIN_URL="$EXTRACTED_URL"
fi

# ============================================================
# 前置验证
# ============================================================
info "前置验证..."

# 1. 验证链接格式
if ! echo "$DOUYIN_URL" | grep -qE '(douyin\.com|iesdouyin\.com)'; then
  die "无效的抖音链接: $DOUYIN_URL"
fi

# 2. 验证必要工具
command -v node    >/dev/null 2>&1 || die "缺少 node"
command -v python3 >/dev/null 2>&1 || die "缺少 python3"
command -v curl    >/dev/null 2>&1 || die "缺少 curl"

# 3. 验证依赖 skill
[[ -f "$DOUYIN_SCRIPT" ]] || die "缺少依赖 skill: douyin-download (期望路径: $DOUYIN_SCRIPT)\n  安装: clawhub install douyin-download"
[[ -f "$OSS_SCRIPT" ]]    || die "缺少依赖 skill: aliyun-oss-upload (期望路径: $OSS_SCRIPT)\n  安装: clawhub install aliyun-oss-upload"

# 4. 验证环境变量
if [[ "$SKIP_OSS" == false ]]; then
  [[ -n "${ALIYUN_OSS_ACCESS_KEY_ID:-}" ]]    || die "未设置 ALIYUN_OSS_ACCESS_KEY_ID"
  [[ -n "${ALIYUN_OSS_ACCESS_KEY_SECRET:-}" ]] || die "未设置 ALIYUN_OSS_ACCESS_KEY_SECRET"
  [[ -n "${ALIYUN_OSS_ENDPOINT:-}" ]]          || die "未设置 ALIYUN_OSS_ENDPOINT"
  [[ -n "${ALIYUN_OSS_BUCKET:-}" ]]            || die "未设置 ALIYUN_OSS_BUCKET"
fi

if [[ "$SKIP_FEISHU" == false ]]; then
  [[ -n "${FEISHU_APP_ID:-}" ]]     || die "未设置 FEISHU_APP_ID"
  [[ -n "${FEISHU_APP_SECRET:-}" ]] || die "未设置 FEISHU_APP_SECRET"
  # 必须有 app_token 或 wiki_token 之一
  if [[ -z "${FEISHU_BITABLE_APP_TOKEN:-}" ]] && [[ -z "${FEISHU_WIKI_TOKEN:-}" ]]; then
    die "未设置 FEISHU_BITABLE_APP_TOKEN 或 FEISHU_WIKI_TOKEN (至少需要一个)"
  fi
  [[ -n "${FEISHU_BITABLE_TABLE_ID:-}" ]] || die "未设置 FEISHU_BITABLE_TABLE_ID"
fi

ok "前置验证通过"

# ============================================================
# Step 1: 获取视频信息
# ============================================================
info "Step 1/4: 获取视频信息..."

VIDEO_INFO=$(node "$DOUYIN_SCRIPT" info "$DOUYIN_URL" 2>&1) || die "获取视频信息失败:\n$VIDEO_INFO"

VIDEO_ID=$(echo "$VIDEO_INFO" | grep '视频ID:' | sed 's/.*视频ID: //')
FULL_TITLE=$(echo "$VIDEO_INFO" | grep '标题:' | sed 's/.*标题: //')

[[ -z "$VIDEO_ID" ]] && die "无法提取视频ID"
[[ -z "$FULL_TITLE" ]] && die "无法提取视频标题"

# 智能提取：热点词 = 去掉#标签后的纯文本
KEYWORDS=$(echo "$FULL_TITLE" | sed 's/#[^ ]*//g' | sed 's/，/ /g; s/,/ /g' | xargs)
# 智能提取：话题 = 所有#标签
TAGS=$(echo "$FULL_TITLE" | grep -oE '#[^ #]+' | tr '\n' ' ' | xargs)

ok "视频ID: $VIDEO_ID"
ok "标题: $FULL_TITLE"
ok "热点词: $KEYWORDS"
ok "话题: $TAGS"

if [[ "$DRY_RUN" == true ]]; then
  info "[DRY-RUN] 跳过后续步骤"
  exit 0
fi

# ============================================================
# Step 2: 下载视频
# ============================================================
info "Step 2/4: 下载视频..."

mkdir -p "$DOWNLOAD_DIR"
VIDEO_FILE="$DOWNLOAD_DIR/${VIDEO_ID}.mp4"

if [[ -f "$VIDEO_FILE" ]]; then
  warn "文件已存在，跳过下载: $VIDEO_FILE"
else
  node "$DOUYIN_SCRIPT" download "$DOUYIN_URL" -o "$DOWNLOAD_DIR" 2>&1 | tail -1
fi

[[ -f "$VIDEO_FILE" ]] || die "下载失败，文件不存在: $VIDEO_FILE"

FILE_SIZE=$(du -h "$VIDEO_FILE" | cut -f1)
ok "下载完成: $VIDEO_FILE ($FILE_SIZE)"

# ============================================================
# Step 3: 上传到OSS
# ============================================================
OSS_KEY="${OSS_PREFIX}/${VIDEO_ID}.mp4"
OSS_URL=""

if [[ "$SKIP_OSS" == true ]]; then
  warn "跳过OSS上传"
else
  info "Step 3/4: 上传到OSS..."

  OSS_OUTPUT=$(python3 "$OSS_SCRIPT" upload --file "$VIDEO_FILE" --key "$OSS_KEY" 2>&1) || die "OSS上传失败:\n$OSS_OUTPUT"

  ENDPOINT_HOST=$(echo "$ALIYUN_OSS_ENDPOINT" | sed 's|https\?://||')
  OSS_URL="https://${ALIYUN_OSS_BUCKET}.${ENDPOINT_HOST}/${OSS_KEY}"

  ok "OSS上传完成: $OSS_URL"
fi

# ============================================================
# Step 4: 写入飞书多维表格
# ============================================================
if [[ "$SKIP_FEISHU" == true ]]; then
  warn "跳过飞书写入"
else
  info "Step 4/4: 写入飞书多维表格..."

  # 获取 tenant_access_token
  TOKEN_RESP=$(curl -s -X POST "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal" \
    -H "Content-Type: application/json" \
    -d "{\"app_id\":\"${FEISHU_APP_ID}\",\"app_secret\":\"${FEISHU_APP_SECRET}\"}")

  TENANT_TOKEN=$(echo "$TOKEN_RESP" | python3 -c "import sys,json; print(json.load(sys.stdin).get('tenant_access_token',''))" 2>/dev/null)
  [[ -z "$TENANT_TOKEN" ]] && die "获取飞书token失败: $TOKEN_RESP"

  # 获取 bitable app_token
  APP_TOKEN="${FEISHU_BITABLE_APP_TOKEN:-}"
  if [[ -z "$APP_TOKEN" ]]; then
    WIKI_RESP=$(curl -s "https://open.feishu.cn/open-apis/wiki/v2/spaces/get_node?token=${FEISHU_WIKI_TOKEN}" \
      -H "Authorization: Bearer ${TENANT_TOKEN}")
    APP_TOKEN=$(echo "$WIKI_RESP" | python3 -c "import sys,json; print(json.load(sys.stdin).get('data',{}).get('node',{}).get('obj_token',''))" 2>/dev/null)
    [[ -z "$APP_TOKEN" ]] && die "获取bitable app_token失败: $WIKI_RESP"
  fi

  TABLE_ID="${FEISHU_BITABLE_TABLE_ID}"

  # JSON转义
  ESCAPED_TITLE=$(echo "$FULL_TITLE" | python3 -c "import sys,json; print(json.dumps(sys.stdin.read().strip()))")
  ESCAPED_KEYWORDS=$(echo "$KEYWORDS" | python3 -c "import sys,json; print(json.dumps(sys.stdin.read().strip()))")
  ESCAPED_TAGS=$(echo "$TAGS" | python3 -c "import sys,json; print(json.dumps(sys.stdin.read().strip()))")

  RECORD_BODY=$(cat <<EOF
{
  "fields": {
    "热点词": ${ESCAPED_KEYWORDS},
    "大概描述": ${ESCAPED_TITLE},
    "视频原始地址": "https://www.douyin.com/video/${VIDEO_ID}",
    "阿里OSS地址": "${OSS_URL}",
    "话题": ${ESCAPED_TAGS},
    "状态": "未制作"
  }
}
EOF
  )

  RECORD_RESP=$(curl -s -X POST \
    "https://open.feishu.cn/open-apis/bitable/v1/apps/${APP_TOKEN}/tables/${TABLE_ID}/records" \
    -H "Authorization: Bearer ${TENANT_TOKEN}" \
    -H "Content-Type: application/json" \
    -d "$RECORD_BODY")

  RECORD_ID=$(echo "$RECORD_RESP" | python3 -c "import sys,json; print(json.load(sys.stdin).get('data',{}).get('record',{}).get('record_id',''))" 2>/dev/null)
  [[ -z "$RECORD_ID" ]] && die "飞书写入失败: $RECORD_RESP"

  ok "飞书写入完成: record_id=$RECORD_ID"
fi

# ============================================================
# 汇总
# ============================================================
echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN} ✅ 工作流执行完成${NC}"
echo -e "${GREEN}========================================${NC}"
echo "  视频ID:    $VIDEO_ID"
echo "  标题:      $FULL_TITLE"
echo "  热点词:    $KEYWORDS"
echo "  话题:      $TAGS"
echo "  本地文件:  $VIDEO_FILE ($FILE_SIZE)"
[[ -n "$OSS_URL" ]] && echo "  OSS地址:   $OSS_URL"
[[ -n "${RECORD_ID:-}" ]] && echo "  飞书记录:  $RECORD_ID"
echo ""
