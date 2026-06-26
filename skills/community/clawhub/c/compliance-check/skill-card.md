## Description: <br>
Checks draft post content against bundled Chinese and English sensitive-word, advertising-law, and platform-rule wordlists before publishing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kong-zi-chg](https://clawhub.ai/user/kong-zi-chg) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and content operators use this skill before publishing drafts to identify sensitive-word and platform-rule matches, then revise content using the generated report and compliance tips. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Draft text can be sent to DeepSeek when DEEPSEEK_API_KEY is configured, which may expose unpublished content to a third-party API. <br>
Mitigation: Review the privacy tradeoff before enabling AI suggestions; keep drafts local by leaving DEEPSEEK_API_KEY unset and removing it from generic environment files before use. <br>
Risk: The included API server binds to 0.0.0.0 and does not provide authentication. <br>
Mitigation: Do not run the API server on shared or public networks unless it is restricted to localhost and protected with authentication. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kong-zi-chg/compliance-check) <br>
- [LDNOOBW English wordlist source](https://raw.githubusercontent.com/LDNOOBW/List-of-Dirty-Naughty-Obscene-and-Otherwise-Bad-Words/master/en) <br>
- [LDNOOBW Chinese wordlist source](https://raw.githubusercontent.com/LDNOOBW/List-of-Dirty-Naughty-Obscene-and-Otherwise-Bad-Words/master/zh) <br>
- [Sensitive-lexicon advertising wordlist source](https://raw.githubusercontent.com/konsheng/Sensitive-lexicon/main/Vocabulary/广告类型.txt) <br>
- [Sensitive-lexicon supplemental wordlist source](https://raw.githubusercontent.com/konsheng/Sensitive-lexicon/main/Vocabulary/补充词库.txt) <br>
- [Sensitive-lexicon adult-content wordlist source](https://raw.githubusercontent.com/konsheng/Sensitive-lexicon/main/Vocabulary/色情类型.txt) <br>
- [Sensitive-lexicon political-sensitive wordlist source](https://raw.githubusercontent.com/konsheng/Sensitive-lexicon/main/Vocabulary/反动词库.txt) <br>
- [Sensitive-lexicon violence/terrorism wordlist source](https://raw.githubusercontent.com/konsheng/Sensitive-lexicon/main/Vocabulary/暴恐词库.txt) <br>
- [Sensitive-lexicon miscellaneous wordlist source](https://raw.githubusercontent.com/konsheng/Sensitive-lexicon/main/Vocabulary/其他词库.txt) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Markdown, Guidance] <br>
**Output Format:** [JSON object by default, or a Markdown report when report format is requested.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include pass/fail status, short and Chinese summaries, hits grouped by source, compliance tips, warnings, truncation status, and optional AI suggestions.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
