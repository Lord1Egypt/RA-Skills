## Description:

Lightpanda guides agents through installing and using the Lightpanda headless browser for CDP, Puppeteer, Playwright, MCP, and page content extraction workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cn-big-cabbage](https://clawhub.ai/user/cn-big-cabbage)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation engineers use this skill to set up Lightpanda, connect Puppeteer or Playwright scripts, configure MCP access, and extract webpage content as HTML or Markdown for agent workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks agents or users to download and execute mutable Lightpanda nightly binaries or containers.

Mitigation: Review the exact Lightpanda release before installation, prefer pinned versions or immutable Docker digests, and verify checksums or signatures before granting execute permissions or running containers.

Risk: Browser automation through CDP or MCP can expose authenticated sessions, sensitive pages, or local services to an agent.

Mitigation: Use an isolated browser profile or container, bind services to localhost where possible, and avoid browsing authenticated or sensitive sites unless the agent is explicitly intended to access that data.

Risk: Persistent MCP or browser-server integration can keep automation access available beyond a single task.

Mitigation: Avoid automatic agent execution of install and configuration commands, review MCP configuration changes, and stop or remove unused browser services after the workflow completes.

## Reference(s):

- [Lightpanda homepage](https://lightpanda.io)
- [Lightpanda documentation](https://lightpanda.io/docs)
- [Lightpanda MCP server documentation](https://lightpanda.io/docs/open-source/guides/mcp-server)
- [Lightpanda Docker Hub repository](https://hub.docker.com/r/lightpanda/browser)
- [ClawHub skill page](https://clawhub.ai/cn-big-cabbage/skills/cn-lightpanda)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with bash, JavaScript, TypeScript, JSON, and YAML examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes installation, CDP server, Puppeteer, Playwright, MCP, Docker, proxy, telemetry, and troubleshooting guidance.]

## Skill Version(s):

0.1.1 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
