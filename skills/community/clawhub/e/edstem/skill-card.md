## Description: <br>
Fetch, sync, and organize EdStem discussion threads for any course or institution, including recent posts, staff/student role labels, and exported thread files for review. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[axel5o5](https://clawhub.ai/user/axel5o5) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, educators, teaching staff, and agents use this skill to fetch authorized EdStem course discussions, monitor new posts, review student and staff exchanges, and prepare course forum content for search or analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A bundled bearer token or user-provided token can expose EdStem account access. <br>
Mitigation: Remove and revoke the bundled token before installation, do not store personal bearer tokens in tracked source files, and keep tokens in private local secret storage. <br>
Risk: Exported EdStem threads can contain sensitive course discussions and student or staff content. <br>
Mitigation: Run the skill only for courses the user is authorized to access, write exports to private directories, avoid unattended syncing unless approved, and delete exported course data when it is no longer needed. <br>


## Reference(s): <br>
- [EdStem Skill on ClawHub](https://clawhub.ai/axel5o5/edstem) <br>
- [EdStem API](https://us.edstem.org/api) <br>
- [EdStem Course URL Pattern](https://edstem.org/us/courses/12345/) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown thread files, JSON thread metadata, and command-oriented guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an authorized EdStem course ID and authentication token; optional output directory, course name, and fetch limit control the exported files.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata, CHANGELOG.md, README.md, PUBLISHING.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
