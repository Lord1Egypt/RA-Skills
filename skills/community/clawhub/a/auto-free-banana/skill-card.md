## Description: <br>
Generates images in Google Flow (labs.google/fx) through browser UI automation. Supports Nano Banana 2 and Nano Banana Pro with landscape/portrait aspect ratios. Use when the user requests Flow-based image generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liujuntao123](https://clawhub.ai/user/liujuntao123) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users can use this skill to submit image-generation prompts to Google Flow through Chrome browser automation, including model, aspect ratio, image count, login, existing-project, and batch options. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can open or attach to a Chrome debugging session and read Google Flow and Google account cookies. <br>
Mitigation: Run it only with explicit user consent, preferably using a dedicated Chrome profile and Google account for Flow generation. <br>
Risk: The skill stores a reusable OAuth token and cookies in a local plaintext cookies.json file. <br>
Mitigation: Review or override the cookie path before use, restrict local file access, and remove the cached cookies.json file after the task is complete. <br>
Risk: The skill calls Google Flow session endpoints and drives browser UI automation for prompt submission. <br>
Mitigation: Confirm the account, proxy, Chrome profile, and target Flow project before running generation commands. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/liujuntao123/auto-free-banana) <br>
- [Metadata Homepage](https://github.com/JimLiu/baoyu-skills#auto-free-banana) <br>
- [Google Flow](https://labs.google/fx/) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Text] <br>
**Output Format:** [Markdown with inline bash commands and browser-visible generation results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Submits prompts through Chrome UI automation; generated images remain visible in the browser rather than being downloaded by the skill.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter reports 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
