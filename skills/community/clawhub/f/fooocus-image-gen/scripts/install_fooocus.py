#!/usr/bin/env python3
"""
Fooocus Installation Script
Automates the installation of Fooocus and its dependencies
"""

import os
import sys
import subprocess
import argparse
import platform
from pathlib import Path

FOOOCUS_REPO = "https://github.com/lllyasviel/Fooocus.git"
DEFAULT_INSTALL_PATH = os.path.expanduser("~/Fooocus")

# Model URLs (from Fooocus official)
MODELS = {
    "juggernautXL_v8Rundiffusion.safetensors": {
        "url": "https://civitai.com/api/download/models/288982",
        "size": "6.9GB",
        "preset": "default"
    },
    "animaPencilXL_v100.safetensors": {
        "url": "https://civitai.com/api/download/models/198144",
        "size": "6.9GB",
        "preset": "anime"
    },
    "realisticStockPhoto_v10.safetensors": {
        "url": "https://civitai.com/api/download/models/154593",
        "size": "6.9GB",
        "preset": "realistic"
    }
}


def run_command(cmd, cwd=None, capture=True, timeout=300):
    """Run a shell command"""
    try:
        if capture:
            result = subprocess.run(
                cmd, shell=True, cwd=cwd, capture_output=True, text=True, timeout=timeout
            )
            return result.returncode == 0, result.stdout, result.stderr
        else:
            result = subprocess.run(cmd, shell=True, cwd=cwd, timeout=timeout)
            return result.returncode == 0, "", ""
    except subprocess.TimeoutExpired:
        return False, "", "Command timed out"
    except Exception as e:
        return False, "", str(e)


def check_git():
    """Check if git is installed"""
    success, stdout, stderr = run_command("git --version")
    if success:
        return True, stdout.strip()
    return False, "Git not found"


def check_python_version():
    """Check Python version"""
    version = sys.version_info
    if version.major == 3 and version.minor >= 10:
        return True, f"Python {version.major}.{version.minor}.{version.micro}"
    return False, f"Python {version.major}.{version.minor}.{version.micro} (requires 3.10+)"


def clone_fooocus(path):
    """Clone Fooocus repository"""
    print(f"Cloning Fooocus to {path}...")
    
    parent_dir = os.path.dirname(path)
    dir_name = os.path.basename(path)
    
    success, stdout, stderr = run_command(
        f"git clone {FOOOCUS_REPO} \"{dir_name}\"",
        cwd=parent_dir if parent_dir else "."
    )
    
    if not success:
        print(f"Failed to clone: {stderr}")
        return False
    
    print("✓ Repository cloned successfully")
    return True


def install_dependencies(fooocus_path):
    """Install Python dependencies"""
    print("\nInstalling dependencies...")
    
    # Check for requirements file
    req_files = [
        "requirements_versions.txt",
        "requirements.txt"
    ]
    
    for req_file in req_files:
        req_path = Path(fooocus_path) / req_file
        if req_path.exists():
            print(f"Installing from {req_file}...")
            success, stdout, stderr = run_command(
                f"{sys.executable} -m pip install -r \"{req_path}\"",
                timeout=600
            )
            if success:
                print(f"✓ Dependencies installed")
                return True
            else:
                print(f"Warning: Some dependencies failed: {stderr}")
                return False
    
    print("No requirements file found")
    return False


def setup_models(fooocus_path, download=False):
    """Setup model directories"""
    models_dir = Path(fooocus_path) / "models" / "checkpoints"
    models_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"\nModel directory: {models_dir}")
    
    if download:
        print("\nPre-downloading models (this will take a while)...")
        for model_name, info in MODELS.items():
            model_path = models_dir / model_name
            if model_path.exists():
                print(f"  ✓ {model_name} already exists")
                continue
            
            print(f"  Downloading {model_name} ({info['size']})...")
            print(f"    URL: {info['url']}")
            print(f"    Note: Models will be downloaded automatically on first run if skipped")
    else:
        print("\nModels will be downloaded automatically on first run.")
        print("To pre-download, run with --download-models")


def create_launcher_scripts(fooocus_path):
    """Create convenient launcher scripts"""
    system = platform.system()
    
    if system == "Windows":
        # Windows batch files
        batch_content = f"""@echo off
cd /d "{fooocus_path}"
python entry_with_update.py %*
pause
"""
        launcher_path = Path(fooocus_path).parent / "run_fooocus.bat"
        with open(launcher_path, "w") as f:
            f.write(batch_content)
        print(f"\nCreated launcher: {launcher_path}")
        
    else:
        # Unix shell scripts
        sh_content = f"""#!/bin/bash
cd "{fooocus_path}"
python entry_with_update.py "$@"
"""
        launcher_path = Path(fooocus_path).parent / "run_fooocus.sh"
        with open(launcher_path, "w") as f:
            f.write(sh_content)
        os.chmod(launcher_path, 0o755)
        print(f"\nCreated launcher: {launcher_path}")


def print_post_install(fooocus_path):
    """Print post-installation instructions"""
    print("\n" + "=" * 60)
    print("Installation Complete!")
    print("=" * 60)
    print(f"\nFooocus installed at: {fooocus_path}")
    print("\nTo start Fooocus:")
    print(f"  cd \"{fooocus_path}\"")
    print(f"  python entry_with_update.py")
    print("\nOr use the launcher script in the parent directory")
    print("\nFirst run will download models (~6-10GB)")
    print("This may take 10-30 minutes depending on your connection")
    print("\nThen access Fooocus at: http://localhost:7865")
    print("\nFor more options:")
    print("  python entry_with_update.py --help")


def main():
    parser = argparse.ArgumentParser(description="Install Fooocus")
    parser.add_argument("--path", default=DEFAULT_INSTALL_PATH, help="Installation path")
    parser.add_argument("--download-models", action="store_true", help="Pre-download models")
    parser.add_argument("--skip-deps", action="store_true", help="Skip dependency installation")
    parser.add_argument("--force", action="store_true", help="Force reinstall if exists")
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("Fooocus Installation")
    print("=" * 60)
    
    # Check prerequisites
    print("\nChecking prerequisites...")
    
    ok, msg = check_python_version()
    print(f"  {'✓' if ok else '✗'} {msg}")
    if not ok:
        print("Error: Python 3.10+ required")
        sys.exit(1)
    
    ok, msg = check_git()
    print(f"  {'✓' if ok else '✗'} {msg}")
    if not ok:
        print("Error: Git is required")
        print("Please install Git: https://git-scm.com/downloads")
        sys.exit(1)
    
    # Check if already installed
    fooocus_path = Path(args.path)
    if fooocus_path.exists():
        if args.force:
            print(f"\nRemoving existing installation at {fooocus_path}...")
            import shutil
            shutil.rmtree(fooocus_path)
        else:
            print(f"\nFooocus already exists at {fooocus_path}")
            print("Use --force to reinstall")
            return
    
    # Clone repository
    if not clone_fooocus(args.path):
        sys.exit(1)
    
    # Install dependencies
    if not args.skip_deps:
        install_dependencies(args.path)
    
    # Setup models
    setup_models(args.path, args.download_models)
    
    # Create launcher
    create_launcher_scripts(args.path)
    
    # Print instructions
    print_post_install(args.path)


if __name__ == "__main__":
    main()
