---
name: bring-photo-mcp
description: Turn product photos into verified Bring! list items via MCP.
version: 1.0.3
author: Thomas Schnuecker
metadata:
  mcp_server: bring-photo-mcp
  version: 1.0.3
  hermes:
    tags: [bring, shopping-list, photos, mcp]
    related_skills: [bring-shopping-lists]
  openclaw:
    requires:
      env:
        - BRING_EMAIL
        - BRING_PASSWORD
        - BRING_DEFAULT_LIST
        - BRING_ALLOWED_LISTS
      bins:
        - bring-photo-mcp
    primaryEnv: BRING_EMAIL
    envVars:
      - name: BRING_EMAIL
        required: true
        description: Bring account email address.
      - name: BRING_PASSWORD
        required: true
        description: Bring account password; store only in a secret store.
      - name: BRING_DEFAULT_LIST
        required: true
        description: Default list name.
      - name: BRING_ALLOWED_LISTS
        required: true
        description: Comma-separated allowlist of writable lists.
      - name: BRING_LOCALE
        required: false
        description: Bring catalog locale; defaults to de-DE.
    install:
      - kind: node
        package: bring-photo-mcp
        bins: [bring-photo-mcp]
---

# Bring Photo MCP

Show an AI agent a package, label, or product photo and say: **"Add this to my shopping list."** This skill guides the agent from visible product details through Bring! catalog classification to a verified list entry with the matching icon, category, and optional original photo.

## When to Use

Use this skill primarily when a product should be added to Bring! from a photo. It also covers safe catalog search, ordinary list operations, photo attachment, and verified writes.

## Boundary

- Perform deterministic list operations exclusively through the `bring_*` MCP tools provided by this server.
- Do not construct, replay, inspect, or send raw Bring HTTP requests. Do not use browser automation, shell commands, or a second Bring client for operations covered by these tools.
- Never expose credentials, list IDs, item-detail UUIDs, image paths, or photo bytes in conversation output.
- Treat every tool response as authoritative for the operation it reports. Do not infer success from intent.

## Photo-led registration workflow

1. Analyse the supplied product photo locally in the conversation. Extract only purchase-relevant facts: visible product name, brand, variant, amount, and ambiguity. If the image is unreadable or ambiguous, ask for clarification; do not write.
2. Search the configured locale catalog with `bring_search_catalog({ query, locale?, limit? })` using the visible main name first, then specific-to-general terms if needed.
3. Decide catalog versus free text:
   - For an exact catalog product, use the catalog main name and its returned icon/category pair.
   - For a product that is not an exact catalog item, retain an identifying free-text `item_name`, but select an explicitly returned catalog icon/category pair.
   - Never assume `Eigene Artikel` is a valid API category.
4. If the catalog search does not make the classification clear, call `bring_suggest_classification({ product_name, hints?, locale? })`. A response with insufficient confidence is a no-write result: present candidates or ask for clarification.
5. Compose `specification` at no more than 30 Unicode code points. Do not repeat the main/catalog name. Prefer `brand + distinguishing variant + amount`, keeping the product identifiable. If a required fact is not visible, do not invent it.
6. Enforce the hard icon/category invariant: every `bring_add_item` call must contain `icon_item_id` and `category_id` from the same valid catalog entry. No create, copy, or move is successful without verified persisted icon and category.
7. Call `bring_add_item({ lists, item_name, specification, icon_item_id, category_id, image_path?, duplicate_policy })`. Add `image_path` only when the user supplied a permitted local photo path.
8. Report the returned persisted fields and verification evidence per list, without repeating sensitive identifiers or local paths.

## Duplicate policy and idempotency

- Use `duplicate_policy=fail` by default. An ambiguous existing item is an explicit no-write result, not a reason to overwrite.
- Use `duplicate_policy=update_exact` only when the intended existing item has exactly the same item identity and specification.
- Repeated identical requests should converge on one verified item per target list. Never silently overwrite another active item with a generic shared name.

## Photo operations

- Use `bring_attach_photo`, `bring_replace_photo`, or `bring_remove_photo` only for a confirmed target item.
- Trust success only when the tool returns its read-back verification (`imageUrl` present after add/replace; absent after removal).
- For images supplied as a conversation attachment rather than a local path, obtain an approved local path through the host workflow before calling a photo tool; do not fabricate a path.

## Copy and move

- For copies, call `bring_copy_item({ source_list, target_lists, item_name, include_photo })`. Metadata must remain catalog-valid; the source remains unchanged.
- For moves, call `bring_move_item({ source_list, target_list, item_name, include_photo })`. The target must be completely verified before the source is removed. If target creation or verification fails, report failure and leave the source untouched.
- For every multi-target add or copy, enumerate the per-list results. If any result fails and any succeeds, report `status: "partial"`; never call it total success. For all failures, report `status: "error"` with stable error codes.

## Other deterministic operations

- Discover allowed lists with `bring_list_lists` and inspect them with `bring_list_items`.
- Verify an existing item with `bring_get_item` before a sensitive follow-up operation.
- Use `bring_check_item`, `bring_uncheck_item`, and `bring_remove_item` only on the confirmed requested list and item.

## Safe response shape

For writes, state: requested operation, overall status, then one concise result per list (success/partial/error, stable error code when present, and non-sensitive verification evidence). State clearly when no write was performed due to ambiguity, insufficient classification confidence, or duplicate policy.
