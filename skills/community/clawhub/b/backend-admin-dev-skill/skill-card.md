## Description: <br>
Guides agents through developing a Vue 3 and Flask backend admin portal with RBAC, project management, image upload, S3-compatible storage, content management, settings, logs, and deployment notes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[258468639](https://clawhub.ai/user/258468639) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to plan and implement backend administration features for a project portal, including permissions, users, projects, file storage, content operations, and deployment configuration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Password storage guidance in the artifact references raw SHA256 hashing. <br>
Mitigation: Use bcrypt or Argon2 for password hashing before applying the design in a real system. <br>
Risk: The artifact describes token-based authentication with tokens stored in localStorage. <br>
Mitigation: Assess token lifetime and storage strategy, and prefer safer session handling for production deployments. <br>
Risk: The artifact includes image and attachment upload workflows plus S3-compatible credentials. <br>
Mitigation: Validate file type and size, scan or restrict uploads, and keep storage credentials scoped and private. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with code snippets, API notes, and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include proposed file paths, API routes, database tables, Docker settings, and security recommendations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
