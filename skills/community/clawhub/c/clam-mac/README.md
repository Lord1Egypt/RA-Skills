<h1 align="center"><img src="assets/logo.png" alt="" width="64" style="vertical-align: middle;">&nbsp; CLAM — CLI on Mac</h1>


<p align="center">
  <a href="docs/README-zh.md">中文</a> | English
</p>

<p align="center">
  <strong>Give any AI Agent hands to control your Mac.</strong><br>
  Auto-discover apps. Generate CLI wrappers. Return structured JSON.
</p>

<p align="center">
  <a href="https://pypi.org/project/clam-mac/"><img src="https://img.shields.io/pypi/v/clam-mac" alt="PyPI"></a>
  <img src="https://img.shields.io/badge/platform-macOS-lightgrey" alt="macOS">
  <img src="https://img.shields.io/badge/python-3.10%2B-blue" alt="Python 3.10+">
  <img src="https://img.shields.io/badge/license-MIT-green" alt="MIT">
</p>

<br>

Your Mac has dozens of apps, but AI can't touch any of them. CLAM fixes that — it scans installed apps, generates typed CLI wrappers on the fly, and gives every command structured JSON output. No APIs, no manual adapters, no AppleScript headaches.

## See It In Action

<table>
<tr>
<td width="45%">
<a href="https://youtu.be/LBmZHGgEl9I">
<img src="assets/demo-getting-started.jpg" width="100%">
</a>
</td>
<td valign="middle" width="55%">
<strong>🚀 Three Commands, 10 Seconds, Any App</strong><br><br>
<code>pip install clam-mac</code> → <code>clam scan</code> → <code>clam install</code> — and any Mac app is AI-controllable. Watch CLAM auto-discover 50+ apps and configure MCP in one go.
</td>
</tr>
<tr><td colspan="2"><br></td></tr>
<tr>
<td width="45%">
<a href="https://youtu.be/G1IOv1YUPQU">
<img src="assets/demo-email.jpg" width="100%">
</a>
</td>
<td valign="middle" width="55%">
<strong>📧 AI Reads Your Email — No API Key Needed</strong><br><br>
Ask "what unread emails do I have?" — AI reads Apple Mail in real time. No OAuth, no Gmail API, no hacks.
</td>
</tr>
<tr><td colspan="2"><br></td></tr>
<tr>
<td width="45%">
<a href="https://youtu.be/3WD85V0U4eo">
<img src="assets/demo-calendar.jpg" width="100%">
</a>
</td>
<td valign="middle" width="55%">
<strong>📅 Daily Briefing in One Prompt</strong><br><br>
"What's on my plate today?" — AI reads Calendar + Reminders and hands you a to-do list. Zero copy-paste.
</td>
</tr>
<tr><td colspan="2"><br></td></tr>
<tr>
<td width="45%">
<a href="https://youtu.be/P95UukSavsI">
<img src="assets/demo-spotify.jpg" width="100%">
</a>
</td>
<td valign="middle" width="55%">
<strong>🎵 Control Spotify from Your AI Chat</strong><br><br>
Say "我想听稻香" — it just works. AI plays, pauses, skips, queries. Voice-control your music, zero config.
</td>
</tr>
</table>

## Install

```bash
pip install clam-mac
```

> **`pip` not found or `externally-managed-environment` error?**
> macOS ships with `pip3` (not `pip`), and Python 3.12+ blocks direct installs. Use a virtual environment:
> ```bash
> python3 -m venv ~/clam-env
> source ~/clam-env/bin/activate
> pip install clam-mac
> ```
> Add `source ~/clam-env/bin/activate` to your `~/.zshrc` to make it permanent.

## Quick Start

```bash
clam scan                              # discover controllable apps
clam install music                     # generate CLI wrapper (~10s)
clam-music play                        # play music
clam-music --json get-current-track    # → structured JSON
clam-music set-sound-volume 50         # set volume
clam-mail list-inbox-messages --unread # list unread emails
```

Fuzzy matching built in: `chrome` → `google-chrome`, `word` → `microsoft-word`.

## Use with AI Agents

### Claude Code (MCP)

```bash
pip install clam-mac
clam mcp-setup
```

That's it — `clam mcp-setup` auto-detects the `clam-mcp` binary and registers it with Claude Code. Restart Claude Code, then just ask:

> "Set volume to 50 and tell me what song is playing"
> "List my unread emails"
> "Open the Downloads folder in Finder"

Claude will automatically call `clam_find_app` → `clam_install` → `clam_execute` — no manual setup per app.

**Available MCP tools:**

| Tool | Description |
|------|-------------|
| `clam_find_app(query)` | Instant app lookup — always start here |
| `clam_install(app_id)` | Generate + install CLI wrapper (~10s) |
| `clam_info(app_id)` | List all available commands and properties |
| `clam_execute(app_id, command, args?)` | Run a command, returns JSON |
| `clam_scan()` | Full scan of all controllable apps |
| `clam_doctor(app_id)` | Check command reliability |

### OpenClaw

Install from [ClawHub](https://clawhub.ai):

```bash
clawhub install clam-mac
```

Once installed, the AI auto-discovers apps via `clam_find_app`, installs wrappers, and executes commands.

### Any Other Agent

CLAM generates standard CLI tools. Anything that can call shell commands works:

```python
import subprocess, json
result = subprocess.run(
    ["clam-music", "--json", "get-current-track"],
    capture_output=True, text=True
)
track = json.loads(result.stdout)
```

## How It Works

CLAM auto-selects the best automation mode for each app:

| Mode | Mechanism | Apps | Commands |
|------|-----------|------|----------|
| **Full** | `.sdef` scripting definitions | Music, Finder, Mail, Chrome, Safari, Word | Dozens to hundreds |
| **UI Scripting** | Menu clicks via Accessibility | Figma, Slack, VS Code, Spotify | All menu items |
| **Basic** | macOS standard suite | DingTalk, WeChat, WPS | Activate, quit, open, version |

No configuration needed — `clam install` picks the right mode automatically.

## Commands

```bash
clam scan              # list controllable apps
clam install <app>     # generate + install CLI wrapper
clam info <app>        # show available commands
clam doctor <app>      # check command reliability
clam list              # list installed wrappers
clam remove <app>      # uninstall wrapper
```

## What's New in v0.2.0

- **Collection queries** — apps with scripting definitions now support `list-<container>-<items>` commands (e.g. `clam-mail list-inbox-messages --unread`)
- **Chinese app support** — QQ Music, WeChat, and other apps with non-ASCII names now install correctly
- **MCP PATH fix** — `clam_execute` reliably finds wrapper binaries regardless of PATH in the MCP server context
- **Better `clam_info`** — shows commands for basic-mode apps and list commands for sdef apps

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `clam-xxx` not found | `source ~/clam-env/bin/activate` or check your `PATH` |
| Permission denied | System Settings > Privacy & Security > Automation |
| UI Scripting error | System Settings > Privacy & Security > Accessibility |
| Only basic commands | App has no scripting support — basic mode is the max |
| MCP tool not found | Restart Claude Code after `claude mcp add` |

## License

[MIT](LICENSE)
