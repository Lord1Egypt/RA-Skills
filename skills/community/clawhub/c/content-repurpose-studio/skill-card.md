## Description: <br>
Transform one source asset into a coordinated pack for multiple channels such as WeChat, Xiaohongshu, TikTok, email, and slides. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[52YuanChangXing](https://clawhub.ai/user/52YuanChangXing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Creators, marketers, and content teams use this skill to turn one article, transcript, or source asset into coordinated channel-specific drafts, shared facts, a launch checklist, and a reuse matrix. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated channel drafts may contain inaccurate, unsupported, or publication-ready claims if the source material is incomplete. <br>
Mitigation: Review generated drafts before publishing or sharing them, and keep assumptions or unconfirmed facts explicitly marked. <br>
Risk: The helper script reads a chosen text file and writes a draft JSON pack, so careless paths can expose unintended input or overwrite an output file. <br>
Mitigation: Run the helper only on source files intended for processing and set a safe output filename. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/52YuanChangXing/content-repurpose-studio) <br>
- [README](artifact/README.md) <br>
- [Example prompt](artifact/examples/example-prompt.md) <br>
- [Channel specs](artifact/resources/channel_specs.yaml) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with structured channel-pack sections and optional JSON draft files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use a local Python helper to read a user-selected text file and write a draft JSON channel pack.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; SKILL.md frontmatter says 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
