## Description: <br>
Analyzes Taobao, JD, and Pinduoduo product reviews, compares products or stores, and generates Word/PDF reports with sentiment, negative review details, and improvement suggestions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tobewin](https://clawhub.ai/user/tobewin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External ecommerce operators and analysts use this skill to collect and analyze customer reviews from Taobao, JD, and Pinduoduo, compare products or stores, and produce review reports for operational decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a logged-in browser session for ecommerce review pages, which may expose account-visible details to the agent during collection. <br>
Mitigation: Run it only in an intended logged-in session and confirm the exact product or store before collection begins. <br>
Risk: Generated DOCX/PDF reports may contain customer review text and account-visible details. <br>
Mitigation: Handle generated reports as privacy-sensitive files and share them only with appropriate recipients. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/tobewin/ecommerce-review-analyzer) <br>
- [Publisher Profile](https://clawhub.ai/user/tobewin) <br>
- [Taobao Product Review Source Pattern](https://item.taobao.com/item.htm?id=PRODUCT_ID) <br>
- [JD Product Review Source Pattern](https://item.jd.com/PRODUCT_ID.html) <br>
- [Pinduoduo Product Review Source Pattern](https://mobile.yangkeduo.com/goods.html?goods_id=PRODUCT_ID) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Files, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance plus DOCX/PDF report files and browser/Python code snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3, OpenClaw v2026.3.22 or newer, OpenClaw browser automation, and logged-in ecommerce platform sessions.] <br>

## Skill Version(s): <br>
1.0.7 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
