#!/usr/bin/env bash
# dsh-sync.sh —— 把 DSH 官方源码拉取/更新到本 skill 的 vendor/ 目录，作为「引用源」。
#
# 为什么需要它：本 skill 的 API 事实是冻结快照。当你要开发的 DSH 版本高于快照基线时，
# 唯一的权威是当前源码。本脚本把源码放进 skill 目录，让核验与后续增量更新都在本地完成。
#
# 设计约束（有意为之）：
#   1. 首次克隆约 200 MB，必须由开发者确认后才动手（除非显式 --yes）。
#   2. 拉下来的是「引用源」，不是依赖：绝不执行 pnpm install / npm install。
#   3. 只读使用：不修改、不构建、不运行拉下来的代码。
#   4. 网络不通时给出可操作的指引，而不是抛一堆 git 报错。
#
# 用法：
#   bash dsh-sync.sh                  # 交互确认后克隆或更新
#   bash dsh-sync.sh --yes            # 跳过确认
#   bash dsh-sync.sh --check-only     # 只探测远端最新状态，不下载
#   bash dsh-sync.sh --tarball        # 降级：只拉 master 源码快照（约 1 次 HTTP，无 git 历史）
#   bash dsh-sync.sh --shallow        # 浅克隆：只要最新代码，不要 tag 历史
#   bash dsh-sync.sh --mirror <前缀>  # 走镜像，例如 --mirror https://ghfast.top/
#   bash dsh-sync.sh --repo <URL>     # 自定义仓库地址
set -uo pipefail

REPO_URL="https://github.com/deepseek-ai/deepseek-harness.git"
MIRROR=""
ASSUME_YES=0
CHECK_ONLY=0
USE_TARBALL=0
SHALLOW=0

while [ $# -gt 0 ]; do
  case "$1" in
    --yes|-y)      ASSUME_YES=1 ;;
    --check-only)  CHECK_ONLY=1 ;;
    --tarball)     USE_TARBALL=1 ;;
    --shallow)     SHALLOW=1 ;;
    --mirror)      MIRROR="${2:-}"; shift ;;
    --repo)        REPO_URL="${2:-}"; shift ;;
    -h|--help)     sed -n '2,30p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
    *) echo "未知参数: $1（用 --help 看用法）" >&2; exit 2 ;;
  esac
  shift
done

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
VENDOR="$SKILL_DIR/vendor"
SRC_DIR="$VENDOR/dsh-src"
SNAP_DIR="$VENDOR/dsh-snapshot"
STATE="$VENDOR/dsh-state.json"

if [ -n "$MIRROR" ]; then
  case "$MIRROR" in */) ;; *) MIRROR="$MIRROR/" ;; esac
  FETCH_URL="${MIRROR}${REPO_URL}"
else
  FETCH_URL="$REPO_URL"
fi

say()  { printf '%s\n' "$*"; }
hr()   { printf '%s\n' "────────────────────────────────────────────────────────────"; }
warn() { printf '\033[33m%s\033[0m\n' "$*"; }
ok()   { printf '\033[32m%s\033[0m\n' "$*"; }
err()  { printf '\033[31m%s\033[0m\n' "$*" >&2; }

# ── git 调用统一入口：低带宽保护，避免在无网环境挂死 ────────────────────────
g() {
  git -c http.lowSpeedLimit=1000 -c http.lowSpeedTime=30 -c advice.detachedHead=false "$@"
}

# ── 1. 远端探测 ──────────────────────────────────────────────────────────────
say "════ DSH 源码同步 ════"
hr
say "仓库    : $FETCH_URL"
say "目标目录: $SRC_DIR"
[ -n "$MIRROR" ] && say "镜像前缀: $MIRROR"
hr

say "→ 探测远端可达性…"
REMOTE_TAGS=""
if REMOTE_TAGS=$(g timeout 90 git ls-remote --tags --refs "$FETCH_URL" 2>&1); then
  COUNT=$(printf '%s\n' "$REMOTE_TAGS" | grep -c 'refs/tags/' || true)
  LATEST_TAG=$(printf '%s\n' "$REMOTE_TAGS" | sed 's|.*refs/tags/||' | sort -V | tail -1)
  ok "  远端可达，共 $COUNT 个 tag，最新 tag：$LATEST_TAG"
else
  err "  远端不可达。git 报错如下："
  printf '%s\n' "$REMOTE_TAGS" | sed 's/^/    /' | head -6
  hr
  warn "处理建议（按成本从低到高）："
  cat <<'TIP'
    1) 配代理后重试：
         export https_proxy=http://127.0.0.1:7890
         export http_proxy=http://127.0.0.1:7890
    2) 用镜像前缀重试（示例，前缀域名请自行确认可用）：
         bash dsh-sync.sh --mirror https://ghfast.top/ --check-only
    3) 改用轻量快照模式（只需要源码、不需要 tag 历史）：
         bash dsh-sync.sh --tarball
    4) 已有本地仓库？直接把它指过来，不联网也行：
         bash dsh-api-probe.sh <你本地的 deepseek-harness 路径>
    ★ 不要用「凭印象写 API」来绕过网络问题。查不到就如实说查不到。
TIP
  if [ "$CHECK_ONLY" -eq 1 ]; then exit 3; fi
  exit 3
fi
hr

if [ "$CHECK_ONLY" -eq 1 ]; then
  ok "仅探测模式结束。要下载请去掉 --check-only。"
  exit 0
fi

# ── 2. 开发者确认 ────────────────────────────────────────────────────────────
if [ "$ASSUME_YES" -eq 0 ]; then
  if [ -d "$SRC_DIR/.git" ]; then
    say "已存在本地副本，将执行增量更新（只拉新增对象，非 200 MB）。"
  else
    warn "首次克隆需要下载约 200 MB（.git 约 190 MB + 工作树），耗时取决于网络。"
    say  "拉下来的源码仅作「引用源」用于核验 API 与查变更历史。"
    warn "本脚本不会、也不应执行 pnpm install —— 它不是依赖，不要在 skill 目录里装它。"
  fi
  printf '%s' "确认继续？[y/N] "
  read -r ans
  case "$ans" in y|Y|yes|YES) ;; *) say "已取消，未做任何改动。"; exit 0 ;; esac
fi

mkdir -p "$VENDOR"

# ── 3a. tarball 降级路径 ─────────────────────────────────────────────────────
if [ "$USE_TARBALL" -eq 1 ]; then
  say "→ tarball 模式：拉取 master 源码快照（无 git 历史）"
  TAR="$VENDOR/dsh-master.tar.gz"
  BASE="${FETCH_URL%.git}"
  case "$BASE" in
    *codeload.github.com*) TARBALL_URL="$BASE/tar.gz/refs/heads/master" ;;
    *) TARBALL_URL="${BASE%/}/../../codeload.github.com/deepseek-ai/deepseek-harness/tar.gz/refs/heads/master" ;;
  esac
  # 直接走 codeload 最稳（已验证可用），镜像前缀对它无效，故显式构造
  TARBALL_URL="https://codeload.github.com/deepseek-ai/deepseek-harness/tar.gz/refs/heads/master"
  if [ -n "$MIRROR" ]; then TARBALL_URL="${MIRROR}${TARBALL_URL}"; fi
  say "  来源: $TARBALL_URL"
  if ! curl -fL --connect-timeout 20 --max-time 600 -o "$TAR" "$TARBALL_URL"; then
    err "  下载失败。参考上面的代理/镜像建议。"
    exit 4
  fi
  if ! gzip -t "$TAR" 2>/dev/null; then
    err "  下载物不是完整的 gzip（可能被网关拦了）。文件留作排查：$TAR"
    exit 4
  fi
  rm -rf "$SNAP_DIR"; mkdir -p "$SNAP_DIR"
  # --force-local：Windows 上 "D:/..." 的冒号会被 tar 当成「远程主机:文件」语法
  if ! tar --force-local -xzf "$TAR" -C "$SNAP_DIR" --strip-components=1; then
    err "  解压失败。"; exit 4
  fi
  n=$(find "$SNAP_DIR" -type f | wc -l)
  if [ "$n" -lt 1000 ]; then
    err "  解压后仅 $n 个文件，明显不完整（阈值 1000）。"
    exit 4
  fi
  rm -f "$TAR"
  ok "  快照完成：$SNAP_DIR（$n 个文件）"
  warn "  注意：tarball 快照没有 tag 历史，dsh-version-diff.sh 需要 git 仓库才能出完整差异。"
  say  "  下一步：bash $SCRIPT_DIR/dsh-api-probe.sh $SNAP_DIR"
  write_state() { :; }
  write_state
  exit 0
fi

# ── 3b. git 主路径 ───────────────────────────────────────────────────────────
if [ -d "$SRC_DIR/.git" ]; then
  say "→ 增量更新…"
  if ! g -C "$SRC_DIR" remote set-url origin "$FETCH_URL"; then
    warn "  设置 remote 失败，继续尝试 fetch。"
  fi
  if ! g -C "$SRC_DIR" fetch --tags --prune origin 2>&1 | tail -6; then
    err "  fetch 失败。本地副本保持原状（不破坏已有数据）。"
    exit 5
  fi
  if ! g -C "$SRC_DIR" checkout master 2>/dev/null; then
    g -C "$SRC_DIR" checkout -B master origin/master || {
      err "  无法切换到 master。"; exit 5; }
  fi
  if ! g -C "$SRC_DIR" merge --ff-only origin/master 2>&1 | tail -3; then
    warn "  快进合并失败（本地分支可能被改过）。已停在当前状态，源码仍可核验。"
  fi
  ok "  更新完成。"
else
  say "→ 首次克隆…"
  rm -rf "$SRC_DIR"
  CLONE_ARGS=(--branch master)
  if [ "$SHALLOW" -eq 1 ]; then
    CLONE_ARGS+=(--depth 1)
    warn "  浅克隆模式：不含 tag 历史，dsh-version-diff.sh 的逐区间对比将不可用。"
  fi
  if ! g clone "${CLONE_ARGS[@]}" "$FETCH_URL" "$SRC_DIR"; then
    err "  克隆失败。检查网络/代理/镜像后重试；也可先试 --tarball。"
    rm -rf "$SRC_DIR"
    exit 5
  fi
  ok "  克隆完成。"
fi

# ── 4. 完整性哨兵：防止拿到「看着像但其实是空的」目录 ────────────────────────
NEED=(packages/AGENTS.md docs/postmortem)
for f in "${NEED[@]}"; do
  if [ ! -e "$SRC_DIR/$f" ]; then
    err "  完整性检查失败：缺少 $f"
    err "  这个目录不是有效的 DSH 仓库，请勿据此核验 API。"
    exit 6
  fi
done
NEWCOUNT=$(find "$SRC_DIR" -name "*.ts" -not -path "*/.git/*" 2>/dev/null | wc -l)
if [ "$NEWCOUNT" -lt 500 ]; then
  err "  完整性检查失败：源码树仅 $NEWCOUNT 个 .ts 文件（阈值 500）。"
  exit 6
fi
ok "  完整性检查通过（$NEWCOUNT 个 .ts 文件）。"
hr

# ── 5. 写同步状态 ────────────────────────────────────────────────────────────
COMMIT=$(g -C "$SRC_DIR" rev-parse HEAD 2>/dev/null)
COMMIT8=$(printf '%s' "$COMMIT" | cut -c1-8)
COMMIT_DATE=$(g -C "$SRC_DIR" log -1 --format='%ci' 2>/dev/null)
TAG_COUNT=$(g -C "$SRC_DIR" tag 2>/dev/null | wc -l)
LOCAL_LATEST=$(g -C "$SRC_DIR" tag 2>/dev/null | sort -V | tail -1)
LOCAL_LATEST_DATE=$(g -C "$SRC_DIR" log -1 --format='%ci' "$LOCAL_LATEST" 2>/dev/null | cut -d' ' -f1)
BRANCH=$(g -C "$SRC_DIR" rev-parse --abbrev-ref HEAD 2>/dev/null)
STAMP=$(date -u +%Y-%m-%dT%H:%M:%SZ 2>/dev/null || echo "unknown")

cat > "$STATE" <<EOF
{
  "syncedAt": "$STAMP",
  "repo": "$FETCH_URL",
  "mode": "git",
  "path": "$SRC_DIR",
  "branch": "$BRANCH",
  "commit": "$COMMIT",
  "commitDate": "$COMMIT_DATE",
  "tagCount": $TAG_COUNT,
  "latestTag": "$LOCAL_LATEST",
  "latestTagDate": "$LOCAL_LATEST_DATE",
  "skillBaseline": "f3803c9697 / dsh-v0.2.2-alpha.2",
  "note": "引用源，非依赖。禁止在此执行 pnpm/npm install。"
}
EOF

say "本地最新 : $LOCAL_LATEST  ($LOCAL_LATEST_DATE)"
say "HEAD     : $COMMIT8  $COMMIT_DATE  分支 $BRANCH"
say "tag 总数 : $TAG_COUNT"
say "状态文件 : $STATE"
hr
say "下一步（二选一或都做）："
say "  核验 API 是否漂移： bash $SCRIPT_DIR/dsh-api-probe.sh \"$SRC_DIR\""
say "  出「基线→最新」差异： bash $SCRIPT_DIR/dsh-version-diff.sh"
