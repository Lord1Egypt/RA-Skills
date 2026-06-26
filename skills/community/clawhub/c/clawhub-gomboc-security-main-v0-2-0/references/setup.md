# Setup Guide

## Prerequisites

- Python 3.7+
- Gomboc account (free at https://app.gomboc.ai)
- Personal Access Token from Gomboc

## 1. Get a Token

1. Sign up at https://app.gomboc.ai (Community Edition is free)
2. Go to Settings → API Tokens
3. Generate a new Personal Access Token
4. Copy the token (starts with `gpt_`)

## 2. Set Environment Variable

```bash
export GOMBOC_PAT="gpt_your_token_here"
```

Or add to your shell profile:

```bash
echo 'export GOMBOC_PAT="gpt_your_token_here"' >> ~/.bashrc
source ~/.bashrc
```

## 3. Verify Setup

```bash
bash scripts/verify-setup.sh
```

Should output:
```
✅ GOMBOC_PAT is set
✅ Python 3 found: Python 3.7+
✅ CLI wrapper found
✅ API connection successful
✅ Setup verification complete!
```

## 4. Run Your First Scan

```bash
python scripts/cli-wrapper.py scan --path ./src
```

## Troubleshooting

### "GOMBOC_PAT not set"
```bash
export GOMBOC_PAT="your_token"
```

### "API connection failed"
- Check your token is correct
- Check you can reach https://api.app.gomboc.ai
- Check your network/firewall

### "Path not found"
- Make sure the path exists
- Use absolute paths if in different directory

## Next Steps

- Run `python scripts/cli-wrapper.py fix --path ./src` to generate fixes
- See `references/mcp-integration.md` for agent integration
- See `references/github-action.md` for CI/CD setup

## Support

- **Gomboc Docs:** https://docs.gomboc.ai
- **Community Edition:** https://docs.gomboc.ai/getting-started-ce
- **GitHub Discussions:** https://github.com/Gomboc-AI/gomboc-ai-feedback/discussions