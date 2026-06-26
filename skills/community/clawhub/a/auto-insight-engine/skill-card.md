## Description: <br>
Collects insight signals from Hacker News, GitHub, Wikipedia, RSS, ArXiv, and extended search, then reports status, trends, or a collection-cycle result. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[534422530](https://clawhub.ai/user/534422530) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators can use this skill to run a local insight-collection cycle, inspect engine status, and review stored trend keywords. It is most appropriate where the local engine module and any external data sharing have been reviewed before deployment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill imports and delegates execution to a separate local auto_insight_engine module that is not bundled in the artifact. <br>
Mitigation: Install only in an environment where that local module is trusted and reviewed before using run, status, or trends modes. <br>
Risk: The skill describes broad network collection, third-party analysis, and knowledge-base ingestion with weak scoping and disclosure. <br>
Mitigation: Confirm what data may be sent to external sources or NVIDIA NIM and what may be written into any knowledge base before deployment. <br>
Risk: The artifact documentation contains unrelated Bilibili-learned sections mixed into the skill description. <br>
Mitigation: Remove or split unrelated learned content before broad deployment so users can review the actual skill behavior clearly. <br>


## Reference(s): <br>
- [ClawHub skill page: Auto Insight Engine](https://clawhub.ai/534422530/auto-insight-engine) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, guidance] <br>
**Output Format:** [JSON object containing status, trends, run results, or error messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The artifact exposes run, status, and trends modes and may depend on a separate local auto_insight_engine module.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
