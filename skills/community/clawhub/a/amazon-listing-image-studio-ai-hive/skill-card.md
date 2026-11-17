## Description:

Helps Amazon sellers, cross-border brands, and listing operations teams turn product facts, authorized assets, brand rules, and marketplace constraints into Amazon listing image plans, prompts, runnable AI-HIVE commands, draft A+ content, and review checklists.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External Amazon sellers, cross-border brands, listing operators, and commerce content teams use this skill to plan and produce marketplace-ready product images, A+ page drafts, prompts, command examples, and quality checks. When generation is requested, the skill guides AI-HIVE OpenAPI model lookup, pricing snapshot review, media upload, task polling, and result download.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores and uses a persistent AI-HIVE API key, and the API endpoint can be overridden.

Mitigation: Use a dedicated limited API key, keep the default AI-HIVE HTTPS endpoint unless a custom endpoint is fully trusted, review ~/.ai-hive/config.json, and rotate the key when needed.

Risk: Product images, prompts, and other reference media may be uploaded to AI-HIVE for generation.

Mitigation: Use the skill only when AI-HIVE is trusted for the project and the uploaded product, brand, logo, personal, or third-party materials are authorized for that use.

Risk: Image or video generation can be billable and may create repeated charges during batch work.

Mitigation: Confirm model, routing mode, parameters, pricing snapshot, and batch size before submission; start with a small sample and keep task records for deduplication and review.

Risk: Generated listing content can become misleading if it invents certifications, effects, testimonials, ranking claims, or platform outcomes.

Mitigation: Require factual product inputs, source-backed claims, human review, and rejection of requests to fake endorsements, bypass platform rules, or copy protected content.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/amazon-listing-image-studio-ai-hive)
- [AI-HIVE chat and API access](https://ai-hive.iclip.cn/chat)
- [AI-HIVE API endpoint](https://ai-hive.iclip.cn/api)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash commands, JSON task records, and checklist-style guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include generated blueprint JSON files, AI-HIVE task identifiers, price snapshots, task status, and downloaded media file locations when users run the provided scripts.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
