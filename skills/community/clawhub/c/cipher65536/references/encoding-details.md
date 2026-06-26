Base65536 Encoding Principles Explained

What is Base65536

Base65536 is an encoding scheme based on Unicode characters, using characters from the Private Use Area (PUA) ranging from U+10000 to U+1FFFF, totaling 65,536 distinct characters.

Encoding Principle

Each Base65536 character represents 16 bits (2 bytes) of data:

· Raw Data: Binary byte stream
· Encoding Process: Every 2 bytes → 1 Base65536 character
· Theoretical Expansion Rate: 50% (2 bytes → 1 character, but Unicode characters occupy more space in UTF-16/UTF-32)

In practical use, due to UTF-8 encoding:

· Characters within ASCII range: 1 byte
· Other Unicode characters: 3-4 bytes (UTF-8)
· Average expansion rate: approximately 50-60%

Comparison with Base64

Feature Base64 Base65536
Character Set A-Za-z0-9+/ U+10000-U+1FFFF
Bits per Character 6 bit 16 bit
Expansion Rate 133% ~50%
Readability Largely unreadable Many special characters
Compatibility Universal Some systems may not support

gzip Compression

When to Use Compression

· Text Files: Significant compression effect (70-80%)
· JSON/XML: Significant compression effect
· Source Code: Good compression effect
· Already Compressed Files: Not recommended to re-compress
· Images/Videos: Limited compression effect

Compression Level

gzip supports compression levels 1-9:

· 1: Fastest, lowest compression ratio
· 9: Slowest, highest compression ratio
· Level 9 is used by default for optimal compression

Compression Detection

Automatically detects gzip format during decoding:

```python
if data[:2] == b'\x1f\x8b':  # gzip magic number
    data = gzip.decompress(data)
```

Metadata Format

```json
{
    "original_name": "original_filename",
    "compressed": true/false,
    "original_size": 12345
}
```

Stored on the first line of the file: #METADATA:{...}

Purpose of Metadata

1. Preserve Original Filename: Automatically restore during decoding
2. Mark Compression Status: Determine whether to decompress during decoding
3. Record Original Size: Used for integrity verification

Implementation Notes

1. Encoding Boundaries

Base65536 encodes in units of 2 bytes:

· If data length is odd, the final byte requires special handling
· Padding or adjustment before encoding is recommended

2. Unicode Issues

Certain Unicode characters may cause problems in specific environments:

· Control Characters: Should be avoided
· Zero-Width Characters: May cause text processing issues
· Surrogate Pairs: Some languages may mishandle them

3. File Size Limitations

· Individual files recommended not to exceed 100MB
· Large files may require longer processing times
· Be mindful of memory usage

Testing and Verification

Round-trip consistency test:

```bash
# Encode
python skill.py encode input.zip -o output.txt

# Decode
python skill.py decode output.txt -o restored.zip

# Verify
sha256sum input.zip restored.zip
# Both SHA256 hashes should be identical
```

Frequently Asked Questions

Q: Encoded text displays abnormally on some platforms?

A: This may be a text rendering issue with the platform. Base65536 uses legal Unicode characters; if a platform does not support them, they may appear as boxes or be skipped. It is recommended to use platforms with full Unicode support.

Q: Why did my text file become larger after encoding?

A: Text files are already near optimal encoding; further compression might increase the size. For plain text, it is recommended to disable compression (--no-compress).

Q: What should I do if decoding fails?

A: Check the following:

1. File integrity (may have been corrupted during transmission)
2. Correct parameters were used during encoding
3. Metadata header is intact
4. Base65536 library version consistency
5. Key correctness