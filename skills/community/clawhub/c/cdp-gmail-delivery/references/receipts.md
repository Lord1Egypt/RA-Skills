# Receipts (Agent-Browser + Chrome Debug + CDP Gmail)

## 1) Agent-browser showed unauthenticated Gmail state

Observed repeatedly from `agent-browser open https://mail.google.com`:

- URL landed on Google sign-in
- Snapshot heading: `Sign in`
- Required manual login in visible desktop browser session

## 2) Shell script restart receipt

Command:

```bash
/home/little7/.openclaw/workspace/scripts/restart_debug_chrome.sh
```

Observed output:

- `==> Restarting Chrome debug session`
- `DISPLAY=:12.0`
- `==> DevTools is up`
- `Endpoint: http://127.0.0.1:9222/json/version`

## 3) CDP session proof (logged-in inbox)

Using Puppeteer CDP connection to `http://127.0.0.1:9222`:

- URL: `https://mail.google.com/mail/u/0/#inbox`
- Title example observed: `Inbox - little7.unifai@gmail.com - Gmail`

## 4) Final send + verification receipt

Terminal result from the successful run:

- `EMAIL_SENT_OK`
- `SUBJECT=TC20260413_0441.txt 202604130320`
- `TO=jouston@gmail.com`
- `FILE=/home/little7/.openclaw/media/inbound/TC20260413_0441.txt`

The flow verified Sent by unique subject before claiming success.

## 5) Attachment block receipt

User-confirmed Gmail compose state showed:

- `Blocked for security reasons!`
- Example blocked item: `cdp-gmail-delivery.skill.zip`

Operational change recorded: use Google Drive share-link fallback (and prefer Drive-first for skill bundles).

## 6) Script/repo context to include in publication

- Local scripts used:
  - `/home/little7/.openclaw/workspace/scripts/restart_debug_chrome.sh`
  - `/home/little7/.openclaw/workspace/tmp/xrdp_chrome_debug_setup.sh`
- Repository context where XRDP Chrome debug script appears in prior work:
  - `https://github.com/joustonhuang/unifai`
  - path mention: `scripts/xrdp_chrome_debug_setup.sh`
