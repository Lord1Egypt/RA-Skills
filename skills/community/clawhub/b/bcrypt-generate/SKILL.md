---
name: bcrypt-generate
description: Hash passwords using bcrypt or verify a password against a bcrypt hash. Use when the user asks to bcrypt a password, generate a bcrypt hash, check if a password matches a hash, or store a password securely.
metadata: {"openclaw":{"requires":{"bins":["python3"]}}}
---

# Bcrypt Generate

Hash passwords with bcrypt or verify existing hashes using Python's `bcrypt` library.

## Input

**For hashing:**
- Password string to hash
- Cost/rounds (default: 10, range: 4–31)

**For verification:**
- Password string
- Existing bcrypt hash string (starts with `$2b$` or `$2a$`)

## Output
- Bcrypt hash string (for hashing mode)
- True/False result (for verification mode)

## Instructions

1. Determine mode: hash a new password, or verify against an existing hash.

2. **Hashing a password:**
   ```
   python3 -c "import bcrypt; print(bcrypt.hashpw(b'PASSWORD', bcrypt.gensalt(rounds=ROUNDS)).decode())"
   ```
   Replace `PASSWORD` with the actual password and `ROUNDS` with the cost factor (default 10).

3. **Verifying a password against a hash:**
   ```
   python3 -c "import bcrypt; print(bcrypt.checkpw(b'PASSWORD', b'HASH'))"
   ```
   Replace `PASSWORD` and `HASH` with the actual values.

4. Check if `bcrypt` Python package is available before running:
   ```
   python3 -c "import bcrypt" 2>&1
   ```
   If it fails with `ModuleNotFoundError`, tell the user:
   > "This skill requires the Python `bcrypt` package. Install with: `pip3 install bcrypt`."

5. If `python3` is not found at all, tell the user:
   > "This skill requires `python3`. Install with: `brew install python3` (macOS) or `sudo apt install python3` (Linux)."

6. Present the hash output on its own line. For verification, report clearly: "Password MATCHES the hash" or "Password does NOT match the hash."

## Examples

**Hash password "mysecret" with cost 10:**
**Command:** `python3 -c "import bcrypt; print(bcrypt.hashpw(b'mysecret', bcrypt.gensalt(rounds=10)).decode())"`
**Output:** `$2b$10$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW`

**Hash password "admin" with cost 12:**
**Command:** `python3 -c "import bcrypt; print(bcrypt.hashpw(b'admin', bcrypt.gensalt(rounds=12)).decode())"`
**Output:** `$2b$12$...` (60-char bcrypt hash)

**Verify "mysecret" against `$2b$10$abc...`:**
**Command:** `python3 -c "import bcrypt; print(bcrypt.checkpw(b'mysecret', b'\$2b\$10\$abc...'))"`
**Output:** `True`

## Error Handling

- `python3` not found → tell user to install Python 3
- `bcrypt` module not found → tell user to run `pip3 install bcrypt`
- Password contains single quotes → escape them or note that the command must be adjusted; prefer using a temp Python script file for complex passwords
- Hash string malformed (does not start with `$2b$` or `$2a$`) → warn the user the hash appears invalid before running
- High cost factor (>= 14) → warn the user this will be slow (intentional for security)
