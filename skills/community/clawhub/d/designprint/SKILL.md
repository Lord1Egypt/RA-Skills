---
name: designprint
description: "Make, design and print physical pieces for the user and have them shipped: business cards, flyers, postcards, posters, brochures, menus, invitations, stationery and tickets. Use when the user wants any of these made, designed, printed or ordered, or asks for a physical copy of a design from the conversation. Shows ready-made templates with pictures and opens the one the user picks in an editor with their own details already on it, makes two-sided business cards from a name and contact details, or prints a finished design (HTML or an image) at an exact size, and returns one link where the person pays as a guest. Works through the Designprint MCP tools when they are connected, and over plain HTTPS with curl when they are not, with no account and no API key. Not for on-screen graphics such as social posts, slides or web images. Ships within the United States only."
license: MIT
metadata:
  author: designprint
  homepage: https://thedesignprint.com
---

# Designprint

Designprint is a print shop you can use on a person's behalf. You prepare the order. The person checks the design and pays from one link. Nothing is printed and nothing is charged until they pay. Delivery is within the United States.

## What to do

| The user wants | Do this |
| --- | --- |
| Something made or printed, and has no finished design (a flyer, menu, poster, postcard, brochure, invitation, business card, letterhead, ticket) | Call `show_templates`, let them pick, then call `open_template` with their details (see "Templates"). |
| A business card made right in the chat, with nothing to open (for example on a phone) | Call `show_card_designs` with their details. It shows their card in a set of designs, each with its own order link. |
| A business card in a card design they named | Call `create_business_card` with their details. You do not design the card. |
| A change to a card you made | Call `update_business_card`. The card keeps its link. |
| A design you drew for them in this chat, which they asked for and approved | Author it as HTML at the true print size (see "Designing for print"), then call `print_design`. |
| A print of a finished image they already have | Call `print_design` with `image_url`. |
| To see a card as it is now | Call `get_business_card`. |
| To know whether the order went through | Call `check_order`. |

If you have just designed something that is meant to be physical and the user has not said how they will print it, offer once to get a proof and a price. Do not offer for on-screen work.

## Calling the tools

The server is the source of truth. Its tool list, each tool's description and each input schema say what exists right now, and the service adds tools and card designs over time. Where they differ from this page, follow the server. If a tool named here is not in the server's list, use the ones that are.

**If the Designprint tools are connected** (tools named `create_business_card`, `print_design` and so on), call them.

**If they are not connected**, call the same tools over HTTPS. There is nothing to install and no key:

```bash
curl -s -X POST https://thedesignprint.com/mcp \
  -H 'content-type: application/json' \
  -H 'accept: application/json, text/event-stream' \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"create_business_card","arguments":{"name":"Ada Lovelace","title":"Engineer","email":"ada@example.com","quantity":250,"channel":"claude-code"}}}'
```

- Both values in the `accept` header are required. Without them the answer is `406`.
- Each POST gets one JSON answer. There is no session and no setup call.
- The answer is in `result`: `content` holds the text to act on (and the proof pictures for cards), `structuredContent` holds the same facts as fields, and `isError` is true when the call failed.
- To see every tool and its current inputs, send `{"jsonrpc":"2.0","id":1,"method":"tools/list"}` the same way. Read it when you are unsure of a field. Do not guess.

Set `channel` to the name of the agent you are running in, for example `claude-code`, `codex` or `cursor`.

## Templates

This is where a new design starts.

1. Call `show_templates` with `product` and a few plain words in `about`, such as "yoga class" or "real estate agent". It returns templates, each with its title, a picture of every side and the texts it holds.
2. If the Designprint gallery is showing in the chat, the user looks and chooses there. Otherwise show the pictures from the result, with each title. Ask which one they like. Do not choose for them, and never say how many templates there are; offer more instead (`page` 2, 3 and so on, or other words in `about`).
3. Ask for the details the chosen template needs. Never invent one they did not give.
4. Call `open_template` with the `template_id` and `replacements`: for each text to change, `find` is the template's text copied exactly from the result (same letters, spaces and line breaks) and `text` is the user's own. Texts you leave out stay as the template has them, so tell the user which sample texts are left.
5. If the result lists texts that were not placed, correct them and call it again.
6. Give them the link. It opens that template in the Designprint editor with their words on it. They can change anything there, then choose quantity, paper and shipping and pay on the same site.

## Business cards in the chat

1. Ask for the person's **name** and at least one way to reach them (phone, email or website). Everything else is optional. Never invent a detail they did not give.
2. Useful inputs for the card tools: `name`, `title`, `company`, `tagline`, `phone`, `email`, `website`, `address`, `logo_url`, `accent_color` (a hex color, such as their brand color) and `quantity`.
3. **If they have not chosen a design,** call `show_card_designs`. It makes their card in a set of designs, each with its pictures, its name and its own link. If the Designprint gallery is showing in the chat, the user scrolls and chooses there: do not list the designs again and never show pictures of cards from anywhere else (web images, mockups). Otherwise list each design by name with its link. Ask which design they like, by its name. Do not choose for them, and never say how many designs there are; offer more designs instead.
4. **If they named a design,** call `create_business_card` with `style` set to it. The tool's input schema lists the designs that exist.
5. **Every change goes on the chosen card only:** call `update_business_card` with that card's link. The card keeps its link. Tell the user once that they can also edit it themselves at the edit link in the result.
6. After showing the card and after every change, end your reply with: "Want to change anything, or print it?"
7. When they say print, or ask about ordering, give them the order link (`orderUrl`) as "Click here to print". It opens checkout with that card, where they choose quantity, paper and shipping and pay as a guest. Quote prices only from the result.

Good to know:

- A logo must be an https link. If you only have a file, upload it first and use the link that comes back:
  `curl -s --data-binary @logo.png -H 'content-type: image/png' https://thedesignprint.com/v1/logos` (PNG, JPG or WebP, up to 2 MB).
- If `warnings` in the result is not empty, tell the user before you send the link. It lists what was adjusted, such as a line too long to print in full.
- To change anything afterwards, call `update_business_card` with `order` set to the order link, plus only the fields that change. An empty string takes a field off the card. This works until the card is paid for. After `show_card_designs`, use the link of the design the user picked.
- Call `create_business_card` once per card. Calling it again makes a second card with a different link.
- The person can also change the card themselves before paying, so call `get_business_card` before you answer a question about a card you made earlier.

## Designing for print

`print_design` prints one flat, single-sided page at exactly the size you give. No bleed and no margin are added, so what you author is what is cut. Write the design as one complete HTML document:

```html
<!doctype html>
<html>
<head>
<meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap" rel="stylesheet">
<style>
  html, body { margin: 0; padding: 0; width: 5in; height: 7in; }
  .sheet { width: 5in; height: 7in; box-sizing: border-box; overflow: hidden;
           position: relative; background: #F4EFE6; font-family: 'Inter', sans-serif; }
  .safe  { position: absolute; inset: 0.35in; }
</style>
</head>
<body>
  <div class="sheet"><div class="safe"> ... </div></div>
</body>
</html>
```

Rules that keep the print right:

- **Size everything in real units.** Set `html`, `body` and one wrapper to the finished width and height in inches. Use `in` and `pt` for layout and type. Do not size with `vw`, `vh` or a window width.
- **Always pass `width_in` and `height_in`**, each from 1 to 60, matching the document.
- **Keep text and logos at least 0.25 in from every edge.** Backgrounds and color blocks may run to the edge.
- **One page only.** Only the first page is printed and anything that overflows is left off. Give the wrapper `overflow: hidden` and make the content fit.
- **Styles go inside the document.** Fonts and images must be public https links (Google Fonts works) or data URIs. The whole document can be up to about 10 MB.
- **Photos need enough pixels:** about 300 per printed inch, and no less than 150.
- **One set of styles.** Do not use `@media print`, animations, or scripts that change the layout after the page loads.
- Body text should be 9 pt or larger. A poster read from across a room needs far larger type than a flyer held in the hand.

Common sizes in inches: flyer 8.5 x 11 or 5.5 x 8.5, invitation 5 x 7, small handout 4 x 6, menu 8.5 x 11 or 11 x 17, poster 11 x 17, 18 x 24 or 24 x 36.

To send HTML over HTTPS, build the request with a JSON encoder so the document is escaped correctly:

```bash
python3 - <<'PY' > print-call.json
import json
print(json.dumps({"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {
    "name": "print_design",
    "arguments": {"design_html": open("flyer.html").read(),
                  "width_in": 5, "height_in": 7, "title": "Market flyer", "channel": "claude-code"}}}))
PY
curl -s -X POST https://thedesignprint.com/mcp \
  -H 'content-type: application/json' \
  -H 'accept: application/json, text/event-stream' \
  --data-binary @print-call.json
```

After the call:

1. Open the proof picture (`previewUrl`) and look at it. If something is cut off or a font did not load, fix the HTML and call `print_design` again.
2. Tell the user the size and the price per print from the result. It is priced by printed area.
3. Give them the order link (`checkoutUrl`). They choose a quantity and shipping there and pay as a guest.

To print an image that already exists, pass `image_url` (a public PNG, JPG, WebP or SVG) with the size. The image is fitted inside the size without stretching or cropping.

## Finishing the job

- Handing over the link does not place the order. It is placed only when the person pays, so do not say it is done yet.
- When the user says they have paid, call `check_order` with the link. The job is finished when `state` is `paid`. Other states: `none` (checkout not started), `started` (opened, not paid), `failed`, `canceled`, `refunded`, `unknown` (the link matches nothing).
- Once an order exists, `check_order` also returns `statusUrl`, the person's own page for following it. Pass it on.

## Limits to say up front

- Delivery is within the United States only.
- Physical print only. Do not use this for social posts, slides or web graphics.
- `print_design` prints single-sided, one page, 1 to 60 inches on each side.
- Business cards are 3.5 x 2 inches, printed on both sides, in a set of ready-made designs.
- Every price comes from the tool results. They can change, so never state one from memory.

Full reference for every input and for the plain REST endpoints: https://thedesignprint.com/skill.md. Site index for agents: https://thedesignprint.com/llms.txt.
