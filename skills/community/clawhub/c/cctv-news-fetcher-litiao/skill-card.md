## Description: <br>
Fetch and parse news highlights from CCTV News Broadcast (Xinwen Lianbo) for a given date. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[litiao1224](https://clawhub.ai/user/litiao1224) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to retrieve CCTV News Broadcast highlights for a requested date and summarize the returned items. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes outbound requests to retrieve news content. <br>
Mitigation: Install only in environments where network access to CCTV news pages is expected, and review the requested date argument before execution. <br>
Risk: Network access and expected domains are not declared as explicitly as the security guidance recommends. <br>
Mitigation: Prefer a release that documents its outbound network behavior and expected domains before broader deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/litiao1224/cctv-news-fetcher-litiao) <br>
- [Example usage](examples/example.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands] <br>
**Output Format:** [JSON from the crawler, summarized by the agent in Markdown or plain text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a YYYYMMDD date argument; uses outbound HTTP requests to CCTV pages and depends on node-html-parser.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
