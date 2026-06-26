## Description: <br>
Verify real local environment facts before an agent uses machine-specific commands, runtimes, compilers, services, or startup scripts, then create or refresh environment baseline JSON and related environment policy, AGENTS, or skill documents from those verified facts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zshTolors](https://clawhub.ai/user/zshTolors) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to verify local toolchains, runtimes, environment variables, services, and startup assumptions before relying on machine-specific commands. It helps them create or refresh synchronized JSON baselines and human-readable environment policy, AGENTS, or reusable skill snippets from verified facts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Custom probe files can run local commands while checking tools, services, databases, or startup scripts. <br>
Mitigation: Review probe files as executable code before use and run only probes that are needed for the current environment task. <br>
Risk: Generated JSON and Markdown can persist hostnames, local paths, PATH entries, command output, and environment variable values. <br>
Mitigation: Inspect and redact generated files before sharing, committing, or using them outside the intended local environment. <br>
Risk: Environment guidance can become stale after toolchain, shell profile, package manager, or machine changes. <br>
Mitigation: Refresh the relevant baseline facts with targeted verification and keep the JSON baseline and human-readable documents synchronized. <br>


## Reference(s): <br>
- [Document Contracts](references/document-contracts.md) <br>
- [Probe File](references/probe-file.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [JSON baseline data plus Markdown environment policy, AGENTS snippets, reusable skill snippets, and command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated environment documents should stay synchronized with verified baseline facts and may include local paths, command output, PATH entries, and environment variable values.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
