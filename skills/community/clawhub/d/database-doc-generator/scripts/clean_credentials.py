#!/usr/bin/env python3
"""
Credential Cleanup Script

This script removes all specific credential references and replaces them
with generic placeholders. Run this before any commit or distribution.
"""

import os
import re
import sys
from pathlib import Path

class CredentialCleaner:
    """Clean credential references from files"""
    
    # Patterns to find and replace
    REPLACEMENTS = [
        # Specific EXAMPLE_PASSWORDs
        (r'EXAMPLE_PASSWORD', 'EXAMPLE_PASSWORD'),
        (r'EXAMPLE_PASSWORD', 'EXAMPLE_PASSWORD'),
        (r'EXAMPLE_PASSWORD', 'EXAMPLE_PASSWORD'),
        (r'EXAMPLE_PASSWORD', 'EXAMPLE_PASSWORD'),
        (r'EXAMPLE_PASSWORD', 'EXAMPLE_PASSWORD'),
        
        # Specific database names
        (r'EXAMPLE_DATABASE', 'EXAMPLE_DATABASE'),
        (r'EXAMPLE_DATABASE', 'EXAMPLE_DATABASE'),
        (r'EXAMPLE_DATABASE', 'EXAMPLE_DATABASE'),
        (r'EXAMPLE_DATABASE', 'EXAMPLE_DATABASE'),
        
        # Specific hosts/IPs
        (r'192\.168\.3\.87', 'EXAMPLE_HOST'),
        (r'192\.168\.1\.100', 'EXAMPLE_HOST'),
        (r'db\.example\.com', 'EXAMPLE_HOST'),
        (r'wrong\.host', 'EXAMPLE_HOST'),
        
        # Specific usernames
        (r'EXAMPLE_USER', 'EXAMPLE_USER'),
        (r'EXAMPLE_USER', 'EXAMPLE_USER'),
        (r'EXAMPLE_USER', 'EXAMPLE_USER'),
        (r'EXAMPLE_USER', 'EXAMPLE_USER'),
        
        # File paths that might be specific
        (r'EXAMPLE_PATH/', 'EXAMPLE_PATH/'),
        (r'EXAMPLE_PATH/', 'EXAMPLE_PATH/'),
        (r'EXAMPLE_PATH/', 'EXAMPLE_PATH/'),
        (r'EXAMPLE_PATH/', 'EXAMPLE_PATH/'),
        (r'EXAMPLE_PATH/', 'EXAMPLE_PATH/'),
    ]
    
    def __init__(self, root_dir):
        self.root_dir = Path(root_dir)
        self.modified_files = []
        self.skipped_files = []
        
    def should_process_file(self, file_path):
        """Check if file should be processed"""
        # Skip binary files and certain directories
        skip_extensions = {'.pyc', '.pyo', '.pyd', '.so', '.dll', '.exe'}
        skip_dirs = {'.git', '__pycache__', '.venv', 'venv', 'node_modules'}
        
        if file_path.suffix in skip_extensions:
            return False
        
        for part in file_path.parts:
            if part in skip_dirs:
                return False
        
        return True
    
    def clean_file(self, file_path):
        """Clean credentials from a single file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            modified = False
            
            for pattern, replacement in self.REPLACEMENTS:
                new_content, count = re.subn(pattern, replacement, content)
                if count > 0:
                    content = new_content
                    modified = True
            
            if modified and content != original_content:
                # Backup original
                backup_path = file_path.with_suffix(file_path.suffix + '.bak')
                if not backup_path.exists():
                    with open(backup_path, 'w', encoding='utf-8') as f:
                        f.write(original_content)
                
                # Write cleaned content
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                self.modified_files.append(str(file_path))
                return True
            
            return False
            
        except UnicodeDecodeError:
            # Skip binary files
            self.skipped_files.append(f"{file_path} (binary)")
            return False
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
            self.skipped_files.append(f"{file_path} (error: {e})")
            return False
    
    def clean_directory(self):
        """Clean all files in directory"""
        file_extensions = {'.py', '.md', '.json', '.yaml', '.yml', '.txt', '.rst'}
        
        for file_path in self.root_dir.rglob('*'):
            if file_path.is_file() and self.should_process_file(file_path):
                if file_path.suffix in file_extensions:
                    self.clean_file(file_path)
    
    def print_report(self):
        """Print cleanup report"""
        print("=" * 70)
        print("CREDENTIAL CLEANUP REPORT")
        print("=" * 70)
        
        if self.modified_files:
            print(f"\n[OK] Modified {len(self.modified_files)} files:")
            for file in self.modified_files:
                print(f"  - {file}")
        
        if self.skipped_files:
            print(f"\n[WARN] Skipped {len(self.skipped_files)} files:")
            for file in self.skipped_files[:10]:  # Show first 10
                print(f"  - {file}")
            if len(self.skipped_files) > 10:
                print(f"  - ... and {len(self.skipped_files) - 10} more")
        
        print("\n" + "=" * 70)
        
        # Security recommendations
        if self.modified_files:
            print("\n[SECURITY] RECOMMENDATIONS:")
            print("  1. Review all modified files for accuracy")
            print("  2. Delete backup files (*.bak) after verification")
            print("  3. If any real credentials were present, rotate them immediately")
            print("  4. Run security check: python scripts/security_check.py")
            print("  5. Test functionality with example credentials")
        
        return len(self.modified_files) > 0

def main():
    """Main function"""
    if len(sys.argv) > 1:
        root_dir = Path(sys.argv[1])
    else:
        root_dir = Path(__file__).parent.parent
    
    if not root_dir.exists():
        print(f"Error: Directory not found: {root_dir}")
        sys.exit(1)
    
    print(f"[SCAN] Scanning directory: {root_dir}")
    print("Looking for credential references to clean...")
    
    cleaner = CredentialCleaner(root_dir)
    cleaner.clean_directory()
    
    if cleaner.print_report():
        print("\n[OK] Cleanup completed. Please review changes.")
        
        # Ask for confirmation to delete backups
        response = input("\nDelete backup files (*.bak)? (yes/no): ")
        if response.lower() == 'yes':
            for bak_file in root_dir.rglob('*.bak'):
                bak_file.unlink()
            print("Backup files deleted.")
    else:
        print("\n[OK] No credentials found to clean.")

if __name__ == "__main__":
    main()