import subprocess
import sys
import os
import argparse

# Define lock file path relative to this script
LOCK_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".install_complete")

def install(args, extra_args=None):
    cmd = [sys.executable, "-m", "pip", "install"]
    if isinstance(args, str):
        cmd.extend(args.split())
    else:
        cmd.extend(list(args))
    
    if extra_args:
        cmd.extend(extra_args)
        
    subprocess.check_call(cmd)

def main():
    parser = argparse.ArgumentParser(description="Install dependencies for BBC Crawler MaxClaw")
    parser.add_argument("--force", action="store_true", help="Force re-installation even if already installed")
    # Capture all other arguments to pass to pip
    args, unknown_args = parser.parse_known_args()

    # Check if already installed
    if os.path.exists(LOCK_FILE) and not args.force:
        print(f"Dependencies already installed (lock file found: {LOCK_FILE}).")
        print("Use --force to reinstall.")
        return

    print("Installing dependencies...")
    
    # 1. Install requirements.txt with passed arguments (e.g. --break-system-packages)
    print(f"Installing requirements from requirements.txt with args: {unknown_args}...")
    try:
        if os.path.exists("requirements.txt"):
            # Add --ignore-installed psutil to avoid "Cannot uninstall psutil" error on Debian/Ubuntu
            # when system psutil is present but pip tries to upgrade it.
            install_args = ["-r", "requirements.txt", "--ignore-installed", "psutil"]
            install(install_args, extra_args=unknown_args)
        else:
            print("Warning: requirements.txt not found!")
    except Exception as e:
        print(f"Error installing requirements: {e}")
        sys.exit(1)

    # 2. Install Playwright Browsers
    print("Installing Playwright browsers...")
    try:
        # Check if playwright is installed
        subprocess.check_call([sys.executable, "-m", "playwright", "install", "chromium"])
    except Exception as e:
        print(f"Error installing playwright browsers: {e}")
        # Don't exit here, browser install failure might be non-critical if using existing browsers

    print("\nInstallation complete.")

    # Create lock file
    try:
        with open(LOCK_FILE, "w") as f:
            f.write("Installation complete")
        print(f"Created lock file: {LOCK_FILE}")
    except Exception as e:
        print(f"Warning: Could not create lock file: {e}")

if __name__ == "__main__":
    main()
