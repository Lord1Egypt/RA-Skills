## Description: <br>
Fetches URLs through Chrome CDP and site-specific adapters, then converts pages, X/Twitter posts, YouTube transcripts, Hacker News threads, and generic pages into Markdown or JSON. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jimliu](https://clawhub.ai/user/jimliu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content workflows use this skill to save web pages, social posts, video transcripts, and discussion threads as Markdown or JSON, with optional local media capture. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Logged-in or private pages may expose sensitive session content during browser-based capture. <br>
Mitigation: Use a dedicated Chrome profile and avoid private or internal URLs unless the capture behavior has been reviewed. <br>
Risk: Debug mode can write page HTML and network data to disk. <br>
Mitigation: Enable debug mode only when needed, store artifacts in a controlled location, and delete them after review. <br>
Risk: X/Twitter sessions may be saved in a local plaintext cookie sidecar. <br>
Mitigation: Use a dedicated profile for authenticated capture and remove the profile or cookie sidecar when finished. <br>
Risk: Generic conversion may send the target URL to defuddle.md as a fallback. <br>
Mitigation: Do not process private or internal URLs when third-party URL sharing is not acceptable. <br>
Risk: Headless capture can produce incomplete or misleading Markdown without a command failure. <br>
Mitigation: Inspect saved Markdown after each run and retry with interaction mode when content appears incomplete, gated, or boilerplate-heavy. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jimliu/baoyu-url-to-markdown) <br>
- [OpenClaw homepage](https://github.com/JimLiu/baoyu-skills#baoyu-url-to-markdown) <br>
- [Adapters & Media](references/adapters.md) <br>
- [Quality Gate & Recovery](references/quality-gate.md) <br>
- [First-Time Setup](references/config/first-time-setup.md) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, json, files, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or JSON, usually written to stdout or a user-selected file; optional media downloads are written as local files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses Chrome/CDP capture, site-specific adapters, optional media download, and quality-gate checks for low-quality captures.] <br>

## Skill Version(s): <br>
1.117.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
