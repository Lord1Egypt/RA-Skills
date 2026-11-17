#!/usr/bin/env python3
"""Upload to Linx using linx-client, or curl when the client is absent."""

import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
from urllib.parse import quote, urlsplit


class UploadError(Exception):
    pass


def expanded(value):
    return Path(os.path.expandvars(value)).expanduser().resolve()


def valid_url(value):
    if not isinstance(value, str) or any(c.isspace() for c in value):
        return False
    parsed = urlsplit(value)
    return (parsed.scheme in ("http", "https") and bool(parsed.netloc)
            and not parsed.username and not parsed.password
            and not parsed.query and not parsed.fragment)


def settings():
    default = Path(os.environ.get("XDG_CONFIG_HOME", "~/.config")) / "linx-client.conf"
    source = expanded(os.environ.get("LINX_CONFIG", str(default)))
    config = {}
    if "LINX_CONFIG" in os.environ or source.exists():
        try:
            config = json.loads(source.read_text())
        except (OSError, ValueError):
            raise UploadError("Cannot read Linx config; check LINX_CONFIG and its JSON syntax.") from None
        if not isinstance(config, dict):
            raise UploadError("Linx config must be a JSON object.")
    for key in ("siteurl", "apikey", "logfile"):
        if key in config and not isinstance(config[key], str):
            raise UploadError("Linx config values must be strings.")
    url = os.environ.get("LINX_URL", config.get("siteurl", "")).strip()
    if not valid_url(url):
        raise UploadError("Set LINX_URL or config siteurl to an HTTP(S) instance base URL without credentials, query, or fragment.")
    key = os.environ.get("LINX_API_KEY", config.get("apikey", "")).strip()
    if any(c in key for c in "\r\n\0"):
        raise UploadError("API key must not contain control delimiters.")
    state = Path(os.environ.get("XDG_STATE_HOME", "~/.local/state")) / "openclaw-linx/uploads.json"
    logfile = expanded(os.environ.get("LINX_LOGFILE", config.get("logfile") or str(state)))
    return {"siteurl": url.rstrip("/") + "/", "apikey": key, "logfile": str(logfile)}


def read_log(path):
    if not path.exists():
        return {}
    try:
        entries = json.loads(path.read_text())
    except (OSError, ValueError):
        raise UploadError("Cannot read upload logfile; refusing to lose deletion keys.") from None
    if not isinstance(entries, dict) or not all(isinstance(k, str) and isinstance(v, str) for k, v in entries.items()):
        raise UploadError("Upload logfile must map URLs to deletion keys.")
    return entries


def save_key(path, url, key):
    entries = read_log(path)
    entries[url] = key
    with tempfile.NamedTemporaryFile(mode="w", dir=path.parent, delete=False) as stream:
        temporary = Path(stream.name)
        try:
            json.dump(entries, stream)
            stream.flush()
            os.fsync(stream.fileno())
            temporary.replace(path)
        finally:
            temporary.unlink(missing_ok=True)


def binary_upload(binary, config_path, file, args):
    command = [binary, "-c", str(config_path), "-no-cb"]
    if args.expiry is not None:
        command += ["-e", str(args.expiry)]
    if args.randomize:
        command += ["-r"]
    if args.name:
        command += ["-f", args.name]
    if args.direct:
        command += ["-selif"]
    result = subprocess.run(command + [str(file)], stdin=subprocess.DEVNULL, capture_output=True, text=True)
    lines = result.stdout.strip().splitlines()
    # The client can report an HTTP error on stdout while exiting zero.
    if result.returncode or len(lines) != 1 or not valid_url(lines[0]):
        raise UploadError("linx-client did not confirm a clean upload. No fallback attempted; inspect the private logfile before retrying.")
    return lines[0]


def curl_upload(curl, config, file, args, directory):
    headers = Path(directory) / "headers"
    headers.write_text("Accept: application/json\n" + (
        "Linx-Api-Key: " + config["apikey"] + "\n" if config["apikey"] else "") + (
        "Linx-Expiry: " + str(args.expiry) + "\n" if args.expiry is not None else "") + (
        "Linx-Randomize: yes\n" if args.randomize else ""))
    headers.chmod(0o600)
    target = config["siteurl"] + "upload/" + quote(args.name or file.name, safe="")
    response = Path(directory) / "response.json"
    result = subprocess.run([
        curl, "--disable", "--silent", "--show-error", "--globoff",
        "--proto", "=http,https", "--connect-timeout", "30", "--max-time", "300",
        "--header", "@" + str(headers), "--upload-file", str(file),
        "--output", str(response), "--write-out", "%{http_code}", target,
    ], stdin=subprocess.DEVNULL, capture_output=True, text=True)
    if result.returncode or result.stdout != "200":
        status = result.stdout if result.stdout.isdigit() else "unavailable"
        raise UploadError(f"curl upload failed (HTTP {status}); no retry attempted.")
    try:
        data = json.loads(response.read_text())
    except (OSError, ValueError):
        raise UploadError("Upload response was not JSON; upload may exist. Do not retry blindly.") from None
    if not isinstance(data, dict) or not valid_url(data.get("url")) or not isinstance(data.get("delete_key"), str) or not data["delete_key"]:
        raise UploadError("Upload response lacks a valid URL or deletion key; upload may exist.")
    # Preserve deletion access even if checksum verification fails afterward.
    save_key(Path(config["logfile"]), data["url"], data["delete_key"])
    checksum = data.get("sha256sum")
    if checksum:
        with file.open("rb") as stream:
            actual = hashlib.file_digest(stream, "sha256").hexdigest()
        if checksum != actual:
            raise UploadError("Upload checksum mismatch; deletion key saved. Do not retry blindly.")
    else:
        print("Warning: server did not provide a checksum.", file=sys.stderr)
    direct = data.get("direct_url")
    return direct if args.direct and valid_url(direct) else data["url"]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--expiry", type=int, help="Expiry in seconds (0 requests no expiry; server policy applies)")
    parser.add_argument("--randomize", action="store_true", help="Request a random server filename")
    parser.add_argument("--name", help="Remote filename; requires exactly one file")
    parser.add_argument("--direct", action="store_true", help="Print direct_url when available")
    parser.add_argument("files", nargs="+", help="Local files to upload; stdin is not supported")
    args = parser.parse_args()
    if args.expiry is not None and args.expiry < 0:
        parser.error("--expiry must be nonnegative")
    if args.name is not None and (len(args.files) != 1 or not args.name or args.name in (".", "..") or any(c in args.name for c in "/\\\r\n\0")):
        parser.error("--name must be a single filename and requires exactly one file")
    config = settings()
    files = [expanded(file) for file in args.files]
    if not all(file.is_file() and os.access(file, os.R_OK) for file in files):
        raise UploadError("Every upload source must be a readable regular file.")
    binary = shutil.which("linx-client")
    curl = shutil.which("curl") if not binary else None
    if not binary and not curl:
        raise UploadError("Install linx-client or curl on the execution host.")
    logfile = Path(config["logfile"])
    logfile.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    read_log(logfile)
    with tempfile.TemporaryDirectory(prefix="openclaw-linx-") as directory:
        config_path = Path(directory) / "client.json"
        config_path.write_text(json.dumps(config))
        config_path.chmod(0o600)
        for file in files:
            url = binary_upload(binary, config_path, file, args) if binary else curl_upload(curl, config, file, args, directory)
            print(url, flush=True)


if __name__ == "__main__":
    try:
        main()
    except (UploadError, OSError) as error:
        message = str(error) if isinstance(error, UploadError) else "Local file or process operation failed; check permissions and private configuration."
        print("Error: " + message, file=sys.stderr)
        sys.exit(1)
