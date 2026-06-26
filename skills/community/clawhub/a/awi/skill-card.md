## Description: <br>
AWI (Agentic Web Interface) is a zero-configuration single-binary tool for reading web pages and running DuckDuckGo searches, with automatic fallback from direct access to adaptive and browser-rendered modes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jzOcb](https://clawhub.ai/user/jzOcb) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use AWI to retrieve web page content, run web searches, and batch-read URLs through an installed command-line binary. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The installer downloads and executes a native AWI binary from a GitHub release without checksum or signature verification. <br>
Mitigation: Install only when the publisher and release binary are trusted, and verify the binary through an independent process before use in sensitive environments. <br>
Risk: Web reads, searches, proxies, and rendered-browser requests can expose URLs, queries, or page content outside the local environment. <br>
Mitigation: Avoid using the skill with secrets, internal URLs, confidential searches, or regulated data unless that data flow has been approved. <br>


## Reference(s): <br>
- [ClawHub AWI listing](https://clawhub.ai/jzOcb/awi) <br>
- [AWI project homepage](https://github.com/jzOcb/awi) <br>
- [AWI install script](artifact/scripts/install.sh) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Command-line output in text, Markdown, or JSON, plus Markdown usage guidance with shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports read, search, and batch URL workflows; command options include backend, output format, timeout, proxy, and cache controls.] <br>

## Skill Version(s): <br>
0.1.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
