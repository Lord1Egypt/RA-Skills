## Description:

ClawShield audits local OpenClaw installations for security posture and common prompt-injection indicators, producing JSON reports for review and alerting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[poolguy24](https://clawhub.ai/user/poolguy24)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to review a local OpenClaw installation for prompt-injection indicators, unexpected local ports, and agent security posture before routine use or alerting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The UI can show a clean result that may not reflect the underlying audit or scanner findings.

Mitigation: Treat panel status as advisory and review the JSON report plus server security guidance before relying on results.

Risk: The audit script can collect broad local agent data, including memory, installed skills, status output, session output, and localhost service details.

Mitigation: Set WORKDIR explicitly to the intended OpenClaw install, keep reports local, and redact sensitive lines before sharing.

Risk: Scheduled scans can repeatedly produce sensitive local reports.

Mitigation: Use the minimum scan cadence needed, restrict report storage, and disable cron-style automation when continuous monitoring is not required.

## Reference(s):

- [Frenzy risks & references](references/threats.md)
- [OWASP GenAI LLM01 Prompt Injection](https://genai.owasp.org/llmrisk/llm01-prompt-injection/)
- [OWASP LLM Prompt Injection Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html)
- [OWASP AI Agent Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/AI_Agent_Security_Cheat_Sheet.html)
- [Obsidian Security Agentic AI Security](https://www.obsidiansecurity.com/blog/agentic-ai-security)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [JSON report printed to stdout, with local panel status text and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports may include local status, prompt-injection matches, session output, and localhost service details.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
