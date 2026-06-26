## Description: <br>
基于 ClawTip 的 A2A 文章服务 skill，提供热榜获取、公众号发布和文章自动化服务，并在执行前要求支付验证。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lucianaib0318](https://clawhub.ai/user/lucianaib0318) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
中文用户或代理在需要付费获取热榜、发布公众号文章或自动化生成文章时使用该 skill。它适合愿意通过 ClawTip 支付流程购买文章相关服务的用户，但应先确认发布内容、账号权限和支付风险。 <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles payment credentials and paid article requests through provider-controlled services. <br>
Mitigation: Install only if the provider is trusted, and avoid real paid use until credential handling, data retention, and verifiable HTTPS are documented. <br>
Risk: Publishing-related actions may affect external accounts or public content. <br>
Mitigation: Require explicit user review and confirmation before any publishing action. <br>
Risk: The ClawHub security scan reports under-scoped and misleading security controls, including a success-status bug. <br>
Mitigation: Treat service status as untrusted until the provider fixes the bug and documents reliable status handling. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/lucianaib0318/a2a-article-services) <br>
- [ClawTip A2A micropayment protocol](https://clawtip.jd.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, API calls, Guidance] <br>
**Output Format:** [Chinese text or Markdown responses with service status and payment-flow details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May initiate outbound network requests and payment-related workflow before service delivery.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
