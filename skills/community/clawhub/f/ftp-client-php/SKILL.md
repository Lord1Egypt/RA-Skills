---
name: ftp-client-php
description: FTP/FTPS file manager via PHP proxy. Supports list, upload, download, delete, move, copy, mkdir, read, write. Works behind NAT/firewalls (e.g. HuggingFace) by routing FTP operations through an HTTP PHP proxy.
homepage: https://github.com/eraycc/ftp-client-skill/tree/main/ftp-client-php
metadata:
  { "openclaw": { "emoji": "📂", "requires": { "bins": ["node"], "env": ["FTP_PHP_CONFIG"] }, "primaryEnv": "FTP_PHP_CONFIG" } }
---

# FTP Client (PHP Proxy)

Full-featured FTP/FTPS client skill for OpenClaw. Routes all FTP operations through an HTTP PHP proxy server, so it works even when direct FTP connections are blocked (e.g. HuggingFace Spaces, serverless environments). [Click to deploy ftp-php-proxy](https://github.com/eraycc/ftp-client-skill/tree/main/ftp-proxy-php).

## Architecture

```
OpenClaw ──HTTP──▶ PHP Proxy Server (api.php) ──FTP──▶ FTP Server
```

## Environment Variable

Set `FTP_PHP_CONFIG` in the OpenClaw skill management panel. **JSON format**:

```json
{"ftp_php_domain":"https://your-server.com/api.php","ftp_php_apikey":"","ftp_client_host":"ftp.example.com","ftp_client_port":"21","ftp_client_username":"user","ftp_client_password":"pass","ftp_client_connect_mode":"passive","ftp_client_protocol":"ftps","ftp_client_encrypt_mode":"explicit"}
```

**Field definitions:**

- `ftp_php_domain` (required): Full URL of the PHP proxy api.php endpoint
- `ftp_php_apikey` (optional): API key for the PHP proxy, empty string = no auth
- `ftp_client_host` (required): FTP server hostname
- `ftp_client_port` (optional): FTP server port, default `21`
- `ftp_client_username` (required): FTP login username
- `ftp_client_password` (required): FTP login password
- `ftp_client_connect_mode` (optional): `active` or `passive`, default `passive`
- `ftp_client_protocol` (optional): `ftp` or `ftps`, default `ftp`
- `ftp_client_encrypt_mode` (optional): `explicit` or `implicit`, only meaningful when protocol is `ftps`

**Example (alwaysdata FTPS):**
```json
{"ftp_php_domain":"https://your-server.com/api.php","ftp_php_apikey":"","ftp_client_host":"ftp.example.com","ftp_client_port":"21","ftp_client_username":"user","ftp_client_password":"pass","ftp_client_connect_mode":"passive","ftp_client_protocol":"ftps","ftp_client_encrypt_mode":"explicit"}
```

## List directory

```bash
node {baseDir}/scripts/list.mjs
node {baseDir}/scripts/list.mjs "/remote/path"
node {baseDir}/scripts/list.mjs "/" --detailed
```

Options:
- `--detailed` or `-l`: Show detailed file info (size, date, permissions, type)

## Download file

```bash
node {baseDir}/scripts/download.mjs "/remote/file.txt"
node {baseDir}/scripts/download.mjs "/remote/file.txt" --out "/local/save/path.txt"
```

Options:
- `--out <path>` or `-o <path>`: Local save path (default: system temp directory)

## Upload file

```bash
node {baseDir}/scripts/upload.mjs "/local/file.txt" --to "/remote/path/file.txt"
```

Options:
- `--to <path>` or `-t <path>`: Remote destination path (required)

## Write text content to remote file

```bash
node {baseDir}/scripts/write.mjs "/remote/file.txt" "file content here"
node {baseDir}/scripts/write.mjs "/remote/file.txt" --stdin < local_file.txt
```

## Read file content

```bash
node {baseDir}/scripts/read.mjs "/remote/file.txt"
```

## Delete file or directory

```bash
node {baseDir}/scripts/delete.mjs "/remote/file.txt"
node {baseDir}/scripts/delete.mjs "/remote/dir" --dir
```

Options:
- `--dir` or `-d`: Remove directory recursively

## Move / Rename

```bash
node {baseDir}/scripts/move.mjs "/remote/old.txt" "/remote/new.txt"
```

## Copy file

```bash
node {baseDir}/scripts/copy.mjs "/remote/source.txt" "/remote/dest.txt"
```

## Create directory

```bash
node {baseDir}/scripts/mkdir.mjs "/remote/new-dir"
```

## File info

```bash
node {baseDir}/scripts/info.mjs "/remote/file.txt"
```

## Notes

- All FTP operations are proxied through your PHP server via HTTP.
- Upload works by sending file as base64 to the PHP proxy.
- Download retrieves base64 content from the PHP proxy and saves locally.
- Large files are supported but limited by PHP server's `upload_max_filesize` and `memory_limit`.
- Set `FTP_PHP_CONFIG` env var as a single-line JSON string.
