---
name: curl-tool
description: Transfer data using HTTP, HTTPS, FTP protocols. Test APIs and download files.
---

# Curl Tool - Data Transfer

Transfer data with HTTP/HTTPS/FTP. Supports custom headers and auth.

## Quick Start

```bash
curl-tool https://api.example.com/data
```

## Features

- GET and POST requests
- Custom headers
- Auth support
- File downloads
- Follow redirects

## Examples

```bash
curl-tool https://api.example.com/users
curl-tool -X POST -d '{"name":"test"}' https://api.example.com
curl-tool -o out.txt https://example.com/file
```

## See Also

- Related documentation: `man curl` (if available)
