#!/usr/bin/env python3
"""Pytest coverage for AgentRelay core protocol guarantees."""

import importlib.util
import json
import sys
from datetime import datetime
from pathlib import Path


MODULE_PATH = Path(__file__).with_name("__init__.py")


def load_agentrelay(tmp_path, monkeypatch):
    """Load the module against an isolated OPENCLAW_DATA_DIR."""
    monkeypatch.setenv("OPENCLAW_DATA_DIR", str(tmp_path))

    module_name = f"agentrelay_test_{datetime.now().strftime('%Y%m%d%H%M%S%f')}"
    spec = importlib.util.spec_from_file_location(module_name, MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def test_send_receive_ack_verify_round_trip(tmp_path, monkeypatch):
    agentrelay = load_agentrelay(tmp_path, monkeypatch)
    event_id = "round_trip_evt"

    sent = agentrelay.AgentRelayTool.send(
        "agent:worker:main",
        "REQ",
        event_id,
        {
            "task": "round_trip",
            "sender_agent": "agent:sender:main",
            "receiver_agent": "agent:worker:main",
        },
    )

    received = agentrelay.AgentRelayTool.receive(f"AgentRelay: {sent['csv_message']}")
    agentrelay.AgentRelayTool.update(event_id, {"status": "completed", "result": "ok"})
    cmp_message = agentrelay.AgentRelayTool.cmp(event_id, received["secret"])
    verified = agentrelay.AgentRelayTool.verify(cmp_message)

    assert received["event_id"] == event_id
    assert verified["status"] == "ok"
    assert verified["verified"] is True
    assert verified["expected_secret"] == sent["secret"]
    assert verified["sender"] == "agent:sender:main"
    assert verified["receiver"] == "agent:worker:main"


def test_verify_uses_registry_after_burn_on_read(tmp_path, monkeypatch):
    agentrelay = load_agentrelay(tmp_path, monkeypatch)
    event_id = "burn_verify_evt"

    sent = agentrelay.AgentRelayTool.send(
        "agent:worker:main",
        "REQ",
        event_id,
        {
            "task": "burn_then_verify",
            "sender_agent": "agent:sender:main",
            "receiver_agent": "agent:worker:main",
            "burn_on_read": True,
        },
    )

    received = agentrelay.AgentRelayTool.receive(f"AgentRelay: {sent['csv_message']}")

    assert agentrelay.get_event_file(event_id).exists() is False

    verified = agentrelay.AgentRelayTool.verify(
        f"CMP,{event_id},,,{received['secret']}"
    )

    assert verified["status"] == "ok"
    assert verified["verified"] is True
    assert verified["file_exists"] is False


def test_verify_returns_mismatch_for_wrong_secret(tmp_path, monkeypatch):
    agentrelay = load_agentrelay(tmp_path, monkeypatch)
    event_id = "mismatch_evt"

    sent = agentrelay.AgentRelayTool.send(
        "agent:worker:main",
        "REQ",
        event_id,
        {
            "task": "wrong_secret",
            "sender_agent": "agent:sender:main",
            "receiver_agent": "agent:worker:main",
        },
    )

    verified = agentrelay.AgentRelayTool.verify(f"CMP,{event_id},,,WRONG1")

    assert verified["status"] == "mismatch"
    assert verified["verified"] is False
    assert verified["expected_secret"] == sent["secret"]
    assert verified["received_secret"] == "WRONG1"


def test_cleanup_removes_expired_file_and_old_registry(tmp_path, monkeypatch):
    agentrelay = load_agentrelay(tmp_path, monkeypatch)
    event_id = "cleanup_evt"

    sent = agentrelay.AgentRelayTool.send(
        "agent:worker:main",
        "REQ",
        event_id,
        {
            "task": "cleanup_test",
            "sender_agent": "agent:sender:main",
            "receiver_agent": "agent:worker:main",
            "ttl_hours": 1,
        },
    )

    file_path = agentrelay.get_event_file(event_id)
    old_time = "2026-03-01T00:00:00"

    with open(file_path, "r", encoding="utf-8") as f:
        file_data = json.load(f)
    file_data["meta"]["created_at"] = old_time
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(file_data, f, ensure_ascii=False, indent=2)

    agentrelay.upsert_registry_event(
        event_id,
        {
            "event_id": event_id,
            "created_at": old_time,
            "updated_at": old_time,
            "ttl_hours": 1,
            "file_path": str(file_path),
            "file_exists": True,
        },
    )
    agentrelay.upsert_registry_event(
        "cleanup_registry_only",
        {
            "event_id": "cleanup_registry_only",
            "created_at": old_time,
            "updated_at": old_time,
            "expired_at": old_time,
            "file_exists": False,
            "ttl_hours": 1,
        },
    )

    result = agentrelay.cleanup_stale_events(
        default_ttl_hours=24,
        registry_ttl_hours=24,
        now=agentrelay.parse_iso_datetime("2026-03-13T00:00:00"),
    )

    assert event_id in result["deleted_files"]
    assert "cleanup_registry_only" in result["deleted_registry"]
    assert file_path.exists() is False
    registry_event = agentrelay.get_registry_event(event_id)
    assert registry_event["status"] == "expired"
    assert registry_event["file_exists"] is False
