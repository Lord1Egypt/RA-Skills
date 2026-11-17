# Smoke Test — Post-Build Verification

> Run `scripts/smoke_test.py` on a produced dataset directory before declaring the dataset done. It catches the most common publication-time failures (`load_dataset()` errors, missing YAML fields, ClassLabel mismatches, missing LICENSE) in seconds, before they bite a downstream user.

## Quick usage

```bash
python /home/z/my-project/skills/dataset-producer/scripts/smoke_test.py \
  /home/z/my-project/download/my_dataset/
```

Exit code 0 means pass; non-zero means fail. Output is human-readable — print each check as `✓`/`✗`/`⚠`.

## What the smoke test checks

| # | Check | Why |
|---|-------|-----|
| 1 | `README.md` exists and YAML frontmatter parses | A broken YAML block will fail `load_dataset()` immediately |
| 2 | All required YAML top-level fields present (`license`, `language`, `pretty_name`, `size_categories`, `task_categories`, `configs`, `dataset_info`) | Missing fields break the Hub UI filters or the loader's split inference |
| 3 | `load_dataset()` succeeds and returns a `DatasetDict` | The canonical "does it load?" test |
| 4 | Each declared split in YAML has the expected row count | Catches `num_examples` mismatches that confuse users when they filter by split. Handles both `dataset_info` shapes: dict (single-config) and list (multi-config — splits of non-default configs are noted, not failed, since the default load only materializes the default config) |
| 5 | ClassLabel fields' `int2str()` works and `names` match YAML | Catches the common mistake of declaring `answer: string` instead of `answer: class_label` |
| 6 | Example row in `### Data Instances` matches schema (all field keys present) | The example is the single most useful section for users — it must actually match the data |
| 7 | `LICENSE` file exists in the dataset root and is non-empty | The `license:` YAML field is metadata; the actual text must be in a `LICENSE` file for the dataset to be legally usable |
| 8 | `create_dataset.py` exists in the dataset root (recommended) | Without provenance, the dataset can't be audited or reproduced |
| 9 | `stats.json` exists (optional, for re-running make_card.py) | Lets you re-run `make_card.py` without rebuilding parquet |

## What to do if it fails

| Failure | Fix |
|---|---|
| `YAML frontmatter fails to parse` | Open README.md in a YAML linter; the indentation under `dataset_info.features` is the most common culprit (especially the `class_label:` block which needs 4-level nesting) |
| `load_dataset() failed: no splits found` | File names don't match `<split>-XXXXX-of-XXXXX.parquet` pattern, OR YAML `configs.data_files` glob doesn't match the actual file paths. Verify with `ls data/` |
| `load_dataset() failed: couldn't infer the same data file format for all splits` | A split declared in YAML has no matching parquet file. Either write the empty shard (produce_dataset.py does this automatically now) or remove the split from YAML |
| `Split '<name>': declared num_examples=X, but actual=Y` | Re-run `produce_dataset.py` and then `make_card.py` to regenerate the YAML with correct stats |
| `ClassLabel int2str() failed` | Either the parquet has string values where ints are expected, or the YAML `class_label.names` list doesn't match what was written. Re-run `make_card.py --auto-example` and re-test |
| `Example row in README is missing keys: [...]` | Re-run `make_card.py --auto-example` to extract a fresh row from the parquet |
| `LICENSE file is empty` | Copy a real license from `assets/licenses/` |
| `create_dataset.py is empty` | Copy `scripts/example_create_dataset.py` to the dataset root as `create_dataset.py` and adapt the constants |

## CI integration

```bash
# In your CI pipeline:
python /home/z/my-project/skills/dataset-producer/scripts/smoke_test.py \
  /home/z/my-project/download/my_dataset/ \
  && echo "Dataset is publish-ready" \
  || { echo "Smoke test failed"; exit 1; }
```

The smoke test exits 0 on pass, 1 on fail. Warnings (`⚠`) don't fail the test — only `✗` failures do.

## What the smoke test does NOT check

- **Content quality** — it doesn't evaluate whether the data is correct, diverse, or unbiased. Use `validate.py` for that.
- **Full schema conformance** — it only verifies that `load_dataset()` succeeds and ClassLabel names match. It doesn't check every row's types. The `validate.py` script does this.
- **README prose quality** — it doesn't check whether `### Curation Rationale` is filled in. Use `references/quality-checklist.md` for that.
- **Hub pushability** — it doesn't actually push to the Hub. Use `huggingface_hub` directly for that.

The smoke test is a fast sanity check, not a substitute for the full quality checklist. Run it after `make_card.py` and before the quality checklist.
