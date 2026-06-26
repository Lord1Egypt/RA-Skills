## Description: <br>
한국 자동차세, 자동차보험, 중고차 시세, 사고 처리, 유지비, 교통위반 질문을 인텐트별로 라우팅하고 Flash 또는 Deep-Dive 형식의 안내를 생성합니다. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sw326](https://clawhub.ai/user/sw326) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to answer Korean car tax, auto insurance, used-car pricing, accident handling, maintenance-cost, and traffic-fine questions with concise, source-aware guidance. It is intended for informational guidance, not legal, insurance underwriting, or claims-settlement advice. <br>

### Deployment Geography for Use: <br>
South Korea <br>

## Known Risks and Mitigations: <br>
Risk: The skill provides Korean car tax, insurance, accident, and traffic-fine information that may be outdated or differ from a user's official bill, policy, or case facts. <br>
Mitigation: Verify important amounts and obligations against official legal, tax, insurer, or government sources before acting. <br>
Risk: Using search or law connectors may expose unnecessary personal information if users include plate numbers, policy numbers, claim IDs, phone numbers, or names. <br>
Mitigation: Avoid entering unnecessary personal identifiers and grant only the search or law connectors required for the current task. <br>
Risk: The skill references a separate law-search helper for deeper legal lookup. <br>
Mitigation: Verify that helper before allowing it to run and treat legal outputs as informational rather than legal advice. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/sw326/car-insurance) <br>
- [Intent router](references/intent_router.md) <br>
- [Output templates](references/output_templates.md) <br>
- [Source tiers](references/source_tiers.md) <br>
- [Korean Local Tax Act reference](https://www.law.go.kr/법령/지방세법) <br>
- [Insurance Damoa comparison platform](https://www.e-insmarket.or.kr) <br>
- [Encar used-car market reference](https://www.encar.com) <br>
- [KB ChaChaCha used-car market reference](https://www.kbchachacha.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown with tables, checklists, brief summaries, and disclaimers] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Flash responses are capped at roughly 20-40 lines; deeper guidance is used when requested or for claim, maintenance, used-car, and insurance-comparison workflows.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
