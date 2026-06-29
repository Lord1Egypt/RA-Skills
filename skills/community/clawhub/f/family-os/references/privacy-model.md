# Privacy Model

Family OS is split into two parts:

- The skill package: reusable, generic, safe to share or publish.
- The household workspace: private local data owned by the user.

Do not store private household information in the skill package. This includes names, addresses, assets, income, medical details, child information, contracts, credentials, account numbers, identity documents, family conflicts, and private relationship notes.

## Local-Only Default

Use local files as the default system of record. Do not upload private files or search the web for private household facts unless the user explicitly asks and the task requires it.

## Sensitive Write Policy

When `ask_before_sensitive_write` is enabled in config, ask before writing:

- identity document numbers or images
- exact home addresses
- medical diagnoses, test reports, or pregnancy/child health details
- bank, brokerage, insurance, loan, or tax identifiers
- account credentials or recovery details
- legal disputes, contract conflicts, or highly personal relationship notes
- detailed child information that could identify the child

For routine household logistics, public facts, ordinary tasks, and non-sensitive preferences, write directly when the user has enabled auto-update.

## Response Hygiene

Summarize sensitive updates instead of repeating full private details in the final response. Prefer: "I updated the health project and added one follow-up task" over restating medical values unless the user requested the values.
