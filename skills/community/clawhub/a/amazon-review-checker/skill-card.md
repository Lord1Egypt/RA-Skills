## Description: <br>
Amazon review authenticity analyzer. Detect fake reviews, suspicious patterns, and rating manipulation. Includes time clustering detection, content similarity analysis, rating distribution checks, and verified purchase validation. Progressive analysis with L1-L4 depth levels. No API key required. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[phheng](https://clawhub.ai/user/phheng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, e-commerce sellers, and developers use this skill to assess Amazon review authenticity from pasted text or structured review data and identify suspicious review patterns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Review text can include personal reviewer details or other unnecessary sensitive information. <br>
Mitigation: Paste only the review fields needed for analysis and omit personal data unless it is required for the review task. <br>
Risk: Generated HTML reports may include untrusted review text and load a remote chart library. <br>
Mitigation: Open generated reports only from trusted inputs and review report content before sharing it. <br>
Risk: Authenticity scores are heuristic and can be incomplete when only review text is provided. <br>
Mitigation: Treat results as decision support and provide dates, ratings, and verified-purchase status when available. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/phheng/amazon-review-checker) <br>
- [Nexscope AI](https://www.nexscope.ai/) <br>
- [Chart.js CDN](https://cdn.jsdelivr.net/npm/chart.js) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands] <br>
**Output Format:** [Markdown-style authenticity report with optional JSON input and generated HTML report file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces an authenticity score, risk classification, detection dimensions, suspicious-review explanations, and suggestions for deeper analysis.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata; artifact frontmatter and changelog mention 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
