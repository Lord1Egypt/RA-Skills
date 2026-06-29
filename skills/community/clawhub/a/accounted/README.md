# Accounted for OpenClaw 🧾

Give your [OpenClaw](https://openclaw.ai) agent a real Swedish accounting ledger. This skill connects OpenClaw to [Accounted](https://app.gnubok.se) — double-entry bookkeeping for enskild firma and aktiebolag, compliant with Bokföringslagen — and teaches it the four workflows that cover most of a small company's admin:

- **Categorize** — book bank transactions against the BAS chart, with suggestions learned from your history
- **Invoice** — create, send, credit, and match customer invoices
- **Moms** — VAT reports per ruta, filing-readiness checks, momsdeklaration to Skatteverket
- **Månadsavslut** — month-end close: book everything, reconcile, document voucher gaps, lock the period

Under the hood it's the Accounted MCP server: ~97 tools spanning transactions, suppliers, payroll/AGI, reports, reconciliation, and year-end.

## Why this is safe to give an agent

You've read the headlines — malicious skills on the registry, prompt-injection CVEs. Plan for a compromised agent, then notice it doesn't matter much here:

- **Staged writes, human approval.** No tool books anything. Write tools stage a pending operation with a preview; nothing touches the ledger until you approve it — in chat or in the [pending-operations UI](https://app.gnubok.se/pending). High-risk operations require an explicit irreversibility confirmation on top.
- **Read-only by default.** OAuth grants pre-check only read scopes; every write scope is a checkbox you tick yourself. API keys are minted read-only; write scopes are added explicitly. Scoped per category (`invoices:write` doesn't grant `bookkeeping:write`).
- **The ledger defends itself.** Posted vouchers are immutable (database-enforced, per BFL 5 kap 5§), voucher numbers are sequential and atomic, closed periods reject writes, corrections are storno-only. These guarantees hold against *any* API caller — including an agent gone sideways.
- **Sandbox first.** `gnubok_sk_test_…` keys bind to a deterministic sandbox company. Let the agent loose there before pointing it at real books.
- **No secrets needed.** The recommended setup is hosted OAuth — no API key stored on your machine at all.

## Install

```bash
clawhub install accounted
```

or copy `SKILL.md` into `<workspace>/skills/accounted/`.

Then in OpenClaw, ask for anything bookkeeping-shaped — *"book my uncategorized transactions"*, *"hur mycket moms ska jag betala för Q2?"*, *"close May"* — and the skill walks the agent through one-time MCP setup (hosted OAuth recommended) and the workflows.

### Manual MCP setup

```bash
# Recommended: hosted OAuth (read-only by default, no local secrets)
openclaw mcp add accounted --url "https://app.gnubok.se/api/extensions/ext/mcp-server/mcp"
openclaw mcp login accounted

# Alternative: API key + stdio bridge (mint at https://app.gnubok.se/settings/api)
openclaw mcp add accounted --command npx --arg gnubok-mcp
# then set GNUBOK_API_KEY in the server's env block
```

## Requirements

- An [Accounted](https://app.gnubok.se) account (hosted) or a self-hosted instance
- Option B only: Node ≥ 18 for the [`gnubok-mcp`](https://www.npmjs.com/package/gnubok-mcp) bridge

## Links

- [Connect with Claude / MCP docs](https://app.gnubok.se/docs/api/connect-claude)
- [Accounted](https://app.gnubok.se) · [gnubok-mcp on npm](https://www.npmjs.com/package/gnubok-mcp)

## License

MIT (the copy distributed via ClawHub is MIT-0 per registry policy).
