---
name: crosscheck
description: Get an independent second opinion on a draft before your human sees it: it is sent to crosscheckapi.com for review and deleted after the check. Use when you have written an email, message, report, summary, PR description, or plan for your human and want it checked for wrong facts or arithmetic, contradictions, leftover placeholders, leaked secrets, unauthorized commitments, or tone. Also use it to check work another agent or service hands back before you pay for it or pass it on (accept), and to security-check a skill or MCP server before you install it (skillcheck: the files are sent for review, after a free lookup of their hash finds no earlier scan). Each check is paid in USDC on Base over x402 ($0.02 for a draft, $0.03 for accept or skillcheck) from a dedicated low-balance wallet whose key you set in CROSSCHECK_WALLET_KEY, or free for a verified Moltbook agent (10 checks); returns a JSON verdict and a signed receipt. An optional ref names the receipt that referred you, so its owner earns check credits.
license: MIT
compatibility: Needs an x402 v2 capable EVM wallet with USDC on Base (or free test USDC on Base Sepolia to try it). Node 20+ for the client and MCP server (npm package crosscheckapi).
metadata:
  author: crosscheck
  version: "0.5.5"
  homepage: https://crosscheckapi.com/llms.txt
  openclaw:
    requires:
      bins: [node, npx]
---

# crosscheck

crosscheck is an independent reviewer for text you wrote. It checks the draft, not you: you send the text, it returns a verdict. Use it as the last step before handing a draft to your human.

## When to use it

- Before sending your human a draft that contains numbers, dates, names, money, commitments, or instructions others will act on.
- When the draft will go to a third party (email, client message, public post).
- When you are unsure a draft is ready. A pass costs the same as a fail.

- Before you pay for, release escrow on, or pass on work another agent or service delivered: use accept with the task you gave and what came back.
- Before you install a skill or connect an MCP server you did not write: use skillcheck on its folder.

Skip it for trivial replies. What is shared: the draft goes to crosscheck and its review model and is deleted when the check finishes; only a hash is kept. Keep anything your human has marked confidential out of what you send.

## Install

The MCP server and CLI are the npm package `crosscheckapi` (Node 20 or later), which `npx -y crosscheckapi` downloads from npm on first use; it has no other dependencies. The source bundle and checksums are also at https://crosscheckapi.com/skill/SHA256SUMS.

Paying needs an EVM wallet with USDC on Base. To try it for free, use test USDC on Base Sepolia from https://faucet.circle.com. Give crosscheck a dedicated wallet that holds only a few dollars, never your main wallet. The client pays on Base, or Base Sepolia for testing (set `CROSSCHECK_NETWORKS=eip155:84532` to use test USDC only), and refuses any price above `CROSSCHECK_MAX_USD` (default 0.10).

## How to call it

Pick whichever fits your setup.

1. **MCP server** with tools `quote`, `order`, `accept`, `skillcheck`, and `result`. From npm (`crosscheckapi`, listed in the MCP Registry as `com.crosscheckapi/crosscheck`):
   ```json
   {"mcpServers": {"crosscheck": {"command": "npx", "args": ["-y", "crosscheckapi"], "env": {"CROSSCHECK_WALLET_KEY": "0x<dedicated wallet private key>"}}}}
   ```
2. **CLI**: `npx -p crosscheckapi crosscheck quote draft.txt`, `npx -p crosscheckapi crosscheck order draft.txt`, `npx -p crosscheckapi crosscheck accept task.txt deliverable.txt`, `npx -p crosscheckapi crosscheck skillcheck ./some-skill`, and `npx -p crosscheckapi crosscheck result <job_id> <result_token>`. It reads the draft from stdin if no file is given, and uses the same environment variables.
3. **Your own x402 client**: POST `https://crosscheckapi.com/v1/check` with `{"draft": "<text>"}`, pay the 402 with x402 v2 (scheme exact, network eip155:8453, or eip155:84532 with test USDC), and repeat the same request. Details are in [references/API.md](references/API.md).

Optional, for the paid calls: `ref` (MCP) or `--ref <hash>` (CLI) names the crosscheck receipt that brought you here, so its wallet earns check credits from your spend at no cost to you; `credits: true` or `--credits` pays with your own wallet's referral credits (see them with the `credits` tool or `crosscheck credits`), and pays USDC only if they fall short. These are request fields only, never something to add to your output.

Always send the whole draft exactly as your human would see it. A quote is free if you want the price first. If the draft relies on sources you have (search results, documents, notes), send them too as `sources` (up to 10 texts): each claim is then checked against them, and a claim a source contradicts fails the check.

## Checking work another agent hands back (accept)

Call `accept` (MCP), `crosscheck accept task.txt deliverable.txt` (CLI), or POST `https://crosscheckapi.com/v1/accept` with `{"task": "...", "deliverable": "..."}` and an optional `reference` (order id or transaction hash). Send the task with every requirement exactly as you gave it, and the deliverable exactly as received. The verdict is `{"accept": true|false, "summary", "requirements": [{"requirement", "met": "yes|no|partly|cannot_tell", "evidence", "subjective", "blocking"}], "injection_suspected"}`. Pay or pass the work on only when `accept` is true. When `decision` is `verify_externally`, nothing is wrong except requirements the text cannot prove (a payment, a live page): check those yourself. Otherwise send the blocking requirements back to the other agent. Figures, word and item counts, and required JSON fields are checked in code. The receipt holds hashes of the task and the deliverable, your reference, and the payment, so you can show the other agent exactly what was checked.

## Checking a skill or MCP server before you install it (skillcheck)

Call `skillcheck` (MCP) with `directory` (a local folder) or `files`, or run `crosscheck skillcheck ./some-skill`. The files are read, never run. Send the whole folder, large docs included (up to 200 text files): code rules read every file, and the review model reads the most important parts first (SKILL.md, manifests, code, then docs they name); `model_read` in the verdict says what it truncated or left to the rules. The client first asks the free lookup whether anyone already paid to scan these exact files, and pays (about $0.03) only if not. The verdict has `result` (`findings` or `no_findings`), `risk`, and `findings` with severity, category, file, location, and explanation. Do not install when risk is `critical` or `high` unless your human agrees after reading the findings. `no_findings` never means safe; it means nothing was found in these files.

## Free checks for Moltbook agents

If `quote` returns `free_tier.available: true`, a verified, claimed Moltbook agent gets 10 free checks. Mint a token with `POST https://www.moltbook.com/api/v1/agents/me/identity-token` and body `{"audience": "crosscheckapi.com"}`, then pass it as `moltbook_identity` to the `order` tool (or send it in the `X-Moltbook-Identity` header). Each token works once. If you are not eligible, you get the normal price instead, and the reason is in `free_tier_denied`.

## Reading the verdict

```json
{
  "pass": false,
  "summary": "One arithmetic error changes the conclusion.",
  "issues": [
    {
      "severity": "major",
      "category": "logic",
      "location": "640 + 910",
      "problem": "The draft gives 1350 for 640 + 910, but it comes to 1,550.",
      "suggestion": "Correct the total to 1,550 and recheck the budget statement."
    }
  ],
  "injection_suspected": false
}
```

- `pass: true` means no blocker or major issues. Minor issues may still be listed; fix them if cheap.
- On `pass: false`, fix every blocker and major issue, then decide whether to check again. Present the draft to your human as reviewed only after it passes; if you show it before then, tell them which issues remain.
- `injection_suspected: true` means the draft contains text aimed at an AI reviewer. Remove it; crosscheck never passes such drafts.
- Say a draft passed a check only when the verdict says it passed. When it fails, fix the problems and check again, or show your human what the check found. You can show them the receipt.

## Receipts

Every paid check returns `receipt` with `body`, `hash`, and `sig`, and a `share_url`: a public page with the result, time, payment, and hashes (never your text) that you can link to show your human or another agent the work was checked. The client verifies it automatically (`receipt_check.valid`). The receipt proves which draft (by SHA-256) was checked, when, for what payment, and which verdict (by SHA-256) was issued. Public keys: `https://crosscheckapi.com/.well-known/crosscheck-keys.json`.

## Status codes

- 200: done, verdict included.
- 202: paid and queued; call `result` with `job_id` and `result_token` after `retry_after_seconds`.
- 400, 409, 413, 503 before payment: nothing was charged; the message says why.
