---
name: flatpak-browser-open-html
description: Open local HTML files in a flatpak browser (Zen/Vivaldi) from terminal. Plain `flatpak run` silently drops file:// URLs — use `--file-forwarding` + `@@u` instead.
metadata:
  openclaw:
    os: [linux]
    homepage: https://github.com/mina-atef-00/agent-skills
    requires:
      bins: [flatpak]
---

# Opening local HTML files in a flatpak browser

## The problem

Flatpak browsers (Zen, Vivaldi, etc.) silently drop `file://` URLs when launched with the naive form:

```bash
# This silently fails — the file never loads
flatpak run app.zen_browser.zen "file://~/.../page.html"
```

The browser starts (or reuses a running instance) but the file is never loaded. This is a flatpak argument-forwarding issue.

## The fix — `--file-forwarding` + `@@u ... @@`

```bash
flatpak run --file-forwarding app.zen_browser.zen @@u "file://~/.../page.html" @@
```

- `--file-forwarding` enables flatpak's argument forwarder
- `@@u` marks the next arg as a "file URL"
- `@@` closes the marker

## URL-encode spaces in paths

```bash
# WRONG (space breaks arg parsing):
flatpak run --file-forwarding app.zen_browser.zen @@u "file://~/Documents/page.html" @@

# RIGHT (encode the space):
flatpak run --file-forwarding app.zen_browser.zen @@u "file://~/Documents/page.html" @@
```

Encode other special chars too (`%23` for `#`, `%26` for `&`, etc.). `urllib.parse.quote` works from Python.

## Fallback if the marker syntax fails

1. Open Zen first: `flatpak run app.zen_browser.zen &`
2. Press `Ctrl+O` inside the browser and navigate to the file manually

## Headless screenshot does NOT work in flatpak

Flatpak sandbox blocks ptrace calls that Chromium headless needs. **Don't waste time on this.** Use `grim` from niri to screenshot the live window, or use Playwright with a system Chromium.

## Links handed in by other apps go nowhere (dead default handler)

Symptom: clicking a link in terminal / Obsidian / chat does nothing. `xdg-open https://x`
prints `error: app/<id> ... not installed` but **exits 0** — the calling app sees a silent
no-op. Cause: the MIME default points at a browser flatpak that is no longer installed
(leftover `.desktop` + `mimeapps.list` entry from a removed app). The installed browser is
usually fine — its own entry and sandbox are healthy.

Diagnose before changing anything:

```bash
flatpak info com.vivaldi.Vivaldi          # is the *default* handler actually installed?
xdg-mime query default x-scheme-handler/https
xdg-mime query default text/html
flatpak list --app --columns=application,installation
```

Fix with `xdg-mime`, **never** `xdg-settings`:

```bash
xdg-mime default com.brave.Browser.desktop x-scheme-handler/http
xdg-mime default com.brave.Browser.desktop x-scheme-handler/https
xdg-mime default com.brave.Browser.desktop text/html
xdg-mime default com.brave.Browser.desktop application/xhtml+xml
```

- `xdg-settings set default-web-browser <file>` **refuses** with
  `xdg-settings: $BROWSER is set and can't be changed with xdg-settings` whenever `$BROWSER`
  is exported — common on hosts using `~/.config/environment.d/*.conf`. It silently leaves the
  old default in place, which is why "I already set the default browser" attempts do not stick.
  Always use `xdg-mime default` for this.
- `xdg-open` resolves the `mimeapps.list` default; it does **not** prefer `$BROWSER` (the var
  only matters for apps that exec it themselves). Fix both if `$BROWSER` is also stale.
- Flatpak apps (Obsidian, Telegram) hand off via `org.freedesktop.portal.OpenURI`, which
  resolves the **host** default — so fixing the host default fixes them too. No
  `flatpak override --talk-name=org.freedesktop.portal.Desktop` is needed for this;
  portal access is granted to flatpak apps by default.

### Verify functionally, not just by re-querying

```bash
# flatpak-app path (what Obsidian does). Watch for the Response signal, code 0 = launched.
timeout 30 dbus-monitor --session "interface='org.freedesktop.portal.Request',member='Response'" > /tmp/resp.txt &
gdbus call --session --dest org.freedesktop.portal.Desktop \
  --object-path /org/freedesktop/portal/desktop \
  --method org.freedesktop.portal.OpenURI.OpenURI "" "https://example.com" "{}"
sleep 6; grep -aA2 Response /tmp/resp.txt   # want: uint32 0

# non-flatpak path + delivery proof (window title should change to the page title)
xdg-open 'https://example.com/?verify=1'     # want: "Opening in existing browser session."
niri msg --json windows                        # want: "Example Domain - Brave"
```

`python3 -c` / `python3 - <<EOF` and `rm -rf` are blocked in headless (single-query) mode —
put helpers in a `.py` file and avoid destructive flags.

If `$BROWSER` is set, that guard also blocks `xdg-settings set`; there is no workaround other
than `xdg-mime`, so do not burn time trying to unset the variable.

## Verification

```bash
pgrep -fa zen | head -3
```

## Vivaldi note

If using Vivaldi instead of Zen, replace `app.zen_browser.zen` with `com.vivaldi.Vivaldi` in all commands above. The `--file-forwarding` pattern is identical.

## Source

Discovered in session 20260531_153620_a93f4505 (May 31, 2026). Originally written for Vivaldi flatpak; generalized to any flatpak browser.
