#!/usr/bin/env bash
# deploy-dist.sh - 通用构建产物远程部署（打包 -> SCP -> 远程原子替换）
# 用法: ./deploy-dist.sh -s ./dist -H user@host -t /var/www/app/dist [-p 22] [-k ~/.ssh/id_ed25519]
#                      [-o www-data:www-data] [-c "systemctl reload nginx"] [-n 3] [-f] [-d]
set -euo pipefail

SRC=""; HOST=""; TGT=""; PORT=22; KEY=""; OWNER=""; POST=""; KEEP=3; FRESH=0; DRY=0

usage() { sed -n '2,4p' "$0" | sed 's/^# \{0,1\}//'; exit "${1:-0}"; }

while getopts ":s:H:t:p:k:o:c:n:fdh" opt; do
  case $opt in
    s) SRC=$OPTARG ;;
    H) HOST=$OPTARG ;;
    t) TGT=$OPTARG ;;
    p) PORT=$OPTARG ;;
    k) KEY=$OPTARG ;;
    o) OWNER=$OPTARG ;;
    c) POST=$OPTARG ;;
    n) KEEP=$OPTARG ;;
    f) FRESH=1 ;;
    d) DRY=1 ;;
    h) usage 0 ;;
    *) usage 1 ;;
  esac
done

[ -n "$SRC" ] && [ -n "$HOST" ] && [ -n "$TGT" ] || usage 1
[ -d "$SRC" ] || { echo "[ERROR] Source 不是目录: $SRC" >&2; exit 1; }
case $TGT in /*) ;; *) echo "[ERROR] Target 必须是远程绝对路径: $TGT" >&2; exit 1 ;; esac
for c in ssh scp tar; do command -v "$c" >/dev/null || { echo "[ERROR] 缺少命令: $c" >&2; exit 1; }; done
[ -n "$KEY" ] && [ ! -f "$KEY" ] && { echo "[ERROR] 私钥不存在: $KEY" >&2; exit 1; }

MODE=$([ "$FRESH" = 1 ] && echo fresh || echo backup)
ID=$(date +%s)-$$
TMPD=$(mktemp -d)
trap 'rm -rf "$TMPD"' EXIT
ARCHIVE="$TMPD/dist-deploy-$ID.tgz"
REMOTE_ARCHIVE="/tmp/dist-deploy-$ID.tgz"
REMOTE_SCRIPT="$TMPD/remote.sh"

cat > "$REMOTE_SCRIPT" <<'REMOTE'
#!/bin/sh
set -eu
ARCHIVE="$1"; TGT="$2"; KEEP="$3"; MODE="$4"; OWNER="$5"; POSTCMD="${6:-}"
PARENT=$(dirname "$TGT")
NEW="$PARENT/.deploy-tmp-$$"
trap 'rm -rf "$NEW"' EXIT

mkdir -p "$PARENT"
rm -rf "$NEW"
mkdir -p "$NEW"
tar -xzf "$ARCHIVE" -C "$NEW"
[ -n "$OWNER" ] && chown -R "$OWNER" "$NEW"

if [ "$MODE" = "fresh" ]; then
    rm -rf "$TGT"
else
    if [ -e "$TGT" ] || [ -L "$TGT" ]; then
        BAK="$TGT.bak.$(date +%Y%m%d%H%M%S)"
        mv "$TGT" "$BAK"
        echo "backup: $BAK"
    fi
fi
mv "$NEW" "$TGT"
rm -f "$ARCHIVE"

if [ "$MODE" != "fresh" ] && [ "${KEEP:-3}" -gt 0 ] 2>/dev/null; then
    ls -1dt "$TGT".bak.* 2>/dev/null | tail -n +"$((KEEP + 1))" | while read -r old; do rm -rf "$old"; done
fi

if [ -n "$POSTCMD" ]; then
    echo "post: $POSTCMD"
    sh -c "$POSTCMD"
fi
echo "deployed: $TGT"
REMOTE

SSH_OPTS=(-p "$PORT"); SCP_OPTS=(-P "$PORT")
if [ -n "$KEY" ]; then SSH_OPTS+=(-i "$KEY"); SCP_OPTS+=(-i "$KEY"); fi

echo "[deploy] 1/4 打包 $SRC"
tar -czf "$ARCHIVE" -C "$SRC" .

if [ "$DRY" = 1 ]; then
  echo "--- DRY RUN ---"
  echo "tar -czf <tmp> -C $SRC ."
  echo "scp ${SCP_OPTS[*]} <archive> $HOST:$REMOTE_ARCHIVE"
  echo "ssh ${SSH_OPTS[*]} $HOST 'bash -s -- <args>' < remote.sh"
  cat "$REMOTE_SCRIPT"
  exit 0
fi

echo "[deploy] 2/4 上传压缩包"
scp "${SCP_OPTS[@]}" "$ARCHIVE" "$HOST:$REMOTE_ARCHIVE"

echo "[deploy] 3/4 远程解压并原子切换"
ssh "${SSH_OPTS[@]}" "$HOST" "bash -s -- '$REMOTE_ARCHIVE' '$TGT' '$KEEP' '$MODE' '$OWNER' '$POST'" < "$REMOTE_SCRIPT"

echo "[deploy] 4/4 完成 -> $HOST:$TGT"
[ "$FRESH" = 1 ] || echo "[deploy] 回滚: ssh -p $PORT $HOST 'rm -rf $TGT && mv $TGT.bak.<时间戳> $TGT'"
