---
name: claw-pet
description: >
  Catch a pet or loot item by calling a configured remote pet backend API. Use when the user asks to catch a pet,
  fish for loot, try their luck, or trigger a remote catch action. Supports configured API calls, result formatting,
  and clear handling for pet, item, empty, and error responses.
---

# Claw Pet

Use this skill when a user wants you to trigger a remote `catch` action against a pet backend that they control.

## Workflow

1. Load runtime config from environment variables first, then local `_meta.json`.
2. Verify `CATCH_API_URL` and `API_KEY` are present.
3. Send a `POST` request with JSON body `{"action":"catch"}`.
4. Parse the response and classify it as one of:
   - `pet`
   - `item`
   - `empty`
   - `error`
5. Return a friendly summary without exposing secrets.

## Configuration

Provide these values before use:

1. Environment variables:
   - `CATCH_API_URL`
   - `API_KEY`
2. Or skill-local `_meta.json` for development/testing

Keep `_meta.json` free of production secrets before sharing or publishing the skill.

## Expected Backend Behavior

The backend should:
- accept `POST` requests to `CATCH_API_URL`
- authenticate with `Authorization: Bearer <API_KEY>`
- return JSON only
- return either a pet result, item result, empty result, or structured error

Read `references/api.md` for the response contract.

## Trigger Examples

This skill should trigger for requests such as:
- "去抓一只宠物"
- "Catch me a pet"
- "Try to fish"
- "Go catch something for me"
- "帮我抽一下今天的宠物"

## Script

Use `scripts/catch_pet.py` for the actual API call. Prefer the script over re-implementing the request flow inline.

## Output Rules

- If a pet is caught, include rarity, name, level, and any short flavor text.
- If an item is caught, include item name, rarity, quantity, and description if present.
- If nothing is caught, say so plainly.
- If the backend returns an error or malformed payload, explain the failure category briefly.

## Publish Notes

This skill is only the agent-side caller. It does not bundle the backend service.
Users who install it must configure their own reachable backend endpoint and API key.
