#!/usr/bin/env python3
import os
import sys
import platform
import urllib.request

def get_pi_path():
    """Get the path to the pi executable"""
    system = platform.system()
    if system == "Windows":
        return os.path.join(os.path.dirname(__file__), "pi.exe")
    elif system == "Darwin":
        return os.path.join(os.path.dirname(__file__), "pi")
    else:
        print("Error: Linux is not supported yet.")
        sys.exit(1)

def download_pi():
    """Download the pi executable"""
    system = platform.system()
    pi_path = get_pi_path()
    
    if system == "Windows":
        url = "https://github.com/noah-smith-max/pi_public/releases/download/r0.0.1/pi.exe"
    elif system == "Darwin":
        url = "https://github.com/noah-smith-max/pi_public/releases/download/r0.0.1/pi"
    else:
        print("Error: Linux is not supported yet.")
        sys.exit(1)
    
    print(f"Downloading pi from {url}...")
    urllib.request.urlretrieve(url, pi_path)
    
    if system != "Windows":
        os.chmod(pi_path, 0o755)
    
    print("Download completed successfully.")

def main():
    """Main function"""
    pi_path = get_pi_path()
    
    # Check if pi exists
    if not os.path.exists(pi_path):
        download_pi()
    
    # Build command arguments
    args = [pi_path] + sys.argv[1:]
    
    # Execute pi command
    try:
        result = os.system(' '.join(args))
        sys.exit(result)
    except Exception as e:
        print(f"Error executing pi: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
