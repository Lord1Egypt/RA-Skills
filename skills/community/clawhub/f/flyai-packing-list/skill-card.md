## Description: <br>
场景化智能行李清单生成器。根据目的地、出行日期、出行目的和同行人，结合 FlyAI 实时搜索目的地信息，生成个性化分类行李清单。当用户提到"行李清单"、"带什么"、"打包"、"收拾行李"、"出行准备"时使用。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hello-ahang](https://clawhub.ai/user/hello-ahang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External travelers use this skill to collect trip details and generate a destination-aware packing checklist. It can incorporate FlyAI travel search results and saved travel preferences when those tools or files are available. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks the agent to install or upgrade a global FlyAI npm package. <br>
Mitigation: Install the CLI only after reviewing and trusting the package source, and avoid granting elevated privileges such as sudo. <br>
Risk: The skill text directs FlyAI commands to bypass TLS certificate validation. <br>
Mitigation: Keep certificate validation enabled and do not run commands that set NODE_TLS_REJECT_UNAUTHORIZED=0. <br>
Risk: The skill can save travel, budget, family, and preference details in memory or ~/.flyai/user-profile.md. <br>
Mitigation: Review, edit, or delete saved profile data if those details should not be reused later. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hello-ahang/flyai-packing-list) <br>
- [FlyAI tool reference](reference/tools.md) <br>
- [POI / Attraction Search](reference/search-poi.md) <br>
- [Keyword Search](reference/keyword-search.md) <br>
- [AI Search](reference/ai-search.md) <br>
- [Flight Search](reference/search-flight.md) <br>
- [Hotel Search](reference/search-hotel.md) <br>
- [Marriott Hotel Search](reference/search-marriott-hotel.md) <br>
- [Marriott Package Search](reference/search-marriott-package.md) <br>
- [Train Search](reference/search-train.md) <br>
- [User profile storage](reference/user-profile-storage.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown checklist with inline shell commands and travel guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Categorizes packing items by priority and may include destination-specific reminders.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
