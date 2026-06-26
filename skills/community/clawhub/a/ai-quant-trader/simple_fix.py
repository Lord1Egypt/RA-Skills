#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python环境修复脚本
"""

import sys
import subprocess
import os

def check_python():
    """检查Python环境"""
    print("🔧 检查Python环境...")
    
    # Python版本
    print(f"Python版本: {sys.version}")
    print(f"Python路径: {sys.executable}")
    
    return True

def install_dependencies():
    """安装依赖"""
    print("📦 安装必要依赖...")
    
    dependencies = [
        "akshare",
        "pandas",
        "numpy",
        "tqdm"
    ]
    
    for dep in dependencies:
        print(f"  安装 {dep}...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", dep, "--quiet"])
            print(f"  ✅ {dep} 安装成功")
        except subprocess.CalledProcessError:
            print(f"  ⚠️  {dep} 安装失败，尝试继续...")
    
    return True

def test_imports():
    """测试导入"""
    print("🧪 测试模块导入...")
    
    modules = {
        "akshare": "数据获取",
        "pandas": "数据处理",
        "numpy": "数值计算"
    }
    
    all_ok = True
    for module, desc in modules.items():
        try:
            __import__(module)
            print(f"  ✅ {desc}({module}): 正常")
        except ImportError as e:
            print(f"  ❌ {desc}({module}): 失败 - {e}")
            all_ok = False
    
    return all_ok

def setup_environment():
    """设置环境"""
    print("⚙️ 设置环境变量...")
    
    # 添加当前目录到Python路径
    current_dir = os.path.dirname(os.path.abspath(__file__))
    if current_dir not in sys.path:
        sys.path.insert(0, current_dir)
    
    print(f"  添加路径: {current_dir}")
    
    # 创建必要的目录
    directories = [
        "user_data",
        "data_cache",
        "screener_cache",
        "screening_results"
    ]
    
    for dir_name in directories:
        dir_path = os.path.join(current_dir, dir_name)
        os.makedirs(dir_path, exist_ok=True)
        print(f"  创建目录: {dir_path}")
    
    return True

def main():
    """主函数"""
    print("=" * 60)
    print("🐍 Python环境修复工具")
    print("=" * 60)
    
    try:
        # 检查Python
        if not check_python():
            return False
        
        # 安装依赖
        if not install_dependencies():
            print("⚠️ 依赖安装有警告，但继续...")
        
        # 测试导入
        if not test_imports():
            print("⚠️ 部分模块导入失败，但继续...")
        
        # 设置环境
        setup_environment()
        
        print("=" * 60)
        print("🎉 Python环境修复完成！")
        print("=" * 60)
        
        # 测试简单功能
        print("\n🧪 测试简单功能...")
        test_code = """
print("✅ Python环境正常")
print(f"工作目录: {os.getcwd()}")
print(f"Python路径: {sys.executable}")
"""
        exec(test_code)
        
        return True
        
    except Exception as e:
        print(f"❌ 修复过程中出现错误: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)