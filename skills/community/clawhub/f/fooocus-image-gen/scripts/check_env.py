#!/usr/bin/env python3
"""
Fooocus Environment Checker
Checks and installs Fooocus and its dependencies
"""

import os
import sys
import subprocess
import json
import argparse
from pathlib import Path

# Default paths
FOOOCUS_DEFAULT_PATH = os.path.expanduser("~/Fooocus")
if sys.platform == "win32":
    FOOOCUS_DEFAULT_PATH = os.path.expanduser("~\\Fooocus")
FOOOCUS_REPO = "https://github.com/lllyasviel/Fooocus.git"
DEFAULT_PORT = 7865


def run_command(cmd, cwd=None, capture=True, timeout=60):
    """Run a shell command and return output"""
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


def check_python():
    """Check Python version"""
    version = sys.version_info
    if version.major == 3 and version.minor >= 10:
        return True, f"Python {version.major}.{version.minor}.{version.micro}"
    return False, f"Python {version.major}.{version.minor}.{version.micro} (requires 3.10+)"


def check_pytorch():
    """Check PyTorch installation"""
    try:
        import torch
        version = torch.__version__
        return True, f"PyTorch {version}"
    except ImportError:
        return False, "PyTorch not installed"


def check_cuda():
    """Check CUDA availability"""
    try:
        import torch
        if torch.cuda.is_available():
            gpu_name = torch.cuda.get_device_name(0)
            vram = torch.cuda.get_device_properties(0).total_memory / (1024**3)
            return True, f"{gpu_name} ({vram:.1f}GB VRAM)", vram
        return False, "CUDA not available (CPU mode only)", 0
    except ImportError:
        return False, "PyTorch not installed", 0


def check_system_requirements():
    """Check overall system requirements"""
    issues = []
    warnings = []
    
    # Check OS
    system = sys.platform
    if system == "win32":
        # Check Windows version
        try:
            import platform
            win_ver = platform.win32_ver()
            if int(win_ver[0]) < 10:
                issues.append("Windows 10 or higher required")
        except:
            pass
    elif system == "darwin":
        warnings.append("macOS detected - Fooocus works but slower than Linux/Windows")
    
    # Check available disk space
    try:
        if system == "win32":
            import ctypes
            free_bytes = ctypes.c_ulonglong(0)
            ctypes.windll.kernel32.GetDiskFreeSpaceExW(
                ctypes.c_wchar_p(os.path.expanduser("~")), 
                None, None, 
                ctypes.pointer(free_bytes)
            )
            free_gb = free_bytes.value / (1024**3)
        else:
            stat = os.statvfs(os.path.expanduser("~"))
            free_gb = (stat.f_bavail * stat.f_frsize) / (1024**3)
        
        if free_gb < 10:
            issues.append(f"Insufficient disk space: {free_gb:.1f}GB free (10GB+ recommended)")
        elif free_gb < 20:
            warnings.append(f"Low disk space: {free_gb:.1f}GB free (20GB+ recommended for multiple models)")
    except Exception as e:
        warnings.append(f"Could not check disk space: {e}")
    
    return issues, warnings


def check_fooocus_installation(path=None):
    """Check if Fooocus is installed"""
    if path is None:
        path = FOOOCUS_DEFAULT_PATH
    
    fooocus_path = Path(path)
    if not fooocus_path.exists():
        return False, f"Not found at {path}", None
    
    # Check for key files
    required_files = ["webui.py", "entry_with_update.py", "modules"]
    missing = []
    for f in required_files:
        if not (fooocus_path / f).exists():
            missing.append(f)
    
    if missing:
        return False, f"Missing: {', '.join(missing)}", str(fooocus_path)
    
    return True, f"Found at {path}", str(fooocus_path)


def check_fooocus_running(port=DEFAULT_PORT):
    """Check if Fooocus is running"""
    import urllib.request
    import urllib.error
    
    try:
        req = urllib.request.Request(
            f"http://localhost:{port}/",
            method="HEAD",
            headers={"User-Agent": "Fooocus-Check/1.0"}
        )
        with urllib.request.urlopen(req, timeout=5) as response:
            return True, f"Running on port {port}"
    except urllib.error.HTTPError as e:
        # Server is running but returned error (might be OK)
        if e.code in [404, 405]:
            return True, f"Running on port {port}"
        return False, f"HTTP error: {e.code}"
    except Exception as e:
        return False, f"Not running: {e}"


def check_models(fooocus_path):
    """Check if required models are downloaded"""
    models_dir = Path(fooocus_path) / "models" / "checkpoints"
    
    if not models_dir.exists():
        return False, "Models directory not found", []
    
    # Look for common model files
    model_extensions = [".safetensors", ".ckpt", ".pth"]
    models = []
    for ext in model_extensions:
        models.extend(list(models_dir.glob(f"*{ext}")))
    
    if models:
        return True, f"Found {len(models)} model(s)", [m.name for m in models]
    return False, "No models found (will download on first run)", []


def install_dependencies():
    """Install required Python packages"""
    print("Installing dependencies...")
    
    packages = [
        "torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121",
        "gradio",
        "websockets",
        "requests",
        "Pillow"
    ]
    
    for package in packages:
        print(f"  Installing {package.split()[0]}...")
        success, stdout, stderr = run_command(
            f"{sys.executable} -m pip install {package}",
            timeout=300
        )
        if not success:
            print(f"  Warning: Failed to install {package}: {stderr}")
            return False
    
    print("✓ Dependencies installed")
    return True


def install_fooocus(path=None, skip_models=False):
    """Install Fooocus from GitHub"""
    if path is None:
        path = FOOOCUS_DEFAULT_PATH
    
    print(f"Installing Fooocus to {path}...")
    
    # Clone repository
    parent_dir = os.path.dirname(path) or "."
    dir_name = os.path.basename(path)
    
    success, stdout, stderr = run_command(
        f"git clone {FOOOCUS_REPO} \"{dir_name}\"",
        cwd=parent_dir
    )
    
    if not success:
        print(f"Failed to clone repository: {stderr}")
        return False
    
    print("✓ Repository cloned successfully")
    
    # Install dependencies
    print("Installing Fooocus dependencies...")
    req_file = Path(path) / "requirements_versions.txt"
    if req_file.exists():
        success, stdout, stderr = run_command(
            f"{sys.executable} -m pip install -r \"{req_file}\"",
            cwd=path,
            timeout=600
        )
        if not success:
            print(f"Warning: Some dependencies failed: {stderr}")
    
    print("✓ Installation complete!")
    print(f"Fooocus installed at: {path}")
    print("\nTo start Fooocus:")
    print(f"  cd {path}")
    print(f"  python entry_with_update.py")
    
    return True


def start_fooocus(path=None, port=DEFAULT_PORT, preset=None):
    """Start Fooocus server"""
    if path is None:
        path = FOOOCUS_DEFAULT_PATH
    
    fooocus_path = Path(path)
    if not fooocus_path.exists():
        print(f"Fooocus not found at {path}")
        return False
    
    print(f"Starting Fooocus on port {port}...")
    
    cmd = f"{sys.executable} entry_with_update.py --port {port}"
    if preset:
        cmd += f" --preset {preset}"
    
    # Start in background
    if sys.platform == "win32":
        subprocess.Popen(
            cmd, cwd=path, shell=True,
            creationflags=subprocess.CREATE_NEW_CONSOLE
        )
    else:
        subprocess.Popen(
            cmd, cwd=path, shell=True,
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
    
    print("Fooocus starting... Wait 10-30 seconds for it to load.")
    print(f"Then access it at: http://localhost:{port}")
    
    return True


def print_environment_report(results):
    """Print formatted environment report"""
    print("=" * 60)
    print("Fooocus Environment Check Report")
    print("=" * 60)
    
    # Python
    py = results["python"]
    status = "✅" if py["ok"] else "❌"
    print(f"\n{status} Python: {py['message']}")
    
    # PyTorch
    pt = results.get("pytorch", {})
    if pt.get("ok"):
        print(f"✅ PyTorch: {pt['message']}")
    else:
        print(f"❌ PyTorch: {pt.get('message', 'Not checked')}")
    
    # CUDA
    cuda = results.get("cuda", {})
    if cuda.get("ok"):
        print(f"✅ CUDA: {cuda['message']}")
    elif cuda.get("message", "").startswith("CUDA not available"):
        print(f"⚠️  CUDA: {cuda['message']}")
        print("   💡 Fooocus can run on CPU but will be very slow")
    else:
        print(f"❌ CUDA: {cuda.get('message', 'Not checked')}")
    
    # System requirements
    sys_req = results.get("system_requirements", {})
    if sys_req.get("issues"):
        print(f"\n❌ System Issues:")
        for issue in sys_req["issues"]:
            print(f"   - {issue}")
    if sys_req.get("warnings"):
        print(f"\n⚠️  System Warnings:")
        for warning in sys_req["warnings"]:
            print(f"   - {warning}")
    
    # Fooocus installation
    inst = results["fooocus_installed"]
    if inst["ok"]:
        print(f"\n✅ Fooocus: {inst['message']}")
    else:
        print(f"\n❌ Fooocus: {inst['message']}")
    
    # Models
    if "models" in results and results["models"]:
        models = results["models"]
        if models.get("ok"):
            print(f"✅ Models: {models['message']}")
        else:
            print(f"⚠️  Models: {models['message']}")
    
    # Running status
    running = results["fooocus_running"]
    if running["ok"]:
        print(f"✅ Service: {running['message']}")
    else:
        print(f"❌ Service: {running['message']}")
    
    print("\n" + "=" * 60)
    
    # Recommendations
    print("\n📋 Recommendations:")
    if not py["ok"]:
        print("   1. Install Python 3.10 or higher")
    elif not pt.get("ok"):
        print("   1. Install PyTorch:")
        print("      pip install torch torchvision torchaudio")
    elif not cuda.get("ok") and not cuda.get("message", "").startswith("CUDA not available"):
        print("   1. Install CUDA-enabled PyTorch:")
        print("      pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121")
    elif not inst["ok"]:
        print("   1. Install Fooocus:")
        print(f"      python check_env.py --install --path {FOOOCUS_DEFAULT_PATH}")
    elif not running["ok"]:
        print("   1. Start Fooocus:")
        print(f"      cd {inst.get('path', FOOOCUS_DEFAULT_PATH)}")
        print("      python entry_with_update.py")
    else:
        print("   ✅ All checks passed! Fooocus is ready to use.")
    
    print("\n" + "=" * 60)


def main():
    parser = argparse.ArgumentParser(description="Fooocus Environment Checker")
    parser.add_argument("--path", help="Fooocus installation path")
    parser.add_argument("--install", action="store_true", help="Install Fooocus if not found")
    parser.add_argument("--install-deps", action="store_true", help="Install Python dependencies")
    parser.add_argument("--start", action="store_true", help="Start Fooocus server")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT, help="Port to use")
    parser.add_argument("--preset", help="Preset to use (default, anime, realistic, etc.)")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--quiet", "-q", action="store_true", help="Minimal output")
    
    args = parser.parse_args()
    
    # Run checks
    results = {
        "python": {},
        "pytorch": {},
        "cuda": {},
        "system_requirements": {},
        "fooocus_installed": {},
        "fooocus_running": {},
    }
    
    # Check Python
    ok, msg = check_python()
    results["python"] = {"ok": ok, "message": msg}
    
    # Check PyTorch
    ok, msg = check_pytorch()
    results["pytorch"] = {"ok": ok, "message": msg}
    
    # Check CUDA
    ok, msg, vram = check_cuda()
    results["cuda"] = {"ok": ok, "message": msg, "vram_gb": vram}
    
    # Check system requirements
    issues, warnings = check_system_requirements()
    results["system_requirements"] = {"issues": issues, "warnings": warnings}
    
    # Check Fooocus installation
    ok, msg, path = check_fooocus_installation(args.path)
    results["fooocus_installed"] = {"ok": ok, "message": msg, "path": path}
    
    # Check if running
    ok, msg = check_fooocus_running(args.port)
    results["fooocus_running"] = {"ok": ok, "message": msg}
    
    # Check models
    if path:
        ok, msg, models = check_models(path)
        results["models"] = {"ok": ok, "message": msg, "models": models}
    
    # Output results
    if args.json:
        print(json.dumps(results, indent=2))
    elif not args.quiet:
        print_environment_report(results)
    
    # Install dependencies if requested
    if args.install_deps:
        if not results["pytorch"]["ok"]:
            print("\nInstalling Python dependencies...")
            install_dependencies()
            # Re-check
            ok, msg = check_pytorch()
            results["pytorch"] = {"ok": ok, "message": msg}
    
    # Install if requested and not found
    if args.install and not results["fooocus_installed"]["ok"]:
        # First ensure dependencies
        if not results["pytorch"]["ok"]:
            print("\nInstalling dependencies first...")
            install_dependencies()
        
        if install_fooocus(args.path):
            # Re-check after installation
            ok, msg, path = check_fooocus_installation(args.path)
            results["fooocus_installed"] = {"ok": ok, "message": msg, "path": path}
    
    # Start if requested
    if args.start and not results["fooocus_running"]["ok"]:
        fooocus_path = results["fooocus_installed"].get("path")
        if fooocus_path:
            start_fooocus(fooocus_path, args.port, args.preset)
        else:
            print("Cannot start: Fooocus not installed")
    
    # Return exit code
    can_run = (
        results["python"]["ok"] and
        results["fooocus_installed"].get("ok") and
        results["fooocus_running"]["ok"]
    )
    
    sys.exit(0 if can_run else 1)


if __name__ == "__main__":
    main()
