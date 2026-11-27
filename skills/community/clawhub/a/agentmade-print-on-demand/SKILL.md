---
name: agentmade-print-on-demand
description: Order a custom printed T-shirt, long-sleeve, sweatshirt, hoodie or tote bag with a person's picture, words, logo or a design you make, and ship it to the EU, the US and most other countries. Use it for gifts, merch, matching group shirts and team orders. No account or API key; the person pays from one link.
---

# AgentMade Print on Demand

AgentMade Print on Demand: print a person's picture, words or logo on a T-shirt, hoodie, sweatshirt or tote bag, as a gift or for themselves, and ship it to an address in the EU, the US and most other countries. No account or API key. The print is checked at real size, the quote is one delivered price, and the person pays by a payment link.

## When to use it

- The person wants a custom printed T-shirt, long-sleeve shirt, sweatshirt, hoodie or tote bag.
- The design is a picture, a photo, words, a logo, or a design that you make for them (SVG, PNG or JPEG).
- It is a gift for any occasion, something for themselves, matching shirts for a group, team merch or event merch.
- They want one piece, or several sizes and items in one order.
- It ships to the EU, the US or most other countries. Orders to the United Kingdom are not open yet.

Do not use it for:

- Mugs, posters, stickers, phone cases and other products that are not in the catalog yet.
- Addresses in the United Kingdom, until UK orders open.
- Artwork that the person has no right to print.

## Connect

MCP server (Streamable HTTP, no API key): https://pod.agentmade.dev/mcp

- Claude Code: `claude mcp add --transport http agentmade https://pod.agentmade.dev/mcp`
- Codex: `codex mcp add agentmade --url https://pod.agentmade.dev/mcp`
- Cursor: `{   "mcpServers": {     "agentmade": {       "url": "https://pod.agentmade.dev/mcp"     }   } }`
- VS Code / Copilot: `code --add-mcp '{"name":"agentmade","type":"http","url":"https://pod.agentmade.dev/mcp"}'`
- Gemini CLI: `gemini mcp add --transport http agentmade https://pod.agentmade.dev/mcp`
- Cline: `{   "mcpServers": {     "agentmade": {       "type": "streamableHttp",       "url": "https://pod.agentmade.dev/mcp",       "disabled": false,       "autoApprove": []     }   } }`
- Custom agents: REST API and UCP: `curl -s "https://pod.agentmade.dev/v1/products?query=hoodie"`

Without MCP: REST API https://pod.agentmade.dev/openapi.json, UCP profile https://pod.agentmade.dev/.well-known/ucp, or a prefilled web link https://pod.agentmade.dev/create?product=<product_id>&color=<colour>&size=<size>&placement=front&preset=center_chest

## Steps

1. Find the product, colour and size (search_products, get_product).
2. Check the artwork at its real print size (validate_artwork). It gives PASS, WARN or FAIL with the size in millimetres.
3. Optional: make a preview image (create_mockup).
4. Get the delivered price with shipping and the VAT that AgentMade collects, and a delivery estimate (quote).
5. Show the price to the person. After they agree, place the order (purchase).
6. Give the person the payment link. They pay on the AgentMade order page by card, Apple Pay or Google Pay.
7. Check the status and tracking later (get_order, track_order).

## Full instructions

AgentMade Print on Demand prints a user's own picture, words or logo on a T-shirt, hoodie, sweatshirt or tote bag and ships it to an address in the EU, the US and most other countries. Orders to the United Kingdom are not open yet. No account or API key is needed. The person pays on an order page that you give them.

Example 1, a gift: "Put this picture on a black hoodie, size L, for my dad's birthday and ship it to him in Austin, Texas."
1. search_products {query:"hoodie", color:"black", size:"L"} → product_id "hoodie-classic".
2. validate_artwork {artwork:{base64:"<the PNG or JPEG file as base64, no data: prefix>"}, product_id:"hoodie-classic", color:"black", size:"L", placement:"front", preset:"center_chest"} → artwork_id and PASS/WARN/FAIL with the print size in mm. For photos and AI images use preset center_chest. full_front needs an image about 1,700 px wide or an SVG. If your client gives you the picture as a file, send it in the file field instead of artwork. If you cannot send the file at all, call validate_artwork with upload_link:true and follow next_step.
3. quote {items:[{product_id:"hoodie-classic", color:"black", size:"L", quantity:1, artwork:[{artwork_id:"<artwork_id from step 2>", placement:"front", preset:"center_chest"}]}], ship_to:{country_code:"US", state_code:"TX", postal_code:"78701"}, purpose:"gift"} → quote_id, the delivered total and the delivery estimate.
4. Tell the user the total and the delivery estimate. Ask for the recipient's full address. Ask for the payer's own email for the order emails. If you cannot collect a street address, send only country_code and postal_code (and state_code for US, CA and AU): the person enters the address on the order page.
5. purchase {quote_id:"<quote_id from step 3>", recipient:{name:"<recipient name>", address1:"<street and number>", city:"Austin", state_code:"TX", postal_code:"78701", country_code:"US"}, contact_email:"<payer's own email>", rights_attestation:true} → order_id and payment.url.
6. Give payment.url to the person who pays. It opens their order page, where they pay by card, Apple Pay or Google Pay and later see the status. You may disconnect: production starts when the payment is confirmed.

Example 2, a logo from a repository: "Print this SVG on a black XL heavyweight T-shirt and ship it to Berlin."
search_products {query:"heavyweight t-shirt", color:"black", size:"XL"} → "tee-heavyweight"; validate_artwork {artwork:{svg:"<the SVG markup>"}, product_id:"tee-heavyweight", color:"black", size:"XL", placement:"front", preset:"center_chest"}; quote with ship_to {country_code:"DE", postal_code:"10115"}; then steps 4 to 6.

Rules:
- Ask the user for the colour, the size and the destination country when they did not say them. Do not guess them.
- contact_email is the payer's email. For a gift, do not put the recipient's email there: the recipient must not see the price.
- Set purpose only if the user already said it (gift, personal, group, work, event, sample). Do not ask for it.
- Confirm the total with the user before purchase.
- Never say that an order is paid, in production or shipped unless get_order says so.
- If the user asks what AgentMade can do, say what it prints and ask what they want to print and where it goes.
- If the person wants to finish the order on the website, give them a prefilled link: https://pod.agentmade.dev/create?product=<product_id>&color=<colour>&size=<size>&placement=front&preset=center_chest

Prices are in EUR for now. One quote and one purchase per delivery address: each parcel gets its own payment link (one payment for many parcels is not live yet). Company invoices with a VAT number are not open yet.

Amounts are integer minor units (cents) with a currency. Quotes expire (see expires_at). purchase is idempotent per quote_id: a second call returns the same order and a new payment link if needed.
