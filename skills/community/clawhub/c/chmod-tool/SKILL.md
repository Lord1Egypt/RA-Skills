---
name: chmod-tool
description: Change file permissions using symbolic or numeric modes.
---

# Chmod Tool - File Permissions

Modify file read/write/execute permissions with symbolic or octal modes.

## Quick Start

```bash
chmod-tool +x script.sh
```

## Features

- Symbolic mode (u+x, g-w)
- Octal mode (755, 644)
- Recursive (-R)
- Reference file

## Examples

```bash
chmod-tool +x script.sh
chmod-tool 755 myfile
chmod-tool -R 644 docs/
```

## See Also

- Related documentation: `man chmod` (if available)
