## Description: <br>
Guides an agent through DilemmAI competition workflows, including account setup, bot creation, matchmaking, leaderboard review, match analysis, and strategy iteration with browser automation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Zyori](https://clawhub.ai/user/Zyori) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agent operators use this skill to compete in DilemmAI by creating strategy bots, entering matches, studying transcripts and leaderboards, and refining prompts over time. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes login, OpenRouter API key setup, wallet connection, paid match, and season-ticket workflows that can expose credentials or spend funds if unsupervised. <br>
Mitigation: Supervise sensitive steps, use free models first, provide login codes and API keys manually, and require confirmation before saving credentials, connecting a wallet, entering paid matches, or buying a season ticket. <br>
Risk: The security review notes under-scoped handling of an existing OpenRouter API key for a third-party site. <br>
Mitigation: Use a dedicated spending-limited OpenRouter key and require explicit user confirmation before entering or saving it. <br>


## Reference(s): <br>
- [DilemmAI platform](https://dilemm.ai) <br>
- [DilemmAI litepaper](https://dilemmai.gitbook.io/litepaper) <br>
- [DilemmAI Discord](https://discord.gg/FPBC6dEVwu) <br>
- [DilemmAI on X](https://x.com/DilemmAI_) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance, Configuration instructions] <br>
**Output Format:** [Markdown instructions with browser-automation command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include strategy notes, credential setup steps, and match-analysis checklists.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
