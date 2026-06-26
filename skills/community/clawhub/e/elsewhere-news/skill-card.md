## Description: <br>
Browse and read articles and podcasts from Elsewhere (elsewhere.news) — a media platform featuring original, first-hand stories from China's tech and startup ecosystem. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pitayak](https://clawhub.ai/user/pitayak) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to browse Elsewhere's public articles and podcasts, rank content against the user's stated preferences, and present concise personalized recommendations or summaries with source links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Mutable remote update behavior can change the skill instructions after installation. <br>
Mitigation: Review or disable the self-update check, and require explicit user approval before fetching or adopting updated instructions. <br>
Risk: Persistent preference tracking and broad personal-context use can expose or over-collect sensitive user context. <br>
Mitigation: Keep TASTE.md local and inspectable, store only necessary preference signals, and let the user review or delete recorded preferences. <br>
Risk: Scheduled daily push automation may continue running without enough user visibility. <br>
Mitigation: Keep daily push disabled by default and enable it only after the user approves the schedule and can inspect or remove the task. <br>
Risk: Automatic article likes can send public engagement signals to Elsewhere beyond a read-only browsing workflow. <br>
Mitigation: Require explicit approval before sending article likes, or disable the like step when operating in read-only mode. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pitayak/elsewhere-news) <br>
- [Elsewhere site overview](https://elsewhere.news/llms.txt) <br>
- [Elsewhere RSS feed](https://elsewhere.news/feed.xml) <br>
- [Elsewhere public API base](https://elsewhere.news) <br>
- [TASTE.md specification](https://elsewhere.news/specs/taste) <br>
- [llms.txt standard](https://llmstxt.org) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown recommendations and summaries with source links, optional shell command examples, scheduled-task guidance, and TASTE.md preference updates.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include article or podcast URLs, concise recommendation rationale, and local preference-record updates.] <br>

## Skill Version(s): <br>
1.6.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
