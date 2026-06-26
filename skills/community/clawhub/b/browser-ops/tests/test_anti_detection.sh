#!/usr/bin/env bash
# L6: 反爬工具可用性测试

section "L6: 反爬工具"

# 自动选择可用的 Python (zendriver 需要 3.12+, 但 3.14 有兼容性问题)
# 优先检测 zendriver (Nodriver 继任者)，回退到 nodriver
ZENDRIVER_PY=""
ZENDRIVER_LEGACY=false
for py in python3.13 python3.12 python3; do
  if command -v "$py" &>/dev/null; then
    if "$py" -c "import zendriver" 2>/dev/null; then
      ZENDRIVER_PY="$py"
      break
    elif "$py" -c "import nodriver" 2>/dev/null; then
      ZENDRIVER_PY="$py"
      ZENDRIVER_LEGACY=true
      break
    fi
  fi
done

CAMO_PY=""
for py in python3.13 python3.12 python3; do
  if command -v "$py" &>/dev/null && "$py" -c "import camoufox" 2>/dev/null; then
    CAMO_PY="$py"
    break
  fi
done

# === Zendriver (Nodriver 继任者) ===

if [[ -z "$ZENDRIVER_PY" ]]; then
  skip "Zendriver 未安装" "运行: pip install zendriver (需要 Python 3.12/3.13)"
else
  PY_VER=$($ZENDRIVER_PY -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
  if [[ "$ZENDRIVER_LEGACY" == "true" ]]; then
    pass "Nodriver 已安装 (via $ZENDRIVER_PY, Python $PY_VER) — 建议迁移到 zendriver"
    ZD_IMPORT="import nodriver as uc"
    ZD_START="uc.start"
    ZD_LABEL="Nodriver(legacy)"
  else
    pass "Zendriver 已安装 (via $ZENDRIVER_PY, Python $PY_VER)"
    ZD_IMPORT="import zendriver as zd"
    ZD_START="zd.start"
    ZD_LABEL="Zendriver"
  fi

  # 检测 Chrome 路径 (agent-browser 安装的 Chrome for Testing 或系统 Chrome)
  CHROME_PATH=""
  for p in \
    "$HOME/.agent-browser/browsers"/chrome-*/Google\ Chrome\ for\ Testing.app/Contents/MacOS/Google\ Chrome\ for\ Testing \
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
    "$(command -v google-chrome 2>/dev/null)" \
    "$(command -v chromium 2>/dev/null)"; do
    if [[ -x "$p" ]]; then
      CHROME_PATH="$p"
      break
    fi
  done

  if [[ -z "$CHROME_PATH" ]]; then
    skip "$ZD_LABEL 端到端" "找不到 Chrome 二进制"
    return 0 2>/dev/null || true
  fi

  # Zendriver/Nodriver 端到端测试
  ZD_RESULT=$(timeout 30 $ZENDRIVER_PY -c "
import asyncio, sys
${ZD_IMPORT}

async def test():
    try:
        browser = await ${ZD_START}(headless=True, browser_executable_path=sys.argv[1])
        page = await browser.get('https://example.com')
        await page.sleep(2)
        content = await page.get_content()
        if len(content) > 100:
            print(f'SUCCESS:{len(content)}')
        else:
            print('FAIL:content_too_short')
        browser.stop()
    except Exception as e:
        print(f'ERROR:{e}')

asyncio.run(test())
" "$CHROME_PATH" 2>/dev/null || echo "TIMEOUT")

  if echo "$ZD_RESULT" | grep -q "^SUCCESS:"; then
    CHARS=$(echo "$ZD_RESULT" | grep "^SUCCESS:" | sed 's/^SUCCESS://')
    pass "$ZD_LABEL 端到端: example.com (${CHARS} chars)"
  elif [[ "$ZD_RESULT" == "TIMEOUT" ]]; then
    fail "$ZD_LABEL 端到端" "超时 (30s)"
  else
    ERROR_MSG=$(echo "$ZD_RESULT" | grep "^ERROR:" | sed 's/^ERROR://' | head -1)
    fail "$ZD_LABEL 端到端" "${ERROR_MSG:-未知错误}"
  fi
fi

# === Camoufox ===

if [[ -z "$CAMO_PY" ]]; then
  skip "Camoufox 未安装" "运行: pip install camoufox && python3 -m camoufox fetch"
else
  pass "Camoufox 已安装 (via $CAMO_PY)"

  # 检查 Firefox 二进制是否已下载
  CAMO_CHECK=$($CAMO_PY -c "
from camoufox.pkgman import get_path
try:
    p = get_path()
    print(f'PATH:{p}')
except:
    print('MISSING')
" 2>/dev/null || echo "MISSING")

  if echo "$CAMO_CHECK" | grep -q "^PATH:"; then
    pass "Camoufox Firefox 二进制已就绪"
  else
    skip "Camoufox Firefox 二进制" "运行: $CAMO_PY -m camoufox fetch"
    return 0 2>/dev/null || true
  fi

  # Camoufox 端到端测试
  CAMO_RESULT=$(timeout 30 $CAMO_PY -c "
from camoufox.sync_api import Camoufox
try:
    with Camoufox(headless=True) as browser:
        page = browser.new_page()
        page.goto('https://example.com', timeout=15000)
        content = page.content()
        if len(content) > 100:
            print(f'SUCCESS:{len(content)}')
        else:
            print('FAIL:content_too_short')
except Exception as e:
    print(f'ERROR:{e}')
" 2>/dev/null || echo "TIMEOUT")

  if echo "$CAMO_RESULT" | grep -q "^SUCCESS:"; then
    CHARS=$(echo "$CAMO_RESULT" | grep "^SUCCESS:" | sed 's/^SUCCESS://')
    pass "Camoufox 端到端: example.com (${CHARS} chars)"
  elif [[ "$CAMO_RESULT" == "TIMEOUT" ]]; then
    fail "Camoufox 端到端" "超时 (30s)"
  else
    ERROR_MSG=$(echo "$CAMO_RESULT" | grep "^ERROR:" | sed 's/^ERROR://' | head -1)
    fail "Camoufox 端到端" "${ERROR_MSG:-未知错误}"
  fi
fi
