## Description: <br>
Use when exporting, importing, packaging, cloning, restoring, or moving an OpenClaw agent between machines or instances, especially when the user mentions clawpacker, .ocpkg packages, agent portability, or reusable agent templates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lc708](https://clawhub.ai/user/lc708) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to find current Clawpacker guidance before exporting, importing, packaging, cloning, restoring, or moving portable OpenClaw agent bundles. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes mutable remote GitHub instructions authoritative for operations that can change local OpenClaw agent state. <br>
Mitigation: Review the GitHub-hosted SKILL.md before each use, prefer a pinned commit or local reviewed copy, and confirm source, destination, dry-run output, and overwrite or force options before allowing import or restore commands. <br>
Risk: If the canonical source is unavailable, guessing Clawpacker command syntax or flags could lead to incorrect package operations. <br>
Mitigation: Stop and request an updated repository path or current local SKILL.md instead of inventing commands. <br>


## Reference(s): <br>
- [Canonical Clawpacker skill (master)](https://raw.githubusercontent.com/cogine-ai/clawpack/master/skills/clawpacker/SKILL.md) <br>
- [Canonical Clawpacker skill (main fallback)](https://raw.githubusercontent.com/cogine-ai/clawpack/main/skills/clawpacker/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with inline shell commands and URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Directs the agent to fetch canonical Clawpacker instructions before proposing package operations.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
