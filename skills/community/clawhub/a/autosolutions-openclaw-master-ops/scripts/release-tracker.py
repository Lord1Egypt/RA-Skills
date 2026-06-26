#!/usr/bin/env python3
"""
OpenClaw Release Tracker

Tracks OpenClaw releases, changelogs, and breaking changes.
Maintains a SQLite database of version history and skill update recommendations.

Usage:
    python3 release-tracker.py sync          # Fetch latest release info
    python3 release-tracker.py history       # Show version history
    python3 release-tracker.py breaking      # Show breaking changes in latest
    python3 release-tracker.py skill-update  # Check if skill needs updates
    python3 release-tracker.py export        # Export to JSON for skill context
"""

import sqlite3
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "release-history.db"

def init_db():
    """Initialize the release tracking database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS releases (
            version TEXT PRIMARY KEY,
            release_date TEXT,
            changelog TEXT,
            is_breaking BOOLEAN DEFAULT FALSE,
            breaking_changes TEXT,
            skill_updates_needed TEXT,
            synced_at TEXT
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS skill_knowledge (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            topic TEXT UNIQUE,
            last_verified_version TEXT,
            last_verified_at TEXT,
            needs_update BOOLEAN DEFAULT FALSE,
            notes TEXT
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS breaking_changes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            version TEXT,
            category TEXT,
            description TEXT,
            migration_action TEXT,
            reported_at TEXT
        )
    """)
    
    conn.commit()
    return conn

def get_openclaw_version():
    """Get current OpenClaw version."""
    try:
        result = subprocess.run(
            ["openclaw", "--version"],
            capture_output=True, text=True, timeout=10
        )
        return result.stdout.strip()
    except Exception as e:
        return f"error: {e}"

def fetch_release_notes(version=None):
    """Fetch release notes from GitHub or local docs."""
    releases = []
    
    # Try to get from openclaw docs
    try:
        docs_path = Path("/home/marius/.npm-global/lib/node_modules/openclaw/docs")
        if docs_path.exists():
            # Check for changelog/release files
            for pattern in ["CHANGELOG.md", "RELEASES.md", "changelog.md"]:
                changelog_file = docs_path / pattern
                if changelog_file.exists():
                    with open(changelog_file) as f:
                        content = f.read()
                        releases.append({
                            "version": version or "local",
                            "changelog": content[:10000],
                            "release_date": datetime.now().isoformat()
                        })
    except Exception as e:
        pass
    
    # Try GitHub API
    try:
        import urllib.request
        url = "https://api.github.com/repos/openclaw/openclaw/releases"
        with urllib.request.urlopen(url, timeout=10) as response:
            github_releases = json.loads(response.read())
            for rel in github_releases[:10]:  # Last 10 releases
                releases.append({
                    "version": rel.get("tag_name", "unknown"),
                    "release_date": rel.get("published_at", ""),
                    "changelog": rel.get("body", "")[:10000],
                    "is_breaking": "breaking" in rel.get("tag_name", "").lower() or 
                                   "major" in rel.get("body", "").lower()
                })
    except Exception as e:
        print(f"Warning: Could not fetch GitHub releases: {e}", file=sys.stderr)
    
    return releases

def detect_breaking_changes(changelog, version):
    """Detect potential breaking changes from changelog."""
    breaking = []
    
    breaking_keywords = [
        ("removed", "feature_removal"),
        ("deprecated", "deprecation"),
        ("breaking", "breaking_change"),
        ("migration", "migration_required"),
        ("changed default", "default_change"),
        ("config schema", "config_change"),
        ("api change", "api_change"),
        ("command removed", "command_removal"),
        ("flag removed", "flag_removal"),
    ]
    
    changelog_lower = changelog.lower()
    for keyword, category in breaking_keywords:
        if keyword in changelog_lower:
            breaking.append({
                "version": version,
                "category": category,
                "description": f"Potential {category} detected: check changelog for '{keyword}'"
            })
    
    return breaking

def sync_releases(conn):
    """Sync latest releases from GitHub."""
    cursor = conn.cursor()
    releases = fetch_release_notes()
    
    for rel in releases:
        version = rel["version"]
        
        # Check if already synced
        cursor.execute("SELECT version FROM releases WHERE version = ?", (version,))
        if cursor.fetchone():
            print(f"  Skipping {version} (already synced)")
            continue
        
        # Detect breaking changes
        breaking = detect_breaking_changes(rel.get("changelog", ""), version)
        is_breaking = len(breaking) > 0
        
        # Insert release
        cursor.execute("""
            INSERT INTO releases 
            (version, release_date, changelog, is_breaking, breaking_changes, synced_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            version,
            rel.get("release_date", ""),
            rel.get("changelog", ""),
            is_breaking,
            json.dumps(breaking),
            datetime.now().isoformat()
        ))
        
        # Insert breaking changes
        for bc in breaking:
            cursor.execute("""
                INSERT INTO breaking_changes 
                (version, category, description, reported_at)
                VALUES (?, ?, ?, ?)
            """, (
                bc["version"],
                bc["category"],
                bc["description"],
                datetime.now().isoformat()
            ))
        
        print(f"  Synced {version}" + (" ⚠️ BREAKING" if is_breaking else ""))
    
    conn.commit()
    print(f"\nSync complete. Total releases: {len(releases)}")

def show_history(conn, limit=10):
    """Show release history."""
    cursor = conn.cursor()
    cursor.execute("""
        SELECT version, release_date, is_breaking, synced_at 
        FROM releases 
        ORDER BY release_date DESC 
        LIMIT ?
    """, (limit,))
    
    rows = cursor.fetchall()
    print(f"\n{'Version':<20} {'Released':<25} {'Breaking':<10} {'Synced'}")
    print("-" * 70)
    for row in rows:
        version, released, breaking, synced = row
        breaking_mark = "⚠️ YES" if breaking else "✓ No"
        print(f"{version:<20} {released[:24] if released else 'Unknown':<25} {breaking_mark:<10} {synced[:19]}")

def show_breaking(conn):
    """Show breaking changes."""
    cursor = conn.cursor()
    cursor.execute("""
        SELECT version, category, description, migration_action, reported_at
        FROM breaking_changes
        ORDER BY reported_at DESC
        LIMIT 20
    """)
    
    rows = cursor.fetchall()
    if not rows:
        print("No breaking changes recorded.")
        return
    
    print(f"\n{'Version':<15} {'Category':<25} {'Description'}")
    print("-" * 80)
    for row in rows:
        version, category, desc, migration, reported = row
        print(f"{version:<15} {category:<25} {desc[:40]}")

def check_skill_updates(conn):
    """Check if skill needs updates based on latest release."""
    current_version = get_openclaw_version()
    cursor = conn.cursor()
    
    # Get latest breaking changes
    cursor.execute("""
        SELECT version, category, description 
        FROM breaking_changes 
        ORDER BY reported_at DESC 
        LIMIT 5
    """)
    
    breaking = cursor.fetchall()
    
    print(f"\nCurrent OpenClaw version: {current_version}")
    print(f"Recent breaking changes: {len(breaking)}")
    
    if breaking:
        print("\n⚠️  Review these for skill updates:")
        for version, category, desc in breaking:
            print(f"  - [{version}] {category}: {desc}")
    else:
        print("✓ No recent breaking changes detected.")
    
    # Check skill knowledge freshness
    cursor.execute("""
        SELECT topic, last_verified_version, needs_update 
        FROM skill_knowledge 
        WHERE needs_update = TRUE OR last_verified_version != ?
    """, (current_version,))
    
    outdated = cursor.fetchall()
    if outdated:
        print(f"\n📝 Skill topics needing updates: {len(outdated)}")
        for topic, verified_ver, needs_update in outdated:
            print(f"  - {topic} (last verified: {verified_ver})")

def export_json(conn):
    """Export release data as JSON for skill context."""
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM releases ORDER BY release_date DESC LIMIT 20")
    releases = cursor.fetchall()
    
    cursor.execute("SELECT * FROM breaking_changes ORDER BY reported_at DESC LIMIT 50")
    breaking = cursor.fetchall()
    
    data = {
        "exported_at": datetime.now().isoformat(),
        "releases": [
            {
                "version": r[0],
                "release_date": r[1],
                "is_breaking": r[3],
                "breaking_changes": json.loads(r[4]) if r[4] else []
            }
            for r in releases
        ],
        "breaking_changes": [
            {
                "version": b[1],
                "category": b[2],
                "description": b[3],
                "migration_action": b[4]
            }
            for b in breaking
        ]
    }
    
    output_path = Path(__file__).parent.parent / "references" / "release-tracker.json"
    with open(output_path, "w") as f:
        json.dump(data, f, indent=2)
    
    print(f"Exported to {output_path}")
    return data

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    conn = init_db()
    command = sys.argv[1]
    
    if command == "sync":
        print("Syncing OpenClaw releases...")
        sync_releases(conn)
    elif command == "history":
        show_history(conn)
    elif command == "breaking":
        show_breaking(conn)
    elif command == "skill-update":
        check_skill_updates(conn)
    elif command == "export":
        export_json(conn)
    elif command == "version":
        print(f"Current OpenClaw: {get_openclaw_version()}")
    else:
        print(f"Unknown command: {command}")
        print(__doc__)
        sys.exit(1)
    
    conn.close()

if __name__ == "__main__":
    main()
