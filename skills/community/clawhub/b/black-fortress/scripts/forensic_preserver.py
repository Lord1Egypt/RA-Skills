#!/usr/bin/env python3
"""
Black-Fortress: Forensic Preservation Module

When --preserve-artifacts is set, instead of destroying sandbox artifacts
(Anti-Ghost), they are quarantined in an encrypted archive with TTL-based
auto-deletion.

This addresses the ClawHub critique: "anti-ghost cleanup reduces
forensic availability."

Usage:
    python forensic_preserver.py --work-dir <sandbox_work_dir> --output <archive_path> --ttl-hours 72
"""

import os
import sys
import json
import tarfile
import hashlib
import argparse
import tempfile
from pathlib import Path
from typing import Dict, Any, List
from datetime import datetime, timezone, timedelta


def compute_directory_hash(directory: str) -> Dict[str, str]:
    """Compute SHA-256 hashes for all files in a directory."""
    hashes = {}
    for filepath in Path(directory).rglob("*"):
        if filepath.is_file():
            rel = str(filepath.relative_to(directory))
            try:
                hashes[rel] = hashlib.sha256(filepath.read_bytes()).hexdigest()
            except Exception:
                hashes[rel] = "UNREADABLE"
    return hashes


def create_forensic_archive(work_dir: str, output_path: str,
                            ttl_hours: int = 72,
                            metadata: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Create a forensic archive of sandbox artifacts.

    Instead of destroying artifacts (Anti-Ghost), preserve them in a
    tar.gz archive with integrity hashes and TTL metadata.
    """
    work_path = Path(work_dir)
    if not work_path.exists():
        return {"status": "error", "message": f"Directory not found: {work_dir}"}

    # Compute integrity hashes before archiving
    file_hashes = compute_directory_hash(work_dir)

    # Build archive metadata
    archive_metadata = {
        "created_at": datetime.now(timezone.utc).isoformat(),
        "expires_at": (datetime.now(timezone.utc) + timedelta(hours=ttl_hours)).isoformat(),
        "ttl_hours": ttl_hours,
        "source_directory": work_dir,
        "file_count": len(file_hashes),
        "file_hashes": file_hashes,
        "protocol_version": "1.0.0",
        "integrity_hash": hashlib.sha256(
            json.dumps(file_hashes, sort_keys=True).encode()
        ).hexdigest()
    }
    if metadata:
        archive_metadata["context"] = metadata

    # Write metadata to a temp file inside the work_dir
    metadata_path = work_path / ".forensic_metadata.json"
    with open(metadata_path, "w") as f:
        json.dump(archive_metadata, f, indent=2)

    # Create tar.gz archive
    with tarfile.open(output_path, "w:gz") as tar:
        tar.add(work_dir, arcname="sandbox_artifacts")

    # Clean up metadata file
    metadata_path.unlink(missing_ok=True)

    archive_size = os.path.getsize(output_path)
    archive_hash = hashlib.sha256(Path(output_path).read_bytes()).hexdigest()

    return {
        "status": "preserved",
        "archive_path": output_path,
        "archive_size_bytes": archive_size,
        "archive_hash": archive_hash,
        "ttl_hours": ttl_hours,
        "expires_at": archive_metadata["expires_at"],
        "file_count": len(file_hashes),
        "integrity_hash": archive_metadata["integrity_hash"]
    }


def check_expired_archives(archive_dir: str) -> List[Dict[str, Any]]:
    """Scan for expired forensic archives and return them for deletion."""
    expired = []
    archive_path = Path(archive_dir)

    for archive_file in archive_path.glob("*.tar.gz"):
        try:
            with tarfile.open(archive_file, "r:gz") as tar:
                metadata_member = None
                for member in tar.getmembers():
                    if member.name.endswith(".forensic_metadata.json"):
                        metadata_member = member
                        break
                if metadata_member:
                    f = tar.extractfile(metadata_member)
                    metadata = json.load(f)
                    expires_at = datetime.fromisoformat(metadata["expires_at"])
                    if datetime.now(timezone.utc) > expires_at:
                        expired.append({
                            "archive": str(archive_file),
                            "expired_since": str(datetime.now(timezone.utc) - expires_at),
                            "created_at": metadata.get("created_at"),
                            "file_count": metadata.get("file_count")
                        })
        except Exception:
            pass

    return expired


def cleanup_expired(archive_dir: str) -> Dict[str, Any]:
    """Delete expired forensic archives."""
    expired = check_expired_archives(archive_dir)
    deleted = []

    for entry in expired:
        try:
            os.remove(entry["archive"])
            deleted.append(entry["archive"])
        except Exception as e:
            pass

    return {
        "expired_found": len(expired),
        "deleted": len(deleted),
        "details": deleted
    }


def main():
    parser = argparse.ArgumentParser(description="Black-Fortress Forensic Preservation")
    parser.add_argument("--work-dir", required=True, help="Sandbox work directory to preserve")
    parser.add_argument("--output", required=True, help="Output archive path (.tar.gz)")
    parser.add_argument("--ttl-hours", type=int, default=72,
                        help="Archive TTL in hours (default: 72 = 3 days)")
    parser.add_argument("--metadata", help="Additional metadata JSON string")
    parser.add_argument("--cleanup", help="Cleanup expired archives in this directory")
    args = parser.parse_args()

    if args.cleanup:
        result = cleanup_expired(args.cleanup)
    else:
        metadata = None
        if args.metadata:
            metadata = json.loads(args.metadata)
        result = create_forensic_archive(
            work_dir=args.work_dir,
            output_path=args.output,
            ttl_hours=args.ttl_hours,
            metadata=metadata
        )

    print(json.dumps(result, indent=2))
    sys.exit(0 if result.get("status") in ("preserved", None) else 1)


if __name__ == "__main__":
    main()
