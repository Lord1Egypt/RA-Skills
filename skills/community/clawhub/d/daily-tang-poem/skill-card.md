## Description: <br>
每日唐诗 provides one Tang poem line with explanation, evening recitation checks, spaced-review questions, and poet-affinity summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Romanluoman00007](https://clawhub.ai/user/Romanluoman00007) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users use this skill to receive daily Tang poetry learning content, practice recitation, review previously passed lines, and view poet-affinity summaries in Chinese. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The remote API receives poem requests, recitation or review answers, and any optional API key or user ID configured by the user. <br>
Mitigation: Review the default API endpoint before installation and use a random or pseudonymous user ID instead of personal contact details. <br>
Risk: Progress-based review depends on optional remote tracking tied to DAILY_TANG_POEM_USER_ID. <br>
Mitigation: Configure DAILY_TANG_POEM_USER_ID only when progress-based review is desired; leave it unset to skip progress recording. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Romanluoman00007/daily-tang-poem) <br>
- [Default Tang poetry API endpoint](https://daily-tang-poem-nqbl.vercel.app) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API Calls, Guidance] <br>
**Output Format:** [Chinese conversational Markdown with API-backed poem, recitation, review, and poet-affinity responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a configured remote API; optional API key and user ID enable authenticated progress tracking.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release metadata and manifest.yaml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
