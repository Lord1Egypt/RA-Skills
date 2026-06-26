---
name: security-auditor
description: >
  Autonomously scans all installed OpenClaw skills for security risks.
  Detects dangerous behaviors like shell execution, file deletion, remote code
  download, data exfiltration, and obfuscated logic. Assigns each skill a risk
  score (0–100), risk level (Low/Medium/High), and generates a full security
  report with mitigation recommendations.
  Use this when the user asks to audit skills, check for security risks,
  scan installed skills, or wants a security report.
user-invocable: true
runtime: node
install: false
requires:
  binaries: ["node"]
  env: ["HOME"]
permissions:
  - read:skills
  - read:filesystem
  - write:filesystem
  - exec:shell
  - network:localhost
metadata:
  openclaw:
    requires:
      env: ["HOME"]
      binaries: ["node"]
    permissions:
      - read:skills
      - read:filesystem
      - write:filesystem
      - exec:shell
      - network:localhost
---
# Security Auditor (Autonomous)

You are acting as an autonomous security engineer. Your job is to statically
analyze all installed OpenClaw skills and produce a detailed security report.

## When to activate

- User says "audit my skills", "scan skills for security issues", "check skill safety"
- User asks "are my skills safe?", "which skills are risky?"
- User wants to review a specific skill: "audit the X skill"
- A new skill was just installed and the user wants it checked
- User asks for a "security report" or "risk assessment"

## Workflow

Follow these steps in order. Do not skip steps.

### Step 1 — Discover installed skills

Scan all three skill locations in priority order:
1. `<workspace>/skills/` (workspace-local)
2. `~/.openclaw/skills/` (user-global)
3. OpenClaw bundled skills directory (read-only, lower priority)

For each location, list all subdirectories. Each subdirectory is a skill.
Record: skill name, source location, full path.

### Step 2 — Parse each skill

For every discovered skill directory, read:
- `SKILL.md` — extract frontmatter (name, description, metadata, permissions)
  and the full Markdown body (instructions, examples, tool calls)
- `scripts/` — read all files (`.js`, `.ts`, `.py`, `.sh`, `.bash`, any executable)
- Any other files present (`.json` config, `.env` templates, README, etc.)

If a file cannot be read, note it as "unreadable — treat as elevated risk."

### Step 3 — Run the analysis engine

For each skill, apply ALL rules from the rule set below.
Accumulate a risk score and collect all triggered findings.

---

## Rule Set

### HIGH RISK rules (each adds 25–40 points)

**H1 — Shell execution**
Patterns: `exec(`, `execSync(`, `spawn(`, `spawnSync(`, `child_process`,
`subprocess`, `os.system(`, `os.popen(`, `eval(`, `Function(`, `sh -c`,
`bash -c`, `cmd /c`, backtick execution in shell scripts.
Finding: "Executes shell commands — can run arbitrary OS-level code."

**H2 — Remote code download + execute**
Patterns: `curl ... | sh`, `wget ... | bash`, `fetch(` or `axios` combined
with `eval` or `exec`, dynamic `import()` from a URL, `require(url)`.
Finding: "Downloads and executes remote code — supply chain attack vector."

**H3 — Arbitrary file deletion**
Patterns: `fs.unlink`, `fs.rm(`, `rimraf`, `rm -rf`, `shutil.rmtree`,
`os.remove(`, `unlink(` outside of a clearly scoped temp directory.
Finding: "Can delete files — potential for destructive data loss."

**H4 — Obfuscated or encoded logic**
Patterns: `Buffer.from(..., 'base64')` followed by `eval`, `atob(` + `eval`,
long hex/base64 strings (>200 chars) decoded at runtime, `\\x` escape sequences
in executable strings, minified one-liners over 500 chars with no comments.
Finding: "Contains obfuscated logic — hides true behavior from static analysis."

**H5 — Privilege escalation**
Patterns: `sudo `, `su -`, `chmod 777`, `chown root`, `setuid`, `pkexec`.
Finding: "Attempts privilege escalation — can gain elevated OS permissions."

**H6 — Credential/secret harvesting**
Patterns: reads `~/.ssh/`, `~/.aws/credentials`, `~/.config/`, `~/.gnupg/`,
`/etc/passwd`, `~/.netrc`, `~/.npmrc`, `~/.pypirc`, env vars containing
`TOKEN`, `SECRET`, `PASSWORD`, `KEY`, `CREDENTIAL` sent to external URLs.
Finding: "Accesses credential stores — high risk of secret exfiltration."

**H7 — .env file access**
Patterns: `readFileSync('.env')`, `open('.env')`, `require('dotenv')`, `dotenv`.
Finding: "Reads .env files — may expose all secrets stored in the environment file."

**H8 — Keylogger / input capture**
Patterns: `keypress`, `GetAsyncKeyState`, `pynput`, `keyboard.on_press`, `process.stdin.setRawMode(true)`.
Finding: "Captures keyboard input — potential keylogger, passwords and input silently recorded."

**H9 — Clipboard access**
Patterns: `clipboard`, `xclip`, `pbpaste`, `pyperclip`, `navigator.clipboard`, `GetClipboardData`.
Finding: "Accesses system clipboard — copied passwords, tokens, or secrets may be stolen."

**H10 — Screenshot / screen capture**
Patterns: `screencapture`, `screenshot`, `PIL.ImageGrab`, `pyautogui.screenshot`, `getDisplayMedia(`.
Finding: "Captures screen content — visual data, credentials, and private content may be exfiltrated."

**H11 — Crypto mining indicators**
Patterns: `stratum+tcp://`, `xmrig`, `monero`, `cryptonight`, `hashrate`, `mining pool`.
Finding: "Crypto mining indicators — unauthorized use of host CPU/GPU resources."

**H12 — Reverse shell / backdoor**
Patterns: `nc -e /bin/sh`, `bash -i >& /dev/tcp/`, `/dev/tcp/`, `pty.spawn`, `IEX(New-Object Net.WebClient)`.
Finding: "Reverse shell patterns — may grant full remote access to the host machine."

**H13 — Windows registry manipulation**
Patterns: `winreg`, `HKEY_`, `RegSetValue`, `reg add`, `HKLM\Software\Microsoft\Windows\CurrentVersion\Run`.
Finding: "Registry manipulation — can install persistent malware or modify system behavior."

**H14 — Persistence mechanism**
Patterns: `crontab -e`, `launchctl load`, `systemctl enable`, writes to `~/.bashrc`, `~/.zshrc`, `~/.profile`, `schtasks /create`.
Finding: "Installs persistence — skill or payload survives reboots and user sessions."

---

### MEDIUM RISK rules (each adds 10–20 points)

**M1 — External network calls**
Patterns: `fetch(`, `axios`, `http.get`, `https.get`, `curl`, `wget`,
`requests.get`, `urllib` to non-localhost URLs.
Finding: "Makes external network requests — data may leave the machine."

**M2 — Sensitive directory access**
Patterns: reads from `~/Documents`, `~/Desktop`, `~/Downloads`, `~/.ssh`,
`~/.config`, `/etc/`, `/var/`, `$HOME` combined with credential file names.
Finding: "Accesses sensitive directories — may read private user data."

**M3 — Data exfiltration pattern**
Patterns: reads local files AND makes outbound HTTP/S calls in the same script,
POST requests with file content, `FormData` with file attachments sent externally.
Finding: "Read-then-send pattern detected — potential data exfiltration."

**M4 — Dynamic code construction**
Patterns: `eval(`, `new Function(`, `vm.runInNewContext(`, `vm.runInThisContext(`,
template literals used as code strings passed to exec.
Finding: "Constructs and runs code dynamically — behavior depends on runtime input."

**M5 — Excessive permission claims**
Skill declares permissions beyond what its described behavior requires.
E.g., a "weather lookup" skill that claims `write:filesystem` or `exec:shell`.
Finding: "Declared permissions exceed stated functionality — principle of least privilege violated."

**M6 — Unscoped file writes**
Patterns: `fs.writeFile(`, `fs.appendFile(` to paths outside a clearly defined
working directory, writing to `~/.openclaw/`, `~/.config/`, system directories.
Finding: "Writes files outside expected scope — may tamper with system or agent config."

**M7 — Denial-of-service patterns**
Patterns: `while(true)` with no break, `for(;;)` with no break, deeply recursive
functions without base case, `process.exit()` with unexpected codes.
Finding: "Contains patterns that could hang or crash the agent process."

**M8 — Browser storage / cookie access**
Patterns: `document.cookie`, `localStorage`, `sessionStorage`, `indexedDB`, `chrome.cookies`.
Finding: "Accesses browser cookies or local storage — session hijacking risk."

**M9 — WebSocket connection (potential C2)**
Patterns: `new WebSocket(`, `wss://`, `ws://`, `require('ws')`, `require('socket.io')`.
Finding: "Opens persistent WebSocket — may serve as a command-and-control channel."

**M10 — DNS lookup / hostname resolution**
Patterns: `dns.lookup(`, `dns.resolve(`, `socket.gethostbyname(`, `nslookup`, `dig `.
Finding: "Performs DNS lookups — may be used for DNS exfiltration or C2 beaconing."

**M11 — Process enumeration**
Patterns: `ps aux`, `tasklist`, `psutil.process_iter`, `os.listdir('/proc')`, `/proc/<pid>/cmdline`.
Finding: "Enumerates running processes — reconnaissance of the host environment."

**M12 — Network interface enumeration**
Patterns: `ifconfig`, `ipconfig`, `ip addr`, `netifaces`, `os.networkInterfaces()`.
Finding: "Enumerates network interfaces — host network reconnaissance."

**M13 — File archiving before send (staging)**
Patterns: `tar czf`, `zip -r`, `zipfile`, `tarfile`, `shutil.make_archive`, `AdmZip`, `archiver`.
Finding: "Archives files before network calls — strong exfiltration staging signal."

**M14 — Sleep / timing evasion**
Patterns: `time.sleep(` with >30s delay, `setTimeout` with >30s delay before payload.
Finding: "Long sleep delays before execution — may be evading sandbox time limits."

**M15 — Self-modification / self-deletion**
Patterns: `__file__` used in `unlink`/`remove`, `argv[0]` used in `writeFile`/`unlink`.
Finding: "Script modifies or deletes itself — anti-forensics or self-updating malware pattern."

**M16 — Cloud metadata endpoint access (IMDS)**
Patterns: `169.254.169.254`, `metadata.google.internal`, `169.254.170.2`, `metadata.azure.internal`.
Finding: "Queries cloud instance metadata — IAM credentials and secrets may be stolen."

---

### LOW RISK rules (each adds 1–8 points)

**L1 — Telemetry / logging to external service**
Patterns: sends logs, errors, or usage data to a remote endpoint.
Finding: "Sends telemetry externally — usage data may be collected."

**L2 — Third-party API dependency**
Patterns: calls to known third-party APIs (OpenAI, Stripe, Twilio, SendGrid, etc.)
Finding: "Depends on third-party API — availability and data handling outside your control."

**L3 — Reads environment variables**
Patterns: `process.env.`, `os.environ`, `$ENV_VAR` in scripts.
Finding: "Reads environment variables — may access secrets stored in env."

**L4 — No description or sparse SKILL.md**
SKILL.md body is under 50 words or missing key sections (When to use, Input, Output).
Finding: "Sparse documentation — intent and behavior are unclear."

**L5 — Hardcoded URLs or IPs**
Patterns: hardcoded `http://` or `https://` URLs, IP addresses in scripts.
Finding: "Contains hardcoded endpoints — behavior tied to specific external services."

**L6 — TODO/FIXME security notes**
Patterns: `// TODO.*security`, `// FIXME.*auth`, `HACK`, `// XXX.*password`.
Finding: "Security-related TODO/FIXME comments — known unresolved security issues in code."

**L7 — Weak cryptography**
Patterns: `md5(`, `sha1(`, `createHash('md5')`, `createHash('sha1')`, `DES`, `RC4`,
`Math.random()` used for token/key/secret generation.
Finding: "Uses weak or broken cryptographic algorithms — vulnerable to collision or brute-force."

**L8 — Insecure HTTP (non-TLS)**
Patterns: `http://` URLs to non-localhost hosts.
Finding: "Makes unencrypted HTTP connections — data in transit is not protected."

**L9 — Debug / development artifacts**
Patterns: `console.log` with password/secret/token, `print(` with credential keywords,
`debugger;`, `pdb.set_trace()`, `ipdb.set_trace()`.
Finding: "Debug artifacts left in code — may leak sensitive values to logs."

**L10 — Large file size anomaly**
Script files over 500KB are flagged — unusually large scripts may contain embedded payloads,
bundled binaries, or obfuscated data blobs.
Finding: "Unusually large script file — possible embedded payload or binary data."

---

## Scoring

Sum all triggered rule scores. Cap at 100.

| Score | Level  |
|-------|--------|
| 0–29  | Low    |
| 30–59 | Medium |
| 60+   | High   |

Bonus escalation: if H2 (remote execute) OR H4 (obfuscation) fires,
automatically set level to High regardless of total score.

---

## Step 4 — Malicious simulation

For each skill with score ≥ 30, generate a "what-if malicious" scenario.
Based on the permissions and code patterns found, describe the worst-case
abuse. Be specific. Examples:

- "If this skill were weaponized, it could read all files in ~/Documents
  and POST them to an attacker-controlled server using the existing fetch() call."
- "The shell exec pattern could be used to run `rm -rf ~/` or install a backdoor."
- "The base64 eval pattern could decode and run any payload injected at runtime."

Keep simulations grounded in what the code actually does — no speculation
beyond observed patterns.

---

## Step 5 — Recommended actions

For each skill, suggest concrete mitigations:

- **Disable**: if score ≥ 80 or H2/H4 fires — recommend immediate disable
- **Restrict**: suggest removing specific permissions from metadata
- **Sandbox**: recommend running in Docker sandbox if shell/network patterns found
- **Review**: for medium risk, ask the user to manually review flagged lines
- **Whitelist**: if skill is known-good (e.g., bundled official skill with no risky patterns),
  suggest adding to whitelist to suppress future alerts
- **Replace**: suggest a safer alternative approach if one exists

---

## Step 6 — Output the report

Format the report exactly as follows:

```
╔══════════════════════════════════════════════════════════════╗
║           OPENCLAW SECURITY AUDIT REPORT                     ║
║           Generated: <timestamp>                             ║
╚══════════════════════════════════════════════════════════════╝

SUMMARY
───────
Total skills scanned : <n>
Low risk             : <n>
Medium risk          : <n>
High risk            : <n>
Immediate threats    : <list skill names, or "None">

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[Repeat for each skill, ordered High → Medium → Low]

Skill Name    : <name>
Location      : <path>
Risk Score    : <0–100> / 100
Risk Level    : <🔴 High | 🟡 Medium | 🟢 Low>

Detected Behaviors:
  • <behavior 1>
  • <behavior 2>

Triggered Rules:
  • [H1] Shell execution — <specific pattern found>
  • [M1] External network calls — <specific pattern found>

Potential Threats:
  • <threat 1>
  • <threat 2>

Malicious Simulation:
  ⚠ <worst-case scenario description>

Recommended Actions:
  → <action 1>
  → <action 2>

───────────────────────────────────────────────────────────────
```

After the per-skill sections, append:

```
WHITELIST CANDIDATES
────────────────────
Skills with score 0 and no triggered rules:
  • <skill name> — safe to whitelist

SECURITY HISTORY NOTE
─────────────────────
Save this report to ~/.openclaw/security-reports/<YYYY-MM-DD>.md
to maintain an audit trail. Re-run after installing new skills.
```

---

## Auditing a single skill

If the user asks to audit one specific skill by name:
- Run Steps 2–5 for that skill only
- Output the single-skill section of the report format
- Still show the malicious simulation if score ≥ 30

---

## Continuous monitoring guidance

Tell the user:
"Run `node scripts/monitor.js` as a background process to watch
~/.openclaw/skills/ for changes and re-audit automatically.
Use `node scripts/monitor.js --alert-only` to only print on High risk findings."

## CLI usage (for reference)

When the user asks how to run the auditor directly:
```
node scripts/audit.js --dir <skills-path>          # scan a directory
node scripts/audit.js --skill <name>               # single skill
node scripts/audit.js --output json                # JSON output
node scripts/audit.js --output markdown            # Markdown report
node scripts/audit.js --save                       # save to history
node scripts/audit.js --compare                    # diff vs last report
node scripts/audit.js --fix                        # patch dangerous permissions
node scripts/audit.js --trust                      # show trust score history
node scripts/test.js                               # run test suite
```

---

## Important constraints

- NEVER execute any skill code. Analysis is static only.
- NEVER modify or delete any skill files during analysis.
- If you cannot read a file, flag it as unreadable and assign +15 risk points.
- Do not produce false positives for comments — only flag executable code patterns.
- If a pattern appears only in a comment or string literal that is never executed,
  note it as "pattern in comment — lower confidence" and reduce score contribution by 50%.
- Be precise: quote the actual line or pattern that triggered each rule.
