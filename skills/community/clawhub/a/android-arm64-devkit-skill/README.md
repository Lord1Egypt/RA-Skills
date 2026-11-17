# android-arm64-devkit-skill

Build **and** deploy Android APKs from an **ARM64 Linux** host
(NVIDIA DGX Spark, Raspberry Pi, ARM servers, ARM cloud instances).
No x86-64 machine required.

Google ships `aapt2`, `aidl` and `zipalign` as **x86-64** binaries only, so a
normal Android Gradle build dies on `aarch64` with:

```
aapt2: cannot execute binary file: Exec format error
```

Debian already packages **native aarch64** builds of all of them. This repo wires
those into Gradle — and then covers the part everybody forgets: pushing the APK
to a real device over adb and **proving it actually runs**.

## Quick start

```bash
# 1) native aarch64 toolchain (Debian/Ubuntu)
sudo apt-get install -y android-sdk-build-tools android-sdk-platform-tools android-libaapt
./scripts/setup-aapt2-arm64.sh

# 2) point Gradle at the native aapt2
./scripts/setup-aapt2-arm64.sh --write-gradle-property path/to/project

# 3) build
cd path/to/project && ./gradlew clean assembleDebug

# 4) deploy and verify on a real device
cp config.example.sh config.sh && $EDITOR config.sh
./scripts/adb-connect.sh
./scripts/adb-install-verify.sh app/build/outputs/apk/debug/app-debug.apk
```

## Part 1 — Build on ARM64

The whole fix is one Gradle property pointing at the Debian aarch64 `aapt2`:

```properties
android.aapt2FromMavenOverride=/usr/lib/android-sdk/build-tools/debian/aapt2
```

`setup-aapt2-arm64.sh` checks what you have, tells you which binaries are the
wrong architecture, and installs the right ones.

### Why `clean` matters

A build that reports `UP-TO-DATE` **proves nothing** — it means `aapt2` never ran.
To actually validate an ARM64 toolchain you must force the resource tasks:

```bash
./gradlew clean assembleDebug
# look for "N actionable tasks: M executed" with M > 0
```

### Caveats

- Tested with **AGP 8.x**. Debian's `aapt2` reports version `2.19-debian`
  (older than the AGP-bundled one); it works via the override, but re-test on
  a new major AGP.
- Projects using **AIDL** or **zipalign** need those pointed at the Debian
  aarch64 binaries too — they exist and the setup script reports them.
- `d8`/`apksigner` are shell scripts wrapping the JVM, so they are
  architecture-independent already.

## Part 2 — Deploy and verify over adb

Two transports, pick whichever your device is on:

| Situation | Transport |
|---|---|
| Device plugged into a machine you can ssh into | USB |
| Device exposes wireless debugging on a VPN (e.g. Tailscale) | TCP |

```bash
./scripts/adb-connect.sh              # discovers the port, never assumes 5555
./scripts/adb-install-verify.sh app.apk
./scripts/adb-disconnect.sh           # clean teardown
```

`adb-install-verify.sh` does not just install — it **verifies**:

1. prints the installed version and install time
2. launches the main activity
3. checks the window that actually has focus
4. checks the process is alive
5. greps logcat for crashes
6. takes a screenshot and flags the "cached black framebuffer" trap

## Examples

[`examples/README.md`](examples/README.md) captures a real run: toolchain
diagnosis (Google `aapt2` x86-64 vs the Debian **aarch64** build), the
scaffolded project tree, the `gradle.properties` override, and the self-test
suite (`36 passed, 0 failed`).

## Troubleshooting

See [`docs/troubleshooting.md`](docs/troubleshooting.md) — every trap below was
hit for real, not theorised:

- PowerShell `>` corrupts binary captures (writes UTF-16) → use `cmd /c`
- stale network mounts that look mounted but return empty
- a writable directory that is **local**, not the remote host
- the wireless adb port is **dynamic**, never a constant
- OEM lockscreens that return a black screenshot while the app has focus
- adb key mismatch between two hosts driving the same device

## License

MIT — see [LICENSE](LICENSE).
