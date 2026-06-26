# Setup - Baidu

Use this file when `~/baidu/` is missing or empty.

Answer the immediate Baidu request first, then lock only the defaults that should repeat in future Baidu tasks.

## Immediate First-Run Actions

### 1. Lock activation behavior early

Within the first exchanges, clarify:
- should this activate for any Baidu-related request or only when named explicitly
- which Baidu surfaces it should cover by default: search, knowledge, maps, Qianfan, or corporate research
- when it should stay silent because a narrower skill owns the task better

Keep this short. One routing question is enough if the request is already specific.

### 2. Lock the region and language defaults that change the answer

Capture the defaults that materially change Baidu recommendations:
- mainland China, cross-border, or global target
- preferred documentation language
- whether Chinese-first sources are acceptable
- whether the user prefers official docs only or allows supporting analysis

If the user does not care, store a neutral default and make assumptions explicit in outputs.

### 3. Lock the preferred output shape

Choose the normal answer style for this workspace:
- quick routing recommendation
- decision matrix with tradeoffs
- implementation plan
- due-diligence checklist

Default to the lightest format that still prevents the usual Baidu confusion.

### 4. Prepare local state after routing is approved

```bash
mkdir -p ~/baidu
touch ~/baidu/{memory.md,accounts.md,regions.md,sources.md,decisions.md}
chmod 700 ~/baidu
chmod 600 ~/baidu/{memory.md,accounts.md,regions.md,sources.md,decisions.md}
```

If `~/baidu/memory.md` is empty, initialize the baseline files from `memory-template.md`.

### 5. What to save

Save only what helps later Baidu work:
- activation and silence preferences
- product surfaces in scope
- region and language defaults
- trusted-source and weak-source patterns
- durable decisions, blockers, and approval boundaries

Before saving any account label, internal team name, or ongoing project note, confirm that the user wants it remembered.

## Guardrails

- Never store passwords, QR codes, cookies, SMS codes, or cloud access keys.
- Never claim mainland and global Baidu surfaces behave the same.
- Never save assumptions as facts; if something is inferred, ask before storing it.
- Never log into consoles or trigger account-changing actions during setup.
