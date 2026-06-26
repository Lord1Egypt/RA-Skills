## Description: <br>
Lightpanda helps agents install and use the Lightpanda lightweight headless browser for browser automation, page extraction, CDP integrations, and MCP-based browsing workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cn-big-cabbage](https://clawhub.ai/user/cn-big-cabbage) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to set up Lightpanda, connect Puppeteer or Playwright through CDP, configure an MCP server, and extract web pages as HTML or Markdown for automation workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill directs agents to download and run unpinned nightly browser binaries. <br>
Mitigation: Use a pinned Lightpanda release, verify checksums or signatures where available, and require user approval before installation or execution. <br>
Risk: Browser automation can access websites, local services, proxies, and credentials if configured carelessly. <br>
Mitigation: Keep the CDP server bound to localhost, avoid hardcoded tokens or proxy passwords, and crawl only sites the user is authorized to access. <br>
Risk: Lightpanda is described as beta and may be unstable or incomplete for some Web APIs and high-concurrency workloads. <br>
Mitigation: Start with limited concurrency, validate output quality against target sites, and fall back to a more compatible browser when required APIs are missing. <br>
Risk: The skill notes default telemetry behavior. <br>
Mitigation: Disable telemetry when required by policy or user preference before starting the browser service. <br>


## Reference(s): <br>
- [Lightpanda homepage](https://lightpanda.io) <br>
- [Lightpanda documentation](https://lightpanda.io/docs) <br>
- [Lightpanda MCP server documentation](https://lightpanda.io/docs/open-source/guides/mcp-server) <br>
- [Docker Hub lightpanda/browser](https://hub.docker.com/r/lightpanda/browser) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands, JSON configuration snippets, and JavaScript or TypeScript examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces setup and usage guidance for a local browser binary, Docker container, CDP endpoint, or MCP server.] <br>

## Skill Version(s): <br>
0.1.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
