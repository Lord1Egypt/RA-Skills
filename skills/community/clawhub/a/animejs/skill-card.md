## Description: <br>
Anime.js adapter patterns for HyperFrames. Use when writing Anime.js animations or timelines inside HyperFrames compositions, registering animations on window.__hfAnime, making Anime.js seek-driven and deterministic, or translating Anime.js examples into render-safe HyperFrames HTML. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lucas-kay8](https://clawhub.ai/user/lucas-kay8) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to implement Anime.js animations inside HyperFrames compositions with deterministic, seek-based playback. It helps convert Anime.js examples into render-safe HTML by registering animations on window.__hfAnime and avoiding wall-clock behavior. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Projects may load Anime.js from public CDNs shown in examples. <br>
Mitigation: Review project policy for public CDN use and pin or vendor approved dependencies where required. <br>
Risk: Validation examples use npx-based commands that may execute external project tooling. <br>
Mitigation: Run validation commands in a controlled project environment according to the project's tooling policy. <br>
Risk: Animations can become nondeterministic if they rely on autoplay, timers, async asset loading, network state, or unseeded randomness. <br>
Mitigation: Create animations synchronously, set autoplay to false, register instances on window.__hfAnime, and use finite durations and loop counts. <br>


## Reference(s): <br>
- [Anime.js documentation](https://animejs.com/documentation/) <br>
- [ClawHub Animejs release page](https://clawhub.ai/lucas-kay8/animejs) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with HTML, JavaScript, and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only guidance for deterministic Anime.js registrations in HyperFrames.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
