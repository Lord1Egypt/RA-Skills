## Description:

Create, generate, convert, and polish ad copy, marketing copy, product copy, landing page copy, headline variants, CTA variants, and promotional messaging through the WeryAI chat completion API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fwwdn](https://clawhub.ai/user/fwwdn)

### License/Terms of Use:

MIT-0

## Use Case:

External users and marketing teams use this skill to draft, rewrite, and polish persuasive copy for ads, landing pages, launches, headlines, CTA variants, and campaign messaging.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credential and prompt-data exposure can occur through endpoint override behavior.

Mitigation: Leave WERYAI_BASE_URL unset unless intentionally using a trusted HTTPS WeryAI-compatible endpoint, and use a revocable API key.

Risk: Submitted marketing material is sent to WeryAI and real runs may consume paid credits.

Mitigation: Review inputs before execution, avoid sending sensitive source copy unless approved, and use dry-run mode when inspecting payload shape.

Risk: Verbose logging may expose prompts or source copy.

Mitigation: Avoid --verbose when prompts, product briefs, campaign copy, or other source material is sensitive.

## Reference(s):

- [Ad Copy Writer Reference](artifact/references/domain.md)
- [WeryAI API endpoint](https://api.weryai.com)
- [ClawHub skill page](https://clawhub.ai/fwwdn/skills/ad-copy-writer)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Plain text or Markdown copy; script helpers return JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses WERYAI_API_KEY, requires Node.js 18 or newer, supports dry-run payload inspection, and may consume paid WeryAI credits during real API calls.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
