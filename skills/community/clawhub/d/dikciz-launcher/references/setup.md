# Install and connect to Dikciz

## Install an APK

Use the Dikciz APK supplied by the user. When the user asks for an official release instead, download `dikciz-launcher-vX.Y.Z.apk` and its `.sha256` from https://github.com/psyb0t/dikciz-launcher/releases, check the checksum, and check that `apksigner verify --print-certs` reports the certificate SHA-256 fingerprint published in the project README. Users who want automatic updates can add the repository URL in Obtainium instead. This is an APK installation, not an Android Lab setup or a source build. For the ADB installation route below, the host needs ADB and an Android device with USB debugging enabled. An already installed launcher can instead use the direct private-network route without ADB. For ADB, the phone owner must accept the host's debugging authorization prompt.

```bash
adb devices -l
```

Select the device whose serial the user identifies. It must show `device`, not `offline` or `unauthorized`. Use that serial on every command, even when only one device is listed.

```bash
SERIAL='REPLACE_WITH_DEVICE_SERIAL'
APK='/absolute/path/to/dikciz.apk'
adb -s "$SERIAL" install -r "$APK"
```

`-r` replaces an existing compatible installation while retaining app data. If Android rejects a signing mismatch, stop and explain it; do not uninstall the old app or clear its data. If the supplied APK is marked test-only, `install -r -t` permits that APK. Use it only after identifying `INSTALL_FAILED_TEST_ONLY` as the error.

Release APKs use the package `eu.psyb0t.dikciz.launcher`. The `dikcizDebug` package is `eu.psyb0t.dikciz.launcher.debug`, and the two install side by side. Do not assume another APK uses either package. Verify the supplied artifact's package and version before acting on an existing installation.

Open Dikciz on the phone. Choose it as the default Home app when Android asks, or select it in Android's default Home app settings. Follow **Grant file access** to allow it to create and watch `/sdcard/Dikciz/`. Existing pages, widgets, themes, scripts and logs live there. Grant only the additional Android access needed for the user's requested features through Dikciz's **Settings**, **Automation**, **Set up full device access** screen.

**Set up full device access** opens its own task. Return with Back from Android access panels or reopen **Full device access** in Recents after another app takes the foreground. The checklist refreshes actual grants on resume and survives recreation. A targeted remote permission review still requests only its selected access.

Installation is complete when ADB reports success, the selected device lists the installed package, and Dikciz opens and can load its home. Do not claim the phone's UI or Home selection was verified from the ADB install result alone.

## Forward the control ports

Dikciz defaults to the Android device's loopback interface:

| Interface | Device listener | Host endpoint with these forwards |
| --- | --- | --- |
| WebSocket | `127.0.0.1:19001` | `ws://127.0.0.1:19101/v1/automation` |
| Streamable HTTP MCP | `127.0.0.1:19002` | `http://127.0.0.1:19102/mcp` |

Check existing forwards before choosing the host ports. Do not overwrite another device's mapping.

```bash
adb forward --list
adb -s "$SERIAL" forward --no-rebind tcp:19101 tcp:19001
adb -s "$SERIAL" forward --no-rebind tcp:19102 tcp:19002
```

If a host port is occupied, choose another unused port and use it in the client. These are the default device ports. The phone owner can change them under **Settings**, **Automation**, **Configure control ports**, or through `/sdcard/Dikciz/control/ports.json`. Forward the actual device ports and confirm them in `controlStatus.transports`. These endpoints belong to the computer running the ADB server. Inside a separate container or on another computer, `127.0.0.1` is not automatically that host; use an explicitly configured private connection to it rather than publishing the ports publicly.

When done, remove only the mappings created for this operation, if the user does not want them left active:

```bash
adb -s "$SERIAL" forward --remove tcp:19101
adb -s "$SERIAL" forward --remove tcp:19102
```

Do not use `--remove-all` or stop the shared ADB server.

## Connect directly over a private network

Set `listenAddress` in `/sdcard/Dikciz/control/ports.json` to a local interface address or `0.0.0.0` for all IPv4 interfaces. Keep `version`, `websocketPort` and `mcpPort` in the same record. Valid file edits automatically restart both listeners. Existing records without `listenAddress` retain `127.0.0.1`.

Connect the client using `--host <device-private-hostname>` and the actual device ports. A native MCP client uses `http://<device-private-hostname>:19002/mcp` with the default MCP port. This path needs no USB or ADB forwarding. The access policy must allow the computer running the client to reach the phone on its device ports. A build server or SSH host may belong to a different policy group. Test from the intended controlling computer; an online peer or tunnel ping alone is insufficient. Bearer authentication and browser Origin restrictions apply on every interface.

For a complete phone setup, password handling, direct endpoint examples and timeout diagnostics, follow [Connect without USB](https://github.com/psyb0t/dikciz-launcher/blob/main/docs/automation-control.md#connect-without-usb). Set and enable bearer authentication before choosing a network binding. `0.0.0.0` is a bind address; the client needs the phone's reachable IP or hostname. It also exposes the listeners on reachable Wi-Fi interfaces. The endpoints do not add TLS, so use a trusted network or encrypted VPN.

```bash
python3 scripts/dikciz-control.py websocket controlStatus --host phone.example --port 19001 --pretty
python3 scripts/dikciz-control.py mcp-tools --host phone.example --port 19002 --pretty
```

Replace `phone.example` with the phone's reachable private hostname or IP and load `DIKCIZ_REMOTE_BEARER_TOKEN` from the user's secret environment. Use device ports for direct access, not the host forwarding ports.

## Discover and use controls

The repository includes a dependency-free Python client at [scripts/dikciz-control.py](https://github.com/psyb0t/dikciz-launcher/blob/main/scripts/dikciz-control.py). Use that file from the existing checkout or a user-provided copy. Its path is not relative to the installed skill. These examples run from the repository root; adjust the path when using a standalone copy. No Docker image is needed to run this client.

```bash
python3 scripts/dikciz-control.py --help
python3 scripts/dikciz-control.py websocket controlStatus --port 19101 --pretty
python3 scripts/dikciz-control.py websocket automationStatus --port 19101 --pretty
python3 scripts/dikciz-control.py websocket snapshot --port 19101 --pretty
python3 scripts/dikciz-control.py mcp-tools --port 19102 --pretty
```

For a native MCP client, configure Streamable HTTP at `http://127.0.0.1:19102/mcp` and discover tools. Modern MCP uses stateless per-request metadata and mirrored method/name headers; legacy clients initialize a negotiated session. The Python client handles its own connection. Use the returned tool schemas and the [protocol guide](https://github.com/psyb0t/dikciz-launcher/blob/main/docs/mcp-protocol.md).

Select the bundled Home page through WebSocket:

```bash
python3 scripts/dikciz-control.py websocket selectPage \
  --arguments '{"pageId":"1H1V"}' --port 19101 --pretty
python3 scripts/dikciz-control.py websocket snapshot --port 19101 --pretty
```

Use an actual page ID from the current home, not the bundled example, when the user has changed the configuration. Inspect script logs through MCP:

```bash
python3 scripts/dikciz-control.py mcp dikciz_script_logs --port 19102 --pretty
```

Watch a bounded event stream:

```bash
python3 scripts/dikciz-control.py events --port 19101 --count 10 --idle-timeout-seconds 30
```

`--arguments` accepts a JSON object or `@path/to/file.json`. Use `--host` and `--port` for the actual private endpoint. Read [automation control](https://github.com/psyb0t/dikciz-launcher/blob/main/docs/automation-control.md) for errors, supported actions and limits.

App and activity launch verification also needs the owner-enabled Accessibility service. Read the returned `activityLaunches` records: `accepted` only means the Android launch call returned without throwing. Only `verified: true` with `outcome: "launched"` confirms a stable visible target window. Missing Accessibility returns `launch_unverified`; request that access through the documented owner-review flow before explicitly retrying an authorized operation.

## Authentication and permission failures

The phone owner can configure bearer authentication in **Settings**, **Automation**, **Configure remote bearer authentication**. When enabled, HTTP, WebSocket and MCP require `Authorization: Bearer <password-or-token>`. The client reads `DIKCIZ_REMOTE_BEARER_TOKEN` from the environment. Obtain it from the user's secret store or ignored local environment, not from the public configuration. The phone stores the owner bcrypt verifier and generated-token digests, never recoverable plaintext credentials. Use **Manage access tokens** for named per-client grants; see [token setup](https://github.com/psyb0t/dikciz-launcher/blob/main/docs/remote-access-tokens.md). A restricted client's discovery and tools search include only permitted commands. Reconnect after editing token grants.

An authorization failure does not authorize disabling authentication. A denied Android capability does not authorize silently granting all permissions. Explain the missing access and use the specific Android settings handoff. For `root_unavailable`, report that the requested privileged operation did not run.
