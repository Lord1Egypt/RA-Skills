#!/usr/bin/env bash
# gb-cad-figure 三平台同步开源发布脚本
# 用法: bash release.sh ["提交说明"]
# 作用: push Gitee(origin) + push GitHub(github); ClawHub 需单独发版本(见底部提示)
set -e
cd "$(dirname "$0")"
MSG="${1:-update: gb-cad-figure 同步开源更新}"

# 暂存未跟踪文件(忽略 __pycache__)
git add -A
if git diff --cached --quiet; then
  echo "[*] 无改动需提交，跳到推送"
else
  git commit -m "$MSG"
fi

echo "=== 推 Gitee (origin) ==="
git push origin
echo "=== 推 GitHub (github) ==="
git push github

echo ""
echo "✅ 源码已同步 Gitee + GitHub"
echo ""
echo "════════════════════════════════════════"
echo " ClawHub 还需单独发版本(等审核):"
echo " npx --yes clawhub skill publish \\"
echo "   $(pwd) \\"
echo "   --slug gb-cad-figure --name \"GB国标·CAD·图形引擎\" \\"
echo "   --version <下一版> --topics \"GB,CAD,等轴测,回转体,工程图\" --json"
echo "════════════════════════════════════════"
