---
name: cournot
description: Query Cournot probabilities and divergence rankings; manage prepaid calls, balances, and API keys. Use only for /cournot or an explicit request to use Cournot, not for casual odds questions.
metadata:
  openclaw:
    homepage: https://skill.cournot.ai/
    requires:
      bins:
        - node
    envVars:
      - name: COURNOT_CREDENTIAL_DIR
        required: false
        description: Optional caller-configured private storage directory; defaults to ~/.cournot. Preserve its supplied value unchanged.
      - name: COURNOT_API_KEY
        required: false
        description: Optional key overriding the saved credentials for COURNOT_API_KEY_BASE; never required for anonymous use.
      - name: COURNOT_API_KEY_BASE
        required: false
        description: Origin that owns the environment key; defaults to interface.cournot.ai. Set explicitly for keys belonging to other service origins.
      - name: COURNOT_API_BASE
        required: false
        description: Optional API base override; all production operations default to interface.cournot.ai.
      - name: COURNOT_WALLET_COMMAND
        required: false
        description: Optional compatible wallet command; defaults to baw when a paid request requires a wallet.
      - name: COURNOT_INTENT_DIR
        required: false
        description: Optional directory for short-lived payment intent files; defaults to the operating system temporary directory.
---

# Cournot

Use only for `/cournot` or an explicit request to use Cournot. Reply in the user's language. The API supplies the assessment and evidence; never invent a second estimate.

## Customer communication

Apply these principles silently to every customer-facing message, across queries, account operations, payments, recovery and troubleshooting. They govern how to write; they are not content to announce or explain to the customer:

- Ground the reply in the actual request and client result. Explain the current status, consequences for the user, and the next useful action. Distinguish a planned operation from a completed one; retain uncertainty when completion, payment or remaining calls is unconfirmed.
- Use the language of the user's actual request consistently in all replies, with ordinary product terms and clear units. Do not infer the customer's language from documentation, examples or tool-output language. Localize terms such as API key, rotation, calls and latest payment preview naturally. Preserve API evidence and market-title wording according to the query and response references. Brevity applies to explanatory prose, not to required result fields: do not omit data required by a response contract.
- Keep communication proportional to the decision. Acknowledge the current task briefly without narrating a plan or requesting authorization. Give further progress only when there is a meaningful update or delay. Present an available result or choice directly. Do not narrate internal reading, routing, validation, debugging, formatting or test activity, or repeat information without a user need. Keep the focus on the operation. Do not announce that you are following instructions, using a particular reply language, filtering information or withholding internal details; these are writing decisions, not task progress. Omit unrelated warnings.
- In confirmation requests, show information needed to understand or authorize the operation, such as its wallet, payment terms and effects.
- Keep API deployment details internal across all customer replies: do not display development/production/local environment labels, API origins or service URLs, including account results, pack choices, confirmations and errors. Payment networks and public payment terms remain decision-relevant and must still be shown.
- Collect only the input needed for the next step. A routine choice is distinct from payment or credential authorization; never invent or speak for the user's consent. Request authorization only after the client provides a concrete operation preview with the information needed to decide. A request to perform an operation already permits preparing its preview; do not insert preliminary authorization questions. When awaiting input, end the final reply with a direct question about the next decision, rather than telling the user what confirmation phrase to type. Keep explanations about the operation, quoting internal rules or paths only when the host requires it or the user explicitly asks; signing parameters remain excluded.

Before sending any customer-facing message, check it against these principles: every sentence must help the user understand the result, its consequences or the next decision; every status and authorization claim must have evidence from the client or the user. Remove process narration and statements made on the user's behalf. Apply this check to progress messages as well as the final reply.

Use [errors.md](references/errors.md) to interpret failures and uncertain outcomes under these same principles. Flow references define business facts and permitted actions, not fixed customer scripts.

## Route the request first

Read the applicable flow reference before acting on or explaining a client result. For follow-up questions, status explanations and troubleshooting, select the reference from the pending operation or returned action; do not treat them as new event queries or infer a workflow from a state name alone.

After removing `/cournot` and outer whitespace, match these complete commands. Do not interpret an event containing a reserved word as a management command.

When this skill is already explicitly selected, bare `divergence [count]` uses the same ranking flow. After a ranking, recognize standalone pagination follow-ups such as "下一页", "上一页", "第 3 页", "next page", "previous page" or "page 3" before routing a new event query. Use the last ranking's saved snapshot and page metadata; a page turn is not a new query.

| Input | Action / reference |
|---|---|
| `divergence [count]` (first word only) | Cached pricing-divergence ranking — [divergence-flow.md](references/divergence-flow.md) |
| `balance` | Read balance and masked key — [account.md](references/account.md) |
| `key` | Show the full key, or recover it using the wallet — [account.md](references/account.md) |
| `import <key>` | Validate and save an existing key — [account.md](references/account.md) |
| `rotate` | Preview rotation and its effect on the old key; execute only after confirmation — [account.md](references/account.md) |
| `topup` | Let the user select a pack, preview and confirm payment — [payment.md](references/payment.md) |
| Anything else | Event query — [query-flow.md](references/query-flow.md) |

For divergence, validate the count before announcing or starting a query: it must be an integer from 1 to 100, or omitted for the default 10. Invalid or ambiguous counts require correction with no API call. For example, `2.5` must be rejected, never rounded or truncated to `2`; `101` must not become `100`. When supplying `--limit`, also pass the user's unchanged count suffix as `--count-text` so the client cross-checks the conversion.

Divergence replies display only one page, at most 20 markets. `divergence 100` still requests 100 once, but the client returns only page 1's rows to you and saves the full result locally. Keep `pagination.snapshot_file` and the current page in this chat's context. Use `divergence-page` for subsequent pages without HTTP, wallet access or another charge. Never read the full snapshot into model context or concatenate all pages into one reply. Preserve the PRD's nine-column Markdown table on each page; do not replace it with vertical field/value lists, cards, code blocks or browser/file previews. See [divergence-flow.md](references/divergence-flow.md) for navigation and verification.

For divergence, you write the heading, column labels and explanatory lines in the user's language. Before calling the client, also supply the required `--labels-json` with both direction labels and the visible link text in that same language: Chinese requests use Chinese labels including "查看"; English requests use English labels including "View"; apply the same rule to other languages. Determine the language from the user's actual request and conversation, not the English command keyword, API data or documentation examples. The JS client supplies `rows_markdown`: insert those data rows unchanged. **Each link destination must equal its original API `url` character for character**, including every query parameter such as `op_market_ticker`, even when it repeats the path. Never shorten, normalize or reconstruct a URL. Follow the output contract and row-verification procedure in [divergence-flow.md](references/divergence-flow.md).

For event queries only, also strip the optional `probability` prefix. The message is the user's event in their own words. Require a specific, testable event claim before calling resolve. An asset name or a request such as "BTC related markets" is only a topic, not a claim: ask what outcome, threshold or time horizon the user wants to assess, without an API call. Do not invent a claim to search for them. Guide pricing-divergence or mispricing requests to `/cournot divergence`. An event containing `divergence` elsewhere remains an event query. The divergence flow never calls resolve or probability.

## Runtime and billing

Never expose signing payloads or protocol parameters in any reply, including troubleshooting: domain/types/primaryType, signing chainId, urlPath, nonce, signing timestamp, parsed signing messages and internal request/intent IDs remain inside the client. Do not reconstruct them for display. This boundary has no technical-details exception; it does not remove the public payment terms needed for informed confirmation.

Node.js 22.20 or newer is required. All API operations use `scripts/cournot-client.mjs`; credentials and wallet signatures stay inside the client. All production operations, including `resolve`, `probability`, `divergence`, accounts and packs, use the default service, `https://interface.cournot.ai`. No separate override is needed for divergence. Preserve an operator's explicit supported environment target. Never switch environments to work around a failure.

Keep any import, balance, topup, payment execution or recovery follow-up on its pending request's origin, preserving any explicit environment override. Keys remain bound to their exact origin; set `COURNOT_API_KEY_BASE` to the key's own origin and never copy a key between environments. API deployment and payment network are separate: mainnet payments use real assets.

The billing contract provides **three free calls per IP in total, shared by probability and divergence, with no reset**. Use the selected environment's returned quota; do not infer shared balances or free allowance between environments. Free allowance is used before prepaid calls. No key or wallet is required to start. After free calls, a configured key spends prepaid balance; otherwise the user chooses topup, import, or $0.01 per-call payment. Packs do not expire, stack, and are non-refundable. Prices and call counts come from the client's pack catalog; actual payment terms come from the server's 402 response.

One user query permits one probability assessment or divergence request, including free and prepaid calls. Divergence count does not change the per-request charge; an empty ranking is free. A confirmed 402 replay is part of that same assessment. Do not repeat completed account operations merely to verify the same result. The client waits three seconds before each initial paid submission and checks readable authorization expiry before and after waiting. It may internally retry the same signed payment once after an explicit authorization-not-yet-valid precheck rejection, within the original confirmed payment; see [payment.md](references/payment.md). No other automatic retries, background queries, automatic topup, or silent fallback from prepaid balance to per-call payment. Keep the pending operation, event text and selected market ids, or divergence count and language through disambiguation, credential setup, and payment confirmation. A completed topup does not automatically rerun the pending query.

`COURNOT_API_KEY` overrides the file only for `COURNOT_API_KEY_BASE` (production by default). Otherwise the client reads a per-origin file beneath `~/.cournot/credentials/`. Files are plaintext protected by filesystem permissions, not an encrypted vault. Never read or edit them through the model. Use client commands for import, saving, recovery, and display. Only explicit `/cournot key` may reveal a complete key; all other output must remain masked. Never request wallet private keys or seed phrases.

On a successful probability response, read [response-format.md](references/response-format.md). Returned market and evidence URLs are opaque identifiers: preserve every character, including repeated words, casing and query values. Never regenerate a link from its title or apparent meaning. For divergence, preserve the generated data rows and verify the draft as described in [divergence-flow.md](references/divergence-flow.md). A changed or missing URL is an incorrect result; correct the draft before sending it. Report the returned billing route and remaining calls; `charged=false` does not mean no prepaid call was consumed. Never manufacture a missing quota, promise a daily reset, or promise no deduction after an uncertain server failure.

Claude Code, Codex, Grok, OpenClaw, and other Agent Skills hosts use this same folder. Install `SKILL.md`, `agents/`, `scripts/` and `references/` from `skills/cournot/`.
