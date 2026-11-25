## Description:

Improve AI image realism without starting over. This focused AI image editor and humanizer targets visible AI image artifacts—plastic skin, malformed hands or faces, extra fingers, repeated textures, and inconsistent lighting—with focused AI image retouching through a local repair or natural whole-image refinement. Use it to make AI portraits, product images, marketing graphics, and social covers look more realistic, remove the obvious AI look, fix AI hands and extra fingers, or refine product imagery, while aiming to keep identity, product shape, brand details, and composition recognizable where possible.

This skill is ready for commercial/non-commercial use.

## Publisher:

[beatra-ai](https://clawhub.ai/user/beatra-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and creative professionals use an agent to diagnose and repair visible AI-generated image artifacts in existing portraits, product images, marketing visuals, and social covers while preserving named identity, branding, and composition details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release is marked suspicious with high confidence because the scanners report broad account permissions and persistent shared credentials beyond the stated image-retouching purpose.

Mitigation: Review the requested account permissions and shared-credential behavior carefully; avoid installation unless you are comfortable granting that access and sharing a persistent credential across packages.

Risk: The security scan was partial because some local references in SKILL.md could not be resolved, leaving evidence about those referenced capabilities incomplete.

Mitigation: Review the unresolved referenced capabilities before installation or granting account access.

## Reference(s):

- [Beatra skill page](https://beatra.ai/skills/ai-image-realism)
- [Diagnosis and routing](references/diagnosis-and-routing.md)
- [Repair recipes](references/repair-recipes.md)
- [Review and recovery](references/review-and-recovery.md)
- [Tasks and results](references/tasks-and-results.md)
- [Billing, errors, and recovery](references/billing-errors-and-recovery.md)
- [Installation and authentication](references/installation-and-auth.md)
- [MCP connection diagnostics](references/mcp-connection.md)
- [Updates and security](references/updates-and-security.md)

## Skill Output:

**Output Type(s):** [Image files, Guidance, Task status and billing details]

**Output Format:** [Edited image files or artifact links with a concise Markdown summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Usually one output per request; edits preserve the source aspect ratio unless the user requests a change.]

## Skill Version(s):

0.3.8 (source: manifest.json, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
