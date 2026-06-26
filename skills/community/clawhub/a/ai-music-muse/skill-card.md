## Description: <br>
Muse AI helps an agent guide users through conversational AI music creation, including songs with vocals, custom lyrics and style choices, and instrumental background music. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[a64307410](https://clawhub.ai/user/a64307410) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to create original songs, lyrics, and instrumental background music through a guided chat workflow backed by Muse service calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles Muse login tokens and stores them locally under ~/.muse/token. <br>
Mitigation: Do not paste tokens into shared or logged chats, and remove ~/.muse/token when the skill is no longer used or the machine is shared. <br>
Risk: The security evidence flags the release as suspicious because users must trust the Muse service and publisher before installing or authenticating. <br>
Mitigation: Install only after reviewing the package and trusting the publisher and Muse service; prefer the reviewed package over the README's git-clone installer. <br>
Risk: Song prompts, lyrics, task IDs, and an anonymous device ID are sent to Muse service endpoints during generation and status checks. <br>
Mitigation: Avoid submitting sensitive or confidential lyrics and review the Muse service relationship before commercial use. <br>


## Reference(s): <br>
- [Muse style catalog](references/style-catalog.md) <br>
- [Muse registration guide](assets/register-guide.md) <br>
- [ClawHub skill page](https://clawhub.ai/a64307410/ai-music-muse) <br>
- [Muse registration page](https://skills.muse.top/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, api calls, guidance] <br>
**Output Format:** [Conversational Markdown with inline shell commands and JSON responses from helper scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include generated song metadata, audio URLs, cover URLs, lyrics previews, task IDs, and authentication prompts.] <br>

## Skill Version(s): <br>
1.0.6 (source: frontmatter, package.json, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
