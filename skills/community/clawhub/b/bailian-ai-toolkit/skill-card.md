## Description:

Helps agents use a project-pinned Alibaba Cloud Bailian CLI for generation, understanding, speech, search, and file-processing tasks after explicit user selection and per-file privacy checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cryptocxf](https://clawhub.ai/user/cryptocxf)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI-agent operators use this skill to route explicitly authorized Alibaba Cloud Bailian tasks through a pinned local CLI, including text, image, video, speech, vision, web search, and single-file upload workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, URLs, search queries, generated content, and explicitly approved local files can be sent to Alibaba Cloud Bailian.

Mitigation: Use the skill only with accounts, prompts, URLs, and files the user has explicitly approved for that service; disclose destination, expected output, possible cost, and unknown retention before transfer.

Risk: OAuth login can save a cloud service session locally.

Mitigation: Run login only after the user requests it, prefer OAuth over pasted secrets, and avoid placing API keys or access secrets in chat, commands, logs, or configuration examples.

Risk: Dependency lifecycle scripts could run during installation if the local npm safeguards are bypassed.

Mitigation: Install with the bundled lockfile and `.npmrc` settings, keep `ignore-scripts=true`, use the pinned `bailian-cli@1.26.0`, and review/test any version upgrade before use.

Risk: Private, credential-bearing, or internal URLs could expose sensitive data if submitted to the cloud service.

Mitigation: Allow only public credential-free HTTPS URLs, and reject localhost, loopback, private network, link-local, cloud metadata, and tokenized URLs.

## Reference(s):

- [Bailian AI Toolkit on ClawHub](https://clawhub.ai/cryptocxf/skills/bailian-ai-toolkit)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Files]

**Output Format:** [Markdown with inline bash code blocks and output path summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference generated media, search results, uploaded-file results, models, and error summaries returned by the Alibaba Cloud Bailian CLI.]

## Skill Version(s):

1.0.1 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
