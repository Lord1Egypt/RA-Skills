# Worked recipes

Three end-to-end recipes for keeping a subject identical across new images with Nano Banana 2 (`google:4@3`). Each shows the scenario, the actual request, and the result shape. Confirm field names and the reference-image cap against the live schema (`runware-run`) before calling. Send requests as a JSON array even for a single task.

Dimension notes for `google:4@3`: `width`/`height` must be an exact supported pair, not arbitrary values. The pairs below are valid 1K sizes (1200x896 is 1K 4:3, 896x1200 is 1K 3:4). Pass `width`+`height` together, or pass `resolution` (`0.5K`/`1K`/`2K`/`4K`) instead, never both. `referenceImages` accepts a URL, a UUID from a prior generation, a data URI, or base64, between 1 and 14 entries.

## Recipe 1: Same character, new scene

Scenario: the user has one studio portrait of a red-haired woman and wants her sitting in a bookstore cafe, same face.

Anchor the identity once and spend the rest of the prompt on what changes. Do not re-describe the face from imagination.

```json
[
  {
    "taskType": "imageInference",
    "model": "google:4@3",
    "positivePrompt": "The same woman from the reference image sitting at a window table in a cozy bookstore cafe, holding a ceramic mug, warm afternoon light, shallow depth of field, candid editorial photography. Keep her face, freckles, copper-red curly hair, and mustard-yellow corduroy jacket identical.",
    "width": 1200,
    "height": 896,
    "inputs": {
      "referenceImages": [
        "https://example.com/character.jpg"
      ]
    }
  }
]
```

Result (one image, `imageUUID` always present, `imageURL` when `outputType` is `URL`):

```json
{
  "data": [
    {
      "taskType": "imageInference",
      "taskUUID": "b2c3d4e5-f6a7-8901-bcde-f23456789012",
      "imageUUID": "9d8c7b6a-5f4e-3d2c-1b0a-9e8d7c6b5a4f",
      "imageURL": "https://im.runware.ai/image/ws/2/ii/9d8c7b6a-5f4e-3d2c-1b0a-9e8d7c6b5a4f.jpg"
    }
  ]
}
```

To vary the same character (new angle, outfit, or medium), reuse the same reference and change only the scene clause. Identity lives in the face and hair, so a wardrobe or medium change does not break the likeness:

- New outfit: `"The same woman from the reference image on a mountain trail at golden hour, wearing a teal windbreaker and a small backpack, smiling, natural light, outdoor lifestyle photography. Keep her face, freckles, green eyes, and copper-red curly hair identical even though the jacket is different."`
- New medium: `"The same woman from the reference image reimagined as a stylized 3D animated character, Pixar-style render, soft global illumination, friendly expression, preserving her copper-red curly hair, freckles, green eyes, and mustard-yellow corduroy jacket."`

## Recipe 2: Lock a hidden detail with a second reference

Scenario: the user has a front shot of a denim jacket and wants a walking-away shot that shows the embroidered phoenix on the back. One reference cannot show a view it never captured, so add a back reference.

The detail carries from the reference, not the text. The prompt below never mentions the phoenix, yet it comes through because a reference shows the back.

```json
[
  {
    "taskType": "imageInference",
    "model": "google:4@3",
    "positivePrompt": "The same woman in the light-wash denim jacket walking away down a sunny tree-lined city street, seen from behind with the back of her denim jacket clearly visible, candid street photography, golden afternoon light. Keep her dark-brown hair and the denim jacket consistent.",
    "width": 896,
    "height": 1200,
    "inputs": {
      "referenceImages": [
        "https://example.com/jacket-front.jpg",
        "https://example.com/jacket-back.jpg"
      ]
    }
  }
]
```

Result:

```json
{
  "data": [
    {
      "taskType": "imageInference",
      "taskUUID": "d4e5f6a7-b8c9-0123-defa-456789012345",
      "imageUUID": "2b3c4d5e-6f7a-8b9c-0d1e-2f3a4b5c6d7e",
      "imageURL": "https://im.runware.ai/image/ws/2/ii/2b3c4d5e-6f7a-8b9c-0d1e-2f3a4b5c6d7e.jpg"
    }
  ]
}
```

Build a small reference set that covers every view your scenes will show: the front plus any side that carries detail the front cannot reveal, like a back panel or an embossed base. Nano Banana 2 takes up to 14 references and they work together.

## Recipe 3: Two locked subjects in one image

Scenario: the user wants their character holding their product, both kept identical. Pass a reference for each locked subject in the same call and the model keeps both. Name each subject by its reference position so the model maps it correctly.

```json
[
  {
    "taskType": "imageInference",
    "model": "google:4@3",
    "positivePrompt": "The woman with copper-red curly hair, freckles, and a mustard-yellow corduroy jacket from the first reference image sitting on a park bench holding the teal ceramic travel mug with a cork base and white mountain logo from the second reference image, autumn leaves around her, warm afternoon light, lifestyle photography. Keep both her identity and the mug design identical.",
    "width": 1200,
    "height": 896,
    "inputs": {
      "referenceImages": [
        "https://example.com/character.jpg",
        "https://example.com/mug.jpg"
      ]
    }
  }
]
```

Result:

```json
{
  "data": [
    {
      "taskType": "imageInference",
      "taskUUID": "e5f6a7b8-c9d0-1234-efab-567890123456",
      "imageUUID": "3c4d5e6f-7a8b-9c0d-1e2f-3a4b5c6d7e8f",
      "imageURL": "https://im.runware.ai/image/ws/2/ii/3c4d5e6f-7a8b-9c0d-1e2f-3a4b5c6d7e8f.jpg"
    }
  ]
}
```

This is the bridge to composition: each reference is held to its source while the scene around them is invented. The same approach scales to 14 references. For pulling many images into one full scene (subject plus product plus backdrop), route to `composite-scene`.
