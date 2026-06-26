# Storage Keys Dictionary

The skill uses the following keys in `window.storage`:

| Key | Description | Scope |
|-----|-------------|-------|
| `enc-dek` | Encrypted Data Encryption Keys | Persistent |
| `enc-cfg` | Encryption Hierarchy Configuration | Persistent |
| `enc-kp-cfg` | Key Provider Configuration (Encrypted) | Persistent/Session |
| `audit` | Encrypted Audit Logs | Persistent |
| `data` | Encrypted Application Data | Persistent |

## Security Note
Sensitive configuration within `enc-kp-cfg` (like API keys) is encrypted with the Local Master Key before storage.
