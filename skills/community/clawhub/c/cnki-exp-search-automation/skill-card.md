## Description: <br>
CNKI literature-search automation skill that uses browser automation to search CNKI, collect result lists, and extract article metadata and abstracts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[killgfat](https://clawhub.ai/user/killgfat) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers and agents use this skill to run CNKI advanced or expert searches, gather bibliographic result lists, and extract article details for literature reviews and academic research workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automating CNKI in a browser can encounter CAPTCHAs, anti-bot checks, access restrictions, or service-term constraints. <br>
Mitigation: Use a dedicated browser profile, solve verification challenges manually, keep request frequency modest, and follow CNKI access terms. <br>
Risk: Extracted bibliographic data or abstracts may be incomplete or incorrect when page structure changes or access requires login. <br>
Mitigation: Review extracted results against the CNKI page before relying on them and retry with updated selectors when extraction returns empty fields. <br>


## Reference(s): <br>
- [CNKI Advanced Search](https://kns.cnki.net/kns8s/AdvSearch?type=expert) <br>
- [CNKI Search Field Reference](references/cnki-fields.md) <br>
- [CNKI Query Examples](references/query-examples.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/killgfat/cnki-exp-search-automation) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, configuration, text] <br>
**Output Format:** [Markdown instructions with browser actions, JavaScript snippets, and JSON or CSV result examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces extracted literature metadata and abstracts when used with a browser tool and CNKI access.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release metadata; skill frontmatter reports 0.0.3) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
