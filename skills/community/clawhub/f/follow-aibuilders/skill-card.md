## Description: <br>
Follow AI Builders generates on-demand digests of AI builder updates from X/Twitter, YouTube podcasts, and selected blogs, with summaries available in English, Chinese, or bilingual form. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[champagne315](https://clawhub.ai/user/champagne315) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to configure a local AI industry digest, fetch public updates from selected AI builders and podcasts, and receive concise summaries with source links. It also guides users through language, lookback-window, source-list, and prompt customization. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional YouTube cookie configuration can expose local browser session data to the local fetch workflow. <br>
Mitigation: Run without YT_DLP_COOKIES when possible; if authentication is unavoidable, use a dedicated cookies.txt or service browser profile rather than a primary browser session. <br>
Risk: Digest runs intentionally perform network fetching and update local state. <br>
Mitigation: Trigger digest runs only when network fetching is expected, and keep .env credentials out of source control with restricted file permissions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/champagne315/follow-aibuilders) <br>
- [yt-dlp releases](https://github.com/yt-dlp/yt-dlp/releases) <br>
- [X Auth Helper](https://chromewebstore.google.com/detail/x-auth-helper/miflinhihdjikdpjjigaiafeoobkhikk) <br>
- [Anthropic Engineering](https://www.anthropic.com/engineering) <br>
- [Claude Blog](https://claude.com/blog) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown digest with source links and inline shell commands for setup or configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can output English, Chinese, or bilingual summaries according to local configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and scripts/package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
