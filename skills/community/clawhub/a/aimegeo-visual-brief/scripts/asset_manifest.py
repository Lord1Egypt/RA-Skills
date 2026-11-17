#!/usr/bin/env python3
"""Validate a local visual asset inventory; no generation or network access."""
import argparse
import json
from pathlib import Path, PurePosixPath
import re
import sys

class InvalidRecord(ValueError):
    pass

def require(ok, message):
    if not ok:
        raise InvalidRecord(message)

def decode_image(path):
    try:
        from PIL import Image
        with Image.open(path) as im:
            require(im.format in {"PNG", "JPEG", "WEBP"}, "unsupported image format")
            require(getattr(im, "n_frames", 1) == 1, "animated images are not accepted")
            im.verify()
        with Image.open(path) as im:
            im.load()
            return im.format.lower(), list(im.size)
    except InvalidRecord:
        raise
    except Exception as exc:
        raise InvalidRecord("image could not be decoded") from exc

def local_path(root, value):
    require(isinstance(value, str) and value.strip(), "file must be a relative path")
    path = PurePosixPath(value)
    require(not path.is_absolute() and not re.match(r"^[A-Za-z]:", value)
            and "\\" not in value and ".." not in path.parts,
            "file must stay inside the inventory directory")
    resolved = (root / value).resolve()
    require(resolved.is_relative_to(root.resolve()), "file symlink escapes the inventory directory")
    require(resolved.is_file(), "file does not exist")
    return resolved

def validate(data, root):
    require(isinstance(data, dict) and set(data) == {"schema_version", "assets"},
            "record must contain schema_version and assets only")
    require(type(data["schema_version"]) is int and data["schema_version"] == 1,
            "unsupported schema_version")
    assets = data["assets"]
    require(isinstance(assets, list) and assets, "assets must be a non-empty list")
    ids, paths = set(), set()
    rows=[]
    for i, asset in enumerate(assets):
        required={"id", "file", "intended_use", "description", "alt_text", "rights_source", "review"}
        require(isinstance(asset, dict) and set(asset) == required, f"assets[{i}] has missing or unknown fields")
        aid=asset["id"]
        require(isinstance(aid,str) and re.fullmatch(r"[a-z0-9][a-z0-9-]{0,63}",aid), f"assets[{i}].id is invalid")
        require(aid not in ids, f"duplicate asset id: {aid}"); ids.add(aid)
        for key in ("intended_use", "description", "alt_text", "rights_source"):
            require(isinstance(asset[key],str) and asset[key].strip(), f"{aid}.{key} must be non-empty text")
        require(asset["review"] in ("approved", "needs_review", "rejected"), f"{aid}.review is invalid")
        if asset["review"] == "approved":
            path=local_path(Path(root).resolve(),asset["file"])
            require(path not in paths, "multiple records cannot reuse the same image file")
            paths.add(path)
            fmt, dimensions=decode_image(path)
            rows.append({"id":aid,"state":"available","format":fmt,"dimensions":dimensions,
                         "review":asset["review"],"rights_source":asset["rights_source"]})
        else:
            require(asset["file"] is None, f"{aid}: non-approved assets must not point to a deliverable file")
            rows.append({"id":aid,"state":"pending","format":None,"dimensions":None,
                         "review":asset["review"],"rights_source":asset["rights_source"]})
    usable=sum(row["state"]=="available" for row in rows)
    return {"valid":True,"summary":{"assets":len(rows),"available":usable,"pending":len(rows)-usable},"assets":rows}

def main(argv=None):
    ap=argparse.ArgumentParser(description=__doc__); ap.add_argument("record",type=Path); args=ap.parse_args(argv)
    try:
        data=json.loads(args.record.read_text(encoding="utf-8")); result=validate(data,args.record.parent)
    except (OSError, json.JSONDecodeError, InvalidRecord, RecursionError) as exc:
        message=str(exc) if isinstance(exc,InvalidRecord) else "record could not be read or parsed"
        print(json.dumps({"valid":False,"error":message},ensure_ascii=False)); return 2
    print(json.dumps(result,ensure_ascii=False,indent=2)); return 0

if __name__ == "__main__": sys.exit(main())
