---
name: email-writer
description: Draft and send emails via browser automation. Supports Gmail, Outlook, QQ Mail, 163 Mail. Requires OpenClaw v2026.3.22+ with browser access.
version: 1.0.5
license: MIT-0
metadata: {"openclaw": {"emoji": "📧", "requires": {"bins": [], "env": []}, "minVersion": "2026.3.22", "needsBrowser": true}}
---

# Email Writer

Email composition and sending tool using OpenClaw browser automation.

> ⚠️ **数据外发提醒**：邮件内容（收件人、主题、正文）、附件将通过浏览器发送至用户选择的邮件服务商（Gmail / Outlook / QQ Mail / 163 Mail）的服务器。请勿在邮件中包含敏感信息。
>
> ⚠️ **安全提醒**：此 skill 通过浏览器自动填写并发送邮件。使用前请确认用户已在浏览器中登录邮箱。建议先用不重要的账号测试。

## Trigger Conditions

Only trigger when the user **explicitly asks to write and send an email to a specific recipient**. Do NOT trigger for:
- General questions about email format or best practices
- Drafting text that happens to be email-like without a "send" intent
- The user just copy-pasting an email address

## Features

- Draft professional emails with AI assistance
- Reply to emails with context
- Support Gmail, Outlook, QQ Mail, 163 Mail
- Multi-language support (Chinese and English)

## Trigger Conditions

Only trigger when the user **explicitly asks to write and send an email** — they provide a recipient, subject, or content. Do NOT trigger for:
- General questions about email format or best practices
- Drafting text that happens to be email-like without a "send" intent
- The user just copy-pasting an email address in conversation

Specific phrases (only when accompanied by actual email content):
- "发送邮件给..."
- "帮我写一封邮件..."
- "回复这封邮件..."
- "Send an email to..."

**Before any browser action, always first confirm with the user:**
1. Recipient email address
2. Subject line
3. Key content points
4. Formal or informal tone
5. That the user is already logged into their email in the browser

## Privacy Warning

> ⚠️ 邮件内容通过浏览器发送至邮件服务商（Gmail/Outlook/QQ/163）的服务器。所有 processing 在本地进行，但发送是网络操作。

## Step 1: Understand Email Request

Ask user for email details:

- Recipient email address
- Subject line
- Content/key points
- Formal or informal tone
- Language preference

## Step 2: Detect Email Provider

```javascript
// Detect which email provider based on URL
function detectProvider(url) {
  if (url.includes('mail.google.com') || url.includes('gmail.com')) return 'gmail';
  if (url.includes('outlook.live.com') || url.includes('outlook.com')) return 'outlook';
  if (url.includes('mail.qq.com')) return 'qq';
  if (url.includes('mail.163.com')) return '163';
  if (url.includes('mail.126.com')) return '126';
  return 'unknown';
}
```

## Step 3: Open Email Client

```javascript
// Open email client based on user preference
await browser.open({ url: "https://mail.google.com" })
await browser.wait({ timeout: 5000 })
```

Supported platforms:
- Gmail: mail.google.com
- Outlook: outlook.live.com
- QQ Mail: mail.qq.com
- 163 Mail: mail.163.com
- 126 Mail: mail.126.com

## Step 4: Compose New Email

### Gmail Compose

```javascript
// Click compose button (Gmail)
await browser.click({ selector: '[gh="cm"]' })
await browser.wait({ timeout: 2000 })

// Fill recipient
await browser.evaluate((email) => {
  const toField = document.querySelector('[name="to"]');
  if (toField) {
    toField.focus();
    toField.value = email;
    toField.dispatchEvent(new Event('input', { bubbles: true }));
  }
}, recipientEmail)

// Fill subject
await browser.evaluate((subject) => {
  const subjectField = document.querySelector('[name="subjectbox"]');
  if (subjectField) {
    subjectField.focus();
    subjectField.value = subject;
  }
}, emailSubject)

// Fill body
await browser.evaluate((body) => {
  const bodyField = document.querySelector('[role="textbox"][contenteditable="true"]');
  if (bodyField) {
    bodyField.focus();
    bodyField.innerHTML = body.replace(/\n/g, '<br>');
  }
}, emailBody)

// Send (Gmail)
await browser.click({ selector: '[gh="s"]' })
```

### Outlook Compose

```javascript
// Click new message button (Outlook)
await browser.click({ selector: '[aria-label="New message"], .ms-Button--primary' })
await browser.wait({ timeout: 2000 })

// Fill recipient (Outlook)
await browser.evaluate((email) => {
  const toField = document.querySelector('[aria-label="To"], input[placeholder*="To"]');
  if (toField) {
    toField.focus();
    toField.value = email;
    toField.dispatchEvent(new Event('input', { bubbles: true }));
  }
}, recipientEmail)

// Fill subject (Outlook)
await browser.evaluate((subject) => {
  const subjectField = document.querySelector('[aria-label="Subject"], input[placeholder*="Subject"]');
  if (subjectField) {
    subjectField.focus();
    subjectField.value = subject;
  }
}, emailSubject)

// Fill body (Outlook)
await browser.evaluate((body) => {
  const bodyField = document.querySelector('[aria-label="Message body"], [role="textbox"]');
  if (bodyField) {
    bodyField.focus();
    bodyField.innerHTML = body.replace(/\n/g, '<br>');
  }
}, emailBody)

// Send (Outlook)
await browser.click({ selector: '[aria-label="Send"], button[title="Send"]' })
```

### QQ Mail Compose

```javascript
// Click compose button (QQ Mail)
await browser.click({ selector: '.compose-button, .btn-compose, [title="写信"]' })
await browser.wait({ timeout: 2000 })

// Fill recipient (QQ Mail)
await browser.evaluate((email) => {
  const toField = document.querySelector('#to_input, input[name="to"]') ||
                  document.querySelector('[aria-label="收件人"]');
  if (toField) {
    toField.focus();
    toField.value = email;
    toField.dispatchEvent(new Event('input', { bubbles: true }));
  }
}, recipientEmail)

// Fill subject (QQ Mail)
await browser.evaluate((subject) => {
  const subjectField = document.querySelector('#subject, input[name="subject"]');
  if (subjectField) {
    subjectField.focus();
    subjectField.value = subject;
  }
}, emailSubject)

// Fill body (QQ Mail)
await browser.evaluate((body) => {
  const bodyField = document.querySelector('#QMEditorArea iframe') ||
                    document.querySelector('.qmEditorArea');
  if (bodyField) {
    if (bodyField.tagName === 'IFRAME') {
      bodyField.contentDocument.body.innerHTML = body.replace(/\n/g, '<br>');
    } else {
      bodyField.innerHTML = body.replace(/\n/g, '<br>');
    }
  }
}, emailBody)

// Send (QQ Mail)
await browser.click({ selector: '.btn-send, [title="发送"], .qmBtn' })
```

### 163 Mail Compose

```javascript
// Click compose button (163 Mail)
await browser.click({ selector: '.nui-mainToolbar-btn, .js-component-composebtn' })
await browser.wait({ timeout: 2000 })

// Fill recipient (163 Mail)
await browser.evaluate((email) => {
  const toField = document.querySelector('#draft_to_input, input[name="to"]') ||
                  document.querySelector('.nui-editableAddr-input');
  if (toField) {
    toField.focus();
    toField.value = email;
    toField.dispatchEvent(new Event('input', { bubbles: true }));
  }
}, recipientEmail)

// Fill subject (163 Mail)
await browser.evaluate((subject) => {
  const subjectField = document.querySelector('#draft_subject, input[name="subject"]');
  if (subjectField) {
    subjectField.focus();
    subjectField.value = subject;
  }
}, emailSubject)

// Fill body (163 Mail)
await browser.evaluate((body) => {
  const bodyField = document.querySelector('.APP-editor-iframe iframe') ||
                    document.querySelector('.nuiEditor');
  if (bodyField) {
    if (bodyField.tagName === 'IFRAME') {
      bodyField.contentDocument.body.innerHTML = body.replace(/\n/g, '<br>');
    } else {
      bodyField.innerHTML = body.replace(/\n/g, '<br>');
    }
  }
}, emailBody)

// Send (163 Mail)
await browser.click({ selector: '.nui-mainToolbar-sendBtn, .js-component-sendbtn' })
```

## Step 5: Reply to Email

### Gmail Reply

```javascript
await browser.click({ selector: '.zA' })
await browser.click({ selector: '[aria-label="Reply"]' })
await browser.wait({ timeout: 2000 })
await browser.evaluate((body) => {
  const bodyField = document.querySelector('[role="textbox"][contenteditable="true"]');
  if (bodyField) bodyField.innerHTML = body.replace(/\n/g, '<br>');
}, replyBody)
await browser.click({ selector: '[gh="s"]' })
```

### Outlook Reply

```javascript
await browser.click({ selector: '[aria-label="Reply"]' })
await browser.wait({ timeout: 2000 })
await browser.evaluate((body) => {
  const bodyField = document.querySelector('[aria-label="Message body"]');
  if (bodyField) bodyField.innerHTML = body.replace(/\n/g, '<br>');
}, replyBody)
await browser.click({ selector: '[aria-label="Send"]' })
```

### QQ Mail Reply

```javascript
await browser.click({ selector: '.btn-reply, [title="回复"]' })
await browser.wait({ timeout: 2000 })
await browser.evaluate((body) => {
  const iframe = document.querySelector('#QMEditorArea iframe');
  if (iframe) iframe.contentDocument.body.innerHTML = body.replace(/\n/g, '<br>');
}, replyBody)
await browser.click({ selector: '.btn-send, [title="发送"]' })
```

### 163 Mail Reply

```javascript
await browser.click({ selector: '.js-component-replybtn, [title="回复"]' })
await browser.wait({ timeout: 2000 })
await browser.evaluate((body) => {
  const iframe = document.querySelector('.APP-editor-iframe iframe');
  if (iframe) iframe.contentDocument.body.innerHTML = body.replace(/\n/g, '<br>');
}, replyBody)
await browser.click({ selector: '.js-component-sendbtn' })
```

## Step 6: Send Confirmation

```javascript
// Wait for send
await browser.wait({ timeout: 3000 })

// Check for success message
const sent = await browser.evaluate(() => {
  const text = document.body.innerText;
  return text.includes('Message sent') ||
         text.includes('Sent') ||
         text.includes('已发送') ||
         text.includes('发送成功') ||
         text.includes('邮件已发送');
})

if (sent) {
  console.log("Email sent successfully!")
}
```

## Email Templates

### Thank You Email

Subject: Thank you for your support

Dear [Name],

Thank you for [specific reason].

[Details]

Best regards,
[Your name]

### Work Report

Subject: Work Report - [Date]

Hi Manager,

Weekly report:

1. Completed tasks
2. In progress
3. Next week plan

Best,
[Your name]

### Meeting Invitation

Subject: Meeting: [Topic]

Hi [Name],

Please join our meeting:

Time: [Time]
Location: [Location/Link]
Agenda:
1. Topic 1
2. Topic 2

Please confirm your attendance.

Thanks,
[Your name]

## Error Handling

- Email not logged in: Prompt user to log in
- Send failed: Prompt user to send manually
- Attachment failed: Suggest manual attachment
- Unknown provider: Ask user which email service

## Limitations

- Cannot handle email verification codes
- Cannot send encrypted emails
- No batch sending support
- QQ/163 may need iframe handling

## Privacy and Security

- No email content uploaded externally
- All processing done locally
- Browser email session accessed
- Review before sending sensitive information

## Notes

- Requires OpenClaw v2026.3.22+
- Gmail has most reliable selectors
- QQ/163 use iframe for email body
- Test with non-sensitive account first
