import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import context_optimizer as co


def test_extract_config_path_parses_last_json_line_with_warnings():
    output = """◇ Doctor warnings\nfoo\n~/.openclaw/openclaw.json\n"""
    path = co._extract_config_path(output)
    assert path == Path("~/.openclaw/openclaw.json").expanduser()


def test_audit_detects_missing_required_settings():
    findings = co.audit({})

    assert "MISSING  memory maxResults not set" in findings
    assert "MISSING  memory minScore not set" in findings
    assert "MISSING  web search maxResults not set" in findings
    assert "MISSING  web fetch maxCharsCap not set" in findings


def test_apply_defaults_balanced_vs_aggressive():
    base = {}

    balanced_updated, _ = co.apply_defaults(base, co.BALANCED_DEFAULTS)
    aggressive_updated, _ = co.apply_defaults(base, co.AGGRESSIVE_DEFAULTS)

    assert co.get_path(balanced_updated, "agents.defaults.memorySearch.query.maxResults") == 3
    assert co.get_path(balanced_updated, "agents.defaults.memorySearch.query.minScore") == 0.75
    assert co.get_path(balanced_updated, "tools.web.search.maxResults") == 3
    assert co.get_path(balanced_updated, "tools.web.fetch.maxCharsCap") == 4000

    assert co.get_path(aggressive_updated, "agents.defaults.memorySearch.query.maxResults") == 2
    assert co.get_path(aggressive_updated, "agents.defaults.memorySearch.query.minScore") == 0.8
    assert co.get_path(aggressive_updated, "tools.web.search.maxResults") == 2
    assert co.get_path(aggressive_updated, "tools.web.fetch.maxCharsCap") == 3000


def test_main_rolls_back_on_invalid_config(monkeypatch, tmp_path):
    config_path = tmp_path / "openclaw.json"
    original = {
        "agents": {"defaults": {"contextPruning": {"mode": "cache-ttl", "ttl": "1h"}}},
        "tools": {"web": {"search": {"enabled": True}, "fetch": {"enabled": True}}},
    }
    config_path.write_text(json.dumps(original, indent=2) + "\n", encoding="utf-8")

    monkeypatch.setattr(co, "discover_config_path", lambda explicit: config_path)
    monkeypatch.setattr(co, "validate_config", lambda: (False, "invalid config"))
    monkeypatch.setattr(sys, "argv", ["context_optimizer.py", "--apply"])

    rc = co.main()

    assert rc == 1
    reloaded = json.loads(config_path.read_text(encoding="utf-8"))
    assert reloaded == original
