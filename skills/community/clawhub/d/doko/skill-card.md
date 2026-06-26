## Description: <br>
Reads, searches, and extracts rendered web page content through a real Chrome browser for pages that need JavaScript, dynamic rendering, or an authenticated browser session. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dokobot](https://clawhub.ai/user/dokobot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and agents use this skill to read, search, summarize, and extract content from web pages that headless fetch tools cannot fully render. It is especially relevant for SPAs, JavaScript-rendered sites, and pages that require a user-controlled Chrome session. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use a real logged-in Chrome session to read private page content through external Dokobot components. <br>
Mitigation: Use it only on URLs the user intentionally approves, avoid logged-in or private sites unless explicitly approved, and prefer local mode for sensitive pages. <br>
Risk: Remote mode depends on DOKO_API_KEY and remote browser control. <br>
Mitigation: Install only if the Dokobot CLI and extension are trusted, enable remote control only when needed, and close Dokobot sessions when finished. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dokobot/doko) <br>
- [Dokobot homepage](https://dokobot.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and CLI text output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the dokobot CLI, Chrome with the Dokobot extension, and optional DOKO_API_KEY for remote mode.] <br>

## Skill Version(s): <br>
2.3.4 (source: server evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
