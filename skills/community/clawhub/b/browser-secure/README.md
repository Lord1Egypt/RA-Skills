# 🔒 Browser Secure v2.0

> **Human-in-the-loop browser capture tool for gated content.**
> Companion to `attention-research` — when discovery finds a paywalled source, this is the key.

## Philosophy

**"Never trust, always verify, encrypt everything, audit all actions"**

Browser Secure is not an autonomous crawler. It is a **human-guided capture tool** that:
1. **Discovers** how to access a site (init)
2. **Hardens** the steps into a reusable playbook (init)
3. **Captures** content with approval at every step (capture)
4. **Records** findings into a structured scrapbook

Use it for: paywalled magazines, subscription news, academic papers, login-walled reports — any source your discovery tool flags as "gated."

**Not for:** OAuth/SSO, 2FA, social media, CAPTCHA, infinite-scroll apps.

---

## 🚀 Quick Start

```bash
# 1. Install
npm run install:full

# 2. Onboard a new site (creates playbook for future captures)
browser-secure init https://www.foreignaffairs.com --name "Foreign Affairs"
#    ↳ Auto-detects: login form, search box, content selectors
#    ↳ Takes screenshots at each step
#    ↳ HIL: confirm access, confirm login requirement, confirm recording

# 3. Capture an article (follows the hardened playbook)
browser-secure capture https://www.foreignaffairs.com/articles/iran-crisis --site foreignaffairs
#    ↳ HIL: approve site access, approve extraction, approve recording
#    ↳ Saves: screenshot, excerpt, (optionally) full text + raw HTML

# 4. View scrapbook
browser-secure scrapbook --list
browser-secure scrapbook --export markdown
```

---

## 📋 Core Workflow

### `init` — Site Onboarding

Explore a site once, harden the steps forever.

```bash
browser-secure init <url> [--name <name>]
```

**What happens:**
1. Navigate to URL
2. Auto-detect: login form, search input, navigation links, content selectors
3. Test first content link to derive extraction selectors
4. Take screenshots at each step (landing, analyzed, sample-content)
5. **HIL prompts:**
   - "Approve accessing this site?"
   - "Is login required?"
   - "Record this site profile and playbook?"

**Output:** Site profile + playbook saved to `~/.browser-secure/scrapbook/site-profiles.yaml`

**Playbook example:**
```yaml
playbook:
  discovery:
    method: search
    search_url: https://www.foreignaffairs.com
    search_input_selector: input[name="q"]
    search_submit_action: press enter
  access:
    login_required: true
    login_url: /login
  extraction:
    title_selector: h1
    body_selector: article
    author_selector: .author-name
    date_selector: time
```

### `capture` — Content Capture

Follow the playbook. Human approval at every gate.

```bash
browser-secure capture <url> --site <site-id> [options]
```

**Options:**
- `--yes` — Auto-approve all HIL steps (records `auto: true` honestly in approval chain)
- `--full-text` — Save complete article body, not just excerpt
- `--save-html` — Save raw page HTML alongside screenshot

**HIL steps (unless `--yes`):**
1. "Approve accessing {site}?"
2. (If login required) "Approve using vault credentials?"
3. "Approve extracting content from this page?"
4. "Record this capture? [shows preview]"

**Output:** Capture saved to `~/.browser-secure/scrapbook/captures.yaml`

**Artifacts stored:**
| Artifact | Location |
|----------|----------|
| Screenshot | `~/.browser-secure/scrapbook/screenshots/capture-{ts}.png` |
| Raw HTML | `~/.browser-secure/scrapbook/html/page-{ts}.html` (with `--save-html`) |
| Scrapbook YAML | `~/.browser-secure/scrapbook/captures.yaml` |

### `scrapbook` — View & Export

```bash
browser-secure scrapbook --list        # All captures
browser-secure scrapbook --sites       # All site profiles
browser-secure scrapbook --export markdown --output report.md
browser-secure scrapbook --export json --output report.json
```

---

## 🛡️ Security Model

Browser Secure inherits its security architecture from v1.x:

| Feature | Protection |
|---------|------------|
| **Vault Integration** | Credentials from Bitwarden/1Password/keychain, never CLI args |
| **Temp Profile Copies** | Real Chrome profiles copied to temp dirs — no SingletonLock conflicts |
| **Session Isolation** | UUID-based work dirs, auto-cleanup |
| **Approval Gates** | HIL at every step (site access, login, extraction, recording) |
| **Honest Audit** | Approval chain records `auto: true` vs `auto: false` |
| **Network Restrictions** | Blocks localhost/private IPs |

---

## 📖 Commands Reference

| Command | Description |
|---------|-------------|
| `browser-secure init <url>` | Onboard a site: analyze, detect, create playbook |
| `browser-secure capture <url> --site <id>` | Capture content using recorded playbook |
| `browser-secure capture <url> --yes --full-text --save-html` | Auto-approved, save everything |
| `browser-secure scrapbook --list` | List all captures |
| `browser-secure scrapbook --sites` | List site profiles with playbooks |
| `browser-secure scrapbook --export markdown` | Export to markdown |
| `browser-secure navigate <url>` | Simple navigation (legacy) |
| `browser-secure act "<instruction>"` | Natural language action (legacy) |
| `browser-secure daemon start --profile <id>` | Start persistent Chrome daemon |
| `browser-secure daemon stop` | Stop daemon |
| `browser-secure profile --list` | List Chrome profiles |
| `browser-secure config --edit` | Edit configuration |

---

## ⚙️ Configuration

`~/.browser-secure/config.yaml`:

```yaml
vault:
  provider: bitwarden  # bitwarden | 1password | keychain | env
  sites:
    foreignaffairs:
      vault: "Personal"
      item: "Foreign Affairs"
      usernameField: "email"
      passwordField: "password"

security:
  screenshotEveryAction: false  # Disable for faster crawling

isolation:
  incognitoMode: true
  secureWorkdir: true
  autoCleanup: true
```

---

## 🔐 Vault Providers

### Bitwarden (Recommended - Free)

```bash
brew install bitwarden-cli
bw login
export BW_SESSION=$(bw unlock --raw)
```

### 1Password (Paid)

```bash
brew install 1password-cli
op signin
eval $(op signin)
```

### macOS Keychain (Local)

### Environment Variables (Fallback)

```bash
export BROWSER_SECURE_FOREIGNAFFAIRS_USERNAME="user@example.com"
export BROWSER_SECURE_FOREIGNAFFAIRS_PASSWORD="secret"
```

---

## 🆘 Troubleshooting

**"No site profile found"**
```bash
browser-secure init <url>   # Run init first
```

**"URL already captured"**
Dedup is automatic. Use `scrapbook --list` to see existing captures.

**Vault locked**
```bash
export BW_SESSION=$(bw unlock --raw)   # Bitwarden
eval $(op signin)                       # 1Password
```

**Chrome keychain prompt**
Normal on first run. Click "Deny" — Browser Secure uses your vault, not Chrome's password storage.

---

## 📄 License

MIT-0

---

## 🔗 Links

- [OpenClaw Documentation](https://docs.openclaw.ai)
- [Bitwarden](https://bitwarden.com)
- [1Password](https://1password.com)
- [Report Issues](https://github.com/NMC-Interactive/browser-secure/issues)
