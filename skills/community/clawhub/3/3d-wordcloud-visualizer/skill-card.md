## Description: <br>
Creates a local browser-based 3D globe word-cloud visualizer from JSON, Markdown, or text files, including Chinese word segmentation and word-frequency analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[0xf4vul](https://clawhub.ai/user/0xf4vul) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and content creators use this skill to generate a standalone HTML viewer that turns local text or conversation exports into an interactive 3D word cloud for keyword exploration and presentation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated HTML for private conversation exports or sensitive documents may load third-party JavaScript from public CDNs when opened. <br>
Mitigation: Review the generated HTML before use and vendor or cache JavaScript dependencies for offline handling of sensitive data. <br>
Risk: Large input files or very large word counts can make the browser slow or unresponsive. <br>
Mitigation: Keep input files near the documented 10 MB guidance and limit the number of displayed keywords for routine use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/0xf4vul/3d-wordcloud-visualizer) <br>
- [Three.js 0.160.0 CDN dependency](https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.min.js) <br>
- [OrbitControls 0.160.0 CDN dependency](https://cdn.jsdelivr.net/npm/three@0.160.0/examples/js/controls/OrbitControls.js) <br>
- [segmentit 2.0.3 CDN dependency](https://cdn.jsdelivr.net/npm/segmentit@2.0.3/dist/umd/segmentit.min.js) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Markdown, Guidance] <br>
**Output Format:** [Markdown response with standalone HTML/CSS/JavaScript file content and usage notes.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated HTML runs locally in a modern WebGL browser and may fetch JavaScript libraries from public CDNs unless dependencies are vendored.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and target metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
