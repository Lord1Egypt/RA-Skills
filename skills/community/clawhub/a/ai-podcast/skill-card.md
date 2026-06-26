## Description: <br>
Generate AI podcast episodes from PDFs, text, notes, and links using MagicPodcast in OpenClaw. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mogens9](https://clawhub.ai/user/mogens9) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to turn PDF URLs, pasted text, notes, or links into two-person podcast episodes and retrieve dashboard or share links from MagicPodcast. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The selected PDF URL or pasted text is sent to MagicPodcast for processing. <br>
Mitigation: Submit only content you have permission to share, and avoid confidential documents unless MagicPodcast privacy and retention terms are acceptable. <br>
Risk: The skill requires a MagicPodcast API key for generation and status checks. <br>
Mitigation: Store the key in the MAGICPODCAST_API_KEY environment variable and avoid exposing it in prompts, shared logs, or generated output. <br>


## Reference(s): <br>
- [MagicPodcast](https://www.magicpodcast.app) <br>
- [MagicPodcast OpenClaw API Key](https://www.magicpodcast.app/openclaw) <br>
- [MagicPodcast Dashboard](https://www.magicpodcast.app/app) <br>
- [ClawHub Skill Page](https://clawhub.ai/mogens9/ai-podcast) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, API calls, Guidance] <br>
**Output Format:** [Markdown-style guidance with curl command templates, status text, and podcast URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl, jq, MAGICPODCAST_API_URL, and MAGICPODCAST_API_KEY; generated podcast links are returned when available.] <br>

## Skill Version(s): <br>
1.0.11 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
