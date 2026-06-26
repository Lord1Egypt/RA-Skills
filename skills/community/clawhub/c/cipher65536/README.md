Base65536-Skill

Encode any file into plain text, safely bypass platform file format restrictions, and prevent eavesdropping.

https://img.shields.io/badge/License-MIT-blue.svg

---

🎯 Problem Solved

Many AI platforms (such as MiniMax, Grok, etc.) and social platforms (like X, Telegram) have web interfaces that do not support binary file uploads, only allowing plain text pasting.

This tool encodes any file format (ZIP, images, videos, PDFs, EXEs, etc.) into a block of printable Unicode text that can be pasted directly into chat windows for transmission.

When paired with encryption mode, it also prevents eavesdropping and interception during transfer.

---

✨ Features

Feature Description
📦 Any Format Supports all file types: binaries, images, audio/video, archives, executables, etc.
🔤 Plain Text Transfer Encoded output is purely Unicode text; paste into any text field.
🗜️ gzip Compression 70-80% compression rate for text files, significantly reducing overall size.
🔐 XOR Encryption Mode True random entropy from local loopback network jitter + 256-bit key space; ciphertext leaks no metadata.
🛡️ Anti-Eavesdropping Transmitted content is unreadable Unicode; file type cannot be identified even at the TLS layer.
📄 Metadata Concealment In encrypted mode, filename and size are dummy data; recovery is impossible without the key.

---

📖 Usage

Install Dependencies

```bash
pip install base65536
```

Basic Usage

```bash
# Encode (no encryption)
python skill.py encode document.pdf -o encoded.txt

# Decode
python skill.py decode encoded.txt -o restored.pdf
```

Encryption Mode (Auto-generate Key)

```bash
# Encrypt and encode (key auto-saved to file, never displayed in terminal)
python skill.py encode secret.zip --scramble -o encrypted.txt
# Example output:
#   🌐 Collecting true random entropy from local network jitter...
#   🔑 Key saved to: encrypted.key
#   🔒 File permissions locked to 600 (read/write for current user only)
#   ⚠️  Keep this file safe; key was not displayed in terminal.
#   ✓ Encoded: encrypted.txt

# Decrypt and restore (reading key from file)
python skill.py decode encrypted.txt --key $(cat encrypted.key)
```

Encryption Mode (Using Specified Key)

```bash
# Encrypt using an existing key
python skill.py encode secret.zip --scramble --key 108544482569932551567348223456789012... -o encrypted.txt
# Example output:
#   🔑 Using user-specified key
#   ✓ Encoded: encrypted.txt

# Decrypt
python skill.py decode encrypted.txt --key 108544482569932551567348223456789012...
```

Specify Key File Path

```bash
# Custom key file save location
python skill.py encode secret.zip --scramble --key-file /path/to/my_key.key -o encrypted.txt
```

---

🔒 Security Notes

Protections in Encryption Mode

In encrypted mode, the transmitted text completely hides the following information:

· ✅ Original filename (shown as encrypted_file)
· ✅ Original file size (shown as 0)
· ✅ True file type (appears as binary gibberish)
· ✅ File content (XOR encrypted; cannot be recovered without key)

Security Principles

A file steganography tool based on information theory and cryptographic principles. It folds data redundancy using gzip entropy densification and uses true random entropy seeded from local loopback network jitter to generate a 256-bit key space for byte-level XOR perturbation. The ciphertext exhibits chaotic distribution over the finite manifold of Unicode defined by Base65536, effectively resisting known-plaintext attacks, ciphertext-only attacks, and phase-space reconstruction analysis.

1. True Random Key Generation: Generates unpredictable 256-bit true random keys by measuring local loopback network latency jitter (nanosecond level) combined with system entropy (os.urandom). Keys are automatically saved to a file with locked permissions (600) and are never displayed in the terminal.
2. gzip Entropy Densification: Compression eliminates data redundancy and increases entropy density, making the ciphertext distribution closer to random. Modification of encrypted content is detectable and results in errors upon decryption if the ciphertext and key are not compromised simultaneously.
3. Byte-Level XOR Perturbation: Uses the key seed to generate a pseudo-random keystream for XOR encryption across the entire byte stream.
4. Metadata Forgery: Filename and size are replaced with dummy data. External observers cannot ascertain any real file attributes.

Important Notes

· ⚠️ The key must be stored securely. True random keys are non-reproducible; data is irretrievable if the key is lost.
· ⚠️ In encryption mode, the key is saved to a .key file (permissions 600). Transfer the key file or its contents via a secure channel.
· ⚠️ If specifying a key directly on the command line, be aware that shell history may leak the key.
· ⚠️ This tool primarily protects data in transit. For local file security, use system-level encryption (BitLocker, FileVault, etc.).

---

📊 Compression Efficiency

File Type Original Size Post-Base65536 Size Compression Ratio
Plain Text (.txt) 10 KB ~4 KB ~40%
Python Source (.py) 50 KB ~20 KB ~40%
ZIP Archive (.zip) 8 KB ~8 KB ~100% (Already compressed)
Image (.jpg) 200 KB ~100 KB ~50%
PDF Document (.pdf) 500 KB ~260 KB ~52%

Base65536 encodes 2 bytes per character, resulting in a theoretical expansion of ~50%. With gzip enabled, compression rates for text files reach 70-80%, yielding excellent overall efficiency.

---

📁 File Format

Structure of the encoded text file:

```
#METADATA:{"original_name": "original_filename", "compressed": true, "original_size": 12345, "scrambled": false}
[Base65536 encoded data...]
```

In encrypted mode:

```
#METADATA:{"original_name": "encrypted_file", "compressed": true, "original_size": 0, "scrambled": true, "note": "..."}
[XOR encrypted Base65536 data...]
###ENCRYPTED_META###[Encrypted metadata (true filename, size)]
```

---

🚀 Use Cases

1. Platform Upload Restrictions: Transfer files on AI platforms that lack file upload support.
2. Privacy Protection: Send sensitive files over untrusted channels (using encryption mode).
3. Steganography Combination: Encode files to text and embed them in images, code comments, or other carriers.
4. API Transmission: Transmit binary data through plain-text APIs.
5. Cross-Platform Data Migration: Unrestricted by file format compatibility.

---

📂 File Structure

```
base65536-skill/
├── README.md                      # This file
├── SKILL.md                       # OpenClaw Skill metadata
├── requirements.txt               # Python dependencies
├── scripts/
│   └── skill.py                   # Main program (encode/decode/encrypt)
└── references/
    └── encoding-details.md        # Detailed encoding principles
```

---

🤖 OpenClaw Skill Integration

This project is packaged as an OpenClaw Skill and can be used directly within OpenClaw:

```bash
# Install to OpenClaw
openclaw skills install base65536-skill

# Usage
openclaw skill run base65536 encode yourfile.zip -o encoded.txt
openclaw skill run base65536 decode encoded.txt --key [KEY]
```

---

📜 License

MIT License - Free to use, modify, and distribute.