"""
Tests for format utilities.

Tests verify formatting for sizes, durations, and timestamps.
"""

import pytest
from datetime import datetime
from toolkit.utils.formatters import Formatters


class TestFormatters:
    """Test cases for Formatters."""
    
    def test_format_file_size_bytes(self):
        """Test formatting bytes."""
        assert Formatters.format_file_size(500) == "500.0 B"
    
    def test_format_file_size_kilobytes(self):
        """Test formatting kilobytes."""
        assert Formatters.format_file_size(1024) == "1.0 KB"
        assert Formatters.format_file_size(1536) == "1.5 KB"
    
    def test_format_file_size_megabytes(self):
        """Test formatting megabytes."""
        assert Formatters.format_file_size(1048576) == "1.0 MB"
        assert Formatters.format_file_size(1572864) == "1.5 MB"
    
    def test_format_file_size_gigabytes(self):
        """Test formatting gigabytes."""
        assert Formatters.format_file_size(1073741824) == "1.0 GB"
    
    def test_format_duration_seconds(self):
        """Test formatting duration in seconds."""
        assert Formatters.format_duration(30) == "30.0s"
        assert Formatters.format_duration(45.5) == "45.5s"
    
    def test_format_duration_minutes(self):
        """Test formatting duration in minutes."""
        assert Formatters.format_duration(90) == "1m 30s"
        assert Formatters.format_duration(150) == "2m 30s"
    
    def test_format_duration_hours(self):
        """Test formatting duration in hours."""
        assert Formatters.format_duration(3661) == "1h 1m"
        assert Formatters.format_duration(7325) == "2h 2m"
    
    def test_format_timestamp_datetime(self):
        """Test formatting datetime object."""
        dt = datetime(2024, 1, 15, 10, 30, 45)
        result = Formatters.format_timestamp(dt)
        assert result == "2024-01-15 10:30:45"
    
    def test_format_timestamp_iso_string(self):
        """Test formatting ISO string."""
        iso_str = "2024-01-15T10:30:45"
        result = Formatters.format_timestamp(iso_str)
        assert result == "2024-01-15 10:30:45"
    
    def test_format_timestamp_unix(self):
        """Test formatting Unix timestamp."""
        unix_ts = 1705315845.0
        result = Formatters.format_timestamp(unix_ts)
        assert len(result) > 0
    
    def test_format_timestamp_custom_format(self):
        """Test formatting with custom format."""
        dt = datetime(2024, 1, 15, 10, 30, 45)
        result = Formatters.format_timestamp(dt, "%Y/%m/%d")
        assert result == "2024/01/15"
    
    def test_format_progress_zero(self):
        """Test progress bar at zero."""
        result = Formatters.format_progress(0, 100)
        assert "0%" in result
    
    def test_format_progress_half(self):
        """Test progress bar at half."""
        result = Formatters.format_progress(50, 100)
        assert "50%" in result
    
    def test_format_progress_complete(self):
        """Test progress bar at complete."""
        result = Formatters.format_progress(100, 100)
        assert "100%" in result
    
    def test_format_progress_zero_total(self):
        """Test progress bar with zero total."""
        result = Formatters.format_progress(0, 0)
        assert "100%" in result
    
    def test_format_number(self):
        """Test number formatting."""
        assert Formatters.format_number(1000) == "1,000"
        assert Formatters.format_number(1234567) == "1,234,567"
    
    def test_format_percentage(self):
        """Test percentage formatting."""
        assert Formatters.format_percentage(95.5) == "95.5%"
        assert Formatters.format_percentage(100, decimals=0) == "100%"
