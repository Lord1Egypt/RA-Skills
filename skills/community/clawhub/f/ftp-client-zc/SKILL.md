# FTP Client Skill (ZC)

**Skill ID**: `ftp-client-zc`

**Description**: Provides basic FTP operations (list, upload, download, delete, rename) for a configured FTP server. All operations are performed via the Node.js `basic-ftp` library. Credentials are obtained from OpenClaw's secret store (key `ftp-client-zc/cred`) or, as a fallback, from a local `creds.json` file (which is excluded from publishing).

## Parameters
| Action | Required args | Optional args | Description |
|--------|----------------|---------------|-------------|
| `list` | `host` (or use stored) | `path` (remote directory, default `/`) | List files/directories in the given remote path.
| `upload` | `localPath`, `remotePath` | `host` | Upload a local file (or directory) to the FTP server.
| `download` | `remotePath`, `localPath` | `host` | Download a remote file (or directory) to local filesystem.
| `delete` | `remotePath` | `host` | Delete a remote file or empty directory.
| `rename` | `oldPath`, `newPath` | `host` | Rename or move a remote file/directory.

If `host`, `user`, and `password` are omitted, the skill will first try to read them from the OpenClaw secret `ftp-client-zc/cred`; if not found, it falls back to the local `creds.json` (which should not be published).

## Usage Examples
```
# List root directory (uses stored credentials)
openclaw skill run ftp-client-zc list

# Upload a file, overriding host
openclaw skill run ftp-client-zc upload --host 47.119.167.86 --user test --password zhangchong --localPath "C:\path\file.txt" --remotePath "/uploads/file.txt"
```

## Security
- Credentials are never logged.
- All network actions require explicit user approval via `/approve` before execution.
- When using the local `creds.json` fallback, ensure the file is protected by filesystem permissions and is excluded from the published npm package via `.npmignore`.

---
*Created by 张小龙🦞*