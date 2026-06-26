# Email Provider Reference

## IMAP Server Settings

| Provider | Host | Port | SSL | Notes |
|---|---|---|---|---|
| iCloud Mail | imap.mail.me.com | 993 | Yes | App password required |
| Outlook / Hotmail / Live | outlook.office365.com | 993 | Yes | App password required if MFA is on |
| Yahoo Mail | imap.mail.yahoo.com | 993 | Yes | App password required |
| AOL Mail | imap.aol.com | 993 | Yes | App password required |
| GMX | imap.gmx.net | 993 | Yes | IMAP must be enabled in settings |
| Web.de | imap.web.de | 993 | Yes | IMAP must be enabled in settings |
| T-Online | secureimap.t-online.de | 993 | Yes | E-Mail-Passwort (not account password) |
| Fastmail | imap.fastmail.com | 993 | Yes | App password recommended |
| Proton Mail | 127.0.0.1 | 1143 | No | Requires Proton Mail Bridge running locally |

---

## App Password Setup Guides

### iCloud Mail
1. Go to [appleid.apple.com](https://appleid.apple.com)
2. Sign In → **Security** section
3. Click **Generate Password…** under "App-Specific Passwords"
4. Label it "OpenClaw Registration Scanner"
5. Copy the generated password (format: `xxxx-xxxx-xxxx-xxxx`)

> **Note:** If IMAP isn't working, go to [icloud.com](https://icloud.com) → Settings → Mail → enable "IMAP Access".

---

### Outlook / Hotmail / Live
1. Go to [account.microsoft.com/security](https://account.microsoft.com/security)
2. Click **Advanced security options**
3. Under "App passwords", click **Create a new app password**
4. Use the generated password in place of your regular password

> **Note:** App passwords are only needed if two-step verification is enabled.  
> If 2FA is off, you can use your regular password – but enabling 2FA is strongly recommended.

---

### Yahoo Mail
1. Go to [login.yahoo.com](https://login.yahoo.com) → Account Security
2. Scroll to **Generate app password**
3. Select "Other App" → enter "OpenClaw"
4. Copy the 16-character app password

> **Note:** Make sure IMAP is enabled: Yahoo Mail Settings → Security → Allow apps that use less secure sign-in (or use app password).

---

### AOL Mail
1. Go to [myaccount.aol.com](https://myaccount.aol.com) → **Security**
2. Scroll to **Generate app password**
3. Select "Other App" → enter "OpenClaw"
4. Copy the generated password

> **Note:** If IMAP access is blocked: AOL Mail Settings → Security → enable "Allow apps that use less secure sign in".

---

### GMX
1. Go to [gmx.net](https://www.gmx.net) → Settings (⚙) → E-Mail → **POP3/IMAP abrufen**
2. Enable **IMAP**
3. GMX does not require an app password – use your regular GMX password
4. If login fails, go to Security settings and confirm "Allow external access"

---

### Web.de
1. Go to [web.de](https://web.de) → Settings → E-Mail → **POP3/IMAP**
2. Enable **IMAP access**
3. Use your regular Web.de password (no app password needed)

---

### T-Online (Telekom)
1. T-Online uses a separate **E-Mail-Passwort** (not your Telekom account password)
2. Set or retrieve it at [email.t-online.de](https://email.t-online.de) → Settings → Change E-Mail-Passwort
3. Username: your full T-Online email address (e.g. `name@t-online.de`)

---

### Fastmail
1. Go to [fastmail.com](https://fastmail.com) → Settings → **Privacy & Security** → **Connected Apps & API Tokens**
2. Click **New App Password**
3. Label it "OpenClaw" and select "Mail (IMAP/SMTP)"
4. Copy the generated password

---

### Proton Mail (via Bridge)
1. Download and install **Proton Mail Bridge** from [proton.me/mail/bridge](https://proton.me/mail/bridge)
2. Sign in to Bridge with your Proton Mail account
3. Bridge exposes IMAP locally at `127.0.0.1:1143` (no SSL)
4. The IMAP password shown in Bridge is different from your Proton password – use the one shown in the Bridge app

> **Note:** Proton Mail Bridge must be running in the background the entire time the scan is active.
