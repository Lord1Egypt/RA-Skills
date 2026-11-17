## Description: <br>
ai-podcast-free helps agents turn pasted plain text into a two-host conversational podcast through the MagicPodcast API and return a shareable link. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to create shareable podcast audio from pasted plain text, with the language explicitly chosen before calling MagicPodcast. It is suited to blog posts, study notes, and similar text-to-audio workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad triggers and overstated translation, localization, PDF, file-processing, or custom-voice claims could cause users or agents to apply the skill outside its supported text-to-podcast workflow. <br>
Mitigation: Use this release only for plain text that the user intentionally wants to send to MagicPodcast, and avoid unsupported workflows unless the publisher updates the documentation and API fields. <br>
Risk: Podcast source text is sent to an external MagicPodcast service. <br>
Mitigation: Review text for sensitive or restricted content before use and avoid sending content that should not leave the user's approved environment. <br>
Risk: The workflow requires a MagicPodcast API key. <br>
Mitigation: Store the key in environment variables, keep it out of source control and logs, and rotate it if exposure is suspected. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/ai-podcast-free) <br>
- [MagicPodcast API key setup](https://www.magicpodcast.app/skill-platform) <br>
- [MagicPodcast dashboard](https://www.magicpodcast.app/app) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, API calls, Text] <br>
**Output Format:** [Markdown with shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns setup guidance, task status handling, and shareable MagicPodcast links when generation completes.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
