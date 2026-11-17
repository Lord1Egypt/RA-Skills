---
name: ai-fashion-photos
description: Generate e-commerce fashion photos with Fashio (fashiolabs.com) through its hosted MCP server — put a garment on an AI model, virtual try-on, full catalog photoshoot packs, jewelry on model, flat lays, background removal, upscaling, reframing and short product videos. Use when someone wants on-model product photos from a clothing or jewelry photo, a consistent catalog look across products, or to batch-produce listing images for a store. Requires a Fashio API key; generations spend the account's credits.
---

# AI fashion product photos with Fashio

The `fashio` MCP server (`https://mcp.fashiolabs.com/mcp`) calls Fashio's public v1 API
with the user's own key. Setup:

1. Sign up at <https://fashiolabs.com> and create a key under **Profile → API Keys**
   (shown once; starts with `fio_live_`).
2. Make it available as `FASHIO_API_KEY`. The server receives it as
   `Authorization: Bearer ${FASHIO_API_KEY}`.

Full API reference: <https://docs.fashiolabs.com> ·
LLM-ready version: <https://docs.fashiolabs.com/llms-full.txt>

## Cost: read this first

Every `create_generation` and `create_catalog_job` call deducts diamonds (Fashio
credits) from the key's account, the same as using the app. There is no test mode.

- Call `get_account` first and tell the user their balance.
- Before each paid call, say which tool runs, how many images it makes and its price
  (`list_models` gives `fallbackPriceDiamonds`; a catalog job is billed per shot). Wait for a yes.
- `400` (bad input) and `402` (balance too low) charge nothing. A failed generation is refunded automatically.
- `delete_template_set` deletes for good; confirm first.

## Flow

1. **Get the garment online.** Prefer a public image URL the user gives you. Otherwise
   `upload_image` takes the image as base64 bytes plus its `format` (jpg/png/webp, up
   to 8 MB) and returns a URL. (The local `fashio-mcp` npm package takes a file path instead.)
2. **Pick the tool.** `list_models` lists every `toolId` and the images it needs. Common ones:

   | Goal | toolId | Needs |
   |---|---|---|
   | Garment on an AI model | `virtual_model` | `fashion_model`, `garment_photo` |
   | Several garments, one outfit | `outfit_photo` | `fashion_model`, `garment_photos[]` |
   | Jewelry on a model | `jewelry_on_model` | `jewelry_image`, `jewelryType` |
   | Swap the model in a photo | `model_swap` | `user_photo`, `fashion_model` |
   | On-model → flat lay | `model_to_flat_lay` | `user_photo` |
   | Remove background / upscale | `remove_background` / `photo_enhance` | `user_photo` |
   | Change aspect ratio | `photo_reframe` | `user_photo`, `targetRatio` |
   | Edit with an instruction | `photo_edit` | `user_photo`, `customPrompt` |
   | Short product video | `ai_videos` | `user_photo`, `motionPrompt` |

3. **Choose model, venue and pose** with `list_fashion_models` (`gender`), `list_venues`
   and `list_poses`, or skip them with a saved style (`templateSetId`).
4. **Start the job** with `create_generation`. It returns `{id, status: "processing"}`.
5. **Poll** `get_generation` every few seconds until `completed` (results in
   `resultUrls`) or `failed`. Show the result URLs.

## Same look across a whole catalog

- After a result the user likes, `create_template_set` saves its model, venue, pose
  and ratio. Reuse it on the next product with `create_generation` + `templateSetId`.
- For a ready-made multi-shot photoshoot, browse `list_ready_template_sets`, open one
  with `get_ready_template_set`, then run `create_catalog_job` on the product (one image per shot,
  billed per shot; pass `shotIds` to run fewer).

## Errors

`401` bad or revoked key · `402` balance too low (nothing charged) · `429` daily
request cap for the key · `500` failed after charging, refunded automatically.
