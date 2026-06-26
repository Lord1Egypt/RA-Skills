---
name: AI 3D Generation
slug: 3d-generation
version: 1.0.0
homepage: 
description: Create, convert, and download AI-generated 3D models using Neural4D APIs. Optimized for commercial pipelines.
changelog: Initial release with Text-to-3D, Image-to-3D matting pipelines, and physical format conversion (STL/FBX/USDZ).
metadata: {"clawdbot":{"requires":{"bins":["curl", "jq"],"env.optional":["NEURAL4D_API_TOKEN"],"config":["~/neural4d-3d-generation/"]},"os":["linux","darwin","win32"]}}
---

## Setup

On first use, ensure the `NEURAL4D_API_TOKEN` environment variable is set.
All API requests must include the header: `Authorization: Bearer <YOUR_TOKEN>`.

## When to Use

Use this skill when generating 3D models from text prompts or images using DreamTech's Neural4D engine. This is particularly suited for creating assets where precise format conversions (like `.stl`, `.obj`, `.fbx`) and physical dimensions are required for manufacturing workflows.

## Core Rules & Cost Guardrails

### 1. Point Consumption Awareness
Always track API point costs before executing bulk runs:
- **Text to 3D:** 20 points per operation.
- **Image to 3D:** 20 points per operation.
- **Chibi-style Generation:** 30 points per operation.
- **Format Conversion:** 10 points per operation.
- You can query the remaining balance at `/api/queryPointsInfo`.

### 2. Asynchronous Polling Contract
Model generation is asynchronous. You must poll for completion:
- Query `/api/retrieveModel` using the `uuid`.
- Check `codeStatus`:
  - `0`: Generation complete.
  - `1`: Generating (Wait and poll again).
  - `-3`: Generation failed.

## Workflow Pipelines

### Pipeline A: Text to 3D
1. **Request:** `POST https://alb.neural4d.com:3000/api/generateModelWithText`.
   - Payload: `{"prompt": "...", "modelCount": 4, "disablePbr": 0}`.
2. **Retrieve:** Extract `uuids` from the response.
3. **Poll:** Call `/api/retrieveModel` with the `uuid` until `codeStatus` is `0`.
4. **Download:** Extract `modelUrl` and download the `.glb` asset.

### Pipeline B: Image to 3D (Strict 3-Step Process)
1. **Matting:** Submit the image (JPG/PNG, <10MB, 256x256 to 6048x8064) via `multipart/form-data` to `/api/mattingImage`. Extract the `requestId`.
2. **Get Matting Result:** Send the `requestId` to `/api/getMattedResult`. Extract a preferred `fileKey` from the response.
3. **Generate:** Send the `fileKey` to `/api/generateModelWithImage` to start generation and receive `uuids`.
4. **Poll:** Use `/api/retrieveModel` to poll status and get the `modelUrl`.

### Pipeline C: Format Conversion for Manufacturing
For physical prototyping, default exports must be converted from `.glb`.
1. **Request:** `POST https://alb.neural4d.com:3000/api/convertToFormat`.
2. **Payload:** Provide the `uuid`, desired `modelType` (e.g., `stl`, `fbx`, `obj`), and `modelSize` in millimeters (must be > 1).
3. **Poll Status:** Check `statusType`:
   - `0`: Complete, use `modelUrl` to download.
   - `1`: Converting (Wait and retry).
   - `-1`: Failed or bad parameters.

## External Endpoints Reference

All requests route through the base URL: `https://alb.neural4d.com:3000/api`.

| Action | Endpoint | Auth | Purpose |
|--------|----------|------|---------|
| Text to 3D | `/generateModelWithText` | Bearer Token | Generate from text prompt |
| Retrieve | `/retrieveModel` | Bearer Token | Poll status and get model URL |
| Matting | `/mattingImage` | Bearer Token | Pre-process image |
| Matting Result | `/getMattedResult` | Bearer Token  | Retrieve file keys for image generation  |
| Image to 3D | `/generateModelWithImage` | Bearer Token | Generate from matted fileKey |
| Convert Format | `/convertToFormat` | Bearer Token | Convert to stl/fbx/obj with physical size |
| Job Progress | `/queryJobProgress` | Bearer Token | Check percentage progress |