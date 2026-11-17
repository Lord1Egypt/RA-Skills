# Optional ChatGPT ZIP batches

Treat ZIP delivery as an experimental optimization when at least three independent image jobs share one visual series and the active ChatGPT surface has already demonstrated native multi-image archive delivery. The normal one-job-at-a-time route in ordinary Chat is authoritative for first runs, revisions, missing files, and sessions that cannot return archives.

Do not require a specific Chrome profile, project, or Work mode. Stay in the authenticated browser window and ordinary Chat surface approved by the user. Select Work only when the user explicitly requests it.

## Prepare

```bash
python <skill-dir>/scripts/batch_zip.py prepare \
  --handoff <handoff-dir> \
  --batch-id <stable-batch-id> \
  --job-id <JOB-01> \
  --job-id <JOB-02>
```

This creates:

- `batches/<batch-id>/batch-manifest.json`
- `batches/<batch-id>/work-prompt.md`

Review both files before transmission. The batch prompt requires separate named images, `qa-report.json`, a copy of the manifest, and one ZIP archive.

## Send through Computer Use

1. Use the user-approved authenticated ChatGPT window and ordinary Chat surface.
2. Confirm the current destination and account state from fresh app state. Do not switch browser profiles or modes without a user instruction.
3. Request action-time confirmation for the exact `work-prompt.md` and any reference files.
4. Send one batch prompt. Do not also send the individual job prompts.
5. Reject any attempt to replace native image generation with Python, Pillow, SVG, HTML, Canvas, deterministic drawing, screenshots, or placeholders.
6. Wait for the final ZIP attachment. A textual promise or an on-screen preview is not a download.
7. If ChatGPT misclassifies the request as editing missing source images, proposes local programmatic rendering, reports missing images, or cannot attach a ZIP, record the batch failure and use the one-job route.

Record a failed batch before serial fallback:

```bash
python <skill-dir>/scripts/batch_zip.py fail \
  --handoff <handoff-dir> \
  --batch-id <stable-batch-id> \
  --reason <stable-failure-code> \
  --missing-file <expected-image.png>
```

## Import

```bash
python <skill-dir>/scripts/batch_zip.py import \
  --handoff <handoff-dir> \
  --batch-id <stable-batch-id> \
  --archive <downloaded.zip>
```

The importer preserves the original archive, rejects traversal, symlinks, encrypted entries, duplicate basenames, and oversized archives, then imports only the filenames from the local manifest. Missing images remain incomplete. `qa-report.json` is recorded as untrusted evidence and never auto-passes visual QA.

## Recovery

- Complete ZIP: inspect every imported image and record local QA.
- Partial ZIP: create a new batch containing only missing jobs.
- Wrong filename but identifiable image: do not guess silently; rename only after visual identification and record the repair.
- Wrong text in one image: revise only that job.
- ZIP unavailable or native multi-image generation rejected: record the batch failure, then fall back to individual ordinary-Chat downloads without changing the job facts or text policy.
- Native image generation unavailable: stop the batch; do not accept programmatic rendering as an equivalent result.
