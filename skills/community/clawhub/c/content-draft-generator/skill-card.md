## Description: <br>
Generates content drafts by analyzing reference URLs, extracting reusable writing patterns, collecting user context, creating a meta-prompt, and producing draft variations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vincentchan](https://clawhub.ai/user/vincentchan) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users, developers, and content teams use this skill to model new articles, posts, or tweets after selected reference examples. It guides an agent through URL collection, content analysis, context gathering, meta-prompt creation, and generation of three draft variations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow fetches user-provided URLs, which could expose private, internal, signed, or tokenized links to the agent runtime or external fetch services. <br>
Mitigation: Use public reference links only and avoid submitting private, internal, signed, or tokenized URLs. <br>
Risk: Generated markdown files may contain confidential strategy, positioning, or draft content supplied during the context interview. <br>
Mitigation: Review generated files before sharing them and delete local artifacts that contain sensitive material. <br>
Risk: Twitter/X references may be transformed to FxTwitter API URLs, so users should expect those references to be fetched through that service. <br>
Mitigation: Do not provide Twitter/X links unless use of FxTwitter for retrieval is acceptable. <br>


## Reference(s): <br>
- [Content Deconstructor](references/content-deconstructor.md) <br>
- [Content Anatomy Generator](references/content-anatomy-generator.md) <br>
- [Content Context Generator](references/content-context-generator.md) <br>
- [Meta Prompt Generator](references/meta-prompt-generator.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown files and conversational Markdown responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces timestamped markdown artifacts for content breakdowns, anatomy guides, context requirements, meta-prompts, and final content drafts.] <br>

## Skill Version(s): <br>
1.0.2 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
