## Description: <br>
Vehicle and automotive image editing for cars, trucks, SUVs, and motorcycles using Bria.ai endpoints for scene generation, reflections, tire refinement, segmentation, atmospheric effects, and lighting harmonization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[galbria](https://clawhub.ai/user/galbria) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, creative operators, and automotive marketing teams use this skill to direct agents through vehicle-aware image editing workflows, including generating scenes, segmenting vehicle parts, refining tires, adding reflections or effects, and harmonizing lighting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Vehicle images are uploaded to Bria.ai for processing, which can expose sensitive customer, location-bearing, or proprietary photos to a third-party service. <br>
Mitigation: Use only images that the user is authorized to send to Bria.ai and avoid sensitive or regulated content unless third-party processing is acceptable. <br>
Risk: Bria credentials may be stored locally at ~/.bria/credentials. <br>
Mitigation: Restrict the credential file's permissions and delete it when the workflow is complete or when credentials should no longer persist. <br>
Risk: The helper can call more than the documented automotive endpoints if an agent or user supplies other Bria paths. <br>
Mitigation: Review requested endpoint paths before execution and prefer the documented /v1/product/vehicle/* endpoints for this skill. <br>


## Reference(s): <br>
- [API Endpoints Reference](references/api-endpoints.md) <br>
- [Shell Client](references/code-examples/bria_client.sh) <br>
- [Bria Automotive Docs](https://docs.bria.ai/product-shot-editing/automotive-endpoints) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, code, guidance] <br>
**Output Format:** [Markdown with inline bash commands and API-call guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return Bria API result URLs, JSON responses, local output filenames, and authentication or billing status messages.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
