## Description: <br>
Generates AI podcast episodes from PDFs, text, notes, and links using MagicPodcast in OpenClaw. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chaoliuzhu](https://clawhub.ai/user/chaoliuzhu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users use this skill to turn approved PDF URLs, pasted text, notes, and links into two-person AI podcast episodes with MagicPodcast. It guides setup, collects the topic, source, and language, starts generation, and returns dashboard or share links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected text or PDF URLs are sent to MagicPodcast for external processing. <br>
Mitigation: Avoid sensitive documents unless the user explicitly approves external processing, and confirm MAGICPODCAST_API_URL points to the intended MagicPodcast service. <br>
Risk: The skill requires a MagicPodcast API key. <br>
Mitigation: Keep MAGICPODCAST_API_KEY private and do not include it in shared logs, generated files, or user-visible output. <br>
Risk: User-provided URLs and job identifiers are used in shell commands and API calls. <br>
Mitigation: Validate HTTP URLs and job identifiers, and JSON-encode request payloads with jq before running curl commands. <br>


## Reference(s): <br>
- [MagicPodcast homepage](https://www.magicpodcast.app) <br>
- [MagicPodcast OpenClaw setup](https://www.magicpodcast.app/openclaw) <br>
- [ClawHub skill page](https://clawhub.ai/chaoliuzhu/delonix-ai-podcast) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command templates and service links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl, jq, MAGICPODCAST_API_URL, and MAGICPODCAST_API_KEY; returns MagicPodcast dashboard and share URLs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
