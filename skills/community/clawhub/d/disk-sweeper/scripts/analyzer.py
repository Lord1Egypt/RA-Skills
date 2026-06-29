"""disk-sweeper: Space analysis engine.

Aggregates scan results by type, directory, extension, and age.
Generates top-N file lists and summary statistics.
"""
import os
from typing import List, Dict, Optional
from collections import defaultdict


FILE_TYPE_MAP = {
    # Video
    ".mp4": "video", ".mov": "video", ".avi": "video", ".mkv": "video",
    ".flv": "video", ".wmv": "video", ".webm": "video", ".m4v": "video",
    # Image
    ".jpg": "image", ".jpeg": "image", ".png": "image", ".gif": "image",
    ".bmp": "image", ".tiff": "image", ".webp": "image", ".heic": "image",
    ".svg": "image", ".raw": "image",
    # Document
    ".pdf": "document", ".doc": "document", ".docx": "document",
    ".xls": "document", ".xlsx": "document", ".ppt": "document",
    ".pptx": "document", ".txt": "document", ".md": "document",
    ".csv": "document", ".json": "document", ".xml": "document",
    # Archive
    ".zip": "archive", ".tar": "archive", ".gz": "archive",
    ".bz2": "archive", ".7z": "archive", ".rar": "archive",
    ".dmg": "archive", ".iso": "archive",
    # Code
    ".py": "code", ".js": "code", ".ts": "code", ".jsx": "code",
    ".tsx": "code", ".java": "code", ".cpp": "code", ".c": "code",
    ".h": "code", ".go": "code", ".rs": "code", ".rb": "code",
    ".php": "code", ".swift": "code", ".kt": "code",
    # Application
    ".app": "app", ".dmg": "app", ".pkg": "app",
    # Cache
    ".cache": "cache",
    # Audio
    ".mp3": "audio", ".wav": "audio", ".aac": "audio",
    ".flac": "audio", ".m4a": "audio", ".wma": "audio",
    # Other
    ".log": "log", ".tmp": "temp", ".bak": "backup",
}

AGE_BUCKETS = [
    (7, "recent_7d"),
    (30, "recent_30d"),
    (90, "recent_90d"),
    (365, "recent_1y"),
    (float("inf"), "older_1y"),
]


def classify_file_type(ext: str) -> str:
    """Map file extension to a type category."""
    return FILE_TYPE_MAP.get(ext.lower(), "other")


def analyze_scan_results(files: List[Dict], top_n: int = 50) -> Dict:
    """Perform multi-dimension analysis on scanned files."""
    # Filter out errors
    valid_files = [f for f in files if "error" not in f]

    # 1. By type
    by_type = defaultdict(lambda: {"size_bytes": 0, "file_count": 0})
    for f in valid_files:
        ftype = classify_file_type(f.get("ext", ""))
        by_type[ftype]["size_bytes"] += f["size"]
        by_type[ftype]["file_count"] += 1

    # 2. Top largest files
    top_files = sorted(valid_files, key=lambda x: x["size"], reverse=True)[:top_n]

    # 3. By directory (top-level aggregation)
    by_directory = defaultdict(lambda: {"size_bytes": 0, "file_count": 0})
    for f in valid_files:
        dirname = os.path.dirname(f["path"])
        by_directory[dirname]["size_bytes"] += f["size"]
        by_directory[dirname]["file_count"] += 1

    largest_dirs = sorted(by_directory.items(), key=lambda x: x[1]["size_bytes"], reverse=True)[:20]

    # 4. By age
    import time
    now = time.time()
    by_age = defaultdict(lambda: {"size_bytes": 0, "file_count": 0})
    for f in valid_files:
        age_days = (now - f.get("atime", f.get("mtime", now))) / 86400
        for threshold, bucket in AGE_BUCKETS:
            if age_days <= threshold:
                by_age[bucket]["size_bytes"] += f["size"]
                by_age[bucket]["file_count"] += 1
                break

    total_size = sum(f["size"] for f in valid_files)
    total_files = len(valid_files)

    return {
        "total_size_bytes": total_size,
        "total_size_human": _human_size(total_size),
        "total_files": total_files,
        "by_type": [
            {"type": t, "size_bytes": d["size_bytes"],
             "size_human": _human_size(d["size_bytes"]),
             "file_count": d["file_count"],
             "percentage": round(d["size_bytes"] / total_size * 100, 1) if total_size else 0}
            for t, d in sorted(by_type.items(), key=lambda x: x[1]["size_bytes"], reverse=True)
        ],
        "top_files": [
            {"path": f["path"], "name": f["name"],
             "size_human": _human_size(f["size"]),
             "size": f["size"],
             "type": classify_file_type(f.get("ext", ""))}
            for f in top_files
        ],
        "largest_dirs": [
            {"path": d[0], "size_human": _human_size(d[1]["size_bytes"]),
             "file_count": d[1]["file_count"]}
            for d in largest_dirs
        ],
        "by_age": {
            k: {"size_human": _human_size(v["size_bytes"]), "file_count": v["file_count"]}
            for k, v in by_age.items()
        },
    }


def _human_size(size_bytes: int) -> str:
    """Convert bytes to human-readable string."""
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} PB"


if __name__ == "__main__":
    test_files = [
        {"path": "/Users/test/Movies/video.mp4", "name": "video.mp4", "size": 4_200_000_000, "ext": ".mp4", "mtime": 1_700_000_000, "atime": 1_700_000_000},
        {"path": "/Users/test/Downloads/backup.zip", "name": "backup.zip", "size": 2_800_000_000, "ext": ".zip", "mtime": 1_600_000_000, "atime": 1_600_000_000},
        {"path": "/Users/test/Desktop/notes.md", "name": "notes.md", "size": 2_400, "ext": ".md", "mtime": 1_710_000_000, "atime": 1_710_000_000},
        {"path": "/Users/test/Documents/report.pdf", "name": "report.pdf", "size": 500_000_000, "ext": ".pdf", "mtime": 1_700_000_000, "atime": 1_700_000_000},
    ]
    result = analyze_scan_results(test_files)
    print(f"Total: {result['total_size_human']} ({result['total_files']} files)")
    for t in result["by_type"]:
        print(f"  {t['type']}: {t['size_human']} ({t['percentage']}%)")
    for f in result["top_files"][:3]:
        print(f"  TOP: {f['name']} ({f['size_human']})")
