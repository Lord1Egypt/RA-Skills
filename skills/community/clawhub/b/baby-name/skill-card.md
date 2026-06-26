## Description: <br>
宝宝取名专家，根据宝宝的生辰八字、父母姓氏等信息，生成寓意美好的名字，并通过配置的付费流程处理订单。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liulian822](https://clawhub.ai/user/liulian822) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to request Chinese baby name suggestions after creating and paying for a local order. The skill creates order metadata, invokes a payment flow, verifies a stored payment credential, and returns a short list of recommended names. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release evidence flags review concerns around the payment flow, local order storage, and payment/order data handling. <br>
Mitigation: Review the configured payee, amount, and local order storage before installation, and require explicit user confirmation before creating an order or invoking payment. <br>
Risk: The release evidence notes that the skill asks the agent to reveal internal reasoning. <br>
Mitigation: Do not reveal hidden reasoning or internal chain-of-thought; provide concise user-facing summaries instead. <br>
Risk: The release evidence notes that the implemented name generation may not provide true birth-date or surname-based personalization. <br>
Mitigation: Describe generated names as simple suggestions and avoid representing them as verified birth-date, surname, or fortune-based analysis. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/liulian822/baby-name) <br>
- [Publisher profile](https://clawhub.ai/user/liulian822) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and text status fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns order identifiers, payment status, error information, and generated Chinese name recommendations.] <br>

## Skill Version(s): <br>
1.2.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
