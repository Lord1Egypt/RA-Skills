# Usage Examples for Artifact Signing Skill

Below are examples of how to use the Artifact Signing skill.

## 1. Generating a Key Pair (for testing)

If you don't have a private key, you can generate one using Python:

```python
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

# Generate private key
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
)

# Save private key to PEM
with open("private_key.pem", "wb") as f:
    f.write(private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    ))

# Save public key to PEM
with open("public_key.pem", "wb") as f:
    f.write(private_key.public_key().public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    ))
```

## 2. Signing an Artifact

Use the `sign_artifact.py` script to sign a file:

```powershell
python c:\Docs\skills\artifact-signing\scripts\sign_artifact.py "my_app.exe" "private_key.pem"
```

This will create `my_app.exe.sig` in the same directory.

## 3. Verifying the Signature

You can use this Python snippet to verify the signature:

```python
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization

# Load public key
with open("public_key.pem", "rb") as f:
    public_key = serialization.load_pem_public_key(f.read())

# Read artifact and signature
with open("my_app.exe", "rb") as f:
    data = f.read()
with open("my_app.exe.sig", "rb") as f:
    signature = f.read()

# Verify
try:
    public_key.verify(
        signature,
        data,
        padding.PKCS1v15(),
        hashes.SHA256()
    )
    print("Signature is valid!")
except Exception:
    print("Signature is INVALID!")
```
