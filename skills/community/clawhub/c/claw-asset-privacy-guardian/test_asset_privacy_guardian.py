#!/usr/bin/env python3
"""
Claw Asset & Privacy Guardian 测试脚本
"""

import os
import tempfile
import shutil
import json
import sys

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from claw_asset_privacy_guardian import PrivacyGuardian, PrivacyFinding, RiskLevel, ProtectionCategory

def create_test_directory() -> str:
    """创建测试目录"""
    temp_dir = tempfile.mkdtemp(prefix="test_privacy_")
    
    # 创建测试文件
    test_files = {
        # 敏感信息测试
        "config_with_keys.py": """
# 测试敏感信息
API_KEY = "sk_test_1234567890abcdef"
STRIPE_SECRET = "sk_live_abcdef1234567890"
DATABASE_URL = "postgresql://user:password123@localhost/db"

# 加密货币地址
WALLET_ADDRESS = "0x742d35Cc6634C0532925a3b844Bc9e90F1f9e5e3"

# 个人信息
EMAIL = "test@example.com"
PHONE = "123-456-7890"
        """,
        
        # 账号安全配置测试
        "auth_config.json": """
{
  "authentication": {
    "enabled": true,
    "mfa": false,
    "session_timeout": 86400,
    "password_policy": {
      "min_length": 6
    }
  }
}
        """,
        
        # 资产安全测试
        "crypto_wallet.txt": """
This is a test file that might contain:
- Bitcoin wallet address: 1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa
- Ethereum address: 0x742d35Cc6634C0532925a3b844Bc9e90F1f9e5e3
- Private key warning: DO NOT SHARE
        """,
        
        # 环境文件测试
        ".env": """
DATABASE_URL=postgresql://user:password@localhost/prod
AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE
AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
STRIPE_SECRET_KEY=sk_live_1234567890
        """,
        
        # 安全文件（应该没有发现）
        "safe_code.py": """
def safe_function():
    return "This code contains no sensitive information"
        """,
    }
    
    # 写入文件
    for filename, content in test_files.items():
        filepath = os.path.join(temp_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content.strip())
    
    return temp_dir

def test_basic_scan():
    """测试基本扫描功能"""
    print("🧪 测试基本扫描功能...")
    
    # 创建测试目录
    test_dir = create_test_directory()
    
    try:
        # 运行扫描
        guardian = PrivacyGuardian()
        report = guardian.scan_directory(test_dir)
        
        print(f"  扫描了 {report.scanned_files} 个文件")
        print(f"  发现 {len(report.findings)} 个隐私安全问题")
        print(f"  敏感文件: {report.sensitive_files_found} 个")
        print(f"  匿名发现: {report.anonymized_findings} 个")
        
        # 验证基本功能
        assert report.scanned_files > 0, "应该扫描一些文件"
        assert len(report.findings) > 0, "应该发现一些隐私安全问题"
        assert report.anonymized_findings == len(report.findings), "所有发现都应该已匿名化"
        
        # 验证风险等级
        stats = report.risk_statistics()
        print(f"  风险统计: {stats}")
        
        # 验证是否有严重或高风险
        has_critical_high = report.has_critical_or_high()
        print(f"  有严重/高风险: {has_critical_high}")
        
        print("  ✅ 基本扫描测试通过")
        return True
        
    finally:
        # 清理测试目录
        shutil.rmtree(test_dir, ignore_errors=True)

def test_anonymization():
    """测试匿名化功能"""
    print("🧪 测试匿名化功能...")
    
    from claw_asset_privacy_guardian import Anonymizer
    
    anonymizer = Anonymizer()
    
    # 测试数据
    test_cases = [
        ("Email: test@example.com", "[EMAIL_REDACTED]"),
        ("Phone: 123-456-7890", "[PHONE_REDACTED]"),
        ("API key: sk_test_123456", "[API_KEY_REDACTED]"),
        ("Wallet: 0x742d35Cc6634C0532925a3b844Bc9e90F1f9e5e3", "[CRYPTO_ADDRESS_REDACTED]"),
    ]
    
    all_passed = True
    for original, expected_pattern in test_cases:
        anonymized = anonymizer.anonymize_text(original)
        
        # 验证匿名化
        if expected_pattern in anonymized:
            print(f"    ✅ {original[:30]}... → 匿名化成功")
        else:
            print(f"    ❌ {original[:30]}... → 匿名化失败: {anonymized}")
            all_passed = False
    
    if all_passed:
        print("  ✅ 匿名化测试通过")
    else:
        print("  ❌ 匿名化测试失败")
    
    return all_passed

def test_report_generation():
    """测试报告生成"""
    print("🧪 测试报告生成...")
    
    # 创建测试目录
    test_dir = create_test_directory()
    
    try:
        guardian = PrivacyGuardian()
        report = guardian.scan_directory(test_dir)
        
        # 测试JSON报告
        json_report = guardian.generate_report(report, "json")
        print(f"  JSON报告长度: {len(json_report)} 字符")
        
        # 验证JSON可以解析
        json_data = json.loads(json_report)
        assert "scan_id" in json_data
        assert "findings" in json_data
        assert "risk_statistics" in json_data
        
        # 验证匿名化
        for finding in json_data["findings"]:
            assert finding["anonymized"] == True, "报告应该已匿名化"
        
        print("    ✅ JSON报告生成和解析成功")
        
        # 测试控制台报告
        console_report = guardian.generate_report(report, "console")
        print(f"  控制台报告长度: {len(console_report)} 字符")
        
        # 验证包含关键信息但不包含敏感信息
        assert "Claw Asset & Privacy Guardian" in console_report
        assert "隐私保护声明" in console_report or "Privacy" in console_report
        assert "test@example.com" not in console_report, "不应该包含具体电子邮件"
        assert "sk_test_" not in console_report, "不应该包含API密钥"
        
        print("    ✅ 控制台报告生成成功")
        
        # 测试Markdown报告
        md_report = guardian.generate_report(report, "markdown")
        print(f"  Markdown报告长度: {len(md_report)} 字符")
        
        assert "# Claw Asset & Privacy Guardian" in md_report
        assert "## 🔒 隐私保护声明" in md_report or "## Privacy" in md_report
        
        print("    ✅ Markdown报告生成成功")
        
        print("  ✅ 报告生成测试通过")
        return True
        
    finally:
        # 清理测试目录
        shutil.rmtree(test_dir, ignore_errors=True)

def test_cli():
    """测试命令行接口"""
    print("🧪 测试命令行接口...")
    
    # 创建测试目录
    test_dir = create_test_directory()
    
    try:
        import subprocess
        
        # 测试基本扫描
        print("  运行命令行扫描...")
        result = subprocess.run(
            [sys.executable, "claw_asset_privacy_guardian.py", test_dir],
            capture_output=True,
            text=True,
            cwd=os.path.dirname(os.path.abspath(__file__))
        )
        
        if result.returncode == 0 or result.returncode == 1:  # 0=无严重问题，1=有严重问题
            print(f"    扫描完成（返回码 {result.returncode}）")
            
            # 验证输出
            assert "Claw Asset & Privacy Guardian" in result.stdout
            assert "隐私保护声明" in result.stdout or "Privacy" in result.stdout
            
            print("    ✅ 命令行扫描测试通过")
        else:
            print(f"    ❌ 命令行扫描失败: {result.stderr}")
            return False
        
        # 测试JSON输出
        print("  运行JSON输出测试...")
        result = subprocess.run(
            [sys.executable, "claw_asset_privacy_guardian.py", test_dir, "--format", "json"],
            capture_output=True,
            text=True,
            cwd=os.path.dirname(os.path.abspath(__file__))
        )
        
        if result.returncode == 0 or result.returncode == 1:
            try:
                json_data = json.loads(result.stdout)
                assert "scan_id" in json_data
                assert "findings" in json_data
                print("    ✅ JSON输出测试通过")
            except json.JSONDecodeError:
                print(f"    ❌ JSON解析失败: {result.stdout[:100]}")
                return False
        else:
            print(f"    ❌ JSON输出失败: {result.stderr}")
            return False
        
        print("  ✅ 命令行接口测试通过")
        return True
        
    finally:
        # 清理测试目录
        shutil.rmtree(test_dir, ignore_errors=True)

def run_all_tests():
    """运行所有测试"""
    print("🔬 运行 Claw Asset & Privacy Guardian 测试套件")
    print("=" * 50)
    
    tests = [
        test_basic_scan,
        test_anonymization,
        test_report_generation,
        test_cli,
    ]
    
    passed = 0
    failed = 0
    
    for test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                failed += 1
        except AssertionError as e:
            print(f"  ❌ 测试失败: {e}")
            failed += 1
        except Exception as e:
            print(f"  ❌ 测试异常: {e}")
            failed += 1
    
    print("=" * 50)
    print(f"测试结果: {passed} 通过, {failed} 失败")
    
    if failed == 0:
        print("🎉 所有测试通过！")
        return 0
    else:
        print("⚠️  部分测试失败")
        return 1

if __name__ == "__main__":
    sys.exit(run_all_tests())