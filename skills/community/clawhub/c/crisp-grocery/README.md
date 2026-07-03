# Crisp Grocery Skill

An OpenClaw/Codex skill for user-authorized Crisp grocery planning and account inspection.

This skill helps an agent work with a user's own Crisp account data to:

- plan meals from order history and current recipes;
- compare current promotions;
- inspect delivery windows, minimum order value, and service fees;
- summarize personalized shopping surfaces such as `Jouw winkel`;
- fetch recipe and ingredient images;
- prepare supervised basket changes with explicit confirmation.

## Unofficial Project

This project is unofficial. It is not affiliated with, endorsed by, sponsored by, or connected to Crisp or Crisp BV.

Use it only with accounts and data you are authorized to access. The skill is designed to be read-only by default and requires explicit confirmation for basket changes. It must not place orders, change payment details, change addresses, or perform checkout.

## Contents

```text
openclaw-crisp-grocery/
  SKILL.md
  references/api-map.md
  references/planning-rules.md
  scripts/crisp_api.py
```

## Security

The repository should not contain tokens, emails, addresses, order IDs, invoices, payment details, APKs, API dumps, or other personal data. Runtime tokens should be provided through environment variables or a local user-controlled token file outside version control.
