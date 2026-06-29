## Description: <br>
Use for Chinese-first, source-grounded anime recommendations when the user asks for anime similar to something they watched, describes nuanced taste, wants feedback-driven refinement, or cares about story texture, romance dynamics, emotional aftertaste, pacing, relationship patterns, and avoidances rather than only genre tags. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kamiender](https://clawhub.ai/user/kamiender) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to produce compact, Chinese-first anime recommendations that match a user's described viewing experience, explain similarities and differences, and refine results from feedback. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Anime facts, availability, episode counts, or adaptation status can be inaccurate if the skill relies on memory or low-quality search results. <br>
Mitigation: Use the skill's source-grounding workflow: check official pages, Bangumi, AniList, MAL/Jikan, or TMDb as appropriate, and separate verified facts from inference when sources are unavailable. <br>
Risk: The optional experimental local CLI/cache/feedback path can store watch history, preference feedback, API cache data, and possible Bangumi or AniList tokens locally. <br>
Mitigation: Keep the lightweight recommendation workflow as the default, and only use the local CLI/cache/feedback features when the user explicitly requests them and accepts local data storage. <br>
Risk: Broad anime preference requests may activate the skill and produce Chinese-first answers when the user expected a different language or style. <br>
Mitigation: Confirm language and recommendation style when the user's preference is unclear, and adapt the output language to the user's request. <br>


## Reference(s): <br>
- [Anime Semantic Recommender repository](https://github.com/KAMIENDER/anime-semantic-recommender) <br>
- [ClawHub skill page](https://clawhub.ai/kamiender/anime-semantic-recommender) <br>
- [Lightweight recommendation methodology](docs/simple-methodology.md) <br>
- [Technical plan and optional local CLI design](docs/technical-plan.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, text, shell commands] <br>
**Output Format:** [Markdown or plain text recommendation lists with optional inline shell commands for the experimental local CLI] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Default responses are compact Chinese-first recommendation explanations; optional local CLI features may produce JSON when explicitly requested.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
