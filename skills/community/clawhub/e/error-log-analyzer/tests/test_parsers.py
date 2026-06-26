"""
Tests for log parsers
"""
import pytest
from src.parsers import LogParser, LogEntry


def test_parse_nodejs_winston_json():
    """Test parsing Node.js Winston JSON format."""
    parser = LogParser()
    
    log_content = '''{"level":"error","message":"Database connection failed","timestamp":"2026-03-06T10:23:45.123Z"}
{"level":"warn","message":"High memory usage","timestamp":"2026-03-06T10:24:12.456Z"}'''
    
    entries = parser.parse(log_content)
    
    assert len(entries) == 2
    assert entries[0].level == 'ERROR'
    assert entries[0].message == 'Database connection failed'
    assert entries[1].level == 'WARN'


def test_parse_python_logging():
    """Test parsing Python logging format."""
    parser = LogParser()
    
    log_content = '''2026-03-06 14:23:11,456 - django.request - ERROR - Internal Server Error
Traceback (most recent call last):
  File "/app/views.py", line 45, in get_users
    raise ValueError("Test error")
ValueError: Test error'''
    
    entries = parser.parse(log_content)
    
    assert len(entries) == 1
    assert entries[0].level == 'ERROR'
    assert 'Internal Server Error' in entries[0].message
    assert entries[0].stack_trace is not None


def test_parse_go_standard():
    """Test parsing Go standard library format."""
    parser = LogParser()
    
    log_content = '''2026/03/06 10:23:45 ERROR: Failed to connect
2026/03/06 10:24:12 WARN: Cache miss'''
    
    entries = parser.parse(log_content)
    
    assert len(entries) == 2
    assert entries[0].level == 'ERROR'
    assert 'Failed to connect' in entries[0].message


def test_auto_detect_format():
    """Test automatic format detection."""
    parser = LogParser()
    
    # Should detect JSON format
    json_log = '{"level":"error","message":"test"}'
    entries = parser.parse(json_log)
    assert len(entries) == 1
    
    # Should detect Python format
    python_log = '2026-03-06 14:23:11,456 - ERROR - test'
    entries = parser.parse(python_log)
    assert len(entries) == 1


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
