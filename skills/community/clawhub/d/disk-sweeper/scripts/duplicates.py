"""disk-sweeper: Duplicate file detection.

Uses SHA-256 content hashing with a 3-phase approach:
1. Group by file size (quick filter)
2. Hash first 4KB (fast reject)
3. Full file hash (final confirmation)
"""
import os
import hashlib
from typing import List, Dict, Optional, Generator
from collections import defaultdict


CHUNK_SIZE = 65536  # 64KB chunks for streaming hash


def size_grouped(files: List[Dict], min_size: int = 1048576) -> Dict[int, List[Dict]]:
    """Phase 1: Group files by exact file size.

    Only files >= min_size are considered for duplicate detection.
    """
    groups = defaultdict(list)
    for f in files:
        if "error" not in f and f.get("size", 0) >= min_size:
            groups[f["size"]].append(f)
    # Filter out sizes with only 1 file (no possible duplicates)
    return {size: flist for size, flist in groups.items() if len(flist) > 1}


def hash_head(filepath: str, bytes_to_read: int = 4096) -> Optional[str]:
    """Phase 2: Hash first 4KB of a file."""
    try:
        with open(filepath, "rb") as f:
            head = f.read(bytes_to_read)
            return hashlib.sha256(head).hexdigest()
    except (OSError, PermissionError):
        return None


def hash_full(filepath: str) -> Optional[str]:
    """Phase 3: Full file SHA-256 hash (streaming)."""
    try:
        h = hashlib.sha256()
        with open(filepath, "rb") as f:
            while True:
                chunk = f.read(CHUNK_SIZE)
                if not chunk:
                    break
                h.update(chunk)
        return h.hexdigest()
    except (OSError, PermissionError):
        return None


def find_duplicates(
    files: List[Dict],
    min_size: int = 1048576,
    progress_callback=None,
) -> List[Dict]:
    """Find duplicate files among the given file list.

    Returns list of duplicate groups, each with hash, size, file count, and paths.
    """
    # Phase 1: Size grouping
    size_groups = size_grouped(files, min_size)
    total_candidates = sum(len(flist) for flist in size_groups.values())
    if progress_callback:
        progress_callback("phase1", f"Size groups: {len(size_groups)}, candidates: {total_candidates}")

    # Phase 2: Head hash screening
    head_groups = defaultdict(list)
    for size, flist in size_groups.items():
        head_hashes = {}
        for f in flist:
            hh = hash_head(f["path"])
            if hh:
                head_hashes.setdefault(hh, []).append(f)

        # Only keep groups with potential duplicates (same head hash, >1 file)
        for hh, hlist in head_hashes.items():
            if len(hlist) > 1:
                head_groups[hh].extend(hlist)

    if progress_callback:
        progress_callback("phase2", f"After head hash: {len(head_groups)} candidate groups")

    # Phase 3: Full hash confirmation
    duplicates = defaultdict(list)
    for hh, flist in head_groups.items():
        for f in flist:
            full_h = hash_full(f["path"])
            if full_h:
                duplicates[full_h].append(f)

    # Group results
    result = []
    seen_hashes = set()
    for full_h, flist in duplicates.items():
        if full_h in seen_hashes:
            continue
        seen_hashes.add(full_h)
        if len(flist) > 1:
            result.append({
                "hash": full_h,
                "size_human": _human_size(flist[0]["size"]),
                "size": flist[0]["size"],
                "count": len(flist),
                "paths": [f["path"] for f in flist],
            })

    return sorted(result, key=lambda g: g["size"] * g["count"], reverse=True)


def _human_size(size_bytes: int) -> str:
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} PB"


if __name__ == "__main__":
    # Test with a known duplicate (the same file)
    test_files = [
        {"path": __file__, "name": os.path.basename(__file__), "size": os.path.getsize(__file__)},
    ]
    print("Duplicate detection module ready")
    print(f"Full hash of self: {hash_full(__file__)[:16]}...")
    print(f"Head hash of self: {hash_head(__file__)[:16]}...")
