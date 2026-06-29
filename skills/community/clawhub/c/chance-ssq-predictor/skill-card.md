## Description: <br>
Provides entertainment-oriented SSQ lottery data analysis and number-selection assistance using statistical summaries such as missing values, frequency, sum value, AC value, span, odd-even ratio, size ratio, and interval distribution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gechengling](https://clawhub.ai/user/gechengling) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill for entertainment-oriented SSQ lottery analysis, including statistical summaries, historical-pattern discussion, and optional number-combination suggestions. Outputs should be treated as non-predictive guidance because lottery draws are random independent events. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Lottery analysis recommendations may be mistaken for reliable predictions or purchase advice. <br>
Mitigation: Present outputs as entertainment-only, non-predictive analysis and remind users that historical data cannot improve the odds of random lottery draws. <br>
Risk: The documentation overstates that the package contains no executable code, while the artifact includes a runnable local Python script. <br>
Mitigation: Review the local script before execution and run it only intentionally in a local environment. <br>
Risk: The security guidance notes that the blue-ball analysis path appears to have an accuracy bug. <br>
Mitigation: Treat blue-ball analysis as unreliable until manually reviewed or corrected, and avoid relying on it for decisions. <br>


## Reference(s): <br>
- [双色球分析方法论详细参考](references/methodology.md) <br>
- [双色球的数理分析](https://zhuanlan.zhihu.com/p/142332075) <br>
- [彩宝网 - 走势分析](https://www.00038.cn/) <br>
- [中彩网 - 官方数据](https://www.zhcw.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown analysis with optional terminal command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include entertainment-only SSQ number combinations and statistical summaries; recommendations are non-predictive.] <br>

## Skill Version(s): <br>
4.2.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
