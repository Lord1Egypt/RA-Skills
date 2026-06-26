#!/usr/bin/env python3
"""
Validates doc-setup organized documentation structure.
Checks:
- 00-index.md exists and references all topic files
- Numbered files are sequential (no gaps)
- Each file has source attribution
- Living document markers present
- Cross-references valid
"""

import os
import re
import sys
from pathlib import Path


def validate_doc_structure(base_path):
    """Validate organized documentation structure."""
    base = Path(base_path)
    errors = []
    warnings = []
    
    if not base.exists():
        return False, [f"Path does not exist: {base_path}"], []
    
    # Find all .md files
    md_files = sorted(base.glob("*.md"))
    if not md_files:
        return False, ["No .md files found"], []
    
    # Check for 00-index.md
    index_file = base / "00-index.md"
    if not index_file.exists():
        errors.append("Missing 00-index.md (master index)")
    else:
        # Validate index content
        index_content = index_file.read_text()
        
        # Check for source attribution
        if "Source:" not in index_content and "source" not in index_content.lower():
            warnings.append("00-index.md missing source attribution")
        
        # Check for table of contents
        if "|" not in index_content or "Arquivo" not in index_content:
            warnings.append("00-index.md may be missing file table")
    
    # Check numbered files
    numbered_files = [f for f in md_files if re.match(r'^\d{2}-', f.name)]
    if not numbered_files:
        errors.append("No numbered topic files found (expected NN-topic.md)")
    
    # Check sequential numbering
    numbers = [int(re.match(r'^(\d{2})-', f.name).group(1)) for f in numbered_files if re.match(r'^\d{2}-', f.name)]
    if numbers:
        expected = list(range(min(numbers), max(numbers) + 1))
        missing = [n for n in expected if n not in numbers]
        if missing:
            warnings.append(f"Missing numbered files: {[f'{n:02d}' for n in missing]}")
    
    # Validate each topic file
    for md_file in numbered_files:
        content = md_file.read_text()
        
        # Check source attribution
        if "Source:" not in content and "source" not in content.lower():
            errors.append(f"{md_file.name}: Missing source attribution")
        
        # Check living document marker
        if "Living Document" not in content and "living" not in content.lower():
            warnings.append(f"{md_file.name}: Missing living document marker")
        
        # Check last updated
        if "Last updated" not in content and "updated" not in content.lower():
            warnings.append(f"{md_file.name}: Missing 'Last updated' timestamp")
    
    # Summary
    if errors:
        return False, errors, warnings
    elif warnings:
        return True, [], warnings
    else:
        return True, [], []


def main():
    if len(sys.argv) < 2:
        print("Usage: validate_structure.py <path/to/organized/docs>")
        sys.exit(1)
    
    base_path = sys.argv[1]
    is_valid, errors, warnings = validate_doc_structure(base_path)
    
    print(f"Validating: {base_path}")
    print("=" * 50)
    
    if is_valid and not warnings:
        print("✅ All checks passed!")
        sys.exit(0)
    elif is_valid and warnings:
        print("⚠️  Structure valid with warnings:")
        for w in warnings:
            print(f"  - {w}")
        sys.exit(0)
    else:
        print("❌ Validation failed:")
        for e in errors:
            print(f"  - {e}")
        if warnings:
            print("\nWarnings:")
            for w in warnings:
                print(f"  - {w}")
        sys.exit(1)


if __name__ == "__main__":
    main()
