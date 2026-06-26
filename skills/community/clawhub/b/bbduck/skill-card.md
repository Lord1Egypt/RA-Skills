## Description: <br>
BBDuck helps agents compress local images with a visual-lossless default, stream compression logs, and prepare compressed results for ZIP download. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhaoolee](https://clawhub.ai/user/zhaoolee) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation agents use BBDuck to compress local JPG, PNG, WebP, and GIF images through a localhost Docker service while prioritizing visual-lossless output. It is especially useful when users need streaming progress logs, per-step timing, and optional ZIP packaging of compressed outputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks users to run a third-party Docker image locally and expose a service port. <br>
Mitigation: Install only after reviewing the Docker image source or digest, bind the service to localhost with 127.0.0.1:28642:8000, stop the container when finished, and send only images intended for compression. <br>


## Reference(s): <br>
- [ClawHub BBDuck listing](https://clawhub.ai/zhaoolee/bbduck) <br>
- [Artifact README](artifact/README.md) <br>
- [Local Swagger UI](http://127.0.0.1:28642/docs) <br>
- [Local OpenAPI JSON](http://127.0.0.1:28642/openapi.json) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, API calls, Files, Guidance] <br>
**Output Format:** [Markdown guidance with curl examples, NDJSON log summaries, API request details, and file or ZIP handling instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Primarily targets local images and the localhost BBDuck service at http://127.0.0.1:28642.] <br>

## Skill Version(s): <br>
0.2.2 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
