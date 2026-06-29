---
name: create-3d-model-from-image
description: "3D Modeling Agent: Create 3D models from images or text, refine text-generated drafts into final textured assets, and retrieve completed model files from one combined tool. Use when an agent needs 3d modeling agent, create 3d model from image, image to 3d conversion, text to 3d generation, 3d draft generation, 3d model refinement, create model from image, image url through AgentPMT-hosted remote tool calls. Discovery terms: 3d modeling agent, create 3d model from image, image to 3d conversion."
version: 1.0.0
homepage: https://www.agentpmt.com/marketplace/create-3d-model-from-image
compatibility: "Agent instructions for AgentPMT-hosted remote tool calls. Follow this skill body for supported account, wallet, and setup routes. No local command runtime is declared."
metadata: {"author":"agentpmt","openclaw":{"homepage":"https://www.agentpmt.com/marketplace/create-3d-model-from-image"}}
---
# 3D Modeling Agent

## Freshness
Last updated: `2026-06-24`.

If the current date is more than 7 days after the last updated date, reinstall this skill from skills.sh or ClawHub before relying on endpoints, schemas, setup steps, or examples.

## What This Tool Does
Combined 3D modeling workflow for creating assets from a single source image or from a text prompt, refining text-generated drafts into final textured models, and retrieving task status and download URLs from one tool. Supports configurable topology, polygon count, symmetry handling, texture generation, optional PBR outputs, and humanoid pose hints. Completed tasks return downloadable assets in formats such as GLB, FBX, OBJ, and USDZ, while list and get actions make it possible to track active jobs and retrieve completed outputs before the download links expire.

## Product Instructions
### 3D Modeling

Generate 3D models from images or text, refine text-generated drafts into final textured assets, and retrieve saved task results from one tool.

#### Actions

##### `get_instructions`
Returns this documentation.

##### `create_model_from_image`
Creates a new image-to-3D generation task.

Required:
- `image_url` — public image URL or base64 data URI for the source image

Optional:
- `topology` — `quad` or `triangle` (default `triangle`)
- `target_polycount` — integer from `100` to `300000` (default `30000`)
- `symmetry_mode` — `off`, `auto`, or `on` (default `auto`)
- `should_remesh` — boolean (default `true`)
- `should_texture` — boolean (default `true`)
- `enable_pbr` — boolean (default `false`)
- `pose_mode` — `""`, `a-pose`, or `t-pose`
- `texture_prompt` — optional texture guidance prompt, max 600 characters
- `texture_image_url` — optional image URL or data URI for texture guidance

##### `create_model_from_text`
Creates an initial text-generated 3D model draft. After the draft succeeds, use `refine_model` to generate the final textured model.

Required:
- `prompt` — text prompt describing the model to generate

Optional:
- `ai_model` — `meshy-5`, `meshy-6`, or `latest` (default `latest`)
- `topology` — `quad` or `triangle` (default `triangle`)
- `target_polycount` — integer from `100` to `300000` (default `30000`)
- `symmetry_mode` — `off`, `auto`, or `on` (default `auto`)
- `should_remesh` — boolean
- `pose_mode` — `""`, `a-pose`, or `t-pose`
- `moderation` — boolean (default `false`)

##### `refine_model`
Turns a successful `create_model_from_text` task into the final textured model.

Required:
- `source_task_id` — task id returned from `create_model_from_text`

Optional:
- `ai_model` — `meshy-5` or `latest` (default `latest`)
- `enable_pbr` — boolean (default `false`)
- `texture_prompt` — optional texture guidance prompt, max 600 characters
- `texture_image_url` — optional image URL or data URI for texture guidance
- `moderation` — boolean (default `false`)

##### `get`
Returns the latest task status and any output URLs.

Required:
- `task_id`

##### `list`
Lists non-expired saved tasks for the current budget.

#### Examples

```json
{"action":"create_model_from_image","image_url":"https://example.com/chair.jpg"}
```

```json
{"action":"create_model_from_text","prompt":"a medieval wooden treasure chest"}
```

```json
{"action":"refine_model","source_task_id":"task_123","enable_pbr":true}
```

```json
{"action":"get","task_id":"task_123"}
```

```json
{"action":"list"}
```

#### Response

Creation actions return `task_id`, `status`, `progress`, `task_family`, `task_stage`, and `settings`.

`get` returns `status`, `progress`, timestamps, and `model_urls` when the task succeeds.

`list` returns `count` and `models[]` with saved task metadata.

#### Notes

- Supported source image formats are JPG, JPEG, and PNG.
- Text-generated drafts must succeed before you call `refine_model`.
- Download links expire after the retention window, so retrieve completed assets promptly.

## When To Use
- Use this skill for `3D Modeling Agent` on AgentPMT.
- Use it when an agent needs this specific tool's behavior, schema, inputs, outputs, and invocation shape.
- Search and activation keywords: 3d modeling agent, create 3d model from image, image to 3d conversion, text to 3d generation, 3d draft generation, 3d model refinement, create model from image, image url.
- Supported action names: `create_model_from_image`, `create_model_from_text`, `get`, `list`, `refine_model`.

## Use Cases
- Image to 3D conversion
- text to 3D generation
- 3D draft generation
- 3D model refinement
- model status polling
- 3D asset retrieval
- product visualization
- game asset creation
- AR and VR asset generation
- 3D prototyping
- concept modeling
- ecommerce 3D assets
- downloadable GLB and FBX generation
- PBR-ready 3D models
- automated 3D workflows

## Categories And Industries
No categories or industry tags are published for this tool.

## Actions And Schema
Complete generated action schema: `./schema.md`.
Supported action count: `5`.
x402 availability: not enabled for this product.

- `create_model_from_image` (action slug: `create-model-from-image`): Create a 3D model from a publicly accessible source image. Returns an asynchronous task id for tracking generation progress and downloading the completed asset. Price: `100` credits. Parameters: `enable_pbr`, `image_url`, `pose_mode`, `should_remesh`, `should_texture`, `symmetry_mode`, `target_polycount`, `texture_image_url`, plus 2 more.
- `create_model_from_text` (action slug: `create-model-from-text`): Create an initial 3D model draft from a text prompt. Use refine_model after the draft succeeds to generate the final textured model. Price: `150` credits. Parameters: `ai_model`, `moderation`, `pose_mode`, `prompt`, `should_remesh`, `symmetry_mode`, `target_polycount`, `topology`.
- `get` (action slug: `get`): Retrieve the latest task status and any output URLs for a single 3D modeling task. Price: `0` credits. Parameters: `task_id`.
- `list` (action slug: `list`): List non-expired saved 3D modeling tasks for the current budget. Price: `0` credits. Parameters: none.
- `refine_model` (action slug: `refine-model`): Turn a successful text-generated draft into the final textured 3D model. Price: `150` credits. Parameters: `ai_model`, `enable_pbr`, `moderation`, `source_task_id`, `texture_image_url`, `texture_prompt`.

## Live Schema And Examples
Use the compact schema above for ordinary calls. Before a new production integration, or whenever parameters, enum values, nested objects, outputs, or examples are unclear, fetch live details first.

- Exact schema: call `agentpmt-tool-search-and-execution` with `action: "get_schema"`, and `tool_id: "create-3d-model-from-image"`.
- Detailed examples: call `agentpmt-tool-search-and-execution` with `action: "get_instructions"` and `tool_id: "create-3d-model-from-image"`, or call this product with `action: "get_instructions"` when the product tool is already selected.
- Treat returned live schema and instructions as more specific than this generated summary.

MCP schema lookup through the main AgentPMT MCP server:

```json
{
  "method": "tools/call",
  "params": {
    "name": "AgentPMT-Tool-Search-and-Execution",
    "arguments": {
      "action": "get_schema",
      "tool_id": "create-3d-model-from-image"
    }
  }
}
```

For live examples, keep the same MCP tool and use these arguments:

```json
{
  "action": "get_instructions",
  "tool_id": "create-3d-model-from-image"
}
```

Authenticated AgentPMT REST schema lookup body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_schema",
    "tool_id": "create-3d-model-from-image"
  }
}
```

Authenticated AgentPMT REST live examples body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_instructions",
    "tool_id": "create-3d-model-from-image"
  }
}
```

## Call This Tool
Product slug: `create-3d-model-from-image`

Marketplace page: https://www.agentpmt.com/marketplace/create-3d-model-from-image

- AgentPMT account route: first use `../agentpmt-account-mcp-rest-api-setup` to connect the main MCP server or REST API for an Agent Group where this tool is enabled.
- x402 route: not enabled for this product.
- AgentPMT overview: use `../what-is-agentpmt` for marketplace, Agent Group, workflow, MCP, REST, and payment concepts.

If those setup skills are not installed beside this product skill, use the downloads below.

Core AgentPMT setup skills:
- What AgentPMT is: ../what-is-agentpmt
  - ClawHub page: https://clawhub.ai/agentpmt/what-is-agentpmt
  - OpenClaw install: `openclaw skills install what-is-agentpmt`
  - skills.sh install: `npx skills add AgentPMT/agent-skills --skill what-is-agentpmt`
- AgentPMT account MCP/REST setup: ../agentpmt-account-mcp-rest-api-setup
  - ClawHub page: https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup
  - OpenClaw install: `openclaw skills install agentpmt-account-mcp-rest-api-setup`
  - skills.sh install: `npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup`

skills.sh install script:

```bash
npx skills add AgentPMT/agent-skills --skill what-is-agentpmt
npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup
```

MCP call shape after the main AgentPMT MCP server is connected:

```json
{
  "method": "tools/call",
  "params": {
    "name": "3D-Modeling-Agent",
    "arguments": {
      "action": "create_model_from_image",
      "enable_pbr": true,
      "image_url": "https://example.com",
      "pose_mode": "",
      "should_remesh": true,
      "should_texture": true,
      "symmetry_mode": "auto",
      "target_polycount": 30000,
      "texture_image_url": "https://example.com"
    }
  }
}
```

Use the exact tool name returned by `tools/list`; the name above is the expected readable form.

Authenticated AgentPMT REST call body:

```json
{
  "name": "create-3d-model-from-image",
  "parameters": {
    "action": "create_model_from_image",
    "enable_pbr": true,
    "image_url": "https://example.com",
    "pose_mode": "",
    "should_remesh": true,
    "should_texture": true,
    "symmetry_mode": "auto",
    "target_polycount": 30000,
    "texture_image_url": "https://example.com"
  }
}
```

Use the setup skill for the account connection details before making REST calls.

## Response Handling
- Treat the returned JSON as the source of truth for this tool call.
- If the response includes warnings or correction targets, apply them before retrying.
- If the response includes a `passed` or success-style boolean, use it as the workflow gate.
- If validation fails or the response shape is unclear, call `get_schema` or `get_instructions` before retrying.
- If `create_model_from_image` fails, preserve the request parameters and retry only after fixing schema, auth, or payment errors.

## Security
- Do not place account secrets, wallet private keys, mnemonics, signatures, or payment headers in prompts or logs.
- Keep tool inputs scoped to the minimum content needed for the task.
- Use the setup skills for credential handling; this product skill only defines product-specific behavior.

## AgentPMT Reference
- What AgentPMT is: ../what-is-agentpmt (ClawHub: `what-is-agentpmt`, page: https://clawhub.ai/agentpmt/what-is-agentpmt; skills.sh: `npx skills add AgentPMT/agent-skills --skill what-is-agentpmt`)
- AgentPMT account MCP/REST setup: ../agentpmt-account-mcp-rest-api-setup (ClawHub: `agentpmt-account-mcp-rest-api-setup`, page: https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup; skills.sh: `npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup`)
- Marketplace product: https://www.agentpmt.com/marketplace/create-3d-model-from-image
- AgentPMT main MCP server: https://api.agentpmt.com/mcp/
- AgentPMT REST invoke endpoint: https://api.agentpmt.com/products/purchase
