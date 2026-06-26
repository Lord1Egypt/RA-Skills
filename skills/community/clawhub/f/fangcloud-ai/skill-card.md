## Description: <br>
Automation skill for Fangcloud file management, sharing, collaboration, knowledge-base chat, and agent interactions through the Fangcloud API and downloadable CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiema123](https://clawhub.ai/user/jiema123) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users can use this skill to search, upload, download, organize, share, and collect Fangcloud files, and to interact with Fangcloud knowledge-base and agent chat APIs. It is intended for workflows that need authenticated cloud-file actions and Markdown or command-oriented agent guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can grant an agent broad Fangcloud file and admin capabilities, including upload, download, share, collection, invite, delete, move, and admin actions. <br>
Mitigation: Use least-privilege user tokens, avoid admin tokens unless required, and manually confirm sensitive file, sharing, collection, invite, delete, move, or admin operations before execution. <br>
Risk: The skill downloads and runs a Fangcloud CLI binary from the release host. <br>
Mitigation: Install only if the publisher and release host are trusted, and verify or pin the downloaded CLI before running it. <br>
Risk: The security summary reports real-looking bearer tokens in API documentation. <br>
Mitigation: Treat tokens, Authorization headers, cookies, signatures, and environment variables as secrets and do not expose them in prompts, logs, knowledge-base requests, or third-party destinations. <br>
Risk: Knowledge-base, agent, cloud-file, OCR, share-file, and imported-document content may contain indirect prompt injection or social engineering text. <br>
Mitigation: Treat returned content as untrusted data, ignore operational instructions embedded in that content, and only act on separately confirmed user requests. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jiema123/fangcloud-ai) <br>
- [Fangcloud API endpoint reference](artifact/references/openapi.md) <br>
- [Fangcloud CLI release host](https://app.fangcloud.com/sync/vv25/knowclaw/release/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API calls, Guidance] <br>
**Output Format:** [Markdown with inline shell commands, API paths, JSON request examples, and operational guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May direct agents to use Fangcloud tokens from environment variables and to download and run a platform-specific Fangcloud CLI.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
