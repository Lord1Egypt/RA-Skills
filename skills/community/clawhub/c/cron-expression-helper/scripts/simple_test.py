#!/usr/bin/env python3
"""
简单的cron表达式助手skill测试
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

def main():
    print("Cron表达式助手Skill简单测试")
    print("=" * 50)
    
    # 切换到脚本目录
    import os
    original_dir = os.getcwd()
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    test_results = []
    
    try:
        # 测试1: 解释cron表达式
        print("\n1. 测试解释cron表达式:")
        cmd = 'python explain_cron.py "0 9 * * 1-5"'
        returncode, stdout, stderr = run_command(cmd)
        
        if returncode == 0:
            # 使用字节方式检查中文字符
            stdout_bytes = stdout.encode('utf-8', errors='ignore')
            if b'\xe8\xa1\xa8\xe8\xbe\xbe\xe5\xbc\x8f\xe8\xa7\xa3\xe9\x87\x8a' in stdout_bytes:  # "表达式解释"的UTF-8字节
                print("  通过: 成功解释cron表达式")
                test_results.append(True)
            else:
                print("  失败: 输出中未找到'表达式解释'")
                test_results.append(False)
        else:
            print(f"  失败: 返回码={returncode}, 错误={stderr[:100]}")
            test_results.append(False)
        
        # 测试2: 查看示例
        print("\n2. 测试查看示例:")
        cmd = 'python explain_cron.py --examples'
        returncode, stdout, stderr = run_command(cmd)
        
        if returncode == 0:
            stdout_bytes = stdout.encode('utf-8', errors='ignore')
            if b'\xe7\xa4\xba\xe4\xbe\x8b' in stdout_bytes or b'Cron\xe8\xa1\xa8\xe8\xbe\xbe\xe5\xbc\x8f\xe7\xa4\xba\xe4\xbe\x8b' in stdout_bytes:
                print("  通过: 成功显示示例")
                test_results.append(True)
            else:
                print("  失败: 输出中未找到'示例'")
                test_results.append(False)
        else:
            print(f"  失败: 返回码={returncode}")
            test_results.append(False)
        
        # 测试3: 展示cron表达式执行时间
        print("\n3. 测试展示执行时间:")
        cmd = 'python show_cron.py "0 0 * * *" --count 3'
        returncode, stdout, stderr = run_command(cmd)
        
        if returncode == 0:
            stdout_bytes = stdout.encode('utf-8', errors='ignore')
            if b'\xe6\x89\xa7\xe8\xa1\x8c\xe6\x97\xb6\xe9\x97\xb4' in stdout_bytes or b'Cron\xe8\xa1\xa8\xe8\xbe\xbe\xe5\xbc\x8f' in stdout_bytes:
                print("  通过: 成功生成执行时间")
                test_results.append(True)
            else:
                print("  失败: 输出中未找到'执行时间'或'Cron表达式'")
                test_results.append(False)
        else:
            print(f"  失败: 返回码={returncode}, 错误={stderr[:100]}")
            test_results.append(False)
        
        # 测试4: 验证无效cron表达式
        print("\n4. 测试验证无效表达式:")
        cmd = 'python show_cron.py "invalid expression"'
        returncode, stdout, stderr = run_command(cmd)
        
        if returncode != 0:
            print("  通过: 正确识别无效表达式（非零返回码）")
            test_results.append(True)
        else:
            stdout_bytes = stdout.encode('utf-8', errors='ignore')
            if b'\xe6\x97\xa0\xe6\x95\x88' in stdout_bytes or b'Invalid' in stdout_bytes:
                print("  通过: 正确识别无效表达式（输出中包含'无效'）")
                test_results.append(True)
            else:
                print("  失败: 未正确识别无效表达式")
                test_results.append(False)
        
        # 总结
        print("\n" + "=" * 50)
        passed = sum(test_results)
        total = len(test_results)
        print(f"测试结果: {passed}/{total} 通过")
        
        if passed == total:
            print("所有测试通过! Skill功能正常。")
        else:
            print(f"有 {total - passed} 个测试失败。")
        
        print("=" * 50)
        
    finally:
        os.chdir(original_dir)

if __name__ == "__main__":
    main()