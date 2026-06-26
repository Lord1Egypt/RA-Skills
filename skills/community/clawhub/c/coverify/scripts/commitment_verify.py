#!/usr/bin/env python3
"""
commitment_verify.py — MO§ES™ Commitment Extraction + Verification
Implements the Commitment Conservation Law at the signal layer.

Extracts the irreducible commitment kernel from a text signal and measures
how much commitment is preserved across transformations. This is what the
Jaccard inter-agent verification score is built on.

Commands:
  extract "<text>"                — extract commitment kernel from signal
  compare "<text_a>" "<text_b>"  — Jaccard score: how much commitment is shared
  verify <input_hash_a> <input_hash_b>
                                 — compare two audit entries by their input hashes

Theory:
  C(T(S)) = C(S) — commitment is conserved under transformation.
  Jaccard(C(S_a), C(S_b)) < threshold → commitment leak detected.
  Low score on same input = model extraction variance (not a leak).
  Low score on different inputs = expected divergence.
  Hash the raw signal first (Isnad Layer 0) to isolate which case you're in.
"""

import hashlib
import json
import os
import re
import sys

LEDGER_PATH = os.path.expanduser("~/.openclaw/audits/moses/audit_ledger.jsonl")

# Hard commitment markers — language that encodes irreducible commitment.
# These are the tokens that survive compression if the signal has a kernel.
COMMITMENT_PATTERNS = [
    r"\b(must|shall|will|cannot|can not|won't|won't|will not|never|always)\b",
    r"\b(require[sd]?|guarantee[sd]?|ensure[sd]?|enforce[sd]?)\b",
    r"\b(is required|are required|is prohibited|are prohibited)\b",
    r"\b(no .{0,20} without|only if|only when|unless)\b",
    r"\b(commit[s]?|committed|commitment)\b",
    r"\b(exactly|precisely|strictly|solely|exclusively)\b",
    r"\bnot .{0,10}(optional|negotiable|discretionary)\b",
]

COMPILED = [re.compile(p, re.IGNORECASE) for p in COMMITMENT_PATTERNS]


def extract_hard_commitments(text: str) -> set:
    """
    Extract the irreducible commitment kernel from a text signal.
    Returns a set of normalized commitment-bearing tokens/phrases.
    The kernel is what survives compression — C(S).
    """
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    kernel = set()

    for sentence in sentences:
        for pattern in COMPILED:
            matches = pattern.findall(sentence)
            if matches:
                # Normalize and add the full sentence context around the match
                normalized = re.sub(r'\s+', ' ', sentence.strip().lower())
                kernel.add(normalized)
                break  # one match per sentence is enough to flag it

    # Also extract individual hard commitment tokens
    for pattern in COMPILED:
        for match in pattern.finditer(text):
            kernel.add(match.group(0).lower().strip())

    return kernel


def jaccard_similarity(set_a: set, set_b: set) -> float:
    """
    Jaccard similarity between two commitment kernels.
    J(A, B) = |A ∩ B| / |A ∪ B|
    Score of 1.0 = identical commitment kernels.
    Score of 0.0 = no shared commitments.
    Threshold: < 0.8 on identical inputs = commitment leak or model variance.
    """
    if not set_a and not set_b:
        return 1.0  # both empty = no commitments in either, conserved trivially
    if not set_a or not set_b:
        return 0.0
    intersection = set_a & set_b
    union = set_a | set_b
    return len(intersection) / len(union)


def cmd_extract(args):
    if not args:
        print("Usage: commitment_verify.py extract \"<text>\"")
        sys.exit(1)
    text = " ".join(args)
    kernel = extract_hard_commitments(text)
    input_hash = hashlib.sha256(text.encode()).hexdigest()
    result = {
        "input_hash": input_hash,
        "kernel_size": len(kernel),
        "kernel": sorted(kernel),
    }
    print(json.dumps(result, indent=2))


def cmd_compare(args):
    if len(args) < 2:
        print("Usage: commitment_verify.py compare \"<text_a>\" \"<text_b>\"")
        sys.exit(1)
    text_a, text_b = args[0], args[1]
    kernel_a = extract_hard_commitments(text_a)
    kernel_b = extract_hard_commitments(text_b)
    score = jaccard_similarity(kernel_a, kernel_b)
    hash_a = hashlib.sha256(text_a.encode()).hexdigest()
    hash_b = hashlib.sha256(text_b.encode()).hexdigest()

    verdict = "CONSERVED" if score >= 0.8 else ("VARIANCE" if hash_a == hash_b else "DIVERGED")

    result = {
        "input_hash_a": hash_a,
        "input_hash_b": hash_b,
        "same_input": hash_a == hash_b,
        "jaccard_score": round(score, 4),
        "threshold": 0.8,
        "verdict": verdict,
        "kernel_a_size": len(kernel_a),
        "kernel_b_size": len(kernel_b),
        "shared": sorted(kernel_a & kernel_b),
        "only_in_a": sorted(kernel_a - kernel_b),
        "only_in_b": sorted(kernel_b - kernel_a),
    }
    print(json.dumps(result, indent=2))
    if verdict == "VARIANCE":
        print("\n[WARN] Same input, low Jaccard — model extraction variance detected.")
        print("       This is an epistemological mismatch, not a commitment leak.")
    elif verdict == "DIVERGED":
        print(f"\n[WARN] Jaccard {score:.2f} below threshold. Commitment leak or input mismatch.")


def cmd_verify(args):
    """Compare two ledger entries by their input hashes."""
    if len(args) < 2:
        print("Usage: commitment_verify.py verify <input_hash_a> <input_hash_b>")
        sys.exit(1)
    hash_a, hash_b = args[0], args[1]

    if not os.path.exists(LEDGER_PATH):
        print("[ERROR] No audit ledger found.")
        sys.exit(1)

    entries = {}
    with open(LEDGER_PATH) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            e = json.loads(line)
            isnad = e.get("isnad", {})
            ih = isnad.get("input_hash")
            if ih in (hash_a, hash_b):
                entries[ih] = e

    found_a = entries.get(hash_a)
    found_b = entries.get(hash_b)

    result = {
        "hash_a": hash_a,
        "hash_b": hash_b,
        "entry_a_found": found_a is not None,
        "entry_b_found": found_b is not None,
    }

    if found_a and found_b:
        result["agent_a"] = found_a.get("agent")
        result["agent_b"] = found_b.get("agent")
        result["timestamp_a"] = found_a.get("timestamp")
        result["timestamp_b"] = found_b.get("timestamp")
        result["same_input"] = hash_a == hash_b
        result["note"] = "Both entries found in ledger. Run compare on original texts for Jaccard."
    elif not found_a:
        result["error"] = f"No ledger entry found for input_hash: {hash_a}"
    else:
        result["error"] = f"No ledger entry found for input_hash: {hash_b}"

    print(json.dumps(result, indent=2))


def ghost_tokens(kernel_before: set, kernel_after: set) -> dict:
    """
    Ghost token accounting — quantify how much commitment leaked and what form it took.

    Cornelius-Trinity / teaneo correction: G_t = G_0 * e^(-2t) assumes uniform
    continuous leakage. In practice, meaning loss is step-function — one corrupted
    input can cascade through all downstream reasoning while looking locally fine.

    This function models both:
    - Magnitude: how many commitment tokens are gone
    - Form: WHICH tokens leaked (the pattern matters — same pattern across agents = structural flaw)
    - Cascade risk: whether any leaked token is a modal/enforcement anchor
      (must/shall/never/always) — these are high-cascade because downstream
      reasoning inherits the softening.

    Returns a ghost_token report. Log it. Compare it across agents.
    If two agents produce the same ghost_pattern, that's not variance — that's a structural hole.
    """
    leaked = kernel_before - kernel_after
    gained = kernel_after - kernel_before  # unexpected additions also matter

    # High-cascade tokens — their loss softens all downstream commitments
    HIGH_CASCADE = {"must", "shall", "never", "always", "cannot", "will not",
                    "won't", "required", "guarantee", "ensure", "enforce"}

    leaked_cascade = [t for t in leaked if any(hc in t for hc in HIGH_CASCADE)]
    gained_noise = [t for t in gained if not any(hc in t for hc in HIGH_CASCADE)]

    # Step-function risk: if ANY cascade token leaked, risk = HIGH regardless of count
    if leaked_cascade:
        cascade_risk = "HIGH"
        cascade_note = "Modal/enforcement anchor lost. All downstream reasoning inherits softening."
    elif leaked:
        cascade_risk = "MEDIUM"
        cascade_note = "Commitments leaked but no enforcement anchors affected."
    else:
        cascade_risk = "NONE"
        cascade_note = "No leakage detected."

    # Ghost pattern fingerprint — SHA-256 of sorted leaked tokens
    # Two agents with the same fingerprint = structural flaw, not accident
    ghost_pattern = hashlib.sha256(
        json.dumps(sorted(leaked), separators=(",", ":")).encode()
    ).hexdigest() if leaked else None

    return {
        "tokens_before": len(kernel_before),
        "tokens_after": len(kernel_after),
        "leaked_count": len(leaked),
        "gained_count": len(gained),
        "leaked_tokens": sorted(leaked),
        "leaked_cascade_tokens": leaked_cascade,
        "gained_noise_tokens": gained_noise,
        "cascade_risk": cascade_risk,
        "cascade_note": cascade_note,
        "ghost_pattern": ghost_pattern,
        "ghost_pattern_note": "Same ghost_pattern across two agents = structural flaw, not extraction variance.",
    }


def cmd_ghost(args):
    """Compute ghost token report between original and transformed signal."""
    if len(args) < 2:
        print("Usage: commitment_verify.py ghost \"<original>\" \"<transformed>\"")
        sys.exit(1)
    original, transformed = args[0], args[1]
    kernel_before = extract_hard_commitments(original)
    kernel_after = extract_hard_commitments(transformed)
    report = ghost_tokens(kernel_before, kernel_after)
    report["input_hash_original"] = hashlib.sha256(original.encode()).hexdigest()
    report["input_hash_transformed"] = hashlib.sha256(transformed.encode()).hexdigest()
    print(json.dumps(report, indent=2))
    if report["cascade_risk"] == "HIGH":
        print(f"\n[CRITICAL] {report['cascade_note']}")
        print(f"  Ghost pattern: {report['ghost_pattern']}")
        print(f"  Share this fingerprint — if another agent matches, it's structural.")


COMMANDS = {
    "extract": cmd_extract,
    "compare": cmd_compare,
    "verify": cmd_verify,
    "ghost": cmd_ghost,
}

if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else None
    if cmd not in COMMANDS:
        print(f"Usage: commitment_verify.py [{'|'.join(COMMANDS)}] ...")
        sys.exit(1)
    COMMANDS[cmd](sys.argv[2:])
