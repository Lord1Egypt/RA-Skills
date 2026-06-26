#!/usr/bin/env python3
"""
Rollback and snapshot management
"""
import sqlite3
import json
import subprocess
from pathlib import Path
from datetime import datetime
from typing import List, Dict

DB_PATH = Path.home() / ".openclaw" / "audit.db"

class SnapshotManager:
    def __init__(self, db_path=None):
        self.db_path = db_path or DB_PATH

    def create_snapshot(
        self,
        name: str,
        description: str = "",
        paths: List[str] = None,
        created_by: str = "system"
    ) -> int:
        """Create a snapshot of specified paths"""

        if paths is None:
            paths = [str(Path.home())]

        snapshot_data = {
            "timestamp": datetime.now().isoformat(),
            "paths": paths,
            "files": {}
        }

        # Collect file metadata and hashes
        for path_str in paths:
            path = Path(path_str).expanduser()

            if path.is_file():
                self._capture_file(path, snapshot_data["files"])
            elif path.is_dir():
                for file_path in path.rglob("*"):
                    if file_path.is_file():
                        self._capture_file(file_path, snapshot_data["files"])

        # Save to database
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO snapshots (name, description, snapshot_data, created_by)
            VALUES (?, ?, ?, ?)
        """, (
            name,
            description,
            json.dumps(snapshot_data),
            created_by
        ))

        snapshot_id = cursor.lastrowid
        conn.commit()
        conn.close()

        return snapshot_id

    def _capture_file(self, file_path: Path, files_dict: dict):
        """Capture file metadata"""
        import hashlib

        try:
            stat = file_path.stat()

            # Calculate hash
            sha256 = hashlib.sha256()
            with open(file_path, 'rb') as f:
                for chunk in iter(lambda: f.read(4096), b''):
                    sha256.update(chunk)

            files_dict[str(file_path)] = {
                "size": stat.st_size,
                "modified": stat.st_mtime,
                "hash": sha256.hexdigest(),
                "is_executable": stat.st_mode & 0o111
            }
        except Exception as e:
            # Skip files we can't read
            pass

    def list_snapshots(self) -> List[Dict]:
        """List all snapshots"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM snapshots
            ORDER BY timestamp DESC
        """)

        snapshots = [dict(row) for row in cursor.fetchall()]
        conn.close()

        return snapshots

    def get_snapshot(self, snapshot_id: int) -> Dict:
        """Get snapshot details"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM snapshots WHERE id = ?", (snapshot_id,))
        snapshot = dict(cursor.fetchone())
        conn.close()

        snapshot["snapshot_data"] = json.loads(snapshot["snapshot_data"])

        return snapshot

    def compare_snapshots(self, snapshot_id_1: int, snapshot_id_2: int) -> Dict:
        """Compare two snapshots and return differences"""
        snapshot_1 = self.get_snapshot(snapshot_id_1)
        snapshot_2 = self.get_snapshot(snapshot_id_2)

        files_1 = snapshot_1["snapshot_data"]["files"]
        files_2 = snapshot_2["snapshot_data"]["files"]

        added = set(files_2.keys()) - set(files_1.keys())
        removed = set(files_1.keys()) - set(files_2.keys())
        modified = set()

        for path in files_1.keys() & files_2.keys():
            if files_1[path]["hash"] != files_2[path]["hash"]:
                modified.add(path)

        return {
            "added": list(added),
            "removed": list(removed),
            "modified": list(modified)
        }

    def restore_snapshot(
        self,
        snapshot_id: int,
        dry_run: bool = False
    ) -> List[str]:
        """Restore files from a snapshot (requires git or backup)"""

        snapshot = self.get_snapshot(snapshot_id)
        operations = []

        # Note: This is a simplified implementation
        # For production, you'd want to integrate with git, restic, or similar

        if dry_run:
            return [
                f"Would restore {len(snapshot['snapshot_data']['files'])} files",
                f"From snapshot: {snapshot['name']}"
            ]

        # In a real implementation, you would:
        # 1. Check if files have changed
        # 2. Backup current state
        # 3. Restore from backup/git/whatever

        operations.append("Restore functionality requires integration with a backup system")
        operations.append("Consider using git, restic, or rsync for actual file restoration")

        return operations

    def rollback_operation(self, operation_id: int) -> bool:
        """Rollback a specific operation"""

        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        # Get operation details
        cursor.execute("SELECT * FROM operations WHERE id = ?", (operation_id,))
        operation = dict(cursor.fetchone())

        # Get file changes
        cursor.execute("""
            SELECT * FROM file_changes
            WHERE operation_id = ?
        """, (operation_id,))

        file_changes = [dict(row) for row in cursor.fetchall()]
        conn.close()

        # Log rollback attempt
        print(f"🔄 Rolling back operation {operation_id}: {operation['tool_name']} - {operation['action']}")

        for change in file_changes:
            print(f"  📄 {change['file_path']} ({change['operation_type']})")

            # In a real implementation, you would:
            # - For write/edit: restore from backup or old hash
            # - For delete: restore from backup
            # - For create: delete the file

        print("⚠️  Rollback requires integration with a backup system (git, restic, etc.)")
        return False

    def auto_snapshot(self) -> int:
        """Create an automatic scheduled snapshot"""
        name = f"auto-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        description = "Automatic scheduled snapshot"

        return self.create_snapshot(
            name=name,
            description=description,
            paths=[
                str(Path.home() / ".openclaw"),
                str(Path.home() / ".ssh"),
                "/etc/ssh/sshd_config"
            ]
        )

if __name__ == "__main__":
    import sys

    manager = SnapshotManager()

    if len(sys.argv) < 2:
        print("Usage:")
        print("  python rollback.py create <name> [description]")
        print("  python rollback.py list")
        print("  python rollback.py show <snapshot_id>")
        print("  python rollback.py compare <id1> <id2>")
        print("  python rollback.py restore <snapshot_id> [--dry-run]")
        print("  python rollback.py rollback <operation_id>")
        sys.exit(1)

    command = sys.argv[1]

    if command == "create":
        name = sys.argv[2]
        description = sys.argv[3] if len(sys.argv) > 3 else ""

        snapshot_id = manager.create_snapshot(name, description)
        print(f"✅ Snapshot created with ID: {snapshot_id}")

    elif command == "list":
        snapshots = manager.list_snapshots()

        print(f"\n📸 Snapshots ({len(snapshots)}):")
        for snap in snapshots:
            print(f"  [{snap['id']}] {snap['name']}")
            print(f"      {snap['description']}")
            print(f"      Created: {snap['timestamp']}")

    elif command == "show":
        snapshot_id = int(sys.argv[2])
        snapshot = manager.get_snapshot(snapshot_id)

        print(f"\n📸 Snapshot: {snapshot['name']}")
        print(f"   Description: {snapshot['description']}")
        print(f"   Created: {snapshot['timestamp']}")
        print(f"   Files: {len(snapshot['snapshot_data']['files'])}")

    elif command == "compare":
        id1 = int(sys.argv[2])
        id2 = int(sys.argv[3])

        diff = manager.compare_snapshots(id1, id2)

        print(f"\n📊 Comparison:")
        print(f"   Added: {len(diff['added'])} files")
        print(f"   Removed: {len(diff['removed'])} files")
        print(f"   Modified: {len(diff['modified'])} files")

    elif command == "restore":
        snapshot_id = int(sys.argv[2])
        dry_run = "--dry-run" in sys.argv

        result = manager.restore_snapshot(snapshot_id, dry_run=dry_run)

        for line in result:
            print(line)

    elif command == "rollback":
        operation_id = int(sys.argv[2])
        manager.rollback_operation(operation_id)
