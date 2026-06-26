#!/usr/bin/env bash
# browser-ops Cookie 同步
# 统一 Cookie 存储 → 所有工具复用
#
# 用法:
#   sync-cookies.sh export              # 从 agent-browser 导出到统一存储
#   sync-cookies.sh health              # 检查所有工具健康状态
#   sync-cookies.sh import-bu           # 从统一存储导入到 browser-use CLI
#   sync-cookies.sh inject-py <url>     # 用 Python 注入 Cookie 到 Playwright 页面
#   sync-cookies.sh login <url>         # 打开 URL 手动登录 → 自动导出
#   sync-cookies.sh status              # 查看当前存储的域名和 Cookie 数量
#   sync-cookies.sh verify              # 端到端验证所有路径

set -uo pipefail

STORE_DIR="$HOME/.browser-ops/cookie-store"
PROFILE_DIR="$HOME/.browser-ops/profiles/shared"
UNIFIED_STATE="$STORE_DIR/unified-state.json"

mkdir -p "$STORE_DIR" "$PROFILE_DIR"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

_count_cookies() {
  python3 -c "import json; print(len(json.load(open('$UNIFIED_STATE')).get('cookies',[])))" 2>/dev/null || echo "0"
}

_list_domains() {
  python3 -c "
import json
cookies = json.load(open('$UNIFIED_STATE')).get('cookies',[])
domains = sorted(set(c.get('domain','') for c in cookies))
print(', '.join(d for d in domains if d))
" 2>/dev/null
}

case "${1:-help}" in

  export)
    echo -e "${GREEN}从 agent-browser 导出 Cookie 到统一存储...${NC}"
    if ! command -v agent-browser &>/dev/null; then
      echo -e "${RED}agent-browser 未安装。${NC}"
      echo "安装: npm i -g agent-browser"
      exit 1
    fi
    agent-browser --profile "$PROFILE_DIR" open "about:blank" 2>/dev/null || true
    sleep 1
    agent-browser state save "$UNIFIED_STATE" 2>/dev/null
    agent-browser close 2>/dev/null

    if [[ -f "$UNIFIED_STATE" && -s "$UNIFIED_STATE" ]]; then
      echo -e "${GREEN}已导出 $(_count_cookies) 条 Cookie 到 $UNIFIED_STATE${NC}"
      echo -e "域名: $(_list_domains)"
    else
      echo -e "${RED}导出失败${NC}"
      exit 1
    fi
    ;;

  health)
    echo -e "${CYAN}=== browser-ops 健康检查 ===${NC}"
    echo ""
    FAIL=0

    # 1. opencli
    if command -v opencli &>/dev/null; then
      DOCTOR=$(opencli doctor 2>&1)
      if echo "$DOCTOR" | grep -q "\[OK\] Connectivity"; then
        echo -e "${GREEN}[OK]${NC} opencli: daemon + extension + connectivity"
      elif echo "$DOCTOR" | grep -q "\[OK\] Daemon"; then
        echo -e "${YELLOW}[WARN]${NC} opencli: daemon running but extension not connected"
        echo "      → Chrome 里装 OpenCLI Browser Bridge 扩展"
        FAIL=1
      else
        echo -e "${RED}[FAIL]${NC} opencli: daemon not running"
        echo "      → 运行: opencli daemon restart"
        FAIL=1
      fi
    else
      echo -e "${RED}[FAIL]${NC} opencli 未安装"
      echo "      → npm i -g @jackwener/opencli"
      FAIL=1
    fi

    # 2. browser-use (按需)
    if command -v browser-use &>/dev/null; then
      echo -e "${GREEN}[OK]${NC} browser-use 已安装"
    else
      echo -e "${YELLOW}[SKIP]${NC} browser-use 未安装 (按需: pip install browser-use)"
    fi

    # 3. zendriver (按需)
    python3 -c "import zendriver" 2>/dev/null \
      && echo -e "${GREEN}[OK]${NC} zendriver 已安装" \
      || echo -e "${YELLOW}[SKIP]${NC} zendriver 未安装 (按需: pip install zendriver)"

    # 4. Cookie store
    echo ""
    if [[ -f "$UNIFIED_STATE" && -s "$UNIFIED_STATE" ]]; then
      AGE_HOURS=$(python3 -c "import os,time; print(f'{(time.time()-os.path.getmtime(os.path.expanduser(\"$UNIFIED_STATE\")))/3600:.0f}')")
      echo -e "${GREEN}[OK]${NC} Cookie 存储: $(_count_cookies) cookies (${AGE_HOURS}h ago)"
      if [[ "$AGE_HOURS" -gt 24 ]]; then
        echo -e "${YELLOW}      → Cookie 超过 24 小时未更新，建议: sync-cookies.sh export${NC}"
      fi
    else
      echo -e "${YELLOW}[SKIP]${NC} Cookie 存储为空 (仅 Stagehand/Zendriver 需要)"
    fi

    echo ""
    if [[ $FAIL -eq 0 ]]; then
      echo -e "${GREEN}=== 全部正常 ===${NC}"
    else
      echo -e "${YELLOW}=== 有问题需要修复 ===${NC}"
    fi
    ;;

  import-bu)
    echo -e "${GREEN}从统一存储导入 Cookie 到 browser-use CLI...${NC}"
    if [[ ! -f "$UNIFIED_STATE" ]]; then
      echo -e "${RED}统一存储不存在: $UNIFIED_STATE${NC}"
      echo "先运行: sync-cookies.sh export 或 sync-cookies.sh login <url>"
      exit 1
    fi

    # Convert unified-state.json (Playwright storageState) to browser-use flat array
    TMP_COOKIES="/tmp/browser-ops-bu-cookies.json"
    python3 -c "
import json, os
data = json.load(open(os.path.expanduser('$UNIFIED_STATE')))
cookies = [{k: v for k, v in c.items() if k not in ('size', 'session')} for c in data['cookies']]
json.dump(cookies, open('$TMP_COOKIES', 'w'), indent=2)
print(f'Converted {len(cookies)} cookies to browser-use format: $TMP_COOKIES')
"
    echo -e "${CYAN}用法: browser-use cookies import $TMP_COOKIES${NC}"
    echo -e "${CYAN}  或: 在 Python 中用 Playwright context.add_cookies() 注入${NC}"
    ;;

  inject-py)
    URL="${2:-}"
    if [[ -z "$URL" ]]; then
      echo -e "${RED}用法: sync-cookies.sh inject-py <url>${NC}"
      exit 1
    fi
    echo -e "${GREEN}通过 Playwright 注入统一 Cookie 并访问 $URL...${NC}"

    if [[ ! -f "$UNIFIED_STATE" ]]; then
      echo -e "${RED}统一存储不存在: $UNIFIED_STATE${NC}"
      exit 1
    fi

    python3 << PYEOF
import json, os, asyncio

async def main():
    from playwright.async_api import async_playwright
    state_file = os.path.expanduser("$UNIFIED_STATE")
    data = json.load(open(state_file))
    cookies = data.get("cookies", [])

    # Filter cookies for target domain
    from urllib.parse import urlparse
    target = urlparse("$URL")
    domain = target.hostname or ""

    matching = [c for c in cookies if domain.endswith(c.get("domain","").lstrip("."))]
    print(f"Injecting {len(matching)} cookies for domain {domain} (of {len(cookies)} total)")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()

        # Convert to Playwright format
        pw_cookies = []
        for c in matching:
            cookie = {
                "name": c["name"],
                "value": c.get("value", ""),
                "domain": c["domain"],
                "path": c.get("path", "/"),
            }
            if c.get("expires", -1) > 0:
                cookie["expires"] = c["expires"]
            if c.get("secure"):
                cookie["secure"] = True
            if c.get("httpOnly"):
                cookie["httpOnly"] = True
            pw_cookies.append(cookie)

        if pw_cookies:
            await context.add_cookies(pw_cookies)

        page = await context.new_page()
        response = await page.goto("$URL", wait_until="domcontentloaded", timeout=15000)
        status = response.status if response else "N/A"
        title = await page.title()
        print(f"Status: {status}")
        print(f"Title: {title}")

        # Check if we landed on login page (indicates cookies didn't work)
        url_after = page.url
        if "login" in url_after.lower() or "sso" in url_after.lower():
            print(f"WARN: Redirected to login: {url_after}")
            print("Cookie injection may not have worked — cookies might be expired")
        else:
            print(f"SUCCESS: Accessed {url_after}")

        await browser.close()

asyncio.run(main())
PYEOF
    ;;

  login)
    URL="${2:-https://example.com}"
    echo -e "${GREEN}打开 $URL 手动登录...${NC}"
    echo -e "${YELLOW}登录完成后，按 Enter 键继续（会自动保存 Cookie）${NC}"

    if command -v agent-browser &>/dev/null; then
      agent-browser close 2>/dev/null; sleep 1
      agent-browser --headed --profile "$PROFILE_DIR" open "$URL" 2>/dev/null || true

      read -r -p "登录完成了吗？按 Enter 继续..."

      agent-browser state save "$UNIFIED_STATE" 2>/dev/null
    else
      echo -e "${YELLOW}agent-browser 未安装，使用 Playwright 打开...${NC}"
      python3 << PYEOF
import asyncio, json, os

async def main():
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        await page.goto("$URL")
        input("登录完成后按 Enter...")

        # Export cookies
        cookies = await context.cookies()
        state = {"cookies": cookies, "origins": []}
        store = os.path.expanduser("$UNIFIED_STATE")
        json.dump(state, open(store, "w"), indent=2)
        print(f"Saved {len(cookies)} cookies")
        await browser.close()

asyncio.run(main())
PYEOF
    fi

    if [[ -f "$UNIFIED_STATE" && -s "$UNIFIED_STATE" ]]; then
      echo -e "${GREEN}已保存 $(_count_cookies) 条 Cookie${NC}"
      echo -e "域名: $(_list_domains)"
      chmod 600 "$UNIFIED_STATE"
    fi
    echo -e "${GREEN}Cookie 已存储到 $UNIFIED_STATE${NC}"
    ;;

  status)
    if [[ ! -f "$UNIFIED_STATE" ]]; then
      echo -e "${YELLOW}统一存储为空${NC}"
      echo "运行: sync-cookies.sh export 或 sync-cookies.sh login <url>"
      exit 0
    fi

    python3 << 'PYEOF'
import json, os
from datetime import datetime

state_file = os.path.expanduser("~/.browser-ops/cookie-store/unified-state.json")
data = json.load(open(state_file))
cookies = data.get("cookies", [])

domains = {}
expired = 0
no_value = 0
import time
now = time.time()

for c in cookies:
    d = c.get("domain", "unknown")
    domains.setdefault(d, []).append(c)
    if c.get("expires", -1) > 0 and c["expires"] < now:
        expired += 1
    if not c.get("value"):
        no_value += 1

mtime = os.path.getmtime(state_file)
age_hours = (now - mtime) / 3600

print(f"统一 Cookie 存储: {len(cookies)} 条")
print(f"覆盖 {len(domains)} 个域名")
print(f"文件: {state_file}")
print(f"大小: {os.path.getsize(state_file):,} bytes")
print(f"更新时间: {datetime.fromtimestamp(mtime).strftime('%Y-%m-%d %H:%M:%S')} ({age_hours:.1f} 小时前)")
if expired > 0:
    print(f"\033[1;33m警告: {expired} 条 Cookie 已过期\033[0m")
if no_value > 0:
    print(f"\033[1;33m警告: {no_value} 条 Cookie 无 value（可能只有 metadata）\033[0m")
print()
for domain in sorted(domains.keys()):
    items = domains[domain]
    session_count = sum(1 for c in items if c.get("session", False))
    persistent_count = len(items) - session_count
    has_value = sum(1 for c in items if c.get("value"))
    value_tag = f" ✅ {has_value} with value" if has_value > 0 else " ⚠️  metadata only"
    print(f"  {domain}: {len(items)} cookies ({persistent_count}p/{session_count}s){value_tag}")
PYEOF
    ;;

  verify)
    echo -e "${CYAN}=== browser-ops Cookie 端到端验证 ===${NC}"
    echo ""

    # 1. Check unified store exists
    if [[ -f "$UNIFIED_STATE" && -s "$UNIFIED_STATE" ]]; then
      echo -e "${GREEN}[PASS]${NC} 统一存储存在: $UNIFIED_STATE ($(_count_cookies) cookies)"
    else
      echo -e "${RED}[FAIL]${NC} 统一存储不存在或为空"
      echo "运行: sync-cookies.sh export 或 sync-cookies.sh login <url>"
      exit 1
    fi

    # 2. Check cookies have values
    HAS_VALUES=$(python3 -c "
import json, os
data = json.load(open(os.path.expanduser('$UNIFIED_STATE')))
cookies_with_values = [c for c in data.get('cookies',[]) if c.get('value')]
print(len(cookies_with_values))
")
    TOTAL=$(_count_cookies)
    if [[ "$HAS_VALUES" -gt 0 ]]; then
      echo -e "${GREEN}[PASS]${NC} Cookie 有 value: $HAS_VALUES / $TOTAL"
    else
      echo -e "${RED}[FAIL]${NC} Cookie 无 value (全是 metadata)"
      echo "运行: sync-cookies.sh export 重新导出（需要 agent-browser）"
    fi

    # 3. Check file permissions
    PERMS=$(stat -f "%Lp" "$UNIFIED_STATE" 2>/dev/null || stat -c "%a" "$UNIFIED_STATE" 2>/dev/null)
    if [[ "$PERMS" == "600" ]]; then
      echo -e "${GREEN}[PASS]${NC} 文件权限: $PERMS (安全)"
    else
      echo -e "${YELLOW}[WARN]${NC} 文件权限: $PERMS (建议 chmod 600)"
    fi

    # 4. Check cookie expiry
    EXPIRED=$(python3 -c "
import json, os, time
data = json.load(open(os.path.expanduser('$UNIFIED_STATE')))
now = time.time()
expired = [c for c in data.get('cookies',[]) if c.get('expires',-1) > 0 and c['expires'] < now]
print(len(expired))
")
    if [[ "$EXPIRED" -eq 0 ]]; then
      echo -e "${GREEN}[PASS]${NC} 无过期 Cookie"
    else
      echo -e "${YELLOW}[WARN]${NC} $EXPIRED 条 Cookie 已过期"
    fi

    # 5. Format conversion test
    echo ""
    echo -e "${CYAN}--- 格式转换验证 ---${NC}"
    TMP="/tmp/browser-ops-verify-cookies.json"
    python3 -c "
import json, os
data = json.load(open(os.path.expanduser('$UNIFIED_STATE')))
cookies = [{k: v for k, v in c.items() if k not in ('size', 'session')} for c in data['cookies']]
json.dump(cookies, open('$TMP', 'w'))
print(f'Playwright → flat array: {len(cookies)} cookies')
import json as j
loaded = j.load(open('$TMP'))
assert isinstance(loaded, list), 'Should be array'
assert all('name' in c and 'domain' in c for c in loaded), 'Each cookie needs name+domain'
print('Format validation: OK')
" && echo -e "${GREEN}[PASS]${NC} unified-state.json → browser-use 格式转换正常" \
  || echo -e "${RED}[FAIL]${NC} 格式转换失败"
    rm -f "$TMP"

    # 6. Playwright injection test (headless)
    echo ""
    echo -e "${CYAN}--- Playwright 注入验证 ---${NC}"
    python3 << 'PYEOF' && echo -e "${GREEN}[PASS]${NC} Playwright Cookie 注入成功" \
  || echo -e "${RED}[FAIL]${NC} Playwright Cookie 注入失败（playwright 可能未安装）"
import json, os, asyncio, sys

async def test():
    try:
        from playwright.async_api import async_playwright
    except ImportError:
        print("playwright not installed — skipping")
        sys.exit(0)

    data = json.load(open(os.path.expanduser("~/.browser-ops/cookie-store/unified-state.json")))
    cookies = data.get("cookies", [])
    if not cookies:
        print("No cookies to inject")
        sys.exit(1)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()

        pw_cookies = []
        for c in cookies:
            cookie = {"name": c["name"], "value": c.get("value",""), "domain": c["domain"], "path": c.get("path","/")}
            if c.get("expires", -1) > 0:
                cookie["expires"] = c["expires"]
            if c.get("secure"):
                cookie["secure"] = True
            if c.get("httpOnly"):
                cookie["httpOnly"] = True
            pw_cookies.append(cookie)

        await context.add_cookies(pw_cookies)
        stored = await context.cookies()
        print(f"Injected {len(pw_cookies)} → retrieved {len(stored)} cookies from context")
        assert len(stored) > 0, "No cookies in context after injection"
        await browser.close()

asyncio.run(test())
PYEOF

    # 7. Tool availability
    echo ""
    echo -e "${CYAN}--- 工具可用性 ---${NC}"
    for tool in agent-browser browser-use; do
      if command -v "$tool" &>/dev/null; then
        echo -e "${GREEN}[PASS]${NC} $tool 已安装"
      else
        echo -e "${YELLOW}[SKIP]${NC} $tool 未安装"
      fi
    done

    python3 -c "import zendriver" 2>/dev/null && echo -e "${GREEN}[PASS]${NC} zendriver 已安装" \
      || echo -e "${YELLOW}[SKIP]${NC} zendriver 未安装"

    echo ""
    echo -e "${CYAN}=== 验证完成 ===${NC}"
    ;;

  *)
    echo "browser-ops Cookie 同步工具"
    echo ""
    echo "用法:"
    echo "  sync-cookies.sh login <url>     打开 URL 登录 → 自动保存 Cookie"
    echo "  sync-cookies.sh export          从 agent-browser 导出到统一存储"
    echo "  sync-cookies.sh health          检查所有工具健康状态"
    echo "  sync-cookies.sh import-bu       转换为 browser-use 格式"
    echo "  sync-cookies.sh inject-py <url> 通过 Playwright 注入 Cookie 并访问"
    echo "  sync-cookies.sh status          查看存储状态"
    echo "  sync-cookies.sh verify          端到端验证所有路径"
    ;;
esac
