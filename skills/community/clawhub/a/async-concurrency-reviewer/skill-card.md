## Description: <br>
Reviews async and concurrency code for deadlocks, race conditions, missing cancellation, blocking calls in async contexts, and misuse of concurrency primitives across multiple languages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Lnguyen1996](https://clawhub.ai/user/Lnguyen1996) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to review pasted async or concurrent code for production bugs such as deadlocks, race conditions, unhandled async failures, and cancellation gaps. It returns severity-ranked findings, corrected code, and concise guidance for safer async and concurrency patterns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may paste confidential or proprietary code into the reviewing agent. <br>
Mitigation: Use only in a trusted host environment and avoid sharing sensitive code unless the agent session and data handling settings are acceptable. <br>
Risk: Optional tracking of common findings could persist review patterns across sessions when agent memory is enabled. <br>
Mitigation: Check and configure the host agent's memory settings before using the skill for sensitive projects. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/Lnguyen1996/async-concurrency-reviewer) <br>
- [Artifact SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Guidance] <br>
**Output Format:** [Markdown report with severity sections and corrected code snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes critical, warning, suggestion, correct-pattern, and summary sections; may surface common issue patterns after repeated reviews if memory is enabled.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
