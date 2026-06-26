## Description: <br>
AI-powered startup mindset coach that helps founders upgrade their thinking patterns, track mental model progress, and set weekly challenges. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[goforu](https://clawhub.ai/user/goforu) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Startup founders use this skill for Socratic coaching, mental model practice, anti-pattern reflection, weekly challenge setting, and progress reporting. It is intended to improve founder thinking patterns rather than provide direct business, pricing, market-selection, or financial advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read private PhoenixClaw journals, profile data, and conversation context. <br>
Mitigation: Confirm PhoenixClaw integration settings before use, limit access to the intended journal path, and review what local data the skill may read. <br>
Risk: The skill can persist sensitive coaching observations in founder profile and weekly report files. <br>
Mitigation: Review generated or appended markdown files regularly and keep only observations the user is comfortable storing locally. <br>
Risk: Opt-in, review, edit, disable, and deletion controls are not clearly documented in the security evidence. <br>
Mitigation: Before installation, verify how to disable PhoenixClaw integration, cron reports, and stored coaching observations. <br>


## Reference(s): <br>
- [Founder Coach Skill Page](https://clawhub.ai/goforu/founder-coach) <br>
- [User Configuration](references/user-config.md) <br>
- [Onboarding Process](references/onboarding.md) <br>
- [Founder Profile Evolution](references/profile-evolution.md) <br>
- [PhoenixClaw Integration Guide](references/phoenixclaw-integration.md) <br>
- [Weekly Challenge System](references/weekly-challenge.md) <br>
- [Weekly Report Generation Guide](references/weekly-report.md) <br>
- [First Round PMF Levels Framework](references/mental-models/pmf-levels.md) <br>
- [4Ps Framework: Getting Unstuck](references/mental-models/4ps-framework.md) <br>
- [NFX Mental Models for Founders](references/mental-models/nfx-models.md) <br>
- [Excuse Thinking Detection Guide](references/anti-patterns/excuse-thinking.md) <br>
- [Fear-Driven Detection Guide](references/anti-patterns/fear-driven.md) <br>
- [Founder Trap Detection Guide](references/anti-patterns/founder-trap.md) <br>
- [Perfectionism Detection Guide](references/anti-patterns/perfectionism.md) <br>
- [Priority Chaos](references/anti-patterns/priority-chaos.md) <br>
- [Comfort Zone Trap](references/anti-patterns/comfort-zone.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, files, configuration, guidance] <br>
**Output Format:** [Markdown coaching responses, markdown profile and weekly report files, and YAML configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or append local founder profile and weekly report files under the user's PhoenixClaw startup workspace when configured.] <br>

## Skill Version(s): <br>
0.0.1 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
