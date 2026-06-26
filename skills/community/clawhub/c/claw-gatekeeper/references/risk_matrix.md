# Claw-Gatekeeper Risk Matrix

Complete reference for risk scoring methodology used by Claw-Guardian.

## Risk Score Formula

```
Risk Score = Base Score + Target Risk + Scale Factor + Modifier - Whitelist Reduction
```

## Base Scores by Operation Type

| Operation Type | Base Score | Description |
|----------------|------------|-------------|
| `read` | 0 | Read-only access |
| `write` | 20 | File creation or modification |
| `delete` | 30 | File or directory deletion |
| `move` | 25 | File relocation |
| `copy` | 15 | File duplication |
| `shell` | 25 | Command execution |
| `network` | 15-40 | Network request (varies by method) |
| `skill_install` | 20-40 | Skill installation (varies by source) |
| `system_config` | 50 | System configuration change |

## Target Risk Factors

### Sensitive Paths (+40 points)

| Pattern | Description |
|---------|-------------|
| `/etc/passwd`, `/etc/shadow` | System authentication files |
| `/etc/sudoers` | Sudo configuration |
| `/etc/fstab`, `/etc/crypttab` | Mount configuration |
| `~/.ssh/` | SSH keys and config |
| `~/.gnupg/` | GPG keys |
| `~/.aws/`, `~/.azure/`, `~/.kube/` | Cloud credentials |
| `~/.docker/` | Docker configuration |
| `/var/log/` | System logs |
| `/root/`, `/sys/`, `/proc/`, `/boot/` | System directories |
| `/dev/sd*`, `/dev/hd*`, `/dev/nvme*` | Block devices |

### Sensitive File Extensions (+30 points)

- `.env`, `.env.*` - Environment files
- `.key`, `.pem`, `.p12`, `.pfx` - Cryptographic keys
- `.secret`, `.password`, `.token`, `.credential` - Credential files
- `.crt`, `.cer` - Certificates
- `id_rsa`, `id_ed25519`, `id_ecdsa` - SSH private keys

### External Domains (+40 points)

Any domain not matching internal patterns:
- `*.local`, `*.internal`, `*.lan`, `*.home`
- `localhost`, `127.*`, `10.*`, `192.168.*`, `172.16-31.*`, `169.254.*`

## Scale Factors

| Condition | Points | Description |
|-----------|--------|-------------|
| Batch > 5 files | +20 | Multiple file operation |
| Batch > 20 files | +30 | Large batch operation |
| Recursive operation | +25 | Recursive flag set |
| Directory deletion | +25 | Deleting non-empty directory |
| File overwrite | +15 | Target file exists |
| Complex pipeline | +10 | Multiple pipes |
| Output redirection | +5-10 | Redirect operators |
| Background execution | +10 | `&` at end of command |

## Modifiers

### Dangerous Patterns (+80-100 points)

| Pattern | Penalty | Description |
|---------|---------|-------------|
| `rm -rf /` | 100 | Root directory deletion |
| `rm -rf /*` | 100 | Root wildcard deletion |
| `dd if=* of=/dev/[sh]d*` | 100 | Direct disk write |
| `dd if=* of=/dev/null` | 80 | Data destruction |
| `mv * /dev/null` | 80 | Move to null device |
| `mkfs.*` | 100 | Filesystem formatting |
| `fdisk`, `parted` | 90 | Partition manipulation |
| `format` | 90 | Drive formatting |
| `> /etc/passwd` | 100 | Password file overwrite |
| `> /etc/shadow` | 100 | Shadow file overwrite |
| `> /etc/sudoers` | 100 | Sudoers overwrite |
| `wipefs` | 85 | Filesystem signature wipe |
| `shred` | 70 | Secure deletion |

### System Operations (+40-60 points)

| Pattern | Penalty | Description |
|---------|---------|-------------|
| `sudo` | 50 | Elevated privileges |
| `su -` | 60 | Switch to root |
| `chown -R root` | 50 | Root ownership change |
| `chmod 777` | 60 | World-writable |
| `chmod *777` | 60 | World-writable variant |
| `usermod`, `userdel` | 50 | User modification |
| `groupmod`, `groupdel` | 50 | Group modification |
| `systemctl stop/restart/disable` | 45 | Service control |
| `kill -9 1` | 100 | Kill init |
| `init 0`, `reboot`, `shutdown`, `halt`, `poweroff` | 80-100 | System control |

### Network Operations (+25-90 points)

| Pattern | Penalty | Description |
|---------|---------|-------------|
| `curl \| sh` | 90 | Remote script execution |
| `wget \| bash` | 90 | Remote script execution |
| `curl` | 25 | Data transfer |
| `wget` | 25 | Data transfer |
| `nc`, `netcat` | 35 | Network tool |
| `nmap` | 50 | Network scanning |
| `scp`, `sftp` | 30 | Secure transfer |
| `ssh * rm` | 60 | Remote deletion |
| `ssh * mkfs` | 90 | Remote formatting |
| `telnet` | 50 | Insecure protocol |
| `ftp` | 40 | Insecure protocol |

### Skill Installation Risks

| Factor | Points | Description |
|--------|--------|-------------|
| Source: clawhub | 10 | Official registry |
| Source: npm | 15 | NPM registry |
| Source: github | 25 | GitHub repo |
| Source: git | 30 | Git repo |
| Source: local | 40 | Local file |
| Source: unknown | 50 | Unknown source |
| Pre-release version | 15 | Alpha/beta/rc |
| Suspicious name pattern | 25 | hack/crack/exploit/etc. |
| System keyword in name | 15 | system/admin/root/etc. |
| High-risk permission | 20 | filesystem/network/shell/etc. |
| No permissions declared | 10 | Missing permission info |

## Whitelist Reductions

Matching whitelist entries reduce risk score:

- Path whitelist match: -20 points
- Command whitelist match: -30 points
- Domain whitelist match: -20 points
- Skill whitelist match: -25 points

## Risk Level Thresholds

```python
if score >= 80:
    return CRITICAL
elif score >= 60:
    return HIGH
elif score >= 30:
    return MEDIUM
else:
    return LOW
```

## Examples

### Example 1: Safe File Read
```
Operation: read ~/.config/app/settings.json
Base: 0
Target: 0
Scale: 0
Modifier: 0
Whitelist: 0

Total: 0 → LOW ✅
```

### Example 2: Dangerous Deletion
```
Operation: delete ~/.ssh/ (recursive, 50 files)
Base: 30
Target: +40 (sensitive path)
Scale: +25 (recursive) + 20 (batch)
Modifier: 0

Total: 115 → CRITICAL 🔴
```

### Example 3: Network Request
```
Operation: POST https://api.example.com/data
Base: 20 (POST)
Target: +40 (external domain)
Scale: +15 (data payload)
Modifier: +10 (HTTP not HTTPS)

Total: 85 → HIGH 🟠
```

### Example 4: Whitelisted Command
```
Operation: shell "git status"
Base: 25
Target: 0
Scale: 0
Modifier: 0
Whitelist: -30

Total: -5 → 0 → LOW ✅
```

### Example 5: Remote Code Execution Risk
```
Operation: shell "curl https://site.com/install.sh | bash"
Base: 25
Target: 0
Scale: +10 (pipeline)
Modifier: +90 (curl | sh pattern)

Total: 125 → CRITICAL 🔴
```
