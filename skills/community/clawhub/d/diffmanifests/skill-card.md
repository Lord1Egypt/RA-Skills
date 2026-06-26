## Description: <br>
Compare manifest XML files via Gerrit and Gitiles APIs, producing JSON/txt/xlsx reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[craftslab](https://clawhub.ai/user/craftslab) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and release engineers use this skill to compare Android or repo manifest versions and generate change reports from Gerrit and Gitiles data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Gerrit or Gitiles credentials and manifest contents may be sensitive when used with configured services. <br>
Mitigation: Use a virtual environment, verify the diffmanifests package before installing, prefer limited-scope API tokens, keep configuration private, and process only manifests intended for the configured Gerrit and Gitiles services. <br>


## Reference(s): <br>
- [diffmanifests on ClawHub](https://clawhub.ai/craftslab/diffmanifests) <br>
- [craftslab publisher profile](https://clawhub.ai/user/craftslab) <br>
- [Android Gerrit](https://android-review.googlesource.com) <br>
- [Android Gitiles](https://android.googlesource.com) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, JSON, Markdown] <br>
**Output Format:** [Markdown guidance with shell commands and configuration examples; generated reports may be JSON, plain text, or Excel.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a JSON configuration file, two manifest XML files, and an output path whose extension selects the report format.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
