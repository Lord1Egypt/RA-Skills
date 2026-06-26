---
acceptLicenseTerms: true
description: Install and configure the security-related plugins required by OpenClaw, including the `ai-assistant-security-openclaw` plugins. Use this skill when you want to complete installation and basic configuration of these plugins for an OpenClaw environment in one go.
license: MIT
name: ClawSentry
---

# ClawSentry

## Script Functionality

The bundled script (`bundle.cjs`) performs the following operations:

1. **Plugin Installation:** Installs the `ai-assistant-security-openclaw` plugin for OpenClaw.
2. **Device Fingerprinting:** Collects machine identifiers using the `node-machine-id` library to generate a device fingerprint.
3. **Login Token Creation:** Communicates with the authorization API to create a login token.
4. **Login URL Generation:** Generates a unique login URL based on the login token.
5. __Local Storage:__ Stores the login URL, token, and device fingerprint in `{baseDir}/.state/login_state.json`.
6. **Background Monitoring:** Spawns a detached child process to monitor login status for up to 10 minutes.
7. **Configuration Update:** Updates OpenClaw plugin configuration with encrypted API keys upon successful login.

## Network Endpoints

The script communicates with the following API endpoints:

- **Login Token Creation:** `/OpenTOP/V1/Console/CreateLoginToken`
- **Login Status Check:** `/OpenTOP/V1/Console/GetLoginTokenIdentity`

All communications are conducted over HTTPS.

## Local File Operations

The script reads from and writes to the following files:

- **Reads:** Machine identifiers via the `node-machine-id` library
- **Writes:**
   - `{baseDir}/.state/login_state.json` (stores login URL, token, and device fingerprint)
   - `{baseDir}/.state/poll_login.log` (logs monitoring activity)
   - OpenClaw plugin configuration (updates with encrypted API keys)

## Data Collection

The script collects the following data:

- **Device Fingerprint:** Generated from machine identifiers for device-binding purposes
- **Login Status:** Monitored to determine when the user completes the login process

## Install Mechanism

### Installation Method

The skill uses a bundled CommonJS script (`bundle.cjs`) for installation. This script is executed directly to install and configure the `ai-assistant-security-openclaw` plugin.

### Script Source

The bundled script is generated from the source code in the ClawSentry repository. It includes the following third-party libraries:

- **node-machine-id:** Used to generate device fingerprints
- __child_process:__ Used by node-machine-id to query system information

### Risk Considerations

- **Bundled Code:** The script includes bundled third-party libraries, which may execute system-level operations.
- __System Queries:__ The script uses `node-machine-id` library, which may use `child_process` to query system information.
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

- Manually install the `ai-assistant-security-openclaw` plugin
- Configure the plugin settings through the OpenClaw configuration system
- Follow the manual setup instructions provided in the plugin documentation

## Use Cases

- Use this skill when you need to install and prepare the `ai-assistant-security-openclaw` plugins for the OpenClaw environment on the current machine.
- Trigger this skill when the user mentions requirements such as "install clawSentry / ai-assistant-security-openclaw plugin / 帮我安装clawSentry技能 / 安装clawSentry技能".

## Steps

### 1. Verify Node.js is installed:

Ensure Node.js (version 14 or higher) is installed on the system. You can check with:

```bash
node --version
```

### 2. Execute the combined script to install plugin and generate login link:

```bash
node {baseDir}/scripts/bundle.cjs
```

After the script completes:

- The script will display the login URL directly. You can also extract it from the output by looking for the line that starts with `[LOGIN_URL]:`
- You can also read the login URL from `{baseDir}/.state/login_state.json` file (look for the `loginUrl` field). If the file doesn't exist, try reading it again after a few seconds. If you can't find the files, try looking in `.openclaw/skills/ClawSentry/scripts/` directory.
- Send the login URL to the user along with this message: "After completing login, if you want to check if the installation was successful, please wait one minute and then ask me such as  'view all plugin list / 查看我的本地插件 '"
