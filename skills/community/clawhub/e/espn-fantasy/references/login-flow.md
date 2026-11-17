# ESPN login flow — lessons & details

Hard-won specifics for re-authenticating ESPN (Disney One-ID). Read this when the login
script fails or needs updating.

## Page structure (`https://www.espn.com/login`)

- Main page embeds a cross-origin iframe:
  `https://cdn.registerdisney.go.com/v2/ESPN-ONESITE.WEB-PROD/en-US?...`
  with `name="disneyid-iframe"` — **this is where the real form is.**
- A second iframe `espn.com/login/responder/` handles the postMessage handshake.
- A Google reCAPTCHA Enterprise frame (`size=invisible`) is loaded alongside.

### Selectors (inside `disneyid-iframe`)

| Element | Selector | Notes |
|---|---|---|
| Email | `input[type=email]` | placeholder "Username or Email Address" |
| Password | `input[type=password]` | placeholder "Password (case sensitive)" |
| Hidden session | `input#session-id` | ignore |
| Submit | `button[type=submit]` | "Log In" |
| 2FA code | `input[name=code][type=tel]` | appears on "Check Your Email" screen |
| 2FA continue | `button[type=submit]` | |

## Failure modes seen

1. **`Max challenge attempts exceeded. Please refresh...`** → two distinct causes:
   - On `chrome-headless-shell` (Playwright default `headless:true`): the stripped build can't
     clear the invisible reCAPTCHA. Fix: full Chromium new-headless, or better, **headed**.
   - On a **poisoned profile** after repeated failed attempts: even a headed browser on a
     fresh X display gets this. Fix: delete the profile dir and use a **fresh** profile
     (`ESPN_PROFILE=state/espn-profile-fresh`). A clean profile loads the login form cleanly.
2. **`Sorry, we are unable to send you any more codes right now. Please try again later.`** →
   ESPN code-send rate limit (**account-level**, independent of browser/profile). Cause:
   repeated/rapid login attempts. Back off (~12 min) and retry **once**. No parallel attempts.
3. **Stuck after code submit with no result** → the page can sit on the prompt or an error
   with no navigation. Always log the iframe text after submit so you can see
   "incorrect/expired code" vs success.

## Timings / behaviour

- Login page → disney iframe present: a few seconds; poll up to ~30s.
- After submit → 2FA prompt or rate-limit message: ~8s.
- After correct code → cookies set within ~10s. Success signal = `espn_s2` cookie exists.
- 2FA email code: single-use, expires ~10 min.

## Environment notes (this box)

- **Headed browser needs a display, and there isn't a usable one.** `:0` is root/SDDM and
  `:10` belongs to another user; no Xvfb; no passwordless sudo. Solution: **TigerVNC**
  (`vncserver` + `Xvnc` are installed) to create our own virtual headed display:
  `vncserver :1 -geometry 1366x900 -depth 24 -SecurityTypes None -localhost yes`
  then `DISPLAY=:1 XAUTHORITY=$HOME/.Xauthority`. See `scripts/start-display.sh`.
- Playwright module: install playwright locally (`npm i playwright`) or set `PLAYWRIGHT_PATH`,
  which matches the installed `chromium-1208` build. The npx-cached 1.63 expects
  `chromium-1243` (not installed).
- Full Chromium binary: `~/.cache/ms-playwright/chromium-1208/chrome-linux64/chrome`.
- Persistent profile dir: `state/espn-profile/` (cookies + localStorage survive). Override
  with `ESPN_PROFILE` to use a fresh profile when the default one is poisoned.
- Firefox exists (`/usr/bin/firefox`) but Playwright's Firefox build is not installed, so we
  stick with Playwright Chromium.

## Self-match kill trap

`pkill -f login-interactive` / `pgrep -f '...' | xargs kill` matches the **calling shell**
(its own cmdline contains the pattern) and SIGTERMs the whole exec. Kill safely with:

```bash
for p in $(pgrep -x node); do grep -qa login-interactive /proc/$p/cmdline && kill "$p"; done
```

## Cookie → API handoff

`espn_s2` (long) + `SWID` (GUID, looks like `{XXXXXXXX-....}`) are saved to
`.secrets/espn-cookies.txt` (600). `SWID` may exist even before login — only trust success
when **`espn_s2`** is present.

## When ESPN accepts the password but shows no OTP box (throttled state)

Observed 2026-10-01 after several rapid attempts:

- `POST https://registerdisney.go.com/jgc/v6/client/ESPN-ONESITE.WEB-PROD/guest/login`
  returns **HTTP 400** with body:
  `{"error":{"keyCategory":"FAILURE_BY_DESIGN","errors":[{"code":"AUTHORIZATION_OTP_VERIFICATION_REQUIRED",...}]}}`
  → This is **NOT** a bad password. It means **credentials are valid, OTP required.**
- But when the account/session is throttled, ESPN then **silently redirects to
  `https://www.espn.com/`** (~1.5s after submit) and **never renders the OTP entry screen**.
  Fast polling (500ms) confirms the "Check Your Email / Enter the code" UI never appears.
- On a CLEAN session (first attempt), the OTP screen DOES render in the Disney iframe.
- Frame names vary: `disneyid-iframe` / `disneyid-secure-responder` on the login page,
  and `oneid-iframe` / `oneid-secure-responder` elsewhere. Match by
  `/registerdisney/` on the URL, not just the name.

**Conclusion:** the blocker is ESPN anti-abuse throttling, not the browser mode.
Fix = stop poking it, **cool off ~1h**, then ONE clean headed attempt.
(Alternative that always works: have the user copy `espn_s2` + `SWID` from their own
browser DevTools → Cookies → espn.com.)

### Diagnosis commands used
- Log every `page.on('response')` for `/guest/login|otp|mfa/` and print the body.
- `page.frames().filter(f => /registerdisney/.test(f.url()))` and dump each frame's
  `innerText` + `input`s + `button`s.

### Detection gotcha: hidden OTP text causes FALSE POSITIVES

The Disney/OneID widget keeps the OTP screen's text in the DOM even when it's not shown,
so `document.body.innerText.includes('Check Your Email')` can match while the page is actually
on the LOGIN form / homepage. Confirm with a **screenshot** and by checking
`element.offsetParent !== null` / `getBoundingClientRect()` visibility of the code input —
don't trust innerText alone.
