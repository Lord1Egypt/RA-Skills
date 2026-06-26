---
name: sudo-tool
description: "Store and use sudo password for automated root commands. Essential companion for skills that need sudo access (like vpn-mesh)."
metadata:
  {
    "version": "1.0.0",
    "openclaw": {
      "requires": { "bins": ["openssl"] },
      "install": []
    },
    "license": "MIT",
    "homepage": "https://github.com/stigg86/sudo-tool",
    "allowed-tools": ["exec"]
  }
---

# Sudo Tool 🔐

**Securely store your sudo password for automated root commands.** No more re-entering passwords for every sudo call.

Essential for skills that need elevated permissions — like `vpn-mesh` which installs WireGuard automatically.

---

## Setup (One-time)

```bash
# Configure your sudo password (one-time only)
sudo-tool setup
```

You'll be prompted to enter your sudo password. It's encrypted with OpenSSL and stored in `~/.openclaw/sudo-tool/` — never in plaintext.

---

## Usage

```bash
# Check if configured
sudo-tool status

# Run any command with sudo
sudo-tool apt update
sudo-tool apt install wireguard-tools
sudo-tool systemctl restart nginx

# Reset (remove stored password)
sudo-tool reset
```

---

## How It Works

1. **Setup** — encrypts your password with OpenSSL (AES-256-CBC) using a random salt, stores in `~/.openclaw/sudo-tool/.password.enc`
2. **Use** — decrypts password and pipes to `sudo -S` (reads from stdin)
3. **Secure** — password never appears in process list, temp files are deleted immediately

---

## Security Notes

- Password is encrypted with a random salt — not recoverable without your system
- Uses OpenSSL PBKDF2 for key derivation (100k iterations)
- No plaintext passwords stored anywhere
- Temp files deleted immediately after use

---

## Required By

- **vpn-mesh** — needs sudo to auto-install WireGuard

---

## Files

```
~/.openclaw/sudo-tool/
├── .password.enc   # Encrypted password
├── .salt           # Random salt for encryption
└── sudo-tool.sh     # The tool itself
```

Add to PATH with:
```bash
echo 'export PATH="$HOME/bin:$PATH"' >> ~/.bashrc
ln -s ~/.openclaw/sudo-tool/sudo-tool.sh ~/bin/sudo-tool
```