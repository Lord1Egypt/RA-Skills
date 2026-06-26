#!/usr/bin/env python3
"""
批量获取所有平台上架/下架榜单
每天 20:00 执行，获取全部 12 个平台的上架 + 下架榜单（共 24 个榜单）
"""

import subprocess
import sys
from datetime import datetime
from pathlib import Path

# 平台列表
PLATFORMS = [
    'appstore_cn',
    'huawei',
    'xiaomi',
    'vivo',
    'oppo',
    'meizu',
    'tencent',
    'baidu',
    'qihoo360',
    'honor',
    'harmony',
    'wandoujia'
]

def log(msg):
    """打印带时间的日志"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"[{timestamp}] {msg}", flush=True)

def fetch_platform(platform: str, offline: bool = False):
    """获取单个平台的榜单"""
    suffix = "下架" if offline else "上架"
    log(f"开始获取 {platform} {suffix}榜单...")
    
    cmd = [
        sys.executable,
        str(Path(__file__).parent / 'diandian_connect.py'),
        '--platform', platform
    ]
    
    if offline:
        cmd.append('--offline')
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        if result.returncode == 0:
            log(f"✅ {platform} {suffix}榜单获取成功")
            return True
        else:
            log(f"❌ {platform} {suffix}榜单获取失败：{result.stderr[:200]}")
            return False
    except subprocess.TimeoutExpired:
        log(f"❌ {platform} {suffix}榜单获取超时（>5 分钟）")
        return False
    except Exception as e:
        log(f"❌ {platform} {suffix}榜单获取异常：{str(e)[:200]}")
        return False

def main():
    log("=" * 60)
    log("开始批量获取所有平台榜单")
    log("=" * 60)
    
    total = len(PLATFORMS) * 2  # 上架 + 下架
    success = 0
    failed = 0
    
    # 获取上架榜单
    log(f"\n📊 开始获取上架榜单（{len(PLATFORMS)}个平台）")
    log("-" * 60)
    for platform in PLATFORMS:
        if fetch_platform(platform, offline=False):
            success += 1
        else:
            failed += 1
    
    # 获取下架榜单
    log(f"\n📉 开始获取下架榜单（{len(PLATFORMS)}个平台）")
    log("-" * 60)
    for platform in PLATFORMS:
        if fetch_platform(platform, offline=True):
            success += 1
        else:
            failed += 1
    
    # 汇总报告
    log("\n" + "=" * 60)
    log("批量获取完成")
    log(f"总计：{total} 个榜单")
    log(f"成功：{success} 个 ✅")
    log(f"失败：{failed} 个 ❌")
    log("=" * 60)
    
    if failed > 0:
        log(f"\n⚠️ 有 {failed} 个榜单获取失败，请检查日志")
        sys.exit(1)
    else:
        log("\n🎉 所有榜单获取成功！")
        sys.exit(0)

if __name__ == '__main__':
    main()
