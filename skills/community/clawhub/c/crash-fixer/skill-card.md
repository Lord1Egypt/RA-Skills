## Description: <br>
Crash Fixer monitors crash reports, deduplicates known issues, analyzes crashes with AI, generates fixes, and creates pull requests. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Ryce](https://clawhub.ai/user/Ryce) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineering teams use this skill to process recent crash reports, analyze likely root causes, generate code fixes, and open pull requests for human review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Crash data and source snippets may be sent to an external AI service. <br>
Mitigation: Run only where this data sharing is acceptable, verify the configured crash reporter URL, and avoid sending sensitive repositories or crash records without approval. <br>
Risk: The skill can create GitHub branches, commits, and pull requests that change code. <br>
Mitigation: Use --dry-run first, provide a least-privilege GitHub token limited to the target repository, and require human review before merging generated pull requests. <br>


## Reference(s): <br>
- [Crash Fixer ClawHub Page](https://clawhub.ai/Ryce/crash-fixer) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, code, shell commands, configuration, guidance] <br>
**Output Format:** [Console output, JSON-formatted AI analysis, GitHub branches, commits, and pull requests] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports --hours, --limit, and --dry-run command flags; requires GH_TOKEN, CRASH_REPORTER_API_KEY, CRASH_REPORTER_URL, and TARGET_REPO environment variables.] <br>

## Skill Version(s): <br>
3.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
