## Description: <br>
Captures quick ratings after restaurants, hotels, trips, events, or meetings and stores them in Fulcra as structured annotations for a personal taste graph. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[keng009](https://clawhub.ai/user/keng009) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and personal-agent operators use this skill to capture low-friction post-experience feedback, including scores, return intent, notes, companions, and tags. The skill writes the resulting rating to Fulcra as a Post-Experience Rating annotation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The package includes bundled helpers beyond the rating workflow, including CRM, health/calendar read, and deletion/admin capabilities. <br>
Mitigation: Review the installed files before use and prefer a narrowed package that keeps only post_experience.py and the minimal Fulcra write helper. <br>
Risk: Saved ratings can include sensitive personal context such as companions, locations, and experience notes. <br>
Mitigation: Use --dry-run or explicit confirmation before saving sensitive ratings, and avoid surfacing ratings in public or group contexts. <br>
Risk: Bundled helpers can reach Fulcra or Attio environments when credentials are available. <br>
Mitigation: Install only in environments where Fulcra and any Attio access are intended, remove unrelated Attio/delete/admin helpers when not needed, and pin API hosts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/keng009/skills/fulcra-post-experience-rater) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [Conversational guidance with JSON payloads and a shell command for saving ratings] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can run in dry-run mode before writing a Fulcra moment annotation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
