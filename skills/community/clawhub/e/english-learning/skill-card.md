## Description: <br>
Provides primary, TEM-4, and TEM-8 English listening materials and helps agents fetch material lists and detailed listening-text segments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leiwonginchaozhou-netizen](https://clawhub.ai/user/leiwonginchaozhou-netizen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Learners and educators use this skill to browse English listening-practice materials by level and retrieve ordered text segments and audio links for a selected lesson. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on Supabase environment variables, and an overly broad anon role could expose or modify data beyond intended public listening-material tables. <br>
Mitigation: Use your own Supabase project values, rotate any example anon key that was ever real, and confirm the anon role can only read intended public listening-material tables. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/leiwonginchaozhou-netizen/english-learning) <br>
- [Publisher profile](https://clawhub.ai/user/leiwonginchaozhou-netizen) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API Calls, Guidance, Configuration] <br>
**Output Format:** [Markdown text with Supabase REST API request details and formatted listening-material lists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SUPABASE_URL and SUPABASE_ANON_KEY environment variables.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
