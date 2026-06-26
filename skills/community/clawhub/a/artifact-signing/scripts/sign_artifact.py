import sys
import os
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization

def sign_artifact(artifact_path, key_path, output_path=None):
    """
    Signs an artifact using a private key.
    
    Args:
        artifact_path (str): Path to the artifact to sign.
        key_path (str): Path to the PEM-encoded private key.
        output_path (str, optional): Path to save the detached signature. 
                                     Defaults to artifact_path + ".sig".
    """
    if not os.path.exists(artifact_path):
        print(f"Error: Artifact not found at {artifact_path}")
        sys.exit(1)
        
    if not os.path.exists(key_path):
        print(f"Error: Private key not found at {key_path}")
        sys.exit(1)
        
    if output_path is None:
        output_path = artifact_path + ".sig"

    try:
        # Load the private key
        with open(key_path, "rb") as key_file:
            private_key = serialization.load_pem_private_key(
                key_file.read(),
                password=None, # Assuming no password for now
            )

        # Read the artifact
        with open(artifact_path, "rb") as f:
            data = f.read()

        # Sign the data
        signature = private_key.sign(
            data,
            padding.PKCS1v15(), # Traditional PKCS#1 v1.5 padding
            hashes.SHA256()
        )

        # Write the detached signature
        with open(output_path, "wb") as f:
            f.write(signature)

        print(f"Successfully signed {artifact_path}")
        print(f"Signature saved to {output_path}")

    except Exception as e:
        print(f"Error signing artifact: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python sign_artifact.py <artifact_path> <key_path> [output_path]")
        sys.exit(1)
    
    artifact = sys.argv[1]
    key = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) > 3 else None
    
    sign_artifact(artifact, key, output)
