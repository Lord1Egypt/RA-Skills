## Description:

搜索淘宝商品并返回价格、销量、店铺、发货地和商品链接，用于按关键词查找商品、比价、排序或排查 API 调用请求。

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiongweixp](https://clawhub.ai/user/xiongweixp)

### License/Terms of Use:

MIT-0

## Use Case:

External users and shopping researchers use this skill to search Taobao by keyword, compare prices and sales signals, and return concise product listings. Developers may also use it to generate or troubleshoot calls to the Bana Taobao search API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses reusable Bana API credentials and saves supplied credentials locally by default.

Mitigation: Review before installing, prefer one-time credential use when appropriate, and avoid sharing long-lived SecureKeys in chat or command history.

Risk: A custom Bana Taobao base URL can send requests and credentials to a different destination.

Mitigation: Only set a custom base URL for a fully trusted service.

Risk: Taobao page changes, login failures, or CAPTCHA challenges can lead to incomplete or failed results.

Mitigation: Report unavailable fields plainly, avoid inferring missing product data, and retry later when the service reports page or CAPTCHA issues.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xiongweixp/skills/bana-taobao-search)
- [Bana Skill Center](https://wxpub.aibana.art)
- [Bana Taobao search API endpoint](https://wxpub.aibana.art/taobao/search)

## Skill Output:

**Output Type(s):** [API Calls, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown summary based on JSON API responses, with optional shell commands for the bundled Python client]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns product title, price, sales text, shop, shipping location, and detail link when available; users should not infer missing fields.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
