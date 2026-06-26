## Description: <br>
Provides Canvas 2D rendering optimization guidance for large element counts using layered rendering, viewport culling, LOD, and frame scheduling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chenxiaoyu0124-web](https://clawhub.ai/user/chenxiaoyu0124-web) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Frontend developers use this skill to diagnose and improve Canvas visualizations that drop frames with thousands of elements. It is aimed at interactive wafer maps, heat maps, scatter plots, map markers, timelines, and large Canvas tables. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: OffscreenCanvas support and behavior vary by browser, which can affect the recommended static-layer strategy. <br>
Mitigation: Feature-detect OffscreenCanvas, provide an HTMLCanvasElement fallback, and test the target browser matrix before release. <br>
Risk: The listed FPS improvements are workload-dependent and may not reproduce with different element geometry, viewport behavior, or interaction patterns. <br>
Mitigation: Benchmark against the actual data size, zoom and pan patterns, and draw operations before relying on the published performance targets. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chenxiaoyu0124-web/canvas-render-optimize) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code] <br>
**Output Format:** [Markdown with TypeScript code snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes workload-dependent performance guidance and browser compatibility notes.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release and clawhub.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
