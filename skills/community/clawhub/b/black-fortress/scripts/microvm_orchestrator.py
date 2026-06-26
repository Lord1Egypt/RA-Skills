#!/usr/bin/env python3
"""
Black-Fortress Layer 2: Micro-VM Orchestrator

Manages sandbox lifecycle — container or micro-VM execution with seccomp.

Usage:
    python microvm_orchestrator.py --mode docker --source <dir> --timeout 300
    python microvm_orchestrator.py --mode firecracker --rootfs <path> --kernel <path> --timeout 300
"""

import os
import sys
import json
import subprocess
import tempfile
import shutil
import time
import hashlib
import argparse
from pathlib import Path
from typing import Optional, Dict, Any


SANDBOX_IMAGE = "black-fortress-runner:latest"
SCRIPT_DIR = Path(__file__).parent
SECCOMP_PROFILE = SCRIPT_DIR / "seccomp-profile.json"
DOCKER_BIN = os.environ.get("DOCKER_BIN", "docker")


def _build_safe_env() -> dict:
    """Build minimal environment for subprocess execution.
    
    Mirrors black_fortress.py _build_safe_env() — only whitelisted
    variables reach subprocesses. Host secrets are stripped.
    """
    WHITELIST = {
        "PATH", "DOCKER_BIN", "PYTHONPATH", "LANG",
        "LC_ALL", "LC_CTYPE", "HOME", "TMPDIR", "TERM",
    }
    safe_env = {k: v for k in WHITELIST if (v := os.environ.get(k))}
    if "PATH" not in safe_env:
        safe_env["PATH"] = "/usr/bin:/bin:/usr/local/bin"
    return safe_env


SANDBOX_ENV = _build_safe_env()


def run_docker_sandbox(source_dir: str, timeout: int,
                       memory_limit: str = "512m",
                       cpu_limit: str = "1") -> Dict[str, Any]:
    """Run feature in a Docker container with full isolation."""
    with tempfile.TemporaryDirectory(prefix="bf-sandbox-") as tmpdir:
        output_dir = os.path.join(tmpdir, "output")
        os.makedirs(output_dir, exist_ok=True)

        # Find the entry point
        entry_point = "main.py"
        source_abs = os.path.abspath(source_dir)
        for candidate in ["__main__.py", "main.py", "app.py"]:
            if os.path.exists(os.path.join(source_abs, candidate)):
                entry_point = candidate
                break

        container_name = f"bf-sandbox-{int(time.time())}"

        # Build as list to avoid shell injection from path interpolation
        cmd = [
            DOCKER_BIN, "run", "--rm",
            "--network=none",
            "--memory", memory_limit,
            "--cpus", cpu_limit,
            "--read-only",
            "--tmpfs", "/tmp:rw,noexec,nosuid,size=100m",
            "-v", f"{source_abs}:/sandbox/source:ro",
            "-v", f"{output_dir}:/sandbox/output:rw",
            "--name", container_name,
        ]

        # Add seccomp profile if available
        if SECCOMP_PROFILE.exists():
            cmd.extend(["--security-opt", f"seccomp={SECCOMP_PROFILE}"])

        cmd.extend([SANDBOX_IMAGE, "python", f"/sandbox/source/{entry_point}"])

        start_time = time.time()
        try:
            result = subprocess.run(
                cmd, capture_output=True,
                text=True, timeout=timeout, env=SANDBOX_ENV
            )
            duration = time.time() - start_time
            return {
                "status": "completed",
                "exit_code": result.returncode,
                "stdout": result.stdout[-5000:],  # Last 5KB
                "stderr": result.stderr[-5000:],
                "duration_seconds": round(duration, 2),
                "output_dir": output_dir,
                "mode": "docker"
            }
        except subprocess.TimeoutExpired:
            return {
                "status": "timeout",
                "exit_code": None,
                "duration_seconds": timeout,
                "output_dir": output_dir,
                "mode": "docker"
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "mode": "docker"
            }


def run_firecracker_sandbox(rootfs: str, kernel: str,
                            source_dir: str, timeout: int) -> Dict[str, Any]:
    """Run feature in a Firecracker micro-VM."""
    # This requires firecracker binary + rootfs + kernel
    # Simplified orchestration — real deployment would use the Firecracker API

    firecracker_bin = shutil.which("firecracker")
    if not firecracker_bin:
        return {
            "status": "error",
            "error": "firecracker binary not found in PATH",
            "mode": "firecracker"
        }

    with tempfile.TemporaryDirectory(prefix="bf-fc-") as tmpdir:
        socket_path = os.path.join(tmpdir, "firecracker.socket")
        config_path = os.path.join(tmpdir, "config.json")

        # Generate Firecracker config
        config = {
            "boot-source": {
                "kernel_image_path": kernel,
                "boot_args": "console=ttyS0 reboot=k panic=1 pci=off"
            },
            "drives": [
                {
                    "drive_id": "rootfs",
                    "path_on_host": rootfs,
                    "is_root_device": True,
                    "is_read_only": True
                }
            ],
            "machine-config": {
                "vcpu_count": 1,
                "mem_size_mib": 512,
                "smt": False
            },
            "network-interfaces": []  # No network
        }

        with open(config_path, "w") as f:
            json.dump(config, f)

        cmd = [
            firecracker_bin,
            "--api-sock", socket_path,
            "--config-file", config_path
        ]

        start_time = time.time()
        try:
            result = subprocess.run(
                cmd, capture_output=True, text=True, timeout=timeout,
                env=SANDBOX_ENV
            )
            duration = time.time() - start_time
            return {
                "status": "completed",
                "exit_code": result.returncode,
                "duration_seconds": round(duration, 2),
                "mode": "firecracker"
            }
        except subprocess.TimeoutExpired:
            return {
                "status": "timeout",
                "exit_code": None,
                "duration_seconds": timeout,
                "mode": "firecracker"
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "mode": "firecracker"
            }


def differential_test(source_dir: str, timeout: int) -> Dict[str, Any]:
    """
    Run the feature in BOTH Docker and Firecracker.
    Compare behavior to detect evasion.
    """
    docker_result = run_docker_sandbox(source_dir, timeout)
    fc_result = run_firecracker_sandbox(
        rootfs="/opt/bf-rootfs.ext4",
        kernel="/opt/vmlinux",
        source_dir=source_dir,
        timeout=timeout
    )

    # Compare exit codes and output
    behavior_match = (
        docker_result.get("exit_code") == fc_result.get("exit_code")
        and docker_result.get("status") == fc_result.get("status")
    )

    return {
        "docker": docker_result,
        "firecracker": fc_result,
        "evasion_detected": not behavior_match,
        "verdict": "pass" if behavior_match else "fail — behavior differs between sandbox types"
    }


def main():
    parser = argparse.ArgumentParser(description="Black-Fortress Micro-VM Orchestrator")
    parser.add_argument("--mode", choices=["docker", "firecracker", "differential"],
                        default="docker")
    parser.add_argument("--source", required=True, help="Feature source directory")
    parser.add_argument("--timeout", type=int, default=300, help="Timeout in seconds")
    parser.add_argument("--rootfs", help="Firecracker rootfs path")
    parser.add_argument("--kernel", help="Firecracker kernel path")
    parser.add_argument("--output", help="Write result to file")
    args = parser.parse_args()

    if args.mode == "docker":
        result = run_docker_sandbox(args.source, args.timeout)
    elif args.mode == "firecracker":
        result = run_firecracker_sandbox(args.rootfs or "", args.kernel or "",
                                         args.source, args.timeout)
    else:
        result = differential_test(args.source, args.timeout)

    output = json.dumps(result, indent=2)
    if args.output:
        with open(args.output, "w") as f:
            f.write(output)
    else:
        print(output)

    sys.exit(0 if result.get("status") == "completed" else 1)


if __name__ == "__main__":
    main()
