## Description: <br>
12306 查询与订票辅助技能，支持余票查询、经停站查询、中转换乘、候补查询与提交/取消、登录状态检查、密码登录与二维码登录、下单与支付链接获取；当用户提到火车票、高铁票、经停站、中转、候补或 12306 查票时触发。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[myxtype](https://clawhub.ai/user/myxtype) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to query China Railway 12306 train availability, routes, transfer options, waitlist state, passenger records, and order status, and to assist with booking, cancellation, and payment-link workflows. <br>

### Deployment Geography for Use: <br>
Global, for China Railway 12306 workflows <br>

## Known Risks and Mitigations: <br>
Risk: The skill can perform real booking, cancellation, and payment-link workflows against a live 12306 account. <br>
Mitigation: Use query-only commands where possible, run dry-run checks before booking, and require explicit user confirmation before booking, canceling, or paying. <br>
Risk: The skill can access passenger records, orders, and account login state. <br>
Mitigation: Install only for accounts the user is authorized to operate, keep outputs private, and avoid sharing passenger or order details unnecessarily. <br>
Risk: The skill stores cookies, cache data, QR-login state, and payment QR files locally. <br>
Mitigation: Protect or delete cache, cookie, QR-login, and payment QR files after use. <br>


## Reference(s): <br>
- [12306 official service](https://kyfw.12306.cn) <br>
- [ClawHub release page](https://clawhub.ai/myxtype/12306-train-assistant) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [Plain text or JSON, often summarized in Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include local file paths for login or payment QR images when those commands are used] <br>

## Skill Version(s): <br>
0.1.7 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
