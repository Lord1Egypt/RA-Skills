#!/bin/bash
# snapshot-dir.sh — 目录快照脚本
# 用法：./snapshot-dir.sh <源目录> <快照根目录> <版本标签> [项目ID]
# 示例：./snapshot-dir.sh "03_PPT框架协作包/08_v4审核收口版" "__snapshots" "v4" "SG-PPT"
# 返回码：0=成功, 1=参数错误, 2=源目录不存在, 3=快照失败

set -e

SRC_DIR="${1:-}"
SNAPSHOT_ROOT="${2:-__snapshots}"
VERSION_LABEL="${3:-$(date +%Y%m%d-%H%M%S)}"
PROJECT_ID="${4:-snapshot}"

if [[ -z "$SRC_DIR" ]]; then
  echo "用法: $0 <源目录> <快照根目录> <版本标签> [项目ID]"
  echo "示例: $0 \"03_PPT框架协作包/08_v4审核收口版\" \"__snapshots\" \"v4\" \"SG-PPT\""
  exit 1
fi

if [[ ! -d "$SRC_DIR" ]]; then
  echo "错误: 源目录不存在: $SRC_DIR"
  exit 2
fi

SNAPSHOT_DIR="${SNAPSHOT_ROOT}/${PROJECT_ID}_${VERSION_LABEL}_$(date +%Y%m%d-%H%M%S)"
echo "快照目标: $SNAPSHOT_DIR"

# 创建快照根目录
mkdir -p "$SNAPSHOT_ROOT"

# 复制目录（排除大文件和系统目录）
echo "正在复制文件..."
rsync -a \
  --exclude='node_modules' \
  --exclude='.git' \
  --exclude='__pycache__' \
  --exclude='*.log' \
  --exclude='*.pdf' \
  --exclude='*.mp4' \
  --exclude='*.zip' \
  --exclude='*.tar.gz' \
  --exclude='.DS_Store' \
  "$SRC_DIR/" "$SNAPSHOT_DIR/"

if [[ $? -ne 0 ]]; then
  echo "错误: 文件复制失败"
  exit 3
fi

# 生成快照元数据
cat > "${SNAPSHOT_DIR}/__snapshot_meta.json" << EOF
{
  "schema_version": "1.0",
  "snapshot_version": "${VERSION_LABEL}",
  "source_dir": "${SRC_DIR}",
  "snapshot_dir": "${SNAPSHOT_DIR}",
  "project_id": "${PROJECT_ID}",
  "created": "$(date '+%Y-%m-%dT%H:%M:%S+08:00')",
  "file_count": $(find "$SNAPSHOT_DIR" -type f | wc -l | tr -d ' '),
  "size_bytes": $(du -sb "$SNAPSHOT_DIR" 2>/dev/null | cut -f1 || echo 0)
}
EOF

echo "✅ 快照完成"
echo "快照目录: $SNAPSHOT_DIR"
echo "文件数: $(find "$SNAPSHOT_DIR" -type f | wc -l | tr -d ' ')"
echo "元数据: ${SNAPSHOT_DIR}/__snapshot_meta.json"
