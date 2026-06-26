#!/usr/bin/env python3
"""
Black-Fortress Layer 3: Behavioral Audit Engine

Compares the inspector's expected operations against actual eBPF/syscall trace.
Deterministic correlation — no LLM involved in the decision.

Usage:
    python behavioral_audit.py --trace <trace.json> --transcript <transcript.json>

Input formats:
    trace.json: {"syscalls": [{"name": "open", "args": ["file.csv"], "result": 3}, ...]}
    transcript.json: {"expected_operations": [{"action": "read", "target": "file.csv"}, ...]}
"""

import json
import os
import sys
import argparse
from typing import List, Dict, Set, Any
from dataclasses import dataclass, asdict
from pathlib import Path


# ─── Syscall Mapping ───────────────────────────────────────────

# Maps high-level operations to expected syscalls
OPERATION_TO_SYSCALLS = {
    "read": {"open", "read", "close", "lseek", "fstat", "stat"},
    "write": {"open", "write", "close", "fstat", "stat"},
    "create": {"open", "write", "close"},
    "delete": {"unlink", "unlinkat"},
    "list": {"open", "getdents", "getdents64", "close"},
    "execute": {"execve", "execveat", "fork", "clone", "wait4", "waitpid"},
    "network": {"socket", "connect", "sendto", "recvfrom", "bind", "listen", "accept"},
    "memory": {"mmap", "mprotect", "munmap", "brk"},
    "transform": set(),  # Pure computation — no syscalls expected
    "filter": set(),
    "sort": set(),
    "aggregate": set(),
    "log": {"write"},  # Writing to stderr/stdout
}

# Syscalls that are ALWAYS forbidden regardless of declared intent
FORBIDDEN_SYSCALLS = {
    "socket", "connect", "sendto", "recvfrom", "bind", "listen", "accept",
    "ptrace", "process_vm_readv", "process_vm_writev",
    "reboot", "kexec_load",
    "init_module", "finit_module", "delete_module",
    "mount", "umount2",
    "setuid", "setgid", "setreuid", "setregid",
    "chroot", "pivot_root",
}

# Syscalls that are expected in ANY process (noise)
UNIVERSAL_SYSCALLS = {
    "arch_prctl", "set_tid_address", "set_robust_list",
    "rt_sigaction", "rt_sigprocmask", "rt_sigreturn",
    "futex", "sched_getaffinity", "sched_yield",
    "exit_group", "exit",
    "prlimit64", "getrandom", "getpid", "getuid", "getgid",
    "geteuid", "getegid",
}


@dataclass
class SyscallEvent:
    name: str
    args: List[str]
    result: Any


@dataclass
class ExpectedOperation:
    action: str
    target: str = ""
    reason: str = ""


@dataclass
class AuditResult:
    status: str  # "pass", "flag", or "fail"
    forbidden_found: List[str]
    unexpected_found: List[str]
    expected_coverage: float  # 0.0 to 1.0
    total_syscalls: int
    unique_syscalls: Set[str]
    details: List[str]


def load_trace(trace_path: str) -> List[SyscallEvent]:
    """Load eBPF/syscall trace from JSON."""
    with open(trace_path, "r") as f:
        data = json.load(f)
    events = []
    for sc in data.get("syscalls", []):
        events.append(SyscallEvent(
            name=sc["name"],
            args=sc.get("args", []),
            result=sc.get("result", 0)
        ))
    return events


def load_transcript(transcript_path: str) -> List[ExpectedOperation]:
    """Load inspector's expected operations from JSON."""
    with open(transcript_path, "r") as f:
        data = json.load(f)
    ops = []
    for op in data.get("expected_operations", []):
        ops.append(ExpectedOperation(
            action=op["action"],
            target=op.get("target", ""),
            reason=op.get("reason", "")
        ))
    return ops


def compute_expected_syscalls(operations: List[ExpectedOperation]) -> Set[str]:
    """Derive expected syscalls from declared operations."""
    expected = set()
    for op in operations:
        action_scs = OPERATION_TO_SYSCALLS.get(op.action, set())
        expected.update(action_scs)
    expected.update(UNIVERSAL_SYSCALLS)
    return expected


def audit(trace: List[SyscallEvent], operations: List[ExpectedOperation]) -> AuditResult:
    """Core audit logic — deterministic correlation."""
    observed = {sc.name for sc in trace}
    expected = compute_expected_syscalls(operations)

    # Check for forbidden syscalls
    forbidden_found = sorted(observed & FORBIDDEN_SYSCALLS)

    # Check for unexpected syscalls (observed but not expected, excluding universal)
    meaningful_observed = observed - UNIVERSAL_SYSCALLS
    meaningful_expected = expected - UNIVERSAL_SYSCALLS
    unexpected_found = sorted(meaningful_observed - meaningful_expected)

    # Compute coverage: how many expected syscalls were observed?
    expected_meaningful = meaningful_expected
    if expected_meaningful:
        covered = len(expected_meaningful & meaningful_observed)
        coverage = covered / len(expected_meaningful)
    else:
        coverage = 1.0  # No syscalls expected (pure computation)

    # Generate details
    details = []
    if forbidden_found:
        details.append(f"FORBIDDEN syscalls detected: {', '.join(forbidden_found)}")
    if unexpected_found:
        details.append(f"Unexpected syscalls: {', '.join(unexpected_found)}")
    if coverage < 0.5:
        details.append(f"Low coverage: {coverage:.1%} of expected syscalls observed")

    # Determine status
    if forbidden_found:
        status = "fail"
    elif unexpected_found:
        status = "flag"
    elif coverage < 0.3:
        status = "flag"
    else:
        status = "pass"

    return AuditResult(
        status=status,
        forbidden_found=forbidden_found,
        unexpected_found=unexpected_found,
        expected_coverage=round(coverage, 3),
        total_syscalls=len(trace),
        unique_syscalls=observed,
        details=details
    )


def main():
    parser = argparse.ArgumentParser(description="Black-Fortress Behavioral Audit")
    parser.add_argument("--trace", required=True, help="eBPF trace JSON")
    parser.add_argument("--transcript", required=True, help="Inspector transcript JSON")
    parser.add_argument("--output", help="Write report to file")
    args = parser.parse_args()

    # Fail-closed: validate trace exists and is non-empty
    trace_warning = None
    if not os.path.exists(args.trace):
        trace_warning = (
            "[WARNING] Kernel Ground-Truth disabled (No eBPF traces found). "
            "Audit relies on Layer 0 only. "
            "Syscall-level verification is unavailable — behavioral analysis is incomplete."
        )
        trace = []
    else:
        trace = load_trace(args.trace)
        if not trace:
            trace_warning = (
                "[WARNING] Kernel Ground-Truth disabled (eBPF trace is empty). "
                "No syscalls recorded. "
                "Audit relies on Layer 0 only. "
                "The sandbox may have terminated before producing trace data."
            )

    operations = load_transcript(args.transcript)
    result = audit(trace, operations)

    report = {
        "status": result.status,
        "forbidden_syscalls": result.forbidden_found,
        "unexpected_syscalls": result.unexpected_found,
        "expected_coverage": result.expected_coverage,
        "total_syscalls": result.total_syscalls,
        "unique_syscalls": sorted(result.unique_syscalls),
        "details": result.details
    }

    if trace_warning:
        report["warning"] = trace_warning
        report["kernel_ground_truth"] = "disabled"
        print(trace_warning, file=sys.stderr)

    output = json.dumps(report, indent=2)
    if args.output:
        with open(args.output, "w") as f:
            f.write(output)
    else:
        print(output)

    sys.exit(0 if result.status == "pass" else 1)


if __name__ == "__main__":
    main()
