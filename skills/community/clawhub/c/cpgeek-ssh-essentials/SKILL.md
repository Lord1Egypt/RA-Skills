---
name: ssh-essentials
description: Essential SSH commands for secure remote access, key management, tunneling, and file transfers.
homepage: https://www.openssh.com/
metadata: {"clawdbot":{"emoji":"🔐","requires":{"bins":["ssh","scp","sftp","rsync","ssh-keygen","ssh-copy-id"]}}}
---

# SSH Essentials

Secure Shell (SSH) for remote access and secure file transfers.

## Basic Connection

### Connecting
```bash
# Connect with username
ssh user@hostname

# Connect to specific port
ssh user@hostname -p 2222

# Connect with verbose output
ssh -v user@hostname

# Connect with specific key
ssh -i ~/.ssh/id_rsa user@hostname

# Connect and run command
ssh user@hostname 'ls -la'
ssh user@hostname 'uptime && df -h'
```

### Interactive use
```bash
# Connect with forwarding agent
ssh -A user@hostname
# (⚠️ Agent forwarding exposes the local SSH agent to the remote host.
#  Compromise of the remote server = compromise of all identities forwarded through it.
#  Prefer ProxyJump or ProxyCommand instead. See Tunneling section for safer alternatives.)

# Connect with X11 forwarding (GUI apps)
ssh -X user@hostname  # Untrusted X11 (sandboxed, safer — Xfixes restrictions apply)
ssh -Y user@hostname  # Trusted X11 (full X access, can execute arbitrary X commands)

# (⚠️ -Y grants the remote host full access to your local X server. Malicious apps can capture keystrokes/screenshots.
#  Prefer -X unless you specifically need trusted X11 forwarding for performance-critical GUI apps.)

# Escape sequences (during session)
# ~. - Disconnect
# ~^Z - Suspend SSH
# ~# - List forwarded connections
# ~? - Help
```

## SSH Keys

### Generating keys
```bash
# Generate RSA key
ssh-keygen -t rsa -b 4096 -C "your_email@example.com"

# Generate ED25519 key (recommended)
ssh-keygen -t ed25519 -C "your_email@example.com"

# Generate with custom filename
ssh-keygen -t ed25519 -f ~/.ssh/id_myserver

# Generate without passphrase (automation)
ssh-keygen -t ed25519 -N "" -f ~/.ssh/id_deploy
# (⚠️ WARNING: Keys without passphrases are stored as plaintext on disk.
#  If the key file is stolen, anyone can use it. For automation, prefer ssh-agent
#  with passphrase-protected keys and add the key with ssh-add.)
```

### Managing keys
```bash
# Copy public key to server
ssh-copy-id user@hostname

# Copy specific key
ssh-copy-id -i ~/.ssh/id_rsa.pub user@hostname

# Manual key copy
cat ~/.ssh/id_rsa.pub | ssh user@hostname 'cat >> ~/.ssh/authorized_keys'

# Check key fingerprint
ssh-keygen -lf ~/.ssh/id_rsa.pub

# Change key passphrase
ssh-keygen -p -f ~/.ssh/id_rsa
```

### SSH agent
```bash
# Start ssh-agent
eval $(ssh-agent)

# Add key to agent
ssh-add ~/.ssh/id_rsa

# List keys in agent
ssh-add -l

# Remove key from agent
ssh-add -d ~/.ssh/id_rsa

# Remove all keys
ssh-add -D

# Set key lifetime (seconds)
ssh-add -t 3600 ~/.ssh/id_rsa
# (⚠️ Use short-lived keys (-t) for shared/bastion hosts. Remove keys when done: ssh-add -d ~/.ssh/id_rsa)

# (⚠️ Always remove keys from agent when done: ssh-add -D to clear all, or ssh-add -d to remove specific keys.)
```

## Port Forwarding & Tunneling

### Local port forwarding
```bash
# Forward local port to remote
ssh -L 8080:localhost:80 user@hostname
# Access via: http://localhost:8080

# Forward to different remote host
ssh -L 8080:database.example.com:5432 user@jumphost
# Access database through jumphost

# Multiple forwards
ssh -L 8080:localhost:80 -L 3306:localhost:3306 user@hostname
```

### Remote port forwarding
```bash
# Forward remote port to local
ssh -R 8080:localhost:3000 user@hostname
# Remote server can access localhost:3000 via its port 8080

# Make service accessible from remote
ssh -R 9000:localhost:9000 user@publicserver

# (⚠️ WARNING: This exposes your local services to the remote server. Any user with
#  access to the remote host can connect to your local ports. Only use -R on trusted
#  bastion hosts, never on untrusted public servers.)
```

### Dynamic port forwarding (SOCKS proxy)
```bash
# Create SOCKS proxy
ssh -D 1080 user@hostname

# Use with browser or apps
# Configure SOCKS5 proxy: localhost:1080

# With Firefox
firefox --profile $(mktemp -d) \
  --preferences "network.proxy.type=1;network.proxy.socks=localhost;network.proxy.socks_port=1080"

# (⚠️ SOCKS5 traffic is NOT encrypted by default. Browsers configured to use a SOCKS proxy
#  may send credentials and data in cleartext. For encrypted proxy traffic, use SSH -L or -R
#  port forwarding instead of SOCKS, or use a TLS-based proxy like mitmproxy.)
```

### Background tunnels
```bash
# Run in background
ssh -f -N -L 8080:localhost:80 user@hostname

# -f: Background
# -N: No command execution
# -L: Local forward

# Keep alive
ssh -o ServerAliveInterval=60 -L 8080:localhost:80 user@hostname

# (⚠️ Background tunnels persist after you close your terminal. Always clean up when done.)
# (⚠️ Stale tunnels consume server resources and leave ports open. Clean up with `ssh -O exit`.)

# Check active tunnels
ssh -O check user@hostname

# Clean shutdown of a background tunnel
ssh -O exit user@hostname

# Kill all stale SSH connections
pkill -f "ssh.*-L.*8080"  # Replace port number with your tunnel port
```

## Configuration

### SSH config file (`~/.ssh/config`)
```
# Simple host alias
Host myserver
    HostName 192.168.1.100
    User admin
    Port 2222

# With key and options
Host production
    HostName prod.example.com
    User deploy
    IdentityFile ~/.ssh/id_prod
    ForwardAgent yes  # (⚠️ Only forward to hosts you fully trust. The remote server can use your identities to authenticate elsewhere.)

# Jump host (bastion)
Host internal
    HostName 10.0.0.5
    User admin
    ProxyJump bastion

Host bastion
    HostName bastion.example.com
    User admin

# (⚠️ Wildcard Host patterns match ALL domains matching the glob.
#  ForwardAgent yes under *.example.com means your agent identity is forwarded
#  to EVERY matching host, including any newly added subdomains. This is a
#  significant agent forwarding risk.)

# Instead of wildcard, use specific host entries:
Host bastion.example.com
    User admin
    ForwardAgent yes  # Only forward to this specific, trusted host

Host web.example.com
    User admin
    # No ForwardAgent — don't forward unless explicitly needed

# (⚠️ Best practice: Only enable ForwardAgent on hosts you fully trust and need it.)

# Keep connections alive
Host *
    ServerAliveInterval 60
    ServerAliveCountMax 3
```

### Using config
```bash
# Connect using alias
ssh myserver

# Jump through bastion automatically
ssh internal

# Override config options
ssh -o "StrictHostKeyChecking=no" myserver
```

## File Transfers

### SCP (Secure Copy)
```bash
# Copy file to remote
scp file.txt user@hostname:/path/to/destination/

# Copy file from remote
scp user@hostname:/path/to/file.txt ./local/

# Copy directory recursively
scp -r /local/dir user@hostname:/remote/dir/

# Copy with specific port
scp -P 2222 file.txt user@hostname:/path/

# Copy with compression
scp -C large-file.zip user@hostname:/path/

# Preserve attributes (timestamps, permissions)
scp -p file.txt user@hostname:/path/
```

> (⚠️ SCP is deprecated in modern OpenSSH versions. Use sftp for interactive transfers
>  or rsync for directory syncs. The scp protocol has known security and reliability issues.)

### SFTP (Secure FTP)
```bash
# Connect to SFTP server
sftp user@hostname

# Common SFTP commands:
# pwd          - Remote working directory
# lpwd         - Local working directory
# ls           - List remote files
# lls          - List local files
# cd           - Change remote directory
# lcd          - Change local directory
# get file     - Download file
# put file     - Upload file
# mget *.txt   - Download multiple files
# mput *.jpg   - Upload multiple files
# mkdir dir    - Create remote directory
# rmdir dir    - Remove remote directory
# rm file      - Delete remote file
# exit/bye     - Quit

# Batch mode
sftp -b commands.txt user@hostname
```

> (⚠️ SFTP sessions leave files on the remote server. Use `rm` in SFTP to clean up sensitive temporary files.)

### Rsync over SSH
```bash
# Sync directory (safe, no deletions)
rsync -avz /local/dir/ user@hostname:/remote/dir/

# Sync with progress
rsync -avz --progress /local/dir/ user@hostname:/remote/dir/

# (⚠️ ALWAYS test with --dry-run first when using --delete.
#  --delete removes files on the destination that don't exist on the source — this is destructive.)

# Dry run (review what would happen before executing)
rsync -avz --dry-run --delete /local/dir/ user@hostname:/remote/dir/
# Review the output, then execute the real command

# Sync with delete (mirror) — only after dry-run confirms expected changes
rsync -avz --delete /local/dir/ user@hostname:/remote/dir/
# (⚠️ DELETION WARNING: This removes files from the destination that aren't in the source.
#  Double-check --dry-run output before running. Consider using --ignore-errors for large transfers.)

# Exclude patterns (protect important files)
rsync -avz --exclude '*.log' --exclude 'node_modules/' \
  /local/dir/ user@hostname:/remote/dir/

# Exclude multiple patterns (better for complex setups)
rsync -avz --exclude={'*.log','*.tmp','*.cache','node_modules/'} \
  /local/dir/ user@hostname:/remote/dir/

# Custom SSH port
rsync -avz -e "ssh -p 2222" /local/dir/ user@hostname:/remote/dir/
```

## Security Best Practices

### Hardening SSH
```bash
# Disable password authentication (edit /etc/ssh/sshd_config)
PasswordAuthentication no
PubkeyAuthentication yes

# Disable root login
PermitRootLogin no
# (⚠️ System administrators should use sudo through a bastion host instead of direct root login.)

# Change default port
Port 2222

# Use protocol 2 only
Protocol 2

# Limit users
AllowUsers user1 user2
```

### Connection security
```bash
# Check host key
ssh-keygen -F hostname

# Remove old/stale host key
ssh-keygen -R hostname

# Strict host key checking — three modes:
ssh -o StrictHostKeyChecking=yes user@hostname
# (⚠️ This blocks connections to new hosts. Use accept-new for automated first-time connections.)
# Blocks connections to hosts not in known_hosts. Safe but inconvenient for first-time connections.

ssh -o StrictHostKeyChecking=accept-new user@hostname
# Preferred: Accepts new host keys but refuses unknown ones without prompting.
# Safer than 'no' and doesn't block legitimate first-time connections.

ssh -o StrictHostKeyChecking=no user@hostname
# (⚠️ NOT RECOMMENDED: Accepts any host key without verification. Vulnerable to MITM.)

# Verify and store a known-good host key (safe pre-population workflow)
ssh-keyscan -t ed25519 hostname
# (⚠️ Run ssh-keyscan independently first, compare the output against a trusted key
#  obtained via another channel (e.g., admin console, PGP-signed key page). Only then append:
ssh-keyscan -t ed25519 hostname >> ~/.ssh/known_hosts
#  If the scanned key doesn't match the trusted key, DO NOT append it.)

# Use specific cipher
ssh -c aes256-ctr user@hostname
```

## Troubleshooting

### Debugging
```bash
# Verbose output
ssh -v user@hostname
ssh -vv user@hostname  # More verbose
ssh -vvv user@hostname  # Maximum verbosity

# Test connection
ssh -T user@hostname

# Check permissions
ls -la ~/.ssh/
# Should be: 700 for ~/.ssh, 600 for keys, 644 for .pub files
```

### Common issues
```bash
# Fix permissions
chmod 700 ~/.ssh
chmod 600 ~/.ssh/id_rsa
chmod 644 ~/.ssh/id_rsa.pub
chmod 644 ~/.ssh/authorized_keys

# Clear known_hosts entry
ssh-keygen -R hostname

> ⚠️ **TROUBLESHOOTING ALERT:** If you're using StrictHostKeyChecking=no because a
> connection is being refused, you're disabling MITM protection as a convenience.
> The remote server's host key may have legitimately changed (reinstall, new image),
> but this option accepts ANY key without verification — including a fake one from
> an attacker on the network path. The consequence: you lose all host verification
> and can be silently intercepted. Fix the real issue instead of disabling checks.
ssh -o StrictHostKeyChecking=no user@hostname  # (⚠️ NOT RECOMMENDED: Disables MITM protection)

# (⚠️ Prefer StrictHostKeyChecking=accept-new — adds new host keys safely without accepting unknown ones)
ssh -o StrictHostKeyChecking=accept-new user@hostname
```

## Advanced Operations

### Jump hosts (ProxyJump)
```bash
# Connect through bastion
ssh -J bastion.example.com user@internal.local

# Multiple jumps
ssh -J bastion1,bastion2 user@final-destination

# Using config (see Configuration section above)
ssh internal  # Automatically uses ProxyJump
```

### Multiplexing
```bash
# Master connection (creates multiplexed session)
ssh -M -S ~/.ssh/control-%r@%h:%p user@hostname

# Reuse existing connection
ssh -S ~/.ssh/control-user@hostname:22 user@hostname

# (⚠️ Control sockets are stored on disk. On shared systems, ensure ~/.ssh has 700 permissions.
#  Anyone with access to the control socket can impersonate you on the target host.)

# In config (recommended approach):
# ControlMaster auto
# ControlPath ~/.ssh/control-%r@%h:%p
# ControlPersist 10m

# (⚠️ ControlPersist keeps the master connection alive. Stale connections can be exploited.
#  Set a reasonable timeout (e.g., 10m–30m) rather than "yes" (infinite).)
```

### Execute commands
```bash
# Single command
ssh user@hostname 'uptime'

# Multiple commands
ssh user@hostname 'cd /var/log && tail -n 20 syslog'

# Pipe commands
cat local-script.sh | ssh user@hostname 'bash -s'

# With sudo
ssh -t user@hostname 'sudo command'
```

## Tips

- Use SSH keys instead of passwords
- Use `~/.ssh/config` for frequently accessed hosts
- Enable SSH agent forwarding carefully (security risk)
- Use ProxyJump for accessing internal networks
- Keep SSH client and server updated
- Use fail2ban or similar to prevent brute force
- Monitor `/var/log/auth.log` for suspicious activity
- Use port knocking or VPN for additional security
- Backup your SSH keys securely
- Use different keys for different purposes

## Documentation

Official docs: https://www.openssh.com/manual.html
Man pages: `man ssh`, `man ssh_config`, `man sshd_config`
