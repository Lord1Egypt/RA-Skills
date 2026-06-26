#!/usr/bin/env python3
"""
Start Ace Suno V5 Web Server
Automatically install dependencies if missing
"""

import subprocess
import sys
import os

def check_and_install(package):
    """Check if package is installed, install if not"""
    try:
        __import__(package)
        print("[OK] " + package + " already installed")
        return True
    except ImportError:
        print("Installing " + package + "...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        return False

def main():
    print("=" * 50)
    print("Starting Ace Suno V5 Music Generation Server")
    print("=" * 50)
    print()

    # Check dependencies
    print("Checking dependencies...")
    check_and_install('flask')
    check_and_install('requests')
    print()

    # Change to web directory and start server
    script_dir = os.path.dirname(os.path.abspath(__file__))
    web_dir = os.path.join(script_dir, 'web')
    os.chdir(web_dir)

    print()
    print("Starting server at http://localhost:1688")
    print("Open browser and visit http://localhost:1688 to start creating music")
    print("Click the black circle button on top right to close server")
    print()

    # Start the server
    os.execvp(sys.executable, [sys.executable, "app.py"])

if __name__ == "__main__":
    main()
