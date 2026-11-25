# Remote Command Execution & SSH Guide

Detailed remote shell command execution (`cmd`/`ssh`) and external SSH tunnel access in `awesun-cli`.

---

## 1. Prerequisites & Session Selection

Command execution requires an active CLI session matching the remote operating system:
- **Windows target**: Connect with `--type cmd`
- **Linux / macOS target**: Connect with `--type ssh`

```bash
# Connect Linux/Mac SSH terminal session
awesun-cli session connect --type ssh --remote-id 1738789907
# Returns session_id: ssh_session_001

# Connect Windows CMD command session
awesun-cli session connect --type cmd --remote-id 1738789907
# Returns session_id: cmd_session_001
```

---

## 2. Remote Command Execution (`session exec`)

Execute shell commands and capture standard output:

```bash
# Single command execution on Linux/macOS
awesun-cli session exec ssh_session_001 "uname -a"

# Directory inspection with arguments
awesun-cli session exec ssh_session_001 "ls" "-la" "/var/log"

# Windows command execution
awesun-cli session exec cmd_session_001 "dir" "C:\\"
awesun-cli session exec cmd_session_001 "ipconfig" "/all"
```

### Scripting & Multi-command Execution
To run multiple commands or pipeline commands, wrap them in a shell interpreter invocation:

```bash
# Linux/macOS multi-command pipeline
awesun-cli session exec ssh_session_001 "sh" "-c" "cd /opt/app && git pull && npm test"

# Windows multi-command execution
awesun-cli session exec cmd_session_001 "cmd" "/c" "cd C:\\app && npm run build"
```

---

## 3. SSH Local Proxy Address (`ssh address`)

When connected to a Linux or macOS machine with `type=ssh`, `awesun-cli` establishes a local proxy tunnel allowing standard SSH clients (like `ssh`, `scp`, `rsync`) to connect directly:

```bash
awesun-cli ssh address ssh_session_001
# Output:
# Address: 127.0.0.1:2222
```

### Direct Connect via Local Port
```bash
# Connect using local SSH client
ssh -p 2222 user@127.0.0.1

# Transfer file via scp over the tunnel
scp -P 2222 local_file.txt user@127.0.0.1:/remote/path/
```
