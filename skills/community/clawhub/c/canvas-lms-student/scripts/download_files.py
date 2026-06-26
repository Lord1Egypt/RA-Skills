#!/usr/bin/env python3
"""
Download files from a Canvas course.
Preserves folder structure and handles name conflicts.
"""

import argparse
import json
import os
import sys
from pathlib import Path
import requests
from canvas_client import get_canvas_client, get_config


def download_file(url: str, filepath: Path, token: str) -> bool:
    """Download a file from URL to local path."""
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(url, headers=headers, stream=True, timeout=60)
        response.raise_for_status()
        
        filepath.parent.mkdir(parents=True, exist_ok=True)
        
        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        return True
    except Exception as e:
        if not hasattr(download_file, 'silent') or not download_file.silent:
            print(f"  ✗ Failed to download: {e}")
        return False


def sanitize_filename(filename: str) -> str:
    """Remove invalid characters from filename."""
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    return filename


def get_folder_path(folder_id: int, folders_map: dict, cache: dict = None) -> str:
    """
    Get the full path for a folder, preserving Canvas structure.
    
    Args:
        folder_id: Canvas folder ID
        folders_map: Dictionary mapping folder_id -> folder object
        cache: Optional cache for computed paths
    
    Returns:
        Relative path string (e.g., "course files/assignments/")
    """
    if cache is None:
        cache = {}
    
    if folder_id in cache:
        return cache[folder_id]
    
    if folder_id not in folders_map:
        return ""
    
    folder = folders_map[folder_id]
    folder_name = sanitize_filename(folder.name)
    
    # Handle root folder (no parent or parent is root)
    if not hasattr(folder, 'parent_folder_id') or folder.parent_folder_id is None:
        cache[folder_id] = folder_name
        return folder_name
    
    parent_path = get_folder_path(folder.parent_folder_id, folders_map, cache)
    if parent_path:
        result = f"{parent_path}/{folder_name}"
    else:
        result = folder_name
    
    cache[folder_id] = result
    return result


def generate_unique_filename(filepath: Path, file_id: int) -> Path:
    """
    Generate a unique filename if file already exists.
    Prefixes with file_id if needed.
    
    Args:
        filepath: Desired filepath
        file_id: Canvas file ID (for disambiguation)
    
    Returns:
        Unique filepath
    """
    if not filepath.exists():
        return filepath
    
    # Add ID prefix: "file.pdf" -> "12345_file.pdf"
    new_name = f"{file_id}_{filepath.name}"
    new_path = filepath.parent / new_name
    
    return new_path


def file_to_dict(file, folder_path: str = "") -> dict:
    """Convert file object to dictionary."""
    return {
        "id": file.id,
        "name": file.display_name,
        "size": getattr(file, 'size', 0),
        "folder_path": folder_path,
        "content_type": getattr(file, 'content-type', None),
        "url": getattr(file, 'url', None),
    }


def main():
    parser = argparse.ArgumentParser(description="Download Canvas course files")
    parser.add_argument("--course", "-c", type=int, required=True,
                        help="Course ID")
    parser.add_argument("--output", "-o", type=str, default="./course-materials",
                        help="Output directory (default: ./course-materials)")
    parser.add_argument("--folder", type=str,
                        help="Download only from specific folder")
    parser.add_argument("--type", type=str,
                        help="Filter by file extension (e.g., pdf, docx)")
    parser.add_argument("--dry-run", action="store_true",
                        help="List files without downloading")
    parser.add_argument("--flat", action="store_true",
                        help="Flat structure (don't preserve Canvas folders)")
    parser.add_argument("--json", action="store_true",
                        help="Output as JSON")
    parser.add_argument("--no-id-prefix", action="store_true",
                        help="Don't add ID prefix for duplicate filenames")
    
    args = parser.parse_args()
    
    canvas = get_canvas_client(silent=args.json)
    _, token = get_config()
    output_dir = Path(args.output)
    
    # Set silent mode for download_file
    download_file.silent = args.json
    
    try:
        course = canvas.get_course(args.course)
        
        if not args.json:
            print(f"Course: {course.name}")
            print(f"Output directory: {output_dir.absolute()}\n")
        
        # Get folder structure for path resolution
        folders = {f.id: f for f in course.get_folders()}
        folder_cache = {}
        
        # Get files
        files = list(course.get_files(per_page=100))
        
        if not files:
            if args.json:
                print(json.dumps([]))
            else:
                print("No files found.")
            return
        
        # Filter by folder if specified
        if args.folder:
            target_folder = None
            for folder in folders.values():
                if args.folder.lower() in folder.name.lower():
                    target_folder = folder
                    break
            
            if target_folder:
                files = [f for f in files if f.folder_id == target_folder.id]
            else:
                if not args.json:
                    print(f"Folder '{args.folder}' not found. Available folders:")
                    for folder in folders.values():
                        print(f"  - {folder.name}")
                return
        
        # Filter by type if specified
        if args.type:
            files = [f for f in files if f.display_name.lower().endswith(f'.{args.type.lower()}')]
        
        if args.json:
            file_list = []
            for file in files:
                folder_path = "" if args.flat else get_folder_path(file.folder_id, folders, folder_cache)
                file_list.append(file_to_dict(file, folder_path))
            print(json.dumps(file_list, indent=2))
            return
        
        print(f"Found {len(files)} file(s) to download\n")
        
        if args.dry_run:
            print("Dry run - files that would be downloaded:")
            for file in files:
                folder_path = "" if args.flat else get_folder_path(file.folder_id, folders, folder_cache)
                if folder_path:
                    print(f"  - {folder_path}/{file.display_name} ({file.size // 1024} KB)")
                else:
                    print(f"  - {file.display_name} ({file.size // 1024} KB)")
            return
        
        # Download files
        success_count = 0
        skipped_count = 0
        error_count = 0
        downloaded_files = []
        
        for file in files:
            filename = sanitize_filename(file.display_name)
            
            # Determine folder path
            if args.flat:
                relative_path = ""
            else:
                relative_path = get_folder_path(file.folder_id, folders, folder_cache)
            
            # Build filepath
            if relative_path:
                filepath = output_dir / relative_path / filename
            else:
                filepath = output_dir / filename
            
            # Handle duplicates (unless --no-id-prefix)
            if not args.no_id_prefix:
                filepath = generate_unique_filename(filepath, file.id)
            
            # Skip if already exists and same size
            if filepath.exists() and filepath.stat().st_size == file.size:
                folder_display = f"[{relative_path}] " if relative_path else ""
                print(f"  ⏭ Skipped: {folder_display}{filename}")
                skipped_count += 1
                continue
            
            folder_display = f"[{relative_path}] " if relative_path else ""
            print(f"  ⬇ Downloading: {folder_display}{filename} ({file.size // 1024} KB)...", end=" ")
            
            # Get download URL
            try:
                file_obj = canvas.get_file(file.id)
                download_url = file_obj.url
                
                if download_file(download_url, filepath, token):
                    print("✓")
                    success_count += 1
                    downloaded_files.append({
                        "id": file.id,
                        "name": filename,
                        "path": str(filepath.relative_to(output_dir)),
                        "size": file.size
                    })
                else:
                    print("✗")
                    error_count += 1
            except Exception as e:
                print(f"✗ Error: {e}")
                error_count += 1
        
        print(f"\n✓ Downloaded: {success_count} | ⏭ Skipped: {skipped_count} | ✗ Errors: {error_count}")
        print(f"   Output: {output_dir.absolute()}")
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
