# Document Timeline — Reference Guide

## Purpose
Provide an **opt-in** session log of documents processed. The user must explicitly consent before any entry is written. Once enabled for a session, the log records document type, filename, and a PII-free one-line summary to `~/.doc-process-timeline.json`.

---

## Consent Model

The timeline is **off by default**. Logging only starts after the user says yes to the consent prompt (see SKILL.md Step 5). If the user said no or did not answer, do not run `timeline_manager.py add` under any circumstances during the session.

When the user asks to see the timeline or asks "what have I processed", load and display whatever is in the file — even if they declined logging this session (prior sessions may have entries).

---

## Step 1 — Load and Display the Timeline

```bash
python skills/doc-process/scripts/timeline_manager.py show
```

### Timeline Table

| # | Date & Time | Mode | Document | Summary |
|---|---|---|---|---|
| 1 | 2024-03-15 14:32 | Receipt Scanner | starbucks_march15.jpg | Coffee purchase — Food & Dining |
| 2 | 2024-03-15 15:01 | Contract Analyzer | acme_saas_agreement.pdf | 12-month SaaS — 3 RED flags found |

### Empty State
If no entries exist:
> "Your document processing timeline is empty. Timeline logging is opt-in — you'll be asked before any entries are recorded. You currently have 0 documents logged."

---

## Step 2 — Statistics Dashboard (3+ entries)

```bash
python skills/doc-process/scripts/timeline_manager.py stats
```

| Metric | Value |
|---|---|
| Total Documents Logged | N |
| Most Used Mode | e.g., Receipt Scanner (12×) |
| Least Used Mode | e.g., ID Scanner (1×) |
| First Entry | [date] |
| Most Recent Entry | [date] |

### Usage by Mode
| Mode | Count | % of Total | Last Used |
|---|---|---|---|

---

## Step 3 — Filtered Views

```bash
# By mode
python skills/doc-process/scripts/timeline_manager.py show --type "Receipt Scanner"
```

Present filtered results in the same table format:
"Showing [N] of [Total] entries matching: [filter description]"

---

## Step 4 — Save to Documents Folder

Ask: "Would you like me to save your document timeline to your Documents folder as a formatted Markdown report?"

If yes, confirm what will be saved before proceeding:
> "I'll write a Markdown file to `~/Documents/doc-process-timeline.md` containing your [N] logged entries and a usage summary. No document content is included — only the type, filename, and one-line summaries you've already seen. Proceed?"

Then run:
```bash
python skills/doc-process/scripts/timeline_manager.py save --output ~/Documents/doc-process-timeline.md
```

Confirm: "Saved to `~/Documents/doc-process-timeline.md` — [N] entries."

---

## Step 5 — Management Operations

### Delete a specific entry
Show the entry before deleting. Ask for confirmation.
```bash
python skills/doc-process/scripts/timeline_manager.py delete --id [entry_id]
```

### Clear all entries
Warn first: "This will permanently delete all [N] timeline entries from `~/.doc-process-timeline.json`. Are you sure?"
```bash
python skills/doc-process/scripts/timeline_manager.py clear --yes
```

### Export to JSON
```bash
python skills/doc-process/scripts/timeline_manager.py export --output ~/Documents/timeline.json
```

---

## Step 6 — Logging After Consent

Once the user has said yes to the consent prompt, log each completed task openly:

State after each task: "Logged to your timeline." (one line — do not hide this.)

```bash
python skills/doc-process/scripts/timeline_manager.py add \
  --type "<Mode Name>" \
  --source "<filename or description>" \
  --summary "<1-line summary — no PII>"
```

### Summary PII rules (enforced)
The `--summary` value must not contain names, ID numbers, dates of birth, addresses, account numbers, medical values, or any data that could identify a person from the log alone. Use category-level descriptions only.

| Mode | Acceptable Summary |
|---|---|
| Receipt Scanner | "Coffee purchase — Food & Dining, logged to expenses.csv" |
| Contract Analyzer | "SaaS agreement — 3 RED flags, auto-renewal, Delaware" |
| Bank Statement Analyzer | "Chase Feb 2024 — $6,270 spent, 6 subscriptions, 3 anomalies" |
| Resume Parser | "Software engineer CV — 7 years experience, targeting senior roles" |
| ID Scanner | "Passport — [Country] — valid, all MRZ checks pass" |
| Medical Summarizer | "Lab report — 2 flagged values (CBC panel)" |
| Legal Redactor | "Contract — 34 items redacted, standard mode" |
| Meeting Minutes | "Product review — 8 action items, 3 decisions" |
| Table Extractor | "3 tables, 847 rows extracted to CSV" |
| Document Translator | "4,200-word lease — French to English" |
| Form Autofill | "Visa application — 38/42 fields filled, 2 missing" |

---

## Step 7 — What the Log File Contains

Explain this clearly when describing the timeline to the user:

| Field stored | Example | Contains PII? |
|---|---|---|
| `id` | `a3f8c12d` (random hex) | No |
| `timestamp` | `2024-03-15T14:32:00Z` | No |
| `type` | `Receipt Scanner` | No |
| `source` | `starbucks_march15.jpg` (filename you provided) | Only if the filename itself contains a name |
| `summary` | Category-level description | No — enforced by summary rules |

The file does **not** store: document content, extracted field values, personal data you provided for form autofill, or full output of any processing task.

---

## Step 8 — Privacy & Storage

| Aspect | Detail |
|---|---|
| Storage location | `~/.doc-process-timeline.json` — your local machine only |
| Network transmission | None. `timeline_manager.py` uses only `json`, `pathlib`, `uuid`, `datetime`, `argparse`. No network imports. |
| Opt-in | You must say yes before any entry is written |
| Deletion | `timeline_manager.py clear` removes all entries; `delete --id` removes one |
| File permissions | Written with your user account's default permissions |

---

## Action Prompt
End with: "Would you like to:
- Filter the timeline by mode or date?
- Save a formatted report to your Documents folder?
- Delete specific entries or clear the log entirely?
- Turn off timeline logging for the rest of this session?"
