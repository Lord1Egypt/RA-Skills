# Bilibili Cookie Setup Guide

## Why Cookie is Needed

Bilibili requires authentication to download AI-generated subtitles (`ai-zh`, `ai-en`) and official subtitles (`zh-CN`, `zh-Hans`, `en-US`). Without a cookie, only danmaku XML is available.

## How to Get Your SESSDATA Cookie

1. Open [bilibili.com](https://www.bilibili.com) and **log in** to your account
2. Press `F12` → go to **Console** tab
3. Run:
   ```javascript
   console.log(document.cookie.match(/SESSDATA=([^;]+)/)?.[1])
   ```
4. Copy the returned string (it looks like: `fa88e7f6%2C1789869469%2C0c9b8%2A31...`)

## How to Save the Cookie

### Method 1: Tell the Agent to Save It
When the agent asks for your cookie, paste the full cookie string. The agent will save it to `~/.config/bilibili-cookies.txt` automatically.

### Method 2: Manual Save
Save the cookie as a **Netscape HTTP Cookie File**:

```
# ~/.config/bilibili-cookies.txt (Netscape format)
.bilibili.com	TRUE	/	TRUE	0	SESSDATA	YOUR_SESSDATA_VALUE_HERE
```

The agent will look for this file at `~/.config/bilibili-cookies.txt`.

## Cookie Format Reference

The cookie file must be in **Netscape format**. Minimal required fields:

```
.bilibili.com	TRUE	/	TRUE	0	SESSDATA	YOUR_SESSDATA_HERE
```

**Key fields:**
- `domain`: `.bilibili.com`
- `include_subdomains`: `TRUE`
- `path`: `/`
- `secure`: `TRUE`
- `expiry`: `0` (session)
- `name`: `SESSDATA`
- `value`: your SESSDATA string

## Cookie Expiry

B站 cookies typically expire in **~30 days**. When subtitle downloads stop working, re-fetch your SESSDATA and update the cookie file using the same process above.

## Privacy Note

The cookie only allows the agent to download subtitles on your behalf. It does **not** give the agent control of your account. However:
- Only use this in a trusted environment
- The cookie is stored locally in `~/.config/bilibili-cookies.txt` and never sent elsewhere
- You can revoke the cookie anytime via your [B站账号设置](https://account.bilibili.com/account/security)
