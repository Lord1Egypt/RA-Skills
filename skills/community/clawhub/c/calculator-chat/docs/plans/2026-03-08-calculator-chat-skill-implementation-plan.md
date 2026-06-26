# Calculator Chat Skill Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Create a cross-platform opencode skill that responds to user messages by typing numbers into the system calculator.

**Architecture:** 
- Node.js CLI tool with platform-specific implementations (PowerShell for Windows, AppleScript for macOS, xdotool for Linux)
- Loaded as custom skill in opencode via skill tool
- Can be published to clawhub

**Tech Stack:** Node.js, PowerShell, AppleScript, xdotool

---

### Task 1: Initialize Project Structure

**Files:**
- Create: `calculator-chat/package.json`
- Create: `calculator-chat/SKILL.md`
- Create: `calculator-chat/mapping.json`

**Step 1: Create package.json**

```json
{
  "name": "calculator-chat",
  "version": "1.0.0",
  "description": "Opencode skill for calculator-based communication",
  "main": "src/index.js",
  "bin": {
    "calc-chat": "./src/index.js"
  },
  "scripts": {
    "start": "node src/index.js"
  },
  "keywords": ["opencode", "skill", "calculator"],
  "license": "MIT"
}
```

**Step 2: Create mapping.json**

```json
{
  "我很喜欢你": "520",
  "I love you": "143",
  "想你": "537",
  "嫁给我": "1314520",
  "好饿啊": "123",
  "晚安": "886",
  "hello": "741",
  "谢谢": "88"
}
```

**Step 3: Commit**

```bash
git add package.json mapping.json
git commit -m "chore: initial project structure"
```

---

### Task 2: Create Main Entry Point

**Files:**
- Create: `calculator-chat/src/index.js`

**Step 1: Write the main entry point**

```javascript
#!/usr/bin/env node

const os = require('os');
const path = require('path');
const { execSync } = require('child_process');
const mapping = require('../mapping.json');

function getPlatform() {
  const platform = os.platform();
  if (platform === 'win32') return 'windows';
  if (platform === 'darwin') return 'macos';
  return 'linux';
}

function textToNumber(text) {
  const lower = text.toLowerCase();
  if (mapping[lower] || mapping[text]) {
    return mapping[lower] || mapping[text];
  }
  let sum = 0;
  for (let i = 0; i < text.length; i++) {
    sum += text.charCodeAt(i);
  }
  return sum.toString();
}

async function run(message) {
  const platform = getPlatform();
  const numberCode = textToNumber(message);
  
  const platformModule = require(`./platform/${platform}.js`);
  await platformModule.launchCalculator();
  await platformModule.typeNumber(numberCode);
}

const message = process.argv.slice(2).join(' ');
if (message) {
  run(message).catch(console.error);
} else {
  console.log('Usage: calc-chat <message>');
}
```

**Step 2: Commit**

```bash
git add src/index.js
git commit -m "feat: add main entry point"
```

---

### Task 3: Implement Windows Platform Module

**Files:**
- Create: `calculator-chat/src/platform/windows.js`

**Step 1: Write Windows implementation**

```javascript
const { execSync } = require('child_process');

async function launchCalculator() {
  execSync('start calc.exe', { shell: 'cmd.exe' });
  await sleep(1000);
}

async function typeNumber(number) {
  const psScript = `
    Add-Type @"
    using System;
    using System.Runtime.InteropServices;
    public class Win32 {
        [DllImport("user32.dll")]
        public static extern IntPtr FindWindow(string lpClassName, string lpWindowName);
        [DllImport("user32.dll")]
        public static extern IntPtr FindWindowEx(IntPtr hwndParent, IntPtr hwndChildAfter, string lpszClass, string lpszWindow);
        [DllImport("user32.dll")]
        public static extern int PostMessage(IntPtr hWnd, int Msg, int wParam, int lParam);
    }
"@
    $calc = Start-Process calc.exe -PassThru
    Start-Sleep -Milliseconds 500
    $hwnd = $calc.MainWindowHandle
    if ($hwnd -eq [IntPtr]::Zero) {
        Start-Sleep -Milliseconds 1000
        $hwnd = $calc.MainWindowHandle
    }
    $chars = '${number}'.ToCharArray()
    foreach ($c in $chars) {
        [Win32]::PostMessage($hwnd, 0x0100, [int][char]$c, 0) | Out-Null
        Start-Sleep -Milliseconds 50
    }
  `;
  execSync(`powershell -Command "${psScript.replace(/"/g, '\\"')}"`, { stdio: 'ignore' });
}

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

module.exports = { launchCalculator, typeNumber };
```

**Step 2: Commit**

```bash
git add src/platform/windows.js
git commit -m "feat: add Windows platform implementation"
```

---

### Task 4: Implement macOS Platform Module

**Files:**
- Create: `calculator-chat/src/platform/macos.js`

**Step 1: Write macOS implementation**

```javascript
const { execSync } = require('child_process');

async function launchCalculator() {
  execSync('open -a Calculator');
  await sleep(500);
}

async function typeNumber(number) {
  const chars = number.split('').join(' ');
  const script = `
    tell application "Calculator"
      activate
    end tell
    delay 0.3
    tell application "System Events"
      keystroke "${chars}"
    end tell
  `;
  execSync(`osascript -e '${script}'`, { stdio: 'ignore' });
}

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

module.exports = { launchCalculator, typeNumber };
```

**Step 2: Commit**

```bash
git add src/platform/macos.js
git commit -m "feat: add macOS platform implementation"
```

---

### Task 5: Implement Linux Platform Module

**Files:**
- Create: `calculator-chat/src/platform/linux.js`

**Step 1: Write Linux implementation**

```javascript
const { execSync } = require('child_process');

async function launchCalculator() {
  execSync('gnome-calculator &', { stdio: 'ignore' });
  await sleep(1000);
}

async function typeNumber(number) {
  try {
    const windowId = execSync('xdotool search --name Calculator | head -1', { encoding: 'utf8' }).trim();
    if (windowId) {
      execSync(`xdotool windowactivate ${windowId} key ${number.split('').join(' ')}`, { stdio: 'ignore' });
    }
  } catch (e) {
    console.error('Failed to type to calculator:', e.message);
  }
}

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

module.exports = { launchCalculator, typeNumber };
```

**Step 2: Commit**

```bash
git add src/platform/linux.js
git commit -m "feat: add Linux platform implementation"
```

---

### Task 6: Create SKILL.md for Opencode

**Files:**
- Create: `calculator-chat/SKILL.md`

**Step 1: Write SKILL.md**

```markdown
---
name: calculator-chat
description: Use when user sends /calc <message> command to communicate via system calculator
---

# Calculator Chat Skill

## Overview

This skill allows AI to respond to users by typing numbers/symbols into the system calculator instead of text.

## Trigger

When user sends a message starting with `/calc `:
```
/calc 我很喜欢你
/calc I love you
```

## Response Flow

1. Extract message after `/calc ` prefix
2. Look up text-to-number mapping in mapping.json
3. If no mapping found, calculate Unicode sum
4. Launch system calculator (platform-specific)
5. Type the number code into calculator

## Text-to-Number Mappings

| Message | Code |
|---------|------|
| 我很喜欢你 | 520 |
| I love you | 143 |
| 想你 | 537 |
| 嫁给我 | 1314520 |

## Platform Commands

| Platform | Launch | Type Keys |
|----------|--------|-----------|
| Windows | `start calc.exe` | PowerShell PostMessage |
| macOS | `open -a Calculator` | AppleScript keystroke |
| Linux | `gnome-calculator &` | xdotool |

## Usage in opencode

```bash
# Install skill
npm install -g .

# Run
calc-chat "我很喜欢你"
```

## Fallback Behavior

If no predefined mapping exists:
- Calculate sum of all character Unicode codes
- Example: "Hi" → 72 + 105 = "177"
```

**Step 2: Commit**

```bash
git add SKILL.md
git commit -m "docs: add SKILL.md for opencode"
```

---

### Task 7: Test the Skill

**Step 1: Test on current platform**

```bash
cd calculator-chat
npm install
node src/index.js "我很喜欢你"
```

Expected: Calculator opens and displays 520

**Step 2: Commit**

```bash
git commit -m "test: verify skill works"
```

---

### Task 8: Make Executable and Publish Prep

**Step 1: Make index.js executable (for Unix)**

Add to package.json:
```json
"bin": {
  "calc-chat": "./src/index.js"
}
```

**Step 2: Add shebang to index.js**

```javascript
#!/usr/bin/env node
// (at top of file)
```

**Step 3: Final commit**

```bash
git add .
git commit -m "feat: make CLI executable"
```

---

**Plan complete.** Two execution options:

1. **Subagent-Driven (this session)** - I dispatch fresh subagent per task, review between tasks, fast iteration

2. **Parallel Session (separate)** - Open new session with executing-plans, batch execution with checkpoints

Which approach?
