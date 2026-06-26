## Description: <br>
Fetches articles, videos, podcasts, and PDFs, then converts, transcribes, translates, and archives the results to a Lexiang knowledge base. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ajaxhe](https://clawhub.ai/user/ajaxhe) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and knowledge workers use this skill to fetch source content, preserve source links and media, translate or transcribe when needed, and archive the resulting material into a Lexiang knowledge base. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can reuse browser login state and local Lexiang or MCP credentials while fetching and archiving content. <br>
Mitigation: Use a dedicated browser profile and dedicated low-privilege tokens, and review credential setup scripts before running them. <br>
Risk: The skill can write content into a Lexiang knowledge base. <br>
Mitigation: Confirm the target space and permissions before use, and prefer tokens scoped to the intended knowledge base. <br>
Risk: Fetching, translating, or archiving paywalled or third-party content may exceed the user's rights or policy obligations. <br>
Mitigation: Confirm authorization to access, transform, and store the target content before executing the workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ajaxhe/skills/fetch-archive-to-lexiang) <br>
- [README](artifact/README.md) <br>
- [Lexiang upload workflow](artifact/references/lexiang-upload.md) <br>
- [PDF archive workflow](artifact/references/pdf-processing.md) <br>
- [YouTube video workflow](artifact/references/youtube-video.md) <br>
- [Podcast audio workflow](artifact/references/podcast-audio.md) <br>
- [Platform-specific handling](artifact/references/platform-specific.md) <br>
- [Troubleshooting](artifact/references/troubleshooting.md) <br>
- [Lexiang](https://lexiangla.com) <br>
- [Lexiang MCP token page](https://lexiangla.com/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, API calls, Guidance] <br>
**Output Format:** [Markdown guidance with command snippets, JSON configuration examples, generated files, and Lexiang links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local Markdown/media artifacts and write or update entries in a configured Lexiang knowledge base.] <br>

## Skill Version(s): <br>
2.8.2 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
