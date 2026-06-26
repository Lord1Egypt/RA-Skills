#!/bin/bash
# Batch download - each book in its own process to avoid Playwright context issues
set -e

OUTPUT_DIR="$HOME/Documents/Books/微信读书/医学&健康/"
PYTHON="/opt/homebrew/Caskroom/miniforge/base/envs/env9/bin/python"
SCRIPT_DIR="$HOME/.openclaw/workspace/skills/chinese-ebook-downloader/scripts"

declare -a BOOKS=(
  "生命密码 尹烨"
  "吃出自愈力 威廉·李"
  "谷物大脑 戴维·珀尔马特"
  "不老时代 年轻 长寿 罗伊森"
  "疗愈的饮食与断食 杨定一"
  "菌群大脑 克里斯廷·洛伯格"
  "疯狂的尿酸 痛风 戴维·珀尔马特"
  "逆龄饮食 再生医学 乔普"
)

DONE=0
FAIL=0
SKIP=0

for entry in "${BOOKS[@]}"; do
  read -r title author <<< "$entry"
  
  # Check if already downloaded
  if ls "$OUTPUT_DIR"/*"$title"*.pdf 1>/dev/null 2>&1; then
    echo "⏭️ $title - already exists, skipping"
    SKIP=$((SKIP+1))
    continue
  fi
  
  echo ""
  echo "=============================="
  echo "📚 $title - $author"
  echo "=============================="
  
  if timeout 180 "$PYTHON" -c "
import sys, asyncio, os
sys.path.insert(0, '$SCRIPT_DIR')
from search_source_c import download_book_from_annas_archive
async def go():
    result = await download_book_from_annas_archive('$title', '$author', output_dir='$OUTPUT_DIR', headless=True)
    if result and result.get('status') == 'done' and result.get('files'):
        for f in result['files']:
            if os.path.exists(f) and os.path.getsize(f) > 1000:
                ext = os.path.splitext(f)[1].lower()
                sz = os.path.getsize(f) / (1024*1024)
                print(f'✅ {ext.upper()}: {os.path.basename(f)} ({sz:.1f} MB)')
                sys.exit(0)
            elif os.path.exists(f):
                os.remove(f)
    print('❌ Failed')
    sys.exit(1)
asyncio.run(go())
" 2>&1; then
    DONE=$((DONE+1))
  else
    echo "❌ Failed: $title"
    FAIL=$((FAIL+1))
  fi
  
  sleep 5
done

echo ""
echo "=============================="
echo "📊 Results: $DONE done, $FAIL failed, $SKIP skipped"
echo "=============================="
