#!/usr/bin/env python3
"""
快速测试微信封面图生成功能
测试 900x386 尺寸和平面矢量插画风格
"""

import os
import sys

# 检查依赖
try:
    import requests
    print("✅ requests 库已安装")
except ImportError:
    print("❌ 缺少 requests 库")
    print("   安装命令: pip install requests")
    sys.exit(1)

try:
    from PIL import Image
    print("✅ Pillow 库已安装")
    PIL_AVAILABLE = True
except ImportError:
    print("⚠️  Pillow 库未安装（图片调整功能将被跳过）")
    print("   安装命令: pip install Pillow")
    PIL_AVAILABLE = False

# 检查 API key
api_key = os.environ.get("GLM_API_KEY")
if not api_key:
    print("\n❌ 未设置 GLM_API_KEY 环境变量")
    print("   设置方法: export GLM_API_KEY='your-api-key-here'")
    sys.exit(1)
else:
    print(f"✅ GLM_API_KEY 已设置 ({api_key[:10]}...)")

print("\n" + "=" * 60)
print("🎨 微信封面图生成功能测试")
print("=" * 60)

# 测试配置
test_cases = [
    {
        "name": "AI企业文章封面",
        "title": "Claude Cowork企业部署完全指南",
        "theme": "AI企业自动化与协作",
        "style": "flat vector illustration",
        "color_scheme": "blue gradient",
    },
    {
        "name": "科技趋势文章封面",
        "title": "2026年AI代理发展趋势",
        "theme": "AI技术趋势与市场分析",
        "style": "futuristic flat design",
        "color_scheme": "blue and cyan gradient",
    },
]

print(f"\n准备测试 {len(test_cases)} 个案例...")
print("\n提示：")
print("  - 每个测试将调用 GLM-Image API（会产生费用）")
print("  - 生成的图片将保存到 output/test/ 目录")
print("  - 图片将自动调整到 900x386 尺寸")
if not PIL_AVAILABLE:
    print("  - ⚠️  由于未安装 Pillow，将跳过图片调整")

# 询问是否继续
response = input("\n是否继续测试？(y/n): ")
if response.lower() != 'y':
    print("测试已取消")
    sys.exit(0)

# 运行测试
import subprocess

output_dir = "output/test"
os.makedirs(output_dir, exist_ok=True)

results = []
for i, test in enumerate(test_cases, 1):
    print(f"\n{'=' * 60}")
    print(f"测试 {i}/{len(test_cases)}: {test['name']}")
    print(f"{'=' * 60}")

    output_file = os.path.join(output_dir, f"test-{i}-{test['name'].replace(' ', '-')}.png")

    cmd = [
        "python",
        "scripts/generate_cover_photo.py",
        "--title", test["title"],
        "--theme", test["theme"],
        "--style", test["style"],
        "--color-scheme", test["color_scheme"],
        "--output", output_file,
    ]

    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(result.stdout)
        results.append((test["name"], True, output_file))
    except subprocess.CalledProcessError as e:
        print(f"❌ 测试失败: {e}")
        print(e.stderr)
        results.append((test["name"], False, None))

# 总结
print("\n" + "=" * 60)
print("📊 测试总结")
print("=" * 60)

successful = sum(1 for _, success, _ in results if success)
print(f"\n✅ 成功: {successful}/{len(test_cases)}")

if successful < len(test_cases):
    print(f"❌ 失败: {len(test_cases) - successful}/{len(test_cases)}")

print("\n生成的文件:")
for name, success, output_file in results:
    if success:
        # 检查文件尺寸
        if PIL_AVAILABLE and os.path.exists(output_file):
            try:
                img = Image.open(output_file)
                size_str = f"{img.width}x{img.height}"
                size_check = "✅" if (img.width == 900 and img.height == 383) else "⚠️"
                print(f"  {size_check} {name}: {output_file} ({size_str})")
            except Exception as e:
                print(f"  ⚠️  {name}: {output_file} (无法读取尺寸)")
        else:
            print(f"  ✅ {name}: {output_file}")
    else:
        print(f"  ❌ {name}: 生成失败")

print("\n" + "=" * 60)
print("✅ 测试完成！")
print(f"   查看生成的封面图: {output_dir}/")
print("=" * 60)
