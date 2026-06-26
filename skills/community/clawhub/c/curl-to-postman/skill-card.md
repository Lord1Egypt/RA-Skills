## Description: <br>
Convert curl commands to Postman Collection v2.1 importable JSON <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liuliwanzi](https://clawhub.ai/user/liuliwanzi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to convert pasted curl commands into Postman Collection v2.1 JSON that can be imported into Postman for API testing and request sharing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Pasted curl commands may include Authorization headers, cookies, API keys, passwords, or private request bodies that are copied into the generated Postman collection. <br>
Mitigation: Remove or mask sensitive values before conversion, and review the generated JSON before importing, syncing, or sharing it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/liuliwanzi/curl-to-postman) <br>
- [Postman Collection v2.1 schema](https://schema.getpostman.com/json/collection/v2.1.0/collection.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, configuration] <br>
**Output Format:** [Pretty-printed Postman Collection v2.1 JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May preserve headers, authentication values, request bodies, query parameters, redirect behavior, and SSL validation settings from the input curl command.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
