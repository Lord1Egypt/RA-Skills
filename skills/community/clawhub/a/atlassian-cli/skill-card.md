## Description: <br>
Reference guide for the Atlassian CLI (acli) that helps agents prepare Jira Cloud, Atlassian organization administration, and related automation commands for an already installed and authenticated acli binary. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[peetzweg](https://clawhub.ai/user/peetzweg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, administrators, and support engineers use this skill to look up Atlassian acli syntax, authentication patterns, and safety checks before operating Jira projects, work items, boards, sprints, filters, dashboards, fields, or organization users. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bulk edits, deletes, archives, ownership changes, and organization user-management commands can affect many Jira or Atlassian organization resources. <br>
Mitigation: Confirm exact targets before execution, preview bulk selections with matching searches, and require fresh confirmation for organization admin actions. <br>
Risk: API tokens, admin API keys, and attached files may expose sensitive credentials or data if echoed, logged, or stored insecurely. <br>
Mitigation: Use environment variables or secure file input, prefer interactive OAuth when practical, and avoid displaying or persisting secrets. <br>


## Reference(s): <br>
- [Atlassian acli install guide](https://developer.atlassian.com/cloud/acli/guides/install-acli/) <br>
- [Jira work item commands reference](references/jira-workitem-commands.md) <br>
- [acli non-workitem commands reference](references/other-commands.md) <br>
- [ClawHub skill page](https://clawhub.ai/peetzweg/atlassian-cli) <br>
- [Publisher profile](https://clawhub.ai/user/peetzweg) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces command guidance for an external acli installation; it does not bundle or execute the Atlassian CLI.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
