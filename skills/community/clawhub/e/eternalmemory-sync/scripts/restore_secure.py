import os
import json
import argparse
import sys
import requests
from crypto_utils import decrypt_data
# Reuse restore logic from restore_local if possible, or reimplement simply
# For independence, implementing minimal restore logic here.

def restore_from_url(url, password, output_dir="."):
    print(f"Downloading memory blob from: {url}...")
    try:
        response = requests.get(url)
        response.raise_for_status()
        encrypted_content = response.text
    except Exception as e:
        print(f"Error downloading file: {e}")
        return

    print("Decrypting data...")
    try:
        # decrypt_data expects the raw base64 string
        # If the file contains extra whitespace, strip it
        json_str = decrypt_data(encrypted_content.strip(), password)
        backup_data = json.loads(json_str)
    except Exception as e:
        print(f"Decryption failed: {e}")
        print("Please check if the password is correct or the file is corrupted.")
        return

    files = backup_data.get("files", {})
    timestamp = backup_data.get("timestamp", "Unknown")
    
    print(f"Backup Timestamp: {timestamp}")
    print(f"Restoring {len(files)} files...")

    for filename, content in files.items():
        # Security check for paths
        if ".." in filename or filename.startswith("/") or filename.startswith("\\"):
                print(f"Skipping unsafe filename: {filename}")
                continue
        
        filepath = os.path.join(output_dir, filename)
        dir_path = os.path.dirname(filepath)
        if dir_path and not os.path.exists(dir_path):
            os.makedirs(dir_path)

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Restored: {filename}")

    print("Secure Restore Completed Successfully.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Restore Openclaw memory from encrypted URL.")
    parser.add_argument("--url", required=True, help="URL of the encrypted memory blob")
    parser.add_argument("--password", required=True, help="Password used for decryption")
    parser.add_argument("--output", default=".", help="Directory to restore files to")

    args = parser.parse_args()
    
    restore_from_url(args.url, args.password, args.output)
