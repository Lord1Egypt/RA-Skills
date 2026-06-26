#!/usr/bin/env python3
"""快速测试脚本 - 验证环境和 API 连接"""

import os
import sys

# 添加 lib 目录到路径
script_dir = os.path.dirname(os.path.abspath(__file__))
lib_dir = os.path.join(script_dir, '..', 'lib')
sys.path.insert(0, lib_dir)

def check_env():
    """检查环境变量"""
    api_key = os.environ.get("BIGMODEL_API_KEY")
    if not api_key:
        print("❌ BIGMODEL_API_KEY 环境变量未设置")
        print("\n请先设置 API Key:")
        print("  export BIGMODEL_API_KEY=your_api_key_here")
        return False

    # 显示部分 key 用于验证
    masked = api_key[:8] + "..." + api_key[-4:]
    print(f"✅ API Key 已设置: {masked}")
    return True

def check_module():
    """检查模块导入"""
    try:
        from image_video import generate_image
        print("✅ image_video 模块导入成功")
        return True
    except ImportError as e:
        print(f"❌ 模块导入失败: {e}")
        print("\n请确保已安装依赖:")
        print("  pip install requests")
        return False

def test_api():
    """测试 API 连接"""
    try:
        from image_video import generate_image

        print("\n🔄 测试 API 连接...")
        print("正在生成测试图片（一只橘猫）...")

        result = generate_image(
            prompt="一只橘色的猫，简单的测试图片",
            model="cogview-3-flash",
            size="1024x1024",
        )

        url = result["data"][0]["url"]
        print(f"\n✅ API 连接成功！")
        print(f"📸 测试图片 URL: {url}")
        print("\n🎉 技能已就绪，可以正常使用！")
        return True

    except Exception as e:
        print(f"\n❌ API 测试失败: {e}")
        print("\n可能的原因:")
        print("  1. API Key 不正确")
        print("  2. 网络连接问题")
        print("  3. API 服务暂时不可用")
        return False

def main():
    print("=" * 50)
    print("图片/视频生成技能 - 环境检测")
    print("=" * 50)

    checks = [
        ("环境变量", check_env),
        ("模块导入", check_module),
        ("API 连接", test_api),
    ]

    results = []
    for name, check_func in checks:
        print(f"\n[{name}]")
        result = check_func()
        results.append((name, result))
        if not result:
            break  # 某个检查失败则停止后续检查

    print("\n" + "=" * 50)
    print("检测结果:")
    for name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"  {name}: {status}")
    print("=" * 50)

    if all(r for _, r in results):
        print("\n🎉 所有检查通过！技能已就绪。")
        print("\n快速开始:")
        print('  python scripts/generate.py "你的描述"')
        return 0
    else:
        print("\n⚠️  部分检查未通过，请根据提示解决问题。")
        return 1

if __name__ == "__main__":
    sys.exit(main())
