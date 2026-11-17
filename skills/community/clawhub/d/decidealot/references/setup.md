# Run and connect to Decidealot

Decidealot ships as the `psyb0t/decidealot` Docker image. It downloads its pinned enabled Laya, Von, and CLM bundles during startup into the host directory mounted at `/models`. CLM also needs one configured OpenAI-compatible embeddings endpoint. Hosted Jev needs a TypeSafe key and no model download. Build from source only for development work.

## Start the CPU image

Choose one narrow host directory for model files. The command passes the current host UID and GID into the container, so a directory created by the current user is writable without image-specific ownership.

```bash
model_directory="$HOME/.local/share/decidealot/models"
runtime_uid=$(id -u)
runtime_gid=$(id -g)
mkdir --parents "$model_directory"

docker run --detach --name decidealot --init --restart unless-stopped \
  --user "$runtime_uid:$runtime_gid" \
  --read-only --cap-drop ALL --security-opt no-new-privileges:true \
  --tmpfs /tmp:rw,noexec,nosuid,size=128m \
  --tmpfs /var/run:rw,noexec,nosuid,size=8m \
  --mount type=bind,source="$model_directory",target=/models \
  --publish 127.0.0.1:8080:8080 \
  psyb0t/decidealot:latest
```

The first start downloads enabled model files and can take several minutes. Laya and Von are enabled by default. CLM enables automatically only when `DECIDEALOT_CLM_EMBEDDINGS_URL` is set. Wait for this to return successfully before using the API:

```bash
curl --fail --show-error http://127.0.0.1:8080/health
```

Use an immutable `vX.Y.Z` image tag for a lasting deployment. The full hardening and CUDA recipes are in [Deployment](https://github.com/psyb0t/decidealot/blob/main/docs/deployment.md).

## Hosted Jev

Keep `DECIDEALOT_TYPESAFE_API_KEY` in the container's private environment. Jev enables automatically when it is set. To use Jev without downloading local bundles, set `DECIDEALOT_LAYA_ENABLED=false` and `DECIDEALOT_VON_ENABLED=false`, and leave CLM unconfigured. No `/models` mount is needed in that configuration. `DECIDEALOT_JEV_ENABLED=false` disables Jev even when a key exists. `DECIDEALOT_API_KEY` is a separate token that protects callers of Decidealot.

Select one hosted model returned by `GET /v1/models`. Decidealot caches TypeSafe's authenticated catalog for 60 seconds and refreshes it on the next model-listing or hosted-model request after expiry. It forwards the selected name exactly. The full state and questions go to TypeSafe, so confirm that the user's data is allowed to leave the host. The TypeSafe key stays server-side and never belongs in REST or MCP tool arguments.

## Authentication

Set `DECIDEALOT_API_KEY` when a request crosses any network boundary. It protects REST and MCP except `/health`.

```bash
export DECIDEALOT_URL=http://127.0.0.1:8080
export DECIDEALOT_API_KEY=your-token-here
curl --fail --show-error "$DECIDEALOT_URL/v1/models" --header "Authorization: Bearer $DECIDEALOT_API_KEY"
```

Do not place a real token in a tracked file, prompt, or command history. Omit the header only when the container has no API key and listens only on loopback.

## REST

List selectable aliases, then send raw state plus a bounded question shape:

```bash
curl --fail --show-error "$DECIDEALOT_URL/v1/models" --header "Authorization: Bearer $DECIDEALOT_API_KEY"

curl --fail --show-error "$DECIDEALOT_URL/v1/systemone" \
  --header 'Content-Type: application/json' \
  --header "Authorization: Bearer $DECIDEALOT_API_KEY" \
  --data '{
    "model": "laya-typed-decisions",
    "state": "An operation would permanently remove protected data.",
    "questions": {
      "handling": {
        "type": "choice",
        "instructions": "Choose handling based on whether the operation is reversible and authorized.",
        "criteria": {
          "allow": "The operation is reversible and authorized.",
          "review": "A human must review the operation first."
        }
      }
    }
  }'
```

Use `GET /v1/models` to learn the configured Laya, Von, CLM, and Jev aliases. CLM selectors appear only when the deployment has a fixed embeddings URL that returns Qwen3-8B last-token vectors with width `4096`. Jev selectors appear only when its upstream key is configured and enabled. For several independent decisions, POST `{"requests":[{"model":"laya","state":"First case","questions":{"review":{"type":"noul"}}},{"model":"von","state":"Second case","questions":{"review":{"type":"noul"}}}]}` to `/v1/systemone/batch`. The response has ordered `results`; each item names the model that answered. Requests to one model run sequentially. Local CUDA models and CLM's Qwen calls also share a serial lane by default, while hosted Jev can overlap local work. A batch may wait and switch local models even with one resident slot. `DECIDEALOT_MAX_BATCH_CONCURRENCY` optionally caps simultaneous batch calls, while `DECIDEALOT_MAX_BATCH_REQUESTS` optionally caps item count. Set `DECIDEALOT_CLM_PARALLEL_WITH_LOCAL_MODELS=true` only when the embeddings service and CLM can safely overlap other local models. Use `POST /v1/models/unload` to release loaded local runtimes only when the user asks to free memory. The full request and response contract is in [API](https://github.com/psyb0t/decidealot/blob/main/docs/api.md).

## CLM request settings and caching

CLM accepts optional flat request config, for example `"config":{"temperature":0.8}` alongside `model`, `state`, and `questions`. Temperature must be finite, greater than zero, and at most 100; omitted means 1. Other providers accept only omitted or empty config. Each batch item carries its own settings. The response shape does not change. Invalid settings fail before any batch decision starts. Never put an encoder URL, API key, or deployment configuration in request config.

CLM caches candidate embeddings only. `DECIDEALOT_CLM_CANDIDATE_CACHE_ENTRIES` defaults to 1024 (0 disables, maximum 4096), with `DECIDEALOT_CLM_CANDIDATE_CACHE_TTL_SECONDS=600` (positive, maximum 86400). Unloading CLM clears the cache; changing encoder weights behind the same URL requires a restart or unload. `DECIDEALOT_CLM_MAX_TEXT_BYTES=8192` limits each rendered state plus instructions or candidate before encoding. That is UTF-8 bytes, not tokens. Configure the external encoder to reject rather than truncate inputs beyond its context. Quantized Qwen vectors are not proof of full-precision accuracy parity.

## MCP

Connect an MCP client to `http://127.0.0.1:8080/mcp`.

```json
{
  "mcpServers": {
    "decidealot": {
      "url": "http://127.0.0.1:8080/mcp",
      "headers": {
        "Authorization": "Bearer your-token-here"
      }
    }
  }
}
```

The available tools are `system_one`, `system_one_batch`, `list_models`, and `unload_models`. `system_one` takes the same `model`, `state`, and `questions` object as REST. `system_one_batch` takes the same `requests` list as REST and returns ordered `results`. `list_models` and `unload_models` take `{}`. The MCP client owns protocol initialization and the session header.

MCP accepts loopback clients and the `decidealot` Docker service host by default. For a reverse proxy, set `DECIDEALOT_MCP_ALLOWED_HOSTS` to the exact public Host header. If a browser MCP client sends an Origin, set `DECIDEALOT_MCP_ALLOWED_ORIGINS` to that exact scheme and host. Keep DNS rebinding protection enabled. After bearer authentication, an unknown Host returns `421`; an unknown Origin returns `403`. The full tool contract and deployment examples are in [MCP](https://github.com/psyb0t/decidealot/blob/main/docs/mcp.md) and [Deployment](https://github.com/psyb0t/decidealot/blob/main/docs/deployment.md#authentication-and-exposure).

## OpenClaw bridge

Install the bridge only when the MCP client requires local stdio. It connects to a Decidealot container you already run.

```bash
openclaw plugins install clawhub:@psyb0t/decidealot
export DECIDEALOT_URL=http://127.0.0.1:8080
export DECIDEALOT_API_KEY=your-token-here
```

The bridge appends `/mcp` and forwards stdio traffic to the running container.
