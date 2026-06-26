## Description: <br>
Manage Capacities notes, daily entries, and weblinks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[davidsmorais](https://clawhub.ai/user/davidsmorais) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to add notes, tasks, thoughts, and weblinks to a Capacities workspace and to look up object and space information through the Capacities API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent uses a Capacities API token and can send note text, URLs, search terms, and space metadata to Capacities. <br>
Mitigation: Install only when this access is intended, keep CAPACITIES_API_TOKEN scoped and protected, and avoid sending secrets or highly sensitive material unless it should be stored in Capacities. <br>
Risk: When multiple Capacities spaces exist, content may be saved to an unintended space if no space ID is provided. <br>
Mitigation: Set CAPACITIES_SPACE_ID explicitly when using multiple spaces and review content before saving. <br>


## Reference(s): <br>
- [ClawHub Capacities skill page](https://clawhub.ai/davidsmorais/capacities) <br>
- [Capacities save-to-daily-note endpoint](https://api.capacities.io/save-to-daily-note) <br>
- [Capacities save-weblink endpoint](https://api.capacities.io/save-weblink) <br>
- [Capacities lookup endpoint](https://api.capacities.io/lookup) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires CAPACITIES_API_TOKEN; CAPACITIES_SPACE_ID is optional for selecting a workspace.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
