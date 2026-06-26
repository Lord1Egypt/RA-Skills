## Description: <br>
Summarize or extract text and transcripts from URLs, podcasts, local files, and YouTube or video links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[utromaya-code](https://clawhub.ai/user/utromaya-code) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to have an agent invoke the summarize CLI for article, URL, local-file, podcast, and video summarization or best-effort transcript extraction. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Content summarized by the skill may be sent to the configured model provider or optional extraction provider. <br>
Mitigation: Avoid confidential files, private URLs, and sensitive videos unless sharing that content with the selected provider or fallback service is acceptable. <br>
Risk: The skill depends on an external Homebrew package and provider credentials configured outside the skill. <br>
Mitigation: Install only if the external package and configured providers are trusted, and scope API keys according to the intended use. <br>


## Reference(s): <br>
- [Summarize homepage](https://summarize.sh) <br>
- [ClawHub skill listing](https://clawhub.ai/utromaya-code/content-summarizer) <br>
- [Publisher profile](https://clawhub.ai/user/utromaya-code) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and optional JSON CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use configured model providers and optional extraction services; supports summary length, token limit, extraction-only, JSON, Firecrawl, and YouTube fallback flags.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
