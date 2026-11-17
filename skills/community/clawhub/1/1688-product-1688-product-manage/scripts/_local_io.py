"""Small local-file helpers; no network or dependency installation."""
import hashlib
import json
import subprocess
from pathlib import Path


def digest(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def run(argv, timeout=60):
    result = subprocess.run(argv, capture_output=True, text=True, timeout=timeout)
    if result.returncode:
        raise ValueError((result.stderr or result.stdout or "command failed")[-1500:])
    return result.stdout


def workspace(source, output, options, implementation):
    source = Path(source).resolve(strict=True)
    if not source.is_file() or source.stat().st_size == 0:
        raise ValueError("输入不是非空普通文件")
    fingerprint = {"source": str(source), "sourceSha256": digest(source), "options": options,
                   "implementation": digest(implementation),
                   "helpers": digest(__file__)}
    key = hashlib.sha256(json.dumps(fingerprint, sort_keys=True).encode()).hexdigest()[:24]
    folder = Path(output).resolve() / key
    folder.mkdir(parents=True, exist_ok=True)
    return source, folder, fingerprint


def cached(folder, fingerprint):
    try:
        data = json.loads((folder / "result.json").read_text(encoding="utf-8"))
        if data["fingerprint"] != fingerprint:
            return None
        for file in data["files"]:
            path = (folder / file["path"]).resolve()
            path.relative_to(folder.resolve())
            if not path.is_file() or digest(path) != file["sha256"]:
                return None
        return dict(data, reused=True)
    except (KeyError, OSError, ValueError, TypeError):
        return None


def finish(folder, fingerprint, result, paths):
    result.update(fingerprint=fingerprint, reused=False,
                  files=[{"path": str(p.relative_to(folder)), "sha256": digest(p)}
                         for p in paths])
    temporary = folder / "result.json.tmp"
    temporary.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    temporary.replace(folder / "result.json")
    return result


def emit(result):
    print(json.dumps(result, ensure_ascii=False, allow_nan=False))
