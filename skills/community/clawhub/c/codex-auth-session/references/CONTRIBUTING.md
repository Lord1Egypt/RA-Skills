# Contributing

Thanks for considering contributing to Codex Auth Session Refresh! 🎉

## How to Contribute

### 🐛 Report Bugs

Open an issue with:
- Your OS version and Node.js version
- The browser you're using (Chrome/Edge)
- Full error output (logs are in `logs/refresh.log.jsonl`)
- Steps to reproduce

### 💡 Feature Requests

Ideas welcome! Open an issue describing:
- What you're trying to solve
- How the feature would work
- Any alternatives you've considered

### 🔧 Pull Requests

1. Fork the repo
2. Create a feature branch: `git checkout -b feat/my-thing`
3. Make your changes
4. Test on Windows if possible (primary target platform)
5. Open a PR with a clear description

## Code Style

- **PowerShell**: Use `$ErrorActionPreference = "Stop"`, PascalCase params, avoid aliases
- **JavaScript**: CommonJS modules (`require`/`module.exports`), no transpilation
- **Docs**: Keep README up to date with any new features or configuration options

## Testing

Since this tool interacts with live browser profiles and ChatGPT sessions, automated testing is limited. Manual verification checklist:

- [ ] `npm install` completes without errors
- [ ] `.\login-profile.ps1` opens browser and extracts token
- [ ] `.\run-refresh.ps1` refreshes without re-login
- [ ] `.\status.ps1` shows correct state
- [ ] `.\install-scheduled-task.ps1` creates the task
- [ ] Backups are created in `backups/`

## Security

If you're submitting changes that touch authentication or file I/O:
- Never log raw tokens or credentials
- Verify `.gitignore` excludes any sensitive paths
- Prefer environment variables over hardcoded paths
