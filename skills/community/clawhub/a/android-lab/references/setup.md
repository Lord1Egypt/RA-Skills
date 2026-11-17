# Android Lab commands

Run these from the Android project root after installing the images for the chosen version. Replace `<version>` with that version.

## Build with Gradle

The project needs an executable Gradle wrapper with `distributionSha256Sum` in `gradle/wrapper/gradle-wrapper.properties`.

```bash
docker run --rm --init --user "$(id -u):$(id -g)" \
  -e HOME=/tmp -e ANDROID_LAB_WORKSPACE=/work -e ANDROID_PROJECT=. \
  -e GRADLE_TASK=:app:assembleDebug -e ANDROID_LAB_GRADLE_MAX_WORKERS=4 \
  -v "$PWD:/work" -w /work android-lab:<version> android-lab gradle
```

`GRADLE_TASK` takes one fully qualified task. Use the app's real variant, for example `:app:assembleProdDebug` for a flavoured app. `ANDROID_PROJECT` is the Gradle root relative to the current directory. `ANDROID_LAB_GRADLE_MAX_WORKERS` accepts 1 to 10. The APK lands in the project's normal build output, and Gradle state stays under `.android-lab/`.

## Emulator and device commands

These need the host Docker socket, so they mount the project at its real path. Define this once per shell:

```bash
LAB_VERSION=<version>
lab() {
  local command="$1"
  shift
  docker run --rm --init --user "$(id -u):$(id -g)" \
    --group-add "$(stat -c %g /var/run/docker.sock)" \
    -e HOME=/tmp -e ANDROID_LAB_WORKSPACE="$PWD" \
    -e ANDROID_LAB_DEV_IMAGE="android-lab:$LAB_VERSION" \
    -e ANDROID_LAB_EMULATOR_IMAGE="android-lab:$LAB_VERSION-emulator-api36" \
    -e ANDROID_LAB_UID="$(id -u)" -e ANDROID_LAB_GID="$(id -g)" \
    -e ANDROID_LAB_VNC_HOST_PORT="${ANDROID_LAB_VNC_HOST_PORT:-61326}" \
    "$@" \
    -v "$PWD:$PWD" -v /var/run/docker.sock:/var/run/docker.sock -w "$PWD" \
    "android-lab:$LAB_VERSION" android-lab "$command"
}
```

Pass a command's inputs as extra `-e NAME=value` arguments after the command name.

```bash
lab start
lab device-info
lab apk-install -e APK=app/build/outputs/apk/debug/app-debug.apk
lab app-start -e PACKAGE_NAME=com.example.app -e ACTIVITY=.MainActivity
lab ui-layout
lab screenshot
lab stop
```

`start` boots the emulator, or reuses the running one, and waits until Android is ready. The viewer is at `http://127.0.0.1:61326/vnc.html?autoconnect=true&resize=scale`. Set `ANDROID_LAB_VNC_HOST_PORT` before `lab start` to use another port. `stop` removes the containers and keeps the saved phone under `.android-lab/shared/`.

| Command | Inputs | Result |
| --- | --- | --- |
| `status` | | Lists this project's lab containers. |
| `restart` | | Restarts the emulator without resetting its disk. |
| `device-info` | | Waits for boot, then prints the API level, Android release and device model. |
| `apk-install` | `APK` | Installs or updates an APK. The path is relative to the project root and must stay inside it. |
| `app-start` | `PACKAGE_NAME`, `ACTIVITY` | Starts an activity. |
| `app-stop` | `PACKAGE_NAME` | Force-stops an app. |
| `app-current` | | Prints the foreground package and activity. |
| `home-role-set` | `PACKAGE_NAME` | Makes a launcher app the Home app. |
| `home-start` | | Opens the Home screen. |
| `ui-layout` | | Writes `layout.json`, a compact list of visible elements with bounds and centers, plus `window.xml`. |
| `uiautomator-dump` | | Writes the raw UIAutomator XML. |
| `screenshot` | | Writes `screenshot.png`. |
| `device-shell` | `DEVICE_COMMAND` | Runs one shell command on the device. |
| `file-push` | `ARTIFACT_FILE`, `DEVICE_FILE` | Copies `.android-lab/shared/artifacts/<ARTIFACT_FILE>` to `DEVICE_FILE` under `/sdcard`. |
| `file-pull` | `DEVICE_FILE`, `ARTIFACT_FILE` | Copies a file under `/sdcard` into the artifacts directory. |
| `uiautomator-run` | `TEST_APK`, `TEST_RUNNER` | Installs and runs an instrumentation test APK. |
| `forward` | `ANDROID_LAB_FORWARD_HOST_PORT`, `ANDROID_LAB_FORWARD_DEVICE_PORT` | Exposes a device-local TCP port on host loopback. Defaults are 19001. It also publishes a second tunnel set by `ANDROID_LAB_MCP_HOST_PORT` and `ANDROID_LAB_MCP_DEVICE_PORT`, default 19002. |
| `unforward` | | Stops forwarding. |

Artifacts land in `.android-lab/shared/artifacts/`. Read `layout.json` to find tap targets and text, and open `screenshot.png` when the visual state matters. Emulator event fixtures such as location, SMS, battery and network state are listed in the [integration guide](https://github.com/psyb0t/android-lab/blob/main/docs/integration.md) and the release's Makefile.

## When something fails

- `Missing local image`: install the chosen version with `--emulator`.
- The emulator does not start: confirm the Docker host exposes `/dev/kvm`.
- The viewer port is taken: pick another `ANDROID_LAB_VNC_HOST_PORT`, then `lab start` again.
- Each project directory gets its own emulator and saved disk. When two run at once, give them different viewer and forward ports.
