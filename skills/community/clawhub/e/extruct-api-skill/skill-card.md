## Description: <br>
Run explicit Extruct API tasks through the bundled Extruct CLI. Covers Deep Search, semantic search, lookalike search, company and people tables, column operations, enrichment, and contact finding. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zkid18](https://clawhub.ai/user/zkid18) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and business users use this skill to operate Extruct company discovery, Deep Search, AI table, enrichment, and contact-finding workflows through CLI-guided commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent to change or delete remote Extruct data. <br>
Mitigation: Inspect the target table or task before mutation, require explicit confirmation before deletes or broad table runs, and summarize affected IDs and counts. <br>
Risk: Contact-finding workflows can collect personal contact details. <br>
Mitigation: Use contact enrichment only for authorized business purposes, request the minimum fields needed, and apply appropriate retention controls. <br>
Risk: The skill depends on resolving and running a bundled CLI. <br>
Mitigation: Resolve the CLI from the skill directory, verify the path before first use, and run authentication or health checks before account operations. <br>


## Reference(s): <br>
- [Extruct API Reference](https://www.extruct.ai/docs/api-reference/introduction) <br>
- [Column Guide](references/column-guide.md) <br>
- [Finding Companies](references/finding-companies.md) <br>
- [Finding People At Companies](references/finding-people-at-companies.md) <br>
- [Researching Companies](references/researching-companies.md) <br>
- [Researching People](references/researching-people.md) <br>
- [ClawHub Skill Listing](https://clawhub.ai/zkid18/extruct-api-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce CLI commands that read, create, update, run, poll, or delete remote Extruct objects when the user authorizes those operations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
