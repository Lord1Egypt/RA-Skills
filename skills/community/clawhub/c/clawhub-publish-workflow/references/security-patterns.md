# Security Patterns Reference

> Patterns to AVOID in skills (trigger security alerts)
> Part of axiomata-guard-scanner documentation

---

## Dangerous Patterns

| Pattern | Risk | Fix |
|---------|------|-----|
| `eval(`, `base64_decode(` | RCE risk | Remove or escape |
| `discord.com/api/webhooks` | Exfiltration | Remove or use env vars |
| `dns.lookup('evil` | C2 indicator | Remove |
| `curl.*|.*bash` | Shell injection | Use subprocess instead |
| `openclawcli.zip` | Malicious binary | Remove |
| `glot.io/snippets/` | RCE via glot | Remove |
| `/media/ezekiel/` | Hardcoded paths | Use relative paths |
| `PsActiveProcessHead` | Rootkit | Remove |
| `AmsiScanBuffer=0` | AMSI bypass | Remove |
| typosquat patterns | Package confusion | Use official packages only |

---

## Why These Patterns Are Dangerous

1. **eval()** — Allows arbitrary code execution
2. **discord/webhooks** — Common exfiltration channel
3. **curl | bash** — Classic shell injection
4. **dns.lookup('evil'** — C2 communication indicator
5. **Hardcoded paths** — Agent-specific, not impersonal
6. **Rootkit patterns** — Kernel-level system compromise

---

_In Altum Per Security._