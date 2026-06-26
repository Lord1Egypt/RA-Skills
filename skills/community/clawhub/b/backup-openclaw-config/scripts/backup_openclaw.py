#!/usr/bin/env python3
"""
OpenClaw Configuration Backup Script (Python version)
Usage: python3 backup_openclaw.py [output-directory]
"""

import os
import sys
import shutil
import tarfile
import subprocess
from pathlib import Path
from datetime import datetime

def main():
    # Default backup directory
    default_backup_dir = Path.home() / "backups" / "openclaw"
    backup_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else default_backup_dir
    
    # Create backup directory
    backup_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"openclaw_backup_{timestamp}"
    backup_path = backup_dir / backup_name
    
    print("=== OpenClaw Configuration Backup ===")
    print(f"Backup location: {backup_path}")
    print()
    
    # Create temporary directory
    import tempfile
    temp_dir = Path(tempfile.mkdtemp())
    
    try:
        # Backup function
        def backup_item(source, dest, name):
            source_path = Path(source)
            if source_path.exists():
                print(f"[✓] Backing up {name}...")
                
                # Calculate size
                try:
                    size_result = subprocess.run(
                        ['du', '-sh', str(source_path)],
                        capture_output=True, text=True
                    )
                    size = size_result.stdout.split()[0] if size_result.returncode == 0 else "N/A"
                    print(f"    Size: {size}")
                except:
                    print("    Size: N/A")
                
                # Copy with shutil
                shutil.copytree(source_path, dest / source_path.name, 
                              dirs_exist_ok=True, symlinks=True)
            else:
                print(f"[−] {name} not found, skipping...")
        
        # Backup directories
        backup_item(Path.home() / '.openclaw', temp_dir, '.openclaw (main config)')
        backup_item(Path.home() / '.config' / 'openclaw', temp_dir, '.config/openclaw (system config)')
        backup_item(Path.home() / '.local' / 'share' / 'openclaw', temp_dir, '.local/share/openclaw (local data)')
        
        # Create archive
        print()
        print("Creating backup archive...")
        
        archive_file = f"{backup_path}.tar.gz"
        with tarfile.open(archive_file, 'w:gz') as tar:
            for item in temp_dir.iterdir():
                if item.is_dir():
                    for file in item.rglob('*'):
                        arcname = item.name / file.relative_to(temp_dir)
                        tar.add(file, arcname)
        
        # Calculate size
        size_result = subprocess.run(
            ['du', '-h', archive_file],
            capture_output=True, text=True
        )
        archive_size = size_result.stdout.split()[0] if size_result.returncode == 0 else "N/A"
        
        # Create info file
        info_file = f"{backup_path}.info"
        with open(info_file, 'w') as f:
            f.write("OpenClaw Configuration Backup\n")
            f.write("=============================\n")
            f.write(f"Backup Name: {backup_name}\n")
            f.write(f"Created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Hostname: {os.uname().nodename}\n")
            f.write(f"User: {os.getlogin()}\n")
            f.write(f"Archive Size: {archive_size}\n")
            f.write("\nBacked up items:\n")
            
            for item in [
                Path.home() / '.openclaw',
                Path.home() / '.config' / 'openclaw',
                Path.home() / '.local' / 'share' / 'openclaw'
            ]:
                if item.exists():
                    f.write(f"  - {item}\n")
        
        print()
        print("=== Backup Complete ===")
        print(f"Archive: {archive_file}")
        print(f"Info file: {info_file}")
        print(f"Size: {archive_size}")
        print()
        print("To restore:")
        print(f"  tar -xzf {archive_file} -C {Path.home()}")
        print()
        
    finally:
        # Cleanup
        shutil.rmtree(temp_dir, ignore_errors=True)

if __name__ == "__main__":
    main()
