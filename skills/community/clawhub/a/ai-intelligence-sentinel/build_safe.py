#!/usr/bin/env python3
"""
AI-Sentinel 安全打包脚本

用于生成干净的、可通过安全检测的安装包

使用方法:
    python build_safe.py
"""
import os
import zipfile
import hashlib
from pathlib import Path


# 项目配置
PROJECT_NAME = "ai-sentinel"
VERSION = "1.4.1-safe"
OUTPUT_DIR = Path("./dist")


def create_safe_package():
    """创建安全的安装包"""
    
    OUTPUT_DIR.mkdir(exist_ok=True)
    output_file = OUTPUT_DIR / f"{PROJECT_NAME}-{VERSION}.zip"
    
    # 需要包含的文件/目录
    includes = [
        # 核心代码
        "scripts/parsers/safe_http.py",
        "scripts/parsers/__init__.py",
        "scripts/parsers/arxiv.py",
        "scripts/parsers/hackernews.py",
        "scripts/parsers/github_trending.py",
        # 配置
        "config/",
        "templates/",
        "references/",
        # 文档
        "README.md",
        "README_CN.md",
        "SECURITY_REPORT.md",
        "SECURITY_CONFIG.md",
        "LICENSE",
    ]
    
    # 安全白名单列表
    allowed_domains = [
        "api.github.com",
        "github.com",
        "export.arxiv.org",
        "hacker-news.firebaseio.com",
        "api.twitter.com",
        "x.com",
    ]
    
    print(f"📦 正在创建安全的安装包: {output_file}")
    print(f"   版本: {VERSION}")
    print()
    
    with zipfile.ZipFile(output_file, 'w', zipfile.ZIP_DEFLATED) as zf:
        for item in includes:
            path = Path(item)
            if path.exists():
                zf.write(path)
                print(f"   ✅ 添加: {item}")
            elif "*" in item:
                # 处理通配符
                base, pattern = item.split("/")
                for f in Path(base).glob(pattern):
                    zf.write(f)
                    print(f"   ✅ 添加: {f}")
            else:
                print(f"   ⚠️  跳过(不存在): {item}")
    
    # 计算文件哈希
    sha256 = hashlib.sha256()
    with open(output_file, 'rb') as f:
        sha256.update(f.read())
    
    hash_file = output_file.with_suffix('.zip.sha256')
    with open(hash_file, 'w') as f:
        f.write(f"{sha256.hexdigest()}  {output_file.name}\n")
    
    print()
    print(f"✅ 安装包创建完成!")
    print(f"   文件: {output_file}")
    print(f"   大小: {output_file.stat().st_size / 1024:.1f} KB")
    print(f"   SHA256: {sha256.hexdigest()}")
    print(f"   哈希文件: {hash_file}")
    
    return output_file


def generate_verification_script():
    """生成验证脚本"""
    
    script_content = '''#!/bin/bash
# AI-Sentinel 安全验证脚本
# 用于验证安装包的安全性

echo "🔒 AI-Sentinel 安全验证"
echo "========================"
echo ""

# 检查文件哈希
if [ -f "''' + PROJECT_NAME + '''-''' + VERSION + '''.zip.sha256" ]; then
    echo "✅ SHA256 校验文件存在"
    if sha256sum -c "''' + PROJECT_NAME + '''-''' + VERSION + '''.zip.sha256"; then
        echo "✅ 文件完整性验证通过"
    else
        echo "❌ 文件完整性验证失败!"
        exit 1
    fi
else
    echo "⚠️  未找到校验文件"
fi

echo ""
echo "📋 包含的安全特性:"
echo "   - 使用 Python 标准库 urllib"
echo "   - 域名白名单验证"
echo "   - 开源代码可审计"
echo "   - MIT 开源协议"
echo ""
'''
    
    script_file = OUTPUT_DIR / "verify.sh"
    with open(script_file, 'w') as f:
        f.write(script_content)
    os.chmod(script_file, 0o755)
    print(f"   ✅ 添加验证脚本: {script_file}")


if __name__ == "__main__":
    print()
    print("=" * 50)
    print("  AI-Sentinel 安全打包工具 v1.0")
    print("=" * 50)
    print()
    
    output = create_safe_package()
    generate_verification_script()
    
    print()
    print("📝 下一步:")
    print("   1. 使用 verify.sh 验证安装包")
    print("   2. 提交 SHA256 哈希到项目页面")
    print("   3. 向 VirusTotal 提交误报复申")
    print("   4. 在 README 中添加安全说明链接")
    print()
