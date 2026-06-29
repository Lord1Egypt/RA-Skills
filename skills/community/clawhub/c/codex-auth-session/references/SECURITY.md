# Security Policy

## 🔐 What This Tool Does

This tool accesses your ChatGPT web session and writes authentication tokens to the local filesystem. This is inherently sensitive — handle with care.

## 🚫 Never Commit To Git

The following are **permanently excluded** via `.gitignore` and must **never** be pushed:

| Path | Contains |
|------|----------|
| `browser-profile/` | ChatGPT login cookies & session state |
| `logs/` | Refresh logs (tokens are masked, but metadata is sensitive) |
| `backups/` | Historical copies of your `auth.json` |
| `auth.json` | Raw access tokens (resides in `~/.codex/`, not in repo) |
| `*.log` | Any log files |
| `.env` | Environment configuration |

## 🛡️ Handling a Breach

If any of these are compromised:

1. **Sign out from all ChatGPT sessions**
   - Go to https://chatgpt.com → Settings → Security → Sign out all devices
2. **Delete the browser profile** — `rm -rf browser-profile/`
3. **Delete all backups** — `rm -rf backups/`
4. **Regenerate credentials** — Change your ChatGPT password
5. **Rotate any API keys** that may have shared the same environment

## 📝 Logging Policy

The refresh script explicitly strips token values before writing to logs:

```javascript
const safe = { ...row };
delete safe.token;          // <-- token never touches disk
fs.appendFileSync(logPath, JSON.stringify(safe) + '\n');
```

Only the following metadata is recorded:
- Timestamp and status (success/error)
- Whether `accountId` was present (boolean)
- Whether `userEmail` was present (boolean)
- Session expiry timestamps

No raw token strings, no JWT payloads, no passwords.

## 🔄 Responsible Disclosure

If you find a vulnerability in how this tool handles authentication data:

- **Don't** open a public issue
- **Do** email the repository owner directly, or open a draft security advisory on GitHub
