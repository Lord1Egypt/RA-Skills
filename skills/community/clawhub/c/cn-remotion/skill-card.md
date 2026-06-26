## Description: <br>
用 React 代码程序化生成视频的框架，支持 CSS/Canvas/SVG/WebGL，可部署到 Lambda/Cloud Run 大规模渲染，适合创意视频生成、数据可视化视频和个性化视频批量生产 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cn-big-cabbage](https://clawhub.ai/user/cn-big-cabbage) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and creators use this skill to get Remotion guidance for building React and TypeScript video projects, previewing and rendering local outputs, and preparing AWS Lambda or Google Cloud Run rendering workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Suggested npm or npx commands may install or execute packages in the user's environment. <br>
Mitigation: Review package installation commands before execution and run them only in the intended project directory. <br>
Risk: Local render and cleanup commands may create, overwrite, or remove generated video files. <br>
Mitigation: Confirm render targets and cleanup paths before allowing an agent to run file-changing commands. <br>
Risk: AWS Lambda or Google Cloud Run deployment guidance can create cloud resources or costs in the wrong account or project. <br>
Mitigation: Use least-privilege cloud credentials and confirm the target account, project, region, and resource names before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cn-big-cabbage/cn-remotion) <br>
- [Remotion homepage](https://remotion.dev) <br>
- [Remotion documentation](https://remotion.dev/docs) <br>
- [Remotion API reference](https://remotion.dev/api) <br>
- [Remotion GitHub repository](https://github.com/remotion-dev/remotion) <br>
- [Remotion Lambda permissions](https://remotion.dev/docs/lambda/permissions) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash and TypeScript code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose npm/npx commands, local render commands, and optional cloud deployment configuration for Remotion workflows.] <br>

## Skill Version(s): <br>
0.1.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
