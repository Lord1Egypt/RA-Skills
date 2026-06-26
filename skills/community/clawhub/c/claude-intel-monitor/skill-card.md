## Description: <br>
Detect intelligence degradation in Claude, GPT, and DeepSeek using 30 standardized Chinese benchmark questions across Math, Reasoning, and Code. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[minirr890112-byte](https://clawhub.ai/user/minirr890112-byte) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and model evaluation teams use this skill to benchmark Claude, GPT, and DeepSeek models against fixed Chinese math, reasoning, and code questions, then compare results with baselines and history to detect possible quality regressions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Benchmark runs send prompts to the selected model provider or configured base URL and may consume paid API quota. <br>
Mitigation: Use only intended provider credentials, review the benchmark prompts and provider endpoint before running, and monitor quota or billing during tests. <br>
Risk: Watch mode makes periodic API calls until stopped. <br>
Mitigation: Run watch mode only with an explicit interval and stop the process when continuous monitoring is no longer needed. <br>
Risk: The tool requires sensitive API credentials for Anthropic, OpenAI, or DeepSeek providers. <br>
Mitigation: Store keys in environment variables or managed secret storage, avoid committing credentials, and rotate any key that may have been exposed. <br>


## Reference(s): <br>
- [ClawHub package page](https://clawhub.ai/minirr890112-byte/claude-intel-monitor) <br>
- [Project homepage](https://github.com/minirr890112-byte/claude-intel-monitor) <br>
- [README](README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and benchmark output summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May describe API-key setup, benchmark execution, baseline comparison, history review, and continuous watch mode.] <br>

## Skill Version(s): <br>
1.1.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
