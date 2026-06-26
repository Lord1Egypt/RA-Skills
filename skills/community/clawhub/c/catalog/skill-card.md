## Description: <br>
Catalog answers short questions about studio services and prices from a fixed local JSON list. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rodbalbino](https://clawhub.ai/user/rodbalbino) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users or studio staff use this skill to answer questions about available studio services and prices using the fixed catalog returned by the bundled script. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks the agent to invoke a local Node.js command when answering catalog questions. <br>
Mitigation: Review the packaged script before installation and run only the bundled artifact; the reviewed script emits a fixed JSON price list and shows no network, persistence, hidden data access, or destructive behavior. <br>
Risk: The catalog data is hardcoded and may become stale or incomplete for real customer-facing use. <br>
Mitigation: Confirm service names and prices with the publisher before relying on the response for commercial commitments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/rodbalbino/catalog) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands] <br>
**Output Format:** [Concise plain text response based on JSON returned by a local Node.js command] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The reviewed script returns service names and prices only.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
