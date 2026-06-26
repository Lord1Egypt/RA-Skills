## Description: <br>
Track expenses and income with multi-backend storage (local/Notion/Google Sheet/Supabase). Credentials are encrypted with AES-256-GCM. Use when user wants to record expenses, view transaction history, or check monthly spending statistics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[codeblackhole1024](https://clawhub.ai/user/codeblackhole1024) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to record expense and income entries, view transaction history, and summarize monthly spending across local or configured provider-backed storage. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Expense records may be stored locally or sent to the selected Notion or Supabase backend. <br>
Mitigation: Choose the local backend when records should remain on-device, and review provider access before enabling cloud-backed storage. <br>
Risk: Provider credentials and expense data are sensitive even when configuration credentials are encrypted. <br>
Mitigation: Use least-privilege Notion or Supabase credentials and protect the local expense data file according to the user's privacy requirements. <br>
Risk: Passing the master password on the command line can expose it through shell history or process inspection. <br>
Mitigation: Prefer interactive password entry or safer secret handling instead of `expense-tracker pass <password>`. <br>
Risk: The Google Sheet backend is listed as an option, but the artifact implementation reports it as not implemented. <br>
Mitigation: Use the local, Notion, or Supabase backend unless Google Sheet behavior is verified in a later release. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/codeblackhole1024/expense-tracker-v2) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill guides an agent to invoke the expense-tracker CLI for setup, record creation, listing, and monthly statistics.] <br>

## Skill Version(s): <br>
1.1.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
