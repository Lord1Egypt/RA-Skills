# Transfers with Studio's stored credentials

Beam Studio keeps storage credentials in its own store (Studio's Credentials
page). Through Studio's MCP server, an agent starts transfers that reference those
credentials by ID. Studio's worker signs the storage requests, so the agent never
sees a key.

## Connect once

The user does this, not the agent:

1. In Studio, open the MCP page and create a token with `read:credentials`,
   `write:transfers`, `run:transfers` and `read:runs` (add `cancel:runs` to let
   the agent cancel). Studio shows the token once.
2. Add Studio's MCP server to the agent. Its URL is `https://<studio MCP host>/mcp`
   when Studio's MCP server is served over HTTPS, or `http://localhost:8766/mcp`
   on the machine running Studio (loopback only by default).
   - Hermes: `hermes mcp add beam-studio --url <MCP URL> --auth header`, then
     paste the token when asked. Hermes keeps it with its other secrets.
   - OpenClaw: `openclaw mcp add beam-studio --url <MCP URL> --header
     "Authorization=Bearer <token>"`. It connects before saving.
3. Start a new session. This file uses the plain tool names (`beam.*`). Agents
   rename them: Hermes calls `beam.list_credentials`
   `mcp__beam_studio__beam_list_credentials`, and OpenClaw calls it
   `beam-studio__beam-list_credentials`.

## Run a transfer

1. `beam.list_credentials` lists each credential's `id`, `name`, `kind` and the
   names of its fields, never the values.
   - Storage keys: kind `s3_compatible_access_key` (S3, R2, Hippius and other
     S3-compatible stores) or `huggingface_token`.
   - The Beam API key the transfer is billed to: kind `beam_api_key`.
   - The listing does not say which provider an S3-compatible key is for. Go by
     its name, or ask the user.
2. Confirm with the user: the source, every destination (existing objects are
   overwritten) and the cost (0.01 credit per GB delivered to each destination,
   plus 1 credit per workflow run).
3. `beam.create_workflow` with a `name` returns the workflow. Then
   `beam.get_workflow` shows its manual trigger.
4. `beam.update_workflow_graph` with the graph below. It replaces the whole graph.
5. `beam.run_workflow` with the `workflowId` starts a run.
6. `beam.get_workflow_run` reports step states and failures. When the transfer
   step succeeds, its outputs carry `beamTransferId` and `beamStatus`; report the
   transfer ID to the user. `beam.cancel_workflow_run` cancels the run and its
   transfer.

To run the same transfer again, call `beam.run_workflow` again.

## Graph

One endpoint step per object, one transfer step, and one trigger edge from the
manual trigger to **every** endpoint step: an endpoint step without a trigger
edge never starts, and the transfer then waits forever. Step and edge IDs must be unique across the whole Studio: use
the prefixes shown with a random suffix of at least 12 hex characters, for
example from a UUID. Never reuse example or sequential suffixes.

```json
{
  "workflowId": "<workflow id>",
  "triggers": [{ "id": "<trigger id from beam.get_workflow>", "type": "manual", "name": "Trigger manually", "enabled": true, "config": {} }],
  "triggerEdges": [
    { "id": "wfte_<random>", "triggerId": "<trigger id>", "toStepId": "wfs_src<random>", "condition": null },
    { "id": "wfte_<random>", "triggerId": "<trigger id>", "toStepId": "wfs_dst<random>", "condition": null }
  ],
  "steps": [
    {
      "id": "wfs_src<random>", "actionPackageName": "@beam/object-storage-endpoint", "actionVersionRange": "^1.0.0",
      "config": { "name": "Source", "provider": "s3", "bucket": "<bucket>", "objectKey": "<key>", "sourceType": "file", "credentialId": "<storage credential id>" },
      "inputBindings": {}, "enabled": true, "required": false, "position": 0, "placement": "local-workers"
    },
    {
      "id": "wfs_dst<random>", "actionPackageName": "@beam/object-storage-endpoint", "actionVersionRange": "^1.0.0",
      "config": { "name": "Destination", "provider": "r2", "bucket": "<bucket>", "objectKey": "<key>", "sourceType": "file", "credentialId": "<storage credential id>" },
      "inputBindings": {}, "enabled": true, "required": false, "position": 1, "placement": "local-workers"
    },
    {
      "id": "wfs_xfer<random>", "actionPackageName": "@beam/transfer", "actionVersionRange": "^1.0.0",
      "config": { "credentialId": "<beam_api_key credential id>", "name": "<transfer name>" },
      "inputBindings": {
        "sourceEndpoints": ["${steps.wfs_src<random>.outputs.endpoint}"],
        "destinationEndpoints": ["${steps.wfs_dst<random>.outputs.endpoint}"]
      },
      "enabled": true, "required": true, "position": 2, "placement": "local-workers"
    }
  ],
  "edges": [
    { "id": "wfe_<random>", "fromStepId": "wfs_src<random>", "toStepId": "wfs_xfer<random>", "condition": null },
    { "id": "wfe_<random>", "fromStepId": "wfs_dst<random>", "toStepId": "wfs_xfer<random>", "condition": null }
  ]
}
```

- **Fan-out**: add one destination endpoint step per destination, wire the
  trigger and an edge to each, and list every one in `destinationEndpoints`.
- **Providers**: `s3`, `r2`, `hippius`, or another S3-compatible profile name.
  Set `region` and `endpointUrl` in an endpoint's `config` when the store needs
  them. Hippius defaults to `https://s3.hippius.com` and region `decentralized`.
- **Hugging Face**: put the repo in `bucket` with its type prefix (for example
  `datasets/org/corpus`) and the file path in `objectKey`.

## Limits

- The transfer step waits up to 3,600 seconds (`maxDurationSeconds` in its
  `config`). A transfer still running then is cancelled. For longer transfers,
  use the helper with keys from the environment.
- Storage keys must not be restricted by IP or network: workers move data from
  many networks.
- `beam.create_transfer`, `beam.run_transfer_now` and `beam.schedule_transfer`
  belong to Studio's retired transfer templates. Current Studio refuses them with
  `410 legacy_product_retired`. Use workflows.
