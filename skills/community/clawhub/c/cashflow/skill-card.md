## Description: <br>
Track personal cash flow with simple terminal commands and local storage for logging daily expenses, reviewing balances, and exporting records. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ckchzh](https://clawhub.ai/user/ckchzh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use Cashflow to record, search, list, and export local personal cash-flow entries from a terminal. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive financial records and command history may be stored locally in plaintext. <br>
Mitigation: Avoid entering sensitive details unless local plaintext storage is acceptable; use a controlled CASHFLOW_DIR and manually delete data.log and history.log when needed. <br>
Risk: The remove command can report that an entry was removed without actually deleting saved entries. <br>
Mitigation: Manually inspect, edit, or delete data.log and history.log to confirm unwanted entries are cleared. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/ckchzh/cashflow) <br>
- [BytesAgain homepage](https://bytesagain.com) <br>
- [Publisher profile](https://clawhub.ai/user/ckchzh) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration] <br>
**Output Format:** [Plain text terminal output with optional redirected files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes local data.log and history.log files under CASHFLOW_DIR or XDG_DATA_HOME.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
