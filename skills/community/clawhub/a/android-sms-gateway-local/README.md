# Android SMS Gateway Local Skill

This repo contains a skill for OpenClaw that sends and receives SMS via the Android SMS Gateway app in Local Server mode with Basic Auth.

**Contents**
- `SKILL.md`
- `references/api.md`
- `scripts/*.sh`

**Install**
1. Clone this repo.
2. Copy the skill folder into your OpenClaw skills directory.

Example:
```bash
# Replace $OPENCLAW_SKILLS with your configured skills directory
cp -R . "$OPENCLAW_SKILLS/android-sms-gateway-local"
```

**Usage**
```bash
chmod +x scripts/*.sh
export SMS_GATE_BASE_URL="http://192.168.1.10:8080"
export SMS_GATE_USER="your-user"
export SMS_GATE_PASS="your-pass"
export PHONE_NUMBERS="+15551234567"
export MESSAGE_TEXT="Hello from Local Server"
./scripts/send_sms.sh
```

**Security**
Never commit credentials. Use environment variables or a local `.env` file that is ignored by git.

**License**
See `LICENSE`.
