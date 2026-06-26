## Description: <br>
Tracks courier shipments from tracking numbers or forwarded delivery SMS messages, stores a local tracking list, and produces status reports with map links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wumaoqianq](https://clawhub.ai/user/wumaoqianq) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and end users can use this skill to query express shipment status, extract tracking numbers from delivery SMS messages, manage a local tracking list, and generate delivery reports with map links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Shipment privacy can be exposed because tracking numbers are sent to external courier-query services. <br>
Mitigation: Use the skill only for tracking numbers you are comfortable submitting to those services, and avoid forwarding SMS messages that include addresses, pickup codes, or other sensitive details. <br>
Risk: Shipment history is retained locally under G:\PC先生\express_data\packages.json. <br>
Mitigation: Run it on a trusted machine and periodically remove old or sensitive shipment records. <br>
Risk: The Juhe API key is read from Desktop\999.txt. <br>
Mitigation: Store only a non-sensitive, scoped API key there and rotate it if the file may have been exposed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wumaoqianq/express-hunter) <br>
- [Publisher profile](https://clawhub.ai/user/wumaoqianq) <br>
- [Juhe express query service](http://v.juhe.cn/exp/index) <br>
- [Kuaidi100 query service](https://www.kuaidi100.com/query) <br>
- [Amap route maps](https://ditu.amap.com/dir) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown and text responses with shell command examples and optional JSON from track.py --json] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May execute local Python scripts that query third-party courier services and update a local packages.json tracking store.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
