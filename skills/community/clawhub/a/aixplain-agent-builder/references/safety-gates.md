# Safety Gates

Use these gates to keep the skill low-risk by default.

## Safe by Default

These actions are allowed without extra approval:

- search marketplace tools, models, and integrations
- inspect existing agent configuration
- propose an architecture or tool plan
- attach existing public marketplace tools that are already read-only

## Require Explicit Approval

Do not proceed unless the user clearly approves the specific step:

- creating or updating a deployed agent
- adding an authenticated integration
- uploading a local file to remote storage when direct local configuration is not sufficient
- enabling write actions on external systems
- using a runtime-execution tool
- using a custom script-backed tool
- changing the underlying model
- bypassing standard SDK or platform flows with direct export calls

## Environment Handling

- Prefer existing environment configuration over ad hoc values provided in chat.
- Prefer existing environment configuration.
- If a key is missing, stop and say what variable is required.

## Permission Language

When a risky step is needed, say exactly what will happen before doing it.

Example:

`This step will create a mail integration with outbound-send capability. Approve if you want me to proceed.`
