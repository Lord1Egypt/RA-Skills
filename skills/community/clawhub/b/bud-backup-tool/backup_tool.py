#!/usr/bin/env python3
"""
Backup Tool - Backup and restore OpenClaw configuration
Backs up: skills, memory, config, workspace files
Restores to a clean installation or recovery scenario
"""

import os
import sys
import json
import shutil
import subprocess
import tarfile
import gzip
from pathlib import Path
from datetime import datetime

TOOL_DIR = Path.home() / ".openclaw" / "backup-tool"
BACKUP_DIR = Path.home() / ".openclaw" / "backups"
CONFIG_FILE = TOOL_DIR / "config.json"
LOG_FILE = TOOL_DIR / "backup.log"

# What to backup
BACKUP_PATTERNS = {
    "skills": Path.home() / ".openclaw" / "skills",
    "workspace": Path.home() / ".openclaw" / "workspace",
    "memory": Path.home() / ".openclaw" / "workspace" / "memory",
    "identity": Path.home() / ".openclaw" / "identity",
    "credentials": Path.home() / ".openclaw" / "credentials",
    "vpn_mesh": Path.home() / ".openclaw" / "vpn-mesh",
    "health_monitor": Path.home() / ".openclaw" / "health-monitor",
}

GITHUB_REPO = "stigg86/openclaw-backup"
BACKUP_BRANCH = "main"

def ensure_dirs():
    os.makedirs(TOOL_DIR, exist_ok=True)
    os.makedirs(BACKUP_DIR, exist_ok=True)
    os.chmod(TOOL_DIR, 0o755)
    os.makedirs(BACKUP_DIR, exist_ok=True)
    os.chmod(BACKUP_DIR, 0o755)

def log(msg):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"[{timestamp}] {msg}")
    ensure_dirs()
    with open(LOG_FILE, 'a') as f:
        f.write(f"[{timestamp}] {msg}\n")

def get_backup_size(path):
    """Get size of directory in human readable format"""
    try:
        result = subprocess.run(
            ['du', '-sh', str(path)],
            capture_output=True, text=True, timeout=30
        )
        return result.stdout.split()[0] if result.returncode == 0 else "0"
    except:
        return "0"

def create_tarball(sources, output_name):
    """Create compressed tarball from source directories"""
    ensure_dirs()
    output_path = BACKUP_DIR / output_name
    
    log(f"Creating backup: {output_name}")
    
    with tarfile.open(output_path, 'w:gz') as tar:
        for name, path in sources.items():
            if path.exists():
                log(f"  Adding {name} ({get_backup_size(path)})")
                tar.add(str(path), arcname=name)
            else:
                log(f"  Skipping {name} (not found)")
    
    size = os.path.getsize(output_path)
    log(f"Backup created: {output_path} ({size / 1024 / 1024:.1f} MB)")
    return output_path

def list_backups():
    """List existing backups"""
    ensure_dirs()
    backups = []
    for f in BACKUP_DIR.glob("openclaw_backup_*.tar.gz"):
        stat = f.stat()
        backups.append({
            'name': f.name,
            'path': str(f),
            'size': f"{stat.st_size / 1024 / 1024:.1f} MB",
            'created': datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M')
        })
    return sorted(backups, key=lambda x: x['created'], reverse=True)

def restore_tarball(backup_path, items=None):
    """Restore from backup tarball"""
    log(f"Restoring from: {backup_path}")
    
    if not Path(backup_path).exists():
        log(f"ERROR: Backup not found: {backup_path}")
        return False
    
    try:
        with tarfile.open(backup_path, 'r:gz') as tar:
            members = tar.getmembers()
            log(f"Found {len(members)} items in backup")
            
            for member in members:
                if items and member.name not in items:
                    continue
                    
                target = Path.home() / ".openclaw" / member.name
                log(f"  Restoring {member.name} -> {target.parent}")
                
                # Extract to parent directory
                tar.extract(member, Path.home() / ".openclaw")
                
        log("Restore complete!")
        return True
    except Exception as e:
        log(f"ERROR: Restore failed: {e}")
        return False

def push_to_github(backup_path, message=None):
    """Push backup to GitHub repo"""
    if message is None:
        message = f"Backup {datetime.now().strftime('%Y-%m-%d %H:%M')}"
    
    work_dir = BACKUP_DIR / "git_push"
    os.makedirs(work_dir, exist_ok=True)
    
    # Clone or update repo
    repo_path = work_dir / "repo"
    if repo_path.exists():
        log("Updating existing backup repo...")
        subprocess.run(['git', 'pull'], cwd=repo_path, capture_output=True)
    else:
        log("Cloning backup repo...")
        result = subprocess.run(
            ['git', 'clone', f'https://github.com/{GITHUB_REPO}.git', str(repo_path)],
            capture_output=True, text=True, timeout=60
        )
        if result.returncode != 0:
            log("ERROR: Could not clone repo. It may not exist yet.")
            log("Create it at: https://github.com/new")
            log(f"  Name: openclaw-backup")
            log(f"  Description: OpenClaw backup repository")
            return False
    
    # Copy backup to repo
    backup_dest = repo_path / "backups" / Path(backup_path).name
    shutil.copy(backup_path, backup_dest)
    
    # Commit and push
    subprocess.run(['git', 'add', 'backups/' + Path(backup_path).name], cwd=repo_path)
    result = subprocess.run(
        ['git', 'commit', '-m', message],
        cwd=repo_path, capture_output=True, text=True
    )
    
    if result.returncode == 0:
        result = subprocess.run(
            ['git', 'push', 'origin', 'main'],
            cwd=repo_path, capture_output=True, text=True, timeout=30
        )
        if result.returncode == 0:
            log(f"Pushed to GitHub: {GITHUB_REPO}")
            return True
    
    log(f"Git push failed: {result.stderr}")
    return False

def run_backup():
    """Run full backup"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M')
    backup_name = f"openclaw_backup_{timestamp}.tar.gz"
    
    log("=" * 50)
    log("Starting OpenClaw backup")
    log("=" * 50)
    
    # Filter to only existing paths
    sources = {k: v for k, v in BACKUP_PATTERNS.items() if v.exists()}
    
    backup_path = create_tarball(sources, backup_name)
    
    log(f"\nBackup summary:")
    for name, path in sources.items():
        log(f"  {name}: {get_backup_size(path)}")
    log(f"  Total: {os.path.getsize(backup_path) / 1024 / 1024:.1f} MB")
    
    return backup_path

def show_status():
    """Show backup status"""
    print("\n📦 OpenClaw Backup Status")
    print("=" * 40)
    
    print("\n🔧 Files to backup:")
    for name, path in BACKUP_PATTERNS.items():
        exists = "✅" if path.exists() else "❌"
        size = get_backup_size(path) if path.exists() else "-"
        print(f"  {exists} {name}: {size}")
    
    print("\n💾 Local backups:")
    backups = list_backups()
    if backups:
        for b in backups[:5]:
            print(f"  {b['created']} - {b['name']} ({b['size']})")
    else:
        print("  No backups yet")
    
    print(f"\n📁 Backup directory: {BACKUP_DIR}")
    print(f"   Total: {sum(f.stat().st_size for f in BACKUP_DIR.glob('*.tar.gz')) / 1024 / 1024:.1f} MB")

if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "status"
    
    if cmd == "backup":
        backup_path = run_backup()
        if len(sys.argv) > 2 and sys.argv[2] == "--push":
            push_to_github(backup_path)
        print(f"\n✅ Backup complete: {backup_path}")
        
    elif cmd == "restore":
        if len(sys.argv) < 3:
            print("Usage: backup-tool restore <backup_file>")
            print("Available backups:")
            for b in list_backups():
                print(f"  {b['name']}")
        else:
            restore_tarball(sys.argv[2])
            
    elif cmd == "list":
        print("\n💾 Available backups:")
        for b in list_backups():
            print(f"  {b['name']} - {b['created']} ({b['size']})")
            
    elif cmd == "push":
        backups = list_backups()
        if backups:
            push_to_github(backups[0]['path'])
        else:
            print("No backups to push. Run 'backup-tool backup' first.")
            
    elif cmd == "status":
        show_status()
        
    else:
        print("Usage: backup-tool [backup|restore|list|push|status]")
        print("  backup    - Create backup")
        print("  restore   - Restore from backup")
        print("  list      - List available backups")
        print("  push      - Push latest backup to GitHub")
        print("  status    - Show backup status")