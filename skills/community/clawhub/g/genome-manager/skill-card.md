## Description: <br>
Genome Manager helps agents create, store, retrieve, mutate, list, and validate Genome Evolution Protocol genome JSON files for reusable behavior patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[KyleChen26](https://clawhub.ai/user/KyleChen26) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to maintain local GEP genome libraries that capture successful workflows, track lineage, and prepare patterns for reuse or sharing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Unvalidated genome names may read or write JSON files outside the intended local genome folder. <br>
Mitigation: Use simple basename-only genome names, avoid path separators, and review local genome files before reuse or sharing. <br>
Risk: Genome prompts or metadata may contain sensitive information if users store secrets in genome records. <br>
Mitigation: Do not store secrets in prompts or metadata, and inspect genome JSON files before sharing them. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, JSON files] <br>
**Output Format:** [Markdown guidance with shell commands and JSON genome records] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates and reads local genome JSON files under the user's OpenClaw genome directory.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
