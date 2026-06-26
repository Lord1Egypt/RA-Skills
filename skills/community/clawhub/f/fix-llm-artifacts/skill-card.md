## Description: <br>
Applies fixes from a prior review-llm-artifacts run, with safe/risky classification. Respects verify-llm-artifacts output when present to skip false positives. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anderskev](https://clawhub.ai/user/anderskev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to apply previously reviewed LLM-artifact fixes while preserving review IDs, stale-review checks, verification overlays, and user approval for risky changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is mostly coherent, but it can automatically run whole-repository autofix tools that may change files beyond the review findings the user approved. <br>
Mitigation: Install only if you are comfortable with the skill modifying repository files beyond the specific review findings during formatting/autofix. Use --dry-run first, review the git diff carefully afterward, and avoid running it on important work without a clean branch or backup. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/anderskev/fix-llm-artifacts) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown status reports, shell commands, and repository file edits] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May modify repository files and run formatter or autofix tools after applying approved findings.] <br>

## Skill Version(s): <br>
1.1.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
