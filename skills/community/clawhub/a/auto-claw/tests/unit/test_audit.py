"""
Unit tests for src/audit.py — Audit Logger
"""
import sys
import json
import time
import tempfile
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

import audit


class TestAuditLogger:
    """Test audit logging system."""

    def test_init_with_directory(self):
        """AuditLogger initializes with a log directory."""
        tmp = tempfile.mkdtemp()
        logger = audit.AuditLogger(tmp)
        assert logger.log_dir == tmp
        assert str(tmp) in str(logger.log_file)

    def test_log_writes_jsonl_entry(self):
        """log() writes one JSON line per call."""
        tmp = tempfile.mkdtemp()
        logger = audit.AuditLogger(tmp)
        logger.log("test_module", "test_action", "system", details={"key": "value"})
        with open(logger.log_file) as f:
            line = f.readline()
        entry = json.loads(line)
        assert entry["module"] == "test_module"
        assert entry["action"] == "test_action"

    def test_query_returns_entries(self):
        """query() returns all logged entries."""
        tmp = tempfile.mkdtemp()
        logger = audit.AuditLogger(tmp)
        logger.log("mod1", "act1", "system")
        logger.log("mod2", "act2", "user")
        results = logger.query()
        assert len(results) == 2

    def test_log_includes_timestamp(self):
        """log() includes ISO timestamp."""
        tmp = tempfile.mkdtemp()
        logger = audit.AuditLogger(tmp)
        before = time.time()
        logger.log("test", "action", "system")
        after = time.time()
        with open(logger.log_file) as f:
            entry = json.loads(f.readline())
        ts = entry["timestamp"]
        # Parse ISO format
        from datetime import datetime
        dt = datetime.fromisoformat(ts)
        assert before <= dt.timestamp() <= after

    def test_log_file_increments_new_file_each_day(self):
        """A new log file is created each day."""
        tmp = tempfile.mkdtemp()
        logger = audit.AuditLogger(tmp)
        assert "audit_" in str(logger.log_file)
        assert ".jsonl" in str(logger.log_file)

    def test_multiple_logs(self):
        """Multiple log() calls produce multiple lines."""
        tmp = tempfile.mkdtemp()
        logger = audit.AuditLogger(tmp)
        for i in range(5):
            logger.log("mod", f"act{i}", "system")
        results = logger.query()
        assert len(results) == 5
