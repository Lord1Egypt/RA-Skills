## Description: <br>
Adversarial implementation review based on Block's g3 dialectical autocoding research. Use when validating implementation completeness against requirements with fresh objectivity. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[killerapp](https://clawhub.ai/user/killerapp) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineering teams use this skill to review implementations against requirements with an independent, adversarial lens before accepting work as complete. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Review guidance can suggest build, test, or run commands that execute code in the target repository. <br>
Mitigation: For untrusted repositories, treat those commands as normal code execution risk and approve each step deliberately. <br>


## Reference(s): <br>
- [Adversarial Cooperation in Code Synthesis](https://block.xyz/documents/adversarial-cooperation-in-code-synthesis.pdf) <br>
- [g3](https://github.com/dhanji/g3) <br>
- [ClawHub skill page](https://clawhub.ai/killerapp/adversarial-coach) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, text] <br>
**Output Format:** [Markdown review verdict with concise requirement checks and action items] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May emit IMPLEMENTATION_APPROVED only when requirements, compilation, tests, and significant gaps have been checked.] <br>

## Skill Version(s): <br>
0.9.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
