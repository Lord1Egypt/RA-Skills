#!/usr/bin/env python3
"""One-shot software inventory across every present package manager.

sw_inventory.py [--apps] [--managers a,b,c] [--diff MANIFEST.json]

One invocation per manager instead of one query per package. Output is a
single JSON object:

  software          entries shaped for the manifest's `software` array
  apps              GUI applications by bundle id (with --apps)
  absent_managers   managers this machine does not have — not errors
  errors            managers that were present but failed to answer
  unmanaged_binaries  ~/.local/bin, /usr/local/bin, Go bin — the tarball tail
  diff              manifest vs this machine (with --diff)

The `manager` strings match references/software-inventory.md exactly. This
script only enumerates and compares: it never installs, never uninstalls,
and never talks to a registry. What to do about a missing package is the
skill's and the user's decision.
"""

import argparse
import json
import os
import plistlib
import re
import shutil
import subprocess
import sys

TIMEOUT = 60


def run(argv, timeout=TIMEOUT, check=True):
    done = subprocess.run(
        argv,
        capture_output=True,
        text=True,
        timeout=timeout,
        stdin=subprocess.DEVNULL,
        env={**os.environ, "LC_ALL": "C", "HOMEBREW_NO_AUTO_UPDATE": "1"},
    )
    if check and done.returncode != 0:
        detail = done.stderr.strip().splitlines()
        raise RuntimeError(detail[0] if detail else f"{argv[0]} exited {done.returncode}")
    return done.stdout


def entry(manager, name, version=None, **extra):
    item = {"manager": manager, "name": name}
    if version:
        item["version"] = version
    item.update({k: v for k, v in extra.items() if v})
    return item


# --- one function per manager; each returns a list of entries ---------------

# `brew list --versions` cannot carry `--full-name` on current Homebrew, so
# taps and versions come from the JSON dump instead — one (slow) call shared
# by the brew and brew-cask listers.
_brew_info_cache = None


def brew_info():
    global _brew_info_cache
    if _brew_info_cache is None:
        _brew_info_cache = json.loads(
            run(["brew", "info", "--json=v2", "--installed"], timeout=300)
        )
    return _brew_info_cache


def list_brew():
    out = []
    for item in brew_info().get("formulae", []):
        tap = item.get("tap")
        installed = item.get("installed") or [{}]
        # A tapped formula's tap is its source; the short name is what the
        # manifest carries. homebrew/core is the default, not a source.
        out.append(entry(
            "brew",
            item.get("name") or item.get("full_name"),
            installed[0].get("version"),
            source=None if tap in (None, "homebrew/core") else tap,
        ))
    return out


def list_brew_cask():
    out = []
    for item in brew_info().get("casks", []):
        tap = item.get("tap")
        out.append(entry(
            "brew-cask",
            item.get("token") or item.get("full_token"),
            item.get("installed"),
            source=None if tap in (None, "homebrew/cask") else tap,
        ))
    return out


def list_brew_tap():
    return [entry("brew-tap", line.strip()) for line in run(["brew", "tap"]).splitlines() if line.strip()]


def node_runtime():
    try:
        return "node " + run(["node", "--version"]).strip().lstrip("v")
    except (RuntimeError, OSError, subprocess.TimeoutExpired):
        return None


def list_npm_like(manager, binary):
    # npm exits non-zero on unmet peer dependencies while still printing a
    # complete JSON tree; the parse, not the exit code, is the check here.
    data = json.loads(run([binary, "ls", "-g", "--depth=0", "--json"], check=False))
    if isinstance(data, list):  # pnpm wraps in a one-element list
        data = data[0] if data else {}
    runtime = node_runtime()
    out = []
    for name, info in sorted((data.get("dependencies") or {}).items()):
        if name == "npm":
            continue
        version = info.get("version") if isinstance(info, dict) else None
        out.append(entry(manager, name, version, runtime=runtime))
    return out


def list_cargo():
    out = []
    for line in run(["cargo", "install", "--list"]).splitlines():
        match = re.match(r"^(\S+) v([^\s:]+)", line)
        if match:
            out.append(entry("cargo", match.group(1), match.group(2)))
    return out


def list_pipx():
    data = json.loads(run(["pipx", "list", "--json"]))
    out = []
    for venv in sorted((data.get("venvs") or {})):
        meta = data["venvs"][venv].get("metadata", {}).get("main_package", {})
        out.append(entry("pipx", meta.get("package", venv), meta.get("package_version")))
    return out


def list_uv_tool():
    out = []
    for line in run(["uv", "tool", "list"]).splitlines():
        match = re.match(r"^(\S+) v(\S+)", line)
        if match:
            out.append(entry("uv-tool", match.group(1), match.group(2)))
    return out


def list_gem():
    out = []
    for line in run(["gem", "list", "--local"]).splitlines():
        match = re.match(r"^(\S+) \(([^)]*)\)", line)
        if not match or "default: " in match.group(2):
            continue
        out.append(entry("gem", match.group(1), match.group(2).split(",")[0].strip()))
    return out


def list_mas():
    out = []
    for line in run(["mas", "list"]).splitlines():
        match = re.match(r"^(\d+)\s+(.+?)\s+\(([^)]*)\)\s*$", line)
        if match:
            out.append(entry("mas", match.group(2), match.group(3), id=match.group(1)))
    return out


def list_vscode_ext():
    out = []
    for binary in ("code", "cursor", "code-insiders", "codium"):
        if not shutil.which(binary):
            continue
        for line in run([binary, "--list-extensions", "--show-versions"], timeout=120).splitlines():
            name, _, version = line.strip().partition("@")
            if name:
                out.append(
                    entry("vscode-ext", name, version or None, editor=binary if binary != "code" else None)
                )
    return out


def list_apt():
    return [entry("apt", n) for n in run(["apt-mark", "showmanual"]).split()]


def list_dnf():
    out = []
    for line in run(["dnf", "repoquery", "--userinstalled", "--qf", "%{name} %{version}"], timeout=300).splitlines():
        parts = line.split()
        if parts:
            out.append(entry("dnf", parts[0], parts[1] if len(parts) > 1 else None))
    return out


def list_pacman():
    out = []
    for line in run(["pacman", "-Qe"]).splitlines():
        parts = line.split()
        if parts:
            out.append(entry("pacman", parts[0], parts[1] if len(parts) > 1 else None))
    return out


def list_snap():
    lines = run(["snap", "list"]).splitlines()
    out = []
    for line in lines[1:]:
        parts = line.split()
        if parts:
            out.append(entry("snap", parts[0], parts[1] if len(parts) > 1 else None))
    return out


def list_flatpak():
    out = []
    for line in run(["flatpak", "list", "--app", "--columns=application,version"]).splitlines():
        parts = line.split("\t")
        if parts and parts[0].strip():
            out.append(entry("flatpak", parts[0].strip(), parts[1].strip() if len(parts) > 1 else None))
    return out


def list_mise():
    out = []
    for line in run(["mise", "ls", "--current"]).splitlines():
        parts = line.split()
        if len(parts) >= 2 and not parts[0].startswith(("#", "Tool")):
            out.append(entry("mise", parts[0], parts[1]))
    return out


def list_asdf():
    out = []
    for line in run(["asdf", "current"]).splitlines():
        parts = line.split()
        if len(parts) >= 2 and parts[1] not in ("______", "unknown") and not parts[0].startswith("Name"):
            out.append(entry("asdf", parts[0], parts[1]))
    return out


MANAGERS = {
    "brew": ("brew", list_brew),
    "brew-cask": ("brew", list_brew_cask),
    "brew-tap": ("brew", list_brew_tap),
    "npm-g": ("npm", lambda: list_npm_like("npm-g", "npm")),
    "pnpm-g": ("pnpm", lambda: list_npm_like("pnpm-g", "pnpm")),
    "cargo": ("cargo", list_cargo),
    "pipx": ("pipx", list_pipx),
    "uv-tool": ("uv", list_uv_tool),
    "gem": ("gem", list_gem),
    "mas": ("mas", list_mas),
    "vscode-ext": ("code", list_vscode_ext),
    "apt": ("apt-mark", list_apt),
    "dnf": ("dnf", list_dnf),
    "pacman": ("pacman", list_pacman),
    "snap": ("snap", list_snap),
    "flatpak": ("flatpak", list_flatpak),
    "mise": ("mise", list_mise),
    "asdf": ("asdf", list_asdf),
}


def unmanaged_binaries():
    dirs = [os.path.expanduser("~/.local/bin"), "/usr/local/bin"]
    if shutil.which("go"):
        try:
            gopath = subprocess.run(
                ["go", "env", "GOPATH"], capture_output=True, text=True, timeout=TIMEOUT
            )
            if gopath.returncode == 0 and gopath.stdout.strip():
                dirs.append(os.path.join(gopath.stdout.strip(), "bin"))
        except (OSError, subprocess.TimeoutExpired):
            pass
    found = {}
    for directory in dirs:
        try:
            names = sorted(
                n for n in os.listdir(directory)
                if not n.startswith(".") and os.access(os.path.join(directory, n), os.X_OK)
            )
        except OSError:
            continue
        if names:
            found[directory] = names
    return found


# --- GUI applications --------------------------------------------------------

def bundle_id_of(app_path):
    try:
        with open(os.path.join(app_path, "Contents", "Info.plist"), "rb") as handle:
            return plistlib.load(handle).get("CFBundleIdentifier")
    except (OSError, plistlib.InvalidFileException, ValueError):
        return None

def apps_macos(errors):
    source_names = {
        "mac_app_store": "app-store",
        "apple": "apple",
        "identified_developer": "identified-developer",
    }
    try:
        data = json.loads(run(["system_profiler", "SPApplicationsDataType", "-json"], timeout=300))
        out = []
        for item in data.get("SPApplicationsDataType", []):
            path = item.get("path")
            if not path:
                continue
            out.append({
                "name": item.get("_name"),
                "version": item.get("version"),
                "bundle_id": bundle_id_of(path),
                "path": path,
                "source": source_names.get(item.get("obtained_from"), "unknown"),
                "discovered_by": "system_profiler",
            })
        return sorted(out, key=lambda a: (a.get("name") or "").lower())
    except (RuntimeError, OSError, subprocess.TimeoutExpired, ValueError) as error:
        errors.append({"manager": "system_profiler", "reason": str(error)})

    # Fallback: walk the two Applications directories and read each bundle's
    # own Info.plist. No install source, but identity and version survive.
    out = []
    for root in ("/Applications", os.path.expanduser("~/Applications")):
        try:
            names = sorted(os.listdir(root))
        except OSError:
            continue
        for name in names:
            if not name.endswith(".app"):
                continue
            path = os.path.join(root, name)
            try:
                with open(os.path.join(path, "Contents", "Info.plist"), "rb") as handle:
                    plist = plistlib.load(handle)
            except (OSError, plistlib.InvalidFileException, ValueError):
                continue
            out.append({
                "name": plist.get("CFBundleDisplayName") or plist.get("CFBundleName") or name[:-4],
                "version": plist.get("CFBundleShortVersionString"),
                "bundle_id": plist.get("CFBundleIdentifier"),
                "path": path,
                "source": "unknown",
                "discovered_by": "plist-walk",
            })
    return out


def apps_linux():
    out = []
    seen = set()
    for root in ("/usr/share/applications", os.path.expanduser("~/.local/share/applications")):
        try:
            names = sorted(os.listdir(root))
        except OSError:
            continue
        for name in names:
            if not name.endswith(".desktop") or name in seen:
                continue
            seen.add(name)
            fields = {}
            try:
                with open(os.path.join(root, name), encoding="utf-8", errors="replace") as handle:
                    for line in handle:
                        key, _, value = line.strip().partition("=")
                        if key in ("Name", "Exec", "NoDisplay") and key not in fields:
                            fields[key] = value
            except OSError:
                continue
            if fields.get("NoDisplay") == "true":
                continue
            out.append({
                "name": fields.get("Name", name[: -len(".desktop")]),
                "desktop_id": name[: -len(".desktop")],
                "path": os.path.join(root, name),
                "source": "unknown",
                "discovered_by": "desktop-files",
            })
    return out


# --- the diff ----------------------------------------------------------------

def software_key(item):
    if item.get("manager") == "mas" and item.get("id"):
        return ("mas", str(item["id"]))
    return (item.get("manager"), item.get("name"))


def diff_against(manifest, software, apps, errored_managers=frozenset()):
    result = {
        "software": {"missing": [], "already_present": [], "version_differs": [], "manager_missing": [], "manager_errored": []},
        "apps": {"present": [], "alternate_path": [], "missing": []},
    }
    here = {software_key(item): item for item in software}
    enumerated_managers = {item.get("manager") for item in software}
    for wanted in manifest.get("software", []):
        manager = wanted.get("manager")
        # A manager whose enumeration threw gave us no inventory; calling its
        # packages "missing" would propose reinstalling what may be installed.
        if manager in errored_managers:
            result["software"]["manager_errored"].append(wanted)
            continue
        if manager in MANAGERS and manager not in enumerated_managers and not shutil.which(MANAGERS[manager][0]):
            result["software"]["manager_missing"].append(wanted)
            continue
        found = here.get(software_key(wanted))
        if found is None:
            result["software"]["missing"].append(wanted)
        elif wanted.get("version") and found.get("version") and wanted["version"] != found["version"]:
            result["software"]["version_differs"].append(
                {**wanted, "current_version": found["version"]}
            )
        else:
            result["software"]["already_present"].append(wanted)

    by_bundle = {app.get("bundle_id"): app for app in apps if app.get("bundle_id")}
    for wanted in manifest.get("apps", []):
        found = by_bundle.get(wanted.get("bundle_id"))
        if found is None:
            result["apps"]["missing"].append(wanted)
        elif wanted.get("path") and found.get("path") and wanted["path"] != found["path"]:
            result["apps"]["alternate_path"].append({**wanted, "current_path": found["path"]})
        else:
            result["apps"]["present"].append(wanted)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--apps", action="store_true", help="also enumerate GUI applications")
    parser.add_argument(
        "--managers", metavar="A,B", help="only these managers (default: every present one)"
    )
    parser.add_argument(
        "--diff", metavar="MANIFEST", help="compare a manifest.json against this machine"
    )
    args = parser.parse_args()

    wanted = set(args.managers.split(",")) if args.managers else set(MANAGERS)
    unknown = wanted - set(MANAGERS)
    if unknown:
        parser.error(f"unknown managers: {', '.join(sorted(unknown))}")

    software, absent, errors = [], [], []
    for manager in sorted(wanted):
        binary, lister = MANAGERS[manager]
        if not shutil.which(binary):
            absent.append(manager)
            continue
        try:
            software.extend(lister())
        except (RuntimeError, OSError, subprocess.TimeoutExpired, ValueError, KeyError) as error:
            errors.append({"manager": manager, "reason": str(error)})

    manifest = None
    if args.diff:
        try:
            with open(args.diff, encoding="utf-8") as handle:
                manifest = json.load(handle)
        except (OSError, ValueError) as error:
            print(f"sw_inventory: cannot read manifest {args.diff}: {error}", file=sys.stderr)
            sys.exit(1)

    # Enumerating apps costs a slow system_profiler run, so only pay for it
    # when asked, or when the diff actually has apps to compare against.
    apps = []
    if args.apps or (manifest is not None and manifest.get("apps")):
        apps = apps_macos(errors) if sys.platform == "darwin" else apps_linux()

    result = {
        "platform": "macos" if sys.platform == "darwin" else "linux",
        "software": software,
        "absent_managers": absent,
        "errors": errors,
        "unmanaged_binaries": unmanaged_binaries(),
    }
    if args.apps:
        result["apps"] = apps

    if manifest is not None:
        result["diff"] = diff_against(
            manifest, software, apps, {e["manager"] for e in errors}
        )

    json.dump(result, sys.stdout, indent=2, sort_keys=True)
    print()


if __name__ == "__main__":
    main()
