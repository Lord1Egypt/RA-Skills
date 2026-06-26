# dirs-submit

Submit URLs to [aidirs.org](https://aidirs.org) and [backlinkdirs.com](https://backlinkdirs.com) with the `ship` CLI.

## What it does

- Browser-based login with token persistence
- Submit a URL to a supported directory
- Preview site metadata without creating a record
- Check CLI version and self-update
- Keep tokens separated per site

## Install

```bash
bash <(curl -fsSL https://raw.githubusercontent.com/RobinWM/ship-cli/main/install.sh)
```

Or from source:

```bash
git clone https://github.com/RobinWM/ship-cli.git
cd ship-cli
bash install.sh
```

## Quick Start

### 1) Login

```bash
ship login
```

Or choose a site explicitly:

```bash
ship login --site aidirs.org
ship login --site backlinkdirs.com
```

### 2) Submit a URL

```bash
ship submit https://example.com
```

### 3) Preview metadata only

```bash
ship fetch https://example.com
```

## Common Commands

```bash
ship login
ship submit https://example.com
ship submit https://example.com --site aidirs.org
ship fetch https://example.com --json
ship version --latest
ship self-update
```

## Typical Results

### Login success

```text
✅ Login successful
```

### Submit success

```text
✅ Submitted successfully
```

### Unauthorized

```text
401 Unauthorized
```

Meaning: token is invalid or expired. Run `ship login` again.

### Subscription required

```text
402 Payment Required
```

Meaning: the account needs an active subscription. If the API returns `upgradeUrl`, show it to the user.

## Config

Default config file:

```text
~/.config/ship/config.json
```

Example structure:

```json
{
  "currentSite": "aidirs.org",
  "sites": {
    "aidirs.org": {
      "token": "xxx",
      "baseUrl": "https://aidirs.org"
    },
    "backlinkdirs.com": {
      "token": "yyy",
      "baseUrl": "https://backlinkdirs.com"
    }
  }
}
```

Rules:

- each site keeps its own token
- logging into one site does not overwrite another site's token
- `currentSite` points to the most recently used site
- if `--site` is omitted, `ship` uses `currentSite`

## Environment Variables

Config file takes priority. Environment variables are fallback only.

```bash
export DIRS_TOKEN="your-token-here"
export DIRS_BASE_URL="https://aidirs.org"
ship submit https://example.com
```

## Repo Layout

```text
skills/dirs-submit/
├─ SKILL.md
├─ README.md
├─ examples/
│  ├─ login-success.md
│  ├─ submit-success.md
│  ├─ submit-error-401.md
│  └─ submit-error-402.md
└─ references/
   ├─ api.md
   └─ config.md
```

- `SKILL.md`: agent-facing execution rules
- `examples/`: expected outputs and error cases
- `references/`: API and config details
