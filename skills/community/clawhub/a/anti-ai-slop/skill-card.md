## Description: <br>
Anti AI-Slop helps agents detect, revise, and score English and Chinese prose for formulaic AI-writing patterns such as filler phrases, passive voice, vague attribution, promotional language, and repetitive structure. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pinky-le](https://clawhub.ai/user/pinky-le) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Writers, editors, reviewers, and agents use this skill to identify AI-like writing patterns, rewrite affected passages, summarize changes, and produce a 50-point quality score for English or Chinese prose. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The style rules are opinionated and may over-edit tone, structure, adverbs, passive voice, or common phrases. <br>
Mitigation: Use the skill intentionally for AI-pattern cleanup and have a human review revisions against the desired voice before publication. <br>
Risk: The skill can remove nuance when the original text intentionally uses formulaic, promotional, or highly structured language. <br>
Mitigation: Preserve source meaning as the primary requirement and apply suggested rewrites selectively when the original wording is intentional. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/pinky-le/anti-ai-slop) <br>
- [English Phrases to Remove](references/phrases-en.md) <br>
- [Chinese AI Phrase Blacklist](references/phrases-zh.md) <br>
- [English Structural Patterns to Avoid](references/structures-en.md) <br>
- [Chinese Structural Patterns](references/structures-zh.md) <br>
- [English Before/After Examples](references/examples-en.md) <br>
- [Chinese Before/After Examples](references/examples-zh.md) <br>
- [stop-slop](https://github.com/hardikpandya/stop-slop) <br>
- [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) <br>
- [humanizer](https://github.com/blader/humanizer) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Analysis, Guidance] <br>
**Output Format:** [Markdown or plain text containing rewritten prose, change summary, and quality score] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports English and Chinese prose review with a five-dimension, 50-point scoring system.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
