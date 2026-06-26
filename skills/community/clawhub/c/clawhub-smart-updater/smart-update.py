#!/usr/bin/env python3
"""
ClawHub Smart Updater - Intelligent skill updater with merge conflict detection.

Features:
- Detects local modifications
- Preserves local changes
- Creates automatic backups
- Generates diff files for conflicts
- Provides merge recommendations
"""

import os
import sys
import json
import hashlib
import shutil
import subprocess
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional

class SmartUpdater:
    def __init__(self, workspace_dir: str = None):
        self.workspace = workspace_dir or os.path.join(os.path.expanduser("~"), ".openclaw", "workspace")
        self.skills_dir = os.path.join(self.workspace, "skills")
        self.temp_dir = os.path.join(self.workspace, "temp", "smart-updates")
        self.backup_dir = os.path.join(self.skills_dir, ".backups")
        self.config_file = os.path.join(self.skills_dir, "clawhub-smart-updater", "config.json")
        
        # Ensure directories exist
        os.makedirs(self.temp_dir, exist_ok=True)
        os.makedirs(self.backup_dir, exist_ok=True)
        
        # Load configuration
        self.config = self.load_config()
        
    def load_config(self) -> dict:
        """Load configuration from config.json."""
        default_config = {
            "backup": {
                "enabled": True,
                "retention_days": 7,
                "directory": "skills/.backups"
            },
            "conflict": {
                "auto_backup": True,
                "generate_diff": True,
                "require_manual_review": True
            },
            "notification": {
                "enabled": True,
                "channel": "whatsapp",
                "target": "<YOUR_PHONE_NUMBER>",
                "on_conflict_only": False
            },
            "update": {
                "auto_apply_safe": True,
                "auto_apply_conflicts": False,
                "ignore_whitespace": True
            }
        }
        
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as f:
                loaded = json.load(f)
                # Merge with defaults
                for key in default_config:
                    if key not in loaded:
                        loaded[key] = default_config[key]
                return loaded
        
        return default_config
    
    def run_command(self, cmd: str) -> Tuple[bool, str]:
        """Run shell command and return success status and output."""
        try:
            result = subprocess.run(
                cmd,
                shell=True,
                capture_output=True,
                text=True,
                timeout=60
            )
            return result.returncode == 0, result.stdout + result.stderr
        except Exception as e:
            return False, str(e)
    
    def get_installed_skills(self) -> Dict[str, str]:
        """Get list of installed skills with versions from ClawHub."""
        success, output = self.run_command("clawhub list")
        if not success:
            print(f"❌ Failed to get installed skills: {output}")
            return {}
        
        skills = {}
        for line in output.strip().split('\n'):
            if line.strip() and '  ' in line:
                parts = line.split()
                if len(parts) >= 2:
                    slug = parts[0]
                    version = parts[1]
                    skills[slug] = version
        
        return skills
    
    def get_latest_version(self, slug: str) -> Optional[str]:
        """Get latest version of a skill from ClawHub."""
        success, output = self.run_command(f"clawhub inspect {slug}")
        if not success:
            return None
        
        for line in output.strip().split('\n'):
            if line.startswith('Latest:'):
                return line.split(':')[1].strip()
        
        return None
    
    def hash_file(self, filepath: str) -> str:
        """Calculate SHA-256 hash of file."""
        sha256_hash = hashlib.sha256()
        with open(filepath, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    
    def backup_skill(self, slug: str) -> Optional[str]:
        """Create backup of skill directory."""
        if not self.config["backup"]["enabled"]:
            return None
        
        source = os.path.join(self.skills_dir, slug)
        if not os.path.exists(source):
            return None
        
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        backup_name = f"{slug}.backup-{timestamp}"
        backup_path = os.path.join(self.backup_dir, backup_name)
        
        try:
            shutil.copytree(source, backup_path)
            print(f"✓ Backup created: {backup_name}")
            return backup_path
        except Exception as e:
            print(f"❌ Backup failed: {e}")
            return None
    
    def download_new_version(self, slug: str) -> Optional[str]:
        """Download new version of skill to temp directory."""
        temp_slug_dir = os.path.join(self.temp_dir, f"{slug}-new")
        
        if os.path.exists(temp_slug_dir):
            shutil.rmtree(temp_slug_dir)
        os.makedirs(temp_slug_dir)
        
        success, output = self.run_command(
            f"clawhub inspect {slug} --files --output \"{temp_slug_dir}\""
        )
        
        if success and os.path.exists(temp_slug_dir):
            print(f"✓ Downloaded new version to temp")
            return temp_slug_dir
        
        print(f"❌ Download failed: {output}")
        return None
    
    def compare_files(self, old_path: str, new_path: str) -> Dict:
        """Compare two files and return difference info."""
        result = {
            "exists_old": os.path.exists(old_path),
            "exists_new": os.path.exists(new_path),
            "hash_old": None,
            "hash_new": None,
            "identical": False,
            "locally_modified": False
        }
        
        if result["exists_old"]:
            result["hash_old"] = self.hash_file(old_path)
        
        if result["exists_new"]:
            result["hash_new"] = self.hash_file(new_path)
        
        if result["hash_old"] and result["hash_new"]:
            result["identical"] = result["hash_old"] == result["hash_new"]
            result["locally_modified"] = not result["identical"]
        
        return result
    
    def categorize_changes(self, slug: str, old_dir: str, new_dir: str) -> Dict:
        """Analyze changes and categorize as safe or conflict."""
        safe_files = []
        conflict_files = []
        
        # Get all files from new version
        new_files = []
        for root, dirs, files in os.walk(new_dir):
            for file in files:
                rel_path = os.path.relpath(os.path.join(root, file), new_dir)
                new_files.append(rel_path)
        
        for rel_path in new_files:
            old_file = os.path.join(old_dir, rel_path)
            new_file = os.path.join(new_dir, rel_path)
            
            comparison = self.compare_files(old_file, new_file)
            
            if comparison["identical"]:
                continue  # No change
            
            # Categorize based on file type
            if rel_path.endswith(('.md', '.txt', '.json')):
                # Documentation and configs are usually safe
                safe_files.append({
                    "file": rel_path,
                    "type": "documentation",
                    "reason": "Non-code file"
                })
            elif rel_path.endswith('.py'):
                # Code files need review if modified locally
                if comparison["locally_modified"]:
                    conflict_files.append({
                        "file": rel_path,
                        "type": "code",
                        "reason": "Both upstream and local modified this file",
                        "old_hash": comparison["hash_old"],
                        "new_hash": comparison["hash_new"]
                    })
                else:
                    safe_files.append({
                        "file": rel_path,
                        "type": "code",
                        "reason": "Upstream only change"
                    })
            else:
                # Other files
                safe_files.append({
                    "file": rel_path,
                    "type": "other",
                    "reason": "Non-code file"
                })
        
        return {
            "safe": safe_files,
            "conflicts": conflict_files,
            "total_changes": len(safe_files) + len(conflict_files)
        }
    
    def generate_diff(self, slug: str, old_dir: str, new_dir: str, conflicts: List[Dict]):
        """Generate diff files for conflicting files."""
        if not self.config["conflict"]["generate_diff"]:
            return
        
        diff_dir = os.path.join(self.temp_dir, f"{slug}-diff")
        os.makedirs(diff_dir, exist_ok=True)
        
        diff_content = []
        diff_content.append(f"# Diff Report for {slug}\n")
        diff_content.append(f"Generated: {datetime.now().isoformat()}\n")
        diff_content.append("=" * 60 + "\n\n")
        
        for conflict in conflicts:
            file_path = conflict["file"]
            old_file = os.path.join(old_dir, file_path)
            new_file = os.path.join(new_dir, file_path)
            
            diff_content.append(f"## File: {file_path}\n\n")
            diff_content.append(f"**Local hash:** {conflict['old_hash']}\n")
            diff_content.append(f"**Upstream hash:** {conflict['new_hash']}\n\n")
            
            # Try to generate unified diff
            if os.path.exists(old_file) and os.path.exists(new_file):
                try:
                    success, output = self.run_command(
                        f"git diff --no-index \"{old_file}\" \"{new_file}\""
                    )
                    if success and output.strip():
                        diff_content.append("```diff\n")
                        diff_content.append(output)
                        diff_content.append("\n```\n\n")
                except:
                    pass
        
        # Write diff report
        diff_file = os.path.join(diff_dir, "diff.txt")
        with open(diff_file, 'w', encoding='utf-8') as f:
            f.writelines(diff_content)
        
        print(f"✓ Diff generated: {diff_file}")
    
    def generate_report(self, results: Dict) -> str:
        """Generate human-readable update report."""
        report = []
        report.append("## 🔄 ClawHub Smart Update Report")
        report.append(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        report.append("")
        
        # Auto-updated skills
        if results.get("auto_updated"):
            report.append("### ✅ Auto-Updated (Safe Changes)")
            for slug, info in results["auto_updated"].items():
                report.append(f"- **{slug}**: {info['old_version']} → {info['new_version']}")
                if info.get("files"):
                    for f in info["files"][:3]:  # Show first 3 files
                        report.append(f"  - {f['file']} ({f['type']})")
            report.append("")
        
        # Conflicts requiring review
        if results.get("conflicts"):
            report.append("### ⚠️ Requires Manual Review")
            for slug, info in results["conflicts"].items():
                report.append(f"- **{slug}**: {info['old_version']} → {info['new_version']}")
                report.append(f"  - Conflicts: {len(info['conflict_files'])} files")
                for f in info["conflict_files"][:3]:  # Show first 3
                    report.append(f"    - {f['file']}")
                report.append(f"  - Diff: temp/{slug}-diff/diff.txt")
            report.append("")
        
        # Skipped
        if results.get("skipped"):
            report.append("### ⏭️ Skipped (Up to Date)")
            for slug in results["skipped"]:
                report.append(f"- {slug}")
            report.append("")
        
        # Statistics
        report.append("### 📊 Statistics")
        report.append(f"- Skills checked: {results.get('total_checked', 0)}")
        report.append(f"- Auto-updated: {len(results.get('auto_updated', {}))}")
        report.append(f"- Conflicts: {len(results.get('conflicts', {}))}")
        report.append(f"- Up to date: {len(results.get('skipped', []))}")
        
        return "\n".join(report)
    
    def run(self, slug: str = None, dry_run: bool = False, force: bool = False) -> Dict:
        """Run smart update process."""
        results = {
            "auto_updated": {},
            "conflicts": {},
            "skipped": [],
            "errors": [],
            "total_checked": 0
        }
        
        # Get installed skills
        skills = self.get_installed_skills()
        if not skills:
            return results
        
        # Filter to specific slug if provided
        if slug:
            skills = {slug: skills[slug]} if slug in skills else {}
        
        results["total_checked"] = len(skills)
        
        print(f"\n🔍 Checking {len(skills)} skills for updates...\n")
        
        for skill_slug, local_version in skills.items():
            print(f"\n📦 Checking {skill_slug}...")
            
            # Get latest version
            latest_version = self.get_latest_version(skill_slug)
            if not latest_version:
                results["errors"].append(f"{skill_slug}: Failed to get latest version")
                continue
            
            # Check if update needed
            if local_version == latest_version:
                print(f"✓ {skill_slug} already up to date ({local_version})")
                results["skipped"].append(skill_slug)
                continue
            
            print(f"Update available: {local_version} → {latest_version}")
            
            if dry_run:
                print(f"  [DRY RUN] Would update {skill_slug}")
                continue
            
            # Create backup
            backup_path = self.backup_skill(skill_slug)
            
            # Download new version
            new_dir = self.download_new_version(skill_slug)
            if not new_dir:
                results["errors"].append(f"{skill_slug}: Download failed")
                continue
            
            old_dir = os.path.join(self.skills_dir, skill_slug)
            
            # Analyze changes
            changes = self.categorize_changes(skill_slug, old_dir, new_dir)
            
            print(f"  Changes detected: {changes['total_changes']}")
            print(f"  - Safe: {len(changes['safe'])}")
            print(f"  - Conflicts: {len(changes['conflicts'])}")
            
            # Generate diff for conflicts
            if changes["conflicts"]:
                self.generate_diff(skill_slug, old_dir, new_dir, changes["conflicts"])
            
            # Apply updates based on config
            if not changes["conflicts"] or force:
                # Safe to apply
                if self.config["update"]["auto_apply_safe"]:
                    print(f"  Applying {len(changes['safe'])} safe changes...")
                    # Copy safe files
                    for file_info in changes["safe"]:
                        src = os.path.join(new_dir, file_info["file"])
                        dst = os.path.join(old_dir, file_info["file"])
                        os.makedirs(os.path.dirname(dst), exist_ok=True)
                        shutil.copy2(src, dst)
                    
                    results["auto_updated"][skill_slug] = {
                        "old_version": local_version,
                        "new_version": latest_version,
                        "files": changes["safe"]
                    }
                    print(f"✓ {skill_slug} updated successfully")
                else:
                    print(f"  Auto-update disabled, skipping {skill_slug}")
            else:
                # Conflicts detected
                results["conflicts"][skill_slug] = {
                    "old_version": local_version,
                    "new_version": latest_version,
                    "conflict_files": changes["conflicts"],
                    "safe_files": changes["safe"],
                    "backup": backup_path
                }
                print(f"⚠️ {skill_slug} requires manual review")
        
        # Generate report
        report = self.generate_report(results)
        print("\n" + "=" * 60)
        print(report)
        
        # Save report to file
        report_file = os.path.join(self.temp_dir, f"update-report-{datetime.now().strftime('%Y-%m-%d')}.md")
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"\n📄 Report saved to: {report_file}")
        
        return results
    
    def cleanup_old_backups(self, older_than_days: int = None):
        """Clean up backups older than specified days."""
        retention = older_than_days or self.config["backup"]["retention_days"]
        cutoff = datetime.now() - timedelta(days=retention)
        
        cleaned = 0
        for item in os.listdir(self.backup_dir):
            item_path = os.path.join(self.backup_dir, item)
            if os.path.isdir(item_path):
                # Parse date from backup name
                try:
                    if '.backup-' in item:
                        date_str = item.split('.backup-')[1]
                        backup_date = datetime.strptime(date_str, "%Y-%m-%d_%H-%M-%S")
                        
                        if backup_date < cutoff:
                            shutil.rmtree(item_path)
                            print(f"✓ Cleaned old backup: {item}")
                            cleaned += 1
                except Exception as e:
                    print(f"⚠️ Could not parse date for {item}: {e}")
        
        print(f"\n🧹 Cleaned {cleaned} old backups (> {retention} days)")


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="ClawHub Smart Updater")
    parser.add_argument("--slug", help="Update specific skill only")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be updated")
    parser.add_argument("--force", action="store_true", help="Force update (skip conflict detection)")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    parser.add_argument("--cleanup-backups", action="store_true", help="Clean old backups")
    parser.add_argument("--older-than", type=int, help="Days for backup cleanup")
    parser.add_argument("--workspace", help="OpenClaw workspace directory")
    
    args = parser.parse_args()
    
    updater = SmartUpdater(args.workspace)
    
    if args.cleanup_backups:
        updater.cleanup_old_backups(args.older_than)
        return
    
    results = updater.run(
        slug=args.slug,
        dry_run=args.dry_run,
        force=args.force
    )
    
    # Exit with error if conflicts detected
    if results["conflicts"]:
        print("\n⚠️  Conflicts detected! Review temp/*/diff.txt files")
        sys.exit(1)
    
    sys.exit(0)


if __name__ == "__main__":
    main()
