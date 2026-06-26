---
name: file-hasher
description: Compute, verify, and compare file hashes using MD5, SHA-1, SHA-256, SHA-512, and more. Use when checking file integrity, verifying downloads against expected checksums, comparing files for equality, generating checksums for directories, hashing strings, or validating checksum files (sha256sum/md5sum format). Supports BSD and standard output formats, JSON output, multi-algorithm hashing, and recursive directory scanning. No external dependencies.
---

# File Hasher

Compute, verify, and compare file hashes. Supports all hashlib algorithms. Zero dependencies.

## Quick Start

```bash
# Hash a file (SHA-256)
python3 scripts/file_hasher.py hash myfile.txt

# Verify a download
python3 scripts/file_hasher.py verify image.iso -e abc123def456...

# Compare two files
python3 scripts/file_hasher.py compare file1.txt file2.txt
```

## Commands

### hash
Compute file hash with one or more algorithms:
```bash
python3 scripts/file_hasher.py hash file.txt                        # SHA-256
python3 scripts/file_hasher.py hash file.txt -a md5                 # MD5
python3 scripts/file_hasher.py hash file.txt -a md5,sha1,sha256     # Multiple
python3 scripts/file_hasher.py hash *.py --bsd                      # BSD format
python3 scripts/file_hasher.py hash data.bin --json                 # JSON output
```

### verify
Check a file against an expected hash:
```bash
python3 scripts/file_hasher.py verify image.iso -e <expected_hash>
python3 scripts/file_hasher.py verify file.tar.gz -e <hash> -a sha512
```

Exit code 0 = match, 1 = mismatch.

### check
Verify files from a checksum file (sha256sum/md5sum/BSD format):
```bash
python3 scripts/file_hasher.py check SHA256SUMS
python3 scripts/file_hasher.py check checksums.txt -a md5
```

Auto-detects algorithm from hash length and BSD format headers.

### compare
Compare two files by hash:
```bash
python3 scripts/file_hasher.py compare original.bin copy.bin
python3 scripts/file_hasher.py compare a.txt b.txt -a md5
```

### directory
Hash all files in a directory:
```bash
python3 scripts/file_hasher.py directory ./src                  # Top level
python3 scripts/file_hasher.py directory ./project -r           # Recursive
python3 scripts/file_hasher.py directory ./dist -r --bsd -a md5 # BSD + MD5
```

### string
Hash a text string directly:
```bash
python3 scripts/file_hasher.py string "hello world"
python3 scripts/file_hasher.py string "password" -a md5,sha256,sha512
```

### algorithms
List all available hash algorithms:
```bash
python3 scripts/file_hasher.py algorithms
```
