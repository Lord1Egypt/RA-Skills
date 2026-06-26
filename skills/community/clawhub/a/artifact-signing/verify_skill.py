from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
import os
import subprocess

def test_signing_flow():
    # 1. Generate test keys
    print("Generating test keys...")
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    )
    public_pem = private_key.public_key().public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    
    with open("test_private.pem", "wb") as f: f.write(private_pem)
    with open("test_public.pem", "wb") as f: f.write(public_pem)
    
    # 2. Create a dummy artifact
    print("Creating dummy artifact...")
    artifact_content = b"This is a test artifact for signing."
    with open("test_artifact.txt", "wb") as f: f.write(artifact_content)
    
    # 3. Use the sign_artifact.py script
    print("Running sign_artifact.py...")
    script_path = os.path.join("scripts", "sign_artifact.py")
    result = subprocess.run(
        ["python", script_path, "test_artifact.txt", "test_private.pem"],
        capture_output=True, text=True
    )
    print(result.stdout)
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
        return False
    
    # 4. Verify the signature
    print("Verifying signature...")
    with open("test_artifact.txt.sig", "rb") as f:
        signature = f.read()
    
    try:
        public_key = serialization.load_pem_public_key(public_pem)
        public_key.verify(
            signature,
            artifact_content,
            padding.PKCS1v15(),
            hashes.SHA256()
        )
        print("VERIFICATION SUCCESSFUL: Signature is valid!")
        return True
    except Exception as e:
        print(f"VERIFICATION FAILED: {e}")
        return False
    finally:
        # Cleanup
        for f in ["test_private.pem", "test_public.pem", "test_artifact.txt", "test_artifact.txt.sig"]:
            if os.path.exists(f): os.remove(f)

if __name__ == "__main__":
    test_signing_flow()
