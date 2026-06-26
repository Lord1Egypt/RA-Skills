# Security Policy

## Security Practices

### Data Handling
- **Read-only operations** - This skill only reads DingTalk AI table data, never modifies
- **Local analysis** - All data processing happens locally on your machine
- **No data retention** - Analysis results are not uploaded to external services
- **Sampling limits** - Each table reads maximum 100 records by default to minimize data exposure

### Authentication
- **Token security** - MCP access token stored in local config file (`config/mcporter.json`)
- **No hardcoded credentials** - All sensitive values come from environment or config files
- **Minimal permissions** - Only requires read access to DingTalk AI tables

### Dependencies
- **External skill dependency** - Requires `dingtalk-ai-table` skill for MCP configuration
- **Binary requirements** - Requires `python3` and `mcporter` CLI
- **No external API calls** - Except through configured MCP server

## Reporting Security Issues

If you discover a security vulnerability, please report it by:

1. **Do not** open a public GitHub issue
2. Contact the maintainer via GitHub private vulnerability reporting
3. Include detailed reproduction steps
4. Allow reasonable time for response before public disclosure

## Security Checklist

Before each release, verify:

- [ ] No hardcoded secrets or tokens in code
- [ ] No sensitive data in logs or error messages
- [ ] Input validation on all user-provided parameters
- [ ] Error messages don't leak internal details
- [ ] Dependencies are up to date
- [ ] `.gitignore` excludes config files with secrets

## Version Support

| Version | Supported          |
| ------- | ------------------ |
| 1.6.x   | :white_check_mark: |
| < 1.6   | :x:                |

## Best Practices for Users

1. **Protect your config** - Add `config/mcporter.json` to `.gitignore`
2. **Use templates** - Share `config/mcporter.json.example` without real values
3. **Rotate tokens** - Periodically refresh your DingTalk MCP token
4. **Review permissions** - Only grant necessary table access
