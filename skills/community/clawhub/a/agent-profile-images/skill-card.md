## Description: <br>
Agent Profile Images for OpenClaw Control UI - upload custom avatars, generate themed AI profile images, preview before saving, and persist agent avatars across refreshes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[maverick-software](https://clawhub.ai/user/maverick-software) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to add avatar upload, themed AI image generation, preview controls, and persistent profile image handling to an OpenClaw Control UI agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The package bundles broad OpenClaw control-panel source snapshots that can affect behavior outside avatar handling. <br>
Mitigation: Apply only a narrow reviewed diff against the exact OpenClaw version in use, and check unrelated admin, file, credential, and wizard code paths before deployment. <br>
Risk: Avatar upload, removal, and generation are admin-scoped changes that touch agent workspace files and identity metadata. <br>
Mitigation: Review method scopes, file path handling, image type limits, and IDENTITY.md updates before enabling these methods in a live control UI. <br>
Risk: The implemented image generation path uses OpenAI Images. <br>
Mitigation: Confirm provider credentials, data handling, cost controls, and policy requirements before enabling AI avatar generation. <br>


## Reference(s): <br>
- [Skill package overview](artifact/SKILL.md) <br>
- [Gateway method scopes snapshot](artifact/references/src-gateway-method-scopes-ts.txt) <br>
- [Gateway protocol schema snapshot](artifact/references/src-gateway-protocol-schema-agents-models-skills-ts.txt) <br>
- [Gateway avatar method implementation snapshot](artifact/references/src-gateway-server-methods-agents-ts.txt) <br>
- [Gateway session utilities snapshot](artifact/references/src-gateway-session-utils-ts.txt) <br>
- [Agents overview UI snapshot](artifact/references/ui-src-ui-views-agents-panels-overview-ts.txt) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Configuration, Guidance] <br>
**Output Format:** [Markdown package instructions with TypeScript source snapshots] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces source-level feature implementation guidance for OpenClaw agent avatar upload, generation, preview, removal, and persistence behavior.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
