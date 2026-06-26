## Description: <br>
Checks whether provided hardware resource assessment elements for a supported clinical product are complete against a local Markdown knowledge base. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hellohushuai](https://clawhub.ai/user/hellohushuai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to verify whether submitted hardware resource assessment elements for supported clinical products match the required inputs. It can return a simple completion confirmation or identify missing assessment elements. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release security scan verdict is suspicious and recommends review before installation. <br>
Mitigation: Review the skill before installing it and use it only in trusted ClawHub maintenance environments. <br>
Risk: The comparison script reads a local knowledge-base directory and depends on product-name matching plus a specific Markdown section structure. <br>
Mitigation: Provide an explicit trusted kb_dir and review missing-element results against the source knowledge-base files before relying on the output. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hellohushuai/get-resource-element) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [Plain text or JSON, with optional shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns ok when all elements are satisfied; otherwise lists missing assessment elements.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
