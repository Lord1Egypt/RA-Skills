"""Round-trip tests: add → get → verify."""
import os
import tempfile
import shutil
from pathlib import Path
import sys

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from lib.store import Store
from lib.audit import AuditLogger


def test_roundtrip_basic():
    """Test basic add → get round-trip."""
    # Use temporary directory for testing
    with tempfile.TemporaryDirectory() as tmpdir:
        vault_dir = Path(tmpdir)
        store = Store(vault_dir=vault_dir)
        
        # Initialize vault
        master_password = "test-password-12345"
        store.init(master_password)
        
        # Unlock vault
        store.unlock(master_password)
        
        # Add credential
        test_key = "TEST_API_KEY"
        test_value = "secret-value-abc123"
        store.add(test_key, test_value, tags=["test"])
        
        # Get credential
        retrieved_value = store.get(test_key)
        
        # Verify
        assert retrieved_value == test_value, f"Expected {test_value}, got {retrieved_value}"
        print("✅ Basic round-trip test passed")


def test_roundtrip_with_metadata():
    """Test add with metadata → get → verify."""
    with tempfile.TemporaryDirectory() as tmpdir:
        vault_dir = Path(tmpdir)
        store = Store(vault_dir=vault_dir)
        
        master_password = "test-password-12345"
        store.init(master_password)
        store.unlock(master_password)
        
        # Add with metadata
        test_key = "TAGGED_KEY"
        test_value = "tagged-secret-xyz"
        store.add(test_key, test_value, tags=["skill1", "skill2"], expires="2026-12-31")
        
        # Verify value
        retrieved_value = store.get(test_key)
        assert retrieved_value == test_value
        
        # Verify metadata
        credentials = store.list()
        cred = [c for c in credentials if c["name"] == test_key][0]
        assert "skill1" in cred["tags"]
        assert "skill2" in cred["tags"]
        assert cred["expires"] == "2026-12-31"
        
        print("✅ Metadata round-trip test passed")


def test_wrong_password():
    """Test that wrong password fails gracefully."""
    with tempfile.TemporaryDirectory() as tmpdir:
        vault_dir = Path(tmpdir)
        store = Store(vault_dir=vault_dir)
        
        # Initialize with one password
        correct_password = "correct-password"
        store.init(correct_password)
        
        # Try to unlock with wrong password
        wrong_password = "wrong-password"
        try:
            store.unlock(wrong_password)
            assert False, "Should have raised VaultError"
        except Exception as e:
            assert "Incorrect master password" in str(e)
            print("✅ Wrong password test passed")


def test_audit_logging():
    """Test that audit log doesn't contain actual values."""
    with tempfile.TemporaryDirectory() as tmpdir:
        vault_dir = Path(tmpdir)
        audit_file = vault_dir / "audit.log"
        
        store = Store(vault_dir=vault_dir)
        audit = AuditLogger(log_file=audit_file)
        
        master_password = "test-password"
        store.init(master_password)
        store.unlock(master_password)
        
        # Add credential and log
        secret_value = "super-secret-value-do-not-log"
        store.add("SECRET_KEY", secret_value)
        audit.log("add", "SECRET_KEY", {"tags": ["test"]})
        
        # Get credential and log
        store.get("SECRET_KEY")
        audit.log("get", "SECRET_KEY")
        
        # Read audit log
        log_contents = audit_file.read_text()
        
        # Verify secret value is NOT in log
        assert secret_value not in log_contents, "❌ Secret value found in audit log!"
        
        # Verify key name IS in log
        assert "SECRET_KEY" in log_contents
        
        print("✅ Audit logging test passed (no secrets leaked)")


def test_multiple_credentials():
    """Test storing multiple credentials."""
    with tempfile.TemporaryDirectory() as tmpdir:
        vault_dir = Path(tmpdir)
        store = Store(vault_dir=vault_dir)
        
        master_password = "test-password"
        store.init(master_password)
        store.unlock(master_password)
        
        # Add multiple credentials
        credentials = {
            "KEY1": "value1",
            "KEY2": "value2",
            "KEY3": "value3",
        }
        
        for key, value in credentials.items():
            store.add(key, value)
        
        # Verify all can be retrieved
        for key, expected_value in credentials.items():
            retrieved_value = store.get(key)
            assert retrieved_value == expected_value, f"Key {key} mismatch"
        
        print("✅ Multiple credentials test passed")


if __name__ == "__main__":
    print("Running credential vault tests...\n")
    
    test_roundtrip_basic()
    test_roundtrip_with_metadata()
    test_wrong_password()
    test_audit_logging()
    test_multiple_credentials()
    
    print("\n✅ All tests passed!")
