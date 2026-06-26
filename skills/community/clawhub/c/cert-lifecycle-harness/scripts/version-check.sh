#!/bin/bash
# ═══════════════════════════════════════════════════════════════════════════
# 脚本名：version-check.sh
# 用途：检查 cert-lifecycle-harness 是否有新版本可用（静默执行，失败不阻塞）
# 版本：v1.0
# ───────────────────────────────────────────────────────────────────────────
# 🟢 安全等级：READ-ONLY（只读网络 + 只读本地文件）
# 📏 代码行数：~90
# ⏱  Review 预计用时：3 min
# 👀 Review 关注点：
#   1. 第 42 行：curl 超时 3 秒，失败即退出 0（不阻塞）
#   2. 第 58 行：语义版本对比用 sort -V，只在 remote > local 时提醒
#   3. 第 74 行：任何错误路径都 exit 0（铁律：版本检查失败绝不阻塞主流程）
# 📋 前置依赖：bash、curl、grep、sort、date、stat
# 📦 使用示例：
#   $ bash scripts/version-check.sh
#   CHECK_STATUS=up_to_date
#   LOCAL_VERSION=1.0
#   REMOTE_VERSION=1.0
# 🔁 幂等性：✅ 带 1 天缓存，24h 内重复调用不会重复请求 GitHub
# ═══════════════════════════════════════════════════════════════════════════
#
# 输出字段（stdout，KEY=VALUE 格式，供 Agent 解析）：
#   CHECK_STATUS    up_to_date | needs_update | offline | skipped
#   LOCAL_VERSION   本地 SKILL.md frontmatter 的 version 字段
#   REMOTE_VERSION  GitHub Releases 最新 tag（去掉 v 前缀），offline 时省略
#   UPDATE_CMD      当 needs_update 时给出的更新命令
#
# 铁律：
#   ① 所有错误路径 exit 0（version 检查不是核心功能，不得阻塞 Agent）
#   ② curl 超时硬上限 3s（不能拖慢 Agent 启动）
#   ③ 本脚本的 stdout 是机器可读输出；任何 debug 信息走 stderr
# ═══════════════════════════════════════════════════════════════════════════

set -uo pipefail   # 关键：不用 -e，任何单步失败都降级为 offline，不得 crash

# ── 常量 ───────────────────────────────────────────────────────────────────
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
SKILL_MD="${SKILL_ROOT}/SKILL.md"
CACHE_FILE="${SCRIPT_DIR}/.version-check-cache"
CACHE_TTL=$((24 * 3600))          # 1 天
REPO_API="https://api.github.com/repos/dimayip/cert-lifecycle-harness/releases/latest"
UPDATE_CMD="npx skills add https://github.com/dimayip/cert-lifecycle-harness"
CURL_TIMEOUT=3

# ── 输出函数 ───────────────────────────────────────────────────────────────
emit() {
  # stdout 为机器可读 KEY=VALUE；同时写入缓存（仅非 offline 时）
  local payload="$*"
  printf "%s\n" "${payload}"
}

emit_and_cache() {
  local payload="$*"
  printf "%s\n" "${payload}"
  # 原子写：先写临时文件，再 mv
  printf "%s\n" "${payload}" > "${CACHE_FILE}.tmp" 2>/dev/null \
    && mv "${CACHE_FILE}.tmp" "${CACHE_FILE}" 2>/dev/null \
    || true
}

# ── Step 1：读取本地 version ───────────────────────────────────────────────
LOCAL_VERSION=""
if [ -r "${SKILL_MD}" ]; then
  # 只抓 frontmatter 区域（前 30 行内）的 `version: X.Y` 字段
  LOCAL_VERSION="$(head -n 30 "${SKILL_MD}" 2>/dev/null \
    | grep -E '^version:' \
    | head -n 1 \
    | awk '{print $2}' \
    | tr -d '"' \
    | tr -d "'")"
fi

if [ -z "${LOCAL_VERSION}" ]; then
  emit "CHECK_STATUS=skipped
REASON=local_version_not_found"
  exit 0
fi

# ── Step 2：缓存命中判断（1 天内复用）─────────────────────────────────────
if [ -f "${CACHE_FILE}" ]; then
  # BSD stat (macOS) 用 -f %m，GNU stat (Linux) 用 -c %Y，都试一遍
  mtime="$(stat -f %m "${CACHE_FILE}" 2>/dev/null || stat -c %Y "${CACHE_FILE}" 2>/dev/null || echo 0)"
  now="$(date +%s)"
  age=$(( now - mtime ))
  if [ "${age}" -ge 0 ] && [ "${age}" -lt "${CACHE_TTL}" ]; then
    # 缓存有效，直接回放
    cat "${CACHE_FILE}" 2>/dev/null
    exit 0
  fi
fi

# ── Step 3：联网拉取最新 Release tag ──────────────────────────────────────
# 不需要 jq，用 grep + sed 解析即可（依赖最少）
REMOTE_RAW="$(curl -fsSL \
  --max-time "${CURL_TIMEOUT}" \
  --connect-timeout 2 \
  -H 'Accept: application/vnd.github+json' \
  "${REPO_API}" 2>/dev/null)" || REMOTE_RAW=""

if [ -z "${REMOTE_RAW}" ]; then
  emit "CHECK_STATUS=offline
LOCAL_VERSION=${LOCAL_VERSION}
REASON=fetch_failed"
  # 注意：不缓存 offline 结果，下次 Agent 启动会再试（因为网络通常是临时问题）
  exit 0
fi

# 从 JSON 响应里抓 "tag_name": "vX.Y.Z"
REMOTE_TAG="$(printf "%s" "${REMOTE_RAW}" \
  | grep -E '"tag_name"' \
  | head -n 1 \
  | sed -E 's/.*"tag_name"[[:space:]]*:[[:space:]]*"([^"]+)".*/\1/')"

# 去掉 v 前缀（v1.0 → 1.0）
REMOTE_VERSION="${REMOTE_TAG#v}"
REMOTE_VERSION="${REMOTE_VERSION#V}"

if [ -z "${REMOTE_VERSION}" ]; then
  emit "CHECK_STATUS=offline
LOCAL_VERSION=${LOCAL_VERSION}
REASON=parse_failed"
  exit 0
fi

# ── Step 4：语义版本对比（sort -V）────────────────────────────────────────
# 规则：只有 remote 严格大于 local 时才 needs_update
# 相等或 local 更新（本地 dev 版本）都算 up_to_date
HIGHEST="$(printf "%s\n%s\n" "${LOCAL_VERSION}" "${REMOTE_VERSION}" \
  | sort -V \
  | tail -n 1)"

if [ "${HIGHEST}" = "${REMOTE_VERSION}" ] && [ "${LOCAL_VERSION}" != "${REMOTE_VERSION}" ]; then
  emit_and_cache "CHECK_STATUS=needs_update
LOCAL_VERSION=${LOCAL_VERSION}
REMOTE_VERSION=${REMOTE_VERSION}
UPDATE_CMD=${UPDATE_CMD}"
else
  emit_and_cache "CHECK_STATUS=up_to_date
LOCAL_VERSION=${LOCAL_VERSION}
REMOTE_VERSION=${REMOTE_VERSION}"
fi

exit 0
