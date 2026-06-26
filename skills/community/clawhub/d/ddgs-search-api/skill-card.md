## Description: <br>
Use when needing to search the web in AI coding tools or OpenClaw. Uses DuckDuckGo API without API key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bird-frank](https://clawhub.ai/user/bird-frank) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to run DuckDuckGo web or news searches from coding tools and OpenClaw workflows. It supports text or JSON output with configurable result count, region, safe search, time window, backend, and proxy settings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries are sent to DuckDuckGo/ddgs backends and may also pass through a configured proxy. <br>
Mitigation: Avoid searching secrets or proprietary data, and use only trusted proxies when proxy settings are enabled. <br>
Risk: Installer and shell-command examples can execute package installation or external commands. <br>
Mitigation: Review commands before running them and prefer trusted package sources. <br>
Risk: Embedding user-supplied query text directly in shell workflows can create command-injection risk. <br>
Mitigation: Escape or pass query strings as structured arguments when integrating the tool into shell workflows. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/bird-frank/ddgs-search-api) <br>
- [Publisher profile](https://clawhub.ai/user/bird-frank) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration guidance] <br>
**Output Format:** [Plain text or JSON search results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search results include title, URL, and body text; news results may also include date and source.] <br>

## Skill Version(s): <br>
0.2.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
