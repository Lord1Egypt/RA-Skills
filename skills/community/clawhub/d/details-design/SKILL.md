---
name: details-design
description: Find and inspect curated website references or reusable components when the user asks to use Details.so, a Details inspiration URL, or the Details Vault.
---

# Use Details design references

Use the connected Details MCP server. If its tools are unavailable, direct the user to the [Details setup guide](https://www.details.so/mcp). An eligible Details account signs in through OAuth.

- For a design brief such as “playful hero sections,” use `search_inspirations`. Keep the requested visual detail in the query. Include business or audience context only when known. Show the returned options with their Details links and let the user choose, unless they asked you to pick.
- For a specific Details inspiration URL or a result the user selected, pass its ID or slug to `get_inspiration`. Inspect the image or ordered motion frames. If the user wants to implement the detail, use the file paths and bundle ID returned for that reference to read the relevant evidence with `read_inspiration_source` or `read_inspiration_bundle`. Identify any missing evidence before making claims about the implementation.
- When the user explicitly wants a reusable Vault component, use `search_vault`. For the selected result, call `get_vault_resource` with `content=implementation` and adapt its instructions to the user's project.

Tool calls record usage. If Details returns an access or allowance error, relay it and link to the setup guide. Keep browsing requests focused on the references until the user asks for implementation.
