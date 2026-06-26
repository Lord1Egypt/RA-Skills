#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BioLIMS Password Encryption Script
Generates AES-CBC encrypted password for login API
"""
import sys
import os
import json
import time
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

# Encryption parameters - Replace with actual values before use
AES_KEY = os.environ.get("BIOLIMS_AES_KEY", "0000000000000000").encode('utf-8')
AES_IV = os.environ.get("BIOLIMS_AES_IV", "0000000000000000").encode('utf-8')
SECRET_KEY = os.environ.get("BIOLIMS_SECRET", "demo")


def encrypt_password(password):
    """
    Encrypt password using AES-CBC

    Args:
        password: Plain text password

    Returns:
        Base64-encoded encrypted string
    """
    # Build data structure for encryption
    data = {
        "password": password,
        "captCode": "",
        "time": int(time.time() * 1000),  # Millisecond timestamp
        "secretKey": SECRET_KEY
    }

    # Convert to JSON string
    plaintext = json.dumps(data)

    # AES-CBC encryption
    cipher = AES.new(AES_KEY, AES.MODE_CBC, AES_IV)
    encrypted = cipher.encrypt(pad(plaintext.encode('utf-8'), AES.block_size))

    # Base64 encoding
    return base64.b64encode(encrypted).decode('utf-8')


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('{"error":"Usage: encrypt_password.py <password>"}', file=sys.stderr)
        sys.exit(1)

    password = sys.argv[1]
    encrypted = encrypt_password(password)
    print(encrypted)
