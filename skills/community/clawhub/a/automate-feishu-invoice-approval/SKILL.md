---
name: automate-feishu-invoice-approval
description: Scaffold, configure, validate, run, and maintain a Feishu/Lark invoice approval bot that uses Codex vision, validates buyer headers, blocks risky individual-seller equipment invoices and inconsistent tax amounts, auto-selects the closest expense category, drafts the approval reason, sends an interactive confirmation card, and submits only after the original uploader confirms. Use for building or troubleshooting Feishu invoice-to-approval workflows, invoice risk gates, approval form mappings, dry-run tests, card callbacks, and duplicate protection.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
metadata: {"openclaw":{"requires":{"bins":["python3","codex","lark-cli"]},"envVars":[{"name":"LARK_APPROVAL_CODE","required":false,"description":"Feishu approval definition code used by the generated service."},{"name":"APPROVAL_MAPPING_FILE","required":false,"description":"Path to the generated approval field mapping file."},{"name":"REQUIRED_BUYER_NAME","required":false,"description":"Exact buyer company name accepted on invoices."},{"name":"REQUIRED_BUYER_TAX_ID","required":false,"description":"Exact buyer tax identifier accepted on invoices."},{"name":"BOT_AUTO_SUBMIT","required":false,"description":"Enables submission after the uploader confirms."},{"name":"BOT_DRY_RUN","required":false,"description":"Prevents real attachment uploads and approval creation when true."},{"name":"BOT_REPLY_ENABLED","required":false,"description":"Enables status and error replies to the uploader."},{"name":"INVOICE_MIN_CONFIDENCE","required":false,"description":"Minimum Codex extraction confidence from zero to one."},{"name":"ALLOWED_SENDER_OPEN_IDS","required":false,"description":"Optional comma-separated uploader allowlist."},{"name":"CODEX_BIN","required":false,"description":"Optional path or command name for the Codex CLI."},{"name":"CODEX_MODEL","required":false,"description":"Optional Codex model override."},{"name":"CODEX_TIMEOUT_SECONDS","required":false,"description":"Codex extraction timeout."},{"name":"LARK_CLI_BIN","required":false,"description":"Optional path or command name for lark-cli."},{"name":"LARK_READY_TIMEOUT_SECONDS","required":false,"description":"Timeout for the Lark event listener to become ready."},{"name":"DATA_DIR","required":false,"description":"Local runtime data directory."},{"name":"DATABASE_PATH","required":false,"description":"SQLite database path for idempotency and audit records."}],"emoji":"🧾"}}
---

# Automate Feishu Invoice Approval

Build a reusable Python service that turns invoice images sent to a Feishu bot into uploader-confirmed expense approvals.

## Core workflow

1. Choose a new or empty target directory. Do not overwrite an existing project.
2. Run `python3 <skill-directory>/scripts/scaffold.py --target <target-directory>`.
3. Read [references/setup.md](references/setup.md) before configuring a first deployment or changing an approval definition.
4. Copy `.env.example` to `.env` and `config/approval_mapping.example.json` to `config/approval_mapping.json`.
5. Fill the buyer name, buyer tax ID, approval code, expense option IDs, and approval widget IDs. Never put an app secret in `.env` or the mapping file.
6. Configure the Feishu application credential with `scripts/setup-lark.sh`.
7. Run the generated project's tests and validation:

   ```bash
   PYTHONPATH=src python3 -m unittest discover -s tests -v
   PYTHONPATH=src python3 -m invoice_approval_bot.cli validate
   ```

8. Start with `BOT_DRY_RUN=true`. Send representative invoices and verify extraction, buyer-header rejection, individual-seller equipment rejection, zero or masked tax rejection, tax-rate arithmetic, category selection, reason generation, confirmation-card callbacks, and duplicate handling.
9. Set `BOT_AUTO_SUBMIT=true` and `BOT_DRY_RUN=false` only when the user explicitly authorizes real approval creation.
10. Run `scripts/run.sh` under the user's preferred supervisor. Read [references/operations.md](references/operations.md) for status meanings and incident checks.

## Safety invariants

- Limit file reads and writes to the Skill bundle and the user-selected target project. Shell access is required to run the scaffolder, tests, validation, `codex`, and `lark-cli`; environment access is limited to the variables declared in frontmatter and the generated project's `.env`.
- Reject an invoice before confirmation when either the normalized buyer name or normalized buyer tax ID differs from the configured values. Tell the uploader which field failed.
- Reject equipment purchases from a seller name that appears to be an individual. Treat repair, maintenance, installation, consulting, design, development, rental, testing, training, and other explicit service items as services even when their names mention equipment.
- Reject invoices when the total or line-item tax is zero, masked with asterisks, missing, unparsable, inconsistent with `amount × tax rate` beyond a 0.02 currency-unit rounding tolerance, or inconsistent between line totals and the invoice tax total. Return every detected risk reason to the uploader.
- Never create a real approval until the original uploader clicks **Submit** on the confirmation card.
- Accept card actions only from the uploader and only for the matching card and source message.
- Keep dry-run enabled during initial setup, approval-form changes, and callback changes.
- Preserve SQLite idempotency and invoice-fingerprint duplicate protection.
- Do not publish or log `.env`, app secrets, approval credentials, real invoice images, extracted invoice JSON, SQLite databases, open IDs, or organization-specific approval/widget IDs.
- Do not invent approval widget or radio-option IDs. Obtain them from the target approval definition.

## Customization

- Edit the JSON Schema enum in `config/invoice-output.schema.json` and the matching `expense_type_options` object together when changing expense categories.
- Keep mapping values on supported paths such as `invoice.expense_category_value`, `invoice.approval_summary`, `invoice.total_amount_number`, and `approval_file.attachment_code`.
- Update or add unit tests whenever changing mappings, normalization, card actions, or submission state transitions.
- Keep the bundled confirmation gate unless the user explicitly requests a different approval policy and understands the risk.

## Bundled resources

- `scripts/scaffold.py` copies a clean, reusable project template.
- `assets/template/` contains the Python service, tests, schema, and safe example configuration.
- `references/setup.md` covers Feishu application and approval mapping setup.
- `references/operations.md` covers dry-run promotion, records, statuses, and troubleshooting.
