## Description: <br>
Use when the user has a method idea or Committed Method Design and reads papers to design tasks, datasets, baselines, metrics, ablations, human evaluation, user studies, or a claim-to-evidence experiment plan. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[snake-fan](https://clawhub.ai/user/snake-fan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers and paper-reading agents use this skill to convert a committed method or concrete research question into a structured experiment plan. It guides claim decomposition, evidence mapping, baseline and metric selection, ablation planning, and review-gated Markdown artifacts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may inspect local research notes or unpublished method artifacts while building an experiment plan. <br>
Mitigation: Confirm the workspace path and source artifact before use, and avoid pointing the workflow at sensitive material that should not be processed. <br>
Risk: Generated experiment designs, baselines, metrics, or ablations may be incomplete or misleading if accepted without review. <br>
Mitigation: Use the built-in decision gates, review generated Markdown before relying on it, and validate proposed evidence routes against the source papers. <br>


## Reference(s): <br>
- [Server-resolved source](https://github.com/snake-fan/Paper-Reading-Skills/tree/main/skills/07-experiment-design) <br>
- [ClawHub listing](https://clawhub.ai/snake-fan/skills/07-experiment-design) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown files and concise decision packets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates or updates experiment-design artifacts under a workspace experiment-designs folder.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
