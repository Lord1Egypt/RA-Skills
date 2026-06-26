## Description: <br>
Aetherviz Master helps agents generate interactive educational HTML pages with Three.js, SVG visualizations, KaTeX formulas, controls, and quizzes from a teaching topic. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liwu800729](https://clawhub.ai/user/liwu800729) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Educators, students, and education content creators use this skill to turn a teaching topic into a responsive interactive lesson page with 3D or SVG visualizations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated HTML may load JavaScript or styles from third-party CDNs, which can be unsuitable for offline, classroom, or sensitive environments. <br>
Mitigation: Review the generated HTML before deployment and vendor, pin, or remove external libraries when a fully self-contained page is required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/liwu800729/aetherviz-master) <br>
- [Three.js r134 CDN](https://cdnjs.cloudflare.com/ajax/libs/three.js/r134/three.min.js) <br>
- [Tailwind CSS CDN](https://cdn.tailwindcss.com) <br>
- [KaTeX 0.16.11 CSS](https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css) <br>
- [D3.js v7](https://d3js.org/d3.v7.min.js) <br>


## Skill Output: <br>
**Output Type(s):** [code, guidance] <br>
**Output Format:** [Single HTML document] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The generated HTML is intended for browser use and may reference CDN-hosted web libraries unless the agent adapts it for fully local use.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
