# Token Management

## Overview

`WorkosCursorSessionToken` is Cursor's session cookie that validates your subscription. It grants access to models included in your Cursor plan (e.g., Claude Sonnet 4).

**Characteristics:**
- Inherits your account's subscription benefits
- Expires periodically (hours to weeks)
- Must be refreshed when expired

## Obtaining Your Token

### Method 1: Browser DevTools (Recommended)

**Open DevTools:**

| Method | Action |
|--------|--------|
| Menu | Three-dot menu → More tools → Developer tools |
| Right-click | Right-click anywhere → Inspect |
| Command menu | `Cmd+Shift+P` → Search "Show DevTools" |
| Shortcut | `Cmd+Option+I` (Mac) / `F12` (Windows/Linux) |

**Steps:**

1. Ensure you're logged into https://cursor.com
2. Open DevTools using any method above
3. Click the **Application** tab in DevTools
4. In the left sidebar, expand **Cookies** → select `https://cursor.com`
5. Find `WorkosCursorSessionToken`
6. Copy the full **Value** (it's a long string)

### Method 2: CLI Verification

```bash
curl -s -o /dev/null -w "%{http_code}" \
  -H "Cookie: WorkosCursorSessionToken=your_token" \
  https://api2.cursor.com/v1/me
```
- Returns `200` = Valid
- Returns `401` = Expired

## Token Refresh Flow

**Step 1: Check if expired**
```bash
curl -s -o /dev/null -w "%{http_code}" \
  -H "Cookie: WorkosCursorSessionToken=your_token" \
  https://api2.cursor.com/v1/me
```

**Step 2: Refresh (if expired)**

1. Open https://cursor.com in your browser
2. Log out completely
3. Log back in
4. Refresh the page
5. Retrieve the new token from DevTools

**Step 3: Update Docker container**

```bash
# Stop old container
docker stop cursor-api
docker rm cursor-api

# Start with new token
docker run -d \
  --name cursor-api \
  -p 3010:3000 \
  -e WORKOS_CURSOR_SESSION_TOKEN=new_token \
  waitkafuka/cursor-api:latest
```

## Auto-Refresh Script

Create `~/scripts/cursor-token-refresh.sh`:

```bash
#!/bin/bash
set -e
CONTAINER_NAME="cursor-api"
NEW_TOKEN="$1"

if [ -z "$NEW_TOKEN" ]; then
    echo "❌ Usage: ./cursor-token-refresh.sh <new_token>"
    exit 1
fi

docker stop $CONTAINER_NAME 2>/dev/null || true
docker rm $CONTAINER_NAME 2>/dev/null || true

docker run -d \
  --name $CONTAINER_NAME \
  -p 3010:3000 \
  -e WORKOS_CURSOR_SESSION_TOKEN="$NEW_TOKEN" \
  waitkafuka/cursor-api:latest

echo "✅ Token updated"
```

Usage:
```bash
chmod +x ~/scripts/cursor-token-refresh.sh
~/scripts/cursor-token-refresh.sh "new_token"
```

## ⚠️ Security Notes

- **Never share your token** — anyone with it can access your Cursor account
- **Store securely** — use a password manager, never plaintext scripts
- **Handle expiry proactively** — expired tokens result in 401 errors
