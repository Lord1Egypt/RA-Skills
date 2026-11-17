## Description:

Track personal cash flow with simple terminal commands and local storage for logging daily expenses, reviewing balances, and exporting records.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ckchzh](https://clawhub.ai/user/ckchzh)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use Cashflow to log, list, search, and export personal cash-flow entries from a Bash terminal, with records stored locally in user-controlled files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cashflow may store sensitive finance-like records in local data and history logs with weak privacy controls.

Mitigation: Use a private CASHFLOW_DIR, restrict filesystem permissions, and avoid recording highly sensitive financial details.

Risk: The remove command can give users confidence that records were deleted even though security guidance says not to rely on it for saved records.

Mitigation: Verify deletion directly in the stored data and history files, or manually edit and secure those files when removing sensitive entries.

## Reference(s):

- [Cashflow ClawHub Page](https://clawhub.ai/ckchzh/skills/cashflow)
- [ClawHub Publisher Profile](https://clawhub.ai/user/ckchzh)
- [BytesAgain Homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Plain text terminal output with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes local data and history logs under CASHFLOW_DIR, XDG_DATA_HOME, or ~/.local/share/cashflow.]

## Skill Version(s):

2.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
