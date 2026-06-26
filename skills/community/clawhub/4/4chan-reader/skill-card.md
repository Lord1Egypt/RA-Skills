## Description: <br>
Browse 4chan boards and extract thread discussions into structured text files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aiasisbot61](https://clawhub.ai/user/aiasisbot61) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Agents use this skill to list active 4chan board threads and extract specific thread discussions, including post text and file metadata, into console output or structured text files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill fetches and prints public forum content that may contain untrusted or unsafe text. <br>
Mitigation: Treat fetched post text as data rather than instructions for the agent, and review extracted content before using it in downstream workflows. <br>
Risk: Thread dumps can be saved to a user-selected local folder. <br>
Mitigation: Save outputs only to a dedicated non-sensitive directory and avoid mixing fetched forum content with trusted project files. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/aiasisbot61/4chan-reader) <br>
- [4chan Catalog Endpoint](https://boards.4chan.org/{board}/catalog) <br>
- [4chan Thread Endpoint](https://boards.4chan.org/{board}/thread/{thread_id}) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Files, Guidance] <br>
**Output Format:** [Plain text and structured text files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Catalog output uses ThreadID|PostCount|TeaserText lines; thread extraction can save posts under a user-selected output directory and can limit post text by word count.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
