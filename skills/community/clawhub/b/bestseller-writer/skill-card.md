## Description: <br>
Turn a shower idea into a full best-seller manuscript in one command using a multi-agent pipeline that plans, writes, edits, and packages fiction or non-fiction books for Amazon KDP. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[PhilipStark](https://clawhub.ai/user/PhilipStark) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators, authors, and publishing-focused operators use this skill to turn a book idea into a generated manuscript, editorial memo, and Amazon KDP publishing package. Developers and agent users can run the included CLI or orchestrate the documented multi-stage workflow inside OpenClaw. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run a long Anthropic-powered generation workflow that sends the book idea and manuscript context to Anthropic and may incur API costs. <br>
Mitigation: Use non-sensitive material, provide an Anthropic API key only in an appropriate environment, and review expected model usage before running. <br>
Risk: The workflow creates multiple local manuscript and publishing-package files. <br>
Mitigation: Set an explicit output directory and review generated files before publishing or sharing them. <br>
Risk: Generated manuscripts and KDP metadata may contain inaccurate, misleading, or commercially unsuitable content. <br>
Mitigation: Fact-check and edit the manuscript, keywords, categories, pricing, and KDP package before publication. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/PhilipStark/bestseller-writer) <br>
- [Publisher profile](https://clawhub.ai/user/PhilipStark) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown files plus CLI status output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes a manuscript, KDP package, plan, character or authority notes, and editorial memo to a local output directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, package.json, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
