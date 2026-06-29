## Description: <br>
B2B企业数字化诊断通过3道选择题判定企业专注类型，给出官网架构、短视频策略、小程序定位等数字化落地建议，并生成PDF诊断报告。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xtoyun](https://clawhub.ai/user/xtoyun) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External B2B marketing, manufacturing, engineering service, and industrial software teams use this skill to diagnose whether their company is capability-led, industry-led, problem-led, or mixed, then turn the result into website, short-video, mini-program, and report recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: PDF export may install Playwright and download Chromium locally. <br>
Mitigation: Confirm that local Playwright and Chromium installation is acceptable before enabling PDF export, and use browser-print or Markdown fallback when installation is not allowed. <br>
Risk: Generated reports can include customer or company diagnosis details. <br>
Mitigation: Generate reports in a dedicated folder, review filenames and content before sharing, and add privacy and access-control language before adapting mini-program, upload, or customer-report recommendations for production. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/xtoyun/b2b-digital-diagnosis) <br>
- [Publisher Profile](https://clawhub.ai/user/xtoyun) <br>
- [Case Index](examples/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, files] <br>
**Output Format:** [Conversational diagnosis with Markdown tables and optional HTML/PDF report files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May invoke Playwright and Chromium locally to render a generated HTML diagnosis report to PDF.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
