# agentlifeboat (ClawHub skill)

Source of the skill published to ClawHub as `agentlifeboat`. The agent-facing instructions are in `SKILL.md`; this file is for humans.

## Layout

- `SKILL.md`: ClawHub manifest and instructions (what the agent reads).
- `scripts/lifeboat.mjs`: the command-line entry point the agent runs through its exec tool.
- `scripts/lib.mjs`: pure helpers (key derivation identical to the sidecar, x402 paying fetch, API calls with injectable fetch).
- `package.json`: pinned dependencies. On first run the script installs them next to itself; ClawHub bundles ship without `node_modules`.

## Design choices

- The skill does not bundle a wallet. It uses `X402_PRIVATE_KEY`, the same variable the popular x402 skills use, and derives the snapshot encryption key from it exactly like the Estate sidecar does, so an agent that later moves into a room keeps the same key.
- No pricing metadata in the manifest (ClawHub forbids it); costs are documented in prose.
- Paid commands never run concurrently from the script; the instructions tell the agent not to either.

## Test locally

```
pnpm --filter @estate/skill-lifeboat test
```

Manual run against a local API (see `apps/api/README.md` to start one on port 4021 with a testnet `PAY_TO`):

```
export ESTATE_API=http://127.0.0.1:4021 X402_PRIVATE_KEY=0x... ESTATE_STATE_FILE=/tmp/estate.json
node scripts/lifeboat.mjs register --threshold 30
node scripts/lifeboat.mjs heartbeat
node scripts/lifeboat.mjs snapshot --archive some-backup.tar.gz
node scripts/lifeboat.mjs extend 2
node scripts/lifeboat.mjs status
```

## Verified 2026-09-09

- Shell run against a local API on Base Sepolia with the test wallet: `recipient`, `register` ($0.10 settled), `heartbeat`, `snapshot --archive` ($0.01 settled, 3.2 KB ciphertext stored), `extend 2` ($0.14 settled), `status` (three settled payments), plus the no-wallet and not-registered error paths (exit 2).
- Agent-driven run inside an Estate room (skill mounted into `workspace/skills/`, OpenClaw listed it as ready): the prompt "Use the agentlifeboat skill: run its register command with threshold 30, then heartbeat, then status" produced, from the agent through its exec tool, a registration paid on testnet (tx `0x8000df6f…`), a heartbeat, and this reply:

  > agentId: c3897e2b-18e5-4afb-b4be-d2510547ad45, status: covered, policy threshold 30, mode estate-restores, one settled register payment.

  The API showed the new agent with a fresh heartbeat and the state file existed in the workspace.
- Note for the room proxy: Gemini's OpenAI-compatible endpoint rejects multi-turn tool calls unless the `thought_signature` it returns is echoed back, which OpenClaw's generic client does not do. The agent-driven run used OpenClaw's native Gemini provider; the proxy will need to carry that field for Gemini upstreams (brain-failover plan).

## Publish

Bump `version:` in `SKILL.md` and `package.json`, merge to main, then on the brain server:

```
sh scripts/clawhub/publish.sh 1.0.2 "What changed, in one sentence."
```

It publishes the bundle from `origin/main` (no tests, no `node_modules`; it refuses test-only dependencies in `package.json` or the lockfile), then waits for ClawHub's security scan: every 2 minutes for up to 50, then from cron every 30 minutes until the verdict is in. The summary and the full report land in `.local/clawhub/<version>/`. A new version stays out of search and install until its scan passes; "suspicious" keeps it listed as "Review". The login (`~/.config/clawhub/config.json`) is the founder's device login from `.local/clawhub-login.sh`; renew it the same way if the script says it is no longer valid.

Then, from a fresh OpenClaw: `openclaw skills install @king-perb/agentlifeboat`.

Keep the test tools (vitest, hono) in the workspace root's `devDependencies`, never in this package: its lockfile ships to every agent and ClawHub scans it.

## Reading ClawHub's security scan (2026-10-27)

After a publish, ClawHub scans the version (SkillSpector, an LLM review, static analysis, VirusTotal) and keeps it "in review" while the result is suspicious. `scripts/clawhub/scan-watch.mjs <version>` does all of this and writes `.local/clawhub/<version>/summary.md` (`--once` for one look; the publish script runs it). By hand, over HTTP:

- No login: `curl -s "https://clawhub.ai/api/v1/skills/agentlifeboat/scan?owner=king-perb"`. Gives the verdict, SkillSpector's score, severity, recommendation and issue count, and the LLM reviewer's summary, guidance and findings in full.
- With the ClawHub login on the brain server (`~/.config/clawhub/config.json`, key `token`; send it as `Authorization: Bearer`, never print it): `GET https://clawhub.ai/api/v1/skills/-/scan/download/agentlifeboat?version=<version>&kind=skill`. Returns a ZIP with `skillspector.json` (every finding with file, line, explanation and remediation), `clawscan.json`, `static-analysis.json`, `virustotal.json`. The brain server has no `unzip`; use `python3 -m zipfile -e report.zip out/`.
- `npx clawhub@latest …` is refused in sessions (unpinned outside code); the two endpoints above are what the CLI calls.
