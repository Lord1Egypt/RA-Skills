## Description: <br>
Active research intelligence that helps an agent track questions, log synthesized findings, flag contradictions, and close research threads in local markdown files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ilyabelikin](https://clawhub.ai/user/ilyabelikin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use Digs to maintain active research threads as local markdown files, capturing open questions, findings, sources, connections, and resolutions over time. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may proactively save conversation-derived research questions, links, and snippets into local markdown files. <br>
Mitigation: Use it only in workspaces where local research-note capture is expected, and review generated dig files for sensitive content. <br>
Risk: The skill can add recurring HEARTBEAT or cron behavior for periodic dig checks without clear opt-in. <br>
Mitigation: Remove or disable the HEARTBEAT or cron behavior before use unless recurring checks are explicitly desired. <br>


## Reference(s): <br>
- [ClawHub Digs skill page](https://clawhub.ai/ilyabelikin/digs) <br>
- [Peeps companion skill](https://github.com/haah-ing/peeps-skill) <br>
- [Pages companion skill](https://github.com/haah-ing/pages-skill) <br>
- [Haah companion skill](https://github.com/haah-ing/haah-skill) <br>
- [Nooks companion skill](https://github.com/haah-ing/nooks-skill) <br>
- [Vibes companion skill](https://github.com/haah-ing/vibes-skill) <br>
- [Walk Score methodology](https://www.walkscore.com/methodology.shtml) <br>
- [Cities for People](https://islandpress.org/books/cities-people) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown files, concise conversational confirmations, and occasional inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates and updates local files under mind/digs/; may also touch mind/digs/digsconfig.yml, mind/digs/closed/, HEARTBEAT.md, or local cron behavior when following the artifact instructions.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
