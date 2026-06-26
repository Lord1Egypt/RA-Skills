# browseros-cli Command Reference

## Global Flags

| Flag | Env Var | Description |
|------|---------|-------------|
| `--server, -s` | `BROWSEROS_URL` | Server URL (auto-detected from `~/.browseros/server.json`) |
| `--page, -p` | `BROWSEROS_PAGE` | Target page ID (default: active page) |
| `--json` | `BOS_JSON=1` | JSON output (structured content) |
| `--debug` | `BOS_DEBUG=1` | Debug output |
| `--timeout, -t` | | Request timeout (default: 2m) |

Server URL resolution: `--server` flag → `BROWSEROS_URL` env → `~/.browseros/server.json` → `~/.config/browseros-cli/config.yaml`

## Navigate

| Command | Usage | Description |
|---------|-------|-------------|
| `open <url>` | `browseros-cli open https://example.com` | Open new tab |
| `open --hidden <url>` | `browseros-cli open --hidden https://example.com` | Open hidden tab |
| `open --bg <url>` | `browseros-cli open --bg https://example.com` | Open in background |
| `open --window <id> <url>` | `browseros-cli open --window 2 https://example.com` | Open in specific window |
| `nav <url>` | `browseros-cli nav https://example.com` | Navigate current tab |
| `back` | `browseros-cli back` | Go back |
| `forward` | `browseros-cli forward` | Go forward |
| `reload` | `browseros-cli reload` | Reload page |
| `pages` | `browseros-cli pages` | List all tabs with IDs |
| `active` | `browseros-cli active` | Show active tab |
| `close [pageId]` | `browseros-cli close 15` | Close a tab |

## Observe

| Command | Usage | Description |
|---------|-------|-------------|
| `snap` | `browseros-cli snap` | Accessibility tree with element IDs |
| `snap -e` | `browseros-cli snap -e` | Enhanced snapshot with structural context |
| `text` | `browseros-cli text` | Page content as markdown |
| `text --selector <css>` | `browseros-cli text --selector ".main"` | Scoped extraction |
| `text --links` | `browseros-cli text --links` | Include links as `[text](url)` |
| `text --images` | `browseros-cli text --images` | Include image references |
| `text --viewport` | `browseros-cli text --viewport` | Only visible content |
| `links` | `browseros-cli links` | All links on page |
| `ss` | `browseros-cli ss` | Screenshot (saves to `screenshot.png`) |
| `ss -o <path>` | `browseros-cli ss -o /tmp/shot.png` | Screenshot to file |
| `ss --full` | `browseros-cli ss --full` | Full page screenshot |
| `ss --format <fmt>` | `browseros-cli ss --format jpeg` | Image format (png, jpeg, webp) |
| `ss --quality <n>` | `browseros-cli ss --quality 80` | Compression quality (jpeg/webp) |
| `eval "<js>"` | `browseros-cli eval "document.title"` | Run JavaScript |
| `dom` | `browseros-cli dom` | Raw HTML DOM |
| `dom --selector <css>` | `browseros-cli dom --selector "#main"` | Scoped DOM |
| `dom-search <query>` | `browseros-cli dom-search "Submit"` | Search DOM (max 25 results) |
| `dom-search --limit <n>` | `browseros-cli dom-search "Submit" --limit 10` | Limit search results |
| `wait --text <text>` | `browseros-cli wait --text "Success"` | Wait for text |
| `wait --selector <css>` | `browseros-cli wait --selector ".loaded"` | Wait for selector |
| `wait --wait-timeout <ms>` | `browseros-cli wait --text "Done" --wait-timeout 30000` | Custom timeout (default: 10000ms) |

## Input

| Command | Usage | Description |
|---------|-------|-------------|
| `click <id>` | `browseros-cli click 12` | Click element |
| `click --right <id>` | `browseros-cli click --right 12` | Right-click |
| `click --middle <id>` | `browseros-cli click --middle 12` | Middle-click |
| `click --double <id>` | `browseros-cli click --double 12` | Double-click |
| `click-at <x> <y>` | `browseros-cli click-at 100 200` | Click coordinates |
| `fill <id> <text>` | `browseros-cli fill 5 "hello"` | Type into input |
| `fill --no-clear <id> <text>` | `browseros-cli fill --no-clear 5 "more"` | Append text |
| `clear <id>` | `browseros-cli clear 5` | Clear input |
| `key <key>` | `browseros-cli key Enter` | Press key |
| `key <combo>` | `browseros-cli key Control+A` | Key combination |
| `hover <id>` | `browseros-cli hover 8` | Hover element |
| `focus <id>` | `browseros-cli focus 8` | Focus element |
| `check <id>` | `browseros-cli check 10` | Check checkbox/radio |
| `uncheck <id>` | `browseros-cli uncheck 10` | Uncheck checkbox |
| `select <id> <value>` | `browseros-cli select 7 "Option A"` | Select dropdown |
| `scroll <dir> [amount]` | `browseros-cli scroll down 500` | Scroll page (default amount: 3) |
| `scroll --element <id> <dir>` | `browseros-cli scroll --element 5 down` | Scroll within element |
| `drag <src> --to <tgt>` | `browseros-cli drag 5 --to 12` | Drag element |
| `upload <id> <file...>` | `browseros-cli upload 3 photo.jpg` | Upload file(s) |
| `dialog accept` | `browseros-cli dialog accept` | Accept JS dialog |
| `dialog dismiss` | `browseros-cli dialog dismiss` | Dismiss JS dialog |
| `dialog accept --text "answer"` | `browseros-cli dialog accept --text "answer"` | Accept prompt with text |

## Files & Export

| Command | Usage | Description |
|---------|-------|-------------|
| `pdf <path>` | `browseros-cli pdf page.pdf` | Save page as PDF |
| `download <id> <dir>` | `browseros-cli download 8 ./downloads` | Download via element click |

## Resources (subcommands)

### bookmark

| Command | Usage | Description |
|---------|-------|-------------|
| `bookmark list` | `browseros-cli bookmark list` | List all bookmarks |
| `bookmark search <q>` | `browseros-cli bookmark search "recipe"` | Search bookmarks |
| `bookmark create <title> [url]` | `browseros-cli bookmark create "My Page" https://example.com` | Create bookmark |
| `bookmark create --parent <id>` | `browseros-cli bookmark create --parent "1" "Folder"` | Create in folder |
| `bookmark remove <id>` | `browseros-cli bookmark remove "abc123"` | Remove bookmark |
| `bookmark update <id>` | `browseros-cli bookmark update "abc" --title "New" --url "..."` | Update bookmark |
| `bookmark move <id>` | `browseros-cli bookmark move "abc" --parent "folder1" --index 0` | Move bookmark |

### history

| Command | Usage | Description |
|---------|-------|-------------|
| `history recent` | `browseros-cli history recent` | Recent history |
| `history recent --max <n>` | `browseros-cli history recent --max 50` | Limit results |
| `history search <q>` | `browseros-cli history search "github"` | Search history |
| `history search --max <n>` | `browseros-cli history search "github" --max 10` | Limit search |
| `history delete <url>` | `browseros-cli history delete "https://..."` | Delete URL from history |
| `history delete-range` | `browseros-cli history delete-range --start 1000 --end 2000` | Delete time range (epoch ms) |

### group (Tab Groups)

| Command | Usage | Description |
|---------|-------|-------------|
| `group list` | `browseros-cli group list` | List all tab groups |
| `group create <pageId...>` | `browseros-cli group create 1 2 3 --title "Research"` | Group tabs |
| `group update <id>` | `browseros-cli group update 1 --title "Done" --color green` | Update group |
| `group update --collapsed` | `browseros-cli group update 1 --collapsed` | Collapse group |
| `group ungroup <pageId...>` | `browseros-cli group ungroup 1 2` | Remove pages from groups |
| `group close <id>` | `browseros-cli group close 1` | Close group + all tabs |

**Group colors:** grey, blue, red, yellow, green, pink, purple, cyan, orange

### window

| Command | Usage | Description |
|---------|-------|-------------|
| `window list` | `browseros-cli window list` | List all windows |
| `window create` | `browseros-cli window create` | Create new window |
| `window create --hidden` | `browseros-cli window create --hidden` | Create hidden window |
| `window close <id>` | `browseros-cli window close 2` | Close window |
| `window activate <id>` | `browseros-cli window activate 2` | Focus window |

## Setup

| Command | Description |
|---------|-------------|
| `install` | Download BrowserOS for current platform |
| `install --dir <path>` | Download to specific directory |
| `install --deb` | Download .deb package (Linux only) |
| `launch` | Find and start BrowserOS |
| `launch --wait <seconds>` | Wait timeout for server ready (default: 30) |
| `init --auto` | Auto-discover server, save config |
| `init <url>` | Non-interactive config |
| `init` | Interactive config |
| `health` | Check server health |
| `status` | Check extension/runtime status |
| `config` | Open config in $EDITOR |
| `config --path` | Print config file path |
| `info [topic]` | BrowserOS feature info |

## Installation

```bash
# Install via npm
npm install -g browseros-cli

# Or run directly without installing
npx browseros-cli --help
```
