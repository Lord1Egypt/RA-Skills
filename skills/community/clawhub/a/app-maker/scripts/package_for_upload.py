#!/usr/bin/env python3
"""
Package App Maker skill for ClawHub upload
Creates a ZIP file with all required files
"""

import zipfile
import os
import json
from pathlib import Path
from datetime import datetime

# Files to include in the upload package
INCLUDE_FILES = [
    "SKILL.md",
    "README.md",
    "QUICKSTART.md",
    "SCREENSHOTS.md",
    "DEMO_VIDEO.md",
    "UPLOAD.md",
    "package.json",
    "_meta.json",
    "config.example.json",
]

INCLUDE_DIRS = [
    "scripts",
    ".clawhub",
]

# Files to exclude
EXCLUDE_PATTERNS = [
    "*.pyc",
    "__pycache__",
    ".git",
    "*.log",
    ".DS_Store",
    "node_modules",
]


def should_exclude(path: Path) -> bool:
    """Check if a path should be excluded"""
    path_str = str(path)
    for pattern in EXCLUDE_PATTERNS:
        if pattern.startswith("*"):
            if path_str.endswith(pattern[1:]):
                return True
        elif pattern in path_str:
            return True
    return False


def create_upload_package(output_dir: Path = None):
    """Create ZIP package for ClawHub upload"""
    
    if output_dir is None:
        output_dir = Path.cwd()
    
    # Get skill directory (parent of scripts directory)
    skill_dir = Path(__file__).parent.parent
    skill_name = skill_dir.name
    
    # Output file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = output_dir / f"{skill_name}_{timestamp}.zip"
    
    print(f" Creating upload package for {skill_name}...")
    print(f"   Source: {skill_dir}")
    print(f"   Output: {output_file}")
    
    # Create ZIP file
    with zipfile.ZipFile(output_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
        file_count = 0
        
        # Add individual files
        for file_name in INCLUDE_FILES:
            file_path = skill_dir / file_name
            if file_path.exists():
                arcname = f"{skill_name}/{file_name}"
                zipf.write(file_path, arcname)
                print(f"   [OK] Added: {file_name}")
                file_count += 1
            else:
                print(f"     Missing: {file_name}")
        
        # Add directories
        for dir_name in INCLUDE_DIRS:
            dir_path = skill_dir / dir_name
            if dir_path.exists():
                for root, dirs, files in os.walk(dir_path):
                    # Filter excluded directories
                    dirs[:] = [d for d in dirs if not should_exclude(Path(d))]
                    
                    for file in files:
                        file_path = Path(root) / file
                        if not should_exclude(file_path):
                            arcname = f"{skill_name}/{file_path.relative_to(skill_dir)}"
                            zipf.write(file_path, arcname)
                            file_count += 1
                
                print(f"    Added: {dir_name}/")
        
        # Add screenshots directory if exists
        screenshots_dir = skill_dir / "screenshots"
        if screenshots_dir.exists():
            for img_file in screenshots_dir.glob("*.png"):
                arcname = f"{skill_name}/screenshots/{img_file.name}"
                zipf.write(img_file, arcname)
                file_count += 1
            print(f"    Added: screenshots/")
        
        # Add tests directory if exists
        tests_dir = skill_dir / "tests"
        if tests_dir.exists():
            for test_file in tests_dir.glob("*.py"):
                arcname = f"{skill_name}/tests/{test_file.name}"
                zipf.write(test_file, arcname)
                file_count += 1
            print(f"    Added: tests/")
    
    # Create manifest file
    manifest = {
        "skill_name": skill_name,
        "version": "1.0.0",
        "package_date": datetime.now().isoformat(),
        "file_count": file_count,
        "package_file": output_file.name,
        "files_included": INCLUDE_FILES + [f"{d}/" for d in INCLUDE_DIRS],
        "upload_instructions": [
            "1. Go to https://clawhub.ai/skills/create",
            "2. Fill in the form (see UPLOAD.md for details)",
            "3. Upload this ZIP file",
            "4. Submit for review"
        ]
    }
    
    manifest_file = output_dir / f"{skill_name}_manifest.json"
    with open(manifest_file, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
    
    print(f"\n Package created successfully!")
    print(f"   ZIP file: {output_file}")
    print(f"   Total files: {file_count}")
    print(f"   Manifest: {manifest_file}")
    
    # Print file size
    file_size = output_file.stat().st_size
    size_mb = file_size / (1024 * 1024)
    print(f"   Package size: {size_mb:.2f} MB")
    
    return output_file


def validate_package():
    """Validate package before upload"""
    skill_dir = Path(__file__).parent.parent
    
    print("\n Validating package...")
    
    errors = []
    warnings = []
    
    # Check required files
    for file_name in INCLUDE_FILES:
        if file_name == "LICENSE":
            continue  # Optional
        file_path = skill_dir / file_name
        if not file_path.exists():
            errors.append(f"Missing required file: {file_name}")
    
    # Check scripts directory
    scripts_dir = skill_dir / "scripts"
    if not scripts_dir.exists():
        errors.append("Missing scripts/ directory")
    elif not (scripts_dir / "app_builder.py").exists():
        errors.append("Missing scripts/app_builder.py")
    
    # Check .clawhub directory
    clawhub_dir = skill_dir / ".clawhub"
    if not clawhub_dir.exists():
        errors.append("Missing .clawhub/ directory")
    elif not (clawhub_dir / "origin.json").exists():
        errors.append("Missing .clawhub/origin.json")
    
    # Check metadata files
    meta_file = skill_dir / "_meta.json"
    if meta_file.exists():
        try:
            with open(meta_file, 'r', encoding='utf-8') as f:
                meta = json.load(f)
                if "name" not in meta:
                    errors.append("_meta.json missing 'name' field")
                if "version" not in meta:
                    warnings.append("_meta.json missing 'version' field")
        except json.JSONDecodeError as e:
            errors.append(f"_meta.json is not valid JSON: {e}")
    
    # Check package.json
    package_file = skill_dir / "package.json"
    if package_file.exists():
        try:
            with open(package_file, 'r', encoding='utf-8') as f:
                package = json.load(f)
                if "skill" not in package:
                    warnings.append("package.json missing 'skill' section")
        except json.JSONDecodeError as e:
            errors.append(f"package.json is not valid JSON: {e}")
    
    # Print results
    if errors:
        print("\n Errors found:")
        for error in errors:
            print(f"   - {error}")
    
    if warnings:
        print("\n  Warnings:")
        for warning in warnings:
            print(f"   - {warning}")
    
    if not errors and not warnings:
        print("\n All validations passed!")
    
    return len(errors) == 0


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Package App Maker for ClawHub upload")
    parser.add_argument("--output", "-o", type=Path, default=None, help="Output directory")
    parser.add_argument("--validate", "-v", action="store_true", help="Validate only, don't create package")
    
    args = parser.parse_args()
    
    if args.validate:
        valid = validate_package()
        exit(0 if valid else 1)
    else:
        # Validate first
        if not validate_package():
            print("\n Please fix errors before packaging")
            exit(1)
        
        # Create package
        create_upload_package(args.output)
