## Description: <br>
Helps users track countdown dates so they can better plan their schedule. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rain-lei](https://clawhub.ai/user/rain-lei) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to store countdown dates in a local JSON file, query days remaining or elapsed for named events, list all saved dates, and manually maintain entries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Countdowns, birthdays, anniversaries, or deadlines may be stored in a local plaintext JSON file. <br>
Mitigation: Install only if local plaintext storage is acceptable for the user's date data. <br>
Risk: Manual edits to the JSON data file can corrupt dates or remove saved entries. <br>
Mitigation: Back up the JSON file before editing it and keep dates in strict YYYY-MM-DD format. <br>
Risk: Broad requests to list saved dates may reveal all locally stored countdown entries. <br>
Mitigation: Use explicit wording when asking the agent to list all saved dates. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/rain-lei/date-count) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown text with JSON examples and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses YYYY-MM-DD dates stored in a local plaintext JSON file.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
