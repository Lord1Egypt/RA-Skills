## Description:

AI-optimized web search, image search and content extraction via BytePlus InfoQuest API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[infoquest-byteplus](https://clawhub.ai/user/infoquest-byteplus)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to gather current web results, image results, and clean content from specific URLs through BytePlus InfoQuest. It is useful for research, source discovery, image reference lookup, and webpage extraction workflows that can send the requested queries or URLs to BytePlus.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries, URLs, and extracted webpage content are sent to BytePlus InfoQuest.

Mitigation: Avoid using the skill with secrets, private internal URLs, proprietary documents, or regulated personal data unless that use is approved.

Risk: Node.js versions older than 18 require an optional node-fetch install path.

Mitigation: Prefer Node.js 18 or newer; if older Node.js must be used, pin and review the node-fetch dependency before deployment.

Risk: The skill requires an INFOQUEST_API_KEY to call the external API.

Mitigation: Store the API key in approved secret management and avoid logging or sharing it in prompts, command history, or output.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/infoquest-byteplus/skills/byted-infoquest-search)
- [BytePlus InfoQuest documentation](https://docs.byteplus.com/en/docs/InfoQuest/What_is_Info_Quest)
- [BytePlus InfoQuest API console](https://console.byteplus.com/infoquest/infoquests)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [JSON search result objects and Markdown-formatted extracted webpage content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and INFOQUEST_API_KEY; search queries, image searches, URLs, and extracted page requests are sent to BytePlus InfoQuest.]

## Skill Version(s):

1.0.3 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
