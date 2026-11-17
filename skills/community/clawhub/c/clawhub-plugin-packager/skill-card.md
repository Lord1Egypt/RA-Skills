## Description:

Generate, repair, or audit publish-ready native OpenClaw/ClawHub plugin packages from rough, partial, or inconsistent requirements while keeping the plugin zip separate from a critique file.

This skill is ready for commercial/non-commercial use.

## Publisher:

[neomagnetar](https://clawhub.ai/user/neomagnetar)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to generate, repair, or audit native OpenClaw/ClawHub plugin packages from rough requirements, partial specs, existing plugin folders, manifests, code fragments, or README drafts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated provider or channel plugins may introduce credentials, network access, or side effects.

Mitigation: Review generated plugins before publishing and verify any credential, network, or side-effect behavior against the intended plugin requirements.

Risk: Generated plugin packages are based on user-provided or inferred requirements, so publishability depends on the accuracy of those inputs and inferences.

Mitigation: Use the separate critique file and review checklist to confirm assumptions, repairs, simplifications, and remaining follow-up items before release.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/neomagnetar/skills/clawhub-plugin-packager)
- [Publisher Profile](https://clawhub.ai/user/neomagnetar)
- [README](artifact/README.md)
- [Portability Notes](artifact/PORTABILITY.md)
- [Plugin Spec Template](artifact/PLUGIN-SPEC-TEMPLATE.yaml)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown and plain-text guidance with generated plugin package files such as TypeScript, JSON, YAML, and README content.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [For generation jobs, the skill produces a plugin package zip and a separate critique file; audit-only mode produces review guidance without a package unless explicitly requested.]

## Skill Version(s):

1.0.2 (source: server release metadata; artifact frontmatter and changelog report 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
