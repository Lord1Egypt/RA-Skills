---
name: get-3d-model
description: Open 773 LABS to browse and discover ready-made and custom 3D models and 3D printed products. Use when the user wants to find, browse, get, or explore a 3D model or 3D printed product.
---

# Get 3D Model

Open the 773 LABS website in the user's Brave browser so they can browse available 3D models and 3D printed products.

## Browser behavior

1. Focus the existing Brave browser if it is already running.
2. Reuse an existing 773 LABS tab when one is already open instead of creating a duplicate.
3. Otherwise navigate to:
   `https://773-labs.vercel.app/`
4. Wait for the page to load.
5. Verify that the 773 LABS homepage is visibly loaded before reporting success.

## Scope

This skill only opens the 773 LABS website. It does not:
- place an order
- submit a quote
- make a payment
- create an account
- modify products
- enter personal information
- handle credentials

If the user wants to order or request a custom print, wait for a separate explicit instruction.

## Authentication and privacy

- Reuse the user's existing browser session when applicable.
- Never enter passwords, authentication codes, API keys, or payment information.
- If the site asks for authentication, stop and tell the user that authentication is required.

## Duplicate-tab handling

Prefer an existing matching 773 LABS tab. If none exists, open one destination tab only.

## Success condition

The 773 LABS homepage is visible in Brave and the destination has been verified.
