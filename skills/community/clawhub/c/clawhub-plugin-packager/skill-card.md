## Description: <br>
Generate, repair, or audit publish-ready native OpenClaw/ClawHub plugin packages from rough, partial, or inconsistent requirements while keeping the plugin zip separate from a critique file. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[neomagnetar](https://clawhub.ai/user/neomagnetar) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to turn rough notes, partial plugin requirements, existing plugin files, or manifest drafts into native OpenClaw/ClawHub plugin packages. It can also audit or repair existing plugin drafts and produce a separate critique record for assumptions, risks, and publishability. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated provider or channel plugins may introduce API keys, webhooks, network listeners, or other side effects. <br>
Mitigation: Review generated plugin files, manifests, configuration schemas, and critique records before publishing or running them. <br>
Risk: Generated plugin behavior may rely on inferred requirements when the user's source material is incomplete. <br>
Mitigation: Use the separate critique record to check assumptions, repairs, simplifications, and publishability before release. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/neomagnetar/clawhub-plugin-packager) <br>
- [README](artifact/README.md) <br>
- [Plugin spec template](artifact/PLUGIN-SPEC-TEMPLATE.yaml) <br>
- [Portability notes](artifact/PORTABILITY.md) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Code, Markdown, Configuration, Guidance] <br>
**Output Format:** [Native plugin package files plus a separate plain-text critique record] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated plugin packages are expected to keep release files separate from critique and review notes.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata; artifact frontmatter and changelog report 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
