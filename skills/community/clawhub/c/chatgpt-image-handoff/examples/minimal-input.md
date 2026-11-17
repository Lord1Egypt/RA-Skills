# Minimal Input

Prepare a recoverable three-image run. Prefer ChatGPT through Computer Use when it is available, but keep a manual and local fallback.

```json
{
  "run_id": "demo-content-cards-v1",
  "backend": "auto",
  "preferred_backend": "chatgpt_computer_use",
  "platform_profile": "xiaohongshu",
  "dimensions": "1080x1440",
  "style_prompt": "Editorial screen-print collage with warm paper texture and a coherent limited palette.",
  "jobs": [
    {
      "job_id": "CARD-01",
      "prompt": "Create a cover image about one long article becoming reusable multi-platform assets.",
      "intended_filename": "01-cover.png"
    },
    {
      "job_id": "CARD-02",
      "prompt": "Show a reviewed source becoming 20 local images and 4 manifests.",
      "fact_sensitivity": "high",
      "text_policy": {
        "mode": "allowlist",
        "allowed_text": [
          "20 local images",
          "4 manifests",
          "02 / 03"
        ],
        "forbidden_patterns": [
          "SHA256",
          "checksum",
          "commit ID",
          "timestamp"
        ],
        "extra_readable_text": "reject"
      },
      "intended_filename": "02-two-branches.png"
    },
    {
      "job_id": "CARD-03",
      "prompt": "Show a human review gate before upload and publishing.",
      "intended_filename": "03-human-gate.png"
    }
  ]
}
```

No reference image is included. The run must stop before sending prompts, uploading files, or publishing anything externally.

Because a local renderer was not declared, the strict job remains generative with an allowlist. Set `local_renderer=available` and leave `render_strategy=auto` to recommend a mixed background-plus-overlay path for high-sensitivity jobs.
