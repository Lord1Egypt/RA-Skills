from __future__ import annotations

import argparse
from pathlib import Path

import summary_templates


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--type_key", default="doc")
    parser.add_argument("--title", default="")
    parser.add_argument("--project_id", default="")
    parser.add_argument("--source_id", default="")
    parser.add_argument("--source_path", default="")
    parser.add_argument("--source_url", default="")
    parser.add_argument("--source_commit", default="")
    parser.add_argument("--save_to", default="")
    args = parser.parse_args()

    data = summary_templates.render(
        args.type_key,
        title=args.title,
        project_id=args.project_id,
        source_id=args.source_id,
        source_path=args.source_path,
        source_url=args.source_url,
        source_commit=args.source_commit,
    )
    text = summary_templates.as_json(data)
    if args.save_to:
        target = Path(args.save_to)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
