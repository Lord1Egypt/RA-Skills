## Description: <br>
Syncs Bunpro Japanese grammar learning progress from the community-documented Frontend API to local SQLite storage for backup, progress tracking, review analysis, and JLPT insights. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mart1n-xyz](https://clawhub.ai/user/mart1n-xyz) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External Bunpro users use this skill to back up grammar-learning progress, sync SRS and review data, and generate local reports about mastery, due reviews, leeches, forecasts, and JLPT progress. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The Bunpro Frontend API token is browser-derived and should be treated like a password. <br>
Mitigation: Use an environment variable or secure secret store, avoid passing the token in chat, logs, or CLI history, and refresh it if exposed. <br>
Risk: The local bunpro.db database can contain private learning progress and account-related data. <br>
Mitigation: Keep the database out of shared folders and source control, and apply local access controls appropriate for personal data. <br>
Risk: The skill uses Bunpro's unofficial, community-documented frontend API, which may change or return authorization errors. <br>
Mitigation: Review the referenced API documentation, use reasonable sync frequency, and refresh the frontend token when 401 errors occur. <br>


## Reference(s): <br>
- [Bunpro](https://www.bunpro.jp) <br>
- [Bunpro API Structure Reference](references/api-structure.md) <br>
- [Bunpro Community API GitHub](https://github.com/cbullard-dev/bunpro-community-api) <br>
- [Bunpro Community Forum API Discussion](https://community.bunpro.jp/t/bunpro-api-when/100574) <br>
- [Bunpro Frontend API Postman Collection](https://www.postman.com/technical-meteorologist-63813544/bunpro-api/collection/a7eufz9/bunpro-frontend-api) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code] <br>
**Output Format:** [Markdown with inline bash, SQL, and Python command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides use of Python scripts that call the Bunpro Frontend API and write a local SQLite database.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
