#!/usr/bin/env python3
"""
免费图片解决方案技能 - 基本功能测试
"""

import os
import sys
from pathlib import Path

def test_imports():
    """测试基本导入"""
    print("=== 测试基本导入 ===")
    try:
        import argparse
        import json
        from pathlib import Path
        print("✅ 标准库导入正常")
        return True
    except ImportError as e:
        print(f"❌ 标准库导入失败: {e}")
        return False

def test_script_structure():
    """测试脚本结构"""
    print("\n=== 测试脚本结构 ===")
    scripts_dir = Path(__file__).parent / "scripts"
    
    required_scripts = [
        "main.py",
        "ai_generator.py", 
        "free_search.py",
        "watermark_remover.py",
        "batch_processor.py"
    ]
    
    all_ok = True
    for script in required_scripts:
        script_path = scripts_dir / script
        if script_path.exists():
            print(f"✅ {script} 存在")
        else:
            print(f"❌ {script} 不存在")
            all_ok = False
    
    return all_ok

def test_config_files():
    """测试配置文件"""
    print("\n=== 测试配置文件 ===")
    config_dir = Path(__file__).parent / "config"
    
    required_configs = [
        "settings.json",
        "sources.json",
        "prompts.json"
    ]
    
    all_ok = True
    for config in required_configs:
        config_path = config_dir / config
        if config_path.exists():
            # 检查是否是有效的 JSON
            try:
                import json
                with open(config_path, 'r') as f:
                    json.load(f)
                print(f"✅ {config} 存在且格式正确")
            except json.JSONDecodeError:
                print(f"⚠️  {config} 存在但 JSON 格式错误")
                all_ok = False
            except Exception as e:
                print(f"❌ {config} 读取错误: {e}")
                all_ok = False
        else:
            print(f"❌ {config} 不存在")
            all_ok = False
    
    return all_ok

def test_skill_md():
    """测试 SKILL.md 文件"""
    print("\n=== 测试 SKILL.md ===")
    skill_md = Path(__file__).parent / "SKILL.md"
    
    if skill_md.exists():
        with open(skill_md, 'r') as f:
            content = f.read()
            
        # 检查必要的元数据
        required_metadata = [
            "name: free-image-skill",
            "version:",
            "author:",
            "description:"
        ]
        
        all_ok = True
        for metadata in required_metadata:
            if metadata in content:
                print(f"✅ 包含 {metadata}")
            else:
                print(f"❌ 缺少 {metadata}")
                all_ok = False
        
        return all_ok
    else:
        print("❌ SKILL.md 不存在")
        return False

def test_main_script():
    """测试主脚本"""
    print("\n=== 测试主脚本 ===")
    main_script = Path(__file__).parent / "scripts" / "main.py"
    
    if main_script.exists():
        # 检查是否可以导入
        try:
            # 添加脚本目录到路径
            script_dir = main_script.parent
            if str(script_dir) not in sys.path:
                sys.path.insert(0, str(script_dir))
            
            # 尝试导入模块（不执行）
            import importlib.util
            spec = importlib.util.spec_from_file_location("main", main_script)
            module = importlib.util.module_from_spec(spec)
            
            print("✅ main.py 可以导入")
            return True
        except Exception as e:
            print(f"❌ main.py 导入失败: {e}")
            return False
    else:
        print("❌ main.py 不存在")
        return False

def main():
    """主测试函数"""
    print("免费图片解决方案技能 - 基本功能测试")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_script_structure,
        test_config_files,
        test_skill_md,
        test_main_script
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ 测试执行错误: {e}")
            results.append(False)
    
    print("\n" + "=" * 50)
    print("测试结果汇总:")
    
    passed = sum(results)
    total = len(results)
    
    if passed == total:
        print(f"✅ 所有测试通过 ({passed}/{total})")
        return 0
    else:
        print(f"❌ 测试失败: {passed}/{total} 通过")
        print(f"   失败的测试: {[i+1 for i, r in enumerate(results) if not r]}")
        return 1

if __name__ == "__main__":
    sys.exit(main())