## Description: <br>
Use BYR CLI for auth, search, detail inspection, and safe torrent download planning with JSON envelopes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1MoreBuild](https://clawhub.ai/user/1MoreBuild) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to guide BYR CLI authentication checks, torrent search and browsing, detail inspection, metadata lookup, diagnostics, and dry-run-first download planning. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Browser cookie import can expose sensitive BYR session credentials. <br>
Mitigation: Prefer manually supplied minimal BYR cookies where possible, avoid sharing or logging cookie and token values, verify auth status before live use, and run `byr auth logout --json` when finished. <br>
Risk: The skill delegates work to the external `byr` binary. <br>
Mitigation: Install only if the `byr-pt-cli` binary and its Homebrew or npm source are trusted in the deployment environment. <br>
Risk: Non-dry-run downloads can write torrent files to local paths. <br>
Mitigation: Run a dry run first, inspect `sourceUrl` and `fileName`, and confirm the explicit output path before executing a write. <br>


## Reference(s): <br>
- [BYR CLI Skill on ClawHub](https://clawhub.ai/1MoreBuild/byr-cli) <br>
- [ClawHub homepage from OpenClaw metadata](https://clawhub.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON-first result summaries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses BYR CLI JSON envelopes where available; download workflows should include dry-run review before file writes.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release metadata and publish.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
