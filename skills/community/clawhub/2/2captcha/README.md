# solve-captcha

[![skills.sh](https://skills.sh/b/adinvadim/2captcha-cli)](https://skills.sh/adinvadim/2captcha-cli)
[ClawHub](https://clawhub.ai/adinvadim/2captcha)

Solve CAPTCHAs from the command line using [2Captcha](https://2captcha.com) human-powered service.

Canonical source: https://github.com/adinvadim/2captcha-cli

## Privacy and authorized use

This tool sends CAPTCHA images, page URLs, sitekeys, challenge IDs, and task metadata to 2Captcha for processing by the 2Captcha service and its human solvers. Use it only for authorized automation, and do not submit sensitive, regulated, internal, or third-party user data unless you have approval.

## Published locations

- GitHub source and feedback: https://github.com/adinvadim/2captcha-cli
- skills.sh install source: https://skills.sh/adinvadim/2captcha-cli
- ClawHub/OpenClaw skill: https://clawhub.ai/adinvadim/2captcha

## Features

- **10 captcha types** — Image, reCAPTCHA v2/v3, hCaptcha, Turnstile, FunCaptcha, GeeTest, Amazon WAF
- **Zero dependencies** — Pure Python 3 stdlib
- **Human-first design** — Clear output, helpful errors, progress indicators
- **Script-friendly** — `--json` output, proper exit codes, `--quiet` mode
- **Flexible config** — Flag > env > config file precedence

## Installation

### Agent skill

```bash
# skills.sh: Codex, Claude Code, Cursor, and other supported agents
npx skills add adinvadim/2captcha-cli
npx skills add adinvadim/2captcha-cli --global
npx skills add adinvadim/2captcha-cli --agent codex
npx skills use adinvadim/2captcha-cli@2captcha

# OpenClaw / ClawHub
openclaw skills install 2captcha
clawhub install 2captcha
```

### CLI

```bash
# Review source, then install locally
git clone https://github.com/adinvadim/2captcha-cli.git
cd 2captcha-cli
python3 solve-captcha --version
mkdir -p ~/.local/bin
ln -sf "$PWD/solve-captcha" ~/.local/bin/solve-captcha

# Or with Homebrew (coming soon)
# brew install adinvadim/tap/solve-captcha

# Or clone manually
git clone https://github.com/adinvadim/2captcha-cli.git
cd 2captcha-cli
chmod +x solve-captcha
sudo ln -s $(pwd)/solve-captcha /usr/local/bin/
```

Old `adamvinsky/2captcha-cli` links are obsolete. Use `adinvadim/2captcha-cli`.

## Configuration

API key lookup order:
1. `--api-key` / `-k` flag
2. `TWOCAPTCHA_API_KEY` environment variable  
3. `~/.config/2captcha/api-key` file
4. `~/.2captcha-api-key` file

```bash
# Option 1: Environment
export TWOCAPTCHA_API_KEY="your-key"

# Option 2: Config file
mkdir -p ~/.config/2captcha
echo "your-key" > ~/.config/2captcha/api-key
```

## Usage

### Quick examples

```bash
# Image captcha
solve-captcha image captcha.png
solve-captcha image https://example.com/captcha.jpg --math

# reCAPTCHA v2
solve-captcha recaptcha2 -s 6Le-wvkSAAAA... -u https://example.com

# hCaptcha
solve-captcha hcaptcha -s a5f74b19-9e45... -u https://example.com

# Cloudflare Turnstile
solve-captcha turnstile -s 0x4AAA... -u https://example.com

# Check balance
solve-captcha balance
```

Do not use these commands on sensitive or internal pages unless sending CAPTCHA content and page metadata to 2Captcha is approved for that workflow.

### Commands

| Command | Description |
|---------|-------------|
| `image <file\|url>` | Solve image captcha (OCR) |
| `recaptcha2` | Solve reCAPTCHA v2 |
| `recaptcha3` | Solve reCAPTCHA v3 |
| `hcaptcha` | Solve hCaptcha |
| `turnstile` | Solve Cloudflare Turnstile |
| `funcaptcha` | Solve Arkose Labs FunCaptcha |
| `geetest` | Solve GeeTest v3 |
| `geetest4` | Solve GeeTest v4 |
| `amazon` | Solve Amazon WAF CAPTCHA |
| `text <question>` | Solve text question |
| `balance` | Check account balance |

### Global flags

| Flag | Description |
|------|-------------|
| `-h, --help` | Show help |
| `-V, --version` | Show version |
| `-k, --api-key` | API key (overrides env/config) |
| `-j, --json` | Output full JSON response |
| `-q, --quiet` | Suppress progress output |
| `-v, --verbose` | Verbose debug output |
| `-t, --timeout` | Timeout in seconds (default: 180) |
| `--no-color` | Disable colored output |

### Image captcha options

```bash
solve-captcha image captcha.png [options]
```

| Option | Description |
|--------|-------------|
| `--phrase` | Answer contains multiple words |
| `--case-sensitive` | Case-sensitive answer |
| `--numeric N` | 0=any, 1=numbers, 2=letters, 3=either, 4=both |
| `--math` | Requires calculation |
| `--min-length N` | Minimum answer length |
| `--max-length N` | Maximum answer length |
| `--comment TEXT` | Instructions for solver |
| `--lang LANG` | Language pool (en, rn) |

## Output

### Human mode (default)

```
$ solve-captcha image captcha.png
Submitting image captcha...
Solving... 12s
✓ Solved in 0.00025 USD
abc123
```

### JSON mode

```
$ solve-captcha --json image captcha.png
{
  "errorId": 0,
  "status": "ready",
  "solution": {"text": "abc123"},
  "cost": "0.00025"
}
```

### Quiet mode (for scripts)

```bash
TOKEN=$(solve-captcha -q recaptcha2 -s KEY -u URL)
```

## Exit codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | General error |
| 2 | Invalid usage / missing args |
| 3 | Timeout |
| 4 | Authentication error |
| 130 | Interrupted (Ctrl-C) |

## Environment

Respects standard conventions:
- `NO_COLOR` — Disable colors
- `TERM=dumb` — Disable colors
- Non-TTY stderr — Disable progress/colors

## Feedback

Open bugs and feature requests in [GitHub Issues](https://github.com/adinvadim/2captcha-cli/issues).

## License

MIT © Vadim Kostin (@adinvadim)
