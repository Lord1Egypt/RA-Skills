#!/usr/bin/env python3
"""
基础测试脚本 - 测试flowchart-gen技能的基本功能
"""

import os
import sys
import subprocess

def test_mermaid_installation():
    """测试Mermaid CLI是否安装"""
    print("1. 测试Mermaid CLI安装...")
    try:
        result = subprocess.run(["mmdc", "--version"], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("   ✅ Mermaid CLI 已安装")
            # 提取版本信息
            for line in result.stdout.split('\n'):
                if 'version' in line.lower():
                    print(f"     版本: {line.strip()}")
                    break
            return True
        else:
            print("   ❌ Mermaid CLI 安装异常")
            return False
    except FileNotFoundError:
        print("   ❌ 未找到Mermaid CLI (mmdc)")
        print("      请安装: npm install -g @mermaid-js/mermaid-cli")
        return False

def test_python_deps():
    """测试Python依赖"""
    print("\n2. 测试Python依赖...")
    
    # 测试PIL/Pillow
    try:
        from PIL import Image
        print("   ✅ PIL/Pillow 已安装")
        print(f"     版本: {Image.__version__}")
    except ImportError:
        print("   ⚠️  PIL/Pillow 未安装（可选）")
        print("      基础图像生成功能将受限")
        print("      安装: pip install pillow")
    
    # 测试其他标准库
    required_libs = ['json', 'argparse', 'tempfile', 'subprocess']
    all_ok = True
    for lib in required_libs:
        try:
            __import__(lib)
            print(f"   ✅ {lib} 可用")
        except ImportError:
            print(f"   ❌ {lib} 不可用")
            all_ok = False
    
    return all_ok

def test_generate_script():
    """测试主生成脚本"""
    print("\n3. 测试生成脚本...")
    
    script_path = os.path.join(os.path.dirname(__file__), "generate.py")
    
    if not os.path.exists(script_path):
        print(f"   ❌ 未找到脚本: {script_path}")
        return False
    
    # 测试脚本是否能正常导入（不执行）
    try:
        with open(script_path, 'r', encoding='utf-8') as f:
            content = f.read()
        print(f"   ✅ 脚本文件存在 ({len(content)} 字节)")
        
        # 检查必要的函数是否存在
        required_functions = ['main', 'ai_to_mermaid', 'generate_with_mermaid']
        for func in required_functions:
            if f'def {func}' in content:
                print(f"     函数 {func}() 存在")
            else:
                print(f"     ⚠️  函数 {func}() 未找到")
        
        return True
    except Exception as e:
        print(f"   ❌ 读取脚本失败: {e}")
        return False

def test_templates():
    """测试模板文件"""
    print("\n4. 测试模板文件...")
    
    templates_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "templates")
    
    if not os.path.exists(templates_dir):
        print(f"   ❌ 模板目录不存在: {templates_dir}")
        return False
    
    template_files = os.listdir(templates_dir)
    if not template_files:
        print(f"   ❌ 模板目录为空: {templates_dir}")
        return False
    
    print(f"   ✅ 找到 {len(template_files)} 个模板文件:")
    for file in template_files:
        filepath = os.path.join(templates_dir, file)
        size = os.path.getsize(filepath)
        print(f"      - {file} ({size} 字节)")
    
    # 检查模板内容
    for file in template_files:
        if file.endswith('.mmd'):
            filepath = os.path.join(templates_dir, file)
            with open(filepath, 'r', encoding='utf-8') as f:
                first_line = f.readline().strip()
            print(f"      {file}: {first_line[:50]}...")
    
    return True

def test_quick_generation():
    """快速生成测试"""
    print("\n5. 快速生成测试...")
    
    script_path = os.path.join(os.path.dirname(__file__), "generate.py")
    output_file = "test_output.png"
    
    # 如果存在先删除
    if os.path.exists(output_file):
        os.remove(output_file)
    
    # 运行测试命令
    cmd = [sys.executable, script_path, "测试流程图", "-o", output_file, "--verbose"]
    
    print(f"   执行命令: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            if os.path.exists(output_file):
                size = os.path.getsize(output_file)
                print(f"   ✅ 成功生成测试文件: {output_file} ({size} 字节)")
                
                # 清理测试文件
                os.remove(output_file)
                print("      测试文件已清理")
                return True
            else:
                print(f"   ❌ 输出文件未生成")
                print(f"     标准输出:\n{result.stdout}")
                print(f"     错误输出:\n{result.stderr}")
                return False
        else:
            print(f"   ❌ 命令执行失败 (退出码: {result.returncode})")
            print(f"     标准输出:\n{result.stdout}")
            print(f"     错误输出:\n{result.stderr}")
            return False
    
    except subprocess.TimeoutExpired:
        print("   ❌ 命令执行超时 (60秒)")
        return False
    except Exception as e:
        print(f"   ❌ 执行异常: {e}")
        return False

def main():
    """主测试函数"""
    print("="*60)
    print("flowchart-gen 技能测试")
    print("="*60)
    
    tests = [
        test_mermaid_installation,
        test_python_deps,
        test_generate_script,
        test_templates,
        test_quick_generation
    ]
    
    results = []
    for test_func in tests:
        try:
            result = test_func()
            results.append(result)
        except Exception as e:
            print(f"   ❌ 测试异常: {e}")
            results.append(False)
    
    print("\n" + "="*60)
    print("测试总结:")
    print("="*60)
    
    passed = sum(results)
    total = len(results)
    
    print(f"通过: {passed}/{total} 项测试")
    
    if passed == total:
        print("✅ 所有测试通过! flowchart-gen 技能可以正常工作。")
        print("\n下一步:")
        print("  1. 查看技能文档: cat SKILL.md")
        print("  2. 运行示例: python scripts/generate.py '用户登录流程' -o login.png")
        print("  3. 探索模板: ls templates/")
    else:
        print("⚠️  部分测试未通过，需要修复。")
        print("\n建议:")
        print("  1. 安装Mermaid CLI: npm install -g @mermaid-js/mermaid-cli")
        print("  2. 安装Python依赖: pip install pillow")
        print("  3. 检查脚本权限: chmod +x scripts/*.py")
        
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())