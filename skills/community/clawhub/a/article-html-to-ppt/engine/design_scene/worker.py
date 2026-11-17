"""Fixed worker entrypoint; the only operation is rendering validated records."""
from __future__ import annotations

import argparse
import os
from pathlib import Path

from .backend import inspect_objects, render
from .runtime import real_preview
from .store import Store, digest, DesignError


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("stage", type=Path)
    parser.add_argument("--preview", action="store_true")
    args = parser.parse_args()
    if os.name == "posix":
        import resource
        resource.setrlimit(resource.RLIMIT_CPU, (150, 150))
        resource.setrlimit(resource.RLIMIT_FSIZE, (128 * 1024 * 1024, 128 * 1024 * 1024))
        resource.setrlimit(resource.RLIMIT_NOFILE, (256, 256))
    with Store(args.stage) as store:
        task = store.json("task.json")
        assets = {}
        for a in task["assets"]["items"]:
            data = store.read("assets/" + a["sha256"] + ".png")
            if digest(data) != a["sha256"]:
                raise DesignError("ASSET_HASH_MISMATCH")
            assets[a["id"]] = data
        data = render(task, assets)
        inspection = inspect_objects(data, task)
        store.write("deck.pptx", data, exclusive=True)
        store.put_json("objects.json", inspection, exclusive=True)
        preview = real_preview(args.stage, task) if args.preview else {"status": "not_requested", "pages": []}
        store.put_json("render.json", preview, exclusive=True)


if __name__ == "__main__":
    main()
