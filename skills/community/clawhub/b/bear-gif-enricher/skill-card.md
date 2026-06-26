## Description: <br>
Bear GIF Enricher enriches Bear research notes tagged "待整理" by extracting a topic, finding a matching GIF via Tenor or Giphy, appending it to the note, and retagging the note. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[terrycarter1985](https://clawhub.ai/user/terrycarter1985) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and automation-minded note takers use this skill to batch enrich Bear notes marked for cleanup with topic-matched GIFs and report failures for follow-up. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bulk execution can persistently edit Bear notes. <br>
Mitigation: Review the scripts first and test on backed-up or disposable notes before running against a real Bear library. <br>
Risk: Note-derived search terms can be sent to Tenor or Giphy. <br>
Mitigation: Avoid running the skill on confidential notes or notes whose titles or first lines should not leave the machine. <br>
Risk: The completion-tag step may create an extra note instead of marking the original note as done. <br>
Mitigation: Fix or manually verify the retagging command before batch use. <br>


## Reference(s): <br>
- [Bear GIF Enricher on ClawHub](https://clawhub.ai/terrycarter1985/bear-gif-enricher) <br>
- [Tenor GIF Search API endpoint used by the skill](https://tenor.googleapis.com/v2/search) <br>
- [Giphy GIF Search API endpoint used by the skill](https://api.giphy.com/v1/gifs/search) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown status text with shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call local Bear/grizzly tooling and external GIF search APIs when the user runs the generated commands.] <br>

## Skill Version(s): <br>
0.1.0 (source: release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
