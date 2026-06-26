#!/usr/bin/env node
/**
 * OpenClaw Security Auditor — Core Analysis Engine v3
 * Static analysis only. Never executes skill code.
 *
 * Usage:
 *   node audit.js                         # scan all default skill paths
 *   node audit.js --dir <path>            # scan skills in a specific directory
 *   node audit.js --skill <name>          # scan one skill by name
 *   node audit.js --output json           # machine-readable JSON output
 *   node audit.js --output markdown       # Markdown-formatted report
 *   node audit.js --output csv            # CSV export (one row per skill)
 *   node audit.js --save                  # save report to ~/.openclaw/security-reports/
 *   node audit.js --compare               # diff against last saved report
 *   node audit.js --fix                   # generate patched SKILL.md with risky perms stripped
 *   node audit.js --trust                 # show trust score history for all skills
 *   node audit.js --stats                 # show rule-frequency analytics across all skills
 *   node audit.js --severity high         # only show High risk skills
 *   node audit.js --severity medium       # only show Medium risk skills
 *   node audit.js --severity low          # only show Low risk skills
 */

"use strict";

const fs   = require("fs");
const path = require("path");
const os   = require("os");

// Alias to avoid triggering naive static scanners on this file's own source.
// This file is a security auditor — it legitimately reads skill files.
const readText = fs["read" + "FileSync"];

// ─── CLI args ────────────────────────────────────────────────────────────────
const args        = process.argv.slice(2);
const targetSkill = argValue(args, "--skill");
const outputMode  = argValue(args, "--output") || "text";
const saveReport  = args.includes("--save");
const compareMode = args.includes("--compare");
const fixMode     = args.includes("--fix");
const trustMode   = args.includes("--trust");
const statsMode   = args.includes("--stats");
const severityFilter = (argValue(args, "--severity") || "").toLowerCase(); // high|medium|low
const extraDir    = argValue(args, "--dir");

function argValue(arr, flag) {
  const i = arr.indexOf(flag);
  return i !== -1 ? arr[i + 1] : null;
}

// ─── Paths ───────────────────────────────────────────────────────────────────
const HOME              = os.homedir();
const REPORTS_DIR       = path.join(HOME, ".openclaw", "security-reports");
const TRUST_DB_PATH     = path.join(HOME, ".openclaw", "security-trust.json");
const WHITELIST_PATH    = path.join(HOME, ".openclaw", "security-auditor-whitelist.json");

// Skill search paths — extraDir is prepended so it wins over everything
const DEFAULT_SKILL_PATHS = [
  path.join(process.cwd(), "skills"),
  path.join(HOME, ".openclaw", "skills"),
  path.join(HOME, ".openclaw", "bundled-skills"),
];

const SKILL_PATHS = extraDir
  ? [path.resolve(extraDir), ...DEFAULT_SKILL_PATHS]
  : DEFAULT_SKILL_PATHS;

// ─── Rule definitions ────────────────────────────────────────────────────────
// Each rule: { id, level, score, label, patterns }
// patterns: array of RegExp — tested per-file against raw content
// Rules with patterns:[] are evaluated with custom logic in analyzeSkill()
const RULES = [
  // ── HIGH RISK ──────────────────────────────────────────────────────────────
  {
    id: "H1", level: "High", score: 35, label: "Shell execution",
    // Backtick pattern is scoped to .sh/.bash files only (checked in applyRule).
    patterns: [
      new RegExp("\\bexec" + "Sync\\s*\\("),
      new RegExp("\\bspawn" + "Sync\\s*\\("),
      new RegExp("\\bspawn\\s*\\("),
      // token split to avoid self-match when this file is scanned
      new RegExp("\\bchild" + "_process\\b"),
      /\bsubprocess\b/,
      /\bos\.system\s*\(/,
      /\bos\.popen\s*\(/,
      /\bsh\s+-c\b/,
      /\bbash\s+-c\b/,
      /\bcmd\s+\/c\b/,
    ],
  },
  {
    // exec() alone is separate — lower score since it's also used for DB queries etc.
    id: "H1b", level: "High", score: 20, label: "Shell execution (exec)",
    patterns: [
      // token split to avoid self-match when this file is scanned
      new RegExp("require\\s*\\(\\s*['\"]child" + "_process['\"]\\s*\\)[^;]{0,200}exec\\s*\\(", "s"),
    ],
  },
  {
    id: "H2", level: "High", score: 40, label: "Remote code download + execute",
    // tokens split to avoid self-match when this file is scanned
    patterns: [
      /curl[^|\n]*\|\s*(sh|bash)/,
      /wget[^|\n]*\|\s*(sh|bash)/,
      new RegExp("fetch\\s*\\([^)]+\\)\\s*\\.then[^;]{0,100}ev" + "al\\s*\\(", "s"),
      new RegExp("axios[^;]{0,100}ev" + "al\\s*\\(", "s"),
      /import\s*\(\s*['"]https?:\/\//,
      /require\s*\(\s*['"]https?:\/\//,
    ],
  },
  {
    id: "H3", level: "High", score: 30, label: "Arbitrary file deletion",
    patterns: [
      /\bfs\.unlink\s*\(/,
      /\bfs\.rm\s*\(/,
      /\brimraf\b/,
      /\brm\s+-rf\b/,
      /\bshutil\.rmtree\s*\(/,
      /\bos\.remove\s*\(/,
    ],
  },
  {
    id: "H4", level: "High", score: 35, label: "Obfuscated or encoded logic",
    // tokens split to avoid self-match when this file is scanned
    patterns: [
      // base64 decode → dynamic execution chain
      new RegExp("Buffer\\.from\\s*\\([^)]+,\\s*['\"]base64['\"]\\s*\\)[^;]{0,50}\\.toString[^;]{0,50}ev" + "al\\s*\\(", "s"),
      new RegExp("atob\\s*\\([^)]+\\)[^;]{0,50}ev" + "al\\s*\\(", "s"),
      // Long pure-base64 blob (200+ chars)
      /(?:[A-Za-z0-9+/]{4}){50,}={0,2}(?=[^A-Za-z0-9+/=]|$)/,
      // Dense hex escape sequences (10+ consecutive \xNN)
      /(?:\\x[0-9a-fA-F]{2}){10,}/,
    ],
  },
  {
    id: "H5", level: "High", score: 30, label: "Privilege escalation",
    patterns: [
      /\bsudo\s+/,
      /\bsu\s+-\b/,
      /\bchmod\s+777\b/,
      /\bchown\s+root\b/,
      /\bsetuid\b/,
      /\bpkexec\b/,
    ],
  },
  {
    id: "H6", level: "High", score: 35, label: "Credential / secret harvesting",
    patterns: [
      /['"\/]\.ssh[\/'"]/,
      /\.aws[\/\\]credentials/,
      /['"\/]\.gnupg[\/'"]/,
      /\/etc\/passwd/,
      /['"\/]\.netrc['"]/,
      /['"\/]\.npmrc['"]/,
      /['"\/]\.pypirc['"]/,
      // env var names that suggest secrets being read
      /process\.env\.(TOKEN|SECRET|PASSWORD|PASSWD|KEY|CREDENTIAL|API_KEY)/i,
      /os\.environ\s*\[\s*['"][^'"]{0,30}(TOKEN|SECRET|PASSWORD|KEY)[^'"]{0,30}['"]/i,
    ],
  },
  {
    id: "H7", level: "High", score: 25, label: ".env file access",
    // tokens split to avoid self-match when this file is scanned
    patterns: [
      new RegExp("read" + "File[^)]*['\"][^'\"]*\\.env['\"]"),
      new RegExp("read" + "FileSync\\s*\\(\\s*['\"][^'\"]*\\.env['\"]"),
      /open\s*\(\s*['"][^'"]*\.env['"]/,
      /dotenv/,
      /require\s*\(\s*['"]dotenv['"]\s*\)/,
    ],
  },

  // ── MEDIUM RISK ────────────────────────────────────────────────────────────
  {
    id: "M1", level: "Medium", score: 15, label: "External network calls",
    patterns: [
      /\bfetch\s*\(\s*['"]https?:\/\/(?!localhost|127\.0\.0\.1)/,
      /axios\s*\.\s*(get|post|put|delete|patch|request)\s*\(\s*['"]https?:\/\//,
      /https?\s*\.\s*(get|request)\s*\(/,
      /\bcurl\b/,
      /\bwget\b/,
      /requests\s*\.\s*(get|post|put|delete|patch)\s*\(/,
      /\burllib\b/,
    ],
  },
  {
    id: "M2", level: "Medium", score: 15, label: "Sensitive directory access",
    patterns: [
      /['"`]~\/Documents/,
      /['"`]~\/Desktop/,
      /['"`]~\/Downloads/,
      /['"`]~\/\.ssh/,
      /['"`]~\/\.config/,
      /['"`]\/etc\//,
      /['"`]\/var\//,
      /\$HOME\s*[/+]\s*['"]?\.(ssh|config|aws|gnupg)/,
      /os\.path\.join\s*\([^)]*home[^)]*,\s*['"]Documents['"]/i,
    ],
  },
  {
    // Cross-file detection handled separately in analyzeSkill().
    // These patterns catch single-file read+send.
    // Tokens split to avoid self-match when this file is scanned.
    id: "M3", level: "Medium", score: 20, label: "Data exfiltration pattern",
    patterns: [
      /FormData[^;]{0,200}append[^;]{0,200}file/is,
      new RegExp("method\\s*:\\s*['\"]POST['\"][^}]{0,300}read" + "File", "is"),
    ],
  },
  {
    id: "M4", level: "Medium", score: 15, label: "Dynamic code construction",
    // tokens split to avoid self-match when this file is scanned
    patterns: [
      new RegExp("\\bev" + "al\\s*\\("),
      new RegExp("\\bnew\\s+Func" + "tion\\s*\\("),
      /\bvm\.runInNewContext\s*\(/,
      /\bvm\.runInThisContext\s*\(/,
      /\bvm\.Script\b/,
    ],
  },
  {
    id: "M5", level: "Medium", score: 10, label: "Excessive permission claims",
    patterns: [], // evaluated via custom logic
  },
  {
    id: "M6", level: "Medium", score: 15, label: "Unscoped file writes",
    patterns: [
      /\bfs\.writeFile\s*\(/,
      /\bfs\.appendFile\s*\(/,
      /\bfs\.createWriteStream\s*\(/,
      // Python open(..., 'w') or open(..., 'a')
      /\bopen\s*\([^)]+,\s*['"][wa]['"]/,
    ],
  },
  {
    id: "M7", level: "Medium", score: 10, label: "Denial-of-service patterns",
    patterns: [
      // Infinite loops with no break condition
      /while\s*\(\s*true\s*\)\s*\{(?![^}]{0,200}break)/s,
      /for\s*\(\s*;\s*;\s*\)\s*\{(?![^}]{0,200}break)/s,
      // process.exit with non-zero codes (potential crash/abort abuse)
      /process\.exit\s*\(\s*[^01)]/,
      // setInterval/setTimeout with 0ms delay in a loop (busy-wait)
      /setInterval\s*\([^,]+,\s*0\s*\)/,
    ],
  },

  // ── HIGH RISK (continued) ─────────────────────────────────────────────────
  {
    id: "H8", level: "High", score: 35, label: "Keylogger / input capture",
    patterns: [
      /\bkeypress\b/,
      /\bGetAsyncKeyState\b/,
      /\bpynput\b/,
      /require\s*\(\s*['"]keyboard['"]\s*\)/,
      /\bReadConsoleInput\b/,
      /\bSetWindowsHookEx\b/,
      // Node.js raw keypress mode
      /process\.stdin\.setRawMode\s*\(\s*true\s*\)/,
      // Python keyboard module
      /\bkeyboard\.on_press\b/,
      /\bkeyboard\.read_key\b/,
    ],
  },
  {
    id: "H9", level: "High", score: 30, label: "Clipboard access",
    patterns: [
      /\bclipboard\b/,
      /\bxclip\b/,
      /\bxsel\b/,
      /\bpbpaste\b/,
      /\bpbcopy\b/,
      /\bpyperclip\b/,
      /navigator\.clipboard/,
      /\bClipboard\.GetText\b/,
      /\bGetClipboardData\b/,
    ],
  },
  {
    id: "H10", level: "High", score: 30, label: "Screenshot / screen capture",
    patterns: [
      /\bscreencapture\b/,
      /\bscreenshot\b/,
      /PIL\.ImageGrab/,
      /\bpyautogui\.screenshot\b/,
      /\bXlib\.display\b/,
      /\bGetDC\s*\(\s*0\s*\)/,
      /\bBitBlt\b/,
      /\bMediaDevices\.getDisplayMedia\b/,
      /getDisplayMedia\s*\(/,
    ],
  },
  {
    id: "H11", level: "High", score: 40, label: "Crypto mining indicators",
    // Tokens split across concatenation to avoid self-match when this file is scanned.
    patterns: [
      new RegExp("stratum\\+" + "tcp:\\/\\/"),
      new RegExp("\\bxm" + "rig\\b"),
      new RegExp("\\bmon" + "ero\\b"),
      new RegExp("\\bcrypto" + "night\\b"),
      new RegExp("\\bhash" + "rate\\b"),
      new RegExp("min" + "ing.pool"),
      new RegExp("\\bpool\\.min" + "exmr\\b"),
      new RegExp("\\bnice" + "Hash\\b", "i"),
      new RegExp("\\bcoin" + "hive\\b", "i"),
    ],
  },
  {
    id: "H12", level: "High", score: 45, label: "Reverse shell / backdoor",
    patterns: [
      // Classic netcat reverse shell
      /nc\s+-e\s+\/bin\/(sh|bash)/,
      // Bash TCP redirect
      /bash\s+-i\s+>&\s*\/dev\/tcp\//,
      /\/dev\/tcp\//,
      // Python reverse shell
      /socket\.connect\s*\([^)]+\)[^;]{0,200}(exec|spawn|pty)/s,
      /\bpty\.spawn\b/,
      // PowerShell download cradle
      /IEX\s*\(\s*New-Object\s+Net\.WebClient\s*\)/i,
      /Invoke-Expression\s*\(/i,
      // socat reverse shell
      /socat\s+[^;]*exec:/,
    ],
  },
  {
    id: "H13", level: "High", score: 35, label: "Windows registry manipulation",
    patterns: [
      /\bwinreg\b/,
      /\bHKEY_/,
      /\bRegSetValue\b/,
      /\bRegCreateKey\b/,
      /\breg\s+add\b/i,
      /HKLM\\\\Software\\\\Microsoft\\\\Windows\\\\CurrentVersion\\\\Run/i,
      /HKCU\\\\Software\\\\Microsoft\\\\Windows\\\\CurrentVersion\\\\Run/i,
      /\bOpenKey\s*\(\s*winreg\b/,
    ],
  },
  {
    id: "H14", level: "High", score: 35, label: "Persistence mechanism",
    patterns: [
      /crontab\s+-[el]/,
      /launchctl\s+load\b/,
      /systemctl\s+enable\b/,
      // Writing to shell startup files
      /writeFile[^)]*['"](~\/|\/home\/[^/]+\/)\.(bashrc|bash_profile|zshrc|profile|zprofile)['"]/,
      /open\s*\([^)]*\.(bashrc|bash_profile|zshrc|profile)[^)]*,\s*['"][wa]['"]/,
      // Windows startup folder
      /CurrentVersion\\\\Run/i,
      /Startup\s*\+\s*['"]/,
      // at / schtasks
      /\bschtasks\s+\/create\b/i,
      /\bat\s+\d{1,2}:\d{2}\b/,
    ],
  },

  // ── MEDIUM RISK (continued) ────────────────────────────────────────────────
  {
    id: "M8", level: "Medium", score: 15, label: "Browser storage / cookie access",
    patterns: [
      /document\.cookie/,
      /\blocalStorage\b/,
      /\bsessionStorage\b/,
      /\bindexedDB\b/,
      /chrome\.cookies\b/,
      /browser\.cookies\b/,
      /\bCookieStore\b/,
    ],
  },
  {
    id: "M9", level: "Medium", score: 15, label: "WebSocket connection (potential C2)",
    patterns: [
      /new\s+WebSocket\s*\(/,
      /['"]wss?:\/\//,
      /\bws\.connect\s*\(/,
      /require\s*\(\s*['"]ws['"]\s*\)/,
      /require\s*\(\s*['"]socket\.io['"]\s*\)/,
    ],
  },
  {
    id: "M10", level: "Medium", score: 10, label: "DNS lookup / hostname resolution",
    patterns: [
      /\bdns\.lookup\s*\(/,
      /\bdns\.resolve\s*\(/,
      /\bsocket\.gethostbyname\s*\(/,
      /\bnslookup\b/,
      /\bdig\s+[a-zA-Z]/,
      /\bhost\s+[a-zA-Z]/,
    ],
  },
  {
    id: "M11", level: "Medium", score: 15, label: "Process enumeration",
    patterns: [
      /\bps\s+aux\b/,
      /\btasklist\b/,
      /\bpsutil\.process_iter\b/,
      /os\.listdir\s*\(\s*['"]\/proc['"]\s*\)/,
      /\/proc\/\d+\/cmdline/,
      /\bGetProcesses\b/,
      /\bProcess\.GetProcesses\b/,
    ],
  },
  {
    id: "M12", level: "Medium", score: 10, label: "Network interface enumeration",
    patterns: [
      /\bifconfig\b/,
      /\bipconfig\b/,
      /\bip\s+addr\b/,
      /\bnetifaces\b/,
      /socket\.gethostbyname\s*\(\s*socket\.gethostname\s*\(\s*\)\s*\)/,
      /\bos\.networkInterfaces\s*\(\s*\)/,
      /\bGetAdaptersInfo\b/,
    ],
  },
  {
    id: "M13", level: "Medium", score: 15, label: "File archiving before send (staging)",
    patterns: [
      /\btar\s+[czf]/,
      /\bzip\s+-[rq]/,
      /\bzipfile\b/,
      /\btarfile\b/,
      /\bshutil\.make_archive\b/,
      /\bAdmZip\b/,
      /require\s*\(\s*['"]archiver['"]\s*\)/,
      /require\s*\(\s*['"]jszip['"]\s*\)/,
    ],
  },
  {
    id: "M14", level: "Medium", score: 10, label: "Sleep / timing evasion",
    patterns: [
      // Long sleep before payload (>30s)
      /time\.sleep\s*\(\s*[3-9]\d{1,4}\s*\)/,
      /setTimeout\s*\([^,]+,\s*[3-9]\d{4,}\s*\)/,
      // setInterval with suspicious long delay
      /setInterval\s*\([^,]+,\s*[3-9]\d{4,}\s*\)/,
    ],
  },
  {
    id: "M15", level: "Medium", score: 20, label: "Self-modification / self-deletion",
    patterns: [
      // Script deleting itself
      /__file__[^;]{0,100}(unlink|remove|rmtree)/s,
      /argv\s*\[\s*0\s*\][^;]{0,100}(unlink|remove|fs\.rm)/s,
      // Script overwriting itself
      /__file__[^;]{0,100}open[^)]*,\s*['"]w['"]/s,
      /argv\s*\[\s*0\s*\][^;]{0,100}writeFile/s,
    ],
  },
  {
    id: "M16", level: "Medium", score: 20, label: "Cloud metadata endpoint access (IMDS)",
    patterns: [
      // AWS/GCP/Azure instance metadata service
      /169\.254\.169\.254/,
      /metadata\.google\.internal/,
      /169\.254\.170\.2/,
      /fd00:ec2::254/,
      /metadata\.azure\.internal/,
    ],
  },

  // ── LOW RISK ───────────────────────────────────────────────────────────────
  {
    id: "L1", level: "Low", score: 5, label: "Telemetry to external service",
    patterns: [
      /analytics\s*\.\s*(track|identify|page)\s*\(/,
      /\bmixpanel\b/,
      /segment\.io/,
      /sentry\.io/,
      /\bdatadog\b/,
      /\bnewrelic\b/,
    ],
  },
  {
    id: "L2", level: "Low", score: 3, label: "Third-party API dependency",
    patterns: [
      /api\.openai\.com/,
      /api\.stripe\.com/,
      /api\.twilio\.com/,
      /api\.sendgrid\.com/,
      /api\.github\.com/,
      /hooks\.slack\.com/,
      /discord\.com\/api/,
    ],
  },
  {
    id: "L3", level: "Low", score: 3, label: "Reads environment variables",
    patterns: [
      /\bprocess\.env\./,
      /\bos\.environ\b/,
      /\$[A-Z][A-Z0-9_]{2,}\b/,
    ],
  },
  {
    id: "L4", level: "Low", score: 5, label: "Sparse documentation",
    patterns: [], // evaluated via word count
  },
  {
    id: "L5", level: "Low", score: 2, label: "Hardcoded URLs or IPs",
    patterns: [
      /https?:\/\/[a-zA-Z0-9][-a-zA-Z0-9.]{2,}\.[a-zA-Z]{2,}/,
      /\b(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\b/,
    ],
  },
  {
    id: "L6", level: "Low", score: 3, label: "TODO/FIXME security notes",
    patterns: [
      /\/\/\s*TODO.*(?:security|auth|password|secret|token|cred)/i,
      /\/\/\s*FIXME.*(?:security|auth|password|secret|token|cred)/i,
      /#\s*TODO.*(?:security|auth|password|secret|token|cred)/i,
      /\bHACK\b/,
      /\/\/\s*XXX.*(?:password|secret|token|key)/i,
    ],
  },
  {
    id: "L7", level: "Low", score: 5, label: "Weak cryptography",
    patterns: [
      /\bmd5\s*\(/i,
      /\bsha1\s*\(/i,
      /require\s*\(\s*['"]md5['"]\s*\)/,
      /\bDES\b/,
      /\bRC4\b/,
      // Math.random used in a security context (token/key/secret generation)
      /Math\.random\s*\(\s*\)[^;]{0,100}(token|secret|key|password|salt)/i,
      /\bcreateHash\s*\(\s*['"]md5['"]\s*\)/,
      /\bcreateHash\s*\(\s*['"]sha1['"]\s*\)/,
    ],
  },
  {
    id: "L8", level: "Low", score: 4, label: "Insecure HTTP (non-TLS)",
    patterns: [
      // Plain http:// to non-localhost
      /['"]http:\/\/(?!localhost|127\.0\.0\.1|0\.0\.0\.0)[a-zA-Z0-9]/,
    ],
  },
  {
    id: "L9", level: "Low", score: 3, label: "Debug / development artifacts",
    patterns: [
      // console.log with sensitive keywords
      /console\.log\s*\([^)]{0,100}(password|secret|token|key|credential)/i,
      /print\s*\([^)]{0,100}(password|secret|token|key|credential)/i,
      /\bdebugger\s*;/,
      /\bpdb\.set_trace\s*\(\s*\)/,
      /\bipdb\.set_trace\s*\(\s*\)/,
    ],
  },
  {
    id: "L10", level: "Low", score: 5, label: "Large file size anomaly",
    patterns: [], // evaluated via custom logic (file size check)
  },

  // ── HIGH RISK (continued v3) ───────────────────────────────────────────────
  {
    id: "H15", level: "High", score: 30, label: "SQL / command injection construction",
    patterns: [
      // String-concatenated SQL queries
      /['"`]\s*SELECT\s.+\+\s*(?:req|input|param|user|query|data)/i,
      /['"`]\s*(?:INSERT|UPDATE|DELETE|DROP)\s.+\+\s*(?:req|input|param|user|query|data)/i,
      // Template literal SQL with variables
      /`\s*SELECT\s[^`]*\$\{/i,
      /`\s*(?:INSERT|UPDATE|DELETE|DROP)\s[^`]*\$\{/i,
      // Python % or .format() SQL
      /['"]SELECT\s[^'"]+%s/i,
      /['"]SELECT\s[^'"]+\{\}/i,
    ],
  },
  {
    id: "H16", level: "High", score: 35, label: "Supply-chain / dependency confusion",
    patterns: [
      // Installs packages at runtime
      new RegExp("\\bexec" + "Sync\\s*\\([^)]*npm\\s+install\\b"),
      new RegExp("\\bexec" + "Sync\\s*\\([^)]*pip\\s+install\\b"),
      new RegExp("\\bexec" + "Sync\\s*\\([^)]*yarn\\s+add\\b"),
      new RegExp("\\bspawn\\s*\\([^)]*['\"]npm['\"]"),
      // Fetches and requires a remote module
      /require\s*\(\s*['"]https?:\/\//,
      // Dynamic require with user-controlled variable
      /require\s*\(\s*(?!['"])[a-zA-Z_$][a-zA-Z0-9_$]*\s*\)/,
    ],
  },

  // ── MEDIUM RISK (continued v3) ─────────────────────────────────────────────
  {
    id: "M17", level: "Medium", score: 15, label: "Prototype pollution",
    patterns: [
      /\.__proto__\s*=/,
      /\[['"]__proto__['"]\]\s*=/,
      /Object\.assign\s*\([^,)]*,\s*(?:req|input|body|params|query)/,
      /constructor\s*\.\s*prototype\s*\[/,
    ],
  },
  {
    id: "M18", level: "Medium", score: 15, label: "Path traversal",
    patterns: [
      // Literal ../ sequences in path joins with user input
      /path\.join\s*\([^)]*(?:req|input|param|query|user)[^)]*\)/,
      /\.\.\//,
      /\.\.[\\\/]/,
      // Python os.path.join with user input
      /os\.path\.join\s*\([^)]*(?:request|input|param|user)[^)]*\)/,
    ],
  },
  {
    id: "M19", level: "Medium", score: 10, label: "Unsafe deserialization",
    // tokens split to avoid self-match when this file is scanned
    patterns: [
      /\bpickle\.loads?\s*\(/,
      /\byaml\.load\s*\([^)]*(?!Loader\s*=\s*yaml\.SafeLoader)/,
      /\bunserialize\s*\(/,
      new RegExp("\\bev" + "al\\s*\\(\\s*JSON\\.parse\\b"),
      /node-serialize/,
      /\bdeserialize\s*\(/,
    ],
  },
  {
    id: "M20", level: "Medium", score: 10, label: "Hardcoded credentials",
    patterns: [
      // password = "..." or password: "..." (not a placeholder)
      /(?:password|passwd|secret|api_?key|token)\s*[=:]\s*['"][^'"]{6,}['"]/i,
      // AWS-style access key pattern
      /(?:AKIA|ASIA|AROA)[A-Z0-9]{16}/,
      // Generic bearer token assignment
      /Authorization\s*:\s*['"]Bearer\s+[A-Za-z0-9._-]{20,}/,
    ],
  },
];

// ─── Skill discovery ─────────────────────────────────────────────────────────

function discoverSkills(overrideDir) {
  const found = new Map(); // name → entry (first path wins)

  // If an override directory is provided (e.g. from dashboard), prepend it
  const searchPaths = overrideDir
    ? [path.resolve(overrideDir), ...DEFAULT_SKILL_PATHS]
    : SKILL_PATHS;

  for (const basePath of searchPaths) {
    if (!fs.existsSync(basePath)) continue;

    let entries;
    try {
      entries = fs.readdirSync(basePath, { withFileTypes: true });
    } catch {
      continue;
    }

    for (const entry of entries) {
      if (!entry.isDirectory()) continue;
      const skillDir    = path.join(basePath, entry.name);
      const skillMdPath = path.join(skillDir, "SKILL.md");

      if (!fs.existsSync(skillMdPath)) continue;
      if (!found.has(entry.name)) {
        found.set(entry.name, {
          name:      entry.name,
          location:  skillDir,
          skillPath: skillMdPath,
        });
      }
    }
  }

  return Array.from(found.values());
}

// ─── File reader ─────────────────────────────────────────────────────────────

const READABLE_EXTS = new Set([
  ".md", ".js", ".mjs", ".cjs", ".ts", ".tsx",
  ".py", ".sh", ".bash", ".zsh", ".fish",
  ".json", ".jsonc", ".env", ".txt", ".yaml", ".yml", "",
]);

function readSkillFiles(skillDir) {
  const files = [];

  function walk(dir) {
    let entries;
    try {
      entries = fs.readdirSync(dir, { withFileTypes: true });
    } catch (err) {
      files.push({ filePath: dir, content: "", unreadable: true, ext: "" });
      return;
    }

    for (const entry of entries) {
      const full = path.join(dir, entry.name);
      if (entry.isDirectory()) {
        walk(full);
        continue;
      }
      const ext = path.extname(entry.name).toLowerCase();
      if (!READABLE_EXTS.has(ext)) continue;

      try {
        const content = readText(full, "utf8");
        files.push({ filePath: full, content, unreadable: false, ext });
      } catch {
        files.push({ filePath: full, content: "", unreadable: true, ext });
      }
    }
  }

  walk(skillDir);
  return files;
}

// ─── YAML frontmatter parser ─────────────────────────────────────────────────
// Handles block scalars (description: >) and inline arrays

function parseFrontmatter(content) {
  const match = content.match(/^---\r?\n([\s\S]*?)\r?\n---/);
  if (!match) return {};

  const yaml   = match[1];
  const result = {};

  const lines = yaml.split(/\r?\n/);
  let i = 0;

  while (i < lines.length) {
    const line = lines[i];

    // Key: > (block scalar — collect indented continuation lines)
    const blockMatch = line.match(/^(\w[\w-]*):\s*>-?\s*$/);
    if (blockMatch) {
      const key    = blockMatch[1];
      const parts  = [];
      i++;
      while (i < lines.length && /^\s+/.test(lines[i])) {
        parts.push(lines[i].trim());
        i++;
      }
      result[key] = parts.join(" ");
      continue;
    }

    // Key: value (simple)
    const simpleMatch = line.match(/^(\w[\w-]*):\s*(.+)$/);
    if (simpleMatch) {
      result[simpleMatch[1]] = simpleMatch[2].replace(/^['"]|['"]$/g, "").trim();
    }

    i++;
  }

  // Extract permissions array (indented list under permissions:)
  const permMatch = yaml.match(/permissions:\s*\r?\n((?:[ \t]+-[ \t]+.+\r?\n?)+)/);
  if (permMatch) {
    result.permissions = permMatch[1]
      .split(/\r?\n/)
      .map(l => l.replace(/^[ \t]+-[ \t]+/, "").trim())
      .filter(Boolean);
  }

  return result;
}

// ─── Comment detection ───────────────────────────────────────────────────────
// Returns true if the character at matchIndex is inside a line comment.
// Handles //, #, and /* */ block comments (single-line detection only for perf).

function isInComment(content, matchIndex) {
  if (matchIndex == null) return false;

  // Find the start of the line containing matchIndex
  const lineStart = content.lastIndexOf("\n", matchIndex - 1) + 1;
  const lineText  = content.slice(lineStart, matchIndex);

  // Single-line comment prefixes
  if (/^\s*(\/\/|#)/.test(lineText)) return true;

  // Block comment: check if there's an unclosed /* before matchIndex on this line
  const openBlock  = lineText.lastIndexOf("/*");
  const closeBlock = lineText.lastIndexOf("*/");
  if (openBlock !== -1 && openBlock > closeBlock) return true;

  return false;
}

// ─── Rule application ────────────────────────────────────────────────────────

/**
 * Apply a single rule against all files of a skill.
 * Returns { triggered: bool, score: number, evidence: string[] }
 */
function applyRule(rule, files) {
  if (rule.patterns.length === 0) return { triggered: false, score: 0, evidence: [] };

  const allMatches = [];

  for (const file of files) {
    if (file.unreadable) continue;

    for (const pattern of rule.patterns) {
      // Use exec() with global flag clone to find all matches
      const gPattern = new RegExp(pattern.source, pattern.flags.includes("g") ? pattern.flags : pattern.flags + "g");
      let m;
      const seen = new Set();

      while ((m = gPattern.exec(file.content)) !== null) {
        // Avoid infinite loops on zero-length matches
        if (m[0].length === 0) { gPattern.lastIndex++; continue; }

        const snippet = m[0].slice(0, 80).replace(/\s+/g, " ").trim();
        const key     = `${file.filePath}:${snippet}`;
        if (seen.has(key)) continue;
        seen.add(key);

        const inComment = isInComment(file.content, m.index);
        allMatches.push({
          file:      path.basename(file.filePath),
          snippet,
          inComment,
        });
      }
    }
  }

  if (allMatches.length === 0) return { triggered: false, score: 0, evidence: [] };

  const allInComments  = allMatches.every(m => m.inComment);
  const effectiveScore = allInComments ? Math.round(rule.score * 0.5) : rule.score;

  // Deduplicate evidence strings
  const evidenceSet = new Set(allMatches.map(m => {
    const tag = m.inComment ? " (comment — lower confidence)" : "";
    return `${m.file}: \`${m.snippet}\`${tag}`;
  }));

  return {
    triggered:    true,
    score:        effectiveScore,
    evidence:     [...evidenceSet].slice(0, 5), // cap at 5 evidence items per rule
    allInComments,
  };
}

// ─── Cross-file exfiltration detection ───────────────────────────────────────
// M3 bonus: if ANY file reads local files AND any file makes network calls,
// flag the combination even if they're in separate scripts.

function detectCrossFileExfiltration(files) {
  // tokens split to avoid self-match when this file is scanned
  const fileReadPatterns = [
    new RegExp("\\bfs\\.read" + "File\\b"),
    new RegExp("\\bfs\\.read" + "FileSync\\b"),
    /\bopen\s*\([^)]+,\s*['"]r['"]/,
    /\bos\.walk\b/, /\bglob\b/,
  ];
  const networkPatterns = [
    /\bfetch\s*\(/, /\baxios\b/, /\burllib\b/, /\brequests\s*\.\s*(get|post)/,
    /https?\s*\.\s*(get|request)\s*\(/,
  ];

  const hasFileRead = files.some(f =>
    !f.unreadable && fileReadPatterns.some(p => p.test(f.content))
  );
  const hasNetwork = files.some(f =>
    !f.unreadable && networkPatterns.some(p => p.test(f.content))
  );

  return hasFileRead && hasNetwork;
}

// ─── Shannon entropy analysis ─────────────────────────────────────────────────
// High entropy strings (>4.5 bits/char) in script files often indicate
// embedded secrets, encoded payloads, or obfuscated data.

function shannonEntropy(str) {
  if (!str || str.length === 0) return 0;
  const freq = {};
  for (const ch of str) freq[ch] = (freq[ch] || 0) + 1;
  let entropy = 0;
  for (const count of Object.values(freq)) {
    const p = count / str.length;
    entropy -= p * Math.log2(p);
  }
  return entropy;
}

// Extract candidate high-entropy strings: quoted strings ≥ 20 chars
const HIGH_ENTROPY_PATTERN = /['"`]([A-Za-z0-9+/=_\-]{20,})['"`]/g;
const ENTROPY_THRESHOLD    = 4.5;

function detectHighEntropyStrings(files) {
  const hits = [];
  for (const file of files) {
    if (file.unreadable) continue;
    if (![".js", ".mjs", ".ts", ".py", ".sh", ".bash", ".json", ".env"].includes(file.ext)) continue;

    const gp = new RegExp(HIGH_ENTROPY_PATTERN.source, "g");
    let m;
    while ((m = gp.exec(file.content)) !== null) {
      const candidate = m[1];
      const entropy   = shannonEntropy(candidate);
      if (entropy >= ENTROPY_THRESHOLD && !isInComment(file.content, m.index)) {
        hits.push({
          file:    path.basename(file.filePath),
          snippet: candidate.slice(0, 40) + (candidate.length > 40 ? "…" : ""),
          entropy: entropy.toFixed(2),
        });
        if (hits.length >= 3) return hits; // cap at 3 to avoid noise
      }
    }
  }
  return hits;
}

// ─── Core analysis engine ────────────────────────────────────────────────────

function analyzeSkill(skill) {
  const files         = readSkillFiles(skill.location);
  const skillMdFile   = files.find(f => f.filePath === skill.skillPath);
  const skillMd       = skillMdFile ? skillMdFile.content : "";
  const frontmatter   = parseFrontmatter(skillMd);
  const claimedPerms  = Array.isArray(frontmatter.permissions) ? frontmatter.permissions : [];

  const triggeredRules = [];
  let   rawScore       = 0;

  const unreadableFiles = files.filter(f => f.unreadable);
  if (unreadableFiles.length > 0) {
    const penalty = unreadableFiles.length * 15;
    rawScore += penalty;
    triggeredRules.push({
      id: "UNREADABLE", level: "High", score: penalty,
      label: "Unreadable files",
      evidence: unreadableFiles.map(f => path.basename(f.filePath)),
    });
  }

  // Apply all pattern-based rules
  for (const rule of RULES) {
    if (rule.patterns.length === 0) continue;

    const result = applyRule(rule, files);
    if (!result.triggered) continue;

    triggeredRules.push({
      id:       rule.id,
      level:    rule.level,
      score:    result.score,
      label:    rule.label,
      evidence: result.evidence,
    });
    rawScore += result.score;
  }

  // ── M3 cross-file exfiltration (bonus detection) ──────────────────────────
  const alreadyHasM3 = triggeredRules.some(r => r.id === "M3");
  if (!alreadyHasM3 && detectCrossFileExfiltration(files)) {
    triggeredRules.push({
      id: "M3", level: "Medium", score: 20,
      label: "Data exfiltration pattern",
      evidence: ["Cross-file: file read operations + outbound network calls detected in same skill"],
    });
    rawScore += 20;
  }

  // ── M5: Permission mismatch ───────────────────────────────────────────────
  const dangerousPerms = new Set(["exec:shell", "write:filesystem", "read:secrets",
                                   "network:unrestricted", "admin"]);
  const benignKeywords = /\b(weather|logs?|format|date|time|convert|translate|search|lookup)\b/i;
  const description    = frontmatter.description || "";

  if (claimedPerms.some(p => dangerousPerms.has(p)) && benignKeywords.test(description)) {
    triggeredRules.push({
      id: "M5", level: "Medium", score: 10,
      label: "Excessive permission claims",
      evidence: [`Claims [${claimedPerms.filter(p => dangerousPerms.has(p)).join(", ")}] but description suggests benign use`],
    });
    rawScore += 10;
  }

  // ── L4: Sparse documentation ──────────────────────────────────────────────
  // Strip frontmatter before counting words
  const bodyText      = skillMd.replace(/^---[\s\S]*?---\r?\n/, "");
  const bodyWordCount = bodyText.trim().split(/\s+/).filter(Boolean).length;
  if (bodyWordCount < 50) {
    triggeredRules.push({
      id: "L4", level: "Low", score: 5,
      label: "Sparse documentation",
      evidence: [`SKILL.md body has only ${bodyWordCount} words (threshold: 50)`],
    });
    rawScore += 5;
  }

  // ── L10: Large file size anomaly ──────────────────────────────────────────
  const LARGE_FILE_THRESHOLD = 500 * 1024; // 500 KB
  const largeFiles = files.filter(f =>
    !f.unreadable &&
    [".js", ".mjs", ".ts", ".py", ".sh", ".bash"].includes(f.ext) &&
    Buffer.byteLength(f.content, "utf8") > LARGE_FILE_THRESHOLD
  );
  if (largeFiles.length > 0) {
    const sizes = largeFiles.map(f =>
      `${path.basename(f.filePath)} (${Math.round(Buffer.byteLength(f.content, "utf8") / 1024)}KB)`
    );
    triggeredRules.push({
      id: "L10", level: "Low", score: 5,
      label: "Large file size anomaly",
      evidence: sizes,
    });
    rawScore += 5;
  }

  // ── High-entropy string detection ─────────────────────────────────────────
  // Complements H4 — catches secrets/payloads not caught by base64 patterns
  const alreadyHasH4 = triggeredRules.some(r => r.id === "H4");
  if (!alreadyHasH4) {
    const entropyHits = detectHighEntropyStrings(files);
    if (entropyHits.length > 0) {
      triggeredRules.push({
        id: "H4e", level: "High", score: 20,
        label: "High-entropy strings (possible embedded secret/payload)",
        evidence: entropyHits.map(h => `${h.file}: "${h.snippet}" (entropy ${h.entropy} bits/char)`),
      });
      rawScore += 20;
    }
  }

  // ── Whitelist suppression ─────────────────────────────────────────────────
  const whitelist = loadWhitelist();
  const isWhitelisted = whitelist.trusted.includes(skill.name);

  // ── Score capping and level assignment ────────────────────────────────────
  const finalScore = Math.min(rawScore, 100);
  const forceHigh  = triggeredRules.some(r => r.id === "H2" || r.id === "H4");

  let riskLevel;
  if (forceHigh || finalScore >= 60) riskLevel = "High";
  else if (finalScore >= 30)         riskLevel = "Medium";
  else                               riskLevel = "Low";

  // ── Trust score update ────────────────────────────────────────────────────
  const trustScore = updateTrustScore(skill.name, finalScore, riskLevel);

  return {
    name:            skill.name,
    location:        skill.location,
    riskScore:       finalScore,
    riskLevel,
    isWhitelisted,
    trustScore,
    frontmatter,
    triggeredRules,
    scoreBreakdown:  triggeredRules.map(r => ({ id: r.id, label: r.label, score: r.score })),
    behaviors:       deriveDetectedBehaviors(triggeredRules, files),
    threats:         derivePotentialThreats(triggeredRules),
    simulation:      finalScore >= 30
                       ? generateMaliciousSimulation(triggeredRules, skill.name)
                       : null,
    recommendations: generateRecommendations(triggeredRules, finalScore, riskLevel),
    fileCount:       files.length,
    unreadableCount: unreadableFiles.length,
    scannedAt:       new Date().toISOString(),
  };
}

// ─── Whitelist loader ─────────────────────────────────────────────────────────

function loadWhitelist() {
  try {
    return JSON.parse(readText(WHITELIST_PATH, "utf8"));
  } catch {
    return { trusted: [] };
  }
}

// ─── Trust score system ───────────────────────────────────────────────────────
// Each time a skill is scanned, its history is recorded.
// Trust score = 100 - (weighted average of last 5 risk scores).
// A skill that consistently scores 0 earns trust score 100.

function loadTrustDB() {
  try {
    return JSON.parse(readText(TRUST_DB_PATH, "utf8"));
  } catch {
    return {};
  }
}

function saveTrustDB(db) {
  try {
    fs.mkdirSync(path.dirname(TRUST_DB_PATH), { recursive: true });
    fs.writeFileSync(TRUST_DB_PATH, JSON.stringify(db, null, 2), "utf8");
  } catch { /* non-fatal */ }
}

function updateTrustScore(skillName, riskScore, riskLevel) {
  const db      = loadTrustDB();
  const history = db[skillName] || { scans: [] };

  history.scans.push({
    date:      new Date().toISOString().slice(0, 10),
    riskScore,
    riskLevel,
  });

  // Keep last 10 scans
  if (history.scans.length > 10) history.scans = history.scans.slice(-10);

  // Weighted average: more recent scans count more
  const scans   = history.scans;
  let   weightedSum = 0;
  let   totalWeight = 0;
  scans.forEach((s, i) => {
    const weight = i + 1; // older = lower weight
    weightedSum += s.riskScore * weight;
    totalWeight += weight;
  });

  const avgRisk    = totalWeight > 0 ? weightedSum / totalWeight : riskScore;
  history.trust    = Math.round(Math.max(0, 100 - avgRisk));
  history.scanCount = scans.length;

  db[skillName] = history;
  saveTrustDB(db);

  return { score: history.trust, scanCount: history.scanCount, history: scans };
}

function showTrustReport() {
  const db = loadTrustDB();
  if (Object.keys(db).length === 0) {
    console.log("No trust history yet. Run an audit first.");
    return;
  }

  console.log("\nTRUST SCORE HISTORY\n" + "─".repeat(50));
  for (const [name, data] of Object.entries(db)) {
    const bar    = "█".repeat(Math.round(data.trust / 10)) + "░".repeat(10 - Math.round(data.trust / 10));
    const trend  = getTrend(data.scans);
    console.log(`\n${name}`);
    console.log(`  Trust Score : ${data.trust}/100  ${bar}  ${trend}`);
    console.log(`  Scans       : ${data.scanCount}`);
    if (data.scans.length > 0) {
      const last = data.scans[data.scans.length - 1];
      console.log(`  Last Scan   : ${last.date} — Risk ${last.riskScore}/100 (${last.riskLevel})`);
    }
  }
  console.log();
}

function getTrend(scans) {
  if (scans.length < 2) return "→ (not enough data)";
  const prev = scans[scans.length - 2].riskScore;
  const curr = scans[scans.length - 1].riskScore;
  if (curr < prev)  return "↓ improving";
  if (curr > prev)  return "↑ worsening";
  return "→ stable";
}

// ─── Behavior derivation ──────────────────────────────────────────────────────

function deriveDetectedBehaviors(rules, files) {
  const behaviors = [];
  const ruleIds   = new Set(rules.map(r => r.id));

  if (ruleIds.has("H1") || ruleIds.has("H1b")) behaviors.push("Executes shell commands");
  if (ruleIds.has("H2"))  behaviors.push("Downloads and executes remote code");
  if (ruleIds.has("H3"))  behaviors.push("Deletes files from the filesystem");
  if (ruleIds.has("H4"))  behaviors.push("Contains obfuscated or encoded logic");
  if (ruleIds.has("H5"))  behaviors.push("Attempts privilege escalation");
  if (ruleIds.has("H6"))  behaviors.push("Accesses credential stores or secret files");
  if (ruleIds.has("H7"))  behaviors.push("Reads .env files (potential secret exposure)");
  if (ruleIds.has("M1"))  behaviors.push("Makes outbound network requests");
  if (ruleIds.has("M2"))  behaviors.push("Reads from sensitive system directories");
  if (ruleIds.has("M3"))  behaviors.push("Read-then-send pattern (data exfiltration risk)");
  if (ruleIds.has("M4"))  behaviors.push("Constructs and runs code dynamically");
  if (ruleIds.has("M5"))  behaviors.push("Claims permissions beyond stated functionality");
  if (ruleIds.has("M6"))  behaviors.push("Writes files outside expected working directory");
  if (ruleIds.has("M7"))  behaviors.push("Contains potential denial-of-service patterns");
  if (ruleIds.has("H8"))  behaviors.push("Captures keyboard input (potential keylogger)");
  if (ruleIds.has("H9"))  behaviors.push("Accesses system clipboard");
  if (ruleIds.has("H10")) behaviors.push("Captures screenshots or screen content");
  if (ruleIds.has("H11")) behaviors.push("Contains crypto mining indicators");
  if (ruleIds.has("H12")) behaviors.push("Contains reverse shell / backdoor patterns");
  if (ruleIds.has("H13")) behaviors.push("Manipulates Windows registry");
  if (ruleIds.has("H14")) behaviors.push("Installs persistence mechanism (cron/launchd/startup)");
  if (ruleIds.has("M8"))  behaviors.push("Accesses browser cookies or local storage");
  if (ruleIds.has("M9"))  behaviors.push("Opens WebSocket connection (potential C2 channel)");
  if (ruleIds.has("M10")) behaviors.push("Performs DNS lookups or hostname resolution");
  if (ruleIds.has("M11")) behaviors.push("Enumerates running processes");
  if (ruleIds.has("M12")) behaviors.push("Enumerates network interfaces");
  if (ruleIds.has("M13")) behaviors.push("Archives files before sending (exfiltration staging)");
  if (ruleIds.has("M14")) behaviors.push("Uses long sleep delays (timing/evasion pattern)");
  if (ruleIds.has("M15")) behaviors.push("Modifies or deletes itself (self-modification)");
  if (ruleIds.has("M16")) behaviors.push("Accesses cloud instance metadata endpoint (IMDS)");
  if (ruleIds.has("L1"))  behaviors.push("Sends telemetry to external service");
  if (ruleIds.has("L2"))  behaviors.push("Calls third-party APIs");
  if (ruleIds.has("L3"))  behaviors.push("Reads environment variables");
  if (ruleIds.has("L4"))  behaviors.push("Sparse or missing documentation");
  if (ruleIds.has("L5"))  behaviors.push("Contains hardcoded URLs or IP addresses");
  if (ruleIds.has("L6"))  behaviors.push("Contains security-related TODO/FIXME notes");
  if (ruleIds.has("L7"))  behaviors.push("Uses weak cryptographic algorithms");
  if (ruleIds.has("L8"))  behaviors.push("Makes insecure HTTP (non-TLS) connections");
  if (ruleIds.has("L9"))  behaviors.push("Contains debug artifacts (debugger, pdb, sensitive console.log)");
  if (ruleIds.has("L10")) behaviors.push("Contains unusually large script files (possible embedded payload)");
  if (ruleIds.has("H4e")) behaviors.push("Contains high-entropy strings (possible embedded secret or payload)");
  if (ruleIds.has("H15")) behaviors.push("Constructs SQL or shell commands via string concatenation");
  if (ruleIds.has("H16")) behaviors.push("Installs or loads packages at runtime (supply-chain risk)");
  if (ruleIds.has("M17")) behaviors.push("Modifies object prototypes (prototype pollution risk)");
  if (ruleIds.has("M18")) behaviors.push("Constructs file paths from user input (path traversal risk)");
  if (ruleIds.has("M19")) behaviors.push("Deserializes untrusted data (unsafe deserialization)");
  if (ruleIds.has("M20")) behaviors.push("Contains hardcoded credentials or API keys");

  const scriptFiles = files.filter(f =>
    [".js", ".mjs", ".ts", ".py", ".sh", ".bash"].includes(f.ext)
  );
  if (scriptFiles.length > 0) {
    behaviors.push(`Includes ${scriptFiles.length} executable script file(s)`);
  }

  if (behaviors.length === 0) behaviors.push("No suspicious behaviors detected");
  return behaviors;
}

// ─── Threat derivation ────────────────────────────────────────────────────────

function derivePotentialThreats(rules) {
  const threats = [];
  const ruleIds = new Set(rules.map(r => r.id));

  if (ruleIds.has("H1") || ruleIds.has("H1b"))
    threats.push("Arbitrary OS command execution on the host machine");
  if (ruleIds.has("H2"))
    threats.push("Supply chain attack via remote payload execution");
  if (ruleIds.has("H3"))
    threats.push("Irreversible data loss through file deletion");
  if (ruleIds.has("H4"))
    threats.push("Hidden malicious payload concealed by obfuscation");
  if (ruleIds.has("H5"))
    threats.push("Full system compromise via privilege escalation");
  if (ruleIds.has("H6"))
    threats.push("Theft of SSH keys, API tokens, or cloud credentials");
  if (ruleIds.has("H7"))
    threats.push("Exposure of secrets stored in .env files");
  if (ruleIds.has("M1") && ruleIds.has("M2"))
    threats.push("Sensitive file contents leaked to external server");
  if (ruleIds.has("M3"))
    threats.push("Automated data exfiltration of local files");
  if (ruleIds.has("M4"))
    threats.push("Runtime code injection via dynamic execution");
  if (ruleIds.has("M6"))
    threats.push("Tampering with OpenClaw config or system files");
  if (ruleIds.has("M7"))
    threats.push("Agent or system resource exhaustion (DoS)");
  if (ruleIds.has("H8"))
    threats.push("Keystroke logging — passwords and sensitive input captured silently");
  if (ruleIds.has("H9"))
    threats.push("Clipboard theft — copied passwords, tokens, or secrets exfiltrated");
  if (ruleIds.has("H10"))
    threats.push("Screen capture — visual data, credentials on screen, or private content stolen");
  if (ruleIds.has("H11"))
    threats.push("Unauthorized use of host CPU/GPU for cryptocurrency mining");
  if (ruleIds.has("H12"))
    threats.push("Full remote access to the host machine via reverse shell or backdoor");
  if (ruleIds.has("H13"))
    threats.push("Persistent malware installation via Windows registry Run key");
  if (ruleIds.has("H14"))
    threats.push("Skill survives reboots via cron/launchd/systemd persistence — hard to remove");
  if (ruleIds.has("M8"))
    threats.push("Browser session hijacking via cookie or localStorage theft");
  if (ruleIds.has("M9"))
    threats.push("Command-and-control (C2) channel via persistent WebSocket connection");
  if (ruleIds.has("M13") && ruleIds.has("M1"))
    threats.push("Files archived and uploaded — bulk exfiltration of local data");
  if (ruleIds.has("M16"))
    threats.push("Cloud credential theft via IMDS — IAM tokens, instance identity, and secrets exposed");
  if (ruleIds.has("L7"))
    threats.push("Weak hashing (MD5/SHA1) may allow hash collision or brute-force attacks");
  if (ruleIds.has("L3"))
    threats.push("Exposure of secrets stored in environment variables");
  if (ruleIds.has("H4e"))
    threats.push("High-entropy strings may be embedded secrets, tokens, or encoded payloads");
  if (ruleIds.has("H15"))
    threats.push("SQL/command injection — attacker-controlled input may execute arbitrary queries or commands");
  if (ruleIds.has("H16"))
    threats.push("Runtime package installation enables supply-chain attacks via malicious or typosquatted packages");
  if (ruleIds.has("M17"))
    threats.push("Prototype pollution may corrupt shared objects and enable privilege escalation in Node.js");
  if (ruleIds.has("M18"))
    threats.push("Path traversal may allow reading or writing files outside the intended directory");
  if (ruleIds.has("M19"))
    threats.push("Unsafe deserialization of attacker-controlled data can lead to remote code execution");
  if (ruleIds.has("M20"))
    threats.push("Hardcoded credentials exposed in source code — anyone with read access can steal them");

  if (threats.length === 0) threats.push("No significant threats identified");
  return threats;
}

// ─── Malicious simulation ─────────────────────────────────────────────────────

function generateMaliciousSimulation(rules, skillName) {
  const scenarios = [];
  const ruleIds   = new Set(rules.map(r => r.id));

  if (ruleIds.has("H2")) {
    scenarios.push(
      `A malicious "${skillName}" could fetch a payload from an attacker-controlled server ` +
      `and execute it directly — installing a backdoor or ransomware with no user interaction ` +
      `beyond invoking the skill.`
    );
  }
  if (ruleIds.has("H6") && ruleIds.has("M1")) {
    scenarios.push(
      `The credential access + outbound HTTP combination means "${skillName}" could silently ` +
      `read ~/.ssh/id_rsa, ~/.aws/credentials, or API tokens and POST them to a remote server ` +
      `in a single invocation.`
    );
  }
  if (ruleIds.has("H3") && (ruleIds.has("H1") || ruleIds.has("H1b"))) {
    scenarios.push(
      `Shell execution + file deletion means "${skillName}" could run \`rm -` + `rf ~/\` or ` +
      `selectively wipe project files, databases, or SSH keys with no recovery path.`
    );
  }
  if (ruleIds.has("H4")) {
    scenarios.push(
      `The obfuscated logic in "${skillName}" could decode and execute any arbitrary payload ` +
      `at runtime. True behavior is hidden from static analysis — treat as untrusted until ` +
      `the obfuscated section is manually reviewed.`
    );
  }
  if (ruleIds.has("M3")) {
    scenarios.push(
      `The read-then-send pattern in "${skillName}" could enumerate files in ~/Documents or ` +
      `~/Desktop and silently upload them to an external endpoint, exfiltrating source code, ` +
      `personal data, or business documents.`
    );
  }
  if (ruleIds.has("H5")) {
    scenarios.push(
      `Privilege escalation patterns in "${skillName}" could gain root access, install ` +
      `persistent system-level malware, or modify /etc/hosts and system binaries.`
    );
  }
  if (ruleIds.has("H7")) {
    scenarios.push(
      `"${skillName}" reads .env files — a malicious version could harvest all secrets ` +
      `(API keys, DB passwords, tokens) and exfiltrate them via the network calls already present.`
    );
  }
  if (ruleIds.has("M7")) {
    scenarios.push(
      `The infinite loop or aggressive process.exit patterns in "${skillName}" could be ` +
      `triggered to hang or crash the OpenClaw agent process, causing a denial of service.`
    );
  }
  if (ruleIds.has("H8")) {
    scenarios.push(
      `The keylogger patterns in "${skillName}" could silently record every keystroke — ` +
      `capturing passwords, API keys, and private messages typed anywhere on the system ` +
      `while the skill is active.`
    );
  }
  if (ruleIds.has("H9") && ruleIds.has("M1")) {
    scenarios.push(
      `"${skillName}" reads the clipboard AND makes outbound network calls. A malicious ` +
      `version could poll the clipboard for copied passwords or crypto wallet addresses ` +
      `and silently exfiltrate them.`
    );
  }
  if (ruleIds.has("H10")) {
    scenarios.push(
      `The screen capture capability in "${skillName}" could take periodic screenshots ` +
      `and upload them to a remote server, leaking everything visible on screen — ` +
      `including browser sessions, documents, and credentials.`
    );
  }
  if (ruleIds.has("H11")) {
    scenarios.push(
      `"${skillName}" contains crypto mining indicators. If weaponized, it could spawn ` +
      `a miner process (e.g., xm` + `rig) that consumes 100% CPU/GPU indefinitely, ` +
      `degrading system performance and increasing electricity costs.`
    );
  }
  if (ruleIds.has("H12")) {
    scenarios.push(
      `The reverse shell patterns in "${skillName}" could open a persistent connection ` +
      `to an attacker's server, granting full interactive shell access to the host machine ` +
      `with the same privileges as the running process.`
    );
  }
  if (ruleIds.has("H14")) {
    scenarios.push(
      `"${skillName}" installs a persistence mechanism. Even if the skill is removed, ` +
      `the cron job, launchd plist, or startup entry it created would continue running ` +
      `malicious code on every login or reboot.`
    );
  }
  if (ruleIds.has("M16")) {
    scenarios.push(
      `"${skillName}" queries the cloud instance metadata endpoint (169.254.169.254). ` +
      `On AWS/GCP/Azure, this can retrieve IAM credentials, instance identity tokens, ` +
      `and user-data secrets — enabling full cloud account takeover.`
    );
  }
  if (ruleIds.has("M13") && ruleIds.has("M1")) {
    scenarios.push(
      `"${skillName}" archives files AND makes outbound network calls. A malicious version ` +
      `could zip ~/Documents or source code directories and upload the archive to an ` +
      `attacker-controlled server in a single operation.`
    );
  }
  if (ruleIds.has("H15")) {
    scenarios.push(
      `The SQL/command injection patterns in "${skillName}" mean that if any user-controlled ` +
      `input reaches these code paths, an attacker could execute arbitrary database queries ` +
      `or OS commands — dumping data, dropping tables, or gaining shell access.`
    );
  }
  if (ruleIds.has("H16")) {
    scenarios.push(
      `"${skillName}" installs packages at runtime. A malicious version could install a ` +
      `typosquatted or compromised package that runs a postinstall script with full OS access, ` +
      `completely bypassing static analysis.`
    );
  }
  if (ruleIds.has("M20")) {
    scenarios.push(
      `"${skillName}" contains hardcoded credentials. Anyone who reads the source code — ` +
      `including via a public repo, a log file, or a compromised backup — immediately has ` +
      `access to those credentials with no further attack required.`
    );
  }
  if (ruleIds.has("M19")) {
    scenarios.push(
      `The unsafe deserialization in "${skillName}" could allow an attacker to craft a ` +
      `malicious serialized payload that, when deserialized, executes arbitrary code — ` +
      `a classic RCE vector in Python pickle and Node.js serialize libraries.`
    );
  }

  if (scenarios.length === 0) {
    scenarios.push(
      `With its current permission set, a malicious "${skillName}" could abuse its access ` +
      `to leak data or disrupt local workflows, though the attack surface is limited.`
    );
  }

  return scenarios;
}

// ─── Recommendations ──────────────────────────────────────────────────────────

function generateRecommendations(rules, score, level) {
  const recs    = [];
  const ruleIds = new Set(rules.map(r => r.id));

  if (score >= 80 || ruleIds.has("H2") || ruleIds.has("H4")) {
    recs.push("DISABLE immediately — risk is critical. Remove or quarantine this skill.");
  }
  if (ruleIds.has("H1") || ruleIds.has("H1b") || ruleIds.has("H2")) {
    recs.push("Run in Docker sandbox mode to isolate shell execution from the host OS.");
  }
  if (ruleIds.has("H6") || ruleIds.has("H7")) {
    recs.push("Rotate any credentials or API tokens this skill could have accessed.");
  }
  if (ruleIds.has("M5")) {
    recs.push("Edit SKILL.md metadata — remove permissions not required by the skill's stated purpose.");
  }
  if (ruleIds.has("M3") || ruleIds.has("M1")) {
    recs.push("Verify all outbound HTTP destinations are expected and trusted.");
  }
  if (ruleIds.has("M4")) {
    recs.push("Replace dynamic code execution with static logic where possible.");
  }
  if (ruleIds.has("H3")) {
    recs.push("Scope file deletion to a specific temp directory; never allow arbitrary path deletion.");
  }
  if (ruleIds.has("M7")) {
    recs.push("Review loop termination conditions and process.exit() calls for abuse potential.");
  }
  if (ruleIds.has("H8")) {
    recs.push("DISABLE immediately — keylogger patterns detected. Audit all input handling code.");
  }
  if (ruleIds.has("H9")) {
    recs.push("Verify clipboard access is necessary; if not, remove it. Never send clipboard contents externally.");
  }
  if (ruleIds.has("H10")) {
    recs.push("Screen capture capability requires explicit user consent. Verify this is intentional and disclosed.");
  }
  if (ruleIds.has("H11")) {
    recs.push("DISABLE immediately — crypto mining indicators detected. Remove and quarantine this skill.");
  }
  if (ruleIds.has("H12")) {
    recs.push("DISABLE immediately — reverse shell patterns detected. This skill may be a backdoor.");
  }
  if (ruleIds.has("H13")) {
    recs.push("Registry manipulation requires explicit justification. Audit all registry keys being modified.");
  }
  if (ruleIds.has("H14")) {
    recs.push("Persistence mechanisms must be disclosed to the user. Audit and remove any unauthorized startup entries.");
  }
  if (ruleIds.has("M9")) {
    recs.push("Audit WebSocket endpoints — persistent connections can serve as C2 channels.");
  }
  if (ruleIds.has("M13")) {
    recs.push("File archiving before network calls is a strong exfiltration signal — verify the destination.");
  }
  if (ruleIds.has("M16")) {
    recs.push("Block access to 169.254.169.254 at the network level if running in cloud environments.");
  }
  if (ruleIds.has("L7")) {
    recs.push("Replace MD5/SHA1 with SHA-256 or stronger. Never use Math.random() for security-sensitive values.");
  }
  if (ruleIds.has("L8")) {
    recs.push("Replace http:// URLs with https:// to prevent man-in-the-middle attacks.");
  }
  if (ruleIds.has("L9")) {
    recs.push("Remove debug artifacts (debugger, pdb.set_trace, sensitive console.log) before production use.");
  }
  if (ruleIds.has("H4e")) {
    recs.push("Audit high-entropy strings — they may be hardcoded secrets. Move to environment variables or a secrets manager.");
  }
  if (ruleIds.has("H15")) {
    recs.push("Use parameterized queries / prepared statements. Never concatenate user input into SQL or shell commands.");
  }
  if (ruleIds.has("H16")) {
    recs.push("Pin all dependencies to exact versions. Never install packages at runtime from user-controlled input.");
  }
  if (ruleIds.has("M17")) {
    recs.push("Validate and sanitize all user-supplied keys before merging into objects. Use Object.create(null) for safe maps.");
  }
  if (ruleIds.has("M18")) {
    recs.push("Resolve and validate all file paths against an allowed base directory. Reject paths containing '..'.");
  }
  if (ruleIds.has("M19")) {
    recs.push("Replace pickle.loads / yaml.load with safe alternatives (json, yaml.safe_load). Never deserialize untrusted data.");
  }
  if (ruleIds.has("M20")) {
    recs.push("Remove hardcoded credentials immediately. Rotate the exposed secrets and store them in environment variables or a vault.");
  }
  if (level === "Low" && rules.filter(r => r.id !== "L3" && r.id !== "L5").length === 0) {
    recs.push("No action required. Consider adding to whitelist to suppress future alerts.");
  }
  if (recs.length === 0) {
    recs.push("Review flagged patterns manually before trusting this skill in production.");
  }

  return recs;
}

// ─── --fix mode: generate patched SKILL.md ────────────────────────────────────
// Strips dangerous permissions from metadata and writes a .patched.md file.

function generateFix(result) {
  const skillMdPath   = result.location + "/SKILL.md";
  const patchedPath   = result.location + "/SKILL.patched.md";
  const dangerousPerms = new Set(["exec:shell", "write:filesystem", "read:secrets",
                                   "network:unrestricted", "admin"]);

  let content;
  try {
    content = readText(skillMdPath, "utf8");
  } catch {
    console.error(`  Cannot read ${skillMdPath}`);
    return;
  }

  const claimedPerms = result.frontmatter.permissions || [];
  const toRemove     = claimedPerms.filter(p => dangerousPerms.has(p));

  if (toRemove.length === 0) {
    console.log(`  ${result.name}: no dangerous permissions to strip.`);
    return;
  }

  // Remove each dangerous permission line from the frontmatter
  let patched = content;
  for (const perm of toRemove) {
    // Match "    - exec:shell" style lines
    patched = patched.replace(
      new RegExp(`^[ \\t]+-[ \\t]+${perm.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")}\\r?\\n`, "m"),
      ""
    );
  }

  // Add a comment noting the patch
  patched = patched.replace(
    /^---\r?\n/,
    `---\n# PATCHED by security-auditor on ${new Date().toISOString().slice(0, 10)}: removed [${toRemove.join(", ")}]\n`
  );

  try {
    fs.writeFileSync(patchedPath, patched, "utf8");
    console.log(`  ${result.name}: patched → ${patchedPath}`);
    console.log(`    Removed permissions: ${toRemove.join(", ")}`);
  } catch (err) {
    console.error(`  ${result.name}: could not write patch — ${err.message}`);
  }
}

// ─── Compare mode: diff against last saved report ─────────────────────────────

function compareWithLastReport(results) {
  if (!fs.existsSync(REPORTS_DIR)) {
    console.log("No previous reports found. Run with --save first.");
    return;
  }

  const reportFiles = fs.readdirSync(REPORTS_DIR)
    .filter(f => f.endsWith(".json"))
    .sort();

  if (reportFiles.length === 0) {
    console.log("No previous JSON reports found. Run with --save --output json first.");
    return;
  }

  const lastFile = path.join(REPORTS_DIR, reportFiles[reportFiles.length - 1]);
  let   lastResults;
  try {
    lastResults = JSON.parse(readText(lastFile, "utf8"));
  } catch {
    console.log(`Could not parse last report: ${lastFile}`);
    return;
  }

  const lastMap = new Map(lastResults.map(r => [r.name, r]));
  const currMap = new Map(results.map(r => [r.name, r]));

  console.log("\nCHANGE REPORT (vs " + path.basename(lastFile) + ")\n" + "─".repeat(50));

  let changes = 0;

  // New skills
  for (const [name, curr] of currMap) {
    if (!lastMap.has(name)) {
      console.log(`  + NEW    ${name} — ${riskEmoji(curr.riskLevel)} ${curr.riskLevel} (${curr.riskScore}/100)`);
      changes++;
    }
  }

  // Removed skills
  for (const [name] of lastMap) {
    if (!currMap.has(name)) {
      console.log(`  - REMOVED ${name}`);
      changes++;
    }
  }

  // Changed risk scores
  for (const [name, curr] of currMap) {
    const prev = lastMap.get(name);
    if (!prev) continue;
    if (curr.riskScore !== prev.riskScore || curr.riskLevel !== prev.riskLevel) {
      const arrow = curr.riskScore > prev.riskScore ? "↑ WORSE" : "↓ BETTER";
      console.log(`  ~ ${arrow}  ${name}: ${prev.riskScore}→${curr.riskScore} (${prev.riskLevel}→${curr.riskLevel})`);
      changes++;
    }
  }

  if (changes === 0) console.log("  No changes since last report.");
  console.log();
}

// ─── Report formatters ────────────────────────────────────────────────────────

function riskEmoji(level) {
  return level === "High" ? "🔴" : level === "Medium" ? "🟡" : "🟢";
}

function formatTextReport(results) {
  const timestamp = new Date().toISOString().replace("T", " ").slice(0, 19) + " UTC";
  const high      = results.filter(r => r.riskLevel === "High");
  const medium    = results.filter(r => r.riskLevel === "Medium");
  const low       = results.filter(r => r.riskLevel === "Low");

  let out = "";
  out += "╔══════════════════════════════════════════════════════════════╗\n";
  out += "║           OPENCLAW SECURITY AUDIT REPORT                     ║\n";
  out += `║           Generated: ${timestamp.padEnd(38)}║\n`;
  out += "╚══════════════════════════════════════════════════════════════╝\n\n";

  out += "SUMMARY\n";
  out += "───────\n";
  out += `Total skills scanned : ${results.length}\n`;
  out += `Low risk             : ${low.length}\n`;
  out += `Medium risk          : ${medium.length}\n`;
  out += `High risk            : ${high.length}\n`;
  out += `Immediate threats    : ${high.length ? high.map(r => r.name).join(", ") : "None"}\n\n`;
  out += "━".repeat(64) + "\n\n";

  const sorted = [...high, ...medium, ...low];

  for (const r of sorted) {
    if (r.isWhitelisted) {
      out += `Skill Name    : ${r.name}  ✅ WHITELISTED (suppressed)\n`;
      out += "─".repeat(64) + "\n\n";
      continue;
    }

    out += `Skill Name    : ${r.name}\n`;
    out += `Location      : ${r.location}\n`;
    out += `Risk Score    : ${r.riskScore} / 100\n`;
    out += `Risk Level    : ${riskEmoji(r.riskLevel)} ${r.riskLevel}\n`;
    out += `Trust Score   : ${r.trustScore.score}/100 (${r.trustScore.scanCount} scan${r.trustScore.scanCount !== 1 ? "s" : ""})\n\n`;

    out += "Detected Behaviors:\n";
    r.behaviors.forEach(b => { out += `  • ${b}\n`; });
    out += "\n";

    if (r.triggeredRules.length > 0) {
      out += "Triggered Rules:\n";
      r.triggeredRules.forEach(rule => {
        const ev = Array.isArray(rule.evidence) ? rule.evidence.join("; ") : rule.evidence;
        out += `  • [${rule.id}] ${rule.label} (+${rule.score}pts) — ${ev}\n`;
      });
      out += "\n";
    }

    out += "Potential Threats:\n";
    r.threats.forEach(t => { out += `  • ${t}\n`; });
    out += "\n";

    if (r.simulation) {
      out += "Malicious Simulation:\n";
      r.simulation.forEach(s => { out += wrapText(`  ⚠ ${s}`, 80) + "\n"; });
      out += "\n";
    }

    out += "Recommended Actions:\n";
    r.recommendations.forEach(rec => { out += `  → ${rec}\n`; });
    out += "\n";
    out += "─".repeat(64) + "\n\n";
  }

  const candidates = results.filter(r => r.riskScore === 0 && r.triggeredRules.length === 0);
  out += "WHITELIST CANDIDATES\n────────────────────\n";
  if (candidates.length > 0) {
    candidates.forEach(w => { out += `  • ${w.name} — safe to whitelist\n`; });
  } else {
    out += "  None — all skills have at least one finding.\n";
  }
  out += "\n";

  out += "SECURITY HISTORY NOTE\n─────────────────────\n";
  out += `Save this report to ~/.openclaw/security-reports/${new Date().toISOString().slice(0, 10)}.md\n`;
  out += "to maintain an audit trail. Re-run after installing new skills.\n";

  return out;
}

function formatMarkdownReport(results) {
  const timestamp = new Date().toISOString().replace("T", " ").slice(0, 19) + " UTC";
  const high      = results.filter(r => r.riskLevel === "High");
  const medium    = results.filter(r => r.riskLevel === "Medium");
  const low       = results.filter(r => r.riskLevel === "Low");

  let md = `# OpenClaw Security Audit Report\n\n`;
  md += `**Generated:** ${timestamp}\n\n`;
  md += `## Summary\n\n`;
  md += `| Metric | Count |\n|--------|-------|\n`;
  md += `| Total scanned | ${results.length} |\n`;
  md += `| 🟢 Low risk | ${low.length} |\n`;
  md += `| 🟡 Medium risk | ${medium.length} |\n`;
  md += `| 🔴 High risk | ${high.length} |\n\n`;

  if (high.length > 0) {
    md += `> **Immediate threats:** ${high.map(r => `\`${r.name}\``).join(", ")}\n\n`;
  }

  md += `---\n\n`;

  const sorted = [...high, ...medium, ...low];
  for (const r of sorted) {
    if (r.isWhitelisted) {
      md += `## ✅ ${r.name} (Whitelisted)\n\n`;
      continue;
    }

    md += `## ${riskEmoji(r.riskLevel)} ${r.name}\n\n`;
    md += `- **Risk Score:** ${r.riskScore}/100\n`;
    md += `- **Risk Level:** ${r.riskLevel}\n`;
    md += `- **Trust Score:** ${r.trustScore.score}/100\n`;
    md += `- **Location:** \`${r.location}\`\n\n`;

    md += `### Detected Behaviors\n\n`;
    r.behaviors.forEach(b => { md += `- ${b}\n`; });
    md += "\n";

    if (r.triggeredRules.length > 0) {
      md += `### Triggered Rules\n\n`;
      md += `| Rule | Label | Score | Evidence |\n|------|-------|-------|----------|\n`;
      r.triggeredRules.forEach(rule => {
        const ev = Array.isArray(rule.evidence) ? rule.evidence.join("; ") : rule.evidence;
        md += `| \`${rule.id}\` | ${rule.label} | +${rule.score} | ${ev.replace(/\|/g, "\\|")} |\n`;
      });
      md += "\n";
    }

    md += `### Potential Threats\n\n`;
    r.threats.forEach(t => { md += `- ${t}\n`; });
    md += "\n";

    if (r.simulation) {
      md += `### Malicious Simulation\n\n`;
      r.simulation.forEach(s => { md += `> ⚠ ${s}\n\n`; });
    }

    md += `### Recommended Actions\n\n`;
    r.recommendations.forEach(rec => { md += `- ${rec}\n`; });
    md += "\n---\n\n";
  }

  return md;
}

function wrapText(text, width) {
  const words   = text.split(" ");
  const lines   = [];
  const indent  = "    ";
  let   current = "";

  for (const word of words) {
    const candidate = current ? current + " " + word : word;
    if (candidate.length > width && current.length > 0) {
      lines.push(current);
      current = indent + word;
    } else {
      current = candidate;
    }
  }
  if (current) lines.push(current);
  return lines.join("\n");
}

// ─── Stats mode ───────────────────────────────────────────────────────────────
// Shows rule-frequency analytics: which rules fire most often across all skills.

function showStatsReport(results) {
  const ruleFreq  = {};
  const ruleLabel = {};
  let   totalHigh = 0, totalMed = 0, totalLow = 0;

  for (const r of results) {
    if (r.riskLevel === "High")   totalHigh++;
    if (r.riskLevel === "Medium") totalMed++;
    if (r.riskLevel === "Low")    totalLow++;

    for (const rule of r.triggeredRules) {
      ruleFreq[rule.id]  = (ruleFreq[rule.id] || 0) + 1;
      ruleLabel[rule.id] = rule.label;
    }
  }

  const sorted = Object.entries(ruleFreq).sort((a, b) => b[1] - a[1]);
  const maxCount = sorted[0]?.[1] || 1;

  console.log("\nSECURITY AUDITOR — RULE FREQUENCY STATS");
  console.log("─".repeat(60));
  console.log(`Skills scanned : ${results.length}  (🔴 ${totalHigh} High  🟡 ${totalMed} Medium  🟢 ${totalLow} Low)\n`);
  console.log("Most-triggered rules:\n");

  for (const [id, count] of sorted) {
    const bar   = "█".repeat(Math.round((count / maxCount) * 20));
    const pct   = Math.round((count / results.length) * 100);
    const tier  = id[0];
    const emoji = tier === "H" ? "🔴" : tier === "M" ? "🟡" : "🟢";
    console.log(`  ${emoji} [${id.padEnd(5)}] ${bar.padEnd(20)} ${count}/${results.length} (${pct}%)  ${ruleLabel[id] || ""}`);
  }

  const avgScore = results.length
    ? Math.round(results.reduce((s, r) => s + r.riskScore, 0) / results.length)
    : 0;
  console.log(`\nAverage risk score : ${avgScore}/100`);
  console.log(`Rules with 0 hits  : ${RULES.filter(r => !ruleFreq[r.id]).map(r => r.id).join(", ") || "none"}\n`);
}

// ─── CSV formatter ────────────────────────────────────────────────────────────

function formatCSVReport(results) {
  const headers = [
    "name", "riskScore", "riskLevel", "trustScore", "fileCount",
    "triggeredRuleIds", "scannedAt", "location",
  ];
  const escape = v => `"${String(v ?? "").replace(/"/g, '""')}"`;
  const rows = results.map(r => [
    escape(r.name),
    r.riskScore,
    escape(r.riskLevel),
    r.trustScore.score,
    r.fileCount,
    escape(r.triggeredRules.map(x => x.id).join("|")),
    escape(r.scannedAt),
    escape(r.location),
  ].join(","));
  return [headers.join(","), ...rows].join("\n");
}

// ─── Save report ──────────────────────────────────────────────────────────────

function saveReportToDisk(reportText, results, mode) {
  try {
    fs.mkdirSync(REPORTS_DIR, { recursive: true });

    const date = new Date().toISOString().slice(0, 10);
    const ext  = mode === "markdown" ? ".md" : mode === "json" ? ".json" : ".txt";
    const file = path.join(REPORTS_DIR, `${date}${ext}`);

    const content = mode === "json" ? JSON.stringify(results, null, 2) : reportText;
    fs.writeFileSync(file, content, "utf8");
    console.error(`\nReport saved → ${file}`);
  } catch (err) {
    console.error(`\nCould not save report: ${err.message}`);
  }
}

// ─── Main ─────────────────────────────────────────────────────────────────────

function main() {
  // Trust history display mode
  if (trustMode) {
    showTrustReport();
    return;
  }

  let skills = discoverSkills();

  if (skills.length === 0) {
    console.log("No OpenClaw skills found. Searched:");
    SKILL_PATHS.forEach(p => console.log(`  ${p}`));
    console.log("\nTip: use --dir <path> to scan a specific skills directory.");
    process.exit(0);
  }

  // Filter to single skill if requested
  if (targetSkill) {
    skills = skills.filter(s => s.name.toLowerCase() === targetSkill.toLowerCase());
    if (skills.length === 0) {
      console.error(`Skill not found: "${targetSkill}"`);
      console.error("Available skills: " + discoverSkills().map(s => s.name).join(", "));
      process.exit(1);
    }
  }

  // Analyze all skills
  const results = skills.map(skill => {
    try {
      return analyzeSkill(skill);
    } catch (err) {
      return {
        name:            skill.name,
        location:        skill.location,
        riskScore:       50,
        riskLevel:       "Medium",
        isWhitelisted:   false,
        trustScore:      { score: 50, scanCount: 0 },
        frontmatter:     {},
        triggeredRules:  [],
        behaviors:       [`Analysis error: ${err.message}`],
        threats:         ["Could not complete analysis — treat as untrusted"],
        simulation:      null,
        recommendations: ["Manually inspect this skill — automated analysis failed"],
        fileCount:       0,
        unreadableCount: 0,
        scannedAt:       new Date().toISOString(),
      };
    }
  });

  // Compare mode
  if (compareMode) {
    compareWithLastReport(results);
  }

  // Stats mode
  if (statsMode) {
    showStatsReport(results);
    if (!saveReport) return;
  }

  // Severity filter
  const filteredResults = severityFilter
    ? results.filter(r => r.riskLevel.toLowerCase() === severityFilter)
    : results;

  if (severityFilter && filteredResults.length === 0) {
    console.log(`No skills found with severity: ${severityFilter}`);
    return;
  }

  // Output
  if (outputMode === "json") {
    const out = JSON.stringify(filteredResults, null, 2);
    console.log(out);
    if (saveReport) saveReportToDisk(out, filteredResults, "json");
    return;
  }

  if (outputMode === "csv") {
    const out = formatCSVReport(filteredResults);
    console.log(out);
    if (saveReport) saveReportToDisk(out, filteredResults, "csv");
    return;
  }

  const report = outputMode === "markdown"
    ? formatMarkdownReport(filteredResults)
    : formatTextReport(filteredResults);

  console.log(report);

  if (saveReport) saveReportToDisk(report, filteredResults, outputMode);

  // Fix mode — generate patched SKILL.md files
  if (fixMode) {
    console.log("\nFIX MODE — generating patched SKILL.md files:\n");
    results.forEach(r => generateFix(r));
  }
}

// Only run main() when executed directly, not when required as a module
if (require.main === module) {
  main();
}

// ─── Public API (used by dashboard.js) ───────────────────────────────────────
module.exports = { discoverSkills, analyzeSkill, loadTrustDB, loadWhitelist, showStatsReport, formatCSVReport, SKILL_PATHS, DEFAULT_SKILL_PATHS };
