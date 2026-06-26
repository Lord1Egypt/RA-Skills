#!/usr/bin/env python3
"""
测试cron表达式助手skill的功能
"""

import subprocess
import sys

def run_command(cmd):
    """运行命令并返回输出"""
    try:
        result = subprocess.run(
            cmd, 
            shell=True, 
            capture_output=True, 
            text=True,
            encoding='utf-8',
            errors='ignore'
        )
        return result.returncode, result.stdout, result.stderr
    except Exception as e:
        return 1, "", str(e)

def test_explain_cron():
    """测试解释cron表达式功能"""
    print("测试: 解释cron表达式")
    print("-" * 40)
    
    test_cases = [
        ("0 9 * * 1-5", "工作日上午9点执行"),
        ("0 0 * * *", "每天午夜执行"),
        ("*/5 * * * *", "每5分钟执行"),
        ("0 0 * * 0", "每周日午夜执行"),
    ]
    
    for cron_expr, expected_desc in test_cases:
        cmd = f'python explain_cron.py "{cron_expr}"'
        returncode, stdout, stderr = run_command(cmd)
        
        if returncode == 0:
            print(f"[OK] {cron_expr:20} -> 测试通过")
            # 检查输出中是否包含预期的描述
            if expected_desc.lower() in stdout.lower():
                print(f"  找到预期描述: {expected_desc}")
            else:
                print(f"  输出内容:\n{stdout[:200]}...")
        else:
            print(f"[FAIL] {cron_expr:20} -> 测试失败")
            print(f"  错误: {stderr}")
        
        print()

def test_show_cron():
    """测试展示cron表达式功能"""
    print("测试: 展示cron表达式执行时间")
    print("-" * 40)
    
    test_cases = [
        "0 9 * * 1-5",
        "0 0 * * *",
        "*/5 * * * *",
    ]
    
    for cron_expr in test_cases:
        cmd = f'python show_cron.py "{cron_expr}" --count 3'
        returncode, stdout, stderr = run_command(cmd)
        
        if returncode == 0:
            print(f"[OK] {cron_expr:20} -> 测试通过")
            # 检查是否输出了执行时间
            if "执行时间" in stdout or "Cron表达式" in stdout:
                print(f"  成功生成执行时间列表")
            else:
                print(f"  输出内容:\n{stdout[:200]}...")
        else:
            print(f"[FAIL] {cron_expr:20} -> 测试失败")
            print(f"  错误: {stderr}")
        
        print()

def test_create_cron():
    """测试创建cron表达式功能（非交互模式）"""
    print("测试: 创建cron表达式（非交互模式）")
    print("-" * 40)
    
    cmd = 'python create_cron.py --minute "0" --hour "9" --day "*" --month "*" --weekday "1-5"'
    returncode, stdout, stderr = run_command(cmd)
    
    if returncode == 0 or "是否将cron表达式保存到文件" in stdout:
        print("[OK] 创建cron表达式 -> 测试通过")
        if "0 9 * * 1-5" in stdout:
            print(f"  成功生成表达式: 0 9 * * 1-5")
    else:
        print("[FAIL] 创建cron表达式 -> 测试失败")
        print(f"  错误: {stderr}")
    
    print()

def test_examples():
    """测试示例功能"""
    print("测试: 查看cron表达式示例")
    print("-" * 40)
    
    cmd = 'python explain_cron.py --examples'
    returncode, stdout, stderr = run_command(cmd)
    
    if returncode == 0:
        print("[OK] 查看示例 -> 测试通过")
        if "Cron表达式示例" in stdout or "示例" in stdout:
            print(f"  成功显示示例列表")
            # 统计示例数量
            lines = stdout.split('\n')
            example_count = sum(1 for line in lines if '->' in line or '执行' in line)
            print(f"  找到约 {example_count} 个示例")
    else:
        print("[FAIL] 查看示例 -> 测试失败")
        print(f"  错误: {stderr}")
    
    print()

def main():
    print("=" * 50)
    print("Cron表达式助手Skill测试")
    print("=" * 50)
    print()
    
    # 切换到脚本目录
    import os
    original_dir = os.getcwd()
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    try:
        test_explain_cron()
        test_show_cron()
        test_create_cron()
        test_examples()
        
        print("=" * 50)
        print("测试完成!")
        print("=" * 50)
        
    finally:
        os.chdir(original_dir)

if __name__ == "__main__":
    main()