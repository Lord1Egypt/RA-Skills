## Description: <br>
Caching anti-pattern analyzer -- detects Redis/Memcached misuse, TTL problems, cache invalidation failures, stampedes, architecture issues, and security hygiene gaps in application-level caching. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[suhteevah](https://clawhub.ai/user/suhteevah) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use CacheLint to scan application code for cache invalidation, TTL, stampede, Redis/Memcached misuse, architecture, and cache security hygiene issues before committing or shipping changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may read a CacheLint license key from the OpenClaw config or environment. <br>
Mitigation: Prefer a protected config file or environment variable and avoid passing the license through the --license-key flag. <br>
Risk: Installing git hooks can modify lefthook.yml and make CacheLint run automatically on future commits and pushes. <br>
Mitigation: Run hooks install only when automatic checks are intended, then review lefthook.yml after installation. <br>
Risk: Server security evidence marks the release as suspicious because optional hooks and license-secret handling require review. <br>
Mitigation: Review the security guidance before installation and limit use to repositories where local scanning and hook behavior are acceptable. <br>


## Reference(s): <br>
- [CacheLint ClawHub release](https://clawhub.ai/suhteevah/cachelint) <br>
- [CacheLint homepage](https://cachelint.pages.dev) <br>
- [CacheLint hook documentation](https://cachelint.pages.dev/docs/hooks) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text, JSON, HTML, and Markdown reports with inline shell commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Exit code 0 indicates a passing score and exit code 1 indicates caching quality below the configured threshold.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
