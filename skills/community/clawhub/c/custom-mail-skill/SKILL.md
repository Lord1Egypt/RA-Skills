---
name: custom-mail
description: Run the Custom Mail console locally with Docker — compose, preview, attachments, send history, and pluggable provider / theme / layout / logo.
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - docker
      env: []
    envVars:
      - name: ADMIN_PASSWORD
        required: true
        description: Login password for the Custom Mail console.
      - name: MAIL_PROVIDER
        required: false
        description: Override plugins.provider (brevo, resend, sendgrid, mailgun, postmark, mailersend, smtp2go, sparkpost).
      - name: MAIL_THEME
        required: false
        description: Override plugins.theme (forest, midnight, ocean, paper, rose, slate, aurora, sunset, nord).
      - name: MAIL_LAYOUT
        required: false
        description: Override plugins.layout (card, minimal, banner, digest, compact).
      - name: MAIL_LOGO
        required: false
        description: Override plugins.logo (auto, image, monogram, none).
      - name: BREVO_API_KEY
        required: false
        description: Brevo API key (default provider). Required to send unless another provider key is set.
      - name: MAIL_API_KEY
        required: false
        description: Fallback API key used when the provider-specific secret is empty.
      - name: RESEND_API_KEY
        required: false
        description: Resend API key. Use with MAIL_PROVIDER=resend.
      - name: SENDGRID_API_KEY
        required: false
        description: SendGrid API key. Use with MAIL_PROVIDER=sendgrid.
      - name: PORT
        required: false
        description: Container listen port (default 8787).
    emoji: "✉️"
    homepage: https://github.com/InnoNestX/Custom-Mail
---

# Custom Mail

## What this skill does

Spin up a **private web mail console** in Docker. Compose mail, preview CommonMark/GFM as HTML, attach files, and browse send history — without running a mail server. Outbound send uses the provider plugin selected in `config/mail.json` (or `MAIL_PROVIDER`). Theme, layout, and logo are the same kind of plugin (`MAIL_THEME`, `MAIL_LAYOUT`, `MAIL_LOGO`).

Runtime is a **Rust** Cloudflare Worker (`workers-rs` → WASM) packaged with Wrangler for local use.

## When to use this skill

Use it when the user wants to:

- run Custom Mail locally or in Docker
- send mail through Brevo, Resend, SendGrid, Mailgun, Postmark, MailerSend, SMTP2GO, or SparkPost
- try the compose / preview / history UI before Cloudflare deploy
- set up a lightweight mail workspace with one password login and their own brand

Trigger phrases (examples):

- "start custom mail in docker"
- "run the mail console locally"
- "deploy custom-mail container"
- "帮我本地跑一下 Custom Mail"
- "用 Docker 启动发信控制台"

## Docker Quick Start

### 1. Pull

```bash
docker pull xuxuclassmate/custom-mail:1.0.0
```

Or `:latest`. GHCR: `ghcr.io/innonestx/custom-mail:1.0.0`

### 2. Export secrets

```bash
export ADMIN_PASSWORD='choose-a-strong-password'
export BREVO_API_KEY='xkeysib-...'   # or another provider key; optional until send is needed
export PORT=8787
```

Other providers / theme / layout / logo without rebuilding the image:

```bash
export MAIL_PROVIDER=resend
export MAIL_THEME=nord
export MAIL_LAYOUT=compact
export MAIL_LOGO=monogram
export RESEND_API_KEY='re_...'
```

### 3. Run

```bash
docker run -d \
  --name custom-mail \
  -p 8787:8787 \
  -e ADMIN_PASSWORD="$ADMIN_PASSWORD" \
  -e BREVO_API_KEY="$BREVO_API_KEY" \
  xuxuclassmate/custom-mail:1.0.0
```

Open http://localhost:8787 — sign in with `ADMIN_PASSWORD`.

Verify:

```bash
curl -s http://localhost:8787/api/health
```

Health includes `"plugins"` (provider, theme, layout, logo) and `"available"` catalogs.

## Docker Compose

```bash
git clone https://github.com/InnoNestX/Custom-Mail.git
cd Custom-Mail
export ADMIN_PASSWORD='choose-a-strong-password'
export BREVO_API_KEY='xkeysib-...'
docker compose up -d
```

Branding and default plugin ids are baked from `config/mail.json` and `plugins/` at image build. Edit those files then `docker compose build` to add JSON/logo files. Slot env vars switch the active plugin without a rebuild.

## Environment

| Variable | Default | Description |
| --- | --- | --- |
| `ADMIN_PASSWORD` | *(required)* | Console login password |
| `MAIL_PROVIDER` | empty | Overrides `plugins.provider` |
| `MAIL_THEME` / `MAIL_LAYOUT` / `MAIL_LOGO` | empty | Override theme, layout, logo slots |
| `MAIL_CONFIG_JSON` | empty | Runtime JSON overlay on `mail.json` |
| `BREVO_API_KEY` | empty | Default provider key; UI loads without it, send needs a key |
| `RESEND_API_KEY` / `SENDGRID_API_KEY` / `MAILGUN_API_KEY` / `POSTMARK_SERVER_TOKEN` / `MAILERSEND_API_KEY` / `SMTP2GO_API_KEY` / `SPARKPOST_API_KEY` | empty | Provider-specific keys |
| `MAILGUN_DOMAIN` | empty | Required for Mailgun if `mail.providerDomain` is empty |
| `MAIL_API_KEY` | empty | Fallback API key |
| `PORT` | `8787` | Listen port |

## Example invocations

```
Pull and run Custom Mail on port 8787 with ADMIN_PASSWORD=dev-secret and my Brevo key.
```

```
Start the custom-mail Docker container with MAIL_PROVIDER=resend, MAIL_THEME=nord, and RESEND_API_KEY.
```

```
Clone InnoNestX/Custom-Mail and bring it up with docker compose.
```

## Production (Cloudflare)

For edge deploy instead of Docker:

```bash
git clone https://github.com/InnoNestX/Custom-Mail.git
cd Custom-Mail
cargo test --lib && npm install
npx wrangler secret put ADMIN_PASSWORD
npx wrangler secret put BREVO_API_KEY   # or the key for plugins.provider
npm run deploy
```

Branding: `config/mail.json` · Docs: https://innonestx.github.io/Custom-Mail/

## Links

- GitHub: https://github.com/InnoNestX/Custom-Mail
- Docker Hub: https://hub.docker.com/r/xuxuclassmate/custom-mail
- Docs: https://innonestx.github.io/Custom-Mail/
- Demo: https://mail.xuxuclassmate.com
