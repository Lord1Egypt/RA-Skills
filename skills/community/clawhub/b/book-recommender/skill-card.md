## Description: <br>
Recommend books based on interests or reading history, look up built-in ratings and reviews, and help manage reading notes and book lists. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cp3d1455926-svg](https://clawhub.ai/user/cp3d1455926-svg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Readers and agents use this skill to get Chinese-language book recommendations, browse books by category or mood, search a built-in book catalog, and keep lightweight reading notes, progress, and bookshelf records. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Reading-list and note data may be saved locally by the skill. <br>
Mitigation: Review where the runtime stores generated JSON files and avoid recording sensitive personal notes unless local storage is acceptable. <br>
Risk: Ratings and reviews appear to come from built-in sample data rather than live Douban lookup in this release. <br>
Mitigation: Treat recommendations and ratings as advisory and verify book details externally before relying on them. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown-style text responses with book lists, ratings, summaries, notes, and reading statistics.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save local JSON files for bookshelf, reading log, and library data.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
