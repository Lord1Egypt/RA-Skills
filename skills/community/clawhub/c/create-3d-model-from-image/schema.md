# 3D Modeling Agent Schema

This generated reference belongs to the adjacent `SKILL.md`. Use it for exact action names, action slugs, parameter summaries, sample parameters, and generated JSON parameter schemas.

Product slug: `create-3d-model-from-image`

x402 availability: not enabled for this product.

## `create_model_from_image`

Action slug: `create-model-from-image`

Price: `100` credits

Create a 3D model from a publicly accessible source image. Returns an asynchronous task id for tracking generation progress and downloading the completed asset.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `enable_pbr` | `boolean` | no | Generate PBR maps including metallic, roughness, and normal outputs when supported. |
| `image_url` | `string` | yes | Public image URL or base64 data URI for the source image. JPG, JPEG, and PNG are supported. |
| `pose_mode` | `string` | no | Pose hint for humanoid subjects. |
| `should_remesh` | `boolean` | no | Apply topology and polygon-count settings. Leave true for most cases. |
| `should_texture` | `boolean` | no | Generate texture maps for the model. |
| `symmetry_mode` | `string` | no | Symmetry handling mode for the generated model. |
| `target_polycount` | `integer` | no | Target polygon count for the output mesh. |
| `texture_image_url` | `string` | no | Optional image URL or data URI to guide texture generation. |
| `texture_prompt` | `string` | no | Optional text guidance for texture generation. |
| `topology` | `string` | no | Mesh topology for the generated model. |

Sample parameters:

```json
{
  "enable_pbr": true,
  "image_url": "https://example.com",
  "pose_mode": "",
  "should_remesh": true,
  "should_texture": true,
  "symmetry_mode": "auto",
  "target_polycount": 30000,
  "texture_image_url": "https://example.com"
}
```

Generated JSON parameter schema:

```json
{
  "enable_pbr": {
    "description": "Generate PBR maps including metallic, roughness, and normal outputs when supported.",
    "required": false,
    "type": "boolean"
  },
  "image_url": {
    "description": "Public image URL or base64 data URI for the source image. JPG, JPEG, and PNG are supported.",
    "required": true,
    "type": "string"
  },
  "pose_mode": {
    "description": "Pose hint for humanoid subjects.",
    "enum": [
      "",
      "a-pose",
      "t-pose"
    ],
    "required": false,
    "type": "string"
  },
  "should_remesh": {
    "default": true,
    "description": "Apply topology and polygon-count settings. Leave true for most cases.",
    "required": false,
    "type": "boolean"
  },
  "should_texture": {
    "default": true,
    "description": "Generate texture maps for the model.",
    "required": false,
    "type": "boolean"
  },
  "symmetry_mode": {
    "default": "auto",
    "description": "Symmetry handling mode for the generated model.",
    "enum": [
      "off",
      "auto",
      "on"
    ],
    "required": false,
    "type": "string"
  },
  "target_polycount": {
    "default": 30000,
    "description": "Target polygon count for the output mesh.",
    "maximum": 300000,
    "minimum": 100,
    "required": false,
    "type": "integer"
  },
  "texture_image_url": {
    "description": "Optional image URL or data URI to guide texture generation.",
    "required": false,
    "type": "string"
  },
  "texture_prompt": {
    "description": "Optional text guidance for texture generation.",
    "required": false,
    "type": "string"
  },
  "topology": {
    "default": "triangle",
    "description": "Mesh topology for the generated model.",
    "enum": [
      "quad",
      "triangle"
    ],
    "required": false,
    "type": "string"
  }
}
```

## `create_model_from_text`

Action slug: `create-model-from-text`

Price: `150` credits

Create an initial 3D model draft from a text prompt. Use refine_model after the draft succeeds to generate the final textured model.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `ai_model` | `string` | no | Text-to-3D model to use for the draft generation step. |
| `moderation` | `boolean` | no | Screen text inputs for harmful content. |
| `pose_mode` | `string` | no | Pose hint for humanoid subjects. |
| `prompt` | `string` | yes | Text prompt describing the model to generate. |
| `should_remesh` | `boolean` | no | Apply topology and polygon-count settings. Defaults depend on the selected AI model. |
| `symmetry_mode` | `string` | no | Symmetry handling mode for the generated draft. |
| `target_polycount` | `integer` | no | Target polygon count for the output mesh. |
| `topology` | `string` | no | Mesh topology for the generated draft. |

Sample parameters:

```json
{
  "ai_model": "latest",
  "moderation": true,
  "pose_mode": "",
  "prompt": "example prompt",
  "should_remesh": true,
  "symmetry_mode": "auto",
  "target_polycount": 30000,
  "topology": "triangle"
}
```

Generated JSON parameter schema:

```json
{
  "ai_model": {
    "default": "latest",
    "description": "Text-to-3D model to use for the draft generation step.",
    "enum": [
      "meshy-5",
      "meshy-6",
      "latest"
    ],
    "required": false,
    "type": "string"
  },
  "moderation": {
    "description": "Screen text inputs for harmful content.",
    "required": false,
    "type": "boolean"
  },
  "pose_mode": {
    "description": "Pose hint for humanoid subjects.",
    "enum": [
      "",
      "a-pose",
      "t-pose"
    ],
    "required": false,
    "type": "string"
  },
  "prompt": {
    "description": "Text prompt describing the model to generate.",
    "required": true,
    "type": "string"
  },
  "should_remesh": {
    "description": "Apply topology and polygon-count settings. Defaults depend on the selected AI model.",
    "required": false,
    "type": "boolean"
  },
  "symmetry_mode": {
    "default": "auto",
    "description": "Symmetry handling mode for the generated draft.",
    "enum": [
      "off",
      "auto",
      "on"
    ],
    "required": false,
    "type": "string"
  },
  "target_polycount": {
    "default": 30000,
    "description": "Target polygon count for the output mesh.",
    "maximum": 300000,
    "minimum": 100,
    "required": false,
    "type": "integer"
  },
  "topology": {
    "default": "triangle",
    "description": "Mesh topology for the generated draft.",
    "enum": [
      "quad",
      "triangle"
    ],
    "required": false,
    "type": "string"
  }
}
```

## `get`

Action slug: `get`

Price: `0` credits

Retrieve the latest task status and any output URLs for a single 3D modeling task.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `task_id` | `string` | yes | Task id returned from a create or refine action. |

Sample parameters:

```json
{
  "task_id": "example task id"
}
```

Generated JSON parameter schema:

```json
{
  "task_id": {
    "description": "Task id returned from a create or refine action.",
    "required": true,
    "type": "string"
  }
}
```

## `list`

Action slug: `list`

Price: `0` credits

List non-expired saved 3D modeling tasks for the current budget.

Parameters:

This action does not require parameters.

Sample parameters:

```json
{}
```

Generated JSON parameter schema:

```json
{}
```

## `refine_model`

Action slug: `refine-model`

Price: `150` credits

Turn a successful text-generated draft into the final textured 3D model.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `ai_model` | `string` | no | Text-to-3D model to use for the refine step. |
| `enable_pbr` | `boolean` | no | Generate PBR maps including metallic, roughness, and normal outputs when supported. |
| `moderation` | `boolean` | no | Screen text inputs for harmful content. |
| `source_task_id` | `string` | yes | Task id returned from create_model_from_text. |
| `texture_image_url` | `string` | no | Optional image URL or data URI to guide texture generation. |
| `texture_prompt` | `string` | no | Optional text guidance for texture generation. |

Sample parameters:

```json
{
  "ai_model": "latest",
  "enable_pbr": true,
  "moderation": true,
  "source_task_id": "example source task id",
  "texture_image_url": "https://example.com",
  "texture_prompt": "example texture prompt"
}
```

Generated JSON parameter schema:

```json
{
  "ai_model": {
    "default": "latest",
    "description": "Text-to-3D model to use for the refine step.",
    "enum": [
      "meshy-5",
      "latest"
    ],
    "required": false,
    "type": "string"
  },
  "enable_pbr": {
    "description": "Generate PBR maps including metallic, roughness, and normal outputs when supported.",
    "required": false,
    "type": "boolean"
  },
  "moderation": {
    "description": "Screen text inputs for harmful content.",
    "required": false,
    "type": "boolean"
  },
  "source_task_id": {
    "description": "Task id returned from create_model_from_text.",
    "required": true,
    "type": "string"
  },
  "texture_image_url": {
    "description": "Optional image URL or data URI to guide texture generation.",
    "required": false,
    "type": "string"
  },
  "texture_prompt": {
    "description": "Optional text guidance for texture generation.",
    "required": false,
    "type": "string"
  }
}
```
