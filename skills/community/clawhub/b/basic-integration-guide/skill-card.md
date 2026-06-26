## Description: <br>
指导开发者如何接入basic基础服务，包括依赖引入、gRPC调用、REST API使用、配置说明。涵盖国际化(i18n)、项目管理、租户管理、字典管理、存储、认证等核心能力 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[effort02](https://clawhub.ai/user/effort02) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and integration engineers use this skill as a reference guide for connecting systems to the Basic service through Maven dependencies, gRPC clients, REST APIs, tenant headers, and authentication context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Copied examples may include placeholder hosts, bearer tokens, or sensitive service configuration. <br>
Mitigation: Replace placeholders before use, store secrets in a secret manager, and avoid committing tenant, token, database, OIDC, OSS, or storage credentials. <br>
Risk: Some documented APIs perform delete, reset, import, publish, rollback, draft-clearing, or batch storage operations. <br>
Mitigation: Require approval, backups, audit logging, and rollback procedures before using those operations in production environments. <br>
Risk: The sample gRPC configuration uses plaintext negotiation. <br>
Mitigation: Use TLS or mTLS where appropriate before adapting the example for production traffic. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/effort02/basic-integration-guide) <br>
- [Publisher profile](https://clawhub.ai/user/effort02) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guide with XML, YAML, Java, Protobuf, curl, and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only output; no code is installed or executed by the skill.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
