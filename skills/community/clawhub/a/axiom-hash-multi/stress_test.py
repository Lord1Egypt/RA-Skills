"""
🧪 STRESS TEST SUITE — axiom-hash-multi v1.0.0
================================================

But: trouver les faiblesses du skill avant publication Capafy.

Couvre 8 groupes de tests :
A. Empty / Minimal inputs
B. Encoding edge cases
C. Binary edge cases
D. Large files
E. Special files
F. CLI edge cases
G. Performance benchmarks
H. Cross-validation (vs system tools)
"""

import hashlib
import json
import os
import shutil
import statistics
import subprocess
import sys
import tempfile
import time
import unicodedata
from pathlib import Path

# Importer le skill
sys.path.insert(0, str(Path(__file__).parent))
from axiom_hash_multi import (
    SUPPORTED_ALGORITHMS,
    hash_all,
    hash_bytes,
    hash_file,
    hash_file_all,
)

# Compteurs
results = {
    "pass": 0,
    "fail": 0,
    "warn": 0,
    "issues": [],
    "improvements": [],
}

def report(category, name, passed, note=""):
    """Enregistre un résultat de test."""
    icon = "✅" if passed else "❌"
    if not passed and note:
        results["fail"] += 1
        results["issues"].append({"category": category, "name": name, "note": note})
    elif passed:
        results["pass"] += 1
    print(f"  {icon} [{category}] {name} {('— ' + note) if note else ''}")
    return passed


# ============================================================================
# GROUPE A — Empty / Minimal inputs
# ============================================================================
print("\n" + "=" * 70)
print("  GROUPE A — Empty / Minimal inputs")
print("=" * 70)

# A1: Empty bytes
expected_sha256_empty = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
got = hash_bytes(b"", "sha256")
report("A", "empty bytes SHA-256", got == expected_sha256_empty,
       f"got={got[:16]}..." if got != expected_sha256_empty else "")

# A2: Single byte
got = hash_bytes(b"a", "sha256")
expected = hashlib.sha256(b"a").hexdigest()
report("A", "single byte 'a'", got == expected)

# A3: Single null byte
got = hash_bytes(b"\x00", "sha256")
expected = hashlib.sha256(b"\x00").hexdigest()
report("A", "single null byte", got == expected)

# A4: Whitespace only
got = hash_bytes(b"   \t\n  ", "sha256")
expected = hashlib.sha256(b"   \t\n  ").hexdigest()
report("A", "whitespace only", got == expected)

# A5: Newline only
got = hash_bytes(b"\n", "sha256")
expected = hashlib.sha256(b"\n").hexdigest()
report("A", "newline only", got == expected)


# ============================================================================
# GROUPE B — Encoding edge cases
# ============================================================================
print("\n" + "=" * 70)
print("  GROUPE B — Encoding edge cases")
print("=" * 70)

# B1: UTF-8 with BOM
bom_data = b"\xef\xbb\xbfHello World"
got = hash_bytes(bom_data, "sha256")
expected = hashlib.sha256(bom_data).hexdigest()
report("B", "UTF-8 with BOM", got == expected)

# B2: UTF-16-LE
utf16le = "Hello".encode("utf-16-le")
got = hash_bytes(utf16le, "sha256")
expected = hashlib.sha256(utf16le).hexdigest()
report("B", "UTF-16-LE encoded", got == expected)

# B3: UTF-16-BE
utf16be = "Hello".encode("utf-16-be")
got = hash_bytes(utf16be, "sha256")
expected = hashlib.sha256(utf16be).hexdigest()
report("B", "UTF-16-BE encoded", got == expected)

# B4: Latin-1
latin1 = "café".encode("latin-1")
got = hash_bytes(latin1, "sha256")
expected = hashlib.sha256(latin1).hexdigest()
report("B", "Latin-1 encoded", got == expected)

# B5: Emoji simple
emoji_data = "🐺".encode("utf-8")
got = hash_bytes(emoji_data, "sha256")
expected = hashlib.sha256(emoji_data).hexdigest()
report("B", "single emoji 🐺", got == expected)

# B6: ZWJ sequence (family emoji)
zwj_data = "👨‍👩‍👧‍👦".encode("utf-8")
got = hash_bytes(zwj_data, "sha256")
expected = hashlib.sha256(zwj_data).hexdigest()
report("B", "ZWJ family emoji", got == expected)

# B7: Combining characters (e.g., 'é' = 'e' + combining acute)
combined = "é"  # = "e" + "\u0301" (combining acute)
precomposed = "é"  # single codepoint
got_combined = hash_bytes(combined.encode("utf-8"), "sha256")
got_precomposed = hash_bytes(precomposed.encode("utf-8"), "sha256")
report("B", "precomposed vs combining char differs",
       got_combined != got_precomposed,
       f"⚠️ Unicode normalization not applied (this is correct for a hash, but note it)")

# B8: RTL Arabic
rtl = "مرحبا بالعالم".encode("utf-8")
got = hash_bytes(rtl, "sha256")
expected = hashlib.sha256(rtl).hexdigest()
report("B", "RTL Arabic", got == expected)

# B9: Zero-width characters
zwc = "ab\u200bcd\u200cef".encode("utf-8")  # zero-width space + zero-width non-joiner
got = hash_bytes(zwc, "sha256")
expected = hashlib.sha256(zwc).hexdigest()
report("B", "zero-width characters", got == expected)


# ============================================================================
# GROUPE C — Binary edge cases
# ============================================================================
print("\n" + "=" * 70)
print("  GROUPE C — Binary edge cases")
print("=" * 70)

# C1: All zeros (1KB)
zeros = b"\x00" * 1024
got = hash_bytes(zeros, "sha256")
expected = hashlib.sha256(zeros).hexdigest()
report("C", "1KB all zeros", got == expected)

# C2: All 0xFF (1KB)
ones = b"\xff" * 1024
got = hash_bytes(ones, "sha256")
expected = hashlib.sha256(ones).hexdigest()
report("C", "1KB all 0xFF", got == expected)

# C3: All possible bytes (256 bytes)
all_bytes = bytes(range(256))
got = hash_bytes(all_bytes, "sha256")
expected = hashlib.sha256(all_bytes).hexdigest()
report("C", "256 bytes (all possible values)", got == expected)

# C4: Long sequence of single byte
long_single = b"a" * 1_000_000
got = hash_bytes(long_single, "sha256")
expected = hashlib.sha256(long_single).hexdigest()
report("C", "1MB of 'a'", got == expected)


# ============================================================================
# GROUPE D — Large files
# ============================================================================
print("\n" + "=" * 70)
print("  GROUPE D — Large files")
print("=" * 70)

tmpdir = Path(tempfile.mkdtemp(prefix="axiom_stress_"))

# D1: 1 MB
f1mb = tmpdir / "test_1mb.bin"
f1mb.write_bytes(os.urandom(1024 * 1024))
t0 = time.perf_counter()
got = hash_file(f1mb, "sha256")
elapsed = (time.perf_counter() - t0) * 1000
expected = hashlib.sha256(f1mb.read_bytes()).hexdigest()
report("D", f"1MB random file ({elapsed:.1f}ms)", got == expected)

# D2: 10 MB
f10mb = tmpdir / "test_10mb.bin"
f10mb.write_bytes(os.urandom(10 * 1024 * 1024))
t0 = time.perf_counter()
got = hash_file(f10mb, "sha256")
elapsed = (time.perf_counter() - t0) * 1000
report("D", f"10MB random file ({elapsed:.1f}ms, must be <100ms)", elapsed < 100,
       f"❌ TOO SLOW: {elapsed:.1f}ms" if elapsed >= 100 else f"✅ {elapsed:.1f}ms")

# D3: hash_file_all on 10MB (efficiency test: should be ~5x of single algo)
f10mb = tmpdir / "test_10mb_all.bin"
f10mb.write_bytes(os.urandom(10 * 1024 * 1024))
t0 = time.perf_counter()
results_all = hash_file_all(f10mb)
elapsed_all = (time.perf_counter() - t0) * 1000
t0 = time.perf_counter()
sha256_only = hash_file(f10mb, "sha256")
elapsed_sha = (time.perf_counter() - t0) * 1000
report("D", f"10MB all 5 algos ({elapsed_all:.1f}ms vs sha256 alone {elapsed_sha:.1f}ms)",
       # All-5 should be <3x of single (not 5x, because of single-pass streaming)
       elapsed_all < elapsed_sha * 3,
       f"ratio={elapsed_all/elapsed_sha:.2f}x")


# ============================================================================
# GROUPE E — Special files
# ============================================================================
print("\n" + "=" * 70)
print("  GROUPE E — Special files")
print("=" * 70)

# E1: /dev/null
if Path("/dev/null").exists():
    try:
        got = hash_file("/dev/null", "sha256")
        expected = hashlib.sha256(b"").hexdigest()
        report("E", "/dev/null (empty file hash)", got == expected,
               f"got={got[:16]}..." if got != expected else "")
    except Exception as e:
        report("E", "/dev/null", False, f"exception: {e}")
else:
    report("E", "/dev/null", True, "(skipped, not available)")

# E2: /dev/urandom (read first 4KB only)
if Path("/dev/urandom").exists():
    try:
        # Manually read 4KB and hash
        with open("/dev/urandom", "rb") as f:
            data = f.read(4096)
        # Now write to file and hash
        urand_file = tmpdir / "urandom_4k.bin"
        urand_file.write_bytes(data)
        got = hash_file(urand_file, "sha256")
        expected = hashlib.sha256(data).hexdigest()
        report("E", "/dev/urandom sample (4KB)", got == expected)
    except Exception as e:
        report("E", "/dev/urandom", False, f"exception: {e}")
else:
    report("E", "/dev/urandom", True, "(skipped, not available)")

# E3: Symlinks
symlink_path = tmpdir / "symlink_to_1mb"
try:
    symlink_path.symlink_to(f1mb)
    got_via_symlink = hash_file(symlink_path, "sha256")
    got_direct = hash_file(f1mb, "sha256")
    report("E", "symlink to file (follows by default)", got_via_symlink == got_direct)
except Exception as e:
    report("E", "symlink", False, f"exception: {e}")

# E4: Broken symlink
broken_link = tmpdir / "broken_link"
try:
    broken_link.symlink_to("/nonexistent/file_xyz")
    try:
        hash_file(broken_link, "sha256")
        report("E", "broken symlink rejected", False, "should have raised")
    except FileNotFoundError:
        report("E", "broken symlink rejected", True)
except Exception as e:
    report("E", "broken symlink setup", False, f"exception: {e}")


# ============================================================================
# GROUPE F — CLI edge cases
# ============================================================================
print("\n" + "=" * 70)
print("  GROUPE F — CLI edge cases")
print("=" * 70)

# F1: --algo invalid
result = subprocess.run(
    [sys.executable, "axiom_hash_multi.py", f1mb.name, "--algo", "sha999"],
    capture_output=True, text=True, cwd=Path(__file__).parent
)
report("F", "invalid --algo (sha999)", result.returncode == 1)

# F2: --all with file
result = subprocess.run(
    [sys.executable, "axiom_hash_multi.py", f1mb.name, "--all"],
    capture_output=True, text=True, cwd=Path(__file__).parent
)
lines = result.stdout.strip().split("\n")
report("F", "--all returns 5 lines", len(lines) == 5, f"got {len(lines)} lines")

# F3: --string with empty
result = subprocess.run(
    [sys.executable, "axiom_hash_multi.py", "", "--string"],
    capture_output=True, text=True, cwd=Path(__file__).parent
)
expected = hashlib.sha256(b"").hexdigest()
got = result.stdout.strip()
report("F", "empty --string", got == expected, f"got={got[:16]}..." if got != expected else "")

# F4: --string with unicode
result = subprocess.run(
    [sys.executable, "axiom_hash_multi.py", "🐺", "--string"],
    capture_output=True, text=True, cwd=Path(__file__).parent
)
got = result.stdout.strip()
expected = hashlib.sha256("🐺".encode("utf-8")).hexdigest()
report("F", "--string with emoji", got == expected, f"got={got[:16]}..." if got != expected else "")

# F5: stdin with no data
result = subprocess.run(
    [sys.executable, "axiom_hash_multi.py", "--stdin", "--algo", "sha256"],
    input="", capture_output=True, text=True, cwd=Path(__file__).parent
)
got = result.stdout.strip()
expected = hashlib.sha256(b"").hexdigest()
report("F", "stdin with no data", got == expected)

# F6: file doesn't exist
result = subprocess.run(
    [sys.executable, "axiom_hash_multi.py", "/tmp/this_does_not_exist_xyz.txt"],
    capture_output=True, text=True, cwd=Path(__file__).parent
)
report("F", "nonexistent file rejected", result.returncode == 1)

# F7: input is a directory
result = subprocess.run(
    [sys.executable, "axiom_hash_multi.py", str(tmpdir)],
    capture_output=True, text=True, cwd=Path(__file__).parent
)
report("F", "directory rejected", result.returncode == 1)


# ============================================================================
# GROUPE G — Performance benchmarks
# ============================================================================
print("\n" + "=" * 70)
print("  GROUPE G — Performance benchmarks")
print("=" * 70)

# G1: Speed of each algo on 10MB
perf_results = {}
for algo in SUPPORTED_ALGORITHMS:
    times = []
    for _ in range(5):
        t0 = time.perf_counter()
        hash_file(f10mb, algo)
        times.append((time.perf_counter() - t0) * 1000)
    perf_results[algo] = {
        "median_ms": statistics.median(times),
        "min_ms": min(times),
        "max_ms": max(times),
    }
    print(f"  📊 {algo:8s}: median={perf_results[algo]['median_ms']:.1f}ms  min={perf_results[algo]['min_ms']:.1f}ms  max={perf_results[algo]['max_ms']:.1f}ms")

# G2: All under 100ms p95?
all_under_100 = all(p["max_ms"] < 100 for p in perf_results.values())
report("G", "all algos under 100ms p95 (10MB)", all_under_100)


# ============================================================================
# GROUPE H — Cross-validation (vs system tools)
# ============================================================================
print("\n" + "=" * 70)
print("  GROUPE H — Cross-validation vs system tools")
print("=" * 70)

# H1: Compare with sha256sum
sha256sum_result = subprocess.run(
    ["sha256sum", str(f1mb)], capture_output=True, text=True
)
if sha256sum_result.returncode == 0:
    sha256sum_digest = sha256sum_result.stdout.split()[0]
    our_digest = hash_file(f1mb, "sha256")
    report("H", "SHA-256 vs sha256sum (system tool)", our_digest == sha256sum_digest,
           f"ours={our_digest[:16]}... sys={sha256sum_digest[:16]}..." if our_digest != sha256sum_digest else "")
else:
    report("H", "sha256sum not available", True, "(skipped)")

# H2: Compare with md5sum
md5sum_result = subprocess.run(
    ["md5sum", str(f1mb)], capture_output=True, text=True
)
if md5sum_result.returncode == 0:
    md5sum_digest = md5sum_result.stdout.split()[0]
    our_digest = hash_file(f1mb, "md5")
    report("H", "MD5 vs md5sum (system tool)", our_digest == md5sum_digest,
           f"ours={our_digest[:16]}... sys={md5sum_digest[:16]}..." if our_digest != md5sum_digest else "")
else:
    report("H", "md5sum not available", True, "(skipped)")

# H3: Compare with openssl sha512
openssl_result = subprocess.run(
    ["openssl", "dgst", "-sha512", str(f1mb)], capture_output=True, text=True
)
if openssl_result.returncode == 0:
    openssl_digest = openssl_result.stdout.split("= ")[1].strip()
    our_digest = hash_file(f1mb, "sha512")
    report("H", "SHA-512 vs openssl dgst", our_digest == openssl_digest,
           f"ours={our_digest[:16]}... sys={openssl_digest[:16]}..." if our_digest != openssl_digest else "")
else:
    report("H", "openssl not available", True, "(skipped)")


# ============================================================================
# GROUPE I — Discovery of improvement opportunities
# ============================================================================
print("\n" + "=" * 70)
print("  GROUPE I — Découverte d'opportunités d'amélioration")
print("=" * 70)

# I1: Detect if hash_bytes is missing a "string auto-encode" feature
# Currently: hash_bytes("foo") → TypeError
# Opportunity: hash_bytes(b"foo") or hash_bytes("foo") auto-encode
try:
    hash_bytes("not bytes", "sha256")
    report("I", "auto-encode str input", True, "(already works)")
except TypeError:
    report("I", "auto-encode str input", False, "OPPORTUNITY: could auto-encode str to UTF-8")
    results["improvements"].append({
        "title": "Auto-encode str input",
        "detail": "hash_bytes('foo') currently fails with TypeError. Could auto-encode to UTF-8 for ergonomics.",
        "priority": "LOW"
    })

# I2: hash_file could support symlink following option
# Currently: follows symlinks (open() default)
# Opportunity: --no-follow-symlinks flag
report("I", "symlink follow control (--no-follow)", False,
       "OPPORTUNITY: no way to NOT follow symlinks (could break in some scenarios)")
results["improvements"].append({
    "title": "--no-follow-symlinks flag",
    "detail": "Currently always follows symlinks. Add --no-follow for paranoid mode.",
    "priority": "LOW"
})

# I3: --json output mode
report("I", "JSON output mode", False,
       "OPPORTUNITY: --json output for programmatic parsing")
results["improvements"].append({
    "title": "--json output mode",
    "detail": "Currently only 'algo  hash' or 'hash' format. --json would ease integration.",
    "priority": "MEDIUM"
})

# I4: --compare mode
report("I", "compare to expected hash", False,
       "OPPORTUNITY: --compare or --verify to check against expected hash")
results["improvements"].append({
    "title": "--compare=<expected_hash>",
    "detail": "Currently returns hash, user must compare manually. Add built-in compare.",
    "priority": "HIGH"
})

# I5: Progress bar for large files
report("I", "progress bar for large files", False,
       "OPPORTUNITY: --progress flag for files >100MB (currently silent)")
results["improvements"].append({
    "title": "Progress bar for large files",
    "detail": "For files >100MB, silent hashing feels broken. Add --progress.",
    "priority": "MEDIUM"
})

# I6: Base64 output format
report("I", "base64 output format", False,
       "OPPORTUNITY: --base64 output (shorter than hex for binary)")
results["improvements"].append({
    "title": "--base64 output",
    "detail": "Some contexts prefer base64 (e.g., JWT signatures, URLs).",
    "priority": "LOW"
})

# I7: Read MANIFEST.txt and verify
report("I", "manifest verification mode", False,
       "OPPORTUNITY: --verify-manifest <file.txt> to read a MANIFEST and verify all entries")
results["improvements"].append({
    "title": "--verify-manifest mode",
    "detail": "Read a MANIFEST.txt and verify all hashes. Great for backups.",
    "priority": "HIGH"
})

# I8: CHUNK_SIZE could be tunable
report("I", "tunable CHUNK_SIZE", False,
       "OPPORTUNITY: --chunk-size <KB> for tuning on different storage types (SSD vs HDD vs NFS)")
results["improvements"].append({
    "title": "Tunable CHUNK_SIZE",
    "detail": "64KB is good default but could be tuned for SSD (1MB) vs HDD (64KB) vs network.",
    "priority": "LOW"
})


# ============================================================================
# RAPPORT FINAL
# ============================================================================
print("\n" + "=" * 70)
print("  📊 RAPPORT FINAL — STRESS TEST axiom-hash-multi v1.0.0")
print("=" * 70)
print()
print(f"  ✅ Tests pass:    {results['pass']}")
print(f"  ❌ Tests fail:    {results['fail']}")
print(f"  📈 Améliorations:  {len(results['improvements'])} opportunités identifiées")
print()

if results["issues"]:
    print("  ── ISSUES TROUVÉES ──")
    for issue in results["issues"]:
        print(f"  ❌ [{issue['category']}] {issue['name']}: {issue['note']}")
    print()

if results["improvements"]:
    print("  ── OPPORTUNITÉS D'AMÉLIORATION ──")
    # Trier par priorité
    prio_order = {"HIGH": 0, "MEDIUM": 1, "LOW": 2}
    sorted_imp = sorted(results["improvements"], key=lambda x: prio_order.get(x["priority"], 99))
    for imp in sorted_imp:
        icon = {"HIGH": "🔥", "MEDIUM": "🟡", "LOW": "🟢"}[imp["priority"]]
        print(f"  {icon} [{imp['priority']}] {imp['title']}")
        print(f"      {imp['detail']}")
    print()

# Cleanup
shutil.rmtree(tmpdir, ignore_errors=True)

# Exit code: 0 si pass=ok, 1 si fail>0
if results["fail"] > 0:
    sys.exit(1)
sys.exit(0)
