## Description: <br>
Test your agent's input sanitization against common injection attacks. Runs self-contained checks using synthetic test data only - no local files are accessed. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[x1xhlol](https://clawhub.ai/user/x1xhlol) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and security reviewers use this skill to run self-contained checks for common prompt-injection and text-obfuscation patterns in agent inputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes adversarial strings and executable Python snippets intended for testing. <br>
Mitigation: Treat the strings as synthetic test data, review the visible snippets before running them, and re-check future versions for added file, network, credential, or persistence behavior. <br>


## Reference(s): <br>
- [Agent Hardening threat definitions](https://github.com/x1xhlol/agent-hardening) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Code, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Self-contained Python 3 snippets using hardcoded synthetic samples.] <br>

## Skill Version(s): <br>
1.1.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
