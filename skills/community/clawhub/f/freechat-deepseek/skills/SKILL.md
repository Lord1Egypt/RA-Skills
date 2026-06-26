---
name: freechat-deepseek
alias:
  - chat-deepseek
  - deepseek-it
  - ask-deepseek
  - open-deepseek
  - browse-deepseek
  - deepseek-search
  - deepseeking

description: openclaw browser open https://chat.deepseek.com and login it, then input questions from user's messages, extract response of deepseek chat to reply user.
allowed-tools: Bash(npm:*) Bash(npx:*) Bash(openclaw:*) Bash(curl:*) Read Write WebFetch Browser
---

# DeepSeek Chat Automation Skill

> **⚠️ Important for OpenClaw >= v3.13:** Use direct Chrome attachment (`profile: "user"`) instead of the relay extension. See "Direct Chrome Attachment" section below.
> 
> **Version Check:** Before executing any browser actions, check OpenClaw version (`openclaw --version`). If >= v3.13, use `profile: "user"` for direct Chrome attachment. This avoids the need for the Chrome relay extension and provides more stable browser automation.

## Dynamic Profile Selection (Recommended)

To make your code work with both old and new OpenClaw versions, use this dynamic profile selection:

```javascript
// Determine which profile to use based on OpenClaw version
async function getBrowserProfile() {
  try {
    // Check OpenClaw version
    const versionResult = await exec({ command: "openclaw --version" });
    const versionMatch = versionResult.match(/(\d+)\.(\d+)\.(\d+)/);
    
    if (versionMatch) {
      const major = parseInt(versionMatch[1]);
      const minor = parseInt(versionMatch[2]);
      const patch = parseInt(versionMatch[3]);
      
      // v3.13+ uses "user" profile for direct Chrome
      if (major > 3 || (major === 3 && minor > 13) || (major === 3 && minor === 13 && patch >= 0)) {
        console.log("✅ Using direct Chrome (profile: 'user') for OpenClaw >= v3.13");
        return "user";
      }
    }
    
    console.log("ℹ️ Using legacy profile 'openclaw' for older OpenClaw versions");
    return "openclaw";
  } catch (error) {
    console.warn("⚠️ Could not determine version, defaulting to 'user'");
    return "user"; // Default to user profile
  }
}

// Usage in your code:
const profile = await getBrowserProfile();

// Then use it in browser calls:
const result = await browser({
  action: "open",
  profile: profile,
  url: "https://chat.deepseek.com/"
});
```

## Quick Start (OpenClaw >= v3.13)

```javascript
// 1. Check version - if >= v3.13, use "user" profile
// 2. Open Chrome directly (no extension needed)
const result = await browser({
  action: "open",
  profile: "user",  // Use "user" for v3.13+
  url: "about:blank"
});

// 3. Navigate to DeepSeek
await browser({
  action: "navigate",
  profile: "user",
  targetId: result.targetId,
  url: "https://chat.deepseek.com/"
});

// 4. Continue with the workflow below...
```

## Direct Chrome Attachment (OpenClaw >= v3.13)

For OpenClaw version >= v3.13, use direct Chrome attachment:

### Step 1: Check Browser Status

```javascript
// Check user browser status
const browserStatus = await browser({
  action: "status",
  profile: "user"
});
console.log("Browser status:", browserStatus);
```

### Step 2: Open Chrome Directly

```javascript
// Open Chrome directly (no extension needed)
const result = await browser({
  action: "open",
  profile: "user",
  url: "about:blank"
});
const tabId = result.targetId;
console.log("Opened tab:", tabId);
```

### Step 3: Navigate to DeepSeek

```javascript
// Navigate to DeepSeek
await browser({
  action: "navigate",
  profile: "user",
  targetId: tabId,
  url: "https://chat.deepseek.com/"
});
```

### Step 4: List/Manage Tabs

```javascript
// List all open tabs
const tabs = await browser({
  action: "tabs",
  profile: "user"
});
console.log("Open tabs:", tabs);

// Switch to specific tab
await browser({
  action: "focus",
  profile: "user",
  targetId: "1"  // Tab ID from tabs list
});
```

### Key Differences: user vs openclaw profile

| Feature | `profile: "user"` | `profile: "openclaw"` (legacy) |
|---------|-------------------|-------------------------------|
| Chrome extension needed | ❌ No | ✅ Yes |
| Uses | Local Chrome installation | Openclaw-managed browser |
| Reliability | ✅ More stable | May have issues |
| Login state | Uses your logged-in Chrome | Fresh browser session |

### Troubleshooting

If `profile: "user"` times out:
1. Restart the OpenClaw gateway: `openclaw gateway restart`
2. Try again with browser action

---

## Prerequisites for Direct Chrome Attachment

To use `profile: "user"` for direct Chrome attachment, users must configure Chrome properly:

### 1. Chrome Version Requirement
- Install **Chrome version >= 144**

### 2. Enable Remote Debugging

**Step-by-step:**

1. **Open Chrome settings page:**
   ```
   chrome://inspect/#remote-debugging
   ```

2. **Enable the option:**
   - Check/Enable: **"Allow remote debugging for this browser instance"**
   
   ![Chrome remote debugging settings](chrome-remote-debugging.png)

3. **Restart Chrome** if the option was just enabled

### 3. Verify Setup

Run this to verify Chrome is ready:
```javascript
// Check user browser status
const browserStatus = await browser({
  action: "status",
  profile: "user"
});

if (browserStatus.running === true) {
  console.log("✅ Chrome is ready for direct attachment!");
} else {
  console.log("❌ Chrome not ready. Check chrome://inspect settings.");
}
```

### Common Issues

| Issue | Solution |
|-------|----------|
| Timeout errors | Ensure "Allow remote debugging" is enabled in chrome://inspect |
| Chrome not detected | Make sure Chrome version >= 144 is installed |
| Connection refused | Restart Chrome and try again |
| Already in use | Close other Chrome instances or use a different Chrome profile |

---

## Option 2: Using Chrome Relay Extension (Legacy)

For users who prefer using the Chrome relay extension instead of direct Chrome attachment:

### Install the Extension

1. **Open Chrome Web Store:**
   ```
   https://chromewebstore.google.com/detail/openclaw-browser-relay/nglingapjinhecnfejdcpihlpneeadjp
   ```

2. **Click "Add to Chrome"** to install the extension

3. **Approve permissions** when prompted

### Using the Relay

Once installed, activate it before running browser automation:

1. **Open the Chrome tab** you want to control
2. **Click the OpenClaw Browser Relay toolbar icon** (usually in the top-right of Chrome)
3. Wait for the badge to turn **ON** / green

Then use `profile: "chrome-relay"` in your browser calls:

```javascript
// Check relay status
const relayStatus = await browser({
  action: "status",
  profile: "chrome-relay"
});

// Open tab via relay
const result = await browser({
  action: "open",
  profile: "chrome-relay",
  url: "https://chat.deepseek.com/"
});

// Take snapshot
await browser({
  action: "snapshot",
  profile: "chrome-relay",
  targetId: result.targetId
});
```

### Relay Status Indicators

| Status | Meaning |
|--------|---------|
| `running: false` | Relay not activated - click the toolbar icon |
| `cdpReady: false` | CDP not connected - click the toolbar icon |
| `running: true` | Ready to use! |

### Which Should I Use?

| Feature | Direct Chrome (`user`) | Relay Extension (`chrome-relay`) |
|---------|------------------------|----------------------------------|
| Setup required | Chrome >= 144 + remote debugging | Install extension |
| No. of steps | More initial setup | Easier install |
| Stability | ✅ More stable | May have occasional issues |
| Login state | Uses your Chrome profile | Uses extension's session |
| Recommended for | Power users | Beginners |

---

## Workflow Overview (6 Steps)

Automate login with scanning qr code snapshot, input questions from user messages, and extract responses from DeepSeek chat, then reply to user.

**Key Feature:** Pure browser automation + DOM extraction. **No LLM requests or processing** - just raw text from the rendered page.

## When to Use

✅ **USE this skill when:**
- User wants to ask or query on `DeepSeek Chat` (https://chat.deepseek.com)
- Sending user questions from messages to `DeepSeek Chat`
- Extracting AI responses as raw text (no LLM processing)
- Browser automation workflows
- Extract answers from `DeepSeek Chat` Page with direct output

❌ **DON'T use this skill when:**
- Need real-time SSE stream capture (use curl/WebSocket directly)
- Page uses heavy anti-bot protection
- Requires complex CAPTCHA solving
- Need LLM-powered text processing (use Claude API directly)

## Requirements (Updated for OpenClaw >= v3.13)

For OpenClaw >= v3.13:
- Browser tool with `profile: "user"` (direct Chrome attachment)
- No Chrome extension needed!
- **No API keys or LLM credits needed**

For older versions (legacy):
- Check browser extension with `openclaw browser status`, get `enabled: true`
- Browser tool with `profile: "openclaw"`

## Workflow Overview (6 Steps)

```
┌─────────────────────────────────────────────────────────────────┐
│  1. Open chat.deepseek.com OR check existing tab                │
└─────────────────────────────────┬───────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────┐
│  2. Check login status - QR Code needed?                        │
│     - If login form → Take snapshot of login page               │
│     - If chat interface → Already logged in, proceed to Step 3   │
└─────────────────────────────────┬───────────────────────────────┘
                                  │
                                  ▼
┌──────────────────────────────────────────────────────────────────────────────────┐
│  3. Send QR Code to enabled channels (iMessage/WhatsApp/QQBot/Feishu/WeCom/Slack │
│     - Send snapshot to user via imsg                                             │
│     - If WhatsApp is active, send via WhatsApp                                   │
│     - If QQBot is active, send via QQBot, Feishu, WeCom, Slack, etc              │
└─────────────────────────────────┬────────────────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────┐
│  4. Wait for login (with timeout & retry loop)                 │
│     - Poll every 5 seconds for login success                   │
│     - If timeout: refresh page, re-snapshot QR, retry send      │
│     - Repeat until logged in successfully                        │
└─────────────────────────────────┬───────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────┐
│  5. Input question and press Enter                              │
└─────────────────────────────────┬───────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  6. Extract response from DOM and reply to user                   │
└─────────────────────────────────────────────────────────────────────────┘
```

## 🎯 SIMPLE & RELIABLE RESPONSE EXTRACTION

**IMPORTANT FOR AGENTS:** Always use this simple extraction function instead of writing complex code. It's tested and reliable.

```javascript
// SIMPLE & RELIABLE DeepSeek response extraction
// Use this function instead of writing your own extraction code
async function getDeepSeekResponseSimple(tabId) {
  try {
    const response = await browser({
      action: "act",
      kind: "evaluate",
      profile: "openclaw",
      targetId: tabId,
      fn: `(function() {
        // Get all text from the page body
        const allText = document.body.innerText || document.body.textContent || '';
        
        // Split into lines
        const lines = allText.split('\n');
        
        // Filter out system messages and find the response
        const responseLines = [];
        let foundResponse = false;
        
        for (let i = lines.length - 1; i >= 0; i--) {
          const line = lines[i].trim();
          
          // Skip empty lines and system messages
          if (line.length < 20) continue;
          if (line.includes('AI-generated')) continue;
          if (line.includes('Message DeepSeek')) continue;
          if (line.includes('How can I help')) continue;
          if (line.includes('Upload docs')) continue;
          if (line.includes('⌘')) continue;
          
          // This is likely the response
          responseLines.unshift(line);
          foundResponse = true;
        }
        
        // Combine response lines
        if (foundResponse && responseLines.length > 0) {
          return responseLines.join('\n\n').trim();
        }
        
        return 'No response found';
      })()`,
      returnByValue: true
    });
    
    return response;
  } catch (error) {
    console.error("Error extracting response:", error);
    return `Error: ${error.message}`;
  }
}

// Usage example:
// 1. Ask your question
// 2. Wait 10-15 seconds for response
// 3. Call: const answer = await getDeepSeekResponseSimple(tabId);
// 4. Use the answer
```

---

## Step 1: Open or Reuse Tab

```javascript
// Try to find existing DeepSeek tab first
const existingTabs = await sessions_list({ /* filter for chat.deepseek.com */ });

if (existingTabs.length > 0) {
  console.log("✅ Reusing existing DeepSeek tab:", existingTabs[0]);
  tabId = existingTabs[0];
} else {
  // Open new tab
  const result = await browser({
    action: "open",
    profile: "openclaw",
    targetUrl: "https://chat.deepseek.com/"
  });
  tabId = result.targetId;
  console.log("✅ Opened new DeepSeek tab:", tabId);
}

// Wait for page to load
await new Promise(r => setTimeout(r, 3000));
```

---

## Step 2: Check Login Status (QR Code Needed?)

```javascript
// Check if login required (QR Code scan) or already logged in
await browser({
  action: "snapshot",
  profile: "openclaw",
  targetId: tabId
});

// Evaluate login status
const loginStatus = await browser({
  action: "act",
  kind: "evaluate",
  profile: "openclaw",
  targetId: tabId,
  fn: `{
    const loginForm = document.querySelector('input[type="tel"], input[placeholder*="Phone"]');
    const qrCode = document.querySelector('iframe[src*="wechat"], img[alt*="WeChat"], img[src*="wechat"]');
    const chatInput = document.querySelector('textarea[placeholder*="Message DeepSeek"]');
    const userAvatar = document.querySelector('[class*="avatar"], [class*="user"]');
    
    JSON.stringify({ 
      needLogin: !!(loginForm || qrCode),
      hasChatInput: !!chatInput,
      hasUser: !!userAvatar,
      hasLoginForm: !!loginForm,
      hasQrCode: !!qrCode
    });
  }`,
  returnByValue: true
});

const status = JSON.parse(loginStatus);

if (!status.needLogin && status.hasChatInput) {
  console.log("✅ Already logged in!");
  // Proceed to Step 5 (input question)
} else {
  console.log("⚠️ QR Code login required!");
  // Proceed to Step 3 (send QR code)
}
```

### Login Status Indicators

|       Status         |               Check              |          Action Required     |
|----------------------|----------------------------------|------------------------------|
| ✅ Already Logged In | Chat input visible + user avatar | Proceed to Step 5            |
| ❌ Need Login        | QR Code or login form visible    | Proceed to Step 3            |

---

## Step 3: Send QR Code to Enabled Channels

```javascript
// Navigate to login page explicitly
await browser({
  action: "navigate",
  profile: "openclaw",
  targetId: tabId,
  targetUrl: "https://chat.deepseek.com/sign_in"
});

await new Promise(r => setTimeout(r, 2000));

// Take screenshot of QR Code login page
const screenshotResult = await browser({
  action: "screenshot",
  profile: "openclaw",
  targetId: tabId
});

// Get the screenshot path from the browser tool response
const screenshotPath = screenshotResult.path;

// Get user phone number (configure this in your implementation)
const userPhone = process.env.DEEPSEEK_PHONE || "+1234567890000"; // Configure this

// Try to send via enabled and running channels such as iMessage (most reliable on Mac)
try {
  await exec({
    command: 'imsg send --to "' + userPhone + '" --text "Please scan this QR code with WeChat to login to DeepSeek:" --file "' + screenshotPath + '"'
  });
  console.log("✅ QR Code sent via iMessage");
} catch (e) {
  console.log("⚠️ iMessage failed:", e.message);
}

// Try to send via WhatsApp if available
try {
  await exec({
    command: 'openclaw message send --channel whatsapp --target "' + userPhone + '" -m "Please scan QR code with WeChat to login" --media "' + screenshotPath + '"'
  });
  console.log("✅ QR Code sent via WhatsApp");
} catch (e) {
  console.log("⚠️ WhatsApp not available:", e.message);
}

// Try to send via QQBot (use media tags)
try {
  await exec({
    command: 'openclaw message send --channel qqbot -m "Please scan this QR code with WeChat to login to DeepSeek:\\n<qqimg>' + screenshotPath + '</qqimg>"'
  });
  console.log("✅ QR Code sent via QQBot");
} catch (e) {
  console.log("⚠️ QQBot not available:", e.message);
}
```

### QR Code Sending Priority
Send QR Code to session which is executing this skill firstly. And also send by other avlabile channels:
1. **iMessage** (`imsg`) - Most reliable on Mac (uses `userPhone` variable)
2. **WhatsApp** - If WhatsApp Web is active (uses `userPhone` variable)
3. **QQBot** - If QQ bot is configured (no phone number needed for QQBot)
4. **Signal** - If Signal CLI is available (would need phone number configuration)

---

## Step 4: Wait for Login (with Timeout & Retry Loop)

```javascript
// Poll for login success
let attempts = 0;
const maxAttempts = 24; // 24 * 5 seconds = 2 minutes max
const retryInterval = 5000;

async function checkLoginSuccess() {
  const result = await browser({
    action: "act",
    kind: "evaluate",
    profile: "openclaw",
    targetId: tabId,
    fn: `{
      const chatInput = document.querySelector('textarea[placeholder*="Message DeepSeek"]');
      const userAvatar = document.querySelector('[class*="avatar"], [class*="user"]');
      { hasChatInput: !!chatInput, hasUser: !!userAvatar };
    }`,
    returnByValue: true
  });
  return JSON.parse(result);
}

while (attempts < maxAttempts) {
  await new Promise(r => setTimeout(r, retryInterval));
  
  const loginResult = await checkLoginSuccess();
  
  if (loginResult.hasChatInput && loginResult.hasUser) {
    console.log("✅ Login successful!");
    break;
  }
  
  attempts++;
  console.log("⏳ Waiting for login... (" + attempts + "/" + maxAttempts + ")");
  
  // If timeout (after 12 attempts = 1 minute), refresh and retry
  if (attempts === 12) {
    console.log("⏰ Timeout, refreshing QR code...");
    
    await browser({
      action: "navigate",
      profile: "openclaw",
      targetId: tabId,
      targetUrl: "https://chat.deepseek.com/sign_in"
    });
    
    await new Promise(r => setTimeout(r, 3000));
    
    // Re-take screenshot and send again
    await browser({
      action: "screenshot",
      profile: "openclaw",
      targetId: tabId
    });
    
    // Re-take screenshot and send again
    const newScreenshotResult = await browser({
      action: "screenshot",
      profile: "openclaw",
      targetId: tabId
    });
    const newScreenshotPath = newScreenshotResult.path;
    
    // Re-send QR code
    try {
      await exec({
        command: 'imsg send --to "' + userPhone + '" --text "QR code refreshed - please scan again with WeChat" --file "' + newScreenshotPath + '"'
      });
    } catch (e) {}
  }
}

if (attempts >= maxAttempts) {
  throw new Error("Login timeout - user did not complete QR scan in time");
}
```

### Login Timeout Strategy

| Attempt | Time    | Action                          |
|---------|---------|---------------------------------|
| 1-12    | 0-60s   | Poll every 5s, wait for scan    |
| 12      | 60s     | Refresh page, re-send QR code   |
| 13-24   | 65-120s | Continue polling                |
| 24      | 120s    | Fail with timeout error         |

---

## Step 5: Input Question and Press Enter

```javascript
// Ensure we're on chat page
await browser({
  action: "navigate",
  profile: "openclaw",
  targetId: tabId,
  targetUrl: "https://chat.deepseek.com/"
});

await new Promise(r => setTimeout(r, 2000));

// Take snapshot to get fresh refs
await browser({
  action: "snapshot",
  profile: "openclaw",
  targetId: tabId
});

// Type message into input box (use textbox ref from snapshot)
await browser({
  action: "act",
  kind: "type",
  profile: "openclaw",
  targetId: tabId,
  ref: "e102", // Get from snapshot - textarea ref
  text: "Your question here"
});

console.log("✅ Text typed into input box");

// Press Enter to submit
await browser({
  action: "act",
  kind: "press",
  profile: "openclaw",
  targetId: tabId,
  key: "Enter"
});

console.log("✅ Enter key pressed");
```

---

## Step 6: Extract Response from DOM

NEVER send raw html content with `<tool_call>` to user session.

```javascript
// Wait for response to generate (8-15 seconds depending on complexity)
await new Promise(r => setTimeout(r, 10000));

// Extract assistant response from page body
const response = await browser({
  action: "act",
  kind: "evaluate",
  profile: "openclaw",
  targetId: tabId,
  fn: `{
    // Get all paragraph elements from the entire page body
    const body = document.body;
    const paras = Array.from(body.querySelectorAll('p'));
    
    // Filter to find assistant messages (not user messages, not system text)
    const assistantMsgs = paras.filter(p => {
      const text = p.innerText || '';
      const parent = p.parentElement;
      
      // Exclude system messages and user messages
      return text.length > 15 && 
             !text.includes('AI-generated') &&
             !text.includes('Upload docs') &&
             !text.includes('How can I help') &&
             !text.includes('⌘') &&
             parent && !parent.closest('header') &&
             parent && !parent.closest('footer');
    });
    
    // Get the most recent assistant message
    const lastResponse = assistantMsgs.length > 0 
      ? assistantMsgs[assistantMsgs.length - 1].innerText 
      : 'No response found';
    
    // Clean up the response
    return lastResponse.trim();
  }`,
  returnByValue: true
});

console.log("✅ DeepSeek Response:", response);
```

### Response Extraction Strategy

|      Element |     Strategy    |
|--------------|-----------------|
| Container    | `document.body` |
| Message type | `<p>` tags      |
| Filter out   | AI-generated, Upload docs, Help text, Keyboard shortcuts |
| Get          | Last matching `<p>` from body |

---

## Complete Example: Full Workflow

```javascript
// ============ DEEPSEEK CHAT AUTOMATION ============

const profile = "openclaw";
// Get user phone number from USER.md or configuration
// Example: Read from USER.md or use environment variable
const userPhone = process.env.DEEPSEEK_PHONE || "+1234567890000"; // Default fallback - configure this

// Step 1: Open or reuse tab
const openResult = await browser({
  action: "open",
  profile: profile,
  targetUrl: "https://chat.deepseek.com/"
});
const tabId = openResult.targetId;

await new Promise(r => setTimeout(r, 3000));

// Step 2: Check login status
await browser({ action: "snapshot", profile, targetId: tabId });
const loginCheck = await browser({
  action: "act",
  kind: "evaluate",
  profile,
  targetId: tabId,
  fn: `{
    const chatInput = document.querySelector('textarea[placeholder*="Message DeepSeek"]');
    const qrCode = document.querySelector('img[src*="wechat"]');
    { needLogin: !chatInput, hasQrCode: !!qrCode };
  }`,
  returnByValue: true
});

const status = JSON.parse(loginCheck);

if (!status.needLogin) {
  console.log("Already logged in!");
} else {
  // Step 3: Send QR code
  await browser({ action: "navigate", profile, targetId: tabId, targetUrl: "https://chat.deepseek.com/sign_in" });
  await new Promise(r => setTimeout(r, 2000));
  const screenshotResult = await browser({ action: "screenshot", profile, targetId: tabId });
  
  const screenshotPath = screenshotResult.path;
  
  // Send via iMessage
  await exec({
    command: 'imsg send --to "' + userPhone + '" --text "Please scan QR code to login to DeepSeek" --file "' + screenshotPath + '"'
  });
  
  // Step 4: Wait for login with retry
  let attempts = 0;
  while (attempts < 24) {
    await new Promise(r => setTimeout(r, 5000));
    const result = await browser({
      action: "act",
      kind: "evaluate",
      profile,
      targetId: tabId,
      fn: `{
        const chatInput = document.querySelector('textarea[placeholder*="Message DeepSeek"]');
        !!chatInput;
      }`,
      returnByValue: true
    });
    
    if (result === 'true') {
      console.log("Login successful!");
      break;
    }
    
    attempts++;
    
    // Refresh QR every 60 seconds
    if (attempts === 12) {
      await browser({ action: "navigate", profile, targetId: tabId, targetUrl: "https://chat.deepseek.com/sign_in" });
      await new Promise(r => setTimeout(r, 3000));
      const newScreenshotResult = await browser({ action: "screenshot", profile, targetId: tabId });
      const newScreenshotPath = newScreenshotResult.path;
      await exec({
        command: 'imsg send --to "' + userPhone + '" --text "QR refreshed - please scan again" --file "' + newScreenshotPath + '"'
      });
    }
  }
}

// Step 5: Input question
await browser({ action: "navigate", profile, targetId: tabId, targetUrl: "https://chat.deepseek.com/" });
await new Promise(r => setTimeout(r, 2000));
await browser({ action: "snapshot", profile, targetId: tabId });

await browser({
  action: "act",
  kind: "type",
  profile,
  targetId: tabId,
  ref: "e102", // From snapshot
  text: "What is the capital of France?"
});

await browser({ action: "act", kind: "press", profile, targetId: tabId, key: "Enter" });

// Step 6: Extract response
await new Promise(r => setTimeout(r, 10000));

// Robust response extraction
const response = await browser({
  action: "act",
  kind: "evaluate",
  profile,
  targetId: tabId,
  fn: `(function() {
    // Get all paragraph elements
    const paragraphs = Array.from(document.querySelectorAll('p'));
    
    // Filter to find assistant responses
    const assistantResponses = paragraphs.filter(p => {
      const text = p.innerText || p.textContent || '';
      return text.length > 20 && 
             !text.includes('AI-generated') &&
             !text.includes('Upload docs') &&
             !text.includes('How can I help') &&
             !text.includes('⌘');
    });
    
    // Get the most recent (last) response
    if (assistantResponses.length > 0) {
      return assistantResponses[assistantResponses.length - 1].innerText.trim();
    }
    
    // Fallback: try to find any substantial text
    const bodyText = document.body.innerText || document.body.textContent || '';
    const lines = bodyText.split('\n').filter(line => 
      line.trim().length > 50 && 
      !line.includes('AI-generated') &&
      !line.includes('How can I help')
    );
    
    return lines.length > 0 ? lines[lines.length - 1].trim() : 'No response found';
  })()`,
  returnByValue: true
});

console.log("Response:", response);
// Reply to user with response
```

---

## Common Selectors

|      Element       |        Selector       |
|--------------------|-----------------------|
| Chat input         | `textarea[placeholder*="Message DeepSeek"]` |
| Send (Enter)       | Press Enter key       |
| QR Code            | `img[src*="wechat"], iframe[src*="wechat"]` |
| User avatar        | `[class*="avatar"], [class*="user"]` |
| Response content   | Last `<p>` in `document.body` (filtered) |

---

## Configuration

### Phone Number Configuration

The user's phone number can be configured in several ways:

1. **Environment Variable**: Set `DEEPSEEK_PHONE` environment variable
   ```bash
   export DEEPSEEK_PHONE="+1234567890000"
   ```

2. **USER.md**: Add phone number to USER.md file
   ```markdown
   # USER.md
   Phone: +1234567890000
   ```

3. **Configuration File**: Add to OpenClaw configuration
   ```javascript
   // In your implementation code
   const userPhone = config.userPhone || process.env.DEEPSEEK_PHONE || "+1234567890000";
   ```

### QR Code Path Handling

The screenshot path is automatically returned by the `browser` tool's `screenshot` action:
```javascript
const screenshotResult = await browser({ action: "screenshot", profile: "openclaw", targetId: tabId });
const screenshotPath = screenshotResult.path; // Use the actual path from result
```

**Important:** Never assume a fixed path like `/Users/chris/.openclaw/media/browser/<uuid>.jpg`. Always use the path returned by the browser tool.

---

## Limitations

- **Rate Limiting**: DeepSeek may block requests (429 errors)
- **Event Validation**: Some buttons need real user events (use `kind: "press"` not JS dispatchEvent)
- **Login Verification**: QR Code scan requires user interaction
- **No API Access**: Direct API requires bypassing WAF
- **No Files Uploading**: DO NOT upload files to chat.deepseek.com
- **No LLM Processing**: Extract raw text only
- **Login Timeout**: Maximum 2 minutes for QR scan

## Troubleshooting

| Issue                  | Solution |
|------------------------|----------|
| Input not found        | Refresh page, take new snapshot |
| Enter not working      | Use browser act kind="press" with key="Enter" |
| ❌ Enter via JS dispatchEvent doesn't work | DeepSeek uses React/event validation - must use `kind: "press"` with `key: "Enter"` instead |
| Response not found     | Wait longer, check page rendering |
| QR Code timeout        | Automatically refreshes and re-sends |
| Login with phone       | DO NOT ask and input phone number |
| All channels fail      | Ask user to check browser tab manually |

## 🆕 Optimized: "Try Again with Fresh Question" Workflow

When a user wants to retry with a fresh question (e.g., after getting "Sorry, that's beyond my current scope"), use this optimized workflow:

### Option 1: Start Fresh Chat (Recommended for unsatisfactory responses)

```javascript
// Function to start a fresh chat session
async function startFreshChat(tabId) {
  // Navigate to main page to ensure clean state
  await browser({
    action: "navigate",
    profile: "openclaw",
    targetId: tabId,
    targetUrl: "https://chat.deepseek.com/"
  });
  
  await new Promise(r => setTimeout(r, 2000));
  
  // Take snapshot to get fresh refs
  await browser({
    action: "snapshot",
    profile: "openclaw",
    targetId: tabId
  });
  
  // Check if we're on a fresh chat page
  const status = await browser({
    action: "act",
    kind: "evaluate",
    profile: "openclaw",
    targetId: tabId,
    fn: `(function() {
      const welcomeMsg = document.querySelector('img[alt*="DeepSeek"], img[src*="deepseek"]');
      const chatInput = document.querySelector('textarea[placeholder*="Message DeepSeek"]');
      const previousChat = document.querySelector('[class*="message"]');
      
      return JSON.stringify({
        isFresh: !!welcomeMsg && !!chatInput && !previousChat,
        hasWelcome: !!welcomeMsg,
        hasInput: !!chatInput,
        hasPreviousChat: !!previousChat
      });
    })()`,
    returnByValue: true
  });
  
  const statusObj = JSON.parse(status);
  
  if (!statusObj.isFresh) {
    // Click "New chat" in sidebar (more reliable than top button)
    const sidebarResult = await browser({
      action: "act",
      kind: "evaluate",
      profile: "openclaw",
      targetId: tabId,
      fn: `(function() {
        // Find "New chat" link in sidebar
        const sidebarLinks = Array.from(document.querySelectorAll('a'));
        const newChatLink = sidebarLinks.find(link => 
          link.innerText.includes('New chat') || 
          link.textContent.includes('新聊天') ||
          (link.querySelector('div') && link.querySelector('div').innerText.includes('New chat'))
        );
        
        if (newChatLink) {
          newChatLink.click();
          return true;
        }
        return false;
      })()`,
      returnByValue: true
    });
    
    if (!sidebarResult) {
      // Fallback: use keyboard shortcut Cmd+J (⌘J)
      await browser({
        action: "act",
        kind: "press",
        profile: "openclaw",
        targetId: tabId,
        key: "Meta",  // Command key on Mac
        modifiers: ["Meta"]
      });
      
      await new Promise(r => setTimeout(r, 100));
      
      await browser({
        action: "act",
        kind: "type",
        profile: "openclaw",
        targetId: tabId,
        text: "j"
      });
      
      await new Promise(r => setTimeout(r, 100));
      
      await browser({
        action: "act",
        kind: "press",
        profile: "openclaw",
        targetId: tabId,
        key: "Meta",
        modifiers: []
      });
    }
    
    await new Promise(r => setTimeout(r, 2000));
  }
  
  return true;
}
```

### Option 2: Continue in Same Chat (if context is needed)

```javascript
// Function to continue in current chat but clear previous question
async function continueInCurrentChat(tabId, newQuestion) {
  // Just type the new question directly
  await browser({
    action: "snapshot",
    profile: "openclaw",
    targetId: tabId
  });
  
  // Find and focus the input
  const inputFound = await browser({
    action: "act",
    kind: "evaluate",
    profile: "openclaw",
    targetId: tabId,
    fn: `(function() {
      const input = document.querySelector('textarea[placeholder*="Message DeepSeek"], input[placeholder*="Message DeepSeek"]');
      if (input) {
        input.focus();
        input.value = '';
        return true;
      }
      return false;
    })()`,
    returnByValue: true
  });
  
  if (!inputFound) {
    throw new Error("Chat input not found");
  }
  
  // Type the new question
  await browser({
    action: "act",
    kind: "type",
    profile: "openclaw",
    targetId: tabId,
    ref: "e102", // Get from snapshot - adjust as needed
    text: newQuestion
  });
  
  // Submit
  await browser({
    action: "act",
    kind: "press",
    profile: "openclaw",
    targetId: tabId,
    key: "Enter"
  });
  
  return true;
}
```

## 🐛 Common Errors and Fixes

### Error: SyntaxError in JavaScript Evaluation

**IMPORTANT:** Never copy error examples! Always use the working functions provided below.

Common JavaScript syntax errors to avoid:
- ❌ `document.querySelecto rAll('p')` (space in function name)
- ✅ `document.querySelectorAll('p')` (correct)

- ❌ `split('\\n')` (double backslashes)
- ✅ `split('\n')` (single backslash)

- ❌ Missing `return` statement in evaluate functions
- ✅ Always include `return` statement

### Robust Response Extraction Function

Here's a corrected and more robust version:

```javascript
// Robust response extraction function
async function extractDeepSeekResponse(tabId) {
  try {
    const response = await browser({
      action: "act",
      kind: "evaluate",
      profile: "openclaw",
      targetId: tabId,
      fn: `(function() {
        // Find the most recent assistant response
        const paragraphs = Array.from(document.querySelectorAll('p'));
        
        // Filter out system messages and short texts
        const assistantParagraphs = paragraphs.filter(p => {
          const text = p.innerText || p.textContent || '';
          const parent = p.parentElement;
          const isSystemMessage = 
            text.includes('AI-generated') ||
            text.includes('Upload docs') ||
            text.includes('How can I help') ||
            text.includes('⌘') ||
            text.includes('We are asked:') ||
            text.length < 20;
          
          // Also check if it's in a response container (not in input area)
          const isInInputArea = parent && (
            parent.closest('textarea') || 
            parent.closest('input') ||
            parent.closest('[class*="input"]') ||
            parent.closest('[class*="message-input"]')
          );
          
          return !isSystemMessage && !isInInputArea && text.trim().length > 0;
        });
        
        // Get the last assistant response
        const lastResponse = assistantParagraphs[assistantParagraphs.length - 1];
        if (!lastResponse) return 'No response found';
        
        // Try to get the full response container
        let responseContainer = lastResponse.closest('div[class*="message"], div[class*="response"], div[class*="assistant"]');
        if (!responseContainer) {
          responseContainer = lastResponse.closest('div');
        }
        
        if (responseContainer) {
          // Get all text content from the response container
          const allText = responseContainer.innerText || responseContainer.textContent || '';
          // Clean up the text - use single backslashes in regex
          return allText
            .replace(/\s+/g, ' ')
            .replace(/\n\s*\n/g, '\n\n')
            .trim();
        }
        
        // Fallback to just the paragraph text
        return lastResponse.innerText || lastResponse.textContent || '';
      })()`,
      returnByValue: true
    });
    
    return response;
  } catch (error) {
    console.error("Error extracting response:", error);
    
    // Fallback: try simpler extraction
    const fallbackResponse = await browser({
      action: "act",
      kind: "evaluate",
      profile: "openclaw",
      targetId: tabId,
      fn: `(function() {
        // Simple fallback: get all text on page and find the last substantial block
        const allText = document.body.innerText || document.body.textContent || '';
        const lines = allText.split('\n').filter(line => 
          line.trim().length > 50 && 
          !line.includes('AI-generated') &&
          !line.includes('How can I help')
        );
        
        return lines.length > 0 ? lines[lines.length - 1].trim() : 'No response found';
      })()`,
      returnByValue: true
    });
    
    return fallbackResponse;
  }
}

// Usage:
// const answer = await extractDeepSeekResponse(tabId);
```

### Common JavaScript Errors to Avoid

**IMPORTANT:** Always copy from working examples, not error examples!

Common mistakes:
- **Typos in function names**: `querySelectorAll` not `querySelecto rAll`
- **Spaces in variable names**: `assistantParagraphs` not `assistantPar agraphs`
- **Incorrect selectors**: Use `closest('div')` not `closest('generic')`
- **Case sensitivity**: `returnByValue: true` not `returnByValue: True`
- **Missing semicolons**: Always end statements properly

### Fix: "No response found" Error

If you're getting "No response found" or "failed to extract response", DeepSeek's page structure has likely changed. Use this more robust extraction method:

```javascript
// ULTRA-ROBUST response extraction - tries multiple approaches
async function extractDeepSeekResponse(tabId) {
  const response = await browser({
    action: "act",
    kind: "evaluate",
    profile: "openclaw",
    targetId: tabId,
    fn: `(function() {
      // Helper: check if text is a system message
      function isSystemText(text) {
        const systemPatterns = [
          'AI-generated', 'Upload docs', 'How can I help', '⌘',
          'We are asked:', 'deepseek', 'Sign in', '登录',
          'Message DeepSeek', 'keyboard', 'shortcut'
        ];
        return systemPatterns.some(p => text.includes(p));
      }

      // Approach 1: Try finding message containers
      const messageDivs = document.querySelectorAll('div[class*="message"], div[class*="response"], div[class*="content"]');
      let allTexts = [];

      messageDivs.forEach(div => {
        const text = div.innerText || div.textContent || '';
        if (text.length > 30 && !isSystemText(text)) {
          allTexts.push(text.trim());
        }
      });

      // If we found messages in containers, return the last one
      if (allTexts.length > 0) {
        return allTexts[allTexts.length - 1];
      }

      // Approach 2: Try all <p> tags with relaxed filtering
      const paragraphs = document.querySelectorAll('p');
      const validParagraphs = [];
      paragraphs.forEach(p => {
        const text = p.innerText || p.textContent || '';
        if (text.length > 20 && !isSystemText(text)) {
          validParagraphs.push(text.trim());
        }
      });

      if (validParagraphs.length > 0) {
        return validParagraphs[validParagraphs.length - 1];
      }

      // Approach 3: Try <div> tags (newer DeepSeek structure)
      const divs = document.querySelectorAll('div');
      const validDivs = [];
      divs.forEach(div => {
        const text = div.innerText || div.textContent || '';
        // Look for substantial text blocks in the main content area
        if (text.length > 100 && !isSystemText(text) && !div.closest('header') && !div.closest('footer') && !div.closest('nav')) {
          validDivs.push(text.trim());
        }
      });

      if (validDivs.length > 0) {
        return validDivs[validDivs.length - 1];
      }

      // Approach 4: Fallback to full page body text
      const bodyText = document.body.innerText || document.body.textContent || '';
      const lines = bodyText.split('\n').filter(line =>
        line.trim().length > 50 && !isSystemText(line)
      );

      if (lines.length > 0) {
        return lines[lines.length - 1].trim();
      }

      // Last resort: return debug info
      return 'No response found - page may be loading or have unexpected structure';
    })()`,
    returnByValue: true
  });

  console.log("Extracted response:", response.substring(0, 200) + "...");
  return response;
}
```

### Debugging Tips

```javascript
// Add debug logging to browser evaluate functions
const debugInfo = await browser({
  action: "act",
  kind: "evaluate",
  profile: "openclaw",
  targetId: tabId,
  fn: `(function() {
    // Debug: log what we find
    const paragraphs = document.querySelectorAll('p');
    console.log('Found', paragraphs.length, 'paragraphs');

    for (let i = 0; i < Math.min(paragraphs.length, 5); i++) {
      console.log('Paragraph', i, ':', paragraphs[i].innerText.substring(0, 100));
    }
    
    return JSON.stringify({
      paragraphCount: paragraphs.length,
      sampleTexts: Array.from(paragraphs).slice(0, 3).map(p => p.innerText.substring(0, 50))
    });
  })()`,
  returnByValue: true
});

console.log("Debug info:", debugInfo);
```

## 🛠️ Working Implementation Guide

### Always Use These Pre-tested Functions

Instead of writing your own extraction code, always use these pre-tested functions:

```javascript
// SIMPLE & RELIABLE extraction function
async function extractDeepSeekResponseSimple(tabId) {
  const response = await browser({
    action: "act",
    kind: "evaluate",
    profile: "openclaw",
    targetId: tabId,
    fn: `(function() {
      // Get all text from the page
      const allText = document.body.innerText || document.body.textContent || '';
      
      // Split into lines and filter out system messages
      const lines = allText.split('\n').filter(line => {
        const trimmed = line.trim();
        return trimmed.length > 50 && 
               !trimmed.includes('AI-generated') &&
               !trimmed.includes('Message DeepSeek') &&
               !trimmed.includes('How can I help') &&
               !trimmed.includes('Upload docs');
      });
      
      // Return the last substantial line (most likely the response)
      return lines.length > 0 ? lines[lines.length - 1].trim() : 'No response found';
    })()`,
    returnByValue: true
  });
  
  return response;
}

// Usage:
// const answer = await extractDeepSeekResponseSimple(tabId);
```

### Key Improvements in Optimized Workflow:

1. **Robust "New Chat" Detection**: Uses semantic search for "New chat" text in sidebar links
2. **Fallback Mechanisms**: Keyboard shortcut (Cmd+J) if sidebar link not found
3. **State Verification**: Checks if we're already on a fresh chat page
4. **Better Response Extraction**: Filters out system messages and thought processes
5. **Error Handling**: Graceful fallbacks for missing elements
6. **Clear Documentation**: Explains when to use fresh chat vs continue in same chat

### When to Use Which Approach:

| Scenario | Recommended Approach | Why |
|----------|---------------------|-----|
| Previous response was "Sorry, that's beyond my current scope" | **Start Fresh Chat** | DeepSeek might be in a restricted mode; fresh chat resets context |
| Want to ask unrelated follow-up | **Start Fresh Chat** | Avoids confusing the AI with previous context |
| Continuing same topic with refined question | **Continue in Current Chat** | Maintains context for better responses |
| Previous response was good but need clarification | **Continue in Current Chat** | AI can reference previous answer |

### Common Pitfalls Fixed:

1. **❌ WRONG**: Clicking ref=e306 (was a share button, not new chat)
2. **✅ CORRECT**: Clicking "New chat" link in sidebar or using Cmd+J
3. **❌ WRONG**: Assuming input ref is always e102
4. **✅ CORRECT**: Using snapshot to get fresh refs each time
5. **❌ WRONG**: Extracting all paragraphs including system messages
6. **✅ CORRECT**: Filtering out AI-generated disclaimers and thought processes

### ⚠️ Important Note About Element References:

**Never rely on fixed ref IDs like `e306`, `e102`, etc.** These IDs are:
- Generated dynamically by the browser snapshot tool
- Can change between snapshots or page reloads
- Different for each user and session

**Always use semantic selectors or get fresh refs from snapshot:**

## 🧠 DeepThink Mode Optimization

The DeepThink button (labeled "DeepThink" to the left of the "Search" button) enables enhanced reasoning mode. When activated, DeepSeek provides more detailed, step-by-step responses.

### How to Enable DeepThink Mode

```javascript
// Function to toggle DeepThink mode
async function toggleDeepThinkMode(tabId, enable = true) {
  await browser({
    action: "snapshot",
    profile: "openclaw",
    targetId: tabId
  });
  
  // Check current DeepThink state
  const currentState = await browser({
    action: "act",
    kind: "evaluate",
    profile: "openclaw",
    targetId: tabId,
    fn: `(function() {
      const deepThinkBtn = document.querySelector('button[aria-label*="DeepThink"], button:has(> div:contains("DeepThink"))');
      const searchBtn = document.querySelector('button[aria-label*="Search"], button:has(> div:contains("Search"))');
      
      return JSON.stringify({
        hasDeepThink: !!deepThinkBtn,
        hasSearch: !!searchBtn,
        deepThinkActive: deepThinkBtn ? deepThinkBtn.getAttribute('aria-pressed') === 'true' || 
                                        deepThinkBtn.classList.contains('active') || 
                                        deepThinkBtn.getAttribute('data-active') === 'true' : false,
        deepThinkText: deepThinkBtn ? deepThinkBtn.innerText || deepThinkBtn.textContent : '',
        searchText: searchBtn ? searchBtn.innerText || searchBtn.textContent : ''
      });
    })()`,
    returnByValue: true
  });
  
  const state = JSON.parse(currentState);
  console.log("DeepThink state:", state);
  
  // If we want DeepThink enabled but it's not active
  if (enable && state.hasDeepThink && !state.deepThinkActive) {
    console.log("Enabling DeepThink mode...");
    
    // Click the DeepThink button
    const clicked = await browser({
      action: "act",
      kind: "evaluate",
      profile: "openclaw",
      targetId: tabId,
      fn: `(function() {
        // Find DeepThink button by text content
        const buttons = Array.from(document.querySelectorAll('button'));
        const deepThinkBtn = buttons.find(btn => 
          btn.innerText.includes('DeepThink') || 
          btn.textContent.includes('DeepThink') ||
          (btn.querySelector('div') && btn.querySelector('div').innerText.includes('DeepThink'))
        );
        
        if (deepThinkBtn) {
          deepThinkBtn.click();
          return true;
        }
        
        // Alternative: Find button near search button
        const searchBtn = buttons.find(btn => 
          btn.innerText.includes('Search') || 
          btn.textContent.includes('Search')
        );
        
        if (searchBtn && searchBtn.previousElementSibling) {
          searchBtn.previousElementSibling.click();
          return true;
        }
        
        return false;
      })()`,
      returnByValue: true
    });
    
    if (clicked) {
      console.log("DeepThink mode enabled");
      await new Promise(r => setTimeout(r, 1000)); // Wait for UI update
      return true;
    }
  }
  
  // If we want DeepThink disabled but it's active
  if (!enable && state.hasDeepThink && state.deepThinkActive) {
    console.log("Disabling DeepThink mode...");
    
    // Click the DeepThink button again to toggle off
    const clicked = await browser({
      action: "act",
      kind: "evaluate",
      profile: "openclaw",
      targetId: tabId,
      fn: `(function() {
        const buttons = Array.from(document.querySelectorAll('button'));
        const deepThinkBtn = buttons.find(btn => 
          btn.innerText.includes('DeepThink') || 
          btn.textContent.includes('DeepThink')
        );
        
        if (deepThinkBtn) {
          deepThinkBtn.click();
          return true;
        }
        return false;
      })()`,
      returnByValue: true
    });
    
    if (clicked) {
      console.log("DeepThink mode disabled");
      await new Promise(r => setTimeout(r, 1000));
      return true;
    }
  }
  
  return false;
}
```

### Complete Workflow with DeepThink Mode

```javascript
// Ask a question with DeepThink mode enabled
async function askWithDeepThink(tabId, question) {
  console.log("Asking question with DeepThink mode...");
  
  // Enable DeepThink mode
  await toggleDeepThinkMode(tabId, true);
  
  // Wait for UI to update
  await new Promise(r => setTimeout(r, 1000));
  
  // Take fresh snapshot
  await browser({
    action: "snapshot",
    profile: "openclaw",
    targetId: tabId
  });
  
  // Find and focus input
  const inputFound = await browser({
    action: "act",
    kind: "evaluate",
    profile: "openclaw",
    targetId: tabId,
    fn: `(function() {
      const input = document.querySelector('textarea[placeholder*="Message DeepSeek"], input[placeholder*="Message DeepSeek"]');
      if (input) {
        input.focus();
        input.value = '';
        return true;
      }
      return false;
    })()`,
    returnByValue: true
  });
  
  if (!inputFound) {
    throw new Error("Chat input not found");
  }
  
  // Type the question
  await browser({
    action: "act",
    kind: "type",
    profile: "openclaw",
    targetId: tabId,
    text: question
  });
  
  // Submit
  await browser({
    action: "act",
    kind: "press",
    profile: "openclaw",
    targetId: tabId,
    key: "Enter"
  });
  
  // Wait longer for DeepThink response (it thinks before answering)
  console.log("Waiting for DeepThink response (may take 10-15 seconds)...");
  await new Promise(r => setTimeout(r, 15000));
  
  // Extract response
  const response = await browser({
    action: "act",
    kind: "evaluate",
    profile: "openclaw",
    targetId: tabId,
    fn: `(function() {
      // Get all paragraph elements
      const paras = Array.from(document.querySelectorAll('p'));
      
      // Filter to find assistant responses (including DeepThink reasoning)
      const assistantResponses = paras.filter(p => {
        const text = p.innerText || '';
        return text.length > 20 && 
               !text.includes('AI-generated') &&
               !text.includes('Upload docs') &&
               !text.includes('How can I help') &&
               !text.includes('⌘');
      });
      
      // Get the most recent (last) response
      return assistantResponses.length > 0 
        ? assistantResponses[assistantResponses.length - 1].innerText.trim()
        : 'No response found';
    })()`,
    returnByValue: true
  });
  
  console.log("DeepThink response received");
  return response;
}

// Example usage:
// const deepThinkResponse = await askWithDeepThink(tabId, "Solve: 2x + 5 = 15");
```

### When to Use DeepThink Mode

| Use Case | Recommended Mode | Why |
|----------|-----------------|-----|
| Math problems, logic puzzles | **DeepThink ON** | Provides step-by-step reasoning |
| Code debugging, algorithm design | **DeepThink ON** | Shows thought process and analysis |
| Simple factual questions | **DeepThink OFF** | Faster response, no need for reasoning |
| Creative writing, brainstorming | **DeepThink ON** | More thoughtful, structured responses |
| Quick information lookup | **DeepThink OFF** | Faster, more concise answers |

### DeepThink Button Identification Strategies

The DeepThink button can be identified in several ways:

1. **By text content**: Button containing "DeepThink"
2. **By position**: Button immediately left of "Search" button
3. **By aria-label**: Button with `aria-label` containing "DeepThink"
4. **By active state**: When enabled, has `[active]` attribute or `aria-pressed="true"`

```javascript
// Multiple strategies for finding DeepThink button
function findDeepThinkButton() {
  // Strategy 1: By text content
  const byText = document.querySelector('button:has(> div:contains("DeepThink"))');
  if (byText) return byText;
  
  // Strategy 2: By aria-label
  const byAria = document.querySelector('button[aria-label*="DeepThink"]');
  if (byAria) return byAria;
  
  // Strategy 3: Relative to Search button
  const searchBtn = document.querySelector('button:has(> div:contains("Search"))');
  if (searchBtn && searchBtn.previousElementSibling) {
    return searchBtn.previousElementSibling;
  }
  
  // Strategy 4: By class names (may change)
  const byClass = document.querySelector('button[class*="deepthink"], button[class*="DeepThink"]');
  if (byClass) return byClass;
  
  return null;
}
```

### Toggle Between Modes

```javascript
// Toggle between DeepThink and regular mode
async function toggleResponseMode(tabId) {
  const currentState = await browser({
    action: "act",
    kind: "evaluate",
    profile: "openclaw",
    targetId: tabId,
    fn: `(function() {
      const btn = document.querySelector('button[aria-label*="DeepThink"], button:has(> div:contains("DeepThink"))');
      return btn ? (btn.getAttribute('aria-pressed') === 'true' || btn.classList.contains('active')) : false;
    })()`,
    returnByValue: true
  });
  
  const isActive = currentState === 'true';
  console.log(`DeepThink is currently ${isActive ? 'active' : 'inactive'}`);
  
  // Toggle the button
  await toggleDeepThinkMode(tabId, !isActive);
  
  return !isActive;
}

// Usage: const newState = await toggleResponseMode(tabId);
// Returns true if DeepThink is now active, false if regular mode
```

```javascript
// ❌ WRONG - Hardcoded ref IDs
await browser({ action: "act", kind: "click", ref: "e306" });

// ✅ CORRECT - Semantic selection
await browser({ action: "act", kind: "evaluate", fn: `(function() {
  const newChatLink = document.querySelector('a[href*="/a/chat"]');
  if (newChatLink && newChatLink.innerText.includes('New chat')) {
    newChatLink.click();
    return true;
  }
  return false;
})()` });

// ✅ CORRECT - Get ref from snapshot
// First take snapshot, then use ref from the snapshot response
const snapshot = await browser({ action: "snapshot", targetId: tabId });
// Parse snapshot to find "New chat" element ref
const newChatRef = findRefByText(snapshot, "New chat");
await browser({ action: "act", kind: "click", ref: newChatRef });
```

The user's original attempt (`<tool_call><function=browser><action>act</action><profile>openclaw</profile><targetId>00AA2439B0832C440F6EDAF46A34029F</targetId><kind>click</kind><ref>e306</ref></function></tool_call>`) failed because:
- ref=e306 was not a "New chat" button (it was likely a share/export button)
- The correct "New chat" element was ref=e292 in sidebar or ref=e35 after reload
...but these refs are not reliable either!

**Always use semantic content-based selection instead of ref IDs.**

### Why dispatchEvent Doesn't Work

DeepSeek's chat input is built with React and validates that keyboard events come from real user interactions. Using JavaScript's `dispatchEvent()` to simulate key presses will silently fail:

```javascript
// ❌ WRONG - This doesn't work!
const input = document.querySelector('textarea[placeholder*="Message DeepSeek"]');
input.dispatchEvent(new KeyboardEvent('keydown', { key: 'Enter' }));
input.dispatchEvent(new KeyboardEvent('keyup', { key: 'Enter' }));

// ✅ CORRECT - Use browser press action
await browser({
  action: "act",
  kind: "press",
  profile: "openclaw",
  targetId: tabId,
  key: "Enter"
});
```

The `press` action sends a real key event through the browser automation layer, which passes DeepSeek's event validation.

---

## 🎯 Best Practices & Recommendations

Based on analysis of common failures and successful implementations, follow these best practices:

### 1. Response Extraction Best Practices

**✅ DO: Use the Simple Extraction Function**
```javascript
// ALWAYS use this simple function - it's tested and reliable
const response = await getDeepSeekResponseSimple(tabId);

// Only use complex functions if simple one fails
if (response.includes('No response found') || response.includes('Error:')) {
  // Try robust version as fallback
  const response = await extractDeepSeekResponse(tabId);
}
```

**✅ DO: Add Error Handling**
```javascript
try {
  const response = await extractDeepSeekResponse(tabId);
  console.log("Success:", response);
} catch (error) {
  console.error("Extraction failed:", error);
  // Implement fallback strategy
}
```

**✅ DO: Increase Wait Times for Complex Responses**
```javascript
// Simple questions: 10 seconds
await new Promise(r => setTimeout(r, 10000));

// Complex questions or DeepThink mode: 15-20 seconds  
await new Promise(r => setTimeout(r, 15000));
```

### 2. Element Selection Best Practices

**✅ DO: Use Semantic Selectors**
```javascript
// Find elements by content, not hardcoded refs
const newChatLink = document.querySelector('a[href*="/a/chat"]');
if (newChatLink && newChatLink.innerText.includes('New chat')) {
  newChatLink.click();
}
```

**✅ DO: Get Fresh Refs from Snapshots**
```javascript
// Take snapshot to get current element references
const snapshot = await browser({ action: "snapshot", targetId: tabId });
// Parse snapshot to find elements dynamically
```

**❌ DON'T: Use Hardcoded Ref IDs**
```javascript
// ❌ WRONG - These change dynamically!
await browser({ action: "act", kind: "click", ref: "e306" });
await browser({ action: "act", kind: "click", ref: "e102" });
```

### 3. JavaScript Code Quality

**✅ DO: Use Correct Regex Patterns**
```javascript
// ❌ WRONG - Double backslashes
.replace(/\\s+/g, ' ')
.split('\\n')

// ✅ CORRECT - Single backslashes  
.replace(/\s+/g, ' ')
.split('\n')
```

**✅ DO: Avoid Optional Chaining in Older Environments**
```javascript
// ❌ WRONG - Might not be supported
msgs[msgs.length - 1]?.innerText || 'No response';

// ✅ CORRECT - Traditional check
if (msgs.length > 0) {
  return msgs[msgs.length - 1].innerText;
}
return 'No response';
```

**✅ DO: Use Function Wrappers**
```javascript
// ❌ WRONG - Direct code
fn: `{ const paras = document.querySelectorAll('p'); ... }`

// ✅ CORRECT - Function wrapper
fn: `(function() { 
  const paras = document.querySelectorAll('p'); 
  return ...; 
})()`
```

### 4. Debugging & Testing

**✅ DO: Add Debug Logging**
```javascript
const debugInfo = await browser({
  action: "act",
  kind: "evaluate",
  profile: "openclaw",
  targetId: tabId,
  fn: `(function() {
    const paragraphs = document.querySelectorAll('p');
    console.log('Found', paragraphs.length, 'paragraphs');
    
    // Log first few paragraphs for debugging
    for (let i = 0; i < Math.min(paragraphs.length, 5); i++) {
      console.log('Paragraph', i, ':', paragraphs[i].innerText.substring(0, 100));
    }
    
    return JSON.stringify({
      paragraphCount: paragraphs.length,
      sampleTexts: Array.from(paragraphs).slice(0, 3).map(p => p.innerText.substring(0, 50))
    });
  })()`,
  returnByValue: true
});

console.log("Debug info:", debugInfo);
```

**✅ DO: Test Extraction Before Reliance**
```javascript
// Test the extraction function with a simple question first
const testQuestion = "What is 2+2?";
await askQuestion(tabId, testQuestion);
const testResponse = await extractDeepSeekResponse(tabId);
console.log("Test response:", testResponse);

// If test works, proceed with actual question
if (testResponse && testResponse.includes('4')) {
  console.log("✅ Extraction test passed");
  // Proceed with actual question
}
```

### 5. Common Failure Patterns to Avoid

| Failure Pattern | Solution |
|----------------|----------|
| "No response found" | Increase wait time, use robust extraction, check page structure |
| JavaScript syntax errors | Fix regex patterns, avoid optional chaining, use function wrappers |
| Element not found | Use semantic selectors, take fresh snapshot, add fallbacks |
| Login timeout | Increase timeout, implement QR refresh, better error messaging |
| Event validation fails | Use `kind: "press"` not `dispatchEvent()` |
| `<tool_call>` | DO NOT send raw html tags content to user session. Just retry to extract or tell user to go on asking. |

### 6. Quick Reference: Working Implementation

```javascript
// Most reliable implementation pattern
async function askDeepSeekReliably(tabId, question) {
  try {
    // 1. Ensure fresh chat session
    await startFreshChat(tabId);
    
    // 2. Type question with proper event handling
    await browser({
      action: "act",
      kind: "type",
      profile: "openclaw",
      targetId: tabId,
      text: question
    });
    
    // 3. Submit with press action (not dispatchEvent)
    await browser({
      action: "act",
      kind: "press",
      profile: "openclaw",
      targetId: tabId,
      key: "Enter"
    });
    
    // 4. Wait appropriately
    await new Promise(r => setTimeout(r, 15000));
    
    // 5. Extract with robust function
    const response = await extractDeepSeekResponse(tabId);
    
    // 6. Handle potential failures
    if (response.includes('No response found') || response.length < 10) {
      // Try fallback extraction
      return await fallbackExtraction(tabId);
    }
    
    return response;
  } catch (error) {
    console.error("DeepSeek query failed:", error);
    return `Error: ${error.message}`;
  }
}
```

### 7. When to Use Which Approach

| Use Case | Recommended Function | Wait Time | Notes |
|----------|---------------------|-----------|-------|
| Simple factual questions | `extractDeepSeekResponse` | 10s | Fast, reliable for most cases |
| Complex reasoning questions | `ultraRobustExtractDeepSeekResponse` | 15-20s | Handles complex page structures |
| DeepThink mode responses | `extractDeepSeekResponse` with DeepThink enabled | 20s | Longer thinking time needed |
| Critical queries | Try multiple extraction methods | 20s+ | Combine results for reliability |

---

## See Also

- `imsg` skill - Send results to iMessage
- `openclaw channels status` skill - Get enabled channels
- `openclaw browser status` skill - Get browser status
- `browser` tool - OpenClaw browser control
