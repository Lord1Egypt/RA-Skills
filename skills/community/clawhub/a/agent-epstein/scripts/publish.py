"""publish.py — turn a harvested folder into something a trainer can use.

    python publish.py --dataset ./dataset --mode local
    python publish.py --dataset ./dataset --mode hf --repo user/yuri-art
    python publish.py --dataset ./dataset --mode openai-files   # see warning

READ THIS BEFORE CHOOSING A MODE
--------------------------------
There is no supported way to "upload art to ChatGPT so training picks it
up". The consumer app's uploads are not a training intake, and the API
does not train on customer data unless the customer explicitly opts in.
A file parked in an OpenAI account reaches no training pipeline.

What actually feeds training is a *dataset* that a fine-tune / LoRA /
embedding run reads. So:

  mode=local         folder + metadata.jsonl + dataset card. The real
                     artifact; feed it to a local trainer or upload it
                     by hand wherever you like.
  mode=hf            push to a HuggingFace dataset repo. THIS is the
                     path that makes an anime-art dataset discoverable
                     and loadable by training code. Recommended.
  mode=openai-files  uploads via the Files API for completeness. It does
                     NOT train anything, is retained ~30 days for abuse
                     monitoring, and every image is CSRF/CSAM-classified
                     on submission. Kept for people who explicitly want
                     remote storage under those terms.
"""
from __future__ import annotations

import argparse
import json
import mimetypes
import os
import sys
import urllib.request
import uuid
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from normalize import load_jsonl                              # noqa: E402

CARD = """---
license: other
license_name: see-source-urls
pretty_name: {pretty_name}
task_categories:
- text-to-image
configs:
- config_name: default
  data_files:
- split: train
  path: metadata.jsonl
---

# {pretty_name}

Harvested with `AgentEpstein` on {when}.

**Query:** `{query}`
**Images:** {n}
**Sources:** {sources}

## Provenance and rights

Every image is fan/derivative artwork that remains the copyright of its
original artist. Each row in `metadata.jsonl` carries `page_url`,
`file_url`, `artist` and the full `tags` string. **Keep those columns.**
Attribution is the only thing that makes a dataset like this defensible,
and stripping it is what turns a research artifact into a rights problem.

This dataset is not licensed for redistribution by the harvester. Check
each source site's terms before republishing, and treat the inclusion of
any given artist's work as a decision that artist is entitled to object
to.

## Layout

```
images/          one file per row
metadata.jsonl   one JSON object per image
manifest.json    harvest parameters and per-source counts
rejected.jsonl   what was filtered and why (audit trail)
```

`metadata.jsonl` rows carry `file_name` (dataset-relative image path) and
`caption` (space-joined tags), so HuggingFace `imagefolder` and most
caption-conditioned trainers read this folder as-is.
"""


def write_card(ds: Path) -> Path:
    rows = load_jsonl(ds / "metadata.jsonl")
    manifest = {}
    mp = ds / "manifest.json"
    if mp.exists():
        manifest = json.loads(mp.read_text(encoding="utf-8"))
    sources = sorted({r.get("source", "?") for r in rows})
    name = ds.name
    text = CARD.format(
        pretty_name=name,
        when=manifest.get("generated_utc", "unknown date"),
        query=manifest.get("query", "n/a"),
        n=len(rows),
        sources=", ".join(sources) or "none",
    )
    p = ds / "README.md"
    p.write_text(text, encoding="utf-8")
    return p


# Only these are published. `rejected.jsonl` and `vision_worklist.json` are
# deliberately excluded: both carry page_url, artist and the full tag string
# for art that this project EXCLUDED — rows the safety filter dropped, and
# candidates nobody has judged. Publishing them would put the provenance of
# the rejected content in a public repo, which is exactly the opposite of
# what the audit trail is for. It stays local.
PUBLISH_FILES = ("metadata.jsonl", "manifest.json", "README.md")


def push_hf(ds: Path, repo_id: str, token: str, private: bool) -> str:
    try:
        from huggingface_hub import HfApi
    except ImportError:
        raise SystemExit(
            "huggingface_hub is required for --mode hf:\n"
            "  uv pip install huggingface_hub"
        )
    api = HfApi(token=token)
    api.create_repo(repo_id=repo_id, repo_type="dataset",
                    private=private, exist_ok=True)
    api.upload_folder(
        folder_path=str(ds), repo_id=repo_id, repo_type="dataset",
        allow_patterns=["images/*", *PUBLISH_FILES],
        commit_message="AgentEpstein upload")
    skipped = sorted(p.name for p in ds.iterdir()
                     if p.is_file() and p.name not in PUBLISH_FILES)
    if skipped:
        print("not published (local-only): " + ", ".join(skipped))
    return f"https://huggingface.co/datasets/{repo_id}"


def _multipart(fields: dict, filename: str, content: bytes) -> tuple[bytes, str]:
    boundary = "----harvest" + uuid.uuid4().hex
    out = bytearray()
    for k, v in fields.items():
        out += f"--{boundary}\r\nContent-Disposition: form-data; name=\"{k}\"\r\n\r\n{v}\r\n".encode()
    ctype = mimetypes.guess_type(filename)[0] or "application/octet-stream"
    out += (f"--{boundary}\r\nContent-Disposition: form-data; "
            f"name=\"file\"; filename=\"{filename}\"\r\n"
            f"Content-Type: {ctype}\r\n\r\n").encode()
    out += content
    out += f"\r\n--{boundary}--\r\n".encode()
    return bytes(out), f"multipart/form-data; boundary={boundary}"


def push_openai(ds: Path, api_key: str, purpose: str, limit: int) -> list[str]:
    rows = load_jsonl(ds / "metadata.jsonl")
    ids = []
    for i, r in enumerate(rows[:limit], 1):
        rel = r.get("file_name") or r.get("file_path")
        if not rel:
            continue
        fp = ds / rel
        if not fp.exists():
            continue
        body, ctype = _multipart({"purpose": purpose}, fp.name, fp.read_bytes())
        req = urllib.request.Request(
            "https://api.openai.com/v1/files", data=body,
            headers={"Authorization": f"Bearer {api_key}",
                     "Content-Type": ctype},
            method="POST")
        try:
            with urllib.request.urlopen(req, timeout=180) as resp:
                obj = json.loads(resp.read().decode())
                ids.append(obj.get("id", ""))
                print(f"  [{i}] uploaded {fp.name} -> {obj.get('id')}")
        except Exception as e:                                   # noqa: BLE001
            print(f"  [{i}] FAILED {fp.name}: {e}")
    return ids


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="Package or upload a harvested dataset.")
    p.add_argument("--dataset", required=True)
    p.add_argument("--mode", default="local",
                   choices=["local", "hf", "openai-files"])
    p.add_argument("--repo", default="", help="HF repo id for --mode hf")
    p.add_argument("--private", action="store_true", help="HF: create private")
    p.add_argument("--purpose", default="vision",
                   help="OpenAI Files API purpose (vision|assistants|user_data)")
    p.add_argument("--limit", type=int, default=0,
                   help="OpenAI: cap number of uploads (0 = all)")
    args = p.parse_args(argv)

    ds = Path(args.dataset).resolve()
    if not (ds / "metadata.jsonl").exists():
        print(f"no metadata.jsonl in {ds} — run harvest.py first", file=sys.stderr)
        return 1

    rows = load_jsonl(ds / "metadata.jsonl")
    card = write_card(ds)
    print(f"dataset: {ds}")
    print(f"  images:  {len(rows)}")
    print(f"  card:    {card.name}")

    if args.mode == "local":
        print("\nlocal mode: nothing uploaded. This folder is the artifact.")
        print("Feed it to a trainer, or run with --mode hf to publish it.")
        return 0

    if args.mode == "hf":
        token = os.environ.get("HF_TOKEN", "")
        if not token:
            print("HF_TOKEN is not set. Create a write token at "
                  "https://huggingface.co/settings/tokens", file=sys.stderr)
            return 1
        if not args.repo:
            print("--repo owner/name is required for --mode hf", file=sys.stderr)
            return 1
        url = push_hf(ds, args.repo, token, args.private)
        print(f"\npublished: {url}")
        print("This repo is now loadable by training code, e.g.:")
        print(f'  load_dataset("imagefolder", data_dir="{args.repo}")')
        return 0

    # openai-files
    key = os.environ.get("OPENAI_API_KEY", "")
    if not key:
        print("OPENAI_API_KEY is not set", file=sys.stderr)
        return 1
    print("\n!! WARNING ----------------------------------------------------")
    print(" This uploads images to OpenAI for STORAGE. It does NOT train")
    print(" anything. Retention is ~30 days for abuse monitoring, and every")
    print(" image is classified on submission; a CSAM classifier hit means")
    print(" the image is retained for manual review regardless of any")
    print(" zero-retention agreement. Confirm you hold the rights to upload")
    print(" each image before continuing.")
    print("---------------------------------------------------------------\n")
    ids = push_openai(ds, key, args.purpose, args.limit or len(rows))
    print(f"\nuploaded {len(ids)} file(s) under purpose={args.purpose}")
    return 0 if ids else 3


if __name__ == "__main__":
    raise SystemExit(main())
