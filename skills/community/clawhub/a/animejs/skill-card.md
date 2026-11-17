## Description:

Anime.js adapter patterns for HyperFrames. Use when writing Anime.js animations or timelines inside HyperFrames compositions, registering animations on window.__hfAnime, making Anime.js seek-driven and deterministic, or translating Anime.js examples into render-safe HyperFrames HTML.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lucas-kay8](https://clawhub.ai/user/lucas-kay8)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to implement Anime.js animations and timelines in HyperFrames compositions with deterministic, seek-based playback.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mutable third-party JavaScript imports can change animation behavior after installation.

Mitigation: Pin Anime.js CDN imports to explicit versions before using generated examples.

Risk: Validation commands can execute unexpected package versions when run through unpinned tooling.

Mitigation: Run HyperFrames validation through a lockfile-pinned local dependency or npx --no-install.

## Reference(s):

- [Anime.js documentation](https://animejs.com/documentation/)
- [HyperFrames Anime.js adapter source](packages/core/src/runtime/adapters/animejs.ts)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance]

**Output Format:** [Markdown guidance with HTML/JavaScript examples and bash commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance emphasizes deterministic, seek-driven animation registration for HyperFrames.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
