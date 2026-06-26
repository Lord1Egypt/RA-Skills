## Description: <br>
按拼音排序中文姓名。当用户需要给中国人名单按拼音排序、给姓名排序、中文姓名排序、拼音排姓名时使用。处理多音字姓（如曾zēng/仇qiú/解xiè）、同音异姓按笔画分组（如于3<余7<俞9<虞13）、同姓先排完再排下一个姓等同音姓排序惯例。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhangxiaopeng-zgci](https://clawhub.ai/user/zhangxiaopeng-zgci) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and other users can use this skill to sort lists of Chinese personal names according to pinyin-based naming conventions. It is useful when names should be grouped by surname pronunciation, ordered by surname stroke count for homophones, and displayed with pinyin annotations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on the third-party pypinyin Python package. <br>
Mitigation: Install pypinyin from a trusted package source and review dependency updates according to the user's normal package management process. <br>
Risk: Sorting accuracy for rare characters may be limited by the script's hardcoded stroke data. <br>
Mitigation: Review results for uncommon names and add or adjust stroke data when higher accuracy is required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhangxiaopeng-zgci/chinese-name-pinyin-sort) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and plain-text sorted name output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The script can emit numbered or grouped sorted lists and may flag homophone groups that cannot be distinguished by pinyin alone.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
