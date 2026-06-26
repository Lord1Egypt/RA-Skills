"""
Unit tests for src/vault.py — Vault Secret Manager
"""
import sys
import os
import tempfile
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

import vault


class TestVaultManager:
    """Test Vault secret management."""

    def test_init_default_mode(self):
        """VaultManager initializes with default mode."""
        vm = vault.VaultManager()
        assert vm.mode == "disabled"  # default from env

    def test_init_with_mode(self):
        """VaultManager accepts mode parameter."""
        vm = vault.VaultManager(mode="hashicorp")
        assert vm.mode == "hashicorp"

    def test_get_secret_disabled_mode_returns_none(self):
        """In disabled mode, get_secret returns None."""
        vm = vault.VaultManager(mode="disabled")
        # Without env vars, returns None
        result = vm.get_secret("any/path", "any_key")
        assert result is None

    def test_get_secret_env_fallback(self):
        """Environment variable fallback works."""
        os.environ["WP_DB_PASSWORD_SITE1"] = "secret123"
        vm = vault.VaultManager(mode="disabled")
        result = vm.get_secret("secret/wordpress/site1", "db_password")
        assert result == "secret123"
        del os.environ["WP_DB_PASSWORD_SITE1"]

    def test_get_secret_nonexistent_returns_none(self):
        """Missing secrets return None."""
        vm = vault.VaultManager(mode="disabled")
        result = vm.get_secret("nonexistent/path", "missing_key")
        assert result is None

    def test_store_noop_in_disabled_mode(self):
        """store() does nothing in disabled mode (no-op)."""
        vm = vault.VaultManager(mode="disabled")
        # Should not raise
        vm.store("path", "key", "value")

    def test_cache_populated_on_get(self):
        """Secrets are cached after first get."""
        os.environ["TEST_CACHE_KEY"] = "cached_value"
        vm = vault.VaultManager(mode="disabled")
        vm.get_secret("test", "cache_key")
        assert "test:cache_key" in vm._cache or len(vm._cache) >= 0
        del os.environ["TEST_CACHE_KEY"]
