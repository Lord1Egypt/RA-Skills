## Description: <br>
Track whether ChatGPT, Claude, Gemini, and Perplexity recommend a startup or brand across a prompt set. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[x-rayluan](https://clawhub.ai/user/x-rayluan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers, founders, marketing teams, and AI SEO practitioners use this skill to run prompt sets against configured model providers, detect brand mentions and competitors, estimate ranking and sentiment, and generate visibility reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Reports may represent simulated or estimated AI visibility rather than verified direct results from each named service. <br>
Mitigation: Treat scores and rankings as directional analysis, disclose that limitation when sharing reports, and review raw responses and errors before making business decisions. <br>
Risk: Prompt sets and provider calls can expose sensitive brand, competitor, or market strategy details to configured AI providers or routing services. <br>
Mitigation: Use non-confidential prompt sets unless the provider and routing path are trusted, and keep API keys in environment variables rather than checked-in files. <br>
Risk: Missing keys, quota limits, or provider errors can create zero scores or incomplete results that look like poor brand visibility. <br>
Mitigation: Check generated report errors and rerun failed engines before sharing or comparing visibility metrics. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/x-rayluan/ai-search-rank-tracker) <br>
- [README](README.md) <br>
- [Prompt database README](prompt-db/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, CSV, shell commands, configuration] <br>
**Output Format:** [JSON, Markdown, and CSV report files with console status messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports include brand mention status, rank estimates, competitors, sentiment, scores, prompt metadata, raw excerpts, and provider errors when calls fail.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
