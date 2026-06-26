## Description: <br>
中文快递追踪助手，可根据快递单号自动识别快递公司并查询实时物流状态。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[freedompixels](https://clawhub.ai/user/freedompixels) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Chinese-speaking external users can add, query, list, and delete courier tracking numbers for common domestic and international carriers. The skill is useful for checking parcel status through Kuaidi100 and keeping a small local tracking list. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Parcel tracking numbers are sent to Kuaidi100 for lookup. <br>
Mitigation: Install only when this data sharing is acceptable for the intended shipments. <br>
Risk: Saved tracking numbers and statuses are retained in a local JSON file. <br>
Mitigation: Use the documented delete or clear commands, or remove the JSON file, when retained shipment history is no longer wanted. <br>


## Reference(s): <br>
- [Kuaidi100](https://www.kuaidi100.com/) <br>
- [ClawHub skill page](https://clawhub.ai/freedompixels/cn-kuaidi-100) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration] <br>
**Output Format:** [Markdown-style text with courier status lines and inline shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores tracked shipment numbers and last known statuses in a local JSON file.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
