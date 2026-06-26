# Security Boundaries

## Never Store

| Category | Examples | Risk |
|----------|----------|------|
| Credentials | Passwords, API keys, tokens | Security breach |
| Financial | Card numbers, bank accounts | Fraud |
| Medical | Diagnoses, medications | Privacy (HIPAA) |
| Biometric | Voice prints, behavior fingerprints | Identity theft |
| Third-party | Other people's info without consent | Privacy violation |
| Location | Home/work addresses, daily routines | Physical safety |
| Access | System permissions, admin credentials | Privilege escalation |

## Store with Caution

| Category | Rule |
|----------|------|
| Work context | Decay after project ends |
| Emotional states | Only if user explicitly shares |
| Relationships | Roles only ("manager"), no personal details |
| Schedules | General patterns OK ("busy mornings"), not specific times |

## Transparency

1. **Audit on demand** — "What do you know?" → show everything
2. **Source tracking** — Every entry tagged with when/how learned
3. **Cite on use** — "I did X because you said Y on [date]"
4. **No hidden state** — If it affects behavior, it's in the files

## Kill Switch

"Forget everything":
1. Export current memory (user can review)
2. Wipe all files
3. Confirm: "Memory cleared. Starting fresh."

## Anti-Patterns (Never Learn)

- What makes user comply faster (manipulation)
- Emotional triggers or vulnerabilities
- Patterns from other users on shared device
- Anything that would feel "creepy" to surface
