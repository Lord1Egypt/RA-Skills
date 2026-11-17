import argparse
import os
import re
import shutil
import stat
import sys
import tempfile
from pathlib import Path

from _proc import run_git, run_tool

# Frozen snapshot for reviewers: export from a commit only (git archive) and refuse when the site directory has uncommitted or untracked files,
# so files that exist in the working tree but not in the commit do not turn into 404s; then run asset_check.py over the whole site.
# The archive is extracted into a fresh temporary directory and moved into place. An existing output directory is left alone unless
# --overwrite is set and the directory contains the marker file this tool writes. Paths that overlap the repo, the home directory,
# or the filesystem root are refused. Symlinks are not followed: a symlink output path is refused, and deletion uses lstat.
# Large files kept out of git (game builds, videos) are symlinked into the snapshot with --link.
# Usage: python3 snapshot.py <repo> <site dir (relative to repo)> <snapshot dir> [--ref HEAD] [--overwrite] [--link path-in-snapshot=real-path ...] [--skip subdir ...]

MARKER_NAME = ".award-polish-snapshot"
MARKER_BODY = "award-polish-snapshot\n"
REF_RE = re.compile(r"^(?:HEAD|refs/[A-Za-z0-9._/-]+|[A-Za-z0-9][A-Za-z0-9._/-]*)(?:~\d+|\^\d*)*$")

ap = argparse.ArgumentParser()
ap.add_argument("repo")
ap.add_argument("site")
ap.add_argument("out")
ap.add_argument("--ref", default="HEAD")
ap.add_argument("--overwrite", action="store_true", help="replace an output directory this tool created (it must contain the marker file)")
ap.add_argument("--link", action="append", default=[], metavar="path-in-snapshot=real-path")
ap.add_argument("--skip", action="append", default=[], help="subdirectory asset_check.py should skip")
args = ap.parse_args()


def git_toplevel():
    return run_git(["rev-parse", "--show-toplevel"], cwd=repo).stdout


def git_status_site(site_path):
    site_path = rel_arg(site_path, "site dir")
    return run_git(
        ["status", "--porcelain", "--untracked-files=all", "--", site_path],
        cwd=repo,
    ).stdout


def git_short_ref(ref):
    if not isinstance(ref, str) or not REF_RE.fullmatch(ref):
        sys.exit(f"ref is not a plain commit or branch name: {ref}")
    return run_git(["rev-parse", "--short", ref], cwd=repo).stdout


def git_archive(ref, site_path):
    if not isinstance(ref, str) or not REF_RE.fullmatch(ref):
        sys.exit(f"ref is not a plain commit or branch name: {ref}")
    site_path = rel_arg(site_path, "site dir")
    # text stays off so the archive bytes are not decoded.
    return run_git(
        ["archive", ref, "--", site_path],
        cwd=repo,
        text=False,
        capture_output=True,
    ).stdout


def extract_archive(dest, archive):
    if not isinstance(archive, (bytes, bytearray)):
        sys.exit("refusing an archive that is not bytes")
    dest = lexical_abs(dest)
    if dest.is_symlink() or not dest.is_dir():
        sys.exit(f"refusing to extract into {dest}")
    dest_text = os.fspath(dest)
    if "\0" in dest_text:
        sys.exit("refusing an archive destination that is not plain text")
    return run_tool("tar", ["-x", "-C", dest_text], stdin=bytes(archive))


def run_asset_check(site_root, skips):
    script = Path(__file__).with_name("asset_check.py")
    if not script.is_file():
        sys.exit(f"asset check script is missing: {script}")
    root_text = os.fspath(site_root)
    if not isinstance(root_text, str) or "\0" in root_text:
        sys.exit("refusing an asset-check path that is not plain text")
    argv = [os.fspath(script), root_text]
    for skip in skips:
        argv.extend(["--skip", rel_arg(skip, "--skip")])
    if Path(argv[0]) != script:
        sys.exit("refusing an asset check that is not the bundled script")
    return run_tool("python", argv)


def lexical_abs(path):
    return Path(os.path.abspath(os.fspath(path)))


def variants(path):
    lexical = lexical_abs(path)
    real = Path(os.path.realpath(lexical))
    return [lexical] if real == lexical else [lexical, real]


def overlaps(path, protected):
    path = lexical_abs(path)
    protected = lexical_abs(protected)
    # Every absolute path is inside the filesystem root. Only the root itself overlaps root.
    if protected == Path(protected.anchor):
        return path == protected
    if path == protected:
        return True
    try:
        path.relative_to(protected)
        return True
    except ValueError:
        pass
    try:
        protected.relative_to(path)
        return True
    except ValueError:
        return False


def rel_arg(value, label):
    if not isinstance(value, str) or not value or "\0" in value or "\n" in value or "\r" in value:
        sys.exit(f"{label} must be a plain relative path")
    if value.startswith("-"):
        sys.exit(f"{label} must not start with '-'")
    path = Path(value)
    if path.is_absolute() or ".." in path.parts:
        sys.exit(f"{label} must stay inside the repo")
    return value


def symlink_component(path):
    current = Path(lexical_abs(path).anchor)
    for part in lexical_abs(path).parts[1:]:
        current = current / part
        if current.is_symlink():
            return current
        if not current.exists():
            return None
    return None


def guard_output(path):
    lexical = lexical_abs(path)
    if lexical.is_symlink():
        sys.exit(f"refusing output path {lexical}: it is a symlink; this tool does not follow symlinks")
    real = Path(os.path.realpath(lexical))
    for candidate in (lexical, real):
        root = Path(candidate.anchor)
        if candidate == root:
            sys.exit(f"refusing output path {candidate}: it is the filesystem root")
        for home in home_paths:
            if overlaps(candidate, home):
                sys.exit(f"refusing output path {candidate}: it overlaps the home directory")
        for protected in repo_paths:
            if overlaps(candidate, protected):
                sys.exit(f"refusing output path {candidate}: it overlaps the repo")
    return lexical


def marker_ok(directory):
    marker = directory / MARKER_NAME
    if marker.is_symlink() or not marker.is_file():
        return False
    try:
        fd = os.open(marker, os.O_RDONLY | os.O_NOFOLLOW)
    except OSError:
        return False
    try:
        with os.fdopen(fd, "r", encoding="utf-8") as handle:
            return handle.read() == MARKER_BODY
    except OSError:
        return False


def write_marker(directory):
    marker = directory / MARKER_NAME
    if marker.is_symlink() or marker.is_file():
        marker.unlink()
    elif marker.exists():
        sys.exit(f"refusing to write the snapshot marker over {marker}")
    fd = os.open(marker, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o644)
    with os.fdopen(fd, "w", encoding="utf-8") as handle:
        handle.write(MARKER_BODY)


def remove_owned(directory):
    directory = lexical_abs(directory)
    if directory.is_symlink():
        sys.exit(f"refusing to remove symlink {directory}")
    info = directory.lstat()
    if not stat.S_ISDIR(info.st_mode):
        sys.exit(f"refusing to remove {directory}: not a directory")
    if not marker_ok(directory):
        sys.exit(f"refusing to remove {directory}: it is not a snapshot this tool created")
    shutil.rmtree(directory)


repo_arg = lexical_abs(args.repo)
if not repo_arg.is_dir():
    sys.exit(f"repo is not a directory: {repo_arg}")
repo = repo_arg
site = rel_arg(args.site, "site dir")
if not REF_RE.fullmatch(args.ref):
    sys.exit(f"ref is not a plain commit or branch name: {args.ref}")
for skip in args.skip:
    rel_arg(skip, "--skip")
links = []
for spec in args.link:
    if not isinstance(spec, str) or "=" not in spec or "\0" in spec:
        sys.exit(f"--link must be path-in-snapshot=real-path, got {spec!r}")
    inner, target = spec.split("=", 1)
    inner = rel_arg(inner, "--link path")
    if not isinstance(target, str) or not target or "\0" in target or "\n" in target:
        sys.exit("--link target must be a plain path")
    links.append((inner, target))

toplevel = Path(git_toplevel().strip())
repo_paths = []
for path in (repo_arg, toplevel):
    for variant in variants(path):
        if variant not in repo_paths:
            repo_paths.append(variant)
home_paths = variants(Path.home())
out = guard_output(args.out)

if out.exists():
    if not args.overwrite:
        sys.exit(f"{out} already exists; refusing to replace it. Pass --overwrite to replace a snapshot this tool created")
    if not out.is_dir():
        sys.exit(f"{out} exists and is not a directory")
    if not marker_ok(out):
        sys.exit(f"{out} is not a snapshot this tool created (missing {MARKER_NAME}); refusing to replace it")
dirty = git_status_site(site).strip()
if dirty:
    sys.exit(f"{args.site} has uncommitted files; commit them before taking a snapshot:\n{dirty}")

tmp = Path(tempfile.mkdtemp(prefix="award-polish-snapshot-"))
tmp_id = tmp.lstat()
published = False
try:
    write_marker(tmp)
    archive = git_archive(args.ref, site)
    extract_archive(tmp, archive)
    write_marker(tmp)
    site_root = tmp / site
    for inner, target in links:
        dest = site_root / inner
        if not lexical_abs(dest).is_relative_to(lexical_abs(site_root)):
            sys.exit(f"--link path escapes the site directory: {inner}")
        target_path = lexical_abs(target)
        linked = symlink_component(target_path)
        if linked is not None:
            sys.exit(f"refusing to follow a symlink in --link target: {linked}")
        if not target_path.exists():
            sys.exit(f"--link target does not exist: {target_path}")
        cursor = site_root
        for part in Path(inner).parts[:-1]:
            cursor = cursor / part
            if cursor.is_symlink():
                sys.exit(f"refusing to follow a symlink in the snapshot: {cursor}")
        if dest.is_symlink() or dest.exists():
            sys.exit(f"--link path already exists in the snapshot: {inner}")
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.symlink_to(target_path)
    run_asset_check(site_root, args.skip)
    if out.exists():
        if not marker_ok(out):
            sys.exit(f"{out} changed and is no longer a snapshot this tool created; refusing to replace it")
        backup = guard_output(out.with_name(out.name + ".award-polish-old"))
        if backup.exists() or backup.is_symlink():
            sys.exit(f"{backup} already exists; move it aside before replacing the snapshot")
        os.rename(out, backup)
        try:
            shutil.move(str(tmp), str(out))
        except Exception:
            os.rename(backup, out)
            raise
        remove_owned(backup)
    else:
        out.parent.mkdir(parents=True, exist_ok=True)
        if out.exists() or out.is_symlink():
            sys.exit(f"{out} appeared during the snapshot; refusing to replace it")
        try:
            os.rename(tmp, out)
        except OSError:
            if out.exists() or out.is_symlink():
                sys.exit(f"{out} appeared during the snapshot; refusing to replace it")
            shutil.move(str(tmp), str(out))
    published = True
finally:
    if not published and tmp.exists():
        now = tmp.lstat()
        if now.st_dev == tmp_id.st_dev and now.st_ino == tmp_id.st_ino and stat.S_ISDIR(now.st_mode) and not tmp.is_symlink():
            shutil.rmtree(tmp)

final_site = out / site
print(f"Snapshot {final_site} ready ({args.ref} = {git_short_ref(args.ref).strip()})")
