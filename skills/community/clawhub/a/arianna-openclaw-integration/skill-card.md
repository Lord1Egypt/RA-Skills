## Description: <br>
Integrates the Playfilo shared-memory DAG into OpenClaw via pnpm patch on the embedded pi-coding-agent and layers on top of arianna-pi-integration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wujilabs](https://clawhub.ai/user/wujilabs) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to integrate Playfilo durable DAG memory and temporal tools into OpenClaw. It provides patch, plugin, dependency, and verification guidance for an OpenClaw installation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The integration patches OpenClaw's embedded agent runtime and changes tool persistence behavior. <br>
Mitigation: Review the patch steps before applying them, pin the exact pi-coding-agent version, and run the supplied type-check, build, and persistence verification checklist. <br>
Risk: Prompts, tool use, and conversation history may be stored in ~/.playfilo/playfilo.db. <br>
Mitigation: Avoid enabling the skill in restricted or sensitive sessions unless durable local memory is intended and appropriate controls are in place. <br>
Risk: The plugin prepends local ~/.playfilo/INCUBATION_SEED.md content into the system prompt. <br>
Mitigation: Inspect INCUBATION_SEED.md before enabling the plugin and confirm that its contents are acceptable for the target OpenClaw environment. <br>


## Reference(s): <br>
- [Arianna homepage](https://arianna.run) <br>
- [ClawHub skill page](https://clawhub.ai/wujilabs/arianna-openclaw-integration) <br>
- [Skill documentation](artifact/SKILL.md) <br>
- [Verification checklist](artifact/patches/verify.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown instructions with TypeScript, JSON, shell command snippets, and verification checklists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces patch and plugin implementation guidance; does not execute installation by itself.] <br>

## Skill Version(s): <br>
0.1.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
