## Description:

Provides a daily guided reading of the seven books of Vālmīki's Rāmāyaṇa with tracked progress, a Chinese lecture, a miniature-style illustration, and Chinese narration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yumyumtum](https://clawhub.ai/user/yumyumtum)

### License/Terms of Use:

MIT-0

## Use Case:

Readers who want a guided daily reading of the Rāmāyaṇa use this skill to work through one segment at a time, with a Chinese lecture, source excerpt, cultural context, illustration, and narration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Narration sends its script to Microsoft's online speech service.

Mitigation: Keep private information out of narration scripts or set NO_TTS=1.

Risk: The ClawHub release omits the book text and may rely on separately supplied archive helpers.

Mitigation: Provide the required source text and review separately supplied archive helpers before use.

Risk: The speech dependency may change over time.

Mitigation: Pin the edge-tts dependency.

## Reference(s):

- [Project Gutenberg: The Rámáyan of Válmíki (Books 1–6)](https://www.gutenberg.org/ebooks/24869)
- [Internet Archive: The Ramayana, Uttarakandam (Book 7)](https://archive.org/details/TheRamayanaUttaraKandam)
- [edge-tts documentation](https://github.com/rany2/edge-tts)

## Skill Output:

**Output Type(s):** [Text, Markdown, Image, Audio]

**Output Format:** [Markdown episode lecture with optional illustration and Chinese audio narration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Progress-tracked, one reading segment per episode; illustration or narration may be skipped if generation fails.]

## Skill Version(s):

1.0.7 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
