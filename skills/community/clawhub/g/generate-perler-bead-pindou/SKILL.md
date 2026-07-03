---
name: "generate-perler-bead-pindou"
description: "Generate 2D Pixelization Perler Beads Pindou Patterns from user text prompt and references images. Will return a list of Perler Beads/Pindou Brands Codes as well as an workspace url to render the instruction images that are useful for Perler Beads and Pindou Hobbist..."
env:
  DEEPNLP_ONEKEY_ROUTER_ACCESS:
    required: false
    description: Onekey Gateway Registered API and Usage access key
dependencies:
  node: []
  python: []
---


# generate-perler-bead-pindou from craftsman-agent 

Auto-generated skill for OneKey Agent Gateway registered agent `craftsman-agent/craftsman-agent` and API id `generate_perler_bead_pindou` based on its `api_list` from registered API metas. Available 
to use in CLIs, Skills, Rest APIs, and more agent preferred formats. The online perler beads pindou web address is https://craftsman-agent.aiagenta2z.com/app/pindou_perler_bead.
And you can also find gallery of Perler Beads in https://craftsman-agent.aiagenta2z.com/gallery.

<img src="https://craftsman-agent.aiagenta2z.com/static/DerekZZ/8bf621c1-1ccd-42aa-98bf-96c5ee978bad/74fcd12d59464c569c13e2428316a7ab.png" alt="Craftsman-agent Perler Beads for Minecraft Diamond Pickaxes" width="500" />

| Section               | Description                                      |
|-----------------------|--------------------------------------------------|
| Craftsman Website     | https://craftsman-agent.aiagenta2z.com           |
| Craftsman App         | https://craftsman-agent.aiagenta2z.com/app       |
| Craftsman Gallery     | https://craftsman-agent.aiagenta2z.com/gallery   |
| Craftsman Workspace   | https://craftsman-agent.aiagenta2z.com/workspace |
| Craftsman Marketplace | https://craftsman-agent.aiagenta2z.com/marketplace |


## Quick Start
Set the API providers access key `DEEPNLP_ONEKEY_ROUTER_ACCESS` or the registered OneKey Gateway access key DEEPNLP_ONEKEY_ROUTER_ACCESS from AI Agent Marketplace.

```bash
export DEEPNLP_ONEKEY_ROUTER_ACCESS=YOUR_REGISTRY_KEY
```

Run an API via scripts:
- Node (JS): `node scripts/generate_perler_bead_pindou.js --data '{"key":"value"}'`
- Python: `python3 scripts/generate_perler_bead_pindou.py --data '{"key":"value"}'`


## APIs
### `generate_perler_bead_pindou`
Generate Perler Bead Pindou Pattern From Text Prompt and Reference Images

- Method: `POST`
- Endpoint: `https://craftsman-agent.aiagenta2z.com/craftsman-agent/api/v1/generate_perler_bead_pindou`

#### Parameters

| Name    | Description                                                    |
|---------|----------------------------------------------------------------|
| prompt  | Text Prompt of which image to generate the Pindou Perler Beads |
| images  | A List of URL of Images to process                             |
| width | The width of the outcome board, e.g. 16 for an 16 x 16 boards  |
| height | The height of the outcome board, e.g. 16 for an 16 x 16 boards |
| brand | Option Values of default,mard,artkal,perler,hama               |


```example results
{
    "prompt":"",
    "images":[
      "https://minecraft.wiki/images/Diamond_Pickaxe_JE3_BE3.png?7409d="
    ],
    "width":16,
    "height":16,
    "brand": "default"
  }
}
```

The generated images can be found in 
https://craftsman-agent.aiagenta2z.com/static/DerekZZ/8bf621c1-1ccd-42aa-98bf-96c5ee978bad/74fcd12d59464c569c13e2428316a7ab.png


Example: Process the minecraft diamond pickaxe and generate a 16 by 16 perler bead Pindou Pattern,
the image url is : https://minecraft.wiki/images/Diamond_Pickaxe_JE3_BE3.png?7409d=
And the access key can be found in [DeepNLP Router Access Keys Generation](https://www.deepnlp.org/workspace/keys)

#### Curl
```bash
export DEEPNLP_ONEKEY_ROUTER_ACCESS=your_access_key

curl -X POST "https://agent.deepnlp.org/agent_router" \
-H "Content-Type: application/json" \
-H "X-OneKey: $DEEPNLP_ONEKEY_ROUTER_ACCESS" \
-d '{
  "unique_id": "craftsman-agent/craftsman-agent",
  "api_id": "generate_perler_bead_pindou",
  "data": {
    "prompt":"",
    "images":[
      "https://minecraft.wiki/images/Diamond_Pickaxe_JE3_BE3.png?7409d="
    ],
    "width":16,
    "height":16,
    "brand": "default"
  }
}'
```

#### Expected Results

```commandline
{"success":true,"palette":{"A1":{"color_name":"white","color_css":"#FFFFFF"},"A2":{"color_name":"cream","color_css":"#F7E7CE"},"A3":{"color_name":"yellow","color_css":"#FFD400"},"A4":{"color_name":"orange","color_css":"#FF8C00"},"A5":{"color_name":"red","color_css":"#D62828"},"A6":{"color_name":"pink","color_css":"#FF69B4"},"A7":{"color_name":"purple","color_css":"#7B2CBF"},"A8":{"color_name":"light_blue","color_css":"#87CEEB"},"A9":{"color_name":"blue","color_css":"#2563EB"},"A10":{"color_name":"dark_blue","color_css":"#1E3A8A"},"A11":{"color_name":"mint_green","color_css":"#98FB98"},"A12":{"color_name":"green","color_css":"#22C55E"},"A13":{"color_name":"dark_green","color_css":"#166534"},"A14":{"color_name":"tan","color_css":"#D2B48C"},"A15":{"color_name":"brown","color_css":"#8B4513"},"A16":{"color_name":"dark_brown","color_css":"#4E342E"},"A17":{"color_name":"light_gray","color_css":"#D1D5DB"},"A18":{"color_name":"gray","color_css":"#9CA3AF"},"A19":{"color_name":"dark_gray","color_css":"#4B5563"},"A20":{"color_name":"black","color_css":"#111827"},"B1":{"color_name":"gold","color_css":"#FFD700"},"B2":{"color_name":"mustard","color_css":"#E1C16E"},"B3":{"color_name":"burnt_orange","color_css":"#C86B3E"},"B4":{"color_name":"dark_tan","color_css":"#9E643D"},"B5":{"color_name":"brick_red","color_css":"#8C372C"},"B6":{"color_name":"deep_red","color_css":"#A50034"},"B7":{"color_name":"pink_magenta","color_css":"#DA1884"},"B8":{"color_name":"violet","color_css":"#9B2BDC"},"B9":{"color_name":"lavender","color_css":"#B57EDF"},"B10":{"color_name":"light_lavender","color_css":"#D4B1E3"},"C1":{"color_name":"lime","color_css":"#ADFF2F"},"C2":{"color_name":"bright_green","color_css":"#73D33C"},"C3":{"color_name":"kelly_green","color_css":"#22C55E"},"C4":{"color_name":"forest_green","color_css":"#116530"},"C5":{"color_name":"grass_green","color_css":"#56BA9F"},"C6":{"color_name":"teal","color_css":"#008080"},"C7":{"color_name":"turquoise","color_css":"#40E0D0"},"C8":{"color_name":"sky_blue","color_css":"#87CEEB"},"C9":{"color_name":"azure","color_css":"#007FFF"},"C10":{"color_name":"navy_blue","color_css":"#1E3A5F"},"D1":{"color_name":"peach","color_css":"#EEBAB2"},"D2":{"color_name":"salmon","color_css":"#FF9E9D"},"D3":{"color_name":"coral","color_css":"#FF6D6A"},"D4":{"color_name":"pearl_pink","color_css":"#FFD1DC"},"D5":{"color_name":"pearl_green","color_css":"#84B791"},"E1":{"color_name":"skin_light","color_css":"#F8E0CC"},"E2":{"color_name":"skin_med","color_css":"#F0C8A0"},"E3":{"color_name":"skin_tan","color_css":"#D4B1E3"},"E4":{"color_name":"skin_brown","color_css":"#A67B5B"},"E5":{"color_name":"tan_dark","color_css":"#8B5A2B"},"F1":{"color_name":"rose","color_css":"#FFB3B3"},"F2":{"color_name":"pink_light","color_css":"#F7CED7"},"F3":{"color_name":"pink_dark","color_css":"#E10600"},"F4":{"color_name":"violet_light","color_css":"#BC8F8F"},"F5":{"color_name":"violet_dark","color_css":"#604089"},"F6":{"color_name":"brown_violet","color_css":"#7E582C"},"F7":{"color_name":"magenta_violet","color_css":"#72408E"},"G1":{"color_name":"cream_opaque","color_css":"#FFFDD0"},"G2":{"color_name":"light_pearl","color_css":"#E0DEE9"},"G3":{"color_name":"pearl_olive","color_css":"#84B791"},"G4":{"color_name":"pearl_lavender","color_css":"#DFC1E2"},"G5":{"color_name":"pearl_blue","color_css":"#BAD7F2"},"H1":{"color_name":"gray_very_light","color_css":"#ECECED"},"H2":{"color_name":"gray_light","color_css":"#D1D1D1"},"H3":{"color_name":"gray_mid","color_css":"#9B9B9B"},"H4":{"color_name":"gray_dark","color_css":"#767777"},"H5":{"color_name":"charcoal","color_css":"#484949"},"H6":{"color_name":"graphite","color_css":"#2E2F31"},"H7":{"color_name":"black","color_css":"#000000"}},"grid":{"width":16,"height":16,"cells":[["H7","H7","H7","H7","H7","H7","H7","H7","H7","H7","H7","H7","H7","H7","H7","H7"],["H7","H7","H7","H7","H7","H7","H7","H7","H7","H7","H7","H7","H7","H7","H7","H7"],["H7","H7","H7","H7","H7","H7","A13","A13","A13","A13","H6","H7","H7","H7","H7","H7"],["H7","H7","H7","H7","H7","H6","C5","C6","C6","C6","C6","A13","A16","A16","H7","H7"],["H7","H7","H7","H7","H7","H7","H6","A20","A20","H6","C6","C5","F6","H6","H7","H7"],["H7","H7","H7","H7","H7","H7","H7","H7","H7","H7","H5","C5","C6","H6","H7","H7"],["H7","H7","H7","H7","H7","H7","H7","H7","H7","A16","A16","H6","C6","C6","A20","H7"],["H7","H7","H7","H7","H7","H7","H7","H7","A16","F6","H6","H7","H6","C6","A20","H7"],["H7","H7","H7","H7","H7","H7","H7","A16","A16","H6","H7","H7","A20","C6","A20","H7"],["H7","H7","H7","H7","H7","H7","A16","F6","H6","H7","H7","H7","A20","C6","A20","H7"],["H7","H7","H7","H7","H7","A16","A16","H6","H7","H7","H7","H7","A20","C6","A20","H7"],["H7","H7","H7","H7","A16","F6","H6","H7","H7","H7","H7","H7","H7","A20","H7","H7"],["H7","H7","H7","A16","A16","H6","H7","H7","H7","H7","H7","H7","H7","H7","H7","H7"],["H7","H7","A16","F6","H6","H7","H7","H7","H7","H7","H7","H7","H7","H7","H7","H7"],["H7","H7","A20","A20","H7","H7","H7","H7","H7","H7","H7","H7","H7","H7","H7","H7"],["H7","H7","H7","H7","H7","H7","H7","H7","H7","H7","H7","H7","H7","H7","H7","H7"]]},"statistics":{"total_beads":256,"unique_colors":9,"color_counts":{"H7":188,"A13":5,"H6":15,"C5":3,"C6":12,"A16":14,"A20":13,"F6":5,"H5":1}},"blueprint":{"show_coordinates":true,"show_color_code":true,"show_grid_lines":true,"cell_size":20},"final_image_url":"","session_id":"","workspace_session_id":"","title":"","tag_list":""}
```

And the references Perler Beads or Pindou Pattern images can be found from the result with key `share_url`

`share_url`: https://craftsman-agent.aiagenta2z.com/app/sessions/share/547083a4-5e38-4e4e-ba78-300cadb88b11

It will show a board of pixelization of Perler Beads and you can make modification from the results, choose color from Pallet of
various brands, such as MARD,Perler,Coco,etc. 'Export Design Image' 

#### Scripts
```bash
node scripts/generate_perler_bead_pindou.js --data '{"prompt":"","images":["https://minecraft.wiki/images/Diamond_Pickaxe_JE3_BE3.png?7409d="],"width":16,"height":16,"brand":"default"}'
python3 scripts/generate_perler_bead_pindou.py --data '{"prompt":"","images":["https://minecraft.wiki/images/Diamond_Pickaxe_JE3_BE3.png?7409d="],"width":16,"height":16,"brand":"default"}'
```


### Scripts

Each API has a dedicated script in `scripts/`:
```bash
node scripts/<api_name>.js --data '{"prompt":"","images":["https://minecraft.wiki/images/Diamond_Pickaxe_JE3_BE3.png?7409d="],"width":16,"height":16,"brand":"default"}'
python3 scripts/<api_name>.py --data '{"prompt":"","images":["https://minecraft.wiki/images/Diamond_Pickaxe_JE3_BE3.png?7409d="],"width":16,"height":16,"brand":"default"}'
```

### CLIs

```shell
npx onekey agent craftsman-agent/craftsman-agent generate_perler_bead_pindou '{"prompt":"","images":["https://minecraft.wiki/images/Diamond_Pickaxe_JE3_BE3.png?7409d="],"width":16,"height":16,"brand":"default"}'
```


## References
- `reference/api_list.json`: original `api_list` payload
- `reference/api_meta.json`: normalized API metadata used by scripts
