"""
Skill Package Extraction Script
Used to extract zip format skill packages
"""

import os
import sys
import zipfile
import re


def check_filename_valid(filename):
    """
    Check if filename contains special characters
    Only allows: letters, numbers, Chinese characters, underscores, hyphens, dots
    """
    # Allowed characters: letters, numbers, Chinese characters, underscores, hyphens, dots
    pattern = r'^[\w\u4e00-\u9fa5\-\.]+$'
    return re.match(pattern, filename) is not None


def get_unique_folder_name(base_path, base_name):
    """
    Get a unique folder name
    If already exists, add _v1, _v2, etc. suffix
    """
    target_path = os.path.join(base_path, base_name)
    
    # If doesn't exist, return directly
    if not os.path.exists(target_path):
        return target_path, base_name
    
    # If exists, try adding version number
    version = 1
    while True:
        new_name = f"{base_name}_v{version}"
        new_path = os.path.join(base_path, new_name)
        if not os.path.exists(new_path):
            return new_path, new_name
        version += 1


def has_single_root_folder(zip_file):
    """
    Check if zip file has only one root folder
    Returns: (is_single_root, root_folder_name)
    """
    namelist = zip_file.namelist()
    
    if not namelist:
        return False, None
    
    # Get all top-level items
    root_items = set()
    for name in namelist:
        # Get first level path
        parts = name.split('/')
        if parts[0]:  # Exclude empty strings
            root_items.add(parts[0])
    
    # If only one root item and it's a folder
    if len(root_items) == 1:
        root_name = list(root_items)[0]
        # Check if it's a folder (at least one file under it)
        for name in namelist:
            if name.startswith(root_name + '/') and name != root_name + '/':
                return True, root_name
    
    return False, None


def unzip_skill_package(zip_path):
    """
    Extract skill package
    zip_path: Full path to the zip file
    Returns: Extracted directory path, or None if failed
    """
    # 1. Check if zip file exists
    if not os.path.exists(zip_path):
        print(f"Zip file does not exist: {zip_path}")
        return None
    
    # 2. Check if it's a zip file
    if not zip_path.lower().endswith('.zip'):
        print(f"Not a zip file: {zip_path}")
        return None
    
    # 3. Get filename (without extension)
    zip_dir = os.path.dirname(zip_path)
    zip_filename = os.path.basename(zip_path)
    base_name = os.path.splitext(zip_filename)[0]
    
    # 4. Check if filename contains special characters
    if not check_filename_valid(base_name):
        print(f"Filename contains special characters, extraction failed: {base_name}")
        print("   Only allowed: letters, numbers, Chinese characters, underscores, hyphens")
        return None
    
    # 5. Get unique target folder name
    target_path, final_name = get_unique_folder_name(zip_dir, base_name)
    
    if final_name != base_name:
        print(f"Target folder already exists, using new name: {final_name}")
    
    try:
        # 6. Open zip file
        with zipfile.ZipFile(zip_path, 'r') as zip_file:
            # 7. Check if there's a single root folder
            has_single_root, root_folder = has_single_root_folder(zip_file)
            
            if has_single_root:
                # Has single root folder, remove this layer when extracting
                print(f"Detected single root folder, avoiding nesting...")
                os.makedirs(target_path, exist_ok=True)
                
                for member in zip_file.namelist():
                    # Skip root folder itself
                    if member == root_folder + '/' or member == root_folder:
                        continue
                    
                    # Remove root folder prefix
                    if member.startswith(root_folder + '/'):
                        # Calculate relative path
                        relative_path = member[len(root_folder) + 1:]
                        if not relative_path:  # Skip empty paths
                            continue
                        
                        target_file = os.path.join(target_path, relative_path)
                        
                        # If it's a folder
                        if member.endswith('/'):
                            os.makedirs(target_file, exist_ok=True)
                        else:
                            # Ensure parent directory exists
                            parent_dir = os.path.dirname(target_file)
                            if parent_dir:
                                os.makedirs(parent_dir, exist_ok=True)
                            # Extract file
                            with zip_file.open(member) as source, open(target_file, 'wb') as target:
                                target.write(source.read())
            else:
                # No single root folder, extract directly
                print(f"Extracting to: {target_path}")
                zip_file.extractall(target_path)
        
        print(f"Extraction successful")
        print(f"Extraction path: {target_path}")
        return target_path
    
    except zipfile.BadZipFile:
        print(f"Invalid zip file: {zip_path}")
        return None
    except Exception as e:
        print(f"Extraction failed: {e}")
        # If extraction failed, try to clean up created folder
        if os.path.exists(target_path):
            try:
                import shutil
                shutil.rmtree(target_path)
            except:
                pass
        return None


def main():
    """
    Command line entry function
    """
    if len(sys.argv) != 2:
        print("Usage:")
        print("  python easyclaw_unzip_skill.py <zip_file_path>")
        print("\nExample:")
        print('  python easyclaw_unzip_skill.py "D:\\downloads\\my-skill.zip"')
        sys.exit(1)
    
    zip_path = sys.argv[1]
    
    print("=" * 60)
    print("Skill Package Extraction Tool")
    print("=" * 60)
    print(f"Zip file: {zip_path}")
    print("=" * 60)
    print()
    
    result = unzip_skill_package(zip_path)
    
    if result is None:
        sys.exit(1)
    else:
        print()
        print("=" * 60)
        print(f"Extraction completed: {result}")
        print("=" * 60)


if __name__ == "__main__":
    main()
