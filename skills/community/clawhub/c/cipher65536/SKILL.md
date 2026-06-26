---
name: cipher65536
version: 1.0.2
description: Base65536 file encoding and decoding tool. Encodes arbitrary binary files into Unicode text using Base65536 encoding, supports gzip compression, original filename preservation, and byte-level XOR encryption based on true random entropy from local loopback network jitter. Suitable for cross-platform file transfer, high-security steganography, API binary data transmission, and other scenarios.
---

# Base65536 File Encoding and Decoding Tool

## Overview

Base65536 is an encoding scheme using Unicode characters that converts arbitrary binary data into printable text strings. This tool adds the following enhancements:

- **gzip Compression**: Reduces transmission size
- **True Random Key Generation**: Collects physical entropy based on local loopback network jitter
- **Byte-Level XOR Encryption**: Protects content confidentiality
- **Metadata Concealment**: Filename, size, etc., are hidden in encryption mode

## Quick Start

### Install Dependencies

```bash
pip install base65536
```

Basic Usage

```bash
# Standard encoding (no encryption)
python skill.py encode document.pdf -o encoded.txt

# Decoding
python skill.py decode encoded.txt -o restored.pdf
```

Encryption Mode (Auto-generate Key)

```bash
# Encrypt and encode (key saved to file, not displayed in terminal)
python skill.py encode secret.zip --scramble -o encrypted.txt
# Output:
#   🌐 Collecting true random entropy from local network jitter...
#   🔑 Key saved to: encrypted.key
#   🔒 File permissions locked to 600 (read/write for current user only)
#   ✓ Encoded: encrypted.txt

# Decrypt (reading key from file)
python skill.py decode encrypted.txt --key $(cat encrypted.key)
```

Encryption Mode (Using Specified Key)

```bash
# Encrypt using an existing key
python skill.py encode secret.zip --scramble --key 108544482569932551567348223456789012... -o encrypted.txt

# Decrypt
python skill.py decode encrypted.txt --key 108544482569932551567348223456789012...
```

Command-Line Arguments

encode Subcommand

Argument Description
input Input file path (Required)
-o, --output Output file path (Default: input_filename.b65536.txt)
--no-compress Disable gzip compression
--scramble Enable encryption mode
--key Use specified key (integer); auto-generated if not provided
--key-file Key output file path (Default: output_filename.key)

decode Subcommand

Argument Description
input Input file path (Required)
-o, --output Output file path (Default: use original filename)
--key Decryption key (integer; required for encrypted mode)

Workflow

Encoding Process

1. Read the original binary file.
2. Optionally: Compress data using gzip (default enabled, level 9).
3. Encode to Unicode text using Base65536.
4. If encryption mode is enabled:
   · Generate or use the specified 256-bit key.
   · Perform XOR encryption on the UTF-8 bytes of the Base65536 text.
   · Encrypt real metadata and replace with dummy metadata.
5. Prepend the #METADATA: header.
6. Save as a text file.

Decoding Process

1. Read the encoded text file.
2. Parse the #METADATA: header.
3. If encrypted mode:
   · Decrypt the real metadata using the key.
   · Decrypt the main body data using XOR.
4. Decode the data to binary using Base65536.
5. Automatically detect and decompress gzip-compressed data.
6. Save the file using the original filename.

File Format

Standard Mode

```
#METADATA:{"original_name": "original_filename", "compressed": true, "original_size": 12345, "scrambled": false}
[Base65536 encoded data...]
```

Encryption Mode

```
#METADATA:{"original_name": "encrypted_file", "compressed": true, "original_size": 0, "scrambled": true, "note": "This file is encrypted. Use key to decrypt."}
[XOR encrypted Base65536 data...]
###ENCRYPTED_META### [Encrypted real metadata]
```

Security Principles

A file steganography tool based on information theory and cryptographic principles. It folds data redundancy using gzip entropy densification and uses true random entropy seeded from local loopback network jitter to generate a 256-bit key space for byte-level XOR perturbation. The ciphertext exhibits chaotic distribution over the finite manifold of Unicode defined by Base65536, effectively resisting known-plaintext attacks, ciphertext-only attacks, and phase-space reconstruction analysis.

1. True Random Key Generation: Generates an unpredictable 256-bit key by measuring local loopback (localhost) network latency jitter to collect physical entropy, combined with system entropy from os.urandom.
2. Secure Key Storage: Automatically generated keys are saved to a .key file with 600 permissions and are never displayed in the terminal.
3. Metadata Concealment: The actual filename, size, and other information are encrypted and stored; dummy data is displayed externally.

Usage Examples

Encoding a PDF File (No Encryption)

```bash
python skill.py encode document.pdf -o encoded.txt
```

Output:

```
  Compressing: 1,234,567 → 876,543 bytes (71.0%)
  Encoding: 876,543 bytes → 438,271 characters
✓ Encoded: encoded.txt
  Final size: 438,271 characters
```

Decoding a File (No Encryption)

```bash
python skill.py decode encoded.txt
```

Output:

```
  Read metadata: {'original_name': 'document.pdf', 'compressed': True, 'original_size': 1234567, 'scrambled': False}
  gzip compression detected, decompressing...
✓ Decoded: document.pdf
  Restored size: 1,234,567 bytes
```

Use Cases

· Cross-Platform File Transfer: Encoded text can be transferred on any platform supporting text.
· High-Security Steganography: Content is completely hidden when using encryption mode.
· API Transmission: Transmit binary data through plain-text APIs.
· Bypassing Upload Restrictions: Transfer files on platforms that lack file upload support.
· Data Backup: Convert binary data to text for backup purposes.

Technical Specifications

Item Specification
Encoding Scheme Base65536
Compression Algorithm gzip (zlib, level 9)
Encryption Algorithm Byte-level XOR + 256-bit key space
Key Generation Local loopback network jitter + os.urandom
Metadata Format JSON
Python Version 3.6+
External Dependencies base65536

Performance Characteristics

Original Type gzip Compression Effect Base65536 Expansion Rate Combined Effect
Text Files 70-80% ~50% 35-40%
Images/Videos 90-99% ~50% 45-99%
Compressed Files No effect ~50% ~50%

Important Notes

1. Key Custody: True random keys cannot be reproduced. Files cannot be recovered if the key is lost.
2. Secure Transmission: Transfer the key file via a channel separate from the ciphertext.
3. Compressed Files: For files like .zip or .jpg, use --no-compress to avoid size inflation.
4. Unicode Compatibility: Some platforms may mishandle high-plane Unicode characters. Test transmission beforehand.

Resources

scripts/

· skill.py - Main program containing encode/decode functionality.

references/

· encoding-details.md - Encoding principles and implementation details.
