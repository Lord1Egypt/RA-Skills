# BasicOps MCP troubleshooting

Use this reference when setup does not produce a usable BasicOps MCP surface.

## Common failure modes

### Server missing entirely
Meaning:
- the client has no BasicOps MCP entry yet

Response:
- add the server entry
- reload the client if needed

### Server present but unauthorized
Meaning:
- bearer token missing, expired, malformed, or placed in the wrong config field

Response:
- re-check the auth header shape
- confirm the token source
- re-run verification after updating auth

### Server present but tools not visible
Meaning:
- the client may need reload/restart
- the transport or config schema may be wrong
- the client may not support this MCP transport the way the config expects

Response:
- re-check the client-specific config shape
- reload or restart the client
- verify again after restart

### User expects the skill to operate BasicOps immediately
Meaning:
- setup is being confused with operation

Response:
- finish setup first
- then hand off to `basicops-mcp-operator`

## Good troubleshooting posture

- isolate whether the problem is discovery, configuration, authentication, or reload state
- keep the next step concrete
- avoid vague advice like "check your setup"

## Good short blocker messages

- "BasicOps MCP is not configured in this client yet."
- "The BasicOps MCP entry exists, but authentication is failing."
- "The client likely needs a reload before the BasicOps tools will appear."
- "The MCP connection is ready, but the operator skill should handle the actual BasicOps work from here."
