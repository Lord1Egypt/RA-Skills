#!/usr/bin/env python3
"""
Shared utilities for clipper scripts
"""

import os
import json
import subprocess
from urllib.parse import urlparse


def get_vault_path(provided_path=None):
    """Get Obsidian vault path from various sources."""
    if provided_path:
        return provided_path
    
    # Try obsidian-cli default
    try:
        result = subprocess.run(
            ["obsidian-cli", "print-default", "--path-only"],
            capture_output=True, text=True, timeout=10
        )
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    
    # Fallback: read obsidian.json
    config_path = os.path.expanduser("~/Library/Application Support/obsidian/obsidian.json")
    if os.path.exists(config_path):
        try:
            with open(config_path) as f:
                config = json.load(f)
            for vault in config.get("vaults", {}).values():
                if vault.get("open"):
                    return vault.get("path", "")
        except (json.JSONDecodeError, IOError):
            pass
    
    # Last resort: common vault location
    default_vault = os.path.expanduser("~/Code/ObsidianLib")
    if os.path.isdir(default_vault):
        return default_vault
    
    return ""


def slugify(text, max_length=50):
    """Convert text to URL-friendly slug."""
    import re
    if not text:
        return "untitled"
    # Keep Chinese, letters, numbers, hyphens
    text = re.sub(r'[^\w\s\u4e00-\u9fff-]', '', text)
    text = re.sub(r'[-\s]+', '-', text).strip('-')
    return text[:max_length] or "untitled"


def git_sync(vault_path, filepath, commit_msg):
    """Pull, add, commit and push changes to git."""
    relative_path = os.path.relpath(filepath, vault_path)
    
    commands = [
        ["git", "pull", "--rebase"],
        ["git", "add", relative_path],
        ["git", "commit", "-m", commit_msg],
        ["git", "push"],
    ]
    
    errors = []
    for cmd in commands:
        try:
            result = subprocess.run(
                cmd, cwd=vault_path,
                capture_output=True, text=True, timeout=30
            )
            # Ignore "nothing to commit" and "no changes" errors
            if result.returncode != 0:
                stderr = result.stderr.strip()
                if "nothing to commit" not in stderr and "no changes" not in stderr:
                    errors.append(f"{cmd[0]}: {stderr}")
        except subprocess.TimeoutExpired:
            errors.append(f"{cmd[0]}: timeout")
        except Exception as e:
            errors.append(f"{cmd[0]}: {str(e)}")
    
    return {"success": len(errors) == 0, "errors": errors if errors else None}


def detect_platform(url):
    """Detect platform from URL."""
    url_lower = url.lower()
    
    if "twitter.com" in url_lower or "x.com" in url_lower:
        return "twitter"
    elif "mp.weixin.qq.com" in url_lower:
        return "wechat"
    elif "xiaohongshu.com" in url_lower or "xhslink.com" in url_lower:
        return "xiaohongshu"
    elif "youtube.com" in url_lower or "youtu.be" in url_lower:
        return "youtube"
    elif "bilibili.com" in url_lower:
        return "bilibili"
    elif "telegram.org" in url_lower or "t.me" in url_lower:
        return "telegram"
    else:
        return "web"


def get_domain(url):
    """Extract domain from URL."""
    parsed = urlparse(url)
    return parsed.netloc.replace('www.', '')
