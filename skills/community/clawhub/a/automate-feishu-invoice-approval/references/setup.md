# Setup reference

Use this reference for first-time deployment and whenever the target Feishu approval definition changes.

## Prerequisites

- Python 3.9 or newer
- An authenticated Codex CLI with image input support
- `lark-cli`
- A Feishu custom application with a bot
- A Feishu expense approval definition the operator is allowed to inspect and launch

Confirm the commands before editing configuration:

```bash
python3 --version
codex --version
lark-cli --version
```

## Create the local project

Run the skill's scaffolder against a new or empty target directory:

```bash
python3 <skill-directory>/scripts/scaffold.py --target <target-directory>
cd <target-directory>
cp .env.example .env
cp config/approval_mapping.example.json config/approval_mapping.json
```

The scaffolder intentionally refuses a non-empty target.

## Configure the Feishu application

Enable the bot and grant only the permissions needed to:

- receive direct-message events and read image resources;
- send or reply to messages as the bot;
- receive interactive-card callbacks;
- upload approval attachments;
- create approval instances.

Subscribe through a long connection to:

- `im.message.receive_v1`
- `card.action.trigger`

Configure the application credential through the generated helper:

```bash
scripts/setup-lark.sh
```

Enter the App ID and App Secret at the prompts. The helper sends the secret to `lark-cli` through standard input; do not store it in `.env`, shell history, source files, or the Skill.

## Configure `.env`

Set at least:

```dotenv
LARK_APPROVAL_CODE=<approval-definition-code>
REQUIRED_BUYER_NAME=<accepted-buyer-company-name>
REQUIRED_BUYER_TAX_ID=<accepted-buyer-tax-id>
BOT_AUTO_SUBMIT=false
BOT_DRY_RUN=true
```

The buyer comparison normalizes whitespace, invisible characters, Unicode punctuation variants, and tax-ID letter case. It does not permit a materially different company name or tax ID.

Keep `ALLOWED_SENDER_OPEN_IDS` empty to accept all users visible to the bot, or add a comma-separated allowlist.

## Map the approval form

Open `config/approval_mapping.json` and replace every placeholder:

- `approval_code`: the approval definition code, unless set through `.env`;
- each key under `expense_type_options`: the exact option ID from the approval's category radio control;
- every `id` under `form`: the exact widget ID from the approval definition.

The bundled mapping demonstrates:

- `radioV2` from `invoice.expense_category_value`;
- `textarea` from `invoice.approval_summary`;
- `formula` from `invoice.total_amount_number`;
- `fieldList` content, date, and amount rows;
- `attachmentV2` from `approval_file.attachment_code`.

Do not use `invoice.expense_category_value` unless `expense_type_options` is present and contains every category allowed by the JSON Schema. The service derives that value from the selected category and its Feishu option ID.

If the target approval uses different widget types, inspect its definition and adjust both the form item shape and tests. Never guess IDs or option values.

## Validate safely

Run:

```bash
PYTHONPATH=src python3 -m unittest discover -s tests -v
PYTHONPATH=src python3 -m invoice_approval_bot.cli validate
```

Keep `BOT_DRY_RUN=true` and `BOT_AUTO_SUBMIT=false` for the first end-to-end test. Then enable `BOT_AUTO_SUBMIT=true` while retaining dry-run so the Submit button builds the complete request without uploading an attachment or creating an approval.

Test at least:

- a valid invoice;
- a wrong buyer name;
- a wrong buyer tax ID;
- OCR spacing or full-width-parenthesis variations;
- a low-confidence image;
- a duplicate invoice;
- Submit and Do not submit card buttons;
- a card action attempted by someone other than the uploader.

Only disable dry-run after all checks pass and the user explicitly authorizes real submissions.
