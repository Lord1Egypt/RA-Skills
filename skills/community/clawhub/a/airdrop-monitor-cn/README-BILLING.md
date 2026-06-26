# SkillPay integration (Python)

## 0) Security first
- Do NOT hardcode API key in code.
- Keep key in env var: `SKILL_BILLING_API_KEY`.
- If key was exposed anywhere, rotate it immediately in SkillPay dashboard.

## 1) Setup
```bash
cd skills/airdrop-monitor-cn
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# edit .env with your real SKILL_BILLING_API_KEY + SKILL_ID
```

## 2) Runtime env
```bash
export SKILL_BILLING_API_KEY="sk_xxx"
export SKILL_ID="your-skill-id"
python app.py
```

## 3) Paid flow
1. User request arrives
2. `charge_user(user_id)`
3. If fail: return `payment_url`
4. If success: execute monitor logic

## 4) user_id strategy (recommended)
- Discord: `discord_<userId>`
- Telegram: `tg_<userId>`
- Wallet-first mode: `wallet_<address>`

## 5) UX copy for insufficient balance
```text
余额不足，请先充值后继续使用：
{{payment_url}}
充值到账后，重新发送你的监控请求即可。
```
