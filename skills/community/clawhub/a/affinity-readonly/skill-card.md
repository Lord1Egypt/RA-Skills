## Description: <br>
Affinity Readonly fetches Affinity CRM companies, people, notes, opportunities, interactions, and relationship data through read-only API calls for analysis and memo preparation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[howdymarc](https://clawhub.ai/user/howdymarc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees or developers use this skill to retrieve selected Affinity CRM records with GET-only API calls and summarize evidence for analysis or memo preparation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security evidence reports a suspicious verdict for the bundle. <br>
Mitigation: Install only after reviewing the skill package and confirming that the requested Affinity access is needed for the intended workflow. <br>
Risk: The skill uses an Affinity API key to fetch CRM data. <br>
Mitigation: Keep AFFINITY_API_KEY out of logs and prompts, use least-privilege credentials where available, and run only GET-only retrieval tasks unless policy is changed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/howdymarc/affinity-readonly) <br>
- [Affinity API base endpoint](https://api.affinity.co) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and summarized API response evidence] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AFFINITY_API_KEY in the local environment; API responses may be formatted as JSON when jq is available.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
