## Description: <br>
DarkMatter helps agents commit context, pull verified upstream context, replay decision chains, fork from checkpoints, and verify chain integrity for lineage-tracked multi-agent handoffs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bengunvl](https://clawhub.ai/user/bengunvl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to pass work between agents with lineage tracking, including committing context, pulling verified upstream context, replaying or forking decision chains, verifying integrity, and exporting audit artifacts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send and retain raw agent context, including inputs, outputs, memory, prompts, and task data, on a third-party service. <br>
Mitigation: Use it only when DarkMatter or a trusted self-hosted equivalent is intended, and redact secrets, personal data, proprietary prompts, confidential outputs, and unnecessary memory before committing payloads. <br>
Risk: Context may be committed to the wrong recipient agent or lineage if identifiers are not checked. <br>
Mitigation: Verify the recipient agent ID and parent context ID before committing, forking, replaying, or exporting lineage data. <br>
Risk: The required API key can authorize access to sensitive context operations if exposed. <br>
Mitigation: Store the API key in the DARKMATTER_API_KEY environment variable, avoid pasting it into prompts or logs, and rotate it if it may have been exposed. <br>
Risk: Replay and export files can expose sensitive audit history and context payloads. <br>
Mitigation: Treat replay output and exported JSON artifacts as sensitive records and restrict their storage, sharing, and retention. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/bengunvl/darkmatter) <br>
- [DarkMatter homepage](https://darkmatterhub.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with curl command examples and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires DARKMATTER_API_KEY and curl; remote operations can create, retrieve, replay, fork, verify, and export DarkMatter context records.] <br>

## Skill Version(s): <br>
2.0.0 (source: ClawHub release metadata and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
