# Webhooks

Read this file for repository webhook inspection, creation, updates, and delivery testing.

## Core Tools

| Goal | Canonical method |
| --- | --- |
| List webhooks | `atomgit_get_repository_webhooks` |
| Inspect one webhook | `atomgit_get_repository_webhook` |
| Create a webhook | `atomgit_create_repository_webhook` |
| Update a webhook | `atomgit_update_repository_webhook` |
| Test a webhook | `atomgit_test_repository_webhook` |

## Typical Flow

1. Read existing webhook configuration before creating a new endpoint.
2. Confirm payload URL, secret, and subscribed events before creation.
3. Use the test endpoint after configuration is saved.
