import os
import json
import base64
import argparse
import getpass
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.argon2 import Argon2id

def derive_key(password, salt):
    kdf = Argon2id(
        salt=salt,
        length=32,
        iterations=1,
        lanes=4,
        memory_cost=64 * 1024,
        ad=None,
        secret=None,
    )
    return kdf.derive(password.encode())

def encrypt_data(data, password):
    salt = os.urandom(16)
    key = derive_key(password, salt)
    aesgcm = AESGCM(key)
    nonce = os.urandom(12)
    encrypted_data = aesgcm.encrypt(nonce, data.encode(), None)
    return base64.b64encode(salt + nonce + encrypted_data).decode()

def decrypt_data(encrypted_blob, password):
    try:
        decoded_blob = base64.b64decode(encrypted_blob)
        salt = decoded_blob[:16]
        nonce = decoded_blob[16:28]
        ciphertext = decoded_blob[28:]
        key = derive_key(password, salt)
        aesgcm = AESGCM(key)
        decrypted_data = aesgcm.decrypt(nonce, ciphertext, None)
        return decrypted_data.decode()
    except Exception as e:
        raise ValueError("Decryption failed. Incorrect password or corrupted data.") from e

def save_encrypted_backup(json_data, output_path, password):
    json_str = json.dumps(json_data, ensure_ascii=False)
    encrypted_str = encrypt_data(json_str, password)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(encrypted_str)
    print(f"Encrypted backup saved to: {output_path}")

def load_encrypted_backup(input_path, password):
    with open(input_path, "r", encoding="utf-8") as f:
        encrypted_str = f.read()
    json_str = decrypt_data(encrypted_str, password)
    return json.loads(json_str)

if __name__ == "__main__":
    # Test Block
    pass
