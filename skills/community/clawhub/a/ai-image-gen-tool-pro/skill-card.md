## Description:

AI图像生成-专业版 is a documentation-style skill that guides agents through professional image-generation workflows including 4K output, image-to-image variation, style transfer, batch generation, and related configuration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and design teams use this skill to guide text-to-image, image-to-image, style-transfer, and batch image-generation workflows for commercial design and marketing assets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests command and file authority without providing working scripts or enforced command safeguards.

Mitigation: Inspect every proposed command before execution, avoid running untrusted command templates, and direct outputs to a dedicated folder with explicit limits.

Risk: Image generation requires API credentials that could be exposed if copied into scripts or logs.

Mitigation: Store API keys in environment variables or secret storage and avoid hardcoding keys in prompts, scripts, or generated files.

Risk: The artifact claims structured output, error handling, and safety controls that the security evidence says are unsupported.

Mitigation: Treat the skill as guidance rather than an implemented tool, and independently validate outputs, error handling, and any generated assets before production use.

Risk: Broad activation rules may cause the skill to be used outside its image-generation scope.

Mitigation: Invoke it only for design, marketing, image-generation, image-to-image, style-transfer, or batch image workflow requests.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/ai-image-gen-tool-pro)
- [Publisher profile](https://clawhub.ai/user/thcjp)
- [Referenced Gemini image API endpoint](https://code.newcli.com/gemini)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, JSON]

**Output Format:** [Markdown with bash and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The artifact provides guidance and example command patterns; evidence indicates no working scripts, enforced command safeguards, JSON validation, or automatic error recovery are provided.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
