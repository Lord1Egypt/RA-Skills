## Description: <br>
Render article markdown into WeChat-style HTML as an independent executor for WeChat layout preview, HTML output, or publishable HTML artifacts generated from article markdown drafts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[abigale-cyber](https://clawhub.ai/user/abigale-cyber) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content operators use this skill to convert finalized article markdown into WeChat-compatible HTML for preview, inspection, and downstream publishing. It can optionally include summary, quote, share-copy, and CTA blocks from a sibling writing-pack sidecar. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The runtime imports renderer code from a hard-coded local user path outside the packaged artifact. <br>
Mitigation: Install only after inspecting that local renderer code, or use a release that vendors the helper or declares a pinned, reviewable dependency. <br>
Risk: The formatter can consume a sibling writing-pack sidecar as article input. <br>
Mitigation: Use writing-pack sidecars only from the same trusted draft directory and review generated HTML before publishing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/abigale-cyber/content-system-wechat-formatter) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [skill.json](artifact/skill.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with generated WeChat-compatible HTML file output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Primary artifact path is content-production/ready/<slug>-wechat.html; output quality depends on the source article and any trusted writing-pack sidecar.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
