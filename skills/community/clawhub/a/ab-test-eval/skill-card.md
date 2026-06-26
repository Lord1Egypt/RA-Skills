## Description: <br>
Runs A/B evaluation workflows for OpenClaw skills, scripts, hooks, and cron jobs across baseline, regression, model-swap, prompt-variant, trigger-accuracy, adversarial, script validation, dry-run, and integration modes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cyrushuang1995-cmyk](https://clawhub.ai/user/cyrushuang1995-cmyk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and evaluators use this skill to design, preview, and run comparative tests for OpenClaw components, then review benchmark artifacts and recommendations before iterating. It is suited to evaluating skills, scripts, hooks, cron payloads, prompt variants, model swaps, and integration behavior. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks for broad testing and command-execution authority, including scripts, hooks, cron payloads, and integration tests. <br>
Mitigation: Use the dry-run preview first, inspect generated eval cases and planned commands, and approve execution only for trusted workspaces. <br>
Risk: Evaluation commands or integration tests could modify data or expose secrets if run against production resources. <br>
Mitigation: Run evaluations in isolated development environments and avoid projects where test commands can touch production data or credentials. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cyrushuang1995-cmyk/ab-test-eval) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, JSON evaluation artifacts, and inline shell-command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local evaluation workspaces, benchmark files, grading JSON, timing JSON, and history entries after user approval.] <br>

## Skill Version(s): <br>
2.1.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
