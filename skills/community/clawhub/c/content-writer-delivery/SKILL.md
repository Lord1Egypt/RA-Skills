---
name: content-writer-delivery
description: Deliver a reviewed article to a user-selected local file, document service, or publishing platform after final confirmation. Use only when the user explicitly asks for delivery.
---

# Content Writer Delivery

This extension acts only after the article is final. It never decides a destination or publishes by default.

## Required confirmation

Before writing, copying, uploading, or publishing, present the final article and obtain confirmation of the exact target path, document, or platform account; the audience/visibility; and whether this is a draft, copy-only action, or public publication.

## Workflow

1. Default to a copy-ready Markdown or HTML block in chat.
2. For a local file, use only the named path and request a separate confirmation before replacing an existing file.
3. For a remote document, create or update only the selected document.
4. For a platform, show a final preview and wait for approval immediately before the final submission.
5. Report the final destination and completed action.

## Boundaries

Do not inspect app data, credentials, contacts, prior drafts, or unrelated documents. Do not change sharing settings, schedule posts, send notifications, or cross-post.
