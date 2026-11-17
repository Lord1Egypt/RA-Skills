---
name: astro-sync
description: >
  Convert and polish a Markdown article into AstroPaper-compatible post format
  for the astro_journal blog (everbox.io). Use when the user wants to publish
  or sync an article (e.g. from ai-thoughts/docs/ or history/docs/) to the Astro blog,
  convert Markdown to Astro format, add AstroPaper frontmatter, or move images into
  src/assets/images/.
---

# Astro Sync

Convert a polished Markdown draft into a ready-to-publish AstroPaper post in the `astro_journal` repo (`/home/jeff/pool/git/astro_journal`), copying and rewriting image references to match the blog's conventions.

## Approval gate — read before anything else

- **Never sync, write, or publish anything without explicit user approval.** This skill converts on demand only; it does not run automatically.
- The **user decides which article** is ready to sync and publish (from `ai-thoughts` or `history` to `astro_journal`) and **points it out explicitly**. Do not guess, propose candidates, or sync articles on your own.
- When the user names an article, still confirm the plan (target category, draft/featured, tags) before writing to the blog repo.
- **Never commit or push without explicit user approval.** After writing the post, ask for go-ahead first; only then stage the post + new images, commit, and push. The blog repo (`astro_journal`) has a single remote `origin`.

## Blog conventions (source of truth: astro_journal/AGENTS.md)

- Posts live in `src/data/blog/<category>/` — categories: `tech`, `travel`, `photo`, `philosophy`, `culture`. **Not** `src/content/`.
- Filenames: `yymmdd-lowercase-slug.md` — 6-digit date prefix, lowercase, hyphens only. No underscores, camelCase, or 10-digit timestamps.
- URLs derive from the filename; never hardcode `/posts/...` links.
- **Cross-links to other articles use absolute GitHub URLs on `j3ffyang`.** A relative link such as `261108-hermes-guest-hardening.md` is resolved by the browser against the post URL, producing `/posts/<category>/<slug>/261108-hermes-guest-hardening.md` — a path the build never creates, because `dist` holds `<slug>/index.html` and zero `.md` files. Publishing the target does not fix it; the path itself is wrong. Write `https://github.com/j3ffyang/ai-thoughts/blob/main/docs/<file>` instead.
- Frontmatter follows the AstroPaper schema (see below).
- Images live in `src/assets/images/`, referenced by literal relative path `../../../assets/images/<file>` from a post in `src/data/blog/<category>/`.
- Renaming a **published** post requires adding a redirect (old URL → new URL) to `postRedirects` in `astro.config.ts`.
- `.orig` files anywhere in the repo are intentional references — never modify or delete them.

## Inputs

- `source` — Path to the source Markdown article (e.g. `ai-thoughts/docs/260803-ollama-to-llamacpp.md` or `history/docs/260629-luoshenfu-literary-analysis.md`). Required. If the user only names an article, locate it by slug or date.
- `category` — Blog category: `tech`, `travel`, `photo`, `philosophy`, or `culture`. Optional. Default `tech`.
- `draft` — `true`/`false`. Optional. Default `false` (published).
- `featured` — `true`/`false`. Optional. Default `false`.
  - `true`: homepage-worthy — a signature/opinion essay, deep dive, or milestone post that defines the blog's voice. Use sparingly (aim ≤ 20% of posts) so the homepage stays curated.
  - `false`: everything else — how-tos, quick notes, release/changelog posts, and `*-zh-hans.md` (legacy `*-chn.md`) translations of an already-published post.
  - When the user doesn't specify, ask which it is (per Procedure step 2); never auto-pick `true`.
  - See `astro_journal/AGENTS.md` → "Featured posts" for the full criteria, cap, and rotation rule; never flip `featured` without the user's explicit approval.
- `tags` — List of lowercase hyphen-separated tags. Optional. Default derived from the article topic. **When the source is from `history/`** (Chinese history / literature / culture), always also include the four base tags `chinese`, `history`, `culture`, `literature` alongside the topic-specific tags; dedupe against tags already present.

## Outputs

- `postPath` — Path to the created post, e.g. `src/data/blog/tech/260803-ollama-to-llamacpp.md`.
- `imagesCopied` — List of image files copied into `src/assets/images/`.

## Procedure

1. **Wait for the user to point out the article** to sync. Do not start until they name it explicitly.
2. **Confirm the plan** with the user: target category, `draft`/`featured`, and tags. Get their go-ahead before writing anything to `astro_journal`.
3. **Locate the blog**: confirm `astro_journal` is checked out at `/home/jeff/pool/git/astro_journal`.
4. **Read the source** article from `source`. If it has no frontmatter, infer the title from the first `#`/`##` heading. The `yymmdd` prefix in the filename is only a **file-creation record** — it does **not** set the publish date (see step 9).
5. **Fact-check before sync (for history/culture articles).** If syncing from `history/docs/` and a matching corrections doc exists (e.g. `docs/260808-corrections-by-citation.md`), confirm the article's 已修正 (confirmed fixes) are already applied, and surface any 待核实 (unverified) items to the user. Historical/literary claims must be verified against at least two independent reliable sources.
6. **Determine the filename**: `yymmdd-lowercase-slug.md`. Normalize the slug: lowercase, hyphens only, strip underscores/camelCase and any existing date prefix/timestamp. Keep the 6-digit `yymmdd` date prefix.
7. **Polish** (light): fix grammar/spelling/clarity in English; preserve code blocks, inline code, and technical terms verbatim. Do not rewrite substance.
8. **Copy images**: for every `../imgs/<file>` reference in the source, copy the image from `imgs/` (in `ai-thoughts` or `history`) into `src/assets/images/`, normalizing the filename to lowercase-hyphens with a 6-digit `yymmdd` prefix. Rewrite the reference in the post to `../../../assets/images/<file>`.
9. **Write frontmatter** (AstroPaper schema):

   ```yaml
   ---
   author: Jeff Yang
   pubDatetime: <ISO-8601 publish time, e.g. 2026-10-10T03:22:32.000Z>
   title: <Post title>
   tags:
     - <tag1>
     - <tag2>
   description: <One-line summary>
   featured: false
   draft: false
   ---
   ```

   `pubDatetime` is the moment the post is **published** — use the current time when astro-sync runs, not the filename date. The `yymmdd` prefix in the filename is only a **file-creation record** and must **not** be used as `pubDatetime`. **Always use a UTC time that has already passed** — the blog's `postFilter` hides posts whose `pubDatetime` is in the future (even by minutes). A future time means the post won't appear on the homepage or in recent posts, though search may still index it. `modDatetime` is optional and only set when an existing post's **substantive content** actually changes — never for housekeeping-only re-syncs (adding `繁体版` cross-links, formatting, or tag edits). The blog sorts by `modDatetime ?? pubDatetime` (`src/utils/getSortedPosts.ts`), so a fresh `modDatetime` on an old post pushes it to the top of the listing. When in doubt, leave `modDatetime` untouched.

   **MUST quote any frontmatter value containing YAML-special characters — especially `: ` (colon + space).** An unquoted `description: Foo: bar` is parsed as a mapping and fails the build at content sync (`bad indentation of a mapping entry` / `mapping values are not allowed in this context`); Cloudflare then keeps the **previous** deployment, so the post never appears and search can't find it. Wrap the whole value in double quotes: `description: "Foo: bar"`. Applies to every field (`title`, `description`, …). This has recurred several times.
10. **Write the post** to `src/data/blog/<category>/<filename>` with the frontmatter followed by the polished body.
11. **Report** `postPath` and `imagesCopied` to the user.
12. **Commit & push (only after approval):** ask the user explicitly whether to commit. On approval, stage the post and any new images in `astro_journal`, commit with a concise message, and push to `origin`. Without approval, leave the changes uncommitted and say so.

## Verification

- File is in `src/data/blog/<category>/` and named `yymmdd-lowercase-slug.md` (lowercase, hyphens only, 6-digit date prefix).
- Frontmatter contains at least `author`, `pubDatetime`, `title`, `tags`, `description`; `draft`/`featured` present when applicable.
- For a `history/`-sourced post, the `tags` list includes `chinese`, `history`, `culture`, and `literature` (alongside any topic tags).
- Any frontmatter value containing `: ` (or other YAML-special characters) is double-quoted.
- Every image reference in the post points to an existing file in `src/assets/images/` (verify with a glob/ls).
- No `../imgs/` references remain in the post.
- No hardcoded `/posts/...` links were introduced.
- No relative cross-links to other articles remain: grep the post for `](` followed by a filename ending in `.md`. Every article link is an absolute `j3ffyang` URL.
- If committed: the post and new images are staged together, and `origin/main` is up to date.
- Optional but recommended: run `npx astro build` in the blog repo — it reproduces content-sync/YAML errors (which `astro check` can miss) and confirms the post renders into `dist/`. Use `npx` directly — `pnpm` is not installed on this machine and `pnpm run ...` fails with "command not found"; `npx` resolves the local `astro` binary fine.

## Error Handling

- **Source not found**: list candidate files and ask which to use.
- **Image missing**: skip it, note it in `imagesCopied` as missing, and tell the user the reference will be broken.
- **Category invalid**: list `tech`, `travel`, `photo`, `philosophy`, `culture` and ask.
- **Filename collision**: if a post already exists at the target path, stop and ask whether to overwrite, use `modDatetime`, or pick a new slug.
