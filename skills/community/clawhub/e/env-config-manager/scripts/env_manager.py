#!/usr/bin/env python3
"""
Env Config Manager - Core Implementation
"""
import os
import json
import re
from pathlib import Path
from typing import Dict, Optional, Any, List
from dotenv import load_dotenv, set_key, dotenv_values
import yaml


def load_env(path: str = ".env") -> Dict[str, Optional[str]]:
    """Load environment variables from a .env file."""
    if not os.path.exists(path):
        return {}
    return dotenv_values(path)


def save_env(data: Dict[str, str], path: str = ".env") -> None:
    """Save environment variables to a .env file."""
    with open(path, "w") as f:
        for key, value in data.items():
            if value is not None:
                f.write(f"{key}={value}\n")


def switch_env(env_name: str, base_path: str = ".") -> Dict[str, Optional[str]]:
    """Switch to a named environment file (.env.{name})."""
    env_file = os.path.join(base_path, f".env.{env_name}")
    if not os.path.exists(env_file):
        raise FileNotFoundError(f"Environment file not found: {env_file}")
    load_dotenv(env_file, override=True)
    return load_env(env_file)


def get_var(key: str, default: Any = None) -> Any:
    """Get an environment variable with optional default."""
    return os.getenv(key, default)


def set_var(key: str, value: str, path: str = ".env") -> None:
    """Set an environment variable in a .env file."""
    set_key(path, key, value)


def validate_schema(env: Dict[str, Any], schema: Dict[str, Any]) -> List[str]:
    """Validate environment variables against a schema."""
    errors = []
    for key, rules in schema.items():
        value = env.get(key)
        if rules.get("required") and (value is None or value == ""):
            errors.append(f"Missing required variable: {key}")
            continue
        if value is None:
            continue
        var_type = rules.get("type")
        if var_type == "int":
            try:
                int(value)
            except ValueError:
                errors.append(f"{key} must be an integer, got: {value}")
        elif var_type == "bool":
            if value.lower() not in ("true", "false", "1", "0", "yes", "no"):
                errors.append(f"{key} must be a boolean, got: {value}")
        elif var_type == "url":
            if not re.match(r"^https?://", str(value)):
                errors.append(f"{key} must be a valid URL, got: {value}")
        min_val = rules.get("min")
        max_val = rules.get("max")
        if var_type == "int" and min_val is not None:
            try:
                if int(value) < min_val:
                    errors.append(f"{key} must be >= {min_val}")
            except ValueError:
                pass
        if var_type == "int" and max_val is not None:
            try:
                if int(value) > max_val:
                    errors.append(f"{key} must be <= {max_val}")
            except ValueError:
                pass
    return errors


def diff_env(env1: Dict[str, Any], env2: Dict[str, Any]) -> Dict[str, Any]:
    """Compare two environment dictionaries and return differences."""
    all_keys = set(env1.keys()) | set(env2.keys())
    diff = {}
    for key in sorted(all_keys):
        v1 = env1.get(key)
        v2 = env2.get(key)
        if v1 != v2:
            diff[key] = {"old": v1, "new": v2}
    return diff


if __name__ == "__main__":
    import sys
    args = sys.argv[1:]
    if not args:
        print("Usage: env_manager.py <command> [args...]")
        print("Commands: load, switch, get, set, validate, diff")
        sys.exit(1)
    cmd = args[0]
    if cmd == "load":
        path = args[1] if len(args) > 1 else ".env"
        env = load_env(path)
        for k, v in env.items():
            print(f"{k}={v}")
    elif cmd == "switch":
        env_name = args[1] if len(args) > 1 else "development"
        env = switch_env(env_name)
        print(f"Switched to {env_name}")
        for k, v in env.items():
            print(f"{k}={v}")
    elif cmd == "get":
        key = args[1]
        print(os.getenv(key, "<not set>"))
    elif cmd == "set":
        key, value = args[1], args[2]
        set_var(key, value)
        print(f"Set {key}={value}")
    elif cmd == "validate":
        schema_path = args[1] if len(args) > 1 else "schema.json"
        with open(schema_path) as f:
            schema = json.load(f)
        env = load_env()
        errors = validate_schema(env, schema)
        if errors:
            for e in errors:
                print(f"ERROR: {e}")
            sys.exit(1)
        else:
            print("Validation passed!")
    elif cmd == "diff":
        f1, f2 = args[1], args[2]
        env1 = load_env(f1)
        env2 = load_env(f2)
        diff = diff_env(env1, env2)
        for k, v in diff.items():
            print(f"{k}: {v['old']} -> {v['new']}")
    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)
