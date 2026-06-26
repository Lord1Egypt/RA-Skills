# captcha-relay

Human-in-the-loop CAPTCHA solving. No third-party solving services. No API keys. Just you and your phone.

## Two Modes

### 📸 Screenshot Mode (default) — Zero infrastructure

Captures the CAPTCHA as a screenshot with a numbered grid overlay, sends it to you (via Telegram, etc.), you reply with cell numbers, and clicks are injected into the browser.

**Works for any CAPTCHA type.** No network setup needed.

```bash
node index.js                   # screenshot mode is the default
node index.js --mode screenshot # explicit
```

### 🔑 Token Relay Mode — Native solving

Detects the CAPTCHA type and sitekey, serves the real CAPTCHA widget on a relay page, you solve it natively on your phone, and the token is injected back via CDP.

**Requires network access** (Tailscale or tunnel) so your phone can reach the relay server.

```bash
node index.js --mode relay              # with localtunnel
node index.js --mode relay --no-tunnel  # with Tailscale/LAN
```

## Quick Start

### Screenshot Mode (easiest)

```bash
cd captcha-relay
npm install
# Launch Chrome with CDP:
chromium --remote-debugging-port=18800

# In another terminal:
node index.js
# → Outputs annotated screenshot path as JSON
# → Send image to human, get cell numbers back, inject clicks
```

### Token Relay Mode

**With Tailscale (recommended):**

```bash
# Install Tailscale on both your server and phone
# See TAILSCALE.md for details

node index.js --mode relay --no-tunnel
# → Outputs relay URL as JSON
# → Open URL on phone, solve CAPTCHA, token auto-injected
```

**With localtunnel:**

```bash
node index.js --mode relay
# → Creates public tunnel URL automatically
```

## Module API

```js
const { solveCaptcha, solveCaptchaScreenshot, injectGridClicks } = require('captcha-relay');

// Screenshot mode
const capture = await solveCaptchaScreenshot({ cdpPort: 18800 });
// capture.imagePath, capture.prompt, capture.rows, capture.cols

// Token relay mode
const result = await solveCaptcha({ cdpPort: 18800, useTunnel: false });
// result.relayUrl, result.token, result.solved
```

## CLI Options

| Flag | Description | Default |
|------|-------------|---------|
| `--mode screenshot\|relay` | Solving mode | `screenshot` |
| `--screenshot` | Alias for `--mode screenshot` | — |
| `--cdp-port N` | Chrome DevTools Protocol port | `18800` |
| `--timeout N` | Timeout in seconds | `120` |
| `--no-tunnel` | Skip tunnel, use local/Tailscale IP | off |
| `--no-inject` | Return token without injecting | off |

## How It Works

```
Screenshot Mode:                    Token Relay Mode:
                                    
Browser hits CAPTCHA                Browser hits CAPTCHA
       ↓                                   ↓
Screenshot + grid overlay           Detect type + sitekey via CDP
       ↓                                   ↓
Send image to human                 Start relay server (real widget)
       ↓                                   ↓
Human replies: "1,3,5"             Generate URL → send to phone
       ↓                                   ↓
Inject clicks at grid cells         Human solves CAPTCHA natively
       ↓                                   ↓
Automation continues ✓              Token injected via CDP
                                           ↓
                                    Automation continues ✓
```

## Supported CAPTCHAs

| Type | Screenshot | Token Relay |
|------|-----------|-------------|
| reCAPTCHA v2 | ✅ | ✅ Tested |
| hCaptcha | ✅ | ✅ Supported |
| Cloudflare Turnstile | ✅ | ✅ Supported |
| Sliders, text, custom | ✅ | ❌ |

## Network Setup (Relay Mode Only)

See [TAILSCALE.md](TAILSCALE.md) for detailed Tailscale setup.

| Method | How | Trade-offs |
|--------|-----|------------|
| **Tailscale** | `--no-tunnel` | Always-on, encrypted, no splash pages |
| **localtunnel** | Default | Works anywhere, has splash page |
| **LAN** | `--no-tunnel` | Same WiFi only |

## Architecture

See [ARCHITECTURE.md](ARCHITECTURE.md) for the full breakdown.

## License

MIT
