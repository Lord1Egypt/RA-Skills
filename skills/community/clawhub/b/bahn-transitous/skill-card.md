## Description: <br>
Search Deutsche Bahn train connections using the bahn-cli tool for German station routes, departure times, and travel planning. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bone187](https://clawhub.ai/user/bone187) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel-planning agents use this skill to find Deutsche Bahn train connections between German stations, including departure and arrival details, platforms, duration, transfers, stops, and train numbers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill calls a local ~/Code/bahn-cli implementation whose source is not provided or pinned in the artifact. <br>
Mitigation: Use it only with a trusted local bahn-cli installation, and inspect or pin that implementation before running generated shell commands. <br>


## Reference(s): <br>
- [Transitous](https://transitous.org/) <br>
- [ClawHub Skill Page](https://clawhub.ai/bone187/bahn-transitous) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and summarized train connection details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Results depend on the local ~/Code/bahn-cli implementation and the Transitous-backed train data available at query time.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
