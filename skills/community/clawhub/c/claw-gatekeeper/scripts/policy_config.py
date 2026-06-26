#!/usr/bin/env python3
"""
Claw-Gatekeeper Policy Configuration Manager
Manages security policies, whitelist, blacklist, and operational modes

Merged from: SafeClaw (policy_manager.py) + Claw-Guardian (policy_config.py)
Features:
- Comprehensive policy management
- Multiple operation modes
- Import/export functionality
- Policy validation
"""

import json
import os
import sys
from pathlib import Path
from typing import List, Dict, Optional, Any, Union
from dataclasses import dataclass, asdict, field
from datetime import datetime


@dataclass
class GuardianPolicy:
    """Security policy configuration with comprehensive settings"""
    # Basic settings
    enabled: bool = True
    version: str = "1.0.0"
    mode: str = "standard"  # standard / strict / loose / emergency
    
    # Risk level controls
    critical_requires_approval: bool = True
    high_requires_approval: bool = True
    medium_requires_approval: bool = False
    low_auto_allow: bool = True
    
    # Whitelists
    whitelist_paths: List[str] = field(default_factory=list)
    whitelist_commands: List[str] = field(default_factory=list)
    whitelist_domains: List[str] = field(default_factory=list)
    whitelist_skills: List[str] = field(default_factory=list)
    
    # Blacklists
    blacklist_paths: List[str] = field(default_factory=list)
    blacklist_commands: List[str] = field(default_factory=list)
    blacklist_domains: List[str] = field(default_factory=list)
    blacklist_skills: List[str] = field(default_factory=list)
    
    # Advanced settings
    batch_threshold: int = 5
    log_all_operations: bool = True
    log_decisions: bool = True
    alert_on_repeated_denial: bool = True
    auto_learn: bool = False
    emergency_stop: bool = False
    check_hidden_files: bool = True
    strict_mode: bool = False
    
    # UI settings
    use_colors: bool = True
    compact_mode: bool = False
    confirmation_timeout: Optional[int] = None  # seconds, None = no timeout
    
    # Auto-decision settings (for non-interactive mode)
    auto_allow_low: bool = True
    auto_allow_medium: bool = False
    auto_allow_high: bool = False


class PolicyConfig:
    """Policy configuration manager with import/export capabilities"""
    
    DEFAULTS = {
        "enabled": True,
        "version": "1.0.0",
        "mode": "standard",
        "critical_requires_approval": True,
        "high_requires_approval": True,
        "medium_requires_approval": False,
        "low_auto_allow": True,
        "whitelist_paths": [
            "~/Downloads",
            "~/Documents",
            "/tmp"
        ],
        "whitelist_commands": [
            "ls",
            "pwd",
            "cat",
            "echo",
            "grep",
            "git status",
            "git log",
            "git diff",
            "git branch"
        ],
        "whitelist_domains": [],
        "whitelist_skills": [],
        "blacklist_paths": [
            "/etc/passwd",
            "/etc/shadow",
            "/etc/sudoers",
            "~/.ssh",
            "~/.gnupg",
            "~/.aws",
            "~/.kube"
        ],
        "blacklist_commands": [
            "rm -rf /",
            "mkfs",
            "dd if=",
            "format",
            "fdisk"
        ],
        "blacklist_domains": [],
        "blacklist_skills": [],
        "batch_threshold": 5,
        "log_all_operations": True,
        "log_decisions": True,
        "alert_on_repeated_denial": True,
        "auto_learn": False,
        "emergency_stop": False,
        "check_hidden_files": True,
        "strict_mode": False,
        "use_colors": True,
        "compact_mode": False,
        "confirmation_timeout": None,
        "auto_allow_low": True,
        "auto_allow_medium": False,
        "auto_allow_high": False
    }
    
    MODE_PRESETS = {
        "standard": {
            "critical_requires_approval": True,
            "high_requires_approval": True,
            "medium_requires_approval": False,
            "low_auto_allow": True,
            "strict_mode": False
        },
        "strict": {
            "critical_requires_approval": True,
            "high_requires_approval": True,
            "medium_requires_approval": True,
            "low_auto_allow": False,
            "strict_mode": True
        },
        "loose": {
            "critical_requires_approval": True,
            "high_requires_approval": False,
            "medium_requires_approval": False,
            "low_auto_allow": True,
            "strict_mode": False
        },
        "emergency": {
            "emergency_stop": True,
            "critical_requires_approval": True,
            "high_requires_approval": True,
            "medium_requires_approval": True,
            "low_auto_allow": False
        }
    }
    
    def __init__(self, config_path: Optional[str] = None):
        self.config_dir = Path.home() / ".claw-gatekeeper"
        self.config_path = Path(config_path) if config_path else self.config_dir / "config.json"
        self.backup_dir = self.config_dir / "backups"
        self.config_dir.mkdir(exist_ok=True)
        self.backup_dir.mkdir(exist_ok=True)
        
        self.policy = self._load_policy()
    
    def _load_policy(self) -> GuardianPolicy:
        """Load policy from file or create default"""
        if self.config_path.exists():
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Validate and merge with defaults
                policy = self._merge_with_defaults(data)
                return GuardianPolicy(**policy)
            except Exception as e:
                print(f"Warning: Could not load config: {e}", file=sys.stderr)
                print("Creating new configuration...", file=sys.stderr)
                return self._create_default()
        else:
            return self._create_default()
    
    def _merge_with_defaults(self, data: Dict) -> Dict:
        """Merge user config with defaults to ensure all fields exist"""
        merged = self.DEFAULTS.copy()
        merged.update(data)
        return merged
    
    def _create_default(self) -> GuardianPolicy:
        """Create default policy and save"""
        policy = GuardianPolicy(**self.DEFAULTS)
        self.save_policy(policy)
        return policy
    
    def save_policy(self, policy: Optional[GuardianPolicy] = None, 
                   backup: bool = True):
        """Save policy to file with optional backup"""
        policy = policy or self.policy
        
        # Create backup if file exists
        if backup and self.config_path.exists():
            self._create_backup()
        
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(asdict(policy), f, indent=2)
    
    def _create_backup(self):
        """Create timestamped backup of current config"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = self.backup_dir / f"config_backup_{timestamp}.json"
        
        try:
            import shutil
            shutil.copy2(self.config_path, backup_path)
            
            # Keep only last 10 backups
            backups = sorted(self.backup_dir.glob("config_backup_*.json"))
            for old_backup in backups[:-10]:
                old_backup.unlink()
        except Exception as e:
            print(f"Warning: Could not create backup: {e}", file=sys.stderr)
    
    def restore_backup(self, backup_file: Optional[str] = None) -> bool:
        """Restore from backup"""
        if backup_file:
            backup_path = Path(backup_file)
        else:
            # Use most recent backup
            backups = sorted(self.backup_dir.glob("config_backup_*.json"))
            if not backups:
                print("No backups found")
                return False
            backup_path = backups[-1]
        
        if not backup_path.exists():
            print(f"Backup not found: {backup_path}")
            return False
        
        try:
            import shutil
            shutil.copy2(backup_path, self.config_path)
            self.policy = self._load_policy()
            print(f"Restored from backup: {backup_path}")
            return True
        except Exception as e:
            print(f"Error restoring backup: {e}")
            return False
    
    def list_backups(self) -> List[Path]:
        """List available backups"""
        return sorted(self.backup_dir.glob("config_backup_*.json"))
    
    def is_path_whitelisted(self, path: str) -> bool:
        """Check if path is whitelisted"""
        path = os.path.expanduser(path)
        for whitelist_path in self.policy.whitelist_paths:
            whitelist_path = os.path.expanduser(whitelist_path)
            if path.startswith(whitelist_path) or whitelist_path in path:
                return True
        return False
    
    def is_path_blacklisted(self, path: str) -> bool:
        """Check if path is blacklisted"""
        path = os.path.expanduser(path)
        for blacklist_path in self.policy.blacklist_paths:
            blacklist_path = os.path.expanduser(blacklist_path)
            if path.startswith(blacklist_path) or blacklist_path in path:
                return True
        return False
    
    def is_command_whitelisted(self, command: str) -> bool:
        """Check if command is whitelisted"""
        for whitelist_cmd in self.policy.whitelist_commands:
            if command.strip().startswith(whitelist_cmd):
                return True
        return False
    
    def is_command_blacklisted(self, command: str) -> bool:
        """Check if command is blacklisted"""
        for blacklist_cmd in self.policy.blacklist_commands:
            if blacklist_cmd in command:
                return True
        return False
    
    def is_domain_whitelisted(self, domain: str) -> bool:
        """Check if domain is whitelisted"""
        return domain in self.policy.whitelist_domains
    
    def is_domain_blacklisted(self, domain: str) -> bool:
        """Check if domain is blacklisted"""
        return domain in self.policy.blacklist_domains
    
    def is_skill_whitelisted(self, skill_name: str) -> bool:
        """Check if skill is whitelisted"""
        return skill_name in self.policy.whitelist_skills
    
    def is_skill_blacklisted(self, skill_name: str) -> bool:
        """Check if skill is blacklisted"""
        return skill_name in self.policy.blacklist_skills
    
    def add_to_whitelist(self, category: str, item: str) -> bool:
        """Add item to whitelist"""
        attr = f"whitelist_{category}"
        if hasattr(self.policy, attr):
            current = getattr(self.policy, attr)
            if item not in current:
                current.append(item)
                self.save_policy()
                return True
        return False
    
    def add_to_blacklist(self, category: str, item: str) -> bool:
        """Add item to blacklist"""
        attr = f"blacklist_{category}"
        if hasattr(self.policy, attr):
            current = getattr(self.policy, attr)
            if item not in current:
                current.append(item)
                self.save_policy()
                return True
        return False
    
    def remove_from_whitelist(self, category: str, item: str) -> bool:
        """Remove item from whitelist"""
        attr = f"whitelist_{category}"
        if hasattr(self.policy, attr):
            current = getattr(self.policy, attr)
            if item in current:
                current.remove(item)
                self.save_policy()
                return True
        return False
    
    def remove_from_blacklist(self, category: str, item: str) -> bool:
        """Remove item from blacklist"""
        attr = f"blacklist_{category}"
        if hasattr(self.policy, attr):
            current = getattr(self.policy, attr)
            if item in current:
                current.remove(item)
                self.save_policy()
                return True
        return False
    
    def update_setting(self, key: str, value: Any) -> bool:
        """Update a setting value"""
        if hasattr(self.policy, key):
            # Type conversion
            current_value = getattr(self.policy, key)
            if isinstance(current_value, bool):
                if isinstance(value, str):
                    value = value.lower() in ['true', 'yes', '1', 'on']
                else:
                    value = bool(value)
            elif isinstance(current_value, int):
                value = int(value)
            elif isinstance(current_value, list) and isinstance(value, str):
                value = [v.strip() for v in value.split(",")]
            
            setattr(self.policy, key, value)
            self.save_policy()
            return True
        return False
    
    def set_mode(self, mode: str) -> bool:
        """Set operation mode with preset configuration"""
        mode = mode.lower()
        if mode not in self.MODE_PRESETS:
            return False
        
        preset = self.MODE_PRESETS[mode]
        self.policy.mode = mode
        
        for key, value in preset.items():
            setattr(self.policy, key, value)
        
        self.save_policy()
        return True
    
    def get_summary(self) -> Dict[str, Any]:
        """Get policy summary for display"""
        return {
            "enabled": self.policy.enabled,
            "version": self.policy.version,
            "mode": self.policy.mode,
            "emergency_stop": self.policy.emergency_stop,
            "approval_rules": {
                "critical": self.policy.critical_requires_approval,
                "high": self.policy.high_requires_approval,
                "medium": self.policy.medium_requires_approval,
                "low": not self.policy.low_auto_allow
            },
            "whitelist_counts": {
                "paths": len(self.policy.whitelist_paths),
                "commands": len(self.policy.whitelist_commands),
                "domains": len(self.policy.whitelist_domains),
                "skills": len(self.policy.whitelist_skills)
            },
            "blacklist_counts": {
                "paths": len(self.policy.blacklist_paths),
                "commands": len(self.policy.blacklist_commands),
                "domains": len(self.policy.blacklist_domains),
                "skills": len(self.policy.blacklist_skills)
            },
            "settings": {
                "batch_threshold": self.policy.batch_threshold,
                "log_all_operations": self.policy.log_all_operations,
                "auto_learn": self.policy.auto_learn,
                "strict_mode": self.policy.strict_mode
            },
            "config_path": str(self.config_path),
            "backups_available": len(self.list_backups())
        }
    
    def export_policy(self, output_path: str, include_sensitive: bool = False):
        """Export policy to file"""
        export_data = asdict(self.policy)
        
        if not include_sensitive:
            # Remove potentially sensitive blacklist entries
            export_data.pop('blacklist_paths', None)
            export_data.pop('blacklist_commands', None)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2)
        
        print(f"Policy exported to: {output_path}")
    
    def import_policy(self, input_path: str, merge: bool = False) -> bool:
        """Import policy from file"""
        try:
            with open(input_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if merge:
                # Merge with existing
                current = asdict(self.policy)
                current.update(data)
                self.policy = GuardianPolicy(**current)
            else:
                # Replace entirely
                self.policy = GuardianPolicy(**data)
            
            self.save_policy()
            print(f"Policy imported from: {input_path}")
            return True
        except Exception as e:
            print(f"Error importing policy: {e}")
            return False
    
    def reset_to_defaults(self, confirm: bool = False):
        """Reset to default configuration"""
        if not confirm:
            print("Warning: This will reset all settings to defaults.")
            print("Use reset_to_defaults(confirm=True) to proceed.")
            return
        
        self.policy = GuardianPolicy(**self.DEFAULTS)
        self.save_policy()
        print("Configuration reset to defaults")
    
    def validate_policy(self) -> List[str]:
        """Validate policy configuration and return warnings"""
        warnings = []
        
        # Check for overly permissive settings
        if not self.policy.critical_requires_approval:
            warnings.append("CRITICAL risks don't require approval - security risk!")
        
        if not self.policy.high_requires_approval:
            warnings.append("HIGH risks don't require approval")
        
        if self.policy.mode == "loose" and not self.policy.high_requires_approval:
            warnings.append("Loose mode with HIGH auto-allow is not recommended for production")
        
        # Check for empty critical lists
        if len(self.policy.blacklist_paths) < 3:
            warnings.append("Blacklist paths is minimal - consider adding more sensitive paths")
        
        return warnings


def main():
    """Command-line interface"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Claw-Guardian Policy Configuration",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s show
  %(prog)s mode strict
  %(prog)s set batch_threshold 10
  %(prog)s add whitelist paths ~/Projects
  %(prog)s export my_policy.json
        """
    )
    
    parser.add_argument("command", choices=[
        "show", "get", "set", "mode", "add", "remove",
        "export", "import", "reset", "backup", "restore", "validate"
    ])
    parser.add_argument("args", nargs="*", help="Command arguments")
    parser.add_argument("--config", "-c", help="Custom config path")
    parser.add_argument("--merge", "-m", action="store_true", 
                       help="Merge when importing")
    parser.add_argument("--include-sensitive", "-s", action="store_true",
                       help="Include sensitive data in export")
    
    args = parser.parse_args()
    
    config = PolicyConfig(config_path=args.config)
    
    if args.command == "show":
        summary = config.get_summary()
        print(json.dumps(summary, indent=2))
    
    elif args.command == "get" and len(args.args) >= 1:
        key = args.args[0]
        if hasattr(config.policy, key):
            value = getattr(config.policy, key)
            print(json.dumps({key: value}, indent=2))
        else:
            print(f"Unknown setting: {key}")
            sys.exit(1)
    
    elif args.command == "set" and len(args.args) >= 2:
        key = args.args[0]
        value = args.args[1]
        
        if config.update_setting(key, value):
            print(f"Updated {key} = {value}")
        else:
            print(f"Failed to update {key}")
            sys.exit(1)
    
    elif args.command == "mode":
        if not args.args:
            print(f"Current mode: {config.policy.mode}")
            print(f"Available modes: standard, strict, loose, emergency")
        else:
            mode = args.args[0]
            if config.set_mode(mode):
                print(f"Mode set to: {mode}")
            else:
                print(f"Invalid mode: {mode}")
                sys.exit(1)
    
    elif args.command == "add" and len(args.args) >= 3:
        list_type = args.args[0]  # whitelist or blacklist
        category = args.args[1]   # paths, commands, domains, skills
        item = args.args[2]
        
        if list_type == "whitelist":
            success = config.add_to_whitelist(category, item)
        else:
            success = config.add_to_blacklist(category, item)
        
        if success:
            print(f"Added '{item}' to {list_type}_{category}")
        else:
            print(f"Failed to add (may already exist)")
            sys.exit(1)
    
    elif args.command == "remove" and len(args.args) >= 3:
        list_type = args.args[0]
        category = args.args[1]
        item = args.args[2]
        
        if list_type == "whitelist":
            success = config.remove_from_whitelist(category, item)
        else:
            success = config.remove_from_blacklist(category, item)
        
        if success:
            print(f"Removed '{item}' from {list_type}_{category}")
        else:
            print(f"Failed to remove (may not exist)")
            sys.exit(1)
    
    elif args.command == "export":
        output_path = args.args[0] if args.args else "guardian_policy.json"
        config.export_policy(output_path, args.include_sensitive)
    
    elif args.command == "import" and len(args.args) >= 1:
        input_path = args.args[0]
        if not config.import_policy(input_path, args.merge):
            sys.exit(1)
    
    elif args.command == "reset":
        print("This will reset all settings to defaults!")
        response = input("Are you sure? Type 'yes' to confirm: ")
        if response.lower() == 'yes':
            config.reset_to_defaults(confirm=True)
        else:
            print("Reset cancelled")
    
    elif args.command == "backup":
        backups = config.list_backups()
        print(f"Available backups ({len(backups)}):")
        for backup in backups[-10:]:  # Show last 10
            print(f"  {backup.name}")
    
    elif args.command == "restore":
        backup_file = args.args[0] if args.args else None
        if not config.restore_backup(backup_file):
            sys.exit(1)
    
    elif args.command == "validate":
        warnings = config.validate_policy()
        if warnings:
            print("Policy validation warnings:")
            for warning in warnings:
                print(f"  ⚠️  {warning}")
        else:
            print("✅ Policy validation passed")
    
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
