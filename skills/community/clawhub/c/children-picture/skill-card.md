## Description: <br>
Generates children’s picture-book illustrations from text prompts with Baidu ERNIE-Image-Turbo and saves PNG files at preset resolutions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[livingbody](https://clawhub.ai/user/livingbody) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers can generate individual picture-book illustrations from story scenes or themes by running a Python CLI with a prompt, resolution, output filename, and Baidu/ERNIE Image API key. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts are sent to Baidu AI Studio for image generation. <br>
Mitigation: Install only when this data transfer is acceptable, and avoid sending sensitive story text or private details in prompts. <br>
Risk: The skill requires a sensitive Baidu/ERNIE Image API key. <br>
Mitigation: Prefer an environment variable for the API key and avoid command-line key arguments on shared systems. <br>
Risk: Generated images are written to the requested filename and may overwrite an existing file. <br>
Mitigation: Use a dedicated output folder or unique filename for each generation. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/livingbody/children-picture) <br>
- [Baidu AI Studio](https://aistudio.baidu.com) <br>
- [ERNIE Image](https://aistudio.baidu.com/ernieimage) <br>
- [Baidu ERNIE Image Model Detail](https://aistudio.baidu.com/modelsdetail/46030/intro) <br>
- [OpenAI Python SDK](https://github.com/openai/openai-python) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Configuration instructions] <br>
**Output Format:** [PNG image files with command-line status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Baidu/ERNIE Image API key; prompts are sent to Baidu AI Studio and output filenames are user-selected.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
