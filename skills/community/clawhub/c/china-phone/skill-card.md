## Description: <br>
China Phone looks up the registered province, city, and carrier for Chinese mobile numbers using public lookup endpoints with offline prefix rules as a fallback. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ToBeWin](https://clawhub.ai/user/ToBeWin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to validate Chinese mobile number format, identify registered province or city, and determine the carrier while masking the number in user-facing output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Online lookups send queried phone numbers to public 360 or Taobao endpoints. <br>
Mitigation: For sensitive numbers, ask before online lookup or use the offline prefix fallback. <br>
Risk: Phone number carrier or location results may be inaccurate for number portability, virtual operators, or registered-location lookups. <br>
Mitigation: Present results as number-segment attribution and note uncertainty when using fallback or virtual-operator rules. <br>


## Reference(s): <br>
- [China Phone ClawHub listing](https://clawhub.ai/ToBeWin/china-phone) <br>
- [360 phone area lookup endpoint](https://cx.shouji.360.cn/phonearea.php?number={phone_number}) <br>
- [Taobao mobile segment lookup endpoint](https://tcc.taobao.com/cc/json/mobile_tel_segment.htm?tel={phone_number}) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, API Calls, Guidance] <br>
**Output Format:** [Markdown or text response with masked phone number, location, carrier, and optional inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should decode escaped Unicode into readable Chinese and mask the middle four digits of phone numbers.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
