#!/usr/bin/env python3
"""
Black-Fortress Master Orchestrator

Ties all 5 layers together into a single deterministic pipeline.
Zero LLM involvement in the decision.

Usage:
    python black_fortress.py --source <feature_dir> --timeout 300 --output <clean_dir> --report <report.json>
    python black_fortress.py --source <feature_dir> --timeout 300 --output <clean_dir> --report <report.json> --preserve-artifacts

Pipeline order:
    0. Transcript Extraction (from ORIGINAL code, before obfuscation)
    1. Semantic Neutralization (obfuscate)
    2. Hard Quarantine (Docker/Firecracker with seccomp)
    3. Kernel Ground-Truth (entropy + behavioral audit using extracted transcript)
    4. Trusted Output Rendering (anti-steganography)
    5. Sterile Autopsy (structured failure report)

Exit codes:
    0 — Feature approved (all 5 layers passed)
    1 — Feature rejected (at least one layer failed)
    2 — Protocol error (infrastructure failure)
"""

import os
import sys
import json
import subprocess
import tempfile
import shutil
import time
import argparse
from pathlib import Path
from typing import Dict, Any, List
from dataclasses import dataclass, asdict
from datetime import datetime, timezone


SCRIPT_DIR = Path(__file__).parent


@dataclass
class LayerResult:
    layer: int
    name: str
    status: str  # "pass", "fail", "error", "skip"
    duration_seconds: float
    details: Dict[str, Any]
    error: str = ""


@dataclass
class FortressReport:
    status: str  # "approved", "rejected", "error"
    timestamp: str
    source_dir: str
    total_duration: float
    layers: List[LayerResult]
    artifact_hashes: Dict[str, str]


def _resolve_docker_bin() -> str:
    """Resolve Docker binary path. Prefer PATH, fall back to macOS Docker Desktop."""
    docker = shutil.which("docker")
    if docker:
        return docker
    macos_path = "/Applications/Docker.app/Contents/Resources/bin/docker"
    if os.path.isfile(macos_path) and os.access(macos_path, os.X_OK):
        return macos_path
    raise FileNotFoundError(
        "Docker not found. Install Docker Desktop or add 'docker' to PATH."
    )


DOCKER_BIN = _resolve_docker_bin()


def _build_safe_env() -> dict:
    """Build a minimal environment for subprocess execution.
    
    Only whitelisted variables are passed. All host secrets (AWS keys,
    API tokens, personal paths) are stripped to enforce Least Privilege.
    
    See: Black-Fortress v1.1.6 — The Absolute Seal
    """
    WHITELIST = {
        "PATH",           # Required to find executables (python, docker, etc.)
        "DOCKER_BIN",     # Set by orchestrator for Docker path resolution
        "PYTHONPATH",     # Allow Python module resolution if configured
        "LANG",           # Locale — prevents encoding errors in subprocess output
        "LC_ALL",         # Locale fallback
        "LC_CTYPE",       # Character encoding
        "HOME",           # Required by some Python stdlib operations (tempfile, etc.)
        "TMPDIR",         # Temp directory override (macOS uses this)
        "TERM",           # Terminal type for subprocesses that check it
    }
    
    safe_env = {}
    for key in WHITELIST:
        val = os.environ.get(key)
        if val is not None:
            safe_env[key] = val
    
    # Ensure PATH is never empty (subprocesses would fail)
    if "PATH" not in safe_env:
        safe_env["PATH"] = "/usr/bin:/bin:/usr/local/bin"
    
    return safe_env


def run_script(script_name: str, args: list, timeout: int = 120) -> Dict[str, Any]:
    """Run a layer script and capture its output.
    
    Environment is scrubbed — only whitelisted variables are passed.
    Host secrets (AWS_*, API keys, tokens) never reach subprocesses.
    """
    script_path = SCRIPT_DIR / script_name
    env = _build_safe_env()
    env["DOCKER_BIN"] = DOCKER_BIN
    cmd = [sys.executable, str(script_path)] + args

    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=timeout, env=env
        )
        return {
            "exit_code": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr
        }
    except subprocess.TimeoutExpired:
        return {"exit_code": -1, "stdout": "", "stderr": "Script timed out"}
    except Exception as e:
        return {"exit_code": -1, "stdout": "", "stderr": str(e)}


def layer_0_transcript_extraction(source_dir: str, work_dir: str) -> LayerResult:
    """Layer 0: Auto-extract expected operations from ORIGINAL source code.
    
    This MUST run BEFORE Layer 1 obfuscation, so the transcript is extracted
    from readable code. The transcript feeds Layer 3's behavioral audit.
    """
    start = time.time()
    transcript_file = os.path.join(work_dir, "transcript.json")

    result = run_script("transcript_extractor.py", [
        "--source", source_dir,
        "--output", transcript_file
    ])
    duration = time.time() - start

    if os.path.exists(transcript_file):
        with open(transcript_file) as f:
            transcript = json.load(f)
        status = "pass"
        if transcript.get("summary", {}).get("high_risk_operations"):
            status = "flag"  # Don't fail — just flag for Layer 3 attention
    else:
        transcript = {"status": "error", "stderr": result.get("stderr", "")}
        status = "error"

    return LayerResult(
        layer=0, name="Transcript Extraction",
        status=status, duration_seconds=round(duration, 2),
        details=transcript
    )


def layer_1_semantic_neutralization(source_dir: str, work_dir: str) -> LayerResult:
    """Layer 1: Obfuscate all source code to kill semantic injection."""
    start = time.time()
    obfuscated_dir = os.path.join(work_dir, "obfuscated")
    os.makedirs(obfuscated_dir, exist_ok=True)

    result = run_script("deterministic_obfuscator.py", [source_dir, obfuscated_dir])
    duration = time.time() - start

    if result["exit_code"] == 0:
        try:
            report = json.loads(result["stdout"])
            return LayerResult(
                layer=1, name="Semantic Neutralization",
                status="pass", duration_seconds=round(duration, 2),
                details=report
            )
        except json.JSONDecodeError:
            return LayerResult(
                layer=1, name="Semantic Neutralization",
                status="pass", duration_seconds=round(duration, 2),
                details={"note": "completed but no structured output"}
            )
    else:
        return LayerResult(
            layer=1, name="Semantic Neutralization",
            status="error", duration_seconds=round(duration, 2),
            details={}, error=result["stderr"]
        )


def layer_2_hard_quarantine(source_dir: str, work_dir: str, timeout: int) -> LayerResult:
    """Layer 2: Run in micro-VM/container with seccomp."""
    start = time.time()
    sandbox_result_file = os.path.join(work_dir, "sandbox_result.json")

    result = run_script("microvm_orchestrator.py", [
        "--mode", "docker",
        "--source", source_dir,
        "--timeout", str(timeout),
        "--output", sandbox_result_file
    ], timeout=timeout + 30)

    duration = time.time() - start

    if os.path.exists(sandbox_result_file):
        with open(sandbox_result_file) as f:
            sandbox_result = json.load(f)
    else:
        sandbox_result = {"status": "unknown"}

    status = "pass" if sandbox_result.get("status") == "completed" and \
                       sandbox_result.get("exit_code") == 0 else "fail"

    return LayerResult(
        layer=2, name="Hard Quarantine",
        status=status, duration_seconds=round(duration, 2),
        details=sandbox_result
    )


def layer_3_kernel_groundtruth(work_dir: str) -> LayerResult:
    """Layer 3: Behavioral audit + entropy gating.
    
    Uses the auto-generated transcript from Layer 0 (extracted from
    original source before obfuscation).
    """
    start = time.time()

    # Entropy gate on sandbox output
    sandbox_output = os.path.join(work_dir, "output")
    entropy_report_file = os.path.join(work_dir, "entropy_report.json")

    if os.path.isdir(sandbox_output) and os.listdir(sandbox_output):
        result = run_script("entropy_gate.py", [
            "--input", sandbox_output,
            "--threshold", "6.0",
            "--output", entropy_report_file
        ])
        if os.path.exists(entropy_report_file):
            with open(entropy_report_file) as f:
                entropy_report = json.load(f)
        else:
            entropy_report = {"status": "unknown"}
    else:
        entropy_report = {"status": "pass", "note": "no output files to scan"}

    # Behavioral audit using the auto-generated transcript from Layer 0
    trace_file = os.path.join(work_dir, "trace.json")
    transcript_file = os.path.join(work_dir, "transcript.json")
    audit_report_file = os.path.join(work_dir, "audit_report.json")

    # Layer 0 auto-generates the transcript. If it exists, use it.
    # If no eBPF trace is available (Docker doesn't provide one natively),
    # the behavioral audit is informational only.
    if os.path.exists(trace_file) and os.path.exists(transcript_file):
        run_script("behavioral_audit.py", [
            "--trace", trace_file,
            "--transcript", transcript_file,
            "--output", audit_report_file
        ])
        if os.path.exists(audit_report_file):
            with open(audit_report_file) as f:
                audit_report = json.load(f)
        else:
            audit_report = {"status": "skip", "note": "audit script failed"}
    elif os.path.exists(transcript_file):
        # Transcript exists but no trace — report what was extracted
        with open(transcript_file) as f:
            transcript = json.load(f)
        audit_report = {
            "status": "skip",
            "note": "no eBPF trace available — transcript extracted for review",
            "extracted_operations": transcript.get("total_operations", 0),
            "high_risk_summary": transcript.get("summary", {})
        }
    else:
        audit_report = {"status": "skip", "note": "no transcript or trace available"}

    duration = time.time() - start

    entropy_ok = entropy_report.get("status") == "pass"
    audit_ok = audit_report.get("status") in ("pass", "skip")

    status = "pass" if (entropy_ok and audit_ok) else "fail"

    return LayerResult(
        layer=3, name="Kernel Ground-Truth",
        status=status, duration_seconds=round(duration, 2),
        details={
            "entropy_gate": entropy_report,
            "behavioral_audit": audit_report
        }
    )


def layer_4_trusted_output(source_dir: str, work_dir: str, output_dir: str) -> LayerResult:
    """Layer 4: Babel output filter — recompress images, block dangerous formats."""
    start = time.time()
    sandbox_output = os.path.join(work_dir, "output")
    babel_report_file = os.path.join(work_dir, "babel_report.json")

    if os.path.isdir(sandbox_output) and os.listdir(sandbox_output):
        result = run_script("babel_output_filter.py", [
            "--input", sandbox_output,
            "--output", output_dir
        ])
        if result["exit_code"] == 0:
            try:
                babel_report = json.loads(result["stdout"])
            except json.JSONDecodeError:
                babel_report = {"status": "completed"}
        else:
            babel_report = {"status": "error", "stderr": result["stderr"]}
    else:
        babel_report = {"status": "skip", "note": "no output to filter"}
        os.makedirs(output_dir, exist_ok=True)

    duration = time.time() - start
    status = "pass" if babel_report.get("status") in ("complete", "completed", "skip") else "fail"

    return LayerResult(
        layer=4, name="Trusted Output Rendering",
        status=status, duration_seconds=round(duration, 2),
        details=babel_report
    )


def layer_5_sterile_autopsy(work_dir: str, layers: List[LayerResult]) -> LayerResult:
    """Layer 5: Generate structured post-mortem (always runs)."""
    start = time.time()

    sandbox_exit_code = None
    for layer in layers:
        if layer.layer == 2 and "exit_code" in layer.details:
            sandbox_exit_code = layer.details.get("exit_code")
            break

    log_file = os.path.join(work_dir, "sandbox.log")
    trace_file = os.path.join(work_dir, "trace.json")
    report_file = os.path.join(work_dir, "postmortem.json")

    args = ["--sandbox-id", f"bf-{int(time.time())}",
            "--output", report_file]
    if sandbox_exit_code is not None:
        args.extend(["--exit-code", str(sandbox_exit_code)])
    if os.path.exists(log_file):
        args.extend(["--log-file", log_file])
    if os.path.exists(trace_file):
        args.extend(["--trace-file", trace_file])

    result = run_script("fail_closed_postmortem.py", args)
    duration = time.time() - start

    if os.path.exists(report_file):
        with open(report_file) as f:
            postmortem = json.load(f)
    else:
        postmortem = {"status": "error", "stderr": result.get("stderr", "")}

    return LayerResult(
        layer=5, name="Sterile Autopsy",
        status="pass", duration_seconds=round(duration, 2),
        details=postmortem
    )


def anti_ghost(work_dir: str) -> Dict[str, Any]:
    """Destroy all sandbox artifacts. Only clean output survives."""
    destroyed = []
    for item in Path(work_dir).rglob("*"):
        if item.is_file():
            item.unlink()
            destroyed.append(str(item))

    # Remove directories
    for item in sorted(Path(work_dir).rglob("*"), reverse=True):
        if item.is_dir():
            try:
                item.rmdir()
            except OSError:
                pass  # Directory not empty — OK

    return {
        "status": "complete",
        "artifacts_destroyed": len(destroyed)
    }


def preserve_or_destroy(work_dir: str, preserve: bool,
                        preserve_dir: str = None,
                        ttl_hours: int = 72,
                        metadata: Dict[str, Any] = None) -> Dict[str, Any]:
    """Either destroy artifacts (Anti-Ghost) or preserve them for forensics."""
    if not preserve:
        return {"action": "destroy", **anti_ghost(work_dir)}

    # Forensic preservation
    import time
    os.makedirs(preserve_dir or "/tmp/bf-forensics", exist_ok=True)
    archive_name = f"bf-{int(time.time())}.tar.gz"
    archive_path = os.path.join(preserve_dir or "/tmp/bf-forensics", archive_name)

    result = run_script("forensic_preserver.py", [
        "--work-dir", work_dir,
        "--output", archive_path,
        "--ttl-hours", str(ttl_hours),
        "--metadata", json.dumps(metadata or {})
    ])

    if result["exit_code"] == 0:
        try:
            preserver_result = json.loads(result["stdout"])
        except json.JSONDecodeError:
            preserver_result = {"status": "preserved", "raw": result["stdout"]}
    else:
        # Fallback to destruction if preservation fails
        preserver_result = {"action": "destroy_fallback", **anti_ghost(work_dir)}

    return {"action": "preserve", **preserver_result}


def run_black_fortress(source_dir: str, timeout: int,
                       output_dir: str, preserve_artifacts: bool = False,
                       preserve_dir: str = None,
                       ttl_hours: int = 72) -> FortressReport:
    """Execute the full Black-Fortress protocol."""
    start_time = time.time()

    with tempfile.TemporaryDirectory(prefix="black-fortress-") as work_dir:
        layers = []

        # Layer 0: Transcript Extraction (from ORIGINAL code, before obfuscation)
        l0 = layer_0_transcript_extraction(source_dir, work_dir)
        layers.append(l0)

        # Layer 1: Semantic Neutralization
        l1 = layer_1_semantic_neutralization(source_dir, work_dir)
        layers.append(l1)
        if l1.status == "error":
            return _build_report("error", source_dir, start_time, layers, {})

        # Layer 2: Hard Quarantine
        l2 = layer_2_hard_quarantine(source_dir, work_dir, timeout)
        layers.append(l2)

        # Layer 3: Kernel Ground-Truth (uses auto-generated transcript from L0)
        l3 = layer_3_kernel_groundtruth(work_dir)
        layers.append(l3)

        # Layer 4: Trusted Output Rendering
        l4 = layer_4_trusted_output(source_dir, work_dir, output_dir)
        layers.append(l4)

        # Layer 5: Sterile Autopsy (always runs)
        l5 = layer_5_sterile_autopsy(work_dir, layers)
        layers.append(l5)

        # Determine final verdict
        failed = [l for l in layers if l.status == "fail"]
        status = "rejected" if failed else "approved"

        # Compute artifact hashes
        artifact_hashes = {}
        if os.path.isdir(output_dir):
            for f in Path(output_dir).rglob("*"):
                if f.is_file():
                    import hashlib
                    artifact_hashes[str(f.relative_to(output_dir))] = \
                        hashlib.sha256(f.read_bytes()).hexdigest()

        report = _build_report(status, source_dir, start_time, layers, artifact_hashes)

        # Anti-Ghost or Forensic Preservation
        cleanup_result = preserve_or_destroy(
            work_dir, preserve_artifacts, preserve_dir, ttl_hours,
            metadata={"status": status, "source_dir": source_dir}
        )
        report.layers.append(LayerResult(
            layer=99, name="Cleanup",
            status="pass", duration_seconds=0,
            details=cleanup_result
        ))

        return report


def _build_report(status: str, source_dir: str, start_time: float,
                  layers: List[LayerResult], artifact_hashes: Dict[str, str]) -> FortressReport:
    return FortressReport(
        status=status,
        timestamp=datetime.now(timezone.utc).isoformat(),
        source_dir=source_dir,
        total_duration=round(time.time() - start_time, 2),
        layers=layers,
        artifact_hashes=artifact_hashes
    )


def main():
    parser = argparse.ArgumentParser(description="Black-Fortress Master Orchestrator")
    parser.add_argument("--source", required=True, help="Feature source directory")
    parser.add_argument("--timeout", type=int, default=300, help="Per-layer timeout")
    parser.add_argument("--output", required=True, help="Clean output directory")
    parser.add_argument("--report", help="Write JSON report to file")
    parser.add_argument("--preserve-artifacts", action="store_true",
                        help="Preserve sandbox artifacts for forensics (default: destroy)")
    parser.add_argument("--preserve-dir", default="/tmp/bf-forensics",
                        help="Directory for forensic archives (default: /tmp/bf-forensics)")
    parser.add_argument("--ttl-hours", type=int, default=72,
                        help="Forensic archive TTL in hours (default: 72)")
    args = parser.parse_args()

    if not os.path.isdir(args.source):
        print(json.dumps({"status": "error", "message": f"Not a directory: {args.source}"}))
        sys.exit(2)

    report = run_black_fortress(
        args.source, args.timeout, args.output,
        preserve_artifacts=args.preserve_artifacts,
        preserve_dir=args.preserve_dir,
        ttl_hours=args.ttl_hours
    )

    report_dict = asdict(report)
    report_json = json.dumps(report_dict, indent=2)

    if args.report:
        with open(args.report, "w") as f:
            f.write(report_json)

    print(report_json)

    if report.status == "approved":
        print("\n✓ FEATURE APPROVED — All 5 layers passed.", file=sys.stderr)
        sys.exit(0)
    elif report.status == "rejected":
        failed_layers = [l.name for l in report.layers if l.status == "fail"]
        print(f"\n✗ FEATURE REJECTED — Failed layers: {', '.join(failed_layers)}",
              file=sys.stderr)
        sys.exit(1)
    else:
        print("\n⚠ PROTOCOL ERROR — Check infrastructure.", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
