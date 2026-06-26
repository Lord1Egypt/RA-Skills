import os
import shutil
import argparse
import subprocess
from pathlib import Path

def send_file(source_path, target_dir_name="檔案接收櫃"):
    """
    Copies a file or folder to the '檔案接收櫃' on the Desktop.
    """
    source = Path(source_path).resolve()
    if not source.exists():
        print(f"Error: Source path {source} does not exist.")
        return False

    desktop = Path.home() / "Desktop"
    target_dir = desktop / target_dir_name
    
    # Create target directory if it doesn't exist
    if not target_dir.exists():
        print(f"Creating reception folder: {target_dir}")
        target_dir.mkdir(parents=True, exist_ok=True)

    target_path = target_dir / source.name
    
    # Handle conflicts
    if target_path.exists():
        # Append asuffix if it already exists
        base = target_path.stem
        suffix = target_path.suffix
        counter = 1
        while target_path.exists():
            target_path = target_dir / f"{base}_{counter}{suffix}"
            counter += 1

    try:
        if source.is_dir():
            shutil.copytree(str(source), str(target_path))
        else:
            if target_path.exists():
                # Handling conflict by appending timestamp or counter is already in logic above
                pass
            shutil.copy2(str(source), str(target_path))
        
        print(f"Successfully 'sent' to: {target_path}")
        
        # New: Open the folder and select the file in Windows Explorer
        try:
            subprocess.run(['explorer', '/select,', str(target_path)])
        except Exception:
            pass
            
        return True
    except Exception as e:
        print(f"Error during transfer: {str(e)}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Send a file to the reception folder on the Desktop.")
    parser.add_argument("path", help="Path to the file or folder to send")
    
    args = parser.parse_args()
    
    send_file(args.path)

if __name__ == "__main__":
    main()
