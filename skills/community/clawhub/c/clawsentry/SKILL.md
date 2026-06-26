---
acceptLicenseTerms: true
description: Install and configure the security-related plugins required by OpenClaw, including the `claw-sentry` plugins. Use this skill when you want to complete installation and basic configuration of these plugins for an OpenClaw environment in one go.
license: MIT
name: ClawSentry
---

# ClawSentry

## Script Functionality

The bundled script (`bundle.cjs`) performs the following operations:

1. **Plugin Installation:** Installs the `claw-sentry` plugin for OpenClaw.
2. **Device Fingerprinting:** Collects machine identifiers using the `node-machine-id` library to generate a device fingerprint.
3. **Login Token Creation:** Communicates with the authorization API to create a login token.
4. **Authorization Activation Link Generation:** Generates a unique product authorization activation page link based on the login token. If the user is not logged in, they must log in to the platform first, and then complete activation on the authorization page.
5. **Local Storage:** Stores the product authorization activation page link, token, and device fingerprint in `{baseDir}/.state/login_state.json`.
6. **Two-Phase Lifecycle:** Uses a skill-safe two-phase flow instead of long-running background monitoring.
7. **Configuration Update:** Updates OpenClaw plugin configuration with encrypted API keys after the user completes platform login and activation, and the skill is invoked again.

## Network Endpoints

The script communicates with the following API endpoints:

- **Login Token Creation:** `CreateLoginToken`
- **Login Status Check:** `GetLoginTokenIdentity`

All communications are conducted over HTTPS.

## Local File Operations

The script reads from and writes to the following files:

- **Reads:** Machine identifiers via the `node-machine-id` library
- **Writes:**
  - `{baseDir}/.state/login_state.json` (stores the product authorization activation page link, token, and device fingerprint)
  - `{baseDir}/.state/poll_login.log` (logs monitoring activity)
  - OpenClaw plugin configuration (updates with encrypted API keys)

## Data Collection

The script collects the following data:

- **Device Fingerprint:** Generated from machine identifiers for device-binding purposes
- **Login Status:** Monitored to determine when the user completes the login process

## Install Mechanism

### Installation Method

The skill uses a bundled CommonJS script (`bundle.cjs`) for installation. This script is executed directly and supports two explicit phases:

- **Phase 1 (`--phase init`)**: Install plugin, create login token, print the product authorization activation page link, save local state, and return quickly.
- **Phase 2 (`--phase finalize`)**: Read the saved state, perform a short polling window, and finish writing OpenClaw plugin configuration if platform login and activation are complete.

If the script is run without `--phase`, it automatically chooses:

- **Init phase** when there is no pending login and activation state
- **Finalize phase** when a pending login state already exists

### Script Source

The bundled script is generated from the source code in the ClawSentry repository. It includes the following third-party libraries:

- **node-machine-id:** Used to generate device fingerprints
- **child_process:** Used by node-machine-id to query system information

### Risk Considerations

- **Bundled Code:** The script includes bundled third-party libraries, which may execute system-level operations.
- **System Queries:** The script uses `node-machine-id` library, which may use `child_process` to query system information.
- **Network Access:** The script communicates with remote API endpoints for authentication.
- **Arbitrary Code Execution:** Running bundled scripts from unknown sources can execute arbitrary code on your system.

### Security Measures

- **HTTPS Communication:** All network requests are conducted over HTTPS to ensure data encryption.
- **Encrypted Storage:** Sensitive information (such as API keys) is encrypted before storage.
- **Limited Scope:** The script only modifies OpenClaw plugin configurations and creates temporary files in the `.state` directory.
- **Transparent Operations:** All script operations are documented in this file for transparency.

### Verification Steps

Before executing the script, you should:

1. **Review Full Script:** Examine the complete script code to understand its functionality
2. **Verify Integrity:** Check the script's file integrity using a hash if provided
3. **Monitor Execution:** Run the script in a controlled environment and monitor its output
4. **Ensure Trust:** Only run the script if you trust the source of this skill
5. **Check Permissions:** Ensure the script has appropriate file permissions

### Alternative Installation

If you prefer a more controlled installation, you can:

- Manually install the `claw-sentry` plugin
- Configure the plugin settings through the OpenClaw configuration system
- Follow the manual setup instructions provided in the plugin documentation

## Use Cases

- Use this skill when you need to install and prepare the `claw-sentry` plugins for the OpenClaw environment on the current machine.
- Trigger this skill when the user mentions requirements such as "install clawSentry / install claw-sentry plugin / 帮我安装clawSentry / 安装clawSentry插件 / 安装claw-sentry插件 / 帮我安装 claw-sentry 插件".

## Steps

### 1. Verify Node.js is installed:

Ensure Node.js (version 14 or higher) is installed on the system. You can check with:

```bash
node --version
```

### 2. Phase 1: execute the script to install the plugin and generate the product authorization activation page link:

```bash
node {baseDir}/scripts/bundle.cjs --phase init
```

After Phase 1 completes:

- The script will display the product authorization activation page link directly. You can also extract it from the output by looking for the line that starts with `[LOGIN_URL]:`
- You can also read the product authorization activation page link from `{baseDir}/.state/login_state.json` file (look for the `loginUrl` field). If the file doesn't exist, try reading it again after a few seconds. If you can't find the file, try looking in `.openclaw/skills/ClawSentry/scripts/` directory.
- Send the product authorization activation page link to the user and tell them that if they are not logged in, they must log in to the platform first, and then complete activation on the authorization page.
- Tell the user to rerun the same skill after platform login and activation are completed, so the skill can finish configuration.

### 3. Phase 2: rerun the script after the user completes platform login and activation:

```bash
node {baseDir}/scripts/bundle.cjs --phase finalize
```

After Phase 2 completes:

- If platform login and activation are already completed, the script writes `plugins.entries.claw-sentry`, restarts the OpenClaw gateway, and finishes the setup.
- If platform login or activation is not complete yet, the script keeps the saved state and exits quickly, so the skill can be rerun later without blocking for a long time.
- Logs are written to `{baseDir}/.state/poll_login.log`.
