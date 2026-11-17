---
name: autoprint
description: "Print existing artwork on custom wall art, apparel, and gifts. Use it for print design through AutoPrint's MCP server."
---

# AutoPrint

Print existing artwork on custom wall art, apparel, and gifts.

## Connect

Add AutoPrint's MCP server: https://autoprintstudio.com/mcp (Streamable HTTP, no sign-in).

## Offers

### Print design

Prepares existing artwork or photos for printing on wall art, apparel, or personalized gifts. Requires artwork_url, a public HTTPS image link, and idea, the desired printed product, size, or style. Imports the supplied image without generating or changing artwork. Recommends a product and returns the artwork with a studio link to preview the product, choose a size, and order on AutoPrint's website. The tool does not generate images, place orders, or take payment.

1. Call `start_design`. It returns an id.
2. Call `check_design` with the id until it is ready; it usually takes under a minute.
3. Give the person the result and its link.
