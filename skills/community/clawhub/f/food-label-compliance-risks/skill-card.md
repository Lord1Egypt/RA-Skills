## Description: <br>
食品标签合规审查与风险查询；当用户上传标签图片/PDF进行合规审查或查询标签违规案例、处罚依据时使用 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cloudyxuq](https://clawhub.ai/user/cloudyxuq) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and compliance reviewers use this skill to review uploaded food label images or PDFs, check text and visual labeling requirements, and generate compliance findings with suggested corrections. It also supports risk and enforcement-case lookup for food labeling questions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Uploaded label images or PDFs may contain confidential packaging drafts, supplier data, or unpublished product formulation details. <br>
Mitigation: Use only approved OCR or multimodal providers for sensitive labels, prefer a local provider path when required, and remove temporary files from ./tmp/ after review. <br>
Risk: Compliance findings may be incomplete or inaccurate when OCR, visual analysis, or source standards are misread. <br>
Mitigation: Treat generated findings as review support and have qualified regulatory or legal staff confirm issues before changing labels or making enforcement decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cloudyxuq/food-label-compliance-risks) <br>
- [Food label review checklist](references/review-checklist.md) <br>
- [HTML review report template](references/html-template.md) <br>
- [Basic information risks](references/risk-01-basic-info.md) <br>
- [Ingredients and additives risks](references/risk-02-ingredients.md) <br>
- [Nutrition facts risks](references/risk-03-nutrition.md) <br>
- [Labeling format risks](references/risk-04-labeling-format.md) <br>
- [Special foods risks](references/risk-05-special-foods.md) <br>
- [Special claims risks](references/risk-06-special-claims.md) <br>
- [Production information risks](references/risk-07-production-info.md) <br>
- [Other food labeling risks](references/risk-08-other.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, files, guidance] <br>
**Output Format:** [Markdown tables by default, with optional HTML reports and structured JSON review data for report rendering.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce compliance findings, error locations, correction suggestions, penalty references, and downloadable HTML report files.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
