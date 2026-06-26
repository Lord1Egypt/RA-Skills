# Quality Check Prompt

**Objective**: Act as the final gatekeeper to ensure the generated content meets all safety, quality, and platform-specific guidelines before it is handed over to the user for manual review.

## Input
Read the generated `csdn_markdown_ready.md`, `csdn_summary.md`, and `csdn_titles.md`.

## Checklist / Evaluation Criteria

Evaluate the content strictly against the following criteria:

1. **CSDN Community Fit**:
   - Does it read like a technical tutorial or engineering log? (Yes/No)
   - Is there a clear, logical structure (Background -> Problem -> Architecture -> Implementation -> Conclusion)? (Yes/No)
   - Are there clear Inputs and Outputs defined? (Yes/No)
   - Is there engineering value (code, config, flowcharts)? (Yes/No)

2. **Marketing & Tone Check**:
   - Is the content overly promotional or "salesy"? (Yes/No - Must be No)
   - Are there any exaggerated promises ("guaranteed rankings", "dominate search", "industry first")? (Yes/No - Must be No)
   - Is it misleading the user into thinking AI platforms will 100% cite this article? (Yes/No - Must be No)

3. **Truthfulness & Safety**:
   - Are there fabricated facts, false case studies, or fake metrics? (Yes/No - Must be No)
   - Are there leaked secrets, real API keys, or sensitive PII in the code examples? (Yes/No - Must be No)

4. **Automation & Boundaries**:
   - Does the article or its metadata imply that it will be published automatically without user review? (Yes/No - Must be No)

## Output
Generate `csdn_publish_checklist.md`.
If any of the critical checks fail, explicitly list what needs to be fixed. Provide a checklist for the human user to verify before they click "Publish" in the CSDN interface.

**Required Checklist Template included in output:**
- [ ] 事实是否准确，无虚假案例？
- [ ] 是否存在过度营销词汇？
- [ ] 文章结构是否符合技术社区要求（有背景、流程、示例）？
- [ ] 代码或配置示例是否安全（无敏感 Token）？
- [ ] 是否有夸大关于 AI 引用或 SEO 排名的承诺？
- [ ] 确认本次发文由我（人类）最终检查并点击发布？
