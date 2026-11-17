## Description:

Looks up the registered province, city, and carrier for Chinese mobile phone numbers using public lookup endpoints with offline prefix fallback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tobewin](https://clawhub.ai/user/tobewin)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to validate Chinese mobile phone number format and return masked province, city, and carrier lookup results. It supports single or batch lookup workflows and can fall back to offline prefix rules when public lookup services are unavailable.

### Deployment Geography for Use:

Global; lookup scope is Chinese mobile phone numbers.

## Known Risks and Mitigations:

Risk: Queried phone numbers may be sent to public 360 and Taobao lookup services.

Mitigation: Use the skill only for numbers the user has permission to check, and prefer the offline prefix fallback when an external lookup is not appropriate.

Risk: Phone-number attribution may reflect the registered number segment rather than the user's current location or actual carrier.

Mitigation: Present lookup results as registered segment information and note that number portability or roaming can make carrier and location results inaccurate.

Risk: Raw endpoint responses can contain escaped Unicode or unmasked phone numbers.

Mitigation: Parse responses before display, output natural Chinese text, and mask the middle four digits in user-facing results.

## Reference(s):

- [China Phone ClawHub release](https://clawhub.ai/tobewin/skills/china-phone)
- [360 phone area lookup endpoint](https://cx.shouji.360.cn/phonearea.php?number={mobile_number})
- [Taobao mobile segment lookup endpoint](https://tcc.taobao.com/cc/json/mobile_tel_segment.htm?tel={mobile_number})

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown or plain text lookup summaries with masked phone numbers and optional shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call public 360 and Taobao lookup services; offline prefix fallback returns less precise carrier or location data.]

## Skill Version(s):

1.0.1 (source: frontmatter, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
