#!/usr/bin/env python3
"""
Configuration management for obsidian-save-article skill.
Handles path configuration storage and retrieval.
"""

import os
import sys
import json
from datetime import datetime

CONFIG_PATH = os.path.expanduser("~/.obsidian-save-article-config.json")
OBSIDIAN_APP_CONFIG = os.path.expanduser("~/Library/Application Support/obsidian/obsidian.json")

def normalize_path(path):
    """Expand ~ and normalize a filesystem path."""
    expanded = os.path.expanduser(path.strip())
    return os.path.abspath(os.path.normpath(expanded))

def is_obsidian_vault(path):
    """Check whether a directory looks like an Obsidian vault."""
    normalized = normalize_path(path)
    return os.path.isdir(normalized) and os.path.isdir(os.path.join(normalized, ".obsidian"))

def load_obsidian_app_vaults():
    """Read vaults from Obsidian's own app config if available."""
    if not os.path.exists(OBSIDIAN_APP_CONFIG):
        return []

    try:
        with open(OBSIDIAN_APP_CONFIG, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except (json.JSONDecodeError, IOError):
        return []

    vaults = []
    for vault_id, info in (data.get("vaults") or {}).items():
        path = info.get("path")
        if not path:
            continue
        normalized = normalize_path(path)
        if is_obsidian_vault(normalized):
            vaults.append({
                "source": "obsidian-app-config",
                "vault_id": vault_id,
                "name": os.path.basename(normalized.rstrip(os.sep)) or normalized,
                "path": normalized,
                "open": bool(info.get("open")),
                "ts": info.get("ts")
            })
    return vaults

def scan_common_vault_locations():
    """Scan common local folders for Obsidian vaults."""
    search_roots = [
        os.path.expanduser("~/Documents"),
        os.path.expanduser("~/Desktop"),
        os.path.expanduser("~/Library/Mobile Documents"),
    ]

    found = []
    seen = set()

    for root in search_roots:
        if not os.path.isdir(root):
            continue

        for current_root, dirs, _files in os.walk(root):
            normalized_root = normalize_path(current_root)
            depth = normalized_root.count(os.sep) - normalize_path(root).count(os.sep)

            if ".obsidian" in dirs and normalized_root not in seen:
                found.append({
                    "source": "filesystem-scan",
                    "name": os.path.basename(normalized_root.rstrip(os.sep)) or normalized_root,
                    "path": normalized_root
                })
                seen.add(normalized_root)
                dirs[:] = [d for d in dirs if d != ".obsidian"]

            if depth >= 4:
                dirs[:] = []

    return found

def discover_vaults():
    """Discover candidate Obsidian vaults, preferring official app config."""
    candidates = []
    seen = set()

    for item in load_obsidian_app_vaults() + scan_common_vault_locations():
        path = normalize_path(item["path"])
        if path in seen:
            continue
        item["path"] = path
        candidates.append(item)
        seen.add(path)

    return candidates

def load_config():
    """Load configuration from file. Returns None if not configured."""
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return None
    return None

def save_config(config):
    """Save configuration to file."""
    vault_path = normalize_path(config.get("vault_path", ""))
    subfolder = (config.get("subfolder", "") or "").strip().strip("/")

    config["configured"] = True
    config["configured_at"] = datetime.now().isoformat()
    config["vault_path"] = vault_path
    config["subfolder"] = subfolder
    
    # Compute full path
    if subfolder:
        full_path = os.path.join(vault_path, subfolder)
    else:
        full_path = vault_path
    
    config["full_path"] = normalize_path(full_path)
    
    # Ensure directory exists
    os.makedirs(config["full_path"], exist_ok=True)
    
    with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    
    return config

def get_save_path():
    """Get the configured save path. Returns None if not configured."""
    config = load_config()
    if config and config.get("configured"):
        return config.get("full_path")
    return None

def get_vault_path():
    """Get the vault path without subfolder."""
    config = load_config()
    if config and config.get("configured"):
        return config.get("vault_path")
    return None

def is_configured():
    """Check if the skill has been configured."""
    config = load_config()
    return config and config.get("configured", False)

def clear_config():
    """Clear the configuration."""
    if os.path.exists(CONFIG_PATH):
        os.remove(CONFIG_PATH)
    return True

def verify_path_exists(path):
    """Verify that a path exists and is accessible."""
    expanded_path = normalize_path(path)
    return os.path.exists(expanded_path) and os.path.isdir(expanded_path)

if __name__ == '__main__':
    # CLI interface for testing
    if len(sys.argv) < 2:
        print("Usage: python config.py <action> [args]")
        print("Actions:")
        print("  status          - Show current configuration status")
        print("  get-path        - Get the configured save path")
        print("  set <vault> [subfolder] - Set the save path")
        print("  scan            - Discover local Obsidian vaults")
        print("  clear           - Clear configuration")
        sys.exit(1)
    
    action = sys.argv[1]
    
    if action == "status":
        config = load_config()
        if config and config.get("configured"):
            print(f"✅ 已配置")
            print(f"   类型: {config.get('type', 'local')}")
            print(f"   Vault: {config.get('vault_path')}")
            print(f"   子文件夹: {config.get('subfolder', '(无)')}")
            print(f"   完整路径: {config.get('full_path')}")
            print(f"   配置时间: {config.get('configured_at')}")
        else:
            print("❌ 未配置 - 请运行配置流程")
    
    elif action == "get-path":
        path = get_save_path()
        if path:
            print(path)
        else:
            print("")
    
    elif action == "set":
        if len(sys.argv) < 3:
            print("Usage: python config.py set <vault_path> [subfolder]")
            sys.exit(1)
        
        vault_path = sys.argv[2]
        subfolder = sys.argv[3] if len(sys.argv) > 3 else ""

        normalized_vault_path = normalize_path(vault_path)
        if not verify_path_exists(normalized_vault_path):
            print("❌ Vault 路径不存在或不可访问")
            print(f"   输入路径: {vault_path}")
            print(f"   解析路径: {normalized_vault_path}")
            sys.exit(2)
        
        # Determine type based on path
        config_type = "icloud" if "iCloud" in normalized_vault_path or "Mobile Documents" in normalized_vault_path else "local"
        
        config = {
            "type": config_type,
            "vault_path": normalized_vault_path,
            "subfolder": subfolder
        }
        
        saved = save_config(config)
        print(f"✅ 配置已保存")
        print(f"   完整路径: {saved.get('full_path')}")

    elif action == "scan":
        print(json.dumps(discover_vaults(), indent=2, ensure_ascii=False))
    
    elif action == "clear":
        clear_config()
        print("✅ 配置已清除")
    
    else:
        print(f"Unknown action: {action}")
        sys.exit(1)
