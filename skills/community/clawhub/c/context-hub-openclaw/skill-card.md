## Description: <br>
Use Context Hub (chub) to fetch versioned API docs and skills before coding, then persist learnings with annotations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[victorlin-houzz](https://clawhub.ai/user/victorlin-houzz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and coding agents use this skill before implementing third-party API or SDK integrations where current documentation, version behavior, webhooks, streaming, auth, or schema details affect correctness. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill relies on the @aisuite/chub CLI and fetched documentation, which can affect implementation choices for high-impact integrations. <br>
Mitigation: Install only if the CLI is trusted, review fetched references before high-impact changes, and use version targeting when SDK major versions differ. <br>
Risk: Annotations and saved .context files could accidentally capture secrets, tokens, private customer data, or overly broad internal notes. <br>
Mitigation: Keep annotations concise and non-sensitive, and review saved context files before committing or sharing them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/victorlin-houzz/context-hub-openclaw) <br>
- [Context Hub repository](https://github.com/andrewyng/context-hub) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the chub CLI; may save fetched references under .context and create concise annotations without secrets.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
