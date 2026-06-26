## Description: <br>
Search, inspect, and install Clawic skills from GitHub with local lexical matching, registry overrides, and safe destination control. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to choose the right `clawic` commands for discovering, inspecting, and installing Clawic skills from a registry while keeping write destinations and overwrite behavior explicit. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Running `npx clawic` may fetch the published npm package if it is not already cached locally. <br>
Mitigation: Install only if the npm package is trusted; use a global install or a pinned project workflow when repeatability matters. <br>
Risk: Installing a skill downloads and writes files from the active registry into the selected destination. <br>
Mitigation: Inspect the slug with `show` first, use a scratch or project-specific destination, and install only from a trusted registry. <br>
Risk: Using `--force` can overwrite previously reviewed files in the target skill directory. <br>
Mitigation: Use `--force` only when replacement is intentional and the destination is disposable or already reviewed. <br>
Risk: Optional local memory under `~/clawic/` could accidentally record sensitive workflow details if used carelessly. <br>
Mitigation: Store reusable defaults only and do not save secrets or credentials in Clawic memory files. <br>


## Reference(s): <br>
- [Clawic CLI Skill Page](https://clawic.com/skills/clawic) <br>
- [ClawHub Release Page](https://clawhub.ai/ivangdavila/clawic) <br>
- [Default Clawic Registry Index](https://raw.githubusercontent.com/clawic/skills/main/registry/index.json) <br>
- [Clawic Registry Base](https://raw.githubusercontent.com/clawic/skills/main/registry) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and concise operational guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include install destination choices, registry base checks, and safety notes for npm execution and file writes.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
