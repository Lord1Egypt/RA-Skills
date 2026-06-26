---
name: ftp-client
description: FTP/FTPS client skill. Connect to FTP servers and perform file operations (list, upload, download, delete, move, copy, mkdir, read). Supports FTP and FTPS (explicit/implicit TLS).
homepage: https://github.com/eraycc/ftp-client-skill
metadata:
  { "openclaw": { "emoji": "📂", "requires": { "bins": ["node"], "env": ["FTP_CONNECTION"] }, "primaryEnv": "FTP_CONNECTION" } }
---

# FTP Client

Full-featured FTP/FTPS client skill for OpenClaw. Connect to remote FTP servers and manage files directly.

## Environment Variable

Set `FTP_CONNECTION` in the OpenClaw skill management panel. Format (comma-separated, last 3 fields optional):

```
host:port,username,password,active/passive,ftp/ftps,explicit/implicit
```

**Examples:**
```
ftp.example.com:21,myuser,mypassword
ftp.example.com:21,myuser,mypassword,passive
ftp.example.com:990,myuser,mypassword,passive,ftps,implicit
```

**Field definitions:**
- Field 1 (required): `host:port` — FTP server address and port
- Field 2 (required): `username` — FTP login username
- Field 3 (required): `password` — FTP login password
- Field 4 (optional): `active` or `passive` — connection mode (default: `passive`)
- Field 5 (optional): `ftp` or `ftps` — protocol (default: `ftp`)
- Field 6 (optional): `explicit` or `implicit` — TLS mode for FTPS (default: not used; only meaningful when field 5 is `ftps`)

> **Note:** If your password contains commas, replace them with `%2C` (URL-encoded). The parser will decode it.

## List directory

```bash
node {baseDir}/scripts/list.mjs
node {baseDir}/scripts/list.mjs "/remote/path"
node {baseDir}/scripts/list.mjs "/" --long
```

Options:
- `--long` or `-l`: Show detailed file info (size, date, permissions)

## Download file

```bash
node {baseDir}/scripts/download.mjs "/remote/file.txt"
node {baseDir}/scripts/download.mjs "/remote/file.txt" --out "/local/path/file.txt"
node {baseDir}/scripts/download.mjs "/remote/dir" --dir
```

Options:
- `--out <path>` or `-o <path>`: Local destination path (default: temp directory)
- `--dir` or `-d`: Download entire directory recursively

## Upload file

```bash
node {baseDir}/scripts/upload.mjs "/local/file.txt"
node {baseDir}/scripts/upload.mjs "/local/file.txt" --to "/remote/path/file.txt"
node {baseDir}/scripts/upload.mjs "/local/dir" --dir --to "/remote/dir"
```

Options:
- `--to <path>` or `-t <path>`: Remote destination path (default: FTP root `/`)
- `--dir` or `-d`: Upload entire directory recursively

## Delete file or directory

```bash
node {baseDir}/scripts/delete.mjs "/remote/file.txt"
node {baseDir}/scripts/delete.mjs "/remote/dir" --dir
```

Options:
- `--dir` or `-d`: Remove directory recursively (including all contents)

## Move / Rename

```bash
node {baseDir}/scripts/move.mjs "/remote/old-name.txt" "/remote/new-name.txt"
node {baseDir}/scripts/move.mjs "/remote/file.txt" "/remote/subdir/file.txt"
```

## Copy file

```bash
node {baseDir}/scripts/copy.mjs "/remote/source.txt" "/remote/dest.txt"
```

> FTP protocol does not natively support copy. This downloads the file to a temp location and re-uploads it.

## Create directory

```bash
node {baseDir}/scripts/mkdir.mjs "/remote/new-dir"
node {baseDir}/scripts/mkdir.mjs "/remote/path/to/deep/dir"
```

Creates the directory and all intermediate directories as needed.

## Read file content

```bash
node {baseDir}/scripts/read.mjs "/remote/file.txt"
node {baseDir}/scripts/read.mjs "/remote/file.txt" --encoding utf8
```

Options:
- `--encoding <enc>`: File encoding (default: `utf8`). Supports: `utf8`, `ascii`, `latin1`, `base64`

## File info (size, date)

```bash
node {baseDir}/scripts/info.mjs "/remote/file.txt"
```

Returns file size and last modification date.

## Notes

- Requires `node` and uses the `basic-ftp` npm package (auto-installed via package.json).
- Set `FTP_CONNECTION` env var before use.
- Passive mode is recommended for most NAT/firewall scenarios.
- For FTPS, the skill supports both explicit (port 21 typical) and implicit (port 990 typical) TLS.
- Large file transfers show progress output.