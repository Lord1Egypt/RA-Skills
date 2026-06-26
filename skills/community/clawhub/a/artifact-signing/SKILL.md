---
name: artifact-signing
description: A skill to sign artifacts using a digital certificate and private key.
---

# Artifact Signing Skill

This skill allows an AI agent to sign files, binaries, or any artifact using a PEM-encoded private key. It generates a detached signature file.

## Dependencies

- Python 3.x
- `cryptography` library (`pip install cryptography`)

## Tools

### `sign_artifact`

Signs a given artifact with a private key.

**Arguments:**

- `artifact_path`: (Required) Absolute path to the file to be signed.
- `key_path`: (Required) Absolute path to the PEM-encoded private key.
- `output_path`: (Optional) Absolute path where the signature should be saved. Defaults to `<artifact_path>.sig`.

**Example Usage:**

```powershell
python c:\Docs\skills\artifact-signing\scripts\sign_artifact.py "C:\path\to\artifact.zip" "C:\path\to\private_key.pem"
```

## Security Considerations

- **Private Key Protection**: Never share your private key. Ensure the key file has restricted permissions.
- **Verification**: Always verify the signature using the corresponding public key before trusting an artifact.
