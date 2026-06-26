"""
Local disk cache for ghostclaw analysis results.

This cache stores full analysis reports keyed by a fast repository fingerprint.
If the repository state hasn't changed, cached results are returned instantly.
"""

import json
import gzip
import hashlib
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, Optional


class LocalCache:
    """
    Simple file-based cache with TTL and optional compression.

    Cache entries are stored as JSON (or gzipped JSON) files: <cache_dir>/<key>.json[.gz]
    Each entry contains:
    {
        "cached_at": "<ISO timestamp>",
        "report": {<original analysis report dict>}
    }
    """

    def __init__(
        self,
        cache_dir: Optional[Path] = None,
        ttl_days: int = 7,
        compression: bool = True,
    ):
        # Default to project-local cache: <repo>/.ghostclaw/storage/cache/
        if cache_dir is None:
            cache_dir = Path.cwd() / ".ghostclaw" / "storage" / "cache"
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.ttl = timedelta(days=ttl_days)
        self.compression = compression

    def _compute_key(self, fingerprint: str) -> str:
        """Compute SHA-256 cache key from fingerprint string."""
        return hashlib.sha256(fingerprint.encode()).hexdigest()

    def get(self, fingerprint: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve a cached report by fingerprint.

        Tries .json.gz first (compressed), then .json (legacy). Returns None if not found, expired, or corrupted.
        """
        key = self._compute_key(fingerprint)
        candidates = [
            (self.cache_dir / f"{key}.json.gz", True),
            (self.cache_dir / f"{key}.json", False),
        ]

        for path, is_compressed in candidates:
            if not path.exists():
                continue

            try:
                if is_compressed:
                    raw_bytes = gzip.decompress(path.read_bytes())
                    data = json.loads(raw_bytes.decode("utf-8"))
                else:
                    data = json.loads(path.read_text(encoding="utf-8"))

                cached_at = datetime.fromisoformat(data["cached_at"])

                # Check TTL
                if datetime.now() - cached_at > self.ttl:
                    path.unlink(missing_ok=True)
                    return None

                return data["report"]
            except Exception:
                # Corrupted or unreadable; try next candidate
                continue

        return None

    def set(self, fingerprint: str, report: Dict[str, Any]) -> None:
        """Store a report in the cache, overwriting any existing entry."""
        key = self._compute_key(fingerprint)
        # Always store compressed as .json.gz for space savings
        path = self.cache_dir / f"{key}.json.gz"

        data = {"cached_at": datetime.now().isoformat(), "report": report}
        json_bytes = json.dumps(data, indent=2).encode("utf-8")
        if self.compression:
            json_bytes = gzip.compress(json_bytes)
        path.write_bytes(json_bytes)

    def clear(self) -> None:
        """Remove all cache entries."""
        for pattern in ("*.json", "*.json.gz"):
            for p in self.cache_dir.glob(pattern):
                p.unlink(missing_ok=True)

    def info(self) -> Dict[str, Any]:
        """Return cache statistics (entry count, total size)."""
        # Consider both .json and .json.gz files
        entries = list(self.cache_dir.glob("*.json")) + list(
            self.cache_dir.glob("*.json.gz")
        )
        total_size = sum(p.stat().st_size for p in entries if p.is_file())
        return {
            "entries": len(entries),
            "total_size_bytes": total_size,
            "cache_dir": str(self.cache_dir),
        }


class PerFileAnalysisCache:
    """
    Caches analysis results on a per-file basis using content hashing.
    Used to skip re-analyzing unchanged files.
    """

    def __init__(self, cache_dir: Optional[Path] = None):
        if cache_dir is None:
            cache_dir = Path.cwd() / ".ghostclaw" / "storage" / "cache" / "files"
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def _compute_hash(self, file_path: Path) -> str:
        """Compute SHA-256 hash of file content."""
        with open(file_path, "rb") as f:
            return hashlib.sha256(f.read()).hexdigest()

    def get(self, file_path: Path, plugin_name: str) -> Optional[Dict[str, Any]]:
        """Retrieve cached analysis for a file and plugin if content hash matches."""
        try:
            content_hash = self._compute_hash(file_path)
            # Cache key incorporates plugin name to avoid cross-plugin collisions
            key = hashlib.sha256(f"{plugin_name}:{content_hash}".encode()).hexdigest()
            cache_file = self.cache_dir / f"{key}.json"
            if cache_file.exists():
                return json.loads(cache_file.read_text(encoding="utf-8"))
        except Exception:
            pass
        return None

    def set(self, file_path: Path, plugin_name: str, result: Dict[str, Any]) -> None:
        """Cache analysis result for a file, plugin, and content hash."""
        try:
            content_hash = self._compute_hash(file_path)
            key = hashlib.sha256(f"{plugin_name}:{content_hash}".encode()).hexdigest()
            cache_file = self.cache_dir / f"{key}.json"
            cache_file.write_text(json.dumps(result), encoding="utf-8")
        except Exception:
            pass
    def clear(self) -> None:
        """Clear all cached analysis files."""
        for f in self.cache_dir.glob("*.json"):
            try:
                f.unlink()
            except Exception:
                pass



def compute_fingerprint(
    repo_path: Path, git_sha: Optional[str] = None, include_files: bool = False
) -> str:
    """
    Compute a fast fingerprint for a repository.

    Strategy:
    1. If git repo: use 'git:' + HEAD SHA (fast, reliable)
    2. If not git: use 'mtime:' + hash of a metadata summary (file sizes + modification times for relevant code files)
    3. Prefix: 'ghostclaw:v1:' to allow future format evolution

    Args:
        repo_path: Path to repository root
        git_sha: Optional pre-computed git SHA (to avoid recomputing)
        include_files: If True, also incorporate file content hashes (expensive; not used)

    Returns:
        Fingerprint string suitable as cache key.
    """
    # Version prefix for cache invalidation on logic changes
    version_prefix = "ghostclaw:v1:"

    if git_sha:
        return version_prefix + f"git:{git_sha}"

    # Try to get git SHA
    try:
        import subprocess

        result = subprocess.run(
            ["git", "-C", str(repo_path), "rev-parse", "HEAD"],
            capture_output=True,
            text=True,
            check=False,
            timeout=5,
        )
        if result.returncode == 0:
            sha = result.stdout.strip()
            if sha:
                return version_prefix + f"git:{str(sha)}"
    except Exception:
        pass

    # Non-git repo or git command failed: use mtime+size summary of code files
    try:
        from ghostclaw.core.detector import detect_stack

        stack = detect_stack(str(repo_path))
        # Determine likely code extensions based on stack
        ext_map = {
            "node": [".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs"],
            "python": [".py"],
            "go": [".go"],
        }
        extensions = ext_map.get(stack, [".py", ".js", ".ts", ".go", ".rs", ".java"])

        # Collect metadata: path, size, mtime
        file_entries = []
        total_size = 0
        mtime_sum = 0

        for ext in extensions:
            try:
                for f in repo_path.rglob(f"*{ext}"):
                    try:
                        stat = f.stat()
                        rel = str(f.relative_to(repo_path))
                        file_entries.append(
                            {"p": rel, "s": stat.st_size, "m": stat.st_mtime}
                        )
                        total_size += stat.st_size
                        mtime_sum += stat.st_mtime
                    except Exception:
                        continue
            except Exception:
                continue

        # Create deterministic summary
        summary = {
            "stack": stack,
            "count": len(file_entries),
            "total_size": total_size,
            "mtime_sum": mtime_sum,
            "files": sorted(file_entries, key=lambda x: x["p"]),
        }

        summary_str = json.dumps(summary, sort_keys=True, separators=(",", ":"))
        digest = hashlib.sha256(summary_str.encode()).hexdigest()
        return version_prefix + f"mtime:{digest}"

    except Exception:
        # Fallback: use repo path and current time (not ideal, but something)
        fallback = f"{repo_path}:{datetime.now().isoformat()}"
        digest = hashlib.sha256(fallback.encode()).hexdigest()
        return version_prefix + f"static:{digest}"


# Example usage:
if __name__ == "__main__":
    test_repo = Path("/home/ev3lynx/Project/opencode-poweruser")
    fp = compute_fingerprint(test_repo)
    print(f"Fingerprint: {fp}")

    cache = LocalCache()
    cached = cache.get(fp)
    if cached:
        print(f"Cache hit! Vibe: {cached.get('vibe_score')}")
    else:
        print("Cache miss")
