## Description:

Generates a local browser-based 3D globe word-cloud visualizer from JSON, Markdown, or TXT text files with Chinese segmentation and top-word frequency analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0xf4vul](https://clawhub.ai/user/0xf4vul)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and agent users use this skill to create a self-contained HTML visualizer for exploring conversation exports or other text files as an interactive 3D word cloud.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The generated browser page relies on public CDN scripts for Three.js, OrbitControls, and segmentit.

Mitigation: For sensitive conversation exports or controlled environments, bundle local copies of the JavaScript dependencies or verify cached dependencies before offline use.

Risk: Large uploaded text files may slow or freeze the browser during segmentation, word-frequency analysis, or 3D rendering.

Mitigation: Keep input files within the documented size guidance or reduce the number of rendered keywords before processing large datasets.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/0xf4vul/skills/3d-wordcloud-visualizer)
- [Three.js CDN dependency](https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.min.js)
- [OrbitControls CDN dependency](https://cdn.jsdelivr.net/npm/three@0.160.0/examples/js/controls/OrbitControls.js)
- [segmentit CDN dependency](https://cdn.jsdelivr.net/npm/segmentit@2.0.3/dist/umd/segmentit.min.js)

## Skill Output:

**Output Type(s):** [Code, Files, Guidance]

**Output Format:** [HTML/CSS/JavaScript file with concise usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated browser page processes uploaded text locally and uses public CDN JavaScript dependencies unless bundled locally.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
