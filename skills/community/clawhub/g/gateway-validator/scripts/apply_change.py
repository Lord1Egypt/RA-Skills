#!/usr/bin/env python3
"""
Apply validated configuration to the production gateway.
Backs up current config before applying changes.
"""

import sys
import os
import shutil
from pathlib import Path
from datetime import datetime
from typing import Optional


def find_config_file() -> Optional[Path]:
    """Find OpenClaw config file."""
    paths = [
        Path.home() / '.openclaw' / 'config.yaml',
        Path.home() / '.openclaw' / 'config.yml',
    ]
    for path in paths:
        if path.exists():
            return path
    return None


def backup_config(config_path: Path) -> Path:
    """Create a backup of current config."""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_path = config_path.parent / f"config.yaml.backup.{timestamp}"
    shutil.copy2(config_path, backup_path)
    return backup_path


def apply_config(source_path: Path, target_path: Path) -> bool:
    """Copy validated config to production location."""
    try:
        shutil.copy2(source_path, target_path)
        return True
    except Exception as e:
        print(f"❌ Failed to apply config: {e}")
        return False


def restart_gateway() -> bool:
    """Attempt to restart the gateway to apply changes."""
    import subprocess
    
    try:
        # Try to restart via openclaw command
        result = subprocess.run(
            ['openclaw', 'gateway', 'restart'],
            capture_output=True,
            text=True,
            timeout=30
        )
        return result.returncode == 0
    except FileNotFoundError:
        print("⚠️  Could not restart gateway: openclaw command not found")
        print("   You may need to restart manually: openclaw gateway restart")
        return False
    except Exception as e:
        print(f"⚠️  Could not restart gateway: {e}")
        print("   You may need to restart manually: openclaw gateway restart")
        return False


def main():
    """CLI entry point."""
    if len(sys.argv) < 2:
        print("Usage: apply_change.py <validated_config.yaml>")
        sys.exit(1)
    
    source_path = Path(sys.argv[1])
    if not source_path.exists():
        print(f"❌ Source config not found: {source_path}")
        sys.exit(1)
    
    target_path = find_config_file()
    if not target_path:
        print("❌ Could not find production config location")
        sys.exit(1)
    
    print(f"📝 Applying validated config...")
    
    # Backup current config
    backup_path = backup_config(target_path)
    print(f"   💾 Backup created: {backup_path.name}")
    
    # Apply new config
    if apply_config(source_path, target_path):
        print(f"   ✅ Config applied to {target_path}")
    else:
        print(f"   ❌ Failed to apply config")
        sys.exit(1)
    
    # Restart gateway
    print("   🔄 Restarting gateway...")
    if restart_gateway():
        print("   ✅ Gateway restarted successfully")
    else:
        print("   ⚠️  Gateway restart may have failed")
    
    print("\n✅ Configuration change complete!")
    print(f"   Backup: {backup_path}")


if __name__ == "__main__":
    main()
