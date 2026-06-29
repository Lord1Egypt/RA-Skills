#!/usr/bin/env python3
import argparse
import importlib.util
from pathlib import Path


def load_assemble_module():
    assemble_path = Path(__file__).with_name("assemble.py")
    spec = importlib.util.spec_from_file_location("epub_bilingual_assemble", assemble_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Rebuild an existing bilingual EPUB with the current math-aware "
            "assembly fixes. Pass the extraction.json used to create the EPUB."
        )
    )
    parser.add_argument("extraction_json", help="Path to an existing extraction.json")
    args = parser.parse_args()

    assemble = load_assemble_module()
    assemble.assemble(Path(args.extraction_json).expanduser().resolve())


if __name__ == "__main__":
    main()
