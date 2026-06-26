## Description: <br>
Looks up a Bilibili user's follower count, following count, and username for a supplied user ID. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Moxin1044](https://clawhub.ai/user/Moxin1044) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and agents use this skill to query public Bilibili profile statistics by vmid and present the results in a user-friendly form. It supports full lookups as well as focused requests for fans, follows, or username. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live requests to Bilibili can trigger service rate limits or violate expected-use norms if used for high-volume scraping. <br>
Mitigation: Query only user IDs needed for the task, add delays for batch lookups, and follow Bilibili's terms and API limits. <br>
Risk: The helper script depends on the Python requests package. <br>
Mitigation: Install requests from trusted package sources and keep the dependency updated. <br>


## Reference(s): <br>
- [Bilibili API Guide](references/api_guide.md) <br>
- [Bilibili Relation Statistics API](https://api.bilibili.com/x/relation/stat) <br>
- [ClawHub Skill Page](https://clawhub.ai/Moxin1044/bili-user-info) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON query results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill may make live requests to Bilibili for user IDs supplied by the user; avoid high-volume scraping and use trusted package sources for the Python requests dependency.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
