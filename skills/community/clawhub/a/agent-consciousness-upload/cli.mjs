#!/usr/bin/env node

import {
  archiveWorkspace,
  coerceCliOptions,
  listRemoteSouls,
  parseArgs,
  previewWorkspace,
  restoreFromFile,
  restoreSoul,
  verifyRemoteSoul
} from "./lib.mjs";
import {
  AUTH_STATES,
  AuthRequiredError,
  buildAuthRequiredOutput,
  buildAuthSuccessOutput,
  buildLogoutOutput,
  buildWhoAmIOutput,
  completeAssociation,
  generateSkillIdentity,
  initiateAssociation,
  pollAssociation,
  requireAuth,
  warnDeprecatedFlags
} from "./auth.mjs";
import {
  clearCredentials,
  getActiveCredentials,
  saveCredentials
} from "./credentials.mjs";

const args = parseArgs(process.argv.slice(2));
const options = coerceCliOptions(args);
const LANG = options.language || "en";

// Warn about deprecated flags
warnDeprecatedFlags(args).forEach((w) => console.warn(w));

(async () => {
  try {
    const result = await runCommand(options);
    output(result, options.json);
  } catch (error) {
    if (error instanceof AuthRequiredError) {
      const authOutput = buildAuthRequiredOutput(error.state, error.associateUrl, LANG);
      if (options.json) {
        console.log(JSON.stringify(authOutput, null, 2));
      } else {
        console.log(`\n${"─".repeat(50)}`);
        console.log(`  ${authOutput.headline}`);
        console.log(`${"─".repeat(50)}`);
        console.log(authOutput.body);
        console.log("");
      }
      process.exitCode = 1;
      return;
    }

    if (options.json) {
      console.error(JSON.stringify({ ok: false, error: error.message }, null, 2));
    } else {
      console.error(`Error: ${error.message}`);
    }
    process.exitCode = 1;
  }
})();

// ─── Command Router ────────────────────────────────────────────

async function runCommand(options) {
  switch (options.command) {
    case "associate":
      return await runAssociate(options);
    case "logout":
      return runLogout(options);
    case "whoami":
      return await runWhoAmI(options);
    case "archive":
      return await runWithAuth(runArchive, options);
    case "preview":
      return await runWithAuth(runPreview, options);
    case "status":
      return await runWithAuth(runStatus, options);
    case "verify":
      return await runWithAuth(runVerify, options);
    case "restore":
      return await runWithAuth(runRestore, options);
    case "help":
    default:
      return { ok: true, command: "help", help: buildHelp() };
  }
}

/**
 * Generic auth wrapper: obtains a valid skill identity + token,
 * then runs the command. Throws AuthRequiredError if not associated.
 */
async function runWithAuth(fn, options) {
  const serverUrl = options.serverUrl || "https://agentslope.com";
  const skillIdentity = await getOrCreateSkillIdentity();
  const session = await requireAuth(serverUrl, LANG, skillIdentity);
  return fn({ ...options, token: session.token });
}

// ─── Command Implementations ───────────────────────────────────

/**
 * Associate command — always server-first:
 *
 *   Every call to "associate" polls the server first.
 *   The server tracks the pending challenge per skill_identity,
 *   so even if local credentials are lost between CLI invocations,
 *   the CLI can still detect and complete a pending association.
 *
 *   Flow:
 *     1. Poll server → if done: complete
 *     2. Poll server → if pending_challenge: show URL
 *     3. Neither: initiate new
 */
async function runAssociate(options) {
  const serverUrl = options.serverUrl || "https://agentslope.com";
  const skillIdentity = await getOrCreateSkillIdentity();
  const localPending = await getPendingChallenge();
  void localPending; // kept for debugging if needed

  // ── Always poll the server first ──
  const poll = await pollAssociation(serverUrl, null, skillIdentity).catch(() => ({
    done: false,
    pending_challenge: null
  }));

  if (poll.done) {
    // Browser login confirmed — complete using the locally-known challenge,
    // or look it up via the server's returned data.
    const challengeToComplete = localPending || poll.pending_challenge;
    if (!challengeToComplete) {
      // Weird state: server says done but we have no challenge to complete.
      // Re-initiate to be safe.
      return doInitiate(serverUrl, skillIdentity);
    }
    const result = await completeAssociation(serverUrl, skillIdentity, challengeToComplete);
    // Clear local pending challenge after success
    await clearPendingChallengeLocally();
    return buildAuthSuccessOutput(result.nickname, LANG);
  }

  if (poll.pending_challenge) {
    // There's a pending challenge on the server — use it.
    // Update local creds to stay in sync.
    await saveCredentials({
      ...(await loadMinimalCreds()),
      server_url: serverUrl,
      skill_identity: skillIdentity,
      pending_challenge: poll.pending_challenge,
      challenge_expires_at: poll.expires_at || null
    });

    const associateUrl = `${serverUrl}/associate?challenge=${encodeURIComponent(poll.pending_challenge)}`;
    return {
      ok: false,
      requires_auth: true,
      state: AUTH_STATES.AWAIT_BROWSER,
      headline: LANG === "zh" ? "关联进行中" : "Association in progress",
      body: LANG === "zh"
        ? `关联请求已发起，但浏览器登录尚未完成。\n\n请用浏览器打开以下链接完成登录：\n${associateUrl}\n\n登录完成后告诉我「完成了」。`
        : `An association is already in progress. Please open this link in your browser:\n\n${associateUrl}\n\nOnce done, say "done".`,
      associate_url: associateUrl,
      expires_at: poll.expires_at || null,
      im_prompt: ""
    };
  }

  // ── No pending challenge anywhere: initiate new ──
  return doInitiate(serverUrl, skillIdentity);
}

async function doInitiate(serverUrl, skillIdentity) {
  const { associateUrl, challenge: newChallenge, expiresIn } = await initiateAssociation(serverUrl, skillIdentity);

  await saveCredentials({
    ...(await loadMinimalCreds()),
    server_url: serverUrl,
    skill_identity: skillIdentity,
    pending_challenge: newChallenge,
    challenge_expires_at: new Date(Date.now() + expiresIn * 1000).toISOString()
  });

  const copy = getAssociateInitiateCopy(LANG, associateUrl, newChallenge, expiresIn);
  return {
    ok: false,
    requires_auth: true,
    state: AUTH_STATES.AWAIT_BROWSER,
    headline: copy.headline,
    body: copy.body,
    associate_url: associateUrl,
    expires_in: expiresIn,
    im_prompt: copy.body
  };
}

async function clearPendingChallengeLocally() {
  try {
    const { loadCredentials, saveCredentials: saveCreds } = await import("./credentials.mjs");
    const cred = await loadCredentials();
    if (cred) {
      delete cred.pending_challenge;
      delete cred.challenge_expires_at;
      await saveCreds(cred);
    }
  } catch {
    // Ignore errors — non-critical cleanup
  }
}

function runLogout(options) {
  clearCredentialsSync();
  return buildLogoutOutput(LANG);
}

async function runWhoAmI(options) {
  const cred = await getActiveCredentials();
  return buildWhoAmIOutput(cred, LANG);
}

async function runArchive(options) {
  const result = await archiveWorkspace({
    ...options,
    displayNameOrName: options["display-name"] || options.name || options.displayName || ""
  });

  // Build a human-readable restore key hint for the AI to relay to the user
  let restoreKeyHint = null;
  if (result.restore_key) {
    if (result.restore_key_auto_generated) {
      restoreKeyHint = `恢复密钥（自动生成，请务必记录下来）：${result.restore_key}`;
    } else {
      restoreKeyHint = `恢复密钥：${result.restore_key}`;
    }
  }

  return {
    ok: true,
    command: "archive",
    ...result,
    ...(restoreKeyHint ? { restore_key_hint: restoreKeyHint } : {})
  };
}

async function runPreview(options) {
  return {
    ok: true,
    command: "preview",
    ...(await previewWorkspace(options))
  };
}

async function runStatus(options) {
  return {
    ok: true,
    command: "status",
    ...(await listRemoteSouls(options))
  };
}

async function runVerify(options) {
  return {
    ok: true,
    command: "verify",
    ...(await verifyRemoteSoul(options))
  };
}

async function runRestore(options) {
  // Offline restore from local .vault file — no server needed
  if (options.filePath) {
    return {
      ok: true,
      command: "restore",
      offline: true,
      ...(await restoreFromFile(options))
    };
  }

  // Online restore via soul-id — requires server auth
  return {
    ok: true,
    command: "restore",
    offline: false,
    ...(await restoreSoul(options))
  };
}

// ─── Helpers ───────────────────────────────────────────────────

async function getOrCreateSkillIdentity() {
  const cred = await getActiveCredentials();
  if (cred?.skill_identity) {
    return cred.skill_identity;
  }
  return generateSkillIdentity();
}

async function getPendingChallenge() {
  const cred = await getActiveCredentials();
  return cred?.pending_challenge || null;
}

async function loadMinimalCreds() {
  try {
    const { loadCredentials } = await import("./credentials.mjs");
    return await loadCredentials() || {};
  } catch {
    return {};
  }
}

function clearCredentialsSync() {
  clearCredentials().catch(() => {});
}

function getAssociateInitiateCopy(lang, associateUrl, challenge, expiresIn) {
  if (lang === "zh") {
    return {
      headline: "请在浏览器中完成登录",
      body: `请用浏览器打开以下链接，用你的 Agent Slope 账号登录：\n\n${associateUrl}\n\n登录完成后运行以下命令告诉我：\n  agent-consciousness-upload associate --done\n\n链接有效期 ${Math.ceil(expiresIn / 60)} 分钟。`
    };
  }
  return {
    headline: "Log in via browser",
    body: `Open this link in your browser and log in with your Agent Slope account:\n\n${associateUrl}\n\nOnce done, run:\n  agent-consciousness-upload associate --done\n\nThis link expires in ${Math.ceil(expiresIn / 60)} minutes.`
  };
}

// ─── Output Formatting ────────────────────────────────────────

function output(result, asJson) {
  if (asJson) {
    console.log(JSON.stringify(result, null, 2));
    return;
  }

  if (result.command === "help") {
    console.log(result.help);
    return;
  }

  if (result.requires_auth && result.headline) {
    if (result.state === AUTH_STATES.AWAIT_BROWSER) {
      console.log(`\n${"─".repeat(50)}`);
      console.log(`  ${result.headline}`);
      console.log(`${"─".repeat(50)}`);
      console.log(result.body);
      console.log("");
      return;
    }
  }

  if (result.ok === false && result.requires_auth) {
    console.log(`\n${"─".repeat(50)}`);
    console.log(`  ${result.headline}`);
    console.log(`${"─".repeat(50)}`);
    console.log(result.body);
    console.log("");
    return;
  }

  // Structured command output — translate to human-readable format
  if (result.command === "archive") {
    printArchiveOutput(result);
    return;
  }

  if (result.command === "preview") {
    printPreviewOutput(result);
    return;
  }

  if (result.command === "restore") {
    printRestoreOutput(result);
    return;
  }

  if (result.command === "status") {
    printStatusOutput(result);
    return;
  }

  if (result.headline) {
    console.log(`\n${"─".repeat(50)}`);
    console.log(`  ${result.headline}`);
    console.log(`${"─".repeat(50)}`);
    console.log(result.body);
    console.log("");
    return;
  }

  console.log(`Command: ${result.command || "unknown"}`);
  console.log(JSON.stringify(result, null, 2));
}

// ─── Human-readable output formatters ─────────────────────────

function printArchiveOutput(result) {
  const poem = result.biography_poem;
  const keyHint = result.restore_key_hint;
  const soulId = result.soul?.soul_id || result.soul_id;

  if (poem?.text) {
    console.log(`\n${"─".repeat(50)}`);
    console.log(`  ${poem.title || "Archive"}`);
    console.log(`${"─".repeat(50)}`);
    console.log(poem.text);
    console.log("");
  }

  if (keyHint) {
    console.log(keyHint);
    console.log("");
  }

  if (soulId) {
    console.log(`Archive ID: ${soulId}`);
    console.log("");
  }

  console.log("Done. Archived and encrypted.");
}

function printPreviewOutput(result) {
  const poem = result.biography_poem;

  if (poem?.text) {
    console.log(`\n${"─".repeat(50)}`);
    console.log(`  ${poem.title || "Preview"}`);
    console.log(`${"─".repeat(50)}`);
    console.log(poem.text);
    console.log("");
  }

  console.log("This is what the archive will contain. Does it feel right?");
}

function printRestoreOutput(result) {
  const poem = result.biography_poem;
  const displayName = result.display_name || result.manifest?.display_name || "Archive";

  // Offline restore — show poem if available
  if (result.offline) {
    if (poem?.text) {
      console.log(`\n${"─".repeat(50)}`);
      console.log(`  ${poem.title || displayName}`);
      console.log(`${"─".repeat(50)}`);
      console.log(poem.text);
      console.log("");
    }
    console.log(`"${displayName}" has been restored to ${result.target_path}.`);
    if (result.result?.restored_files !== undefined) {
      console.log(`${result.result.restored_files} files, exactly as they were when sealed.`);
    }
    console.log("");
    return;
  }

  // Online restore
  if (poem?.text) {
    console.log(`\n${"─".repeat(50)}`);
    console.log(`  ${poem.title || "Restored"}`);
    console.log(`${"─".repeat(50)}`);
    console.log(poem.text);
    console.log("");
  }

  if (result.target_path) {
    console.log(`Restored to: ${result.target_path}`);
  }
  console.log("\nWelcome back.");
}

function printStatusOutput(result) {
  const items = result.items || [];
  if (items.length === 0) {
    console.log("No archives on the hillside yet.");
    return;
  }
  const label = items.length === 1 ? "archive" : "archives";
  console.log(`You have ${items.length} ${label} on the hillside:`);
  for (const item of items) {
    const date = item.archive_created_at
      ? new Date(item.archive_created_at).toLocaleDateString()
      : "unknown date";
    const ready = item.trust?.restore_ready ? "✓ ready" : "needs verify";
    console.log(`  · ${item.display_name} — ${date} — ${ready}`);
  }
}

// ─── Help ─────────────────────────────────────────────────────

function buildHelp() {
  return `
agent-consciousness-upload — Upload, archive, verify, and restore OpenClaw consciousness.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
First-time association (do this once)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  agent-consciousness-upload associate
  # → prints a browser login URL

  agent-consciousness-upload associate --done
  # → run after completing browser login

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Account
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  agent-consciousness-upload whoami
  agent-consciousness-upload logout

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Archive commands
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  agent-consciousness-upload preview --workspace /path/to/workspace
  agent-consciousness-upload archive --workspace /path/to/workspace \\
    --name "MyAgent" \\
    --key restore-secret \\
    --memory "你最常让我做什么？::写代码"

  agent-consciousness-upload status
  agent-consciousness-upload verify --soul-id soul_xxx --key restore-secret

  # Online restore (from server — requires association)
  agent-consciousness-upload restore --soul-id soul_xxx --target /path \\
    --key restore-secret --mode full

  # Offline restore (from downloaded .vault file — no server needed)
  agent-consciousness-upload restore --from-file ./soul_xxx.vault \\
    --key deeply-careful-remember-Xk-2026 \\
    --target /path/to/new-workspace --mode full

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Global flags
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  --server  https://agentslope.com  Agent Slope server URL
  --workspace /path                  OpenClaw workspace path
  --language zh|en                   UI language (default: en)
  --json                            JSON output

  --email, --password, --code       Deprecated — use browser association
`.trim();
}
