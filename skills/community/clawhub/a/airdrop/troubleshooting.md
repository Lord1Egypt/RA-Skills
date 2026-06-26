# Troubleshooting - AirDrop

Use this guide when the handoff does not behave as expected.

## `swift` or `xcrun` not available

- Check `xcrun swift --version`.
- If unavailable, either install Xcode Command Line Tools or switch to Shortcut mode.
- Do not pretend direct mode exists without a Swift runtime.

## Chooser launched but no device appears

- Confirm AirDrop is enabled in Finder on both devices.
- Confirm Wi-Fi and Bluetooth are on.
- Confirm the devices are nearby and awake.
- Retry with one small file before testing a larger bundle.

## Shortcut mode fails

- Run `shortcuts list` and match the exact shortcut name.
- Confirm the shortcut accepts file input.
- Retry with one file and no extra pre-processing.

## Wrong files were about to be shared

- Stop before recipient selection.
- Reduce the payload to the approved subset.
- Prefer a staged ZIP when the source folder contains unrelated files.

## Helper prints success but transfer still did not complete

- Remember that success only means the AirDrop chooser launched.
- Ask the user whether the device appeared and whether they accepted the transfer.
- If not, troubleshoot visibility instead of rerunning the same command repeatedly.

## Item cannot be shared

- Confirm every argument is an existing local file path.
- Stage generated text into a file first.
- Strip unsupported or empty paths before retrying.

## User wants zero-click recipient targeting

- Do not promise it through an official AirDrop CLI because macOS does not expose a stable `airdrop send <recipient>` command.
- Offer Shortcut mode only if the user already owns a local automation that handles the final routing behavior.
