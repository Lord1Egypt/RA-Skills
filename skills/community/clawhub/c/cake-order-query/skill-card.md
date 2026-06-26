## Description: <br>
通过订单号调用蛋糕订单查询 API，返回对应的蛋糕商品名称或接口错误消息。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[echojiandong](https://clawhub.ai/user/echojiandong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and service agents use this skill to look up cake order details when a user provides a valid order number or asks for cake order lookup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Order numbers are sent to the disclosed cake order API. <br>
Mitigation: Use the skill only with the intended cake order system and provide only the specific order number needed for the lookup. <br>
Risk: Ambiguous order requests could cause the agent to query the wrong order. <br>
Mitigation: Ask for clarification before sending any API request when the user has not provided a clear numeric order number. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/echojiandong/cake-order-query) <br>
- [Cake order lookup API](https://trade.dangaoss.cn/cake_api/ck_orders) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Guidance] <br>
**Output Format:** [Plain text response with the matched cake product name or the API error message.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a specific numeric order number before the agent sends a lookup request.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
