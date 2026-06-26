# Backend Storage Schema

In the Node.js version, the service expects a storage mechanism to handle the following keys. By default, it uses `.anydef-vault.json` in the current working directory.

| Key | Description | Type |
|-----|-------------|------|
| `enc-vault-salt` | Base64 encoded salt for PBKDF2 derivation. | String |
| `enc-kek-wrapped` | The KEK wrapped by the Master Key (IV:Cipher:Tag). | String |
| `enc-dek-{scope}` | The DEK for a specific scope wrapped by KEK. | String |

## Security Policy
The storage file itself contains only encrypted blobs and public salts. Without the user-provided passphrase, the data is cryptographically useless.
