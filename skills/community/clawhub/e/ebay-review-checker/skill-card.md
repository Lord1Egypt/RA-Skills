## Description: <br>
eBay review and feedback authenticity analyzer. Detect fake reviews, suspicious seller feedback patterns, and buyer manipulation. Includes time clustering detection, content similarity analysis, and eBay-specific red flag identification. No API key required. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[phheng](https://clawhub.ai/user/phheng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers can use this skill to analyze pasted or structured seller feedback for review-pattern signals, suspicious clustering, and authenticity scoring. The output should support manual review rather than serve as a final eBay fraud determination. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review says the skill is advertised as an eBay fraud checker while the implementation is largely Amazon-oriented and may overstate what it can detect. <br>
Mitigation: Use scores as review-support signals only, verify eBay seller decisions manually, and test the skill on representative eBay feedback before relying on results. <br>
Risk: The security guidance warns against opening generated HTML reports from untrusted review text until report escaping and third-party JavaScript loading are addressed. <br>
Mitigation: Open generated reports only from trusted input, avoid sharing reports created from untrusted feedback, and review report generation before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/phheng/ebay-review-checker) <br>
- [Publisher profile](https://clawhub.ai/user/phheng) <br>
- [Nexscope AI](https://www.nexscope.ai/) <br>
- [Chart.js CDN used by generated reports](https://cdn.jsdelivr.net/npm/chart.js) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text or Markdown analysis reports, command examples, and optional HTML report files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Scores and risk labels are heuristic and depend on the review fields supplied by the user.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
