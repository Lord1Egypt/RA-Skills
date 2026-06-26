# Operation Taxonomy

Complete classification of destructive operations for AI agents.

## CRITICAL — Always Requires Verification

### File Destruction
| Operation | Pattern | Examples |
|-----------|---------|----------|
| rm / remove | `rm`, `rmdir`, `Remove-Item`, `del` | `rm -rf /tmp/old`, `Remove-Item *.log` |
| unlink | `unlink()`, `os.remove()` | Python file deletion |
| trash | `trash-cli`, `gio trash` | Move to system trash |
| empty-trash | `rm -rf ~/.Trash`, `Clear-RecycleBin` | Permanent deletion of trashed files |
| overwrite | Write to existing file without version control | `> file.txt` (clobber) |
| truncate | `truncate -s 0`, `fsutil` | Zero-length file without backup |

### Database Destruction
| Operation | Pattern | Examples |
|-----------|---------|----------|
| DROP | `DROP TABLE`, `DROP DATABASE` | Schema destruction |
| DELETE (unqualified) | `DELETE FROM table` (no WHERE) | Mass data deletion |
| TRUNCATE | `TRUNCATE TABLE` | Instant table empty |
| destructive migration | `down()` migration, `rollback` | Schema reversal with data loss |
| ALTER destructive | `ALTER TABLE ... DROP COLUMN` | Structural deletion |

## HIGH — Requires Verification

### External Transmission
| Operation | Pattern | Examples |
|-----------|---------|----------|
| send email | SMTP send, API email | `sendmail`, SES, SendGrid |
| post message | Social media API | Twitter/X, LinkedIn, Mastodon |
| publish | CMS publish, blog post | WordPress, Ghost, static site |
| API write | POST/PUT/DELETE to external | Any mutating external API call |
| webhook trigger | Outgoing webhook POST | Triggering external systems |

### Mass Operations
| Operation | Threshold | Examples |
|-----------|-----------|----------|
| bulk file modify | >10 files in single op | Batch rename, sed across directory |
| bulk delete | >10 files | `find . -name "*.tmp" -delete` |
| recursive operations | `**` glob, `-r` flag | `rm -rf`, `chmod -R` |

### System Changes
| Operation | Pattern | Examples |
|-----------|---------|----------|
| service control | `systemctl`, `Start-Service` | Stop/start/restart services |
| firewall modify | `iptables`, `netsh advfirewall` | Add/remove rules |
| registry edit | `reg add`, `Set-ItemProperty` | Windows registry changes |
| user management | `useradd`, `New-LocalUser` | Create/delete accounts |
| scheduled task | `schtasks`, `cron` | Add/remove automation |
| environment | `setx`, `[Environment]::SetEnvironmentVariable` | System-wide env vars |

## MEDIUM — Verify if Target is Important

### Network Unknown
| Operation | Pattern | Examples |
|-----------|---------|----------|
| new domain | URL not in known list | First call to api.newvendor.com |
| unverified endpoint | No prior successful calls | POST to unvalidated webhook |
| DNS change | `nsupdate`, registrar API | Pointing domain elsewhere |
| certificate | `certbot`, `New-SelfSignedCertificate` | TLS/SSL modifications |

### Configuration
| Operation | Pattern | Examples |
|-----------|---------|----------|
| .env overwrite | Write to `.env`, `secrets.yaml` | Credential/environment changes |
| config modify | Edit `.ini`, `.toml`, `.json` config | Application settings |
| SSH keys | `ssh-keygen`, `authorized_keys` | Authentication changes |
| API keys | Rotate, revoke, regenerate | Service authentication |

## NON-DESTRUCTIVE — No Guardian Check

| Category | Examples |
|----------|----------|
| Read-only | `cat`, `ls`, `Get-Content`, `SELECT` queries |
| Analysis | `grep`, `find`, `awk`, search, audit |
| Safe write | Append to log, create new file in temp |
| Status check | `ping`, `curl -I`, health checks |
| Internal query | Database SELECT, API GET with no side effects |

## Ambiguous — Default to Destructive

| Operation | Why Ambiguous | Guardian Action |
|-----------|---------------|-----------------|
| `git reset --hard` | Destroys uncommitted work | VERIFY backup |
| `git push --force` | Overwrites remote history | VERIFY backup |
| `docker system prune` | Deletes containers/images | VERIFY backup |
| `npm audit fix` | Modifies dependencies | VERIFY backup |
| Package manager update | System-wide changes | VERIFY backup |
| Migration `up()` | Schema changes | VERIFY backup |

## Rules

1. **When in doubt, destructive.** If an operation could be either, treat as destructive.
2. **Chained operations count as one.** `find . -name "*.log" -exec rm {} \;` is mass delete even if `find` itself is read-only.
3. **Destructive intent is irrelevant.** The taxonomy cares about operation effect, not agent intent.
4. **Context matters.** `rm test-file-in-temp` is different from `rm /etc/passwd`. Guardian checks target path.
