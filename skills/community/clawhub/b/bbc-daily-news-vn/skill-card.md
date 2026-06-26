## Description: <br>
Fetch the latest trending global news when users ask about current or breaking news. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[MrNquyen](https://clawhub.ai/user/MrNquyen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to fetch BBC Vietnamese RSS headlines for current-news requests, then summarize returned titles, links, summaries, and publication times without changing factual content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill fetches live RSS content and may not represent comprehensive global trending news. <br>
Mitigation: Treat results as sourced BBC Vietnamese RSS headlines and preserve links, summaries, and publication times for user review. <br>
Risk: Unpinned Python dependencies can change behavior over time. <br>
Mitigation: Pin dependency versions before production use and install only in an environment where running the disclosed local script is acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/MrNquyen/bbc-daily-news-vn) <br>
- [BBC Vietnamese RSS feed](https://feeds.bbci.co.uk/vietnamese/rss.xml) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown response with sourced headline fields and optional shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Fetches up to 10 items from the BBC Vietnamese RSS feed; requires Python dependencies and UTF-8 output.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
