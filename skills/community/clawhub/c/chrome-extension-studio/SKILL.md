---
name: chrome-extension-studio
description: Design, prototype, build, QA, and ship Chrome extensions across separate plugin, template, and product repos with explicit publish lanes.
---

# Chrome Extension Studio

Use this skill when the task is to design, prototype, build, package, QA, or ship a Chrome extension and the workflow needs to stay clean across multiple repositories.

## Core model

- Plugin repo: workflow instructions, validation, and orchestration only
- Template repo: reusable MV3 starter and release contract
- Product repo: one extension per repo

Do not collapse those roles into one repo.

## Publish lanes

- `prototype-local`
- `beta-private`
- `cws-public`
- `source-release`

Every product repo must declare exactly one lane in `extension.release.json`.
Every product repo should keep structured `design` metadata in `extension.release.json` as the source of truth for the brief.
Every product repo should also keep `docs/release-plan.md` generated from that profile.
Every product repo should keep `docs/extension-brief.md` product-specific, not as a generic template.
Every product repo should keep `docs/store-listing.md` generated from structured listing metadata in the profile.

## Required files in each product repo

- `extension.release.json`
- `docs/extension-brief.md`
- `docs/store-listing.md`
- `docs/qa-checklist.md`
- `docs/release-plan.md`

## Workflow

1. Confirm the target product repo and its current publish lane.
2. If the repo does not exist yet, create it from the separate template repo:

```bash
python3 ../../scripts/create_product_repo.py "My Extension" --publish-type prototype-local --git-init
```

3. Write or update the product brief before changing code.
4. Keep permissions, host matches, and store copy intentionally narrow.
5. Build the extension package inside the product repo, not inside the plugin repo.
6. Regenerate `docs/store-listing.md` and `docs/release-plan.md` after release-profile changes.
7. Run the local release cycle before recommending any ship step.
8. Validate the release contract before recommending any ship step.

## Validation

Run the validator from the plugin repo against the product repo profile:

```bash
python3 ../../scripts/validate_release_profile.py /path/to/product-repo/extension.release.json
```

Generate or refresh the release plan:

```bash
python3 ../../scripts/generate_release_plan.py /path/to/product-repo/extension.release.json
```

Generate or refresh the store-listing draft:

```bash
python3 ../../scripts/generate_store_listing.py /path/to/product-repo/extension.release.json
```

Generate or refresh the design brief:

```bash
python3 ../../scripts/generate_design_brief.py /path/to/product-repo/extension.release.json
```

Run the local release-preparation cycle:

```bash
python3 ../../scripts/execute_release_cycle.py /path/to/product-repo/extension.release.json
```

## Guardrails

- Do not publish a local prototype through the public lane.
- Do not store Chrome Web Store metadata only in chat; keep it in repo docs.
- Do not reuse one product repo for multiple unrelated extensions.
- Do not change publish type silently; update `extension.release.json` first.
