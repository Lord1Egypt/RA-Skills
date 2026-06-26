#!/usr/bin/env python3
"""Test suite for Chronos configuration module."""
import json
import os
import sys
import tempfile
from pathlib import Path

# Add skill to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.config import get_chat_id, get_config, inspect_config


def set_config_path(config_file: Path) -> str | None:
    original = os.environ.get("CHRONOS_CONFIG_PATH")
    os.environ["CHRONOS_CONFIG_PATH"] = str(config_file)
    return original


def restore_config_path(original: str | None) -> None:
    if original is None:
        os.environ.pop("CHRONOS_CONFIG_PATH", None)
    else:
        os.environ["CHRONOS_CONFIG_PATH"] = original


def clear_chat_env() -> None:
    os.environ.pop("CHRONOS_CHAT_ID", None)


def test_default():
    clear_chat_env()

    with tempfile.TemporaryDirectory() as tmpdir:
        original_config_path = set_config_path(Path(tmpdir) / "config.json")
        try:
            info = inspect_config()
            assert info["status"] == "error"
            assert info["source"] is None
            try:
                get_chat_id()
                raise AssertionError("Expected get_chat_id() to raise ValueError")
            except ValueError:
                print("[ok] Missing chat_id now raises a clear error")
        finally:
            restore_config_path(original_config_path)


def test_env_override():
    os.environ["CHRONOS_CHAT_ID"] = "999888777"
    result = get_chat_id()
    assert result == "999888777", f"Expected 999888777, got {result}"
    info = inspect_config()
    assert info["source"] == "env"
    clear_chat_env()
    print("[ok] Environment variable overrides config file")


def test_config_file():
    clear_chat_env()

    with tempfile.TemporaryDirectory() as tmpdir:
        config_file = Path(tmpdir) / "config.json"
        test_chat_id = "777666555"
        with open(config_file, "w", encoding="utf-8") as f:
            json.dump({"chat_id": test_chat_id}, f)

        original_config_path = set_config_path(config_file)
        try:
            result = get_chat_id()
            assert result == test_chat_id, f"Expected {test_chat_id}, got {result}"
            info = inspect_config()
            assert info["source"] == "config"
            print("[ok] Config file is read correctly")
        finally:
            restore_config_path(original_config_path)


def test_partial_config():
    clear_chat_env()

    with tempfile.TemporaryDirectory() as tmpdir:
        config_file = Path(tmpdir) / "config.json"
        with open(config_file, "w", encoding="utf-8") as f:
            json.dump({"other_key": "value"}, f)

        original_config_path = set_config_path(config_file)
        try:
            try:
                get_chat_id()
                raise AssertionError("Expected missing chat_id to raise ValueError")
            except ValueError:
                print("[ok] Missing chat_id in config raises ValueError")
        finally:
            restore_config_path(original_config_path)


def test_invalid_json_config():
    clear_chat_env()

    with tempfile.TemporaryDirectory() as tmpdir:
        config_file = Path(tmpdir) / "config.json"
        config_file.write_text("{not valid json", encoding="utf-8")

        original_config_path = set_config_path(config_file)
        try:
            info = inspect_config()
            assert info["status"] == "error"
            assert "Failed to read chronos config" in (info["error"] or "")
            print("[ok] Invalid JSON is surfaced clearly")
        finally:
            restore_config_path(original_config_path)


def test_whitespace_chat_id_is_rejected():
    clear_chat_env()

    with tempfile.TemporaryDirectory() as tmpdir:
        config_file = Path(tmpdir) / "config.json"
        with open(config_file, "w", encoding="utf-8") as f:
            json.dump({"chat_id": "   "}, f)

        original_config_path = set_config_path(config_file)
        try:
            info = inspect_config()
            assert info["status"] == "error"
            assert not info["file_chat_id_present"]
            print("[ok] Whitespace chat_id is treated as missing")
        finally:
            restore_config_path(original_config_path)


def test_get_config():
    clear_chat_env()

    with tempfile.TemporaryDirectory() as tmpdir:
        config_file = Path(tmpdir) / "config.json"
        test_chat_id = "111222333"
        with open(config_file, "w", encoding="utf-8") as f:
            json.dump({"chat_id": test_chat_id, "custom_key": "custom_value"}, f)

        original_config_path = set_config_path(config_file)
        try:
            config = get_config()
            assert config["chat_id"] == test_chat_id, "Chat ID mismatch"
            assert config["custom_key"] == "custom_value", "Custom key missing"
            assert config["chat_id_source"] == "config"
            assert config["config_path"] == str(config_file)
            print("[ok] get_config returns merged configuration")
        finally:
            restore_config_path(original_config_path)


if __name__ == "__main__":
    print("Running Chronos config tests...\n")
    test_default()
    test_env_override()
    test_config_file()
    test_partial_config()
    test_invalid_json_config()
    test_whitespace_chat_id_is_rejected()
    test_get_config()
    print("\nAll tests passed.")
