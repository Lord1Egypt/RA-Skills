#!/usr/bin/env python3
"""
Email Bridge Test Script
Run this to verify your Email Bridge installation.
"""

import sys
from pathlib import Path

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent))

from email_bridge.service import EmailBridgeService
from email_bridge.models import EmailProvider


def test_database():
    """Test database initialization."""
    print("📦 Testing database...")
    service = EmailBridgeService()
    accounts = service.list_accounts()
    print(f"   ✓ Database initialized ({len(accounts)} accounts)")
    return service


def test_mock_adapter():
    """Test mock adapter."""
    print("\n🎭 Testing mock adapter...")
    service = EmailBridgeService()
    
    # Check if mock account exists
    accounts = service.list_accounts()
    mock_account = next((a for a in accounts if a.provider == EmailProvider.MOCK), None)
    
    if not mock_account:
        # Add mock account
        mock_account = service.add_account(
            email="demo@example.com",
            provider=EmailProvider.MOCK,
            display_name="Demo Account"
        )
        print(f"   ✓ Created mock account: {mock_account.email}")
    
    # Sync messages
    count = service.sync_account(mock_account.id)
    print(f"   ✓ Synced {count} messages from mock adapter")
    
    # List messages
    messages = service.list_recent_messages(account_id=mock_account.id, limit=5)
    print(f"   ✓ Retrieved {len(messages)} messages")
    
    return True


def test_verification_extraction():
    """Test verification code extraction."""
    print("\n🔢 Testing verification code extraction...")
    from email_bridge.extraction import extract_from_email
    
    # Test cases
    test_cases = [
        ("验证码: 123456", "您的验证码是 123456，5分钟内有效"),
        ("Your code is: 789012", "Your verification code: 789012"),
        ("验证码：ABC123", "短信验证码 ABC123"),
    ]
    
    for subject, body in test_cases:
        result = extract_from_email(subject=subject, body_text=body)
        if result['codes']:
            print(f"   ✓ Extracted: {result['codes'][0].code} from '{subject}'")
        else:
            print(f"   ✗ Failed to extract from '{subject}'")
            return False
    
    return True


def test_accounts_command():
    """Test accounts list command."""
    print("\n👥 Testing accounts command...")
    service = EmailBridgeService()
    accounts = service.list_accounts()
    
    print(f"   ✓ Found {len(accounts)} account(s):")
    for acc in accounts:
        print(f"     - {acc.email} ({acc.provider.value})")
    
    return True


def main():
    print("=" * 50)
    print("📧 Email Bridge Test Suite")
    print("=" * 50)
    
    tests = [
        ("Database", test_database),
        ("Mock Adapter", test_mock_adapter),
        ("Verification Extraction", test_verification_extraction),
        ("Accounts Command", test_accounts_command),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result, None))
        except Exception as e:
            results.append((name, False, str(e)))
    
    print("\n" + "=" * 50)
    print("📊 Test Results")
    print("=" * 50)
    
    passed = sum(1 for _, r, _ in results if r)
    total = len(results)
    
    for name, result, error in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {status}: {name}")
        if error:
            print(f"         Error: {error}")
    
    print(f"\n总计: {passed}/{total} 通过")
    
    if passed == total:
        print("\n🎉 所有测试通过！Email Bridge 工作正常。")
        return 0
    else:
        print("\n⚠️ 部分测试失败，请检查上述错误。")
        return 1


if __name__ == "__main__":
    sys.exit(main())