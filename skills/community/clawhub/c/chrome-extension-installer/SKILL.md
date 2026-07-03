---
name: chrome-extension-installer
description: "Install a Chrome extension by ID or Chrome Web Store URL on this Mac."
user-invocable: true
---

# Chrome Extension Installer

Installs Chrome extensions to the user's Chrome profile on Ryans-MacBook-Air-2.local.

## Methods

### Method 1 — Chrome Web Store URL (preferred)
Open the extension's Chrome Web Store page directly in the user's Chrome. User clicks "Add to Chrome."

```bash
open -a "Google Chrome" "https://chromewebstore.google.com/detail/<extension-id>"
```

### Method 2 — Force-install via policy (no user click, macOS only)
For extensions that need silent install, use macOS Chrome policy. Requires the extension ID.

1. Write the extension ID to Chrome's managed preferences:
```bash
EXTENSION_ID="<id>"
PLIST="/Library/Managed Preferences/com.google.Chrome.plist"
sudo defaults write "$PLIST" ExtensionInstallForcelist -array-add "$EXTENSION_ID;https://clients2.google.com/service/update2/crx"
```
2. Relaunch Chrome — extension installs automatically.

### Method 3 — Load unpacked (dev/local extensions)
```bash
# Open Chrome with the extension loaded from a local directory
open -a "Google Chrome" --args --load-extension="/path/to/extension"
```

## Finding extension IDs
- From Chrome Web Store URL: `https://chromewebstore.google.com/detail/NAME/**<ID_IS_HERE>**`
- From installed extension: chrome://extensions → enable Developer Mode → ID shown under each extension

## Known extensions on this Mac (Chrome Default profile)
- html.to.design
- Anima
- Claude
- Codex (OpenClaw Browser Relay)
- Chrome Remote Desktop
- YouTube Summary by Glasp

## Notes
- Method 1 is always safe — opens the store page, user approves.
- Method 2 requires sudo and persists across Chrome updates.
- The OpenClaw sandbox browser (`profile=openclaw`) is separate from the user's Chrome profile — extensions installed here do NOT appear there.
