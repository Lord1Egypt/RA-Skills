## Description: <br>
Migrates Kubernetes nginx Ingress resources to Alibaba Cloud API Gateway (APIG) by classifying annotations, mapping unsupported behavior, generating migrated Ingress YAML, and producing a deployment report from user-provided YAML. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and platform engineers use this skill to migrate nginx Ingress YAML to Alibaba Cloud API Gateway format without cluster or cloud access. It produces compatibility analysis, migration artifacts, and deployment guidance for APIG ingressClass adoption. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated YAML, WasmPlugin code, deployment commands, or rollback commands could be incorrect for a specific Kubernetes environment. <br>
Mitigation: Review generated artifacts, confirm the Kubernetes context and namespace, and test with dry-run or staging before applying or deleting live Ingress resources. <br>
Risk: Automatically running kubectl, docker login/push, or registry operations could modify clusters or external registries unexpectedly. <br>
Mitigation: Keep those operations manual; use this skill for offline migration assistance and require explicit human execution for cluster and registry changes. <br>
Risk: Generated custom WasmPlugin code or dependencies may need security and compatibility review before deployment. <br>
Mitigation: Review generated code, pin dependencies where practical, and build and test plugins in a controlled environment before pushing images or binding them to Ingress resources. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sdk-team/alibabacloud-nginx-ingress-to-api-gateway) <br>
- [Alibaba Cloud APIG nginx Ingress migration guide](https://help.aliyun.com/zh/api-gateway/cloud-native-api-gateway/user-guide/migrating-from-nginx-ingress-to-cloud-native-api-gateway) <br>
- [ingress-nginx annotations](https://kubernetes.github.io/ingress-nginx/user-guide/nginx-configuration/annotations/#annotations) <br>
- [Alibaba Cloud Higress Ingress annotations](https://help.aliyun.com/zh/api-gateway/cloud-native-api-gateway/user-guide/annotations-supported-by-higress-ingress-gateways) <br>
- [Alibaba Cloud APIG platform plugins](https://help.aliyun.com/zh/api-gateway/cloud-native-api-gateway/user-guide/platform-plug-ins/) <br>
- [Annotation mapping](references/annotation-mapping.md) <br>
- [Migration patterns](references/migration-patterns.md) <br>
- [Built-in plugins](references/builtin-plugins.md) <br>
- [WasmPlugin SDK](references/wasm-plugin-sdk.md) <br>
- [Plugin deployment](references/plugin-deployment.md) <br>
- [Verification method](references/verification-method.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown migration report with YAML, Go, and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Offline analysis from user-provided Ingress YAML; the skill does not execute cluster, registry, or cloud write operations.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
