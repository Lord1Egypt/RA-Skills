## Description:

This skill helps website operators, brand content teams, and AI search growth consultants diagnose and optimize Chinese GEO/AEO content by producing citation-readiness scores, fact gaps, structure issues, rewrite guidance, validation plans, and optional AI-HIVE generation commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External content, marketing, ecommerce, and AI search teams use this skill to turn page text, business goals, public evidence, audience notes, and channel constraints into a reviewable GEO/AEO optimization workflow. It can also generate project blueprints, prompts, shell commands, and AI-HIVE task records when authorized visual generation is needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The executable client handles AI-HIVE API keys and can read credentials from command-line arguments, environment variables, or a local config file.

Mitigation: Use a limited, revocable API key, avoid pasting real keys into prompts or logs, and keep the generated local config file private.

Risk: A custom AI-HIVE base URL could redirect API requests away from the default trusted endpoint.

Mitigation: Use only the default AI-HIVE endpoint unless a trusted operator has reviewed and approved the replacement URL.

Risk: Media upload and result download paths may involve files that are sensitive, unlicensed, or unsuitable for third-party processing.

Mitigation: Upload only authorized, non-sensitive files and choose a non-sensitive output directory before running generation or download commands.

Risk: Image or video generation may incur costs and can create outputs that require factual, legal, or brand review.

Mitigation: Review final prompts, routing mode, model choice, and parameters before submission, start with a small sample, and manually verify claims, likenesses, trademarks, and platform constraints.

## Reference(s):

- [AI-HIVE chat and API access](https://ai-hive.iclip.cn/chat)
- [AI-HIVE API endpoint](https://ai-hive.iclip.cn/api)
- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/geo-content-diagnosis-ai-hive)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with structured checklists, inline shell commands, optional JSON files, and AI-HIVE task records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create a local blueprint JSON file and download generated media when the user authorizes AI-HIVE API execution.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
