#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""测试配置文件是否正确"""

import os
import json
from pathlib import Path

AGENT_DIR = Path.home() / ".openclaw/agents/gzh-assistant"
CONFIG_FILE = AGENT_DIR / "wechat/credentials.json"
IMAGE_DIR_DEFAULT = AGENT_DIR / "wechat_images"


def check_credentials():
    """检查凭证配置"""
    print("检查凭证配置...")
    if not CONFIG_FILE.exists():
        print(f"  ❌ 配置文件不存在: {CONFIG_FILE}")
        print(f"  请创建配置文件: {CONFIG_FILE}")
        return False
    
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        try:
            creds = json.load(f)
        except json.JSONDecodeError as e:
            print(f"  ❌ JSON 格式错误: {e}")
            return False
    
    required = ["app_id", "app_secret"]
    for key in required:
        if key not in creds:
            print(f"  ❌ 缺少字段: {key}")
            return False
        if not creds[key]:
            print(f"  ❌ 字段为空: {key}")
            return False
    
    # 检查 AppID 格式
    app_id = creds["app_id"]
    if not app_id.startswith("wx"):
        print(f"  ⚠️  AppID 应以 wx 开头，当前: {app_id}")
    
    # 检查 AppSecret 长度
    app_secret = creds["app_secret"]
    if len(app_secret) < 20:
        print(f"  ⚠️  AppSecret 长度异常，当前: {len(app_secret)}")
    
    print(f"  ✅ AppID: {app_id}")
    print(f"  ✅ AppSecret: {'*' * 20}{app_secret[-4:]}")
    return True


def check_image_dir():
    """检查图片目录"""
    print("\n检查图片目录...")
    
    # 从配置读取
    image_dir = IMAGE_DIR_DEFAULT
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            creds = json.load(f)
            custom_dir = creds.get("image_dir")
            if custom_dir:
                image_dir = Path(custom_dir)
    
    if not image_dir.exists():
        print(f"  ⚠️  目录不存在: {image_dir}")
        print("  将使用默认目录")
        return False
    
    print(f"  ✅ 目录存在: {image_dir}")
    
    # 检查封面图
    cover_files = ["cover.png", "cover.jpg", "cover.jpeg"]
    cover_found = any((image_dir / f).exists() for f in cover_files)
    if cover_found:
        for f in cover_files:
            if (image_dir / f).exists():
                size = os.path.getsize(image_dir / f)
                print(f"  ✅ 封面图: {f} ({size/1024:.1f} KB)")
                break
    else:
        print(f"  ⚠️  封面图不存在（需要 cover.png 或 cover.jpg）")
    
    # 检查内容图
    layer_files = ["layer1.png", "layer1.jpg", "layer2.png", "layer2.jpg", "layer3.png", "layer3.jpg", "layer4.png", "layer4.jpg"]
    for i in range(1, 5):
        for ext in ["png", "jpg"]:
            path = image_dir / f"layer{i}.{ext}"
            if path.exists():
                size = os.path.getsize(path)
                print(f"  ✅ 内容图{i}: layer{i}.{ext} ({size/1024:.1f} KB)")
                break
    
    return True


def main():
    print("=" * 50)
    print("1-Click WOA - 配置检查")
    print("=" * 50)
    
    ok = True
    ok = check_credentials() and ok
    ok = check_image_dir() and ok
    
    print("\n" + "=" * 50)
    if ok:
        print("✅ 配置检查通过！可以运行发布脚本。")
    else:
        print("⚠️  配置有问题，请修复后再试。")
    print("=" * 50)
    
    return 0 if ok else 1


if __name__ == "__main__":
    exit(main())
