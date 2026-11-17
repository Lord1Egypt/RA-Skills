#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""校验 cad-file-reader v0 交接 JSON。"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from cad_contract import validate_contract_file


def main() -> int:
    import pyboot
    pyboot.ensure_utf8_io()
    parser = argparse.ArgumentParser(description="校验 cad-file-reader/v0 交接 JSON")
    parser.add_argument("inputs", nargs="+", help="识图/测量候选 JSON")
    args = parser.parse_args()
    failed = False
    for value in args.inputs:
        path = Path(value)
        try:
            errors = validate_contract_file(path)
        except Exception as exc:
            errors = [f"{type(exc).__name__}: {exc}"]
        result = {"file": str(path), "ok": not errors, "errors": errors}
        print(json.dumps(result, ensure_ascii=False))
        failed = failed or bool(errors)
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
