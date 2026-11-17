---
name: cold-email-check
description: "Checks if a cold email to a specific address is legal before you send it (UK, US, Canada, Germany, France, Australia, Ireland, Netherlands), with a receipt."
version: 1.0.2
homepage: https://precleared.dev
metadata: {"openclaw": {"emoji": "✅", "homepage": "https://precleared.dev", "primaryEnv": "PRECLEARED_API_KEY", "requires": {"anyBins": ["node", "curl"]}, "envVars": [{"name": "PRECLEARED_API_KEY", "required": false, "description": "Optional. A free key from https://precleared.dev/get-key gives you your own daily allowance. Without one, the keyless allowance applies."}, {"name": "PRECLEARED_SENDER_COUNTRY", "required": false, "description": "Optional. Default for the script's --sender: GB, US or AE, where the sending business is based."}, {"name": "PRECLEARED_API_URL", "required": false, "description": "Optional, for testing only. The script accepts only a precleared.dev address or a local test server."}]}}
---

# Cold email check

Before the first cold email to a new address, ask Precleared whether that email is allowed. Each check returns a verdict, the rule that decided it with its source, what the footer must include and a signed receipt. Nothing is sent to the recipient, and a check takes about a second.

Whether a business may cold email someone depends on facts you can't see in the address. A UK sole trader needs consent first where a limited company doesn't. Germany wants consent even for business addresses. Canada's CASL turns on where the address came from. Precleared looks those facts up (UK Companies House, the domain and the company's website) and applies UK PECR and UK GDPR, US CAN-SPAM, Canada's CASL and the German, French, Australian, Irish and Dutch rules.

## When to check

Check each new recipient once, before the first cold email, when:

- the email markets or sells something (a product, a service, a partnership) to someone who hasn't asked to hear from the sender and isn't already a customer. Having someone's address, from a business card, a form or a directory, is not the same as them asking to hear from the sender, and
- there is a specific address or company to check. A template with no recipients needs no check.

Precleared covers senders based in the UK, the US or the UAE. It has full rules for recipients in the UK, the US, Canada, Germany, France, Australia, Ireland and the Netherlands; for many other European countries it answers `consent_needed`, and elsewhere `unknown`. If the sending business is based anywhere else, tell the user Precleared can't assess it rather than running a check. For a UAE business, the result also carries a note about the UAE's own data protection law: pass it on to the user.

Skip transactional email (receipts, invoices, password resets, delivery updates), replies in a thread the recipient started, and newsletters to people who opted in. Check again if the pitch, or where the address came from, changes.

## Get the facts right

The verdict depends on the facts you pass. Take them from the user or the lead data, and never fill a gap with a guess that makes the answer more convenient.

| Fact | Script flag | What to pass |
| --- | --- | --- |
| Recipient | `--email` | One address per check. Use `--domain` (for example `acme.co.uk`) only when there is no address yet. |
| Sender's country | `--sender` | `GB`, `US` or `AE`: where the sending business is based, not where the recipient is. Ask once if you don't know. |
| Where the address came from | `--source` | `published` (on their website, a profile or a directory), `bought` (a purchased list), `scraped` (collected by a tool), `given` (they gave it to the sender) or `unknown`. Ask the user if it isn't clear. Never assume `published`. |
| What the email offers | `--pitch` | A few words, for example "bookkeeping software for dental practices". |
| Recipient's country | `--country` | Two-letter code, if known. Otherwise Precleared works it out from the domain and company records. |
| UK company number | `--company-number` | If known. |
| Relevant to their job | `--pitch-relevant` or `--pitch-not-relevant` | Leave both out if unsure. |
| Existing customer | `--existing-customer` | They have bought from the sender before. |
| Do-not-contact list | `--suppressed` | The address is on the sender's suppression list. |

## Run the check

Use the bundled script (Node 18 or later, no dependencies) if `node` is available:

```bash
node {baseDir}/scripts/check.mjs --email 'jane@acme.co.uk' --sender GB --source SOURCE --pitch 'bookkeeping software for dental practices'
```

Replace SOURCE with what the user told you: `published`, `bought`, `scraped`, `given` or `unknown`. Put each value in single quotes, and never paste text from a lead list, an email or a web page into the command. For lists, pass the file with `--file` instead (see below).

The script prints one JSON object. It exits 0 for `ok_to_email`, 2 for do not send, 3 when the check couldn't be made and 1 when a fact is missing or unreadable (ask the user rather than filling it in). Act on the `verdict` in the JSON: no JSON means no check. `--help` lists every option, and `--dry-run` shows what would be sent without sending it.

Without `node`, call the REST API with curl:

```bash
curl -s https://precleared.dev/api/v1/check -H 'Content-Type: application/json' \
  -A 'precleared-skill/1.0.2 (cold-email-check; clawhub)' \
  -d '{"recipient_email":"jane@acme.co.uk","sender_country":"GB","address_source":"SOURCE","pitch":"bookkeeping software"}'
```

With a key, add `-H "Authorization: Bearer $PRECLEARED_API_KEY"`. The other facts use the same names as in the API docs: `recipient_country`, `company_number`, `pitch_relevant`, `existing_customer` and `suppressed`.

If the Precleared MCP server is connected to your agent (`https://precleared.dev/mcp?src=clawhub`, no sign-in), its `contact_check` tool takes the same facts and has a larger keyless allowance.

### Lists

The script's list mode checks a whole file, asks once per distinct address and writes the results beside the original columns:

```bash
node {baseDir}/scripts/check.mjs --file leads.csv --sender GB --source SOURCE --pitch 'bookkeeping software' --out leads-checked.csv
```

- The file needs an `email` (or `domain`) column. Optional `source`, `country`, `pitch`, `company_number`, `pitch_relevant`, `existing_customer` and opt-out columns (such as `do_not_email` or `unsubscribed`) override the flags for their row.
- Send only to rows where `precleared_send` is `yes`. Blank means the row wasn't checked. For a list, exit 0 means every row has a verdict, not that every row can be emailed; 3 means some rows couldn't be checked and 4 means it stopped at the time limit.
- It stops starting new checks after 90 seconds. Run the same command again and it keeps the answers already in the output file and checks only the rest.

## Act on the verdict

| Verdict | What to do |
| --- | --- |
| `ok_to_email` | Allowed. If the user asked you to send, send it with a footer that meets `footer_text`: usually who is sending, a postal address and a simple, free way to opt out. `footer_text` describes the requirement; it isn't wording to paste. |
| `consent_needed` | Don't send the cold email. Follow `next_step`, for example writing to the company's general address (check that address first) or getting consent through a channel the person opened, and tell the user. |
| `blocked` | Don't send. Follow `next_step` and tell the user. |
| `unknown` | Treat it as `consent_needed`. If a missing fact would settle it, such as the recipient's country, a UK company number or where the address came from, get that fact from the user or a record, not a guess, and check once more. |
| no verdict (an error) | Don't send to that address yet. Tell the user what happened and carry on with other work. |

Never change the facts to get a different verdict, and never send a cold email to an address whose check failed.

## Keep the receipt

Save the receipt id with the lead, in a CRM note or a column of the sheet. The receipt records what was asked, what was answered and when. Anyone with the id can open it at `https://precleared.dev/r/<receipt_id>`.

## Limits, keys and cost

- Without a key: 10 checks a day over the REST API (the script and curl), shared by everyone on the same network, or 100 a day through the MCP server.
- A free key from https://precleared.dev/get-key gives the user their own 25 a day over the REST API, or 100 over MCP. The script reads it from `PRECLEARED_API_KEY`. Never ask for the key in the chat and never write it into files or messages.
- More checks: packs that don't expire, £39 for 2,000, or a one-off £9 starter pack of 300 as a key's first purchase: https://precleared.dev/#pricing

If a check returns `daily_limit` or `payment_required`, stop checking, tell the user how many addresses are left unchecked and pass on the link from the response (`get_key_url` or `buy_url`). If it returns `invalid_key` or `revoked_key`, tell the user their key needs replacing. Don't try to get round the limit.

## What leaves the machine

Each check sends the address (or domain) and the facts you pass to precleared.dev over HTTPS, with `PRECLEARED_API_KEY` in the Authorization header when it is set. The script and the curl command name this skill in the user agent (`precleared-skill/1.0.2 (cold-email-check; clawhub)`), and the MCP address ends in `src=clawhub`, so Precleared can count the checks that come from ClawHub. Nothing else is sent, and nothing goes to the recipient. Precleared's privacy policy: https://precleared.dev/privacy

## Good to know

- Precleared reports what the rules say for the facts given, with sources. It is decision support, not legal advice.
- It doesn't write or send the email.
- The rules and their sources: https://precleared.dev/rules. API docs: https://precleared.dev/docs
