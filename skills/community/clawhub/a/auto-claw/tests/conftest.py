"""
Auto-Claw Test Suite — pytest configuration and shared fixtures
"""
import os
import sys
import json
import tempfile
from pathlib import Path

# Ensure src/ is on path
SRC = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(SRC))

import pytest


@pytest.fixture
def temp_web_root(tmp_path):
    """Create a fake WordPress web root for testing."""
    wp_root = tmp_path / "wordpress"
    wp_root.mkdir()
    (wp_root / "wp-config.php").write_text("<?php // WP config")
    (wp_root / "wp-content").mkdir()
    (wp_root / "wp-content" / "themes").mkdir()
    (wp_root / "wp-content" / "plugins").mkdir()
    (wp_root / "wp-content" / "uploads").mkdir()
    return wp_root


@pytest.fixture
def sample_html():
    """Minimal HTML page for testing scanners."""
    return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Test Page</title>
    <meta name="description" content="">
    <link rel="canonical" href="https://example.com/test">
</head>
<body>
    <h1>Test Heading</h1>
    <p>Some content here.</p>
    <img src="test.jpg" alt="">
    <a href="https://example.com/page">Link</a>
</body>
</html>"""


@pytest.fixture
def sample_seo_report():
    """Mock SEO scan result."""
    return {
        "url": "https://example.com",
        "score": 44,
        "issues": [
            {"type": "title", "severity": "high", "message": "Title missing"},
            {"type": "description", "severity": "high", "message": "Meta description missing"},
        ],
        "pages": 1,
        "total_issues": 2,
    }


@pytest.fixture
def vault_config():
    """Mock Vault config for testing."""
    return {
        "mode": "disabled",
        "path": tempfile.mkdtemp(),
    }


@pytest.fixture
def audit_log_path(tmp_path):
    """Temp audit log directory."""
    log_dir = tmp_path / "audit"
    log_dir.mkdir()
    return str(log_dir)
