## Description: <br>
Analyzes how well a specific brand or product is mentioned and represented by LLMs for Generative Engine Optimization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ljseeking](https://clawhub.ai/user/ljseeking) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, marketers, and brand analysts use this skill to test whether a target brand appears in LLM-generated industry recommendations, assess mention sentiment, identify competitors, and receive a concise GEO analysis report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Brand names, category keywords, and generated analysis text are sent to DeepSeek and may be sensitive brand-research data. <br>
Mitigation: Use a dedicated DeepSeek API key, avoid submitting confidential brand research unless approved, and confirm that DeepSeek data handling is acceptable for the deployment context. <br>
Risk: The skill consumes DeepSeek API quota and may incur usage costs. <br>
Mitigation: Review expected API usage before running large batches and monitor the API key's quota or billing controls. <br>
Risk: Unpinned Python dependencies can change behavior across installs. <br>
Mitigation: Pin and review dependency versions before production deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ljseeking/geo-analyzer) <br>
- [Skill homepage](https://github.com/LJseeking/lifesignal) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, JSON, Markdown, Shell commands, Guidance] <br>
**Output Format:** [JSON containing structured GEO results and a natural-language analysis report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires DEEPSEEK_API_KEY and sends brand name, category keyword, and generated analysis text to the DeepSeek API.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
