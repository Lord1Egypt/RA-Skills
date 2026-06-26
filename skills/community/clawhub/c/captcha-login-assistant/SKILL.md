---
name: "captcha-login-assistant"
description: "Assist with web login processes that require CAPTCHA verification. Uses Chrome DevTools MCP to capture screenshots, recognizes CAPTCHA codes using AI vision, automatically fills forms and submits login. Applicable for web systems requiring CAPTCHA authentication."
---

# CAPTCHA Login Assistant

## Overview

This skill automates the login process for web systems requiring CAPTCHA verification. It uses Chrome DevTools MCP to capture login page screenshots, employs AI vision to recognize CAPTCHA codes, automatically fills in account credentials and CAPTCHA, and completes the login operation.

## Applicable Scenarios

- Web system logins requiring CAPTCHA verification
- Login scenarios with short CAPTCHA validity periods
- Situations requiring rapid consecutive login operations

## Core Workflow

### 1. Preparation

Ensure the following tools are available:
- Chrome DevTools MCP service
- Target login page URL
- Valid account credentials (username and password)

### 2. Login Steps

#### Step 1: Refresh Page to Get New CAPTCHA
```javascript
// Navigate to login page and refresh
mcp_chrome-devtools-mcp_navigate_page({
  "type": "reload"
})
```

#### Step 2: Capture Login Page Screenshot
```javascript
// Capture current page viewport
mcp_chrome-devtools-mcp_take_screenshot({
  "filePath": "path/to/login_screenshot.png"
})
```

#### Step 3: Recognize CAPTCHA
- View the CAPTCHA image in the screenshot
- CAPTCHA is usually located to the right of the "Enter CAPTCHA" input field
- Carefully identify CAPTCHA characters (note case sensitivity)

#### Step 4: Quickly Fill Form
```javascript
// Use JavaScript to fill all fields simultaneously
mcp_chrome-devtools-mcp_evaluate_script({
  "function": "() => {\n    const username = document.querySelector('input[name=\"username\"]');\n    const password = document.querySelector('input[name=\"password\"]');\n    const verifyCode = document.querySelector('input[name=\"verifyCode\"]');\n    \n    if (username) {\n      username.value = 'your_username';\n      username.dispatchEvent(new Event('input', { bubbles: true }));\n    }\n    if (password) {\n      password.value = 'your_password';\n      password.dispatchEvent(new Event('input', { bubbles: true }));\n    }\n    if (verifyCode) {\n      verifyCode.value = 'recognized_captcha';\n      verifyCode.dispatchEvent(new Event('input', { bubbles: true }));\n    }\n    return 'filled';\n  }"
})
```

#### Step 5: Click Login Button
```javascript
// Click login button
mcp_chrome-devtools-mcp_evaluate_script({
  "function": "() => {\n    const loginBtn = document.querySelector('button[type=\"submit\"]') || document.querySelector('button');\n    if (loginBtn) {\n      loginBtn.click();\n      return 'login_clicked';\n    }\n    return 'button_not_found';\n  }"
})
```

#### Step 6: Verify Login Result
```javascript
// Wait for post-login page elements
mcp_chrome-devtools-mcp_wait_for({
  "text": ["Home", "Dashboard", "System", "Logout"],
  "timeout": 5000
})
```

## Key Insights

### CAPTCHA Recognition Tips

1. **Clear Screenshot** - Ensure CAPTCHA image is clearly visible within screenshot bounds
2. **Time Sensitivity** - CAPTCHA typically has short validity (1-3 seconds), fill immediately after recognition
3. **Careful Identification** - Distinguish similar characters (e.g., 0 vs O, 1 vs l, 5 vs S)
4. **Case Sensitivity** - CAPTCHA is usually case-sensitive

### Common Issues

#### CAPTCHA Verification Failed
- **Cause**: CAPTCHA has expired
- **Solution**: Immediately recapture screenshot, recognize new CAPTCHA, and resubmit

#### Page Element Not Found
- **Cause**: Page not fully loaded or element ID changed
- **Solution**: Get page snapshot first to confirm element existence

#### Redirected Back to Login After Login
- **Cause**: Session expired or token invalid
- **Solution**: Re-execute complete login workflow

## Best Practices

1. **Parallel Processing** - Screenshot capture and form preparation can be done in parallel
2. **Quick Response** - Fill form immediately after CAPTCHA recognition to minimize expiration risk
3. **Use JavaScript** - Direct DOM manipulation is faster than fill tools
4. **Verify Results** - Check page content after login to confirm success

## Examples

### Example 1: Standard Login Workflow

```
User: Help me login to this system http://example.com/login, username admin, password 123456

Execution Steps:
1. Navigate to login page
2. Capture screenshot to get CAPTCHA
3. Recognize CAPTCHA as "Ab3d"
4. Use JavaScript to fill username, password, and CAPTCHA
5. Click login button
6. Verify successful login
```

### Example 2: CAPTCHA Expiration Retry

```
If login fails showing "CAPTCHA verification failed":
1. Immediately recapture screenshot
2. Recognize new CAPTCHA
3. Refill and submit
4. Retry multiple times if necessary
```

## Important Notes

1. **Security** - Do not log passwords in logs
2. **Privacy** - Handle screenshots containing sensitive information appropriately
3. **Rate Limiting** - Be aware of system login rate limits to avoid triggering security mechanisms
4. **CAPTCHA Complexity** - For complex CAPTCHAs (distorted, with interference lines), multiple attempts may be needed

## Troubleshooting

| Issue | Possible Cause | Solution |
|-------|---------------|----------|
| Empty CAPTCHA recognition | Screenshot doesn't include CAPTCHA | Adjust screenshot bounds |
| Login button not found | Page not fully loaded | Wait for page load before operation |
| Repeated verification failures | CAPTCHA expires too quickly | Manual login or contact administrator |
| Redirect to login after login | Session issue | Clear cookies and retry |
