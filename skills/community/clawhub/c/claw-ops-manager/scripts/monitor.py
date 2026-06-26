#!/usr/bin/env python3
"""
File system monitor - tracks changes to protected paths
"""
import sqlite3
import os
import time
import hashlib
from pathlib import Path
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

DB_PATH = Path.home() / ".openclaw" / "audit.db"

class FileChangeHandler(FileSystemEventHandler):
    """Handle file system events"""

    def __init__(self, protected_paths, operation_id=None):
        self.protected_paths = protected_paths
        self.operation_id = operation_id

    def calculate_hash(self, file_path):
        """Calculate file hash"""
        try:
            sha256 = hashlib.sha256()
            with open(file_path, 'rb') as f:
                for chunk in iter(lambda: f.read(4096), b''):
                    sha256.update(chunk)
            return sha256.hexdigest()
        except:
            return None

    def log_change(self, file_path, event_type):
        """Log a file change to the database"""
        # Check if path is protected
        is_protected = any(
            str(file_path).startswith(protected)
            for protected in self.protected_paths
        )

        if not is_protected:
            return

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        file_hash = self.calculate_hash(file_path)

        cursor.execute("""
            INSERT INTO file_changes (
                operation_id, file_path, operation_type,
                new_hash, timestamp
            ) VALUES (?, ?, ?, ?, ?)
        """, (
            self.operation_id,
            str(file_path),
            event_type,
            file_hash,
            datetime.now().isoformat()
        ))

        conn.commit()
        conn.close()

        print(f"🔒 Protected file changed: {file_path} ({event_type})")

    def on_modified(self, event):
        if not event.is_directory:
            self.log_change(event.src_path, 'modified')

    def on_created(self, event):
        if not event.is_directory:
            self.log_change(event.src_path, 'created')

    def on_deleted(self, event):
        if not event.is_directory:
            self.log_change(event.src_path, 'deleted')

    def on_moved(self, event):
        if not event.is_directory:
            self.log_change(event.src_path, 'moved_from')
            self.log_change(event.dest_path, 'moved_to')

def start_monitor(paths_to_watch, protected_paths=None):
    """Start monitoring file system changes"""
    if protected_paths is None:
        protected_paths = [
            "/etc/ssh",
            "/etc/sudoers",
            "~/.ssh",
            "~/.openclaw"
        ]

    event_handler = FileChangeHandler(protected_paths)
    observer = Observer()

    for path in paths_to_watch:
        expanded_path = Path(path).expanduser()
        if expanded_path.exists():
            observer.schedule(event_handler, str(expanded_path), recursive=True)
            print(f"📁 Monitoring: {expanded_path}")
        else:
            print(f"⚠️  Path not found: {expanded_path}")

    observer.start()
    print(f"🔍 File monitor started")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    # Example: monitor home directory
    import sys

    paths = sys.argv[1:] if len(sys.argv) > 1 else [str(Path.home())]

    print("🔍 Starting file system monitor...")
    start_monitor(paths)
