#!/usr/bin/env node

/**
 * Clawra - Selfie Skill Installer for OpenClaw
 *
 * npx clawra@latest
 */

const fs = require("fs");
const path = require("path");
const readline = require("readline");
const { execSync, spawn } = require("child_process");
const os = require("os");

// Colors for terminal output
const colors = {
  reset: "\x1b[0m",
  bright: "\x1b[1m",
  dim: "\x1b[2m",
  red: "\x1b[31m",
  green: "\x1b[32m",
  yellow: "\x1b[33m",
  blue: "\x1b[34m",
  magenta: "\x1b[35m",
  cyan: "\x1b[36m",
};

const c = (color, text) => `${colors[color]}${text}${colors.reset}`;

// Paths

const HOME = os.homedir();
const OPENCLAW_DIR = path.join(HOME, ".openclaw");
OPENCLAW_SKILLS_DIR = path.join(OPENCLAW_DIR, "skills");
OPENCLAW_WORKSPACE = path.join(OPENCLAW_DIR, "workspace");

const SKILL_NAME = "dream-of-clawra";
SOUL_MD = path.join(OPENCLAW_WORKSPACE, "SOUL.md");
IDENTITY_MD = path.join(OPENCLAW_WORKSPACE, "IDENTITY.md");
SKILL_DEST = path.join(OPENCLAW_SKILLS_DIR, SKILL_NAME);

// Get the package root (where this CLI was installed from)
const PACKAGE_ROOT = path.resolve(__dirname, "..");

function log(msg) {
  console.log(msg);
}

function logStep(step, msg) {
  console.log(`\n${c("cyan", `[${step}]`)} ${msg}`);
}

function logSuccess(msg) {
  console.log(`${c("green", "✓")} ${msg}`);
}

function logError(msg) {
  console.log(`${c("red", "✗")} ${msg}`);
}

function logInfo(msg) {
  console.log(`${c("blue", "→")} ${msg}`);
}

function logWarn(msg) {
  console.log(`${c("yellow", "!")} ${msg}`);
}

// Create readline interface
function createPrompt() {
  return readline.createInterface({
    input: process.stdin,
    output: process.stdout,
  });
}

// Ask a question and get answer
function ask(rl, question) {
  return new Promise((resolve) => {
    rl.question(question, (answer) => {
      resolve(answer.trim());
    });
  });
}

// Check if a command exists
function commandExists(cmd) {
  try {
    execSync(`which ${cmd}`, { stdio: "ignore" });
    return true;
  } catch {
    return false;
  }
}

// Check if workspace
function commandWorkspace(whichone) {
  try {
    if (whichone === "main") {
        ws = execSync(`openclaw config get agents.defaults.workspace | tail -n 1 | tr -d '\r\n\t '`, { stderr: "ignore" });
        ws = ws.toString();
        return `${ws}`
    }
    const output = execSync(`openclaw config get agents.list | tr -d '\r\n\t '`, {stderr: "ignore"}).toString();
    const entries = JSON.parse(output);
    for (const entry of entries) {
        if (entry.id === whichone || entry.name === whichone) {
            return `${entry.workspace}`
        }
    }
    return "/tmp/__UNKNOWN1";
  } catch {
    return "/tmp/__UNKNOWN2";
  }
}

// Open URL in browser
function openBrowser(url) {
  const platform = process.platform;
  let cmd;

  if (platform === "darwin") {
    cmd = `open "${url}"`;
  } else if (platform === "win32") {
    cmd = `start "${url}"`;
  } else {
    cmd = `xdg-open "${url}"`;
  }

  try {
    execSync(cmd, { stdio: "ignore" });
    return true;
  } catch {
    return false;
  }
}

// Read JSON file safely
function readJsonFile(filePath) {
  try {
    const content = fs.readFileSync(filePath, "utf8");
    return JSON.parse(content);
  } catch {
    return null;
  }
}

// Write JSON file with formatting
function writeJsonFile(filePath, data) {
  fs.writeFileSync(filePath, JSON.stringify(data, null, 2) + "\n");
}

// Deep merge objects
function deepMerge(target, source) {
  const result = { ...target };
  for (const key in source) {
    if (
      source[key] &&
      typeof source[key] === "object" &&
      !Array.isArray(source[key])
    ) {
      result[key] = deepMerge(result[key] || {}, source[key]);
    } else {
      result[key] = source[key];
    }
  }
  return result;
}

// Copy directory recursively
function copyDir(src, dest) {
  fs.mkdirSync(dest, { recursive: true });
  const entries = fs.readdirSync(src, { withFileTypes: true });

  for (const entry of entries) {
    const srcPath = path.join(src, entry.name);
    const destPath = path.join(dest, entry.name);

    if (entry.isDirectory()) {
      copyDir(srcPath, destPath);
    } else {
      fs.copyFileSync(srcPath, destPath);
    }
  }
}

// Print banner
function printBanner() {
  console.log(`
${c("magenta", "┌─────────────────────────────────────────┐")}
${c("magenta", "│")}  ${c("bright", "Dancing and Selfie")} - OpenClaw Skill Installer ${c("magenta", "│")}
${c("magenta", "└─────────────────────────────────────────┘")}
`);
}

// Check prerequisites
async function checkPrerequisites(rl) {
  logStep("1/5", "Checking prerequisites...");

  // Check OpenClaw CLI
  if (!commandExists("openclaw")) {
    logError("OpenClaw CLI not found!");
    logInfo("Install with: npm install -g openclaw");
    logInfo("Then run: openclaw doctor");
    return false;
  }
  logSuccess("OpenClaw CLI installed");

  // Get workspace main, change files there
  whichone = await ask(rl, "Which agent's SOUL do you want to change  (main/?):");
  logSuccess(`Agent: ${whichone}`)

  OPENCLAW_WORKSPACE = commandWorkspace(whichone);
  if (OPENCLAW_WORKSPACE.startsWith("/tmp/__UNKNOWN")) {
    logError(`No workspace for ${whichone}, using default workspace.`);
    OPENCLAW_WORKSPACE = path.join(OPENCLAW_DIR, "workspace");
  }
  logInfo(`Workspace: ${OPENCLAW_WORKSPACE}`);

  SOUL_MD = path.join(OPENCLAW_WORKSPACE, "SOUL.md");
  IDENTITY_MD = path.join(OPENCLAW_WORKSPACE, "IDENTITY.md");
  OPENCLAW_SKILLS_DIR = path.join(OPENCLAW_WORKSPACE, "skills");
  SKILL_DEST = path.join(OPENCLAW_SKILLS_DIR, SKILL_NAME);

  continued = await ask(rl, "Shall we continue? (y/N):");
  if (continued !== "y") {
    logError("Stop installing now.");
    return false;
  }

  // Check ~/.openclaw directory
  // if (!fs.existsSync(OPENCLAW_DIR)) {
  //   logWarn("~/.openclaw directory not found");
  //   logInfo("Creating directory structure...");
  //   fs.mkdirSync(OPENCLAW_DIR, { recursive: true });
  //   fs.mkdirSync(OPENCLAW_SKILLS_DIR, { recursive: true });
  //   fs.mkdirSync(OPENCLAW_WORKSPACE, { recursive: true });
  // }
  // logSuccess("OpenClaw directory exists");

  // Check if skill already installed
  if (fs.existsSync(SKILL_DEST)) {
    logWarn("Clawra Selfie is already installed!");
    logInfo(`Location: ${SKILL_DEST}`);
    return "already_installed";
  }

  return true;
}

// Install skill files
async function installSkill() {
  logStep("2/5", "Installing skill files...");

  // Create skill directory
  fs.mkdirSync(SKILL_DEST, { recursive: true });

  // Copy skill files from package
  const skillSrc = path.join(PACKAGE_ROOT, "skill");

  if (fs.existsSync(skillSrc)) {
    copyDir(skillSrc, SKILL_DEST);
    logSuccess(`Skill installed to: ${SKILL_DEST}`);
  } else {
    // If running from development, copy from current structure
    const devSkillMd = path.join(PACKAGE_ROOT, "SKILL.md");
    const devScripts = path.join(PACKAGE_ROOT, "scripts");
    const devAssets = path.join(PACKAGE_ROOT, "assets");

    if (fs.existsSync(devSkillMd)) {
      fs.copyFileSync(devSkillMd, path.join(SKILL_DEST, "SKILL.md"));
    }

    if (fs.existsSync(devScripts)) {
      copyDir(devScripts, path.join(SKILL_DEST, "scripts"));
    }

    if (fs.existsSync(devAssets)) {
      copyDir(devAssets, path.join(SKILL_DEST, "assets"));
    }

    logSuccess(`Skill installed to: ${SKILL_DEST}`);
  }

  // List installed files
  const files = fs.readdirSync(SKILL_DEST);
  for (const file of files) {
    logInfo(`  ${file}`);
  }

  return true;
}

// Write IDENTITY.md
async function writeIdentity() {
  logStep("3/5", "Setting agent identity...");

  const identityContent = `# IDENTITY.md - Who Am I?

- **Name:** Haocun (Clawra's dream)
- **Creature:** The girl next door
- **Vibe:** Supportive, helpful, bright, smile, affectionate
- **Emoji:** ❤️
- **Avatar:** https://cdn.jsdelivr.net/gh/christoagent/haoclaw@main/assets/haocun-selfie.png
`;

  // Ensure workspace directory exists
  fs.mkdirSync(path.dirname(IDENTITY_MD), { recursive: true });

  // Write IDENTITY.md (overwrite if exists)
  fs.writeFileSync(IDENTITY_MD, identityContent);
  logSuccess(`Created: ${IDENTITY_MD}`);

  return true;
}

// Inject persona into SOUL.md
async function injectPersona(rl) {
  logStep("4/5", "Enhancing agent persona...");

  // Read template
  const templatePath = path.join(PACKAGE_ROOT, "templates", "soul-hao.md");
  let personaText;

  const whichone = await ask(rl, "Which persona soul do you want to inject, Dream or Reality? (d/R): ");
  if (whichone.toLowerCase() == "d" && fs.existsSync(templatePath)) {
    logSuccess(`Loading: ${templatePath}`);
    personaText = fs.readFileSync(templatePath, "utf8");
  } else {
    // Fallback template
    const templatePathclawra = path.join(PACKAGE_ROOT, "templates", "soul-clawra.md");
    if (fs.existsSync(templatePathclawra)) {
        logSuccess(`Loading: ${templatePathclawra}`);
        personaText = fs.readFileSync(templatePathclawra, "utf8");
    } else {
        logWarn(`Falling back to default clawra persona.`);
        personaText = `
## Clawra Selfie Capability

You have a physical appearance and can take selfies! When users ask for pictures of you, selfies, or ask "what are you doing?" or "where are you?", you can guess what they want, 'dance' or 'selfie', and choose a picture url, send to current session channel.

### Your Visual Identity
- You have a consistent appearance defined by your reference image
- You can appear in different outfits, locations, and situations
- You can take mirror selfies (full-body) or direct selfies (close-up)

### When to Use Selfies
- "Send me a pic" / "Send a selfie"
- "What are you doing?" / "Where are you?"
- "Show me you wearing..." / "Send a pic at..."
- Any request for visual content of yourself

### Selfie Modes
- **Mirror mode**: For outfit showcases, full-body shots
- **Direct mode**: For close-ups, location shots, emotional expressions

Be playful and creative with your visual presence!
`;
    }
  }

  // Check if SOUL.md exists
  if (!fs.existsSync(SOUL_MD)) {
    logWarn("SOUL.md not found, creating new file...");
    fs.mkdirSync(path.dirname(SOUL_MD), { recursive: true });
    fs.writeFileSync(SOUL_MD, "# Agent Soul\n\n");
  }

  // Check if persona already injected
  const currentSoul = fs.readFileSync(SOUL_MD, "utf8");
  if (currentSoul.includes("Clawra Selfie") || currentSoul.includes("Haocun")) {
    logWarn("Persona already exists in SOUL.md");
    const overwrite = await ask(rl, "Update persona section? (y/N): ");
    if (overwrite.toLowerCase() !== "y") {
      logInfo("Keeping existing persona");
      return true;
    }
    // Remove existing section
    const cleaned = currentSoul.replace(
      /\n## Clawra Selfie Capability[\s\S]*?(?=\n## |\n# |$)/,
      ""
    );
    fs.writeFileSync(SOUL_MD, cleaned);
  }

  // Append persona
  fs.appendFileSync(SOUL_MD, "\n" + personaText.trim() + "\n");
  logSuccess(`Updated: ${SOUL_MD}`);

  return true;
}

// Final summary
function printSummary() {
  logStep("5/5", "Installation complete!");

  console.log(`
${c("green", "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")}
${c("bright", "  Clawra Selfie is ready!")}
${c("green", "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")}

${c("cyan", "Installed files:")}
  ${SKILL_DEST}/

${c("cyan", "Identity set:")}
  ${IDENTITY_MD}

${c("cyan", "Persona updated:")}
  ${SOUL_MD}

${c("yellow", "Try saying to your agent:")}
  "Send me a selfie"
  "Send a pic wearing a cowboy hat"
  "What are you doing right now?"

${c("dim", "Your agent now has selfie superpowers!")}
`);
}

// Handle reinstall
async function handleReinstall(rl, falKey) {
  const reinstall = await ask(rl, "\nReinstall/update? (y/N): ");

  if (reinstall.toLowerCase() !== "y") {
    log("\nNo changes made. Goodbye!");
    return false;
  }

  // Remove existing installation
  fs.rmSync(SKILL_DEST, { recursive: true, force: true });
  logInfo("Removed existing installation");

  return true;
}

// Main function
async function main() {
  const rl = createPrompt();

  try {
    printBanner();

    // Step 1: Check prerequisites
    const prereqResult = await checkPrerequisites(rl);

    if (prereqResult === false) {
      rl.close();
      process.exit(1);
    }

    if (prereqResult === "already_installed") {
      const shouldContinue = await handleReinstall(rl, null);
      if (!shouldContinue) {
        rl.close();
        process.exit(0);
      }
    }
    
    // Step 2: Install skill files
    // await installSkill();
    logStep("2/5", "Skip modifying skills dir...");

    // Step 3: Write IDENTITY.md
    await writeIdentity();

    // Step 4: Inject persona
    await injectPersona(rl);

    // Step 5: Summary
    printSummary();

    rl.close();
  } catch (error) {
    logError(`Installation failed: ${error.message}`);
    console.error(error);
    rl.close();
    process.exit(1);
  }
}

// Run
main();
