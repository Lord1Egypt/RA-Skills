## Description: <br>
Content Creator coordinates humanizer, de-ai-ify, copywriting, and tweet-writer workflows to produce persuasive, platform-ready social content while preserving factual integrity. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[h4gen](https://clawhub.ai/user/h4gen) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and content teams use this skill to draft LinkedIn posts and X thread adaptations with clearer hooks, voice edits, persuasion structure, and factual-integrity checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Setup commands use npx and include an update-all step that can change installed skill behavior. <br>
Mitigation: Review the install and update commands before running them, and confirm the resolved upstream skills match the intended versions. <br>
Risk: Humanized social copy could mislead readers if it implies personal experience, evidence, or certainty the user did not provide. <br>
Mitigation: Require explicit author context and proof points, preserve uncertainty, and avoid fabricated anecdotes, citations, or guaranteed outcome claims. <br>
Risk: The skill depends on separate upstream writing skills, so missing or changed dependencies can alter output quality. <br>
Mitigation: Verify that humanizer, de-ai-ify, copywriting, and tweet-writer are installed before use and recheck outputs against the stated quality gates. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/h4gen/content-creator-skill) <br>
- [Inspected Upstream Skills](references/inspected-skills.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown sections containing final social copy, edit summaries, persuasion-structure notes, a five-tweet X thread, and optional hook or CTA variants.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should avoid fabricated anecdotes, unsupported claims, guaranteed reach claims, and manipulative persuasion.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
