#!/usr/bin/env python3
"""
Check if TeamTalk SDK is installed on the current system.
Detects platform, searches common paths, and reports version.
"""
import os
import sys
import struct
import platform

COMMON_PATHS = [
    os.path.expanduser("~/teamtalk-sdk"),
    os.path.expanduser("~/TeamTalk5"),
    os.path.expanduser("~/TeamTalkSDK"),
    "/opt/teamtalk-sdk",
    "/usr/local/teamtalk-sdk",
    "/usr/local/TeamTalk5",
    "C:\\Program Files\\TeamTalk 5 SDK",
    "C:\\TeamTalk5",
]

PLATFORM_ALIASES = {
    "win32": "win64",
    "windows": "win64",
    "win64": "win64",
    "darwin": "macos",
    "macos": "macos",
    "mac": "macos",
    "linux": "linux",
    "linux2": "linux",
    "ubuntu": "linux",
    "android": "android",
    "ios": "ios",
    "raspbian": "raspbian",
    "raspberrypi": "raspbian",
    "armhf": "raspbian",
}


def detect_platform():
    system = platform.system().lower()
    machine = platform.machine().lower()

    if system == "windows":
        return "win64"
    elif system == "darwin":
        return "macos"
    elif system == "linux":
        if machine in ("aarch64", "armv7l", "armhf"):
            return "raspbian"
        return "linux"
    elif "android" in system:
        return "android"
    return "linux"


def detect_sdk_version(sdk_path):
    version_file = os.path.join(sdk_path, "version.txt")
    if os.path.isfile(version_file):
        with open(version_file) as f:
            return f.read().strip()
    for root, dirs, files in os.walk(sdk_path):
        for f in files:
            if f.lower() in ("teamtalk5.dll", "libteamtalk.so", "libteamtalk.dylib"):
                ver = os.path.basename(os.path.dirname(root))
                if ver.startswith("v"):
                    return ver
    for root, dirs, files in os.walk(sdk_path):
        for f in files:
            if f == "TeamTalk5.def":
                return os.path.basename(os.path.dirname(root))
    return None


def find_sdk_dirs():
    sdk_dirs = []
    for path in COMMON_PATHS:
        expanded = os.path.expandvars(path)
        if os.path.isdir(expanded):
            version = detect_sdk_version(expanded)
            sdk_dirs.append((expanded, version))
    return sdk_dirs


def find_dlls(sdk_path):
    dlls = []
    for root, dirs, files in os.walk(sdk_path):
        for f in files:
            if f.lower() in ("teamtalk5.dll", "libteamtalk.so", "libteamtalk.dylib",
                              "teamtalk5pro.dll", "libteamtalk5pro.so"):
                dlls.append(os.path.join(root, f))
    return dlls


def get_ubuntu_version():
    try:
        with open("/etc/os-release") as f:
            for line in f:
                if line.startswith("VERSION_ID="):
                    ver = line.split("=")[1].strip().strip('"')
                    return f"ubuntu{ver.replace('.', '')}"
    except FileNotFoundError:
        pass
    return None


def main():
    args = set(sys.argv[1:])
    detect_only = "--detect-only" in args

    plat = detect_platform()
    ubuntu_ver = get_ubuntu_version()

    if detect_only:
        info = {"platform": plat}
        if ubuntu_ver:
            info["ubuntu_version"] = ubuntu_ver
        info["arch"] = struct.calcsize("P") * 8
        info["machine"] = platform.machine()
        print(f"detected_platform={plat}")
        if ubuntu_ver:
            print(f"ubuntu_version={ubuntu_ver}")
        print(f"arch={info['arch']}-bit")
        print(f"machine={info['machine']}")
        return 0

    sdk_dirs = find_sdk_dirs()
    if not sdk_dirs:
        print(f"PLATFORM={plat}")
        if ubuntu_ver:
            print(f"UBUNTU_VERSION={ubuntu_ver}")
        print("SDK_NOT_FOUND=true")
        print("SDK_PATH=")
        print("SDK_VERSION=")
        return 1

    for path, version in sdk_dirs:
        dlls = find_dlls(path)
        edition = "professional" if any("pro" in d.lower() for d in dlls) else "standard"
        has_server = any("tt5srv" in f for f in os.listdir(path)) if os.path.isdir(path) else False

        print(f"PLATFORM={plat}")
        if ubuntu_ver:
            print(f"UBUNTU_VERSION={ubuntu_ver}")
        print(f"SDK_FOUND=true")
        print(f"SDK_PATH={path}")
        print(f"SDK_VERSION={version or 'unknown'}")
        print(f"SDK_EDITION={edition}")
        print(f"HAS_SERVER={'true' if has_server else 'false'}")
        print(f"DLL_COUNT={len(dlls)}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
