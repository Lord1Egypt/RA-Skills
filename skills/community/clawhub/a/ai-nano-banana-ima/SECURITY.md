# Security Disclosure: ai-nano-banana-ima

## Purpose

This document explains endpoint usage, credential flow, and local data behavior for `ai-nano-banana-ima`.

## Network Endpoints

| Domain | Used For | Trigger |
|---|---|---|
| `api.imastudio.com` | Product list, task create, task detail polling | All requests |
| `imapi.liveme.com` | Upload-token request for local image inputs | Only when `image_to_image` includes local files |
| `*.aliyuncs.com` / `*.esxscloud.com` | Presigned binary upload + media CDN delivery | Returned by upload-token API |

For remote HTTPS images, the script can pass URLs directly without upload-token calls.

## Credential Flow

| Credential | Where Sent | Why |
|---|---|---|
| `IMA_API_KEY` | `api.imastudio.com` | Open API auth (`Authorization: Bearer ...`) |
| `IMA_API_KEY` | `imapi.liveme.com` | Upload-token auth for local image uploads |

No API key is sent to presigned upload hosts during binary upload.

## Model Scope Enforcement

The script hard-limits exposed model IDs to:

- `gemini-3.1-flash-image`
- `gemini-3-pro-image`

Any other model ID is rejected locally.

## Local Data

| Path | Content | Retention |
|---|---|---|
| `~/.openclaw/memory/ima_prefs.json` | Per-user model preference cache | Until manually removed |
| `~/.openclaw/logs/ima_skills/` | Operational logs | Auto-cleaned by script after 7 days |

No API key is written into repository files.
