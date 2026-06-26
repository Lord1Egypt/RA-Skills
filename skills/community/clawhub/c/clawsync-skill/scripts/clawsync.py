#!/usr/bin/env python3
"""
ClawSync - OpenClaw Configuration Backup and Sync
Main entry point
"""

import sys
import os

# Ensure Python 3.8+
if sys.version_info < (3, 8):
    print("Error: Python 3.8+ required", file=sys.stderr)
    sys.exit(1)

from pathlib import Path
import argparse
import json
import shutil
import zipfile
from datetime import datetime
from typing import List, Dict, Optional, Tuple
import hashlib

__version__ = "1.0.0"

class ClawSync:
    """Main class for OpenClaw backup and restore"""
    
    def __init__(self):
        self.openclaw_dir = Path.home() / ".openclaw"
        self.backup_dir = Path.home() / "clawsync-backups"
        self.backup_dir.mkdir(exist_ok=True)
        
    def _get_openclaw_path(self) -> Path:
        """Get OpenClaw configuration directory"""
        # Check environment variable
        env_path = os.environ.get("OPENCLAW_HOME")
        if env_path:
            return Path(env_path)
        
        # Default locations
        return Path.home() / ".openclaw"
    
    def _get_backup_items(self, quick: bool = False, include_workspace: bool = False,
                         include_history: bool = False) -> List[Tuple[str, Path]]:
        """Get list of items to backup"""
        items = []
        oc_dir = self._get_openclaw_path()
        
        if not oc_dir.exists():
            return []
        
        # Always include: Skills
        skills_dir = oc_dir / "skills"
        if skills_dir.exists():
            items.append(("skills", skills_dir))
        
        # Always include: Settings
        for config_file in ["config.yaml", "config.json", "settings.json", ".openclawrc"]:
            config_path = oc_dir / config_file
            if config_path.exists():
                items.append((f"settings/{config_file}", config_path))
        
        # Settings directory
        settings_dir = oc_dir / "settings"
        if settings_dir.exists():
            items.append(("settings", settings_dir))
        
        # Include: Memory (unless quick)
        if not quick:
            memory_dir = oc_dir / "memory"
            if memory_dir.exists():
                items.append(("memory", memory_dir))
            
            # Include: Credentials
            creds_dir = oc_dir / "credentials"
            if creds_dir.exists():
                items.append(("credentials", creds_dir))
        
        # Optional: History
        if include_history:
            history_dir = oc_dir / "history"
            if history_dir.exists():
                items.append(("history", history_dir))
        
        # Optional: Workspace
        if include_workspace:
            workspace_dir = oc_dir / "workspace"
            if workspace_dir.exists():
                items.append(("workspace", workspace_dir))
        
        return items
    
    def create_backup(self, output: str = None, encrypt: bool = False,
                     quick: bool = False, include_workspace: bool = False,
                     include_history: bool = False, compress: int = 6) -> Dict:
        """Create a backup of OpenClaw configuration"""
        
        # Determine output path
        if output:
            output_path = Path(output).expanduser().resolve()
        else:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = self.backup_dir / f"openclaw_backup_{timestamp}.zip"
        
        # Ensure output directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Get items to backup
        items = self._get_backup_items(quick, include_workspace, include_history)
        
        if not items:
            return {"error": "No OpenClaw configuration found to backup"}
        
        # Create manifest
        manifest = {
            "version": __version__,
            "created": datetime.now().isoformat(),
            "hostname": os.environ.get("COMPUTERNAME", "unknown"),
            "items": [],
            "quick": quick
        }
        
        try:
            # Create ZIP archive
            with zipfile.ZipFile(output_path, 'w', compression=zipfile.ZIP_DEFLATED,
                               compresslevel=compress) as zf:
                
                # Add each item
                for item_name, item_path in items:
                    if item_path.is_file():
                        arcname = item_name if '/' in item_name else f"{item_name}/{item_path.name}"
                        zf.write(item_path, arcname)
                        manifest["items"].append({
                            "name": item_name,
                            "path": str(item_path.relative_to(self._get_openclaw_path())),
                            "type": "file",
                            "size": item_path.stat().st_size
                        })
                    elif item_path.is_dir():
                        for file_path in item_path.rglob("*"):
                            if file_path.is_file():
                                arcname = f"{item_name}/{file_path.relative_to(item_path)}"
                                zf.write(file_path, arcname)
                        
                        # Count files and size
                        file_count = sum(1 for _ in item_path.rglob("*") if _.is_file())
                        total_size = sum(f.stat().st_size for f in item_path.rglob("*") if f.is_file())
                        
                        manifest["items"].append({
                            "name": item_name,
                            "path": str(item_path.relative_to(self._get_openclaw_path())),
                            "type": "directory",
                            "file_count": file_count,
                            "total_size": total_size
                        })
                
                # Add manifest
                zf.writestr("manifest.json", json.dumps(manifest, indent=2))
                
                # Add README
                readme = f"""OpenClaw Backup
Generated: {manifest['created']}
Version: {manifest['version']}

To restore, run:
  clawsync restore --backup {output_path.name}

Contents:
"""
                for item in manifest["items"]:
                    readme += f"  - {item['name']}\n"
                
                zf.writestr("README.txt", readme)
            
            # TODO: Implement encryption if requested
            if encrypt:
                print("[INFO] Encryption not yet implemented, backup created unencrypted")
            
            return {
                "success": True,
                "backup_path": str(output_path),
                "items_backed_up": len(items),
                "size": output_path.stat().st_size
            }
            
        except Exception as e:
            return {"error": f"Failed to create backup: {str(e)}"}
    
    def list_backups(self, location: str = None) -> List[Dict]:
        """List available backups"""
        if location:
            search_dir = Path(location).expanduser().resolve()
        else:
            search_dir = self.backup_dir
        
        if not search_dir.exists():
            return []
        
        backups = []
        for backup_file in search_dir.glob("openclaw_backup_*.zip"):
            try:
                with zipfile.ZipFile(backup_file, 'r') as zf:
                    manifest_data = zf.read("manifest.json").decode('utf-8')
                    manifest = json.loads(manifest_data)
                    
                    backups.append({
                        "filename": backup_file.name,
                        "path": str(backup_file),
                        "created": manifest.get("created"),
                        "version": manifest.get("version"),
                        "size": backup_file.stat().st_size,
                        "items": len(manifest.get("items", []))
                    })
            except Exception:
                # Skip corrupted backups
                pass
        
        # Sort by date (newest first)
        backups.sort(key=lambda x: x.get("created", ""), reverse=True)
        return backups
    
    def restore_backup(self, backup_path: str, selective: bool = False,
                      overwrite: bool = False, dry_run: bool = False) -> Dict:
        """Restore from backup"""
        backup_file = Path(backup_path).expanduser().resolve()
        
        if not backup_file.exists():
            return {"error": f"Backup file not found: {backup_file}"}
        
        oc_dir = self._get_openclaw_path()
        
        try:
            with zipfile.ZipFile(backup_file, 'r') as zf:
                # Read manifest
                manifest_data = zf.read("manifest.json").decode('utf-8')
                manifest = json.loads(manifest_data)
                
                if dry_run:
                    return {
                        "dry_run": True,
                        "backup_date": manifest.get("created"),
                        "items": manifest.get("items", []),
                        "restore_target": str(oc_dir)
                    }
                
                # Extract all files
                if not oc_dir.exists():
                    oc_dir.mkdir(parents=True)
                
                extracted_count = 0
                for item in zf.namelist():
                    if item in ["manifest.json", "README.txt"]:
                        continue
                    
                    target_path = oc_dir / item
                    
                    # Check for conflicts
                    if target_path.exists() and not overwrite:
                        continue
                    
                    # Extract
                    zf.extract(item, oc_dir.parent)
                    extracted_count += 1
                
                return {
                    "success": True,
                    "restored_items": extracted_count,
                    "backup_date": manifest.get("created"),
                    "target": str(oc_dir)
                }
                
        except Exception as e:
            return {"error": f"Failed to restore backup: {str(e)}"}
    
    def verify_backup(self, backup_path: str) -> Dict:
        """Verify backup integrity"""
        backup_file = Path(backup_path).expanduser().resolve()
        
        if not backup_file.exists():
            return {"error": f"Backup file not found: {backup_file}"}
        
        try:
            with zipfile.ZipFile(backup_file, 'r') as zf:
                # Check manifest exists
                if "manifest.json" not in zf.namelist():
                    return {"valid": False, "error": "Missing manifest.json"}
                
                # Read manifest
                manifest_data = zf.read("manifest.json").decode('utf-8')
                manifest = json.loads(manifest_data)
                
                # Check all listed items exist
                missing = []
                for item in manifest.get("items", []):
                    item_path = item.get("name")
                    # Check if any files from this item exist in backup
                    found = any(name.startswith(item_path) for name in zf.namelist())
                    if not found:
                        missing.append(item_path)
                
                if missing:
                    return {
                        "valid": False,
                        "error": f"Missing items in backup: {missing}"
                    }
                
                return {
                    "valid": True,
                    "backup_date": manifest.get("created"),
                    "version": manifest.get("version"),
                    "items": len(manifest.get("items", []))
                }
                
        except zipfile.BadZipFile:
            return {"valid": False, "error": "Corrupted ZIP file"}
        except Exception as e:
            return {"valid": False, "error": str(e)}

def main():
    parser = argparse.ArgumentParser(
        description="ClawSync - OpenClaw Configuration Backup and Sync",
        prog="clawsync"
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Backup command
    backup_parser = subparsers.add_parser("backup", help="Create backup")
    backup_parser.add_argument("--output", help="Output file path")
    backup_parser.add_argument("--encrypt", action="store_true", help="Encrypt backup")
    backup_parser.add_argument("--quick", action="store_true", help="Quick backup (settings + skills only)")
    backup_parser.add_argument("--include-workspace", action="store_true", help="Include workspace files")
    backup_parser.add_argument("--include-history", action="store_true", help="Include conversation history")
    backup_parser.add_argument("--compress", type=int, default=6, choices=range(1, 10),
                              help="Compression level (1-9)")
    
    # List command
    list_parser = subparsers.add_parser("list", help="List backups")
    list_parser.add_argument("--location", help="Backup directory")
    
    # Restore command
    restore_parser = subparsers.add_parser("restore", help="Restore from backup")
    restore_parser.add_argument("--backup", help="Backup file to restore")
    restore_parser.add_argument("--selective", action="store_true", help="Selective restore")
    restore_parser.add_argument("--overwrite", action="store_true", help="Overwrite existing files")
    restore_parser.add_argument("--dry-run", action="store_true", help="Preview changes")
    
    # Verify command
    verify_parser = subparsers.add_parser("verify", help="Verify backup integrity")
    verify_parser.add_argument("--backup", required=True, help="Backup file to verify")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(0)
    
    sync = ClawSync()
    
    if args.command == "backup":
        result = sync.create_backup(
            output=args.output,
            encrypt=args.encrypt,
            quick=args.quick,
            include_workspace=args.include_workspace,
            include_history=args.include_history,
            compress=args.compress
        )
        
        if "error" in result:
            print(f"[ERROR] {result['error']}", file=sys.stderr)
            sys.exit(1)
        
        print(f"[SUCCESS] Backup created: {result['backup_path']}")
        print(f"  Items: {result['items_backed_up']}")
        print(f"  Size: {result['size'] / 1024:.1f} KB")
    
    elif args.command == "list":
        backups = sync.list_backups(args.location)
        
        if not backups:
            print("No backups found")
            sys.exit(0)
        
        print(f"\nFound {len(backups)} backup(s):\n")
        print(f"{'Date':<20} {'Size':<12} {'Items':<8} {'Filename'}")
        print("-" * 60)
        
        for b in backups:
            date = b.get("created", "unknown")[:19] if b.get("created") else "unknown"
            size = f"{b.get('size', 0) / 1024:.1f} KB"
            print(f"{date:<20} {size:<12} {b.get('items', 0):<8} {b.get('filename')}")
    
    elif args.command == "restore":
        if not args.backup:
            # List available backups and ask
            backups = sync.list_backups()
            if not backups:
                print("[ERROR] No backups found", file=sys.stderr)
                sys.exit(1)
            
            print("Available backups:")
            for i, b in enumerate(backups, 1):
                print(f"  {i}. {b['filename']} ({b.get('created', 'unknown')[:10]})")
            
            print("\nPlease specify backup with --backup")
            sys.exit(0)
        
        result = sync.restore_backup(
            backup_path=args.backup,
            selective=args.selective,
            overwrite=args.overwrite,
            dry_run=args.dry_run
        )
        
        if "error" in result:
            print(f"[ERROR] {result['error']}", file=sys.stderr)
            sys.exit(1)
        
        if result.get("dry_run"):
            print(f"[DRY RUN] Would restore from: {result['backup_date']}")
            print(f"  Target: {result['restore_target']}")
            print(f"  Items: {len(result['items'])}")
        else:
            print(f"[SUCCESS] Restored {result['restored_items']} items")
            print(f"  From backup: {result['backup_date']}")
            print(f"  Target: {result['target']}")
    
    elif args.command == "verify":
        result = sync.verify_backup(args.backup)
        
        if "error" in result:
            print(f"[ERROR] {result['error']}", file=sys.stderr)
            sys.exit(1)
        
        if result.get("valid"):
            print(f"[VALID] Backup is valid")
            print(f"  Created: {result.get('backup_date')}")
            print(f"  Version: {result.get('version')}")
            print(f"  Items: {result.get('items')}")
        else:
            print(f"[INVALID] {result.get('error')}", file=sys.stderr)
            sys.exit(1)

if __name__ == "__main__":
    main()
