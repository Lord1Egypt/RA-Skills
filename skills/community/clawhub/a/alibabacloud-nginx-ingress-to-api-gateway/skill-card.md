## Description:

Migrates Kubernetes nginx Ingress resources to Alibaba Cloud API Gateway by classifying nginx annotations, generating APIG-ready Ingress YAML, and producing migration guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and platform engineers use this skill to assess nginx Ingress compatibility with Alibaba Cloud API Gateway and prepare migrated APIG Ingress manifests. It supports offline analysis from pasted YAML, files, or directories without requiring cloud credentials or cluster access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated WasmPlugin authentication or authorization examples may include unsafe gateway behavior.

Mitigation: Review generated WasmPlugin code before deployment and change external-auth examples to fail closed on dispatch errors.

Risk: Generated deployment guidance may use dependencies or images that are not pinned.

Mitigation: Pin dependencies and image digests or use reviewed versions before building or deploying plugins.

Risk: Generated operational commands may include delete operations that could affect unintended resources.

Mitigation: Preview delete commands and scope them to the intended namespace before running them.

Risk: Request bodies, Authorization headers, mirrored traffic, and log attributes can contain sensitive data.

Mitigation: Treat these values as sensitive and review generated plugin logging, mirroring, and request-handling behavior before deployment.

## Reference(s):

- [Annotation Mapping](references/annotation-mapping.md)
- [Migration Patterns](references/migration-patterns.md)
- [Built-in Plugins](references/builtin-plugins.md)
- [Plugin Deployment](references/plugin-deployment.md)
- [WasmPlugin SDK](references/wasm-plugin-sdk.md)
- [Verification Method](references/verification-method.md)
- [Alibaba Cloud APIG nginx Ingress migration guide](https://help.aliyun.com/zh/api-gateway/cloud-native-api-gateway/user-guide/migrating-from-nginx-ingress-to-cloud-native-api-gateway)
- [Kubernetes ingress-nginx annotations](https://kubernetes.github.io/ingress-nginx/user-guide/nginx-configuration/annotations/#annotations)
- [Alibaba Cloud Higress Ingress gateway supported annotations](https://help.aliyun.com/zh/api-gateway/cloud-native-api-gateway/user-guide/annotations-supported-by-higress-ingress-gateways)
- [Alibaba Cloud APIG platform plug-ins](https://help.aliyun.com/zh/api-gateway/cloud-native-api-gateway/user-guide/platform-plug-ins/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with YAML, Go, and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses placeholders such as <REGION> and <YOUR_REGISTRY> for deployment-specific values.]

## Skill Version(s):

0.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
