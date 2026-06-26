---

Cipher65536 Encryption Mode Details

1. Security Model Overview

The encryption mode (--scramble) of Cipher65536 is a steganographic and cryptographic file protection tool based on the principles of information theory. Its core design goal is to ensure that the ciphertext exhibits a uniform random distribution over the Unicode manifold, thereby resisting Known-Plaintext Attacks (KPA), Ciphertext-Only Attacks (COA), and Phase Space Reconstruction analysis.

This mode implements a Three-Layer Entropy Densification Architecture:

1. Data Folding: gzip compression eliminates redundant patterns in the plaintext.
2. Random Perturbation: Byte-level XOR encryption using a true random key.
3. Information Hiding: Real metadata (filename, size) is encrypted and replaced with fake data.

2. True Random Key Generation (Physical Entropy Source)

Unlike common tools that rely solely on pseudo-random number generators (PRNGs) seeded by system time, Cipher65536 collects physical entropy from local loopback network jitter.

Collection Mechanism

The tool establishes a TCP connection to 127.0.0.1 and measures the nanosecond-level latency variance (perf_counter_ns) of the TCP handshake and packet echo process.

1. Server Setup: Binds to ephemeral ports on localhost.
2. Jitter Sampling: Measures Δt of connect(), accept(), send(), and recv() loops.
3. Entropy Extraction: The least significant bits (LSBs) of these nanosecond timestamps are highly sensitive to CPU scheduling, interrupt handling, and bus contention, making them truly unpredictable physical noise.
4. Whitening: Collected entropy is hashed with SHA-256 (combining with os.urandom) to remove potential bias and create a uniformly distributed 256-bit seed.

Security Guarantee

· Non-reproducibility: The specific network jitter at the exact moment of encryption cannot be reproduced, even on the same machine.
· Key Space: 2^256 (approx. 1.15 * 10^77), making brute-force attacks computationally infeasible.
· Terminal Safety: The generated key is never printed to stdout/stderr. It is directly saved to a .key file with 600 permissions (owner read/write only) to prevent leakage via shell history or screen loggers.

3. Byte-Level XOR Perturbation

Encryption is performed using a symmetric XOR stream cipher with a keystream derived via SHAKE-256 (SHA-3 XOF) .

Process

1. Keystream Derivation: keystream = SHAKE-256(key_seed, length=len(plaintext))
2. Encryption: ciphertext = plaintext XOR keystream
3. Encoding: The XOR output (binary noise) is encoded with Base65536 for text-safe transmission.

Cryptographic Properties

· Semantic Security: Identical plaintext blocks produce different ciphertext due to the unique keystream for the entire file.
· Information-Theoretic Chaoticity: The gzip pre-compression increases entropy density. Even if an attacker knows the plaintext is English text, the XOR output combined with Base65536 encoding appears as uniformly distributed random Unicode characters.

4. Metadata Concealment and Forgery

In standard mode, metadata is exposed:

```json
# Standard Mode Header (Exposed)
#METADATA:{"original_name": "top_secret.pdf", "compressed": true, "original_size": 123456}
```

In encryption mode, this information is fully concealed.

Concealment Mechanism

1. Real Metadata Encryption: The actual JSON string is encrypted using a unique XOR keystream derived from the main key.
2. Base65536 Wrapping: The encrypted bytes are encoded to look like the rest of the ciphertext.
3. Fake Header: The public header is replaced with dummy data to mislead traffic analysis.

```json
# Encryption Mode Header (Dummy Data)
#METADATA:{"original_name": "encrypted_file", "compressed": true, "original_size": 0, "scrambled": true, "note": "This file is encrypted."}
```

Resilience

· Traffic Analysis Resistance: An observer monitoring the file size or transmission time cannot determine the true file type (e.g., whether it is a 1KB text file or a 1MB video) or its actual name.
· Tamper Detection: If the ciphertext or encrypted metadata is modified by even a single bit, the XOR decryption will result in invalid JSON or corrupt gzip headers, causing the decryption process to fail immediately with an explicit error, thereby preventing the acceptance of corrupted data.

5. Attack Resistance Matrix

Attack Vector Defense Mechanism
Known-Plaintext Attack True random key ensures each encryption session uses a different keystream.
Ciphertext-Only Attack gzip entropy densification + XOR produces uniformly distributed noise indistinguishable from random data.
Metadata Leakage Filename and size are encrypted and stored as binary noise.
Replay Attack Not applicable (tool encrypts files, not communication sessions).
Cold Boot / Memory Dump Key resides in process memory only briefly; key file permissions are locked.
Platform Filtering Ciphertext is valid Unicode, bypassing binary upload restrictions.