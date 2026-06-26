#!/usr/bin/env python3
"""
安装文档处理技能所需依赖
"""

import sys
import subprocess
import platform

def run_command(cmd, description):
    """运行命令并显示进度"""
    print(f"🔧 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"  ✅ 完成")
            return True
        else:
            print(f"  ❌ 失败: {result.stderr}")
            return False
    except Exception as e:
        print(f"  ❌ 错误: {str(e)}")
        return False

def check_python_version():
    """检查Python版本"""
    print("🐍 检查Python版本...")
    version = sys.version_info
    print(f"  Python版本: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print("  ❌ 需要Python 3.7或更高版本")
        return False
    
    print("  ✅ Python版本符合要求")
    return True

def check_pip():
    """检查pip是否可用"""
    print("📦 检查pip...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "--version"], 
                      capture_output=True, check=True)
        print("  ✅ pip可用")
        return True
    except:
        print("  ❌ pip不可用，请先安装pip")
        return False

def install_dependencies():
    """安装所有依赖"""
    print("=" * 50)
    print("安装文档处理技能依赖")
    print("=" * 50)
    
    # 检查前提条件
    if not check_python_version():
        return False
    
    if not check_pip():
        return False
    
    # 基础依赖
    dependencies = [
        "PyPDF2>=3.0.0",
        "python-docx>=0.8.11",
        "pdf2docx>=0.5.6",
        "Pillow>=9.0.0",
        "pdfplumber>=0.8.0",
        "docx2pdf>=0.1.8",
    ]
    
    # 根据操作系统添加特定依赖
    system = platform.system()
    if system == "Windows":
        dependencies.extend([
            "comtypes>=1.1.14",
            "pywin32>=305",
        ])
        print("🌐 检测到Windows系统，添加Windows特定依赖")
    
    print(f"\n📋 将要安装 {len(dependencies)} 个依赖包:")
    for dep in dependencies:
        print(f"  • {dep}")
    
    print("\n" + "=" * 50)
    
    # 安装每个依赖
    success_count = 0
    fail_count = 0
    
    for dep in dependencies:
        package_name = dep.split('>=')[0] if '>=' in dep else dep.split('==')[0] if '==' in dep else dep
        
        if run_command(f"{sys.executable} -m pip install --upgrade {dep}", f"安装 {package_name}"):
            success_count += 1
        else:
            fail_count += 1
    
    print("\n" + "=" * 50)
    print("安装结果:")
    print(f"  ✅ 成功: {success_count} 个包")
    print(f"  ❌ 失败: {fail_count} 个包")
    
    if fail_count == 0:
        print("\n🎉 所有依赖安装成功!")
        print("\n技能现在可以使用以下功能:")
        print("  • PDF页面提取 (pdf_extractor.py)")
        print("  • PDF转Word (pdf_to_word.py)")
        print("  • Word转PDF (word_to_pdf.py)")
        print("  • PDF合并/拆分 (pdf_merger.py, pdf_splitter.py)")
        print("  • PDF去水印 (remove_watermark.py)")
        print("  • 批量处理 (batch_processor.py)")
        return True
    else:
        print(f"\n⚠  {fail_count} 个包安装失败，部分功能可能受限")
        print("可以尝试手动安装失败的包:")
        print(f"  {sys.executable} -m pip install 包名")
        return False

def check_installed_packages():
    """检查已安装的包"""
    print("🔍 检查已安装的包...")
    
    packages = [
        "PyPDF2",
        "python-docx", 
        "pdf2docx",
        "Pillow",
        "pdfplumber",
        "docx2pdf",
    ]
    
    if platform.system() == "Windows":
        packages.extend(["comtypes", "pywin32"])
    
    installed = []
    missing = []
    
    for package in packages:
        try:
            subprocess.run([sys.executable, "-m", "pip", "show", package], 
                          capture_output=True, check=True)
            installed.append(package)
        except:
            missing.append(package)
    
    print(f"  ✅ 已安装: {len(installed)} 个包")
    for pkg in installed:
        print(f"    • {pkg}")
    
    if missing:
        print(f"  ❌ 缺失: {len(missing)} 个包")
        for pkg in missing:
            print(f"    • {pkg}")
    
    return len(missing) == 0

def main():
    parser = argparse.ArgumentParser(description='安装文档处理技能依赖')
    parser.add_argument('--check', action='store_true', help='只检查不安装')
    parser.add_argument('--upgrade', action='store_true', help='升级已安装的包')
    
    args = parser.parse_args()
    
    if args.check:
        return 0 if check_installed_packages() else 1
    
    return 0 if install_dependencies() else 1

if __name__ == "__main__":
    # 添加argparse导入
    import argparse
    sys.exit(main())