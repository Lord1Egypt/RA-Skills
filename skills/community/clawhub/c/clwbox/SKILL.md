---
name: clawbox
version: 1.0.0
description: Use the ClawBox CLI to upload, download, organize, search, and share files on ClawBox (clawbox.ink) or a self-hosted ClawBox server. Trigger this skill when users mention clawbox, clawbox, cloud file storage, uploading files to the cloud, semantic file search, file sharing links, organizing files into folders, or managing tokens and storage quotas. Also use when code imports or references the clawbox CLI tool.
---

# ClawBox

ClawBox — a cloud file system for agents with token-based auth, semantic search, folders, and file sharing.

## Setup

If the CLI is not installed, run the setup script:

```bash
bash ClawBoxSkill/scripts/setup.sh
```

Or manually:

```bash
git clone https://github.com/Alfra-AI/clawbox.git
cd clawbox
pip install .
clawbox init
```

## Commands

```bash
clawbox init                                 # Get a token from clawbox.ink
clawbox init --api-url http://localhost:8000  # Self-hosted server
clawbox config --show                        # View current config
clawbox upload <file>                        # Upload a file
clawbox upload <file> --path /docs/file.pdf  # Upload into a folder
clawbox download <file_id>                   # Download by ID
clawbox list                                 # List all files
clawbox list --folder /docs/ --recursive     # List folder contents
clawbox search "query"                       # Semantic search
clawbox embed <file_id>                      # Generate embeddings
clawbox embed --failed                       # Retry failed embeddings
clawbox delete <file_id>                     # Delete a file
clawbox status                               # Check server + token health
```

## Workflow

1. Check if `clawbox` is installed. If not, run the setup script.
2. Run `clawbox status` to verify server connection and token.
3. If no token, run `clawbox init`.
4. Prefer non-destructive inspection before mutation: `status`, `config --show`, `list`.
5. Ask before deletion unless the user explicitly requested it.
6. Report key output after each operation: file id, download path, share link, etc.

## Key details

- Config: `~/.clawbox/config.json`
- Default server: `https://clawbox.ink`
- Searchable formats: text, JSON, XML, PDF, Word, Excel, PowerPoint, CSV
- Storage: 10 MB free (anonymous), 1 GB with Google login
- Folders: virtual paths like `/docs/reports/`, created implicitly on upload

For detailed API reference, read `ClawBoxSkill/references/api.md`.
For self-hosting and deployment, read `ClawBoxSkill/references/self-hosting.md`.
For troubleshooting, read `ClawBoxSkill/references/troubleshooting.md`.
