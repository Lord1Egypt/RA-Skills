---
name: "android-lab"
description: "Install Android Lab's local Docker images, then build an Android app, boot a private emulator, install APKs and inspect the UI from the app's own directory. Use when an Android build or emulator is needed without a host SDK or ADB."
license: WTFPL
homepage: https://github.com/psyb0t/android-lab
user-invocable: true
metadata:
  openclaw:
    emoji: "🤖"
    requires:
      bins:
        - docker
        - git
        - curl
permissions:
  filesystem: "Mounts the Android project directory into the lab containers. Gradle caches, the debug signing identity, the emulator disk and screenshots are written under the project's .android-lab/ directory."
  shell: "Runs docker to build the local images and to start the build, emulator and device-helper containers; runs git and curl to fetch the selected Android Lab release."
  network: "Downloads the Android Lab release from GitHub and Android SDK components from dl.google.com during the image build. Gradle downloads the project's dependencies. The emulator viewer and forwarded ports bind 127.0.0.1 only."
---

# Android Lab

Android Lab is a set of locally built Docker images: a tool image with the Android SDK, Gradle runner and device scripts, and an emulator image. Everything runs from the Android project's own directory. No lab checkout, host SDK or host ADB is needed.

Run every command from the Android project root. Never use host `adb`, a host Android SDK, USB devices or physical phones. All device commands reach only the lab's private emulator.

## 1. Check the host

- Linux on x86_64 with Docker and Docker Compose v2, plus `git` and `curl`.
- The emulator needs `/dev/kvm` on the Docker host. Builds do not.
- `docker info` must succeed as the current user.

## 2. Pick a version

Use the version the project already pins: look for `android-lab:<version>` or `ANDROID_LAB_VERSION` in its Makefile, Dockerfiles, CI workflows and docs. If it pins none, list the releases and take the highest:

```bash
git ls-remote --tags --refs https://github.com/psyb0t/android-lab.git 'v*' | sed 's|.*refs/tags/v||' | sort -V | tail -1
```

Tell the user which version you chose and why. Use that exact version for every command below, written here as `<version>`.

## 3. Get license consent

The image build downloads the Android SDK. Show the user https://developer.android.com/studio/terms and ask whether they accept it. Only after an explicit yes, set `ANDROID_LAB_ACCEPT_ANDROID_LICENSES=yes`. Never accept it on their behalf.

## 4. Install the images

Download the installer from the release tag, read it, then run it as a file:

```bash
curl -fsSLo /tmp/android-lab-install.sh https://raw.githubusercontent.com/psyb0t/android-lab/v<version>/install.sh
ANDROID_LAB_ACCEPT_ANDROID_LICENSES=yes bash /tmp/android-lab-install.sh <version> --emulator
```

It builds `android-lab:<version>` and `android-lab:<version>-emulator-api36`, keeps images that already exist, and prints their names. Drop `--emulator` when only builds are needed. A first build takes several minutes. When the installer runs inside a container that uses the host Docker socket, add `--work-dir <dir>` with a directory that exists at the same path on the host.

## 5. Build, run and inspect

Read [commands](references/setup.md) before running anything here. It has the exact `docker run` commands for:

- a Gradle task such as `:app:assembleDebug`;
- starting the emulator and opening its viewer;
- installing an APK, starting an app, UI layout, screenshots, shell and file transfer;
- forwarding a device port to the host and stopping the lab.

Prefer the project's own Makefile targets when it already integrates Android Lab. Inspect UI with the compact layout JSON first, then screenshots.

## Boundaries

- Keep `.android-lab/` in the project's `.gitignore`. It holds caches, the signing identity and the saved phone. Do not delete it.
- Stop the lab when the user is done, unless they asked to keep it running. Stopping keeps the phone disk.
- Do not substitute a different image version, pull SDK images from a registry, or publish the built images.

## Done when

The requested build, install or inspection command exited 0, and its output exists: the APK under the project's build directory, or `layout.json` and `screenshot.png` under `.android-lab/shared/artifacts/`. Report the version used and whether the emulator is still running.
