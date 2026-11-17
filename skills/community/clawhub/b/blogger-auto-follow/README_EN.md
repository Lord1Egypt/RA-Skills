# Blogger Auto-Follow

Turn a user-supplied creator list into fixed, single-platform follow batches.
After the user reviews the full list, the tool performs consecutive approved
batches in a visible browser. Each batch is limited to 30 accounts by default.

```bash
python3 scripts/blogger_auto_follow.py \
  --platform bilibili \
  --file examples/bilibili_10_bloggers.json \
  --dry-run
```

Run the approved batch by omitting `--dry-run`. On the first run, the user signs
in in the opened browser and verifies the account. The platform-specific,
dedicated profile is stored under `data/browser_profiles/<platform>/` and is
reused by later batches; it never attaches to the user's everyday Chrome.
The terminal requests a count-bound confirmation phrase before each batch (for
example, `EXECUTE 30`).

The tool acts only on the reviewed list, does not add targets or switch
platforms, and stops the batch when the page cannot be safely interpreted.
Results are written to `data/batch_results/`.

See [SKILL.md](SKILL.md) for invocation and operating boundaries.

\## 📄 License

This project is licensed under the [MIT License](LICENSE).
