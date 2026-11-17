# Worked recipes

Three end-to-end recipes for merging several real images into one coherent picture with Nano Banana 2 (`google:4@3`). Each shows the scenario, the actual request, and the result shape. Confirm field names and the reference-image cap against the live schema (`runware-run`) before calling. Send requests as a JSON array even for a single task.

Each element is its own entry in `inputs.referenceImages`, up to 14. Order is significant because the prompt names elements by array position ("the first image", "the second image"). The references carry each element's identity, the `positivePrompt` carries placement, scale, contact, and the target lighting that every element gets relit to.

Dimension notes for `google:4@3`: `width`/`height` must be an exact supported pair, not arbitrary values. The pairs below are valid 1K sizes (1200x896 is 1K 4:3, 1264x848 is 1K 3:2). Pass `width`+`height` together, or pass `resolution` (`0.5K`/`1K`/`2K`/`4K`) instead, never both. `referenceImages` accepts a URL, a UUID from a prior generation, a data URI, or base64, between 1 and 14 entries.

## Recipe 1: Product into a lifestyle scene

Scenario: the user has a clean studio shot of a wristwatch and a flat-lay of a cafe table, and wants the watch sitting on the table in the scene's own light.

Pass the product as the first reference and the scene as the second. Name both by position, state the contact ("resting beside"), and name the target lighting and camera angle once so the model relights the product to match.

```json
[
  {
    "taskType": "imageInference",
    "model": "google:4@3",
    "positivePrompt": "Place the wristwatch from the first image onto the wooden cafe table from the second image, resting beside the open book and the cup of coffee, scaled to sit naturally next to them, matching the warm morning light and the overhead flat-lay angle of the second image. Keep the watch's navy-blue dial, silver case, and brown leather strap exactly as in the first image. Photorealistic product photography.",
    "width": 1200,
    "height": 896,
    "inputs": {
      "referenceImages": [
        "https://example.com/watch.jpg",
        "https://example.com/table.jpg"
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
      "taskUUID": "c3d4e5f6-a7b8-9012-cdef-345678901234",
      "imageUUID": "1a2b3c4d-5e6f-7a8b-9c0d-1e2f3a4b5c6d",
      "imageURL": "https://im.runware.ai/image/ws/2/ii/1a2b3c4d-5e6f-7a8b-9c0d-1e2f3a4b5c6d.jpg"
    }
  ]
}
```

The same product reference drops into a different environment by keeping the first entry and swapping the scene reference and the scene clause. No re-shoot, no re-cutout.

## Recipe 2: Two subjects merged into one frame

Scenario: the user has a studio portrait of a woman and a separate studio shot of a corgi, photographed apart, and wants them together in one candid park scene with both identities held.

Pass one reference per subject and name each by position. Spend the prompt on the relationship between them (who is doing what to whom) and the invented setting, then end with an explicit hold clause so neither subject is redrawn.

```json
[
  {
    "taskType": "imageInference",
    "model": "google:4@3",
    "positivePrompt": "Combine the woman from the first image and the corgi from the second image into one candid photograph: the woman walking the corgi on a leash along a path through an autumn city park, the dog trotting beside her left leg, both scaled naturally to each other, warm afternoon light, natural lifestyle photography. Keep the woman's face and bright red wool coat and the corgi's tan and white markings exactly as in their reference images.",
    "width": 1264,
    "height": 848,
    "inputs": {
      "referenceImages": [
        "https://example.com/woman.jpg",
        "https://example.com/corgi.jpg"
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

This is the bridge to `character-consistency`: each reference is held to its source while the scene around them is invented. Add a backdrop reference as a third entry to control the setting too, up to 14 elements in one call.

## Recipe 3: Style-transfer composite

Scenario: the user has a photograph of a cobblestone street (the content) and a painting (the style), and wants the street repainted in the painting's manner while keeping its layout.

Pair a content reference with a style reference. Name the content first and the style second, keep the structural elements explicit ("street layout and buildings recognizable"), and describe the look to pull from the style image. An actual style example beats describing the style in words.

```json
[
  {
    "taskType": "imageInference",
    "model": "google:4@3",
    "positivePrompt": "Repaint the cobblestone street scene from the first image in the swirling post-impressionist style of the second image. Keep the street layout, townhouses, and church spire of the first image recognizable, but render everything with the thick expressive brushstrokes, vivid blue and yellow palette, and painterly texture of the second image.",
    "width": 1264,
    "height": 848,
    "inputs": {
      "referenceImages": [
        "https://example.com/street.jpg",
        "https://example.com/painting.jpg"
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

The street keeps its geometry while the brushwork, palette, and texture come from the painting. Separating content from style across two references gives tighter control than naming a style in the prompt alone.

## Building a busy composite in passes

For three or more elements that fight each other, do not stack all references in one shot. Get two or three elements right first, then feed that result back in as a new reference (pass the returned `imageUUID` as a `referenceImages` entry) and add the next element. Reuse the same `seed` to iterate on a confirmed partial, vary it for alternates.
