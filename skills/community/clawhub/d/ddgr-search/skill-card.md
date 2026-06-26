## Description: <br>
Perform web searches using ddgr with a configurable result count from the command line. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[javedniazi](https://clawhub.ai/user/javedniazi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to issue command-line web searches through a local ddgr installation and retrieve a chosen number of results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search terms leave the local machine through ddgr's external search provider. <br>
Mitigation: Avoid searching for passwords, tokens, private project names, customer data, or other sensitive information. <br>
Risk: The skill depends on the local ddgr executable. <br>
Mitigation: Install and run it only in environments where the local ddgr binary is trusted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/javedniazi/ddgr-search) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Command-line text output from ddgr, with agent guidance in Markdown] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a trusted local ddgr executable and sends search terms to the external search provider used by ddgr.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
