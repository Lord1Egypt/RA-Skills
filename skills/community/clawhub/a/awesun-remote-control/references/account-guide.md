# Account & Service Management Guide

Detailed authentication workflows, headless cloud operations, and service license management for `awesun-cli`.

---

## 1. Login Authentication

`awesun-cli` requires an authenticated session before executing device or session operations.

### Local Environment (with Desktop Browser)
In local graphical environments (macOS/Windows desktop), the CLI automatically launches the default web browser to complete OAuth authentication:

```bash
awesun-cli login
```

### Cloud / Headless Environment (No Browser)
In container, SSH, or cloud VM environments without a GUI, use `--url`. The CLI prints an authentication URL to `stdout` instead of launching a browser:

```bash
awesun-cli login --url
# Output:
# Please visit the following URL to authenticate:
# https://cc.sunlogin.oray.com/auth.html#/?clid=...
# URL will expire at HH:MM:SS, please complete the login before then, or re-run the command.
```

#### Automated / Headless Wait Script (PID Pattern)
Because `login` blocks until the user authorizes or the URL expires, background the process, capture the printed URL, relay it to the user, and wait on the PID:

```bash
# 1. Launch in background and output log
nohup awesun-cli login --url > /tmp/awesun_qr.log 2>&1 &
echo $! > /tmp/awesun_login.pid

# 2. Wait for auth URL to be generated
for i in $(seq 1 10); do grep -q "https://" /tmp/awesun_qr.log && break; sleep 0.5; done
cat /tmp/awesun_qr.log   # Relay this URL to user

# 3. Wait on the process PID (exits automatically on login completion or expiry)
PID=$(cat /tmp/awesun_login.pid)
while kill -0 "$PID" 2>/dev/null; do sleep 2; done

# 4. Verify login outcome
awesun-cli login status
```

---

## 2. Status Verification & Logout

### Check Status
```bash
awesun-cli login status
```
Returns currently logged in user info (UserID, Account, Mobile, Token status). If not logged in, returns an unauthenticated status.

### Logout
```bash
# Normal logout
awesun-cli logout

# Complete logout and clear all locally cached credentials/tokens
awesun-cli logout --clean
```

---

## 3. License & Service Management

`awesun-cli` uses dual entitlement verification. Either `MCP Add-on` or `Company CLI` unlocks CLI capabilities.

```bash
# View user, service status, and CLI access
awesun-cli service info
```

### Output Interpretation
- **`unlocked`**: `yes` if an active CLI service or MCP add-on is unexpired.
- **`MCP Add-on`**: Add-on license entitlement with its specific expiry date.
- **`Company CLI`**: Enterprise service group entitlement with corporate CLI authorization.

### Claiming Free Trial
When receiving license errors (unlicensed account), claim the 30-day complimentary MCP trial:

```bash
awesun-cli service get-trial
```
After claiming, run `awesun-cli service info` to confirm `unlocked: yes`.
