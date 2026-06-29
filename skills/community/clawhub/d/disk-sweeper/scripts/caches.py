"""disk-sweeper: Chinese app cache recognition.

Identifies cache directories for popular Chinese applications
and evaluates cleanup safety level.
"""
import os
import glob
from typing import List, Dict, Optional


# Known Chinese application cache patterns
CACHE_PATTERNS = [
    {
        "app": "WeChat (微信)",
        "paths": [
            "~/Library/Containers/com.tencent.xinWeChat/Data/Library/Caches/*",
            "~/Library/Containers/com.tencent.xinWeChat/Data/Library/Application Support/com.tencent.xinWeChat/*",
        ],
        "safety": "CAUTION",
        "description": "WeChat chat history cache, including images, videos, and documents",
    },
    {
        "app": "DingTalk (钉钉)",
        "paths": [
            "~/Library/Containers/com.dingtalk.mac/Data/Library/Caches/*",
            "~/Library/Application Support/com.dingtalk.mac/*",
        ],
        "safety": "CAUTION",
        "description": "DingTalk cache files and attachments",
    },
    {
        "app": "QQ",
        "paths": [
            "~/Library/Containers/com.tencent.qq/Data/Library/Caches/*",
        ],
        "safety": "CAUTION",
        "description": "QQ cache including images and chat files",
    },
    {
        "app": "Baidu Netdisk (百度网盘)",
        "paths": [
            "~/Library/Application Support/com.baidu.BaiduNetdisk-mac/*/Cache/*",
        ],
        "safety": "SAFE",
        "description": "Baidu Netdisk temporary download cache",
    },
    {
        "app": "WPS Office",
        "paths": [
            "~/Library/Containers/com.kingsoft.wpsoffice.mac/Data/Library/Caches/*",
        ],
        "safety": "CAUTION",
        "description": "WPS office cache and temporary files",
    },
    {
        "app": "Netease Music (网易云音乐)",
        "paths": [
            "~/Library/Containers/com.netease.163music/Data/Library/Caches/*",
        ],
        "safety": "SAFE",
        "description": "Music streaming cache (will be re-downloaded)",
    },
    {
        "app": "Xcode",
        "paths": [
            "~/Library/Developer/Xcode/DerivedData/*",
            "~/Library/Developer/Xcode/Archives/*",
            "~/Library/Developer/Xcode/iOS DeviceSupport/*",
            "~/Library/Developer/CoreSimulator/*",
        ],
        "safety": "CLEANABLE",
        "description": "Xcode build artifacts, archvies, and simulator data",
    },
    {
        "app": "Docker",
        "paths": [
            "~/Library/Containers/com.docker.docker/Data/vms/*",
        ],
        "safety": "CLEANABLE",
        "description": "Docker VM disk images and container data",
    },
    {
        "app": "npm/yarn/pnpm",
        "paths": [
            "~/.npm/_cacache/*",
            "~/.yarn/cache/*",
            "~/.pnpm-store/*",
        ],
        "safety": "SAFE",
        "description": "Package manager cache (reconstructable)",
    },
    {
        "app": "Homebrew",
        "paths": [
            "~/Library/Caches/Homebrew/*",
        ],
        "safety": "SAFE",
        "description": "Homebrew download cache",
    },
    {
        "app": "macOS System Caches",
        "paths": [
            "~/Library/Caches/*",
        ],
        "safety": "CLEANABLE",
        "description": "macOS application system caches",
    },
]


def find_cache_dirs() -> List[Dict]:
    """Scan for known cache directories and return their info.

    Returns list of dicts with app name, path, size, safety level, and description.
    """
    results = []
    seen_paths = set()

    for pattern in CACHE_PATTERNS:
        for path_glob in pattern["paths"]:
            expanded = os.path.expanduser(path_glob)
            matches = glob.glob(expanded)
            for match in matches:
                if match in seen_paths:
                    continue
                seen_paths.add(match)

                if not os.path.exists(match):
                    continue

                size = _get_dir_size(match)
                if size < 1024:  # Skip empty or tiny caches
                    continue

                results.append({
                    "app": pattern["app"],
                    "path": match,
                    "size_bytes": size,
                    "size_human": _human_size(size),
                    "safety": pattern["safety"],
                    "description": pattern["description"],
                })

    return sorted(results, key=lambda x: x["size_bytes"], reverse=True)


def _get_dir_size(path: str) -> int:
    """Calculate total size of a directory."""
    total = 0
    try:
        for dirpath, dirnames, filenames in os.walk(path, followlinks=False):
            for f in filenames:
                try:
                    fp = os.path.join(dirpath, f)
                    total += os.path.getsize(fp)
                except (OSError, PermissionError):
                    continue
    except (OSError, PermissionError):
        pass
    return total


def _human_size(size_bytes: int) -> str:
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} PB"


if __name__ == "__main__":
    caches = find_cache_dirs()
    if caches:
        print(f"Found {len(caches)} cache directories:")
        for c in caches[:10]:
            icon = {"SAFE": "🟢", "CLEANABLE": "🟡", "CAUTION": "🟠"}
            print(f"  {icon.get(c['safety'], '⚪')} {c['app']}: {c['size_human']}")
            print(f"    {c['path'][:60]}...")
            print(f"    Safety: {c['safety']} | {c['description']}")
    else:
        print("No cache directories found (expected on minimal test environment)")
        print("Cache scanner ready and operational")
