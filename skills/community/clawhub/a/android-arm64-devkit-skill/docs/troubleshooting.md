# Troubleshooting

Every entry below was hit for real while building and deploying on an ARM64
host. Symptoms first, cause second, fix last.

## Build

### `aapt2: cannot execute binary file: Exec format error`

**Cause.** Google publishes `aapt2` (and `aidl`, `zipalign`) for
`linux`, `osx` and `windows` — all **x86-64**. On an `aarch64` host the kernel
refuses to exec them. Naming is misleading: the artifact is called
`aapt2-<version>-linux.jar`, but "linux" here means *x86-64 Linux*.

Confirm it yourself:

```bash
unzip -o -q ~/.gradle/caches/modules-2/files-2.1/com.android.tools.build/aapt2/*/*/aapt2-*-linux.jar -d /tmp/x
file /tmp/x/aapt2     # -> ELF 64-bit ... x86-64
```

**Fix.** Point Gradle at a native aarch64 build:

```properties
android.aapt2FromMavenOverride=/usr/lib/android-sdk/build-tools/debian/aapt2
```

Debian ships native aarch64 builds via `android-libaapt` (plus `android-sdk-build-tools`
for `aidl` / `zipalign` / `split-select`). `scripts/setup-aapt2-arm64.sh` reports
what you have and installs what is missing.

### The build "succeeds" but proves nothing

**Symptom.** `BUILD SUCCESSFUL`, but every task is `UP-TO-DATE`.

**Cause.** Gradle skipped the resource tasks, so `aapt2` never executed. The
output came from a previous build (or was never produced at all).

**Fix.** Force the work and read the counters:

```bash
./gradlew clean assembleDebug
# require "N actionable tasks: M executed" with M > 0,
# and a real task list containing packageDebugResources / packageDebug
```

### Works with one AGP, fails with another

Debian's `aapt2` reports an older version than the AGP-bundled one. It works via
the override with AGP 8.x, but the override option is explicitly marked
**experimental** by AGP. Re-test after any AGP major upgrade. Projects using
**AIDL** or explicit **zipalign** invocations need those pointed at the Debian
aarch64 binaries as well.

## Deploy

### Wireless debugging: `cannot connect` / `Connection refused`

**Cause.** The TCP port is **not stable**. Some OEMs randomise it every time
wireless debugging restarts, so an old `5555` is stale.

**Fix.** Read the port instead of assuming it. The authoritative source is the
adb server that already owns the transport:

```bash
adb devices -l          # look for an entry like  <name>:<port>
```

Or read it over USB:

```bash
adb -s <SERIAL> shell getprop service.adb.tcp.port
```

If that is empty, wireless debugging is not exposed. `scripts/adb-connect.sh`
does this discovery for you and refuses to guess.

### `unauthorized`

**Cause.** The device authorizes specific host keys. The key on this host is not
the one that was accepted, so the device refuses it. Two hosts driving one
device will each have their own key.

**Fix.** Use the key that is already authorized, copied from that host (with
permissions `600`), then restart the local adb server:

```bash
cp /path/from/authorized/host/.android/adbkey      ~/.android/adbkey
cp /path/from/authorized/host/.android/adbkey.pub  ~/.android/adbkey.pub
chmod 600 ~/.android/adbkey
adb kill-server && adb start-server
```

Otherwise accept the "Allow USB debugging" prompt on the device while it is
attached over USB.

### `error: device offline` / shell hangs

**Fix.** A wedged adb server is the usual cause:

```bash
adb kill-server && adb start-server
```

`scripts/adb-disconnect.sh --restart-server` does this.

### The device disappears over a VPN after a few minutes

**Cause.** Mobile OEMs put the VPN client into deep sleep when the screen has
been off for a while, so `adbd` stops answering on the virtual interface.
Wireless debugging over a VPN is not a always-on transport.

**Fix.** Wake the VPN client on the device, then reconnect. When the device is
also attached over USB, use USB as the primary transport and the VPN as fallback.

## Transfers and captures

### A binary file is copied but arrives corrupted

**Cause.** PowerShell's `>` redirection writes **UTF-16 text**, not raw bytes.
Piping a PNG through it produces a broken file with the right-looking name.

**Fix.** Redirect inside `cmd`, which is binary-safe:

```
cmd /c "adb -s <SERIAL> exec-out screencap -p > C:\path\shot.png"
```

When running adb on a remote Windows host over ssh, the same applies:

```bash
ssh <win-host> 'cmd /c "adb ... exec-out screencap -p > C:\path\shot.png"'
```

### A shared/network mount looks mounted but is empty

**Cause.** A stale network mount can still appear in the mount table while
returning an empty directory listing — and writes may silently fail.

**Diagnosis.** Check both the mount table *and* an actual listing:

```bash
mount | grep <mountpoint>
ls -la <mountpoint>        # empty listing on a mounted path == suspect
```

### A directory is writable but is not the remote host

**Cause.** A path that *looks* like the remote filesystem can be a plain local
directory with the same name. Copying there succeeds and goes nowhere.

**Diagnosis.** Confirm the path is a real mount point (`findmnt` / `mount`)
before trusting it, and always verify the transfer:

```bash
md5sum local-file
ssh <host> 'powershell -NoProfile -Command "(Get-FileHash <path> -Algorithm MD5).Hash"'
```

Compare the hashes. A transfer that is not verified is not a transfer.

### Screenshot is a black image while the app has focus

**Cause.** Some OEM lockscreens keep a cached black framebuffer and hand it to
`screencap` even though `dumpsys window` reports your activity as focused. The
giveaway is a suspiciously small and constant file size.

**Fix.** Wake the display, dismiss the lockscreen, then capture:

```bash
adb -s <SERIAL> shell input keyevent 224     # WAKEUP
adb -s <SERIAL> shell svc power stayon true
adb -s <SERIAL> shell input keyevent 3       # HOME
adb -s <SERIAL> shell dumpsys window | grep mCurrentFocus   # confirm it is you
adb -s <SERIAL> exec-out screencap -p > shot.png
```

`adb-install-verify.sh` warns automatically when the capture is below ~30 KB.
