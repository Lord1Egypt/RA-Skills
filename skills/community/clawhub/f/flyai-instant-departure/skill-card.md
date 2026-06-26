## Description: <br>
Helps travelers find where they can depart right now by searching feasible flights, same-night hotels, attractions, and booking links from a starting city and earliest departure time. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hello-ahang](https://clawhub.ai/user/hello-ahang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel assistants use this skill to plan spontaneous trips by comparing destinations reachable from a departure city within a short time window. It returns actionable options that combine transportation, lodging, attractions, prices, and booking links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can ask an agent to install or update an unpinned global CLI package. <br>
Mitigation: Review the package source and version before installation, avoid sudo when possible, and prefer pinned versions in managed environments. <br>
Risk: The workflow documents disabling TLS verification for FlyAI searches when certificate errors occur. <br>
Mitigation: Do not run searches with TLS verification disabled unless the environment and network are trusted and the risk is explicitly accepted. <br>
Risk: The skill may persist detailed travel preferences in memory or a plaintext local profile file. <br>
Mitigation: Store profile data only after user consent and avoid saving sensitive travel, family, or location details unless necessary. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/hello-ahang/flyai-instant-departure) <br>
- [Workflow Reference](reference/workflow.md) <br>
- [User Profile Storage Reference](reference/user-profile-storage.md) <br>
- [Flight Search Reference](reference/search-flight.md) <br>
- [Hotel Search Reference](reference/search-hotel.md) <br>
- [POI Search Reference](reference/search-poi.md) <br>
- [Train Search Reference](reference/search-train.md) <br>
- [Example Conversations](reference/examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, guidance] <br>
**Output Format:** [Markdown travel options with booking links and inline FlyAI CLI command usage] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Time-sensitive travel results may include prices, availability, user travel preferences, and third-party booking URLs.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
