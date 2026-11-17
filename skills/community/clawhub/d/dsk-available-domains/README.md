# dsk-available-domains (OpenClaw / ClawHub skill)

Teaches an agent to call Domain Search King's **remote MCP** (live RDAP). No API key.

Copy this folder into `C:\Users\neman\domainsearchking\skills\dsk-available-domains\` before publish if you want it in the DSK repo.

## What agents type after it's live

```bash
clawhub install dsk-available-domains
```

Same as the ClawHub domain skill that's already spreading (`clawhub install agentdomainservice`), except this one hits **our** MCP and refuses to guess.

## You publish (GitHub OAuth — I cannot do this)

GitHub account must be at least one week old.

```bash
npm i -g clawhub
clawhub login
cd D:\temp\claude\2026-08-25-dsk-clawhub-skill\dsk-available-domains
clawhub skill publish . --dry-run
clawhub skill publish . ^
  --slug dsk-available-domains ^
  --name "DSK available domains (RDAP)" ^
  --version 1.0.0 ^
  --changelog "Initial: live RDAP domain MCP, no API key" ^
  --categories integrations,research ^
  --topics "domains,mcp,rdap,naming"
```

Listing: `https://clawhub.ai/<your-github-handle>/dsk-available-domains` after their security scan.

Also copy `SKILL.md` to `domainsearchking/skill.md` and deploy so agents can `curl https://domainsearchking.com/skill.md`.
