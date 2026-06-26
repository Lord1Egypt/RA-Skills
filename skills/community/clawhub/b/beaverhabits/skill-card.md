## Description: <br>
Track and manage your habits using the Beaver Habit Tracker API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[daya0576](https://clawhub.ai/user/daya0576) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and personal-productivity agents use this skill to list Beaver Habits records, view a recent completion overview, and mark habits done or undone through the Beaver Habit Tracker API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a Beaver Habits API token that can read and update habit completion records. <br>
Mitigation: Install only when you are comfortable granting that access, store the token securely, and rotate or revoke it if exposure is suspected. <br>
Risk: An untrusted SERVER_URL could send the API token or habit data to an unintended service. <br>
Mitigation: Leave SERVER_URL unset for the hosted Beaver Habits service or set it only to a trusted self-hosted instance. <br>
Risk: Marking the wrong habit or date can change personal habit history. <br>
Mitigation: Review habit names and dates before asking the agent to complete or uncomplete a habit. <br>


## Reference(s): <br>
- [Beaver Habit Tracker API Documentation](https://beaverhabits.com/docs) <br>
- [Beaver Habit Tracker](https://beaverhabits.com) <br>
- [Beaver Habits GitHub Project](https://github.com/daya0576/beaverhabits) <br>
- [ClawHub Skill Page](https://clawhub.ai/daya0576/beaverhabits) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Shell commands, Markdown, Guidance] <br>
**Output Format:** [Markdown text with ASCII tables, inline shell commands, and API response summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires BEAVERHABITS_API_KEY and curl; SERVER_URL is optional for trusted self-hosted Beaver Habits instances.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
