## Description: <br>
快递追踪助手。输入快递单号查询物流状态，自动识别快递公司。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[freedompixels](https://clawhub.ai/user/freedompixels) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to query Chinese courier tracking status, auto-detect common courier companies, and manage a local list of tracked shipments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Package tracking numbers are sent to kuaidi100.com for lookup. <br>
Mitigation: Use the skill only for tracking numbers you are comfortable submitting to that public tracking service. <br>
Risk: Saved tracking entries are stored in a plain local JSON file. <br>
Mitigation: Use one-off query commands when you do not want a shipment added to local tracking history, and protect or remove the local data file according to your privacy needs. <br>
Risk: Clear and delete commands modify the local tracking history. <br>
Mitigation: Review the requested operation before running destructive commands. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/freedompixels/cn-kuaidi-tracker) <br>
- [Kuaidi100 public tracking service](https://www.kuaidi100.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration] <br>
**Output Format:** [Plain text responses from a Python command-line helper] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can create, update, list, delete, and clear entries in a local JSON tracking file.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
