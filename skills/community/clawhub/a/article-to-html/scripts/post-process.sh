#!/bin/bash
# 信息图 HTML 后处理 + 截图一键脚本
# 用法: bash post-process.sh <html文件路径> [输出图片路径]
#
# 功能：
# 1. 运行 fix-html.js 修复 CSS（边距、宽度、coord、overflow）
# 2. 注入运行时 CSS 覆盖（字号兜底放大）
# 3. 截图输出 PNG

set -e

HTML_FILE="$1"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
OUTPUT="${2:-${HTML_FILE%.html}.png}"

if [ -z "$HTML_FILE" ]; then
  echo "用法: bash post-process.sh <html文件> [输出图片路径]"
  exit 1
fi

export PATH="/opt/homebrew/bin:$HOME/Library/pnpm:$PATH"

# Step 1: fix-html.js 修复 CSS
echo "→ Step 1: fix-html.js"
node "$SCRIPT_DIR/fix-html.js" "$HTML_FILE"

# Step 2: 注入运行时字号兜底
echo "→ Step 2: 注入字号兜底 CSS"

if ! grep -q "POST-PROCESS" "$HTML_FILE"; then
  python3 -c "
import sys
html = open(sys.argv[1]).read()
css = '''/* === POST-PROCESS: 字号兜底 === */
.container { font-size: max(14px, 1em); }
.container h1, .container [class*=\"title\"]:first-child { font-size: max(48px, 1em) !important; }
.container h2, .container h3 { font-size: max(28px, 1em) !important; }
.container p, .container li, .container td { font-size: max(20px, 0.9em) !important; }
.container .coord { display: none !important; }
'''
html = html.replace('</style>', css + '</style>', 1)
open(sys.argv[1], 'w').write(html)
print('   注入完成')
" "$HTML_FILE"
else
  echo "   已注入过，跳过"
fi

echo "→ 完成: $HTML_FILE"
echo "→ 可用 Chrome DevTools 截图，或浏览器打开查看"
