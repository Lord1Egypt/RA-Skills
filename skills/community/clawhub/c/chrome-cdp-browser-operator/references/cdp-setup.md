# CDP Setup

## Preferred mode

Launch a dedicated Chrome profile and expose the debugging port:

```powershell
chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\chrome\x-profile"
```

Keep that browser logged in. The operator then attaches to `http://127.0.0.1:9222`.

## Why a fallback exists

CDP attachment is convenient because it reuses the already logged-in profile. When attachment becomes flaky, the skill can launch a persistent context directly with Playwright and the same profile path.
