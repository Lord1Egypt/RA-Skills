#!/usr/bin/env python3
"""
1688 数据采集脚本
检查浏览器 → 导航工作台 → 导航生意参谋 → 获取插件数据 → 保存 JSON

用法：
  python3 fetch_data.py [output.json]

  默认输出到临时目录中的 1688_raw_data.json（跨平台：Linux/macOS→/tmp，Windows→%TEMP%）
  退出码: 0=成功, 1=需要登录, 2=采集失败
"""

import sys, json, time, os, subprocess, platform
from pathlib import Path

if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

# skill 目录
SKILL_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SKILL_DIR / 'scripts'))

from cdp_client import CdpClient

# 跨平台临时目录
TMP_DIR = os.environ.get('TMPDIR', os.environ.get('TEMP', '/tmp'))
OUTPUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(TMP_DIR, '1688_raw_data.json')


def _start_browser():
    """跨平台启动浏览器"""
    if platform.system() == 'Windows':
        script = SKILL_DIR / 'scripts' / 'start-browser.ps1'
        cmd = ['powershell', '-ExecutionPolicy', 'Bypass', '-File', str(script)]
    else:
        script = SKILL_DIR / 'scripts' / 'start-browser.sh'
        cmd = ['bash', str(script)]
    
    result = subprocess.run(cmd, check=False)
    return result.returncode == 0


def main():
    # 检查浏览器
    if not CdpClient.is_running():
        print("浏览器未运行，启动中...")
        if not _start_browser():
            print("❌ 浏览器启动失败")
            sys.exit(2)

    with CdpClient() as c:
        c.ensure_tab(retries=3)

        # 检查登录状态
        url = c.eval("window.location.href")
        if url and 'login' in url.lower():
            print("❌ 需要登录（Cookie 已失效）")
            sys.exit(1)

        print("✅ 浏览器就绪，开始采集...")

        # 导航到工作台
        print("→ 工作台...")
        c.navigate(
            "https://work.1688.com/?_path_=sellerPro/sellberBaseNew_Index/seller2018IndexPage",
            wait_seconds=5
        )
        time.sleep(3)

        # 导航到生意参谋
        print("→ 生意参谋...")
        c.navigate(
            "https://sycm.1688.com/ms/home/index.htm",
            wait_seconds=5
        )
        time.sleep(8)

        # 获取全部数据
        print("→ 获取插件数据...")
        all_data = c.fetch_data(mode='full', limit=100)

        if not all_data.get('success'):
            print("❌ 数据采集失败:", all_data.get('error', 'unknown'))
            sys.exit(2)

        # 保存
        with open(OUTPUT, 'w', encoding='utf-8') as f:
            json.dump(all_data, f, ensure_ascii=False, indent=2)

        sycm_list = all_data.get('data', {}).get('sycm', [])
        work_list = all_data.get('data', {}).get('work', [])
        s = sycm_list[-1] if sycm_list else {}
        print(f"✅ 采集完成 → {OUTPUT}")
        print(f"   sycm: {len(sycm_list)} 条, work: {len(work_list)} 条")
        if s.get('companyName'):
            print(f"   店铺: {s['companyName']}")
            if s.get('rankTrend'):
                print(f"   排名: 第{s['rankTrend'].get('rank')}名")
            print(f"   日期: {s.get('flowStats', {}).get('statDate', '—')}")
        sys.exit(0)


if __name__ == '__main__':
    main()