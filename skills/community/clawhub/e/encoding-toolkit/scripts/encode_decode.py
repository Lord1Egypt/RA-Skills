#!/usr/bin/env python3
"""Multi-format encoder/decoder: Base64, URL, HTML, Hex, ROT13, and more."""

import argparse
import base64
import hashlib
import html
import sys
import urllib.parse


ENCODINGS = {
    "base64": "Base64 encode/decode",
    "base64url": "Base64 URL-safe encode/decode",
    "base32": "Base32 encode/decode",
    "hex": "Hexadecimal encode/decode",
    "url": "URL percent-encoding encode/decode",
    "html": "HTML entity encode/decode",
    "rot13": "ROT13 encode/decode (symmetric)",
    "binary": "Binary (8-bit) encode/decode",
    "ascii85": "ASCII85 / Base85 encode/decode",
}

HASH_ALGORITHMS = {
    "md5": "MD5 hash (128-bit)",
    "sha1": "SHA-1 hash (160-bit)",
    "sha256": "SHA-256 hash (256-bit)",
    "sha512": "SHA-512 hash (512-bit)",
    "sha3-256": "SHA3-256 hash (256-bit)",
}


def encode(data: str, encoding: str) -> str:
    """Encode data using the specified encoding."""
    raw = data.encode("utf-8")

    if encoding == "base64":
        return base64.b64encode(raw).decode("ascii")
    elif encoding == "base64url":
        return base64.urlsafe_b64encode(raw).decode("ascii").rstrip("=")
    elif encoding == "base32":
        return base64.b32encode(raw).decode("ascii")
    elif encoding == "hex":
        return raw.hex()
    elif encoding == "url":
        return urllib.parse.quote(data, safe="")
    elif encoding == "html":
        return html.escape(data, quote=True)
    elif encoding == "rot13":
        import codecs
        return codecs.encode(data, "rot_13")
    elif encoding == "binary":
        return " ".join(format(b, "08b") for b in raw)
    elif encoding == "ascii85":
        return base64.a85encode(raw).decode("ascii")
    else:
        raise ValueError(f"Unknown encoding: {encoding}")


def decode(data: str, encoding: str) -> str:
    """Decode data using the specified encoding."""
    if encoding == "base64":
        # Add padding if needed
        padding = 4 - len(data) % 4
        if padding != 4:
            data += "=" * padding
        return base64.b64decode(data).decode("utf-8", errors="replace")
    elif encoding == "base64url":
        padding = 4 - len(data) % 4
        if padding != 4:
            data += "=" * padding
        return base64.urlsafe_b64decode(data).decode("utf-8", errors="replace")
    elif encoding == "base32":
        padding = 8 - len(data) % 8
        if padding != 8:
            data += "=" * padding
        return base64.b32decode(data.upper()).decode("utf-8", errors="replace")
    elif encoding == "hex":
        data = data.replace(" ", "").replace("0x", "").replace(",", "")
        return bytes.fromhex(data).decode("utf-8", errors="replace")
    elif encoding == "url":
        return urllib.parse.unquote(data)
    elif encoding == "html":
        return html.unescape(data)
    elif encoding == "rot13":
        import codecs
        return codecs.decode(data, "rot_13")
    elif encoding == "binary":
        bits = data.replace(" ", "")
        if len(bits) % 8 != 0:
            raise ValueError("Binary string length must be a multiple of 8")
        chars = [chr(int(bits[i:i+8], 2)) for i in range(0, len(bits), 8)]
        return "".join(chars)
    elif encoding == "ascii85":
        return base64.a85decode(data).decode("utf-8", errors="replace")
    else:
        raise ValueError(f"Unknown encoding: {encoding}")


def compute_hash(data: str, algorithm: str) -> str:
    """Compute a hash of the input data."""
    raw = data.encode("utf-8")
    if algorithm == "md5":
        return hashlib.md5(raw).hexdigest()
    elif algorithm == "sha1":
        return hashlib.sha1(raw).hexdigest()
    elif algorithm == "sha256":
        return hashlib.sha256(raw).hexdigest()
    elif algorithm == "sha512":
        return hashlib.sha512(raw).hexdigest()
    elif algorithm == "sha3-256":
        return hashlib.sha3_256(raw).hexdigest()
    else:
        raise ValueError(f"Unknown hash algorithm: {algorithm}")


def detect_encoding(data: str) -> list[str]:
    """Try to detect the encoding of input data."""
    guesses = []
    # Check base64
    import re
    if re.match(r'^[A-Za-z0-9+/=]+$', data) and len(data) % 4 == 0 and len(data) >= 4:
        guesses.append("base64")
    if re.match(r'^[A-Za-z0-9_-]+={0,2}$', data) and len(data) >= 4:
        guesses.append("base64url")
    # Check hex
    clean = data.replace(" ", "").replace("0x", "").replace(",", "")
    if re.match(r'^[0-9a-fA-F]+$', clean) and len(clean) % 2 == 0 and len(clean) >= 2:
        guesses.append("hex")
    # Check URL encoding
    if "%" in data and re.search(r'%[0-9a-fA-F]{2}', data):
        guesses.append("url")
    # Check HTML entities
    if "&" in data and (";" in data) and re.search(r'&[#\w]+;', data):
        guesses.append("html")
    # Check binary
    clean_bin = data.replace(" ", "")
    if re.match(r'^[01]+$', clean_bin) and len(clean_bin) % 8 == 0 and len(clean_bin) >= 8:
        guesses.append("binary")
    # Check base32
    if re.match(r'^[A-Z2-7=]+$', data) and len(data) >= 8:
        guesses.append("base32")
    return guesses


def main():
    parser = argparse.ArgumentParser(
        description="Multi-format encoder/decoder and hasher",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Supported encodings: " + ", ".join(ENCODINGS.keys()) + "\n"
               "Supported hashes: " + ", ".join(HASH_ALGORITHMS.keys()) + "\n\n"
               "Examples:\n"
               "  encode base64 \"Hello World\"\n"
               "  decode base64 \"SGVsbG8gV29ybGQ=\"\n"
               "  encode url \"hello world & goodbye\"\n"
               "  decode hex \"48656c6c6f\"\n"
               "  hash sha256 \"my secret\"\n"
               "  detect \"SGVsbG8gV29ybGQ=\"\n",
    )

    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    # Encode
    enc_parser = subparsers.add_parser("encode", help="Encode data")
    enc_parser.add_argument("encoding", choices=ENCODINGS.keys(), help="Encoding format")
    enc_parser.add_argument("data", nargs="?", help="Data to encode")
    enc_parser.add_argument("--stdin", action="store_true", help="Read from stdin")
    enc_parser.add_argument("--file", help="Read from file")

    # Decode
    dec_parser = subparsers.add_parser("decode", help="Decode data")
    dec_parser.add_argument("encoding", choices=ENCODINGS.keys(), help="Encoding format")
    dec_parser.add_argument("data", nargs="?", help="Data to decode")
    dec_parser.add_argument("--stdin", action="store_true", help="Read from stdin")
    dec_parser.add_argument("--file", help="Read from file")

    # Hash
    hash_parser = subparsers.add_parser("hash", help="Hash data")
    hash_parser.add_argument("algorithm", choices=HASH_ALGORITHMS.keys(), help="Hash algorithm")
    hash_parser.add_argument("data", nargs="?", help="Data to hash")
    hash_parser.add_argument("--stdin", action="store_true", help="Read from stdin")
    hash_parser.add_argument("--file", help="Read from file")
    hash_parser.add_argument("--all", action="store_true", help="Show all hash algorithms")

    # Detect
    det_parser = subparsers.add_parser("detect", help="Detect encoding of data")
    det_parser.add_argument("data", nargs="?", help="Data to analyze")
    det_parser.add_argument("--stdin", action="store_true", help="Read from stdin")

    # List
    subparsers.add_parser("list", help="List supported encodings and hashes")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    if args.command == "list":
        print("Supported encodings:")
        for name, desc in ENCODINGS.items():
            print(f"  {name:<12} {desc}")
        print()
        print("Supported hash algorithms:")
        for name, desc in HASH_ALGORITHMS.items():
            print(f"  {name:<12} {desc}")
        sys.exit(0)

    # Get input data
    if args.command in ("encode", "decode", "hash", "detect"):
        if getattr(args, "stdin", False):
            data = sys.stdin.read().rstrip("\n")
        elif getattr(args, "file", None):
            try:
                with open(args.file) as f:
                    data = f.read().rstrip("\n")
            except FileNotFoundError:
                print(f"Error: File not found: {args.file}", file=sys.stderr)
                sys.exit(1)
        elif args.data:
            data = args.data
        else:
            parser.print_help()
            sys.exit(1)

    try:
        if args.command == "encode":
            print(encode(data, args.encoding))
        elif args.command == "decode":
            print(decode(data, args.encoding))
        elif args.command == "hash":
            if getattr(args, "all", False):
                for alg in HASH_ALGORITHMS:
                    print(f"{alg:<12} {compute_hash(data, alg)}")
            else:
                print(compute_hash(data, args.algorithm))
        elif args.command == "detect":
            guesses = detect_encoding(data)
            if guesses:
                print("Detected possible encodings:")
                for g in guesses:
                    try:
                        decoded = decode(data, g)
                        preview = decoded[:80] + ("..." if len(decoded) > 80 else "")
                        print(f"  {g:<12} → {preview}")
                    except Exception:
                        print(f"  {g:<12} → (decode failed)")
            else:
                print("Could not detect encoding. Data may be plain text.")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
