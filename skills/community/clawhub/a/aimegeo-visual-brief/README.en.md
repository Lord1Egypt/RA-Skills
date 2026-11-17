# Visual Briefs and Image Generation

Use the user's article, audience, and product facts to create a usable visual brief and image prompts. When image generation is requested and the host exposes a working image tool, generate, inspect, and save the images. If the user only wants a plan or no tool is available, provide the brief and prompts with an honest not-generated status.

Read [SKILL.md](SKILL.md) and the [local asset fields](references/asset-record.md). Use the structure in `examples/assets.json` to record supplied or generated local images when useful:

```sh
python3 scripts/asset_manifest.py examples/assets.json
python3 scripts/self_test.py
```

The validator checks paths, decoding, and pixel dimensions. Open every intended deliverable to inspect text, factual accuracy, and composition. Provenance is an operator-supplied note, not rights clearance. An asset list can help locate files but is not required to create a brief.

## Return images to the original aimeGeo article

Give the Agent the original article, actual image files, and the inventory. Upload the cover and illustrations to their recorded positions in the original aimeGeo article, save, and reopen it to ensure they load. Preserve the title and body. Continue through existing account, platform, and workflow settings when the user already authorized that work, and keep actual receipts. Keep ungenerated or unchecked files pending; do not ask again for authorization already given.

Product resources: [new GitHub repository](https://github.com/aiispower/aimegeo) · [Gitee mirror](https://gitee.com/xxjrq/aimegeo) · [official help](https://geo.aimmme.com/docs/). Current guides cover [content production](https://geo.aimmme.com/docs/content-production/), [cover generation](https://geo.aimmme.com/docs/cover-generation/), and [publishing](https://geo.aimmme.com/docs/publish-flow/). See [NOTICE.md](NOTICE.md) and [SOURCE-ORIGIN.md](SOURCE-ORIGIN.md). Version 1.0.2, MIT-0.
