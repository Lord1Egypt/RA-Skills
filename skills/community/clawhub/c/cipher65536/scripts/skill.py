#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Base65536 File Encoding/Decoding Tool
Encodes arbitrary files into Unicode text using Base65536 encoding, supports gzip compression,
original filename preservation, and byte-level XOR encryption based on true random keys
derived from local network jitter. Hides real metadata in encryption mode.

Installation:
    pip install base65536

Usage:
    # Standard encoding (no encryption, plaintext metadata)
    python skill.py encode <input_file> [-o <output_file>] [--no-compress]

    # Encrypted encoding (true random key + XOR encryption, hidden metadata)
    python skill.py encode <input_file> --scramble [-o <output_file>] [--key-file <key_file>]

    # Encrypted encoding (using specified key)
    python skill.py encode <input_file> --scramble --key <key_integer> [-o <output_file>]

    # Decoding (if file is encrypted, key is required)
    python skill.py decode <input_file> --key <key_integer> [-o <output_file>]

Note:
    - Auto-generated keys in encryption mode are saved to a file and never displayed in the terminal.
    - Key file permissions are automatically locked to 600 (owner read/write only).
    - Keys are derived from local loopback network jitter measurements and are non-reproducible; store them securely.

Author: TurinFohlem
Version: 3.0.3
"""

import argparse
import gzip
import base65536
import os
import json
import hashlib
import time
import socket
import stat

# ============================================================
# Cryptographically Secure Keystream Derivation
# ============================================================
def secure_keystream(seed: int, length: int) -> bytes:
    """Derives a pseudo-random byte stream from an integer seed (SHAKE-256)."""
    seed_bytes = seed.to_bytes(32, 'big')
    return hashlib.shake_256(seed_bytes).digest(length)

# ============================================================
# True Random Key Generator (Local Loopback Network Jitter Entropy Source)
# ============================================================
def get_true_jitter() -> bytes:
    """Measures real localhost TCP jitter, fixing deadlock: server must echo data."""
    entropy = b""
    
    for port in range(54321, 54326):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(('127.0.0.1', port))
        server.listen(1)
        
        for _ in range(20):
            try:
                t1 = time.perf_counter_ns()
                client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client.connect(('127.0.0.1', port))
                t2 = time.perf_counter_ns()
                
                conn, _ = server.accept()
                t3 = time.perf_counter_ns()
                
                # Measure round trip: client sends, server echoes
                client.send(b'X')
                data = conn.recv(1)
                if data == b'X':          # Verify correct echo
                    conn.send(b'X')       # Critical fix: server must send packet back
                t4 = time.perf_counter_ns()
                
                # Client receives echo (completes one full round trip)
                client.recv(1)
                t5 = time.perf_counter_ns()
                
                entropy += (t2 - t1).to_bytes(8, 'little')
                entropy += (t3 - t2).to_bytes(8, 'little')
                entropy += (t4 - t3).to_bytes(8, 'little')
                entropy += (t5 - t4).to_bytes(8, 'little')
                
                client.close()
                conn.close()
                
            except Exception:
                # Silent failure, continue collecting entropy (avoid hanging)
                pass
        
        server.close()
    
    entropy += os.urandom(32)
    return hashlib.sha256(entropy).digest()

def generate_true_random_key() -> int:
    """Generates a 256-bit true random key."""
    seed_bytes = get_true_jitter()
    return int.from_bytes(seed_bytes, byteorder='big')

# ============================================================
# Secure Key Output
# ============================================================
def output_key(key_int: int, output_path: str = None):
    if output_path is None:
        output_path = "cipher65536.key"
    
    if os.path.exists(output_path):
        base, ext = os.path.splitext(output_path)
        counter = 1
        while os.path.exists(f"{base}_{counter}{ext}"):
            counter += 1
        output_path = f"{base}_{counter}{ext}"
        print(f"  ⚠️  Key file already exists, saving as: {output_path}")
    
    with open(output_path, "w") as f:
        f.write(f"# cipher65536 encryption key\n")
        f.write(f"# Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"# Keep this file secure.\n")
        f.write(f"{key_int}\n")
    
    try:
        os.chmod(output_path, stat.S_IRUSR | stat.S_IWUSR)
        perm_locked = True
    except Exception:
        perm_locked = False
    
    print(f"  🔑 Key saved to: {output_path}")
    if perm_locked:
        print(f"  🔒 File permissions 600 (owner read/write only)")

# ============================================================
# XOR Encryption/Decryption Core
# ============================================================
def xor_bytes(data: bytes, seed: int) -> bytes:
    keystream = secure_keystream(seed, len(data))
    return bytes(a ^ b for a, b in zip(data, keystream))

def encrypt_body(text: str, seed: int) -> str:
    data_bytes = text.encode('utf-8')
    encrypted_bytes = xor_bytes(data_bytes, seed)
    return base65536.encode(encrypted_bytes)

def decrypt_body(encrypted_b65536: str, seed: int) -> str:
    encrypted_bytes = base65536.decode(encrypted_b65536)
    decrypted_bytes = xor_bytes(encrypted_bytes, seed)
    return decrypted_bytes.decode('utf-8')

# ============================================================
# Main Program
# ============================================================
def main():
    parser = argparse.ArgumentParser(description="Base65536 Encoding/Decoding Tool (True Random Key Edition)")
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    encode_parser = subparsers.add_parser("encode", help="Encode file")
    encode_parser.add_argument("input", help="Input file path")
    encode_parser.add_argument("-o", "--output", help="Output file path")
    encode_parser.add_argument("--no-compress", action="store_true", help="Do not compress")
    encode_parser.add_argument("--scramble", action="store_true", help="True random key + XOR encryption and hide metadata")
    encode_parser.add_argument("--key", help="Specify key integer (auto-generated if not provided)")
    encode_parser.add_argument("--key-file", help="Key output file path")
    
    decode_parser = subparsers.add_parser("decode", help="Decode file")
    decode_parser.add_argument("input", help="Input file path")
    decode_parser.add_argument("-o", "--output", help="Output file path")
    decode_parser.add_argument("--key", help="Decryption key integer (required for encrypted mode)")
    
    args = parser.parse_args()
    
    if args.command == "encode":
        with open(args.input, "rb") as f:
            data = f.read()
        
        original_size = len(data)
        original_name = os.path.basename(args.input)
        
        compressed_flag = not args.no_compress
        if compressed_flag:
            compressed_data = gzip.compress(data, compresslevel=9)
            print(f"  Compressing: {original_size} → {len(compressed_data)} bytes ({len(compressed_data)/original_size*100:.1f}%)")
        else:
            compressed_data = data
        
        b65536_text = base65536.encode(compressed_data)
        print(f"  Encoding: {len(compressed_data)} bytes → {len(b65536_text)} characters")
        
        real_metadata = {
            "original_name": original_name,
            "compressed": compressed_flag,
            "original_size": original_size
        }
        
        if args.scramble:
            # Key handling
            if args.key:
                key_int = int(args.key)
                print(f"  🔑 Using user-specified key")
            else:
                print("  🌐 Collecting true random entropy from local network jitter...")
                key_int = generate_true_random_key()
                if args.key_file:
                    key_output = args.key_file
                else:
                    base = os.path.splitext(args.output or original_name)[0]
                    key_output = base + ".key"
                output_key(key_int, key_output)
            
            # Encrypt body
            encrypted_body = encrypt_body(b65536_text, key_int)
            
            # Encrypt real metadata
            real_meta_json = json.dumps(real_metadata).encode('utf-8')
            meta_key_bytes = secure_keystream(key_int, len(real_meta_json))
            encrypted_meta = bytes([a ^ b for a, b in zip(real_meta_json, meta_key_bytes)])
            encrypted_meta_b65536 = base65536.encode(encrypted_meta)
            
            # Fake metadata (placed in header)
            fake_metadata = {
                "original_name": "encrypted_file",
                "compressed": True,
                "original_size": 0,
                "scrambled": True,
                "note": "This file is encrypted. Use key to decrypt."
            }
            metadata_line = f"#METADATA:{json.dumps(fake_metadata)}\n"
            
            final_text = metadata_line + encrypted_body + "\n###ENCRYPTED_META###" + encrypted_meta_b65536
        else:
            real_metadata["scrambled"] = False
            metadata_line = f"#METADATA:{json.dumps(real_metadata)}\n"
            final_text = metadata_line + b65536_text
        
        output = args.output or original_name + ".b65536.txt"
        with open(output, "w", encoding="utf-8") as f:
            f.write(final_text)
        
        print(f"✓ Encoded: {output}")
        if args.scramble and not args.key:
            print(f"  ⚠️  Key not displayed in terminal. Retrieve from key file.")
        print(f"  Final size: {len(final_text)} characters")
    
    elif args.command == "decode":
        with open(args.input, "r", encoding="utf-8") as f:
            content = f.read()
        
        if "\n" in content:
            first_line, rest = content.split("\n", 1)
        else:
            first_line, rest = content, ""
        
        metadata = None
        if first_line.startswith("#METADATA:"):
            try:
                metadata = json.loads(first_line[10:])
                print(f"  Read metadata: {metadata}")
            except:
                print("  Warning: Metadata corrupted, attempting direct decode")
        
        is_scrambled = metadata.get("scrambled", False) if metadata else False
        
        if is_scrambled:
            if not args.key:
                print("❌ Error: This file is encrypted. Provide --key to decrypt.")
                return
            try:
                key_int = int(args.key)
            except ValueError:
                print("❌ Error: Key must be an integer.")
                return
            
            print(f"  Decrypting with key...")
            
            if "###ENCRYPTED_META###" in rest:
                encrypted_body, encrypted_meta_b65536 = rest.split("###ENCRYPTED_META###", 1)
                encrypted_body = encrypted_body.rstrip("\n")
            else:
                print("❌ Error: Encrypted file format incorrect. Missing encrypted metadata.")
                return
            
            # Decrypt real metadata
            encrypted_meta = base65536.decode(encrypted_meta_b65536.strip())
            # Fix: Use actual length of encrypted metadata
            meta_key_bytes = secure_keystream(key_int, len(encrypted_meta))
            real_meta_json_bytes = bytes([a ^ b for a, b in zip(encrypted_meta, meta_key_bytes)])
            try:
                real_metadata = json.loads(real_meta_json_bytes.decode('utf-8'))
                print(f"  Decrypted metadata: {real_metadata}")
            except:
                print("❌ Error: Incorrect key or file corruption. Cannot decrypt metadata.")
                return
            
            b65536_text = decrypt_body(encrypted_body, key_int)
        else:
            real_metadata = metadata
            b65536_text = rest
        
        data = base65536.decode(b65536_text.strip())
        
        if real_metadata and real_metadata.get("compressed", False):
            if data[:2] == b'\x1f\x8b':
                print("  gzip compression detected, decompressing...")
                data = gzip.decompress(data)
            else:
                print("  Warning: Metadata marked as compressed but data is not in gzip format. Attempting direct restoration.")
        
        if args.output:
            output = args.output
        else:
            output = real_metadata.get("original_name", "restored_file") if real_metadata else "restored_file"
            if os.path.exists(output):
                base, ext = os.path.splitext(output)
                output = f"{base}_restored{ext}"
                print(f"  File already exists, renaming to: {output}")
        
        with open(output, "wb") as f:
            f.write(data)
        
        print(f"✓ Decoded: {output}")
        print(f"  Restored size: {len(data)} bytes")

if __name__ == "__main__":
    main()