## Description: <br>
Async/await anti-pattern analyzer -- detects promise misuse, async resource leaks, event loop blocking, missing cancellation, async error patterns, and coordination issues. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[suhteevah](https://clawhub.ai/user/suhteevah) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use AsyncGuard to scan local codebases for async/await anti-patterns, promise misuse, resource leaks, event loop blocking, missing cancellation handling, and async coordination issues. It can produce local scan results for one-off audits, CI checks, and optional git hook workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: ClawScan reported a suspicious verdict because license validation can execute commands from a crafted license token. <br>
Mitigation: Review before installation, do not configure paid-tier license tokens unless the publisher and token source are trusted, and prefer a fixed version that parses JWT JSON through stdin or files instead of embedding decoded token text in interpreter command strings. <br>


## Reference(s): <br>
- [AsyncGuard homepage](https://asyncguard.pages.dev) <br>
- [AsyncGuard hook documentation](https://asyncguard.pages.dev/docs/hooks) <br>
- [ClawHub AsyncGuard release page](https://clawhub.ai/suhteevah/asyncguard) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Text, JSON, HTML, and Markdown reports with file, line, severity, check ID, description, recommendation, score, and grade details.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs locally against user-selected files or directories; paid tiers require ASYNCGUARD_LICENSE_KEY and optional lefthook configuration.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release metadata; artifact frontmatter reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
