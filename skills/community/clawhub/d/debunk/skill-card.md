## Description: <br>
Debunk（事实核查） helps agents fact-check links, images, videos, or text and produce structured verification reports and social reply drafts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tino-chen](https://clawhub.ai/user/tino-chen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to verify factual claims in shared content, summarize source-backed findings, and draft responses for personal or social contexts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Reply-writing guidance may soften or obscure corrections when a claim is materially false. <br>
Mitigation: Review and edit generated replies so false claims are corrected clearly and supported by cited sources. <br>
Risk: The skill may fetch external web pages through browser automation for anti-scraping sites. <br>
Mitigation: Use the bundled private-address blocking, avoid untrusted internal URLs, and review fetched content before relying on it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tino-chen/debunk) <br>
- [Skill guide](https://tino-chen.github.io/notes/workflows/debunk.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown fact-check report with plain-text reply drafts and inline shell commands when URL extraction is needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May rely on web search, web fetch, Playwright URL extraction, OCR, or video-analysis tools depending on the user input and configured environment.] <br>

## Skill Version(s): <br>
1.4.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
