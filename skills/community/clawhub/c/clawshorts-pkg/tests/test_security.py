"""Tests for security module."""
import pytest
from clawshorts.validators import validate_ip
from clawshorts.security import sanitize_log_message


class TestValidateIP:
    """Tests for IP validation."""
    
    def test_valid_ip(self):
        """Test valid IP addresses."""
        assert validate_ip("192.168.1.1") is True
        assert validate_ip("10.0.0.1") is True
        assert validate_ip("255.255.255.255") is True
    
    def test_invalid_ip_octet_overflow(self):
        """Test invalid IP with octet > 255."""
        assert validate_ip("256.1.1.1") is False
        assert validate_ip("192.168.1.256") is False
    
    def test_invalid_ip_format(self):
        """Test invalid IP formats."""
        assert validate_ip("192.168.1") is False
        assert validate_ip("192.168.1.1.1") is False
        assert validate_ip("abc.def.ghi.jkl") is False
        assert validate_ip("") is False


class TestSanitizeLogMessage:
    """Tests for log sanitization."""
    
    def test_masks_ip(self):
        """Test IP addresses are masked."""
        result = sanitize_log_message("Connecting to 192.168.1.100")
        assert "192.168.1.100" not in result
        assert "[IP]" in result
    
    def test_masks_tokens(self):
        """Test tokens are masked."""
        result = sanitize_log_message("Token: abcdefghijklmnopqrstuvwxyz")
        assert "abcdefghijklmnopqrstuvwxyz" not in result
        assert "[TOKEN]" in result
