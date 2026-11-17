#!/usr/bin/env python3
"""Copy one entry into the staging tree, robustly.

stage_copy.py SRC DEST [--exclude NAME]... [--hash] [--hash-prefix PREFIX]

What `cp -Rp` gets wrong on a real home directory, done right:

- symlinks are copied as symlinks, dangling ones included, never followed;
- unreadable files, vanished files and special files (sockets, fifos,
  devices) are skipped and *recorded* instead of sinking the whole copy;
- file and directory modes are preserved;
- `--exclude` prunes by basename (exact or fnmatch pattern) at any depth;
- `--hash` emits a SHA-256 per copied regular file, keyed by the path
  relative to DEST (posix separators). `--hash-prefix files/home/dev/site`
  prefixes every key, producing manifest-ready `checksums` keys.

DEST must not already exist. On a fatal error the script removes everything
it created and exits non-zero. Per-item problems are not fatal: they land in
the `skipped` array of the JSON printed to stdout, and the exit code stays 0.

This script only copies. It never decides what should travel — that is the
skill's job — and it never writes outside DEST.
"""

import argparse
import fnmatch
import hashlib
import json
import os
import shutil
import stat
import sys

CHUNK = 1024 * 1024


def fail(message):
    print(f"stage_copy: {message}", file=sys.stderr)
    sys.exit(1)


def is_excluded(name, patterns):
    return any(name == p or fnmatch.fnmatch(name, p) for p in patterns)


def sha256_of(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        while True:
            chunk = handle.read(CHUNK)
            if not chunk:
                break
            digest.update(chunk)
    return digest.hexdigest()


class Copier:
    def __init__(self, excludes, want_hash, hash_prefix):
        self.excludes = excludes
        self.want_hash = want_hash
        self.hash_prefix = hash_prefix
        self.result = {
            "copied_files": 0,
            "copied_dirs": 0,
            "copied_symlinks": 0,
            "bytes": 0,
            "excluded": [],
            "skipped": [],
        }
        if want_hash:
            self.result["hashes"] = {}

    def skip(self, path, reason):
        self.result["skipped"].append({"path": str(path), "reason": reason})

    def hash_key(self, rel):
        if not self.hash_prefix:
            return rel
        return f"{self.hash_prefix.rstrip('/')}/{rel}" if rel else self.hash_prefix.rstrip("/")

    def copy_symlink(self, src, dest):
        target = os.readlink(src)
        os.symlink(target, dest)
        self.result["copied_symlinks"] += 1

    def copy_file(self, src, dest, rel):
        shutil.copy2(src, dest, follow_symlinks=False)
        self.result["copied_files"] += 1
        self.result["bytes"] += os.lstat(dest).st_size
        if self.want_hash:
            self.result["hashes"][self.hash_key(rel)] = sha256_of(dest)

    def copy_entry(self, src, dest, rel):
        """Copies one non-directory entry, recording rather than raising."""
        try:
            mode = os.lstat(src).st_mode
            if stat.S_ISLNK(mode):
                self.copy_symlink(src, dest)
            elif stat.S_ISREG(mode):
                self.copy_file(src, dest, rel)
            else:
                self.skip(src, "special file (socket, fifo, or device)")
        except FileNotFoundError:
            self.skip(src, "vanished while copying")
        except PermissionError:
            self.skip(src, "permission denied")
        except OSError as error:
            self.skip(src, f"could not copy: {error.strerror or error}")

    def copy_tree(self, src_root, dest_root):
        # Directory modes are applied after their contents land, deepest
        # first, so a read-only source directory does not lock us out of
        # writing its own children into the copy.
        finished_dirs = []
        os.makedirs(dest_root)
        finished_dirs.append((src_root, dest_root))
        self.result["copied_dirs"] += 1

        def on_error(error):
            self.skip(error.filename or src_root, "directory not readable")

        for dirpath, dirnames, filenames in os.walk(
            src_root, topdown=True, onerror=on_error, followlinks=False
        ):
            rel_dir = os.path.relpath(dirpath, src_root)
            kept = []
            for name in sorted(dirnames):
                if is_excluded(name, self.excludes):
                    self.result["excluded"].append(
                        os.path.normpath(os.path.join(rel_dir, name)).replace(os.sep, "/")
                    )
                else:
                    kept.append(name)
            dirnames[:] = kept

            dest_dir = (
                dest_root
                if rel_dir == "."
                else os.path.join(dest_root, rel_dir)
            )
            for name in kept:
                sub_src = os.path.join(dirpath, name)
                sub_dest = os.path.join(dest_dir, name)
                # A symlink to a directory lists under dirnames on some
                # platforms' walk order but must stay a link in the copy.
                if os.path.islink(sub_src):
                    dirnames.remove(name)
                    rel = os.path.normpath(os.path.join(rel_dir, name)).replace(os.sep, "/")
                    self.copy_entry(sub_src, sub_dest, rel)
                    continue
                try:
                    os.mkdir(sub_dest)
                    self.result["copied_dirs"] += 1
                    finished_dirs.append((sub_src, sub_dest))
                except OSError as error:
                    dirnames.remove(name)
                    self.skip(sub_src, f"could not create directory in staging: {error.strerror or error}")

            for name in sorted(filenames):
                if is_excluded(name, self.excludes):
                    self.result["excluded"].append(
                        os.path.normpath(os.path.join(rel_dir, name)).replace(os.sep, "/")
                    )
                    continue
                rel = os.path.normpath(os.path.join(rel_dir, name)).replace(os.sep, "/")
                self.copy_entry(os.path.join(dirpath, name), os.path.join(dest_dir, name), rel)

        for sub_src, sub_dest in reversed(finished_dirs):
            try:
                shutil.copystat(sub_src, sub_dest, follow_symlinks=False)
            except OSError:
                self.skip(sub_src, "could not preserve directory metadata")


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("src", help="file, directory, or symlink to copy")
    parser.add_argument("dest", help="destination path inside staging; must not exist")
    parser.add_argument(
        "--exclude",
        action="append",
        default=[],
        metavar="NAME",
        help="basename or fnmatch pattern to prune, repeatable",
    )
    parser.add_argument(
        "--hash", action="store_true", help="emit SHA-256 per copied regular file"
    )
    parser.add_argument(
        "--hash-prefix",
        default="",
        metavar="PREFIX",
        help="prefix for hash keys, e.g. the archive path of DEST",
    )
    args = parser.parse_args()

    src = os.path.abspath(args.src)
    dest = os.path.abspath(args.dest)

    try:
        src_mode = os.lstat(src).st_mode
    except OSError as error:
        fail(f"cannot read {args.src}: {error.strerror or error}")
    if os.path.lexists(dest):
        fail(f"{args.dest} already exists; staging copies never overwrite")
    if (dest + os.sep).startswith(src + os.sep):
        fail(f"{args.dest} is inside {args.src}; the copy would recurse into itself")

    # Track the topmost path this run creates, so a fatal error can undo
    # exactly what this run did and nothing more.
    created_root = dest
    parent = os.path.dirname(dest)
    while parent and not os.path.exists(parent):
        created_root = parent
        parent = os.path.dirname(parent)
    try:
        os.makedirs(os.path.dirname(dest), exist_ok=True)
    except OSError as error:
        fail(f"cannot create parent of {args.dest}: {error.strerror or error}")

    copier = Copier(args.exclude, args.hash, args.hash_prefix)
    try:
        if stat.S_ISDIR(src_mode):
            copier.copy_tree(src, dest)
        else:
            # With a prefix, the prefix alone already names this one entry.
            copier.copy_entry(
                src, dest, "" if args.hash_prefix else os.path.basename(dest)
            )
    except BaseException:
        # created_root is a regular file when SRC was one; rmtree would
        # silently leave it behind.
        if os.path.isdir(created_root) and not os.path.islink(created_root):
            shutil.rmtree(created_root, ignore_errors=True)
        else:
            try:
                os.unlink(created_root)
            except OSError:
                pass
        raise

    copier.result["src"] = src
    copier.result["dest"] = dest
    json.dump(copier.result, sys.stdout, indent=2, sort_keys=True)
    print()


if __name__ == "__main__":
    main()
