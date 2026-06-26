#!/usr/bin/env node

/**
 * SMTP Email CLI
 * Send email via SMTP protocol. Works with Gmail, Outlook, 163.com, and any standard SMTP server.
 * Supports attachments, HTML content, and multiple recipients.
 */

const nodemailer = require('nodemailer');
const path = require('path');
const fs = require('fs');
const { marked } = require('marked');
const mimeTypes = require('mime-types');

// Load .env and import utils
require('.');

const { printError } = require('.');

// Simple markdown detection patterns
const MD_PATTERNS = [
  /^#{1,6}\s/m,              // Headers
  /\[.+\]\(.+\)/m,          // Links
  /\*\*.+\*\*/m,            // Bold
  /^\s*[\*\-\+]\s/m,        // Lists
  /^\|.+\|/m,               // Tables
  /^\s*\d+\./m              // Numbered lists
];

// Check if content looks like markdown
function isMarkdown(content, filename = null) {
  if (filename && filename.toLowerCase().endsWith('.md')) {
    return true;
  }
  for (const pattern of MD_PATTERNS) {
    if (pattern.test(content)) {
      return true;
    }
  }
  return false;
}

// Convert markdown to HTML with styling
function markdownToHtml(markdown) {
  marked.setOptions({
    gfm: true,
    breaks: true,
    headerIds: false,
    mangle: false
  });

  let html = marked.parse(markdown);

  const styledHtml = `<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <style>
    body {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
      line-height: 1.6;
      color: #333;
      max-width: 800px;
      margin: 0 auto;
      padding: 20px;
    }
    h1, h2, h3, h4, h5, h6 {
      color: #2c3e50;
      margin-top: 14px;
      margin-bottom: 16px;
    }
    h1 { font-size: 12px; border-bottom: 1px solid #eee; padding-bottom: 6px; }
    h2 { font-size: 12px; border-bottom: 1px solid #eee; padding-bottom: 6px; }
    h3 { font-size: 10px; }
    p { margin: 12px 0; }
    a { color: #3498db; text-decoration: none; }
    a:hover { text-decoration: underline; }
    code {
      background: #f4f4f4;
      padding: 2px 6px;
      border-radius: 3px;
      font-family: 'Courier New', monospace;
      font-size: 0.9em;
    }
    pre {
      background: #f4f4f4;
      padding: 16px;
      border-radius: 6px;
      overflow-x: auto;
    }
    pre code { padding: 0; background: none; }
    blockquote {
      border-left: 4px solid #ddd;
      margin: 0;
      padding-left: 16px;
      color: #666;
    }
    ul, ol { padding-left: 24px; }
    li { margin: 4px 0; }
    table {
      border-collapse: collapse;
      width: 100%;
      margin: 16px 0;
    }
    th, td {
      border: 1px solid #ddd;
      padding: 12px;
      text-align: left;
    }
    th {
      background: #f4f4f4;
      font-weight: 600;
    }
    tr:nth-child(even) { background: #f9f9f9; }
    hr {
      border: none;
      border-top: 1px solid #eee;
      margin: 24px 0;
    }
  </style>
</head>
<body>
${html}
</body>
</html>`;

  return styledHtml;
}

// Create SMTP transporter
function createTransporter() {
  const config = {
    host: process.env.SMTP_HOST,
    port: parseInt(process.env.SMTP_PORT) || 587,
    secure: process.env.SMTP_SECURE === 'true',
    auth: {
      user: process.env.SMTP_USER,
      pass: process.env.SMTP_PASS,
    },
    tls: {
      rejectUnauthorized: process.env.SMTP_REJECT_UNAUTHORIZED !== 'false',
    },
  };

  if (!config.host || !config.auth.user || !config.auth.pass) {
    throw new Error('Missing SMTP configuration. Please set SMTP_HOST, SMTP_USER, and SMTP_PASS in .env');
  }

  return nodemailer.createTransport(config);
}

// Build from field with optional name
function buildFromField(fromEmail) {
  const email = fromEmail || process.env.SMTP_FROM || process.env.SMTP_USER;
  const name = process.env.FROM_NAME;
  if (name) {
    return `"${name}" <${email}>`;
  }
  return email;
}

// Append signature to email content
function appendSignature(content, isHtml) {
  if (isHtml) {
    const sig = process.env.EMAIL_SIGNATURE;
    if (sig) {
      if (content.includes('</body>')) {
        return content.replace('</body>', `${sig}</body>`);
      }
      return content + '\n' + sig;
    }
  } else {
    const sig = process.env.EMAIL_SIGNATURE_TEXT;
    if (sig) {
      return content + '\n\n' + sig;
    }
  }
  return content;
}

// Send email
async function sendEmail(options) {
  const transporter = createTransporter();

  try {
    await transporter.verify();
    console.error('SMTP server is ready to send');
  } catch (err) {
    throw new Error(`SMTP connection failed: ${err.message}`);
  }

  let htmlContent = options.html;
  let textContent = options.text;

  if (htmlContent && process.env.EMAIL_SIGNATURE) {
    htmlContent = appendSignature(htmlContent, true);
  }
  if (textContent && process.env.EMAIL_SIGNATURE_TEXT) {
    textContent = appendSignature(textContent, false);
  }

  const mailOptions = {
    from: options.from ? (process.env.FROM_NAME ? `"${process.env.FROM_NAME}" <${options.from}>` : options.from) : buildFromField(),
    to: options.to,
    cc: options.cc || undefined,
    bcc: options.bcc || undefined,
    subject: options.subject || '(no subject)',
    text: textContent || undefined,
    html: htmlContent || undefined,
    attachments: options.attachments || [],
  };

  if (!mailOptions.text && !mailOptions.html) {
    mailOptions.text = options.body || '';
    if (process.env.EMAIL_SIGNATURE_TEXT) {
      mailOptions.text = appendSignature(mailOptions.text, false);
    }
  }

  const info = await transporter.sendMail(mailOptions);

  return {
    success: true,
    messageId: info.messageId,
    response: info.response,
    to: mailOptions.to,
  };
}

// Read file content for attachments with proper MIME types
function readAttachment(filePath) {
  if (!fs.existsSync(filePath)) {
    throw new Error(`Attachment file not found: ${filePath}`);
  }

  const filename = path.basename(filePath);
  const contentType = mimeTypes.lookup(filePath) || 'application/octet-stream';

  return {
    filename: filename,
    path: path.resolve(filePath),
    contentType: contentType
  };
}

// Process multiple attachments
function processAttachments(attachOption) {
  if (!attachOption) return [];

  const files = [];
  const entries = Array.isArray(attachOption) ? attachOption : [attachOption];

  for (const entry of entries) {
    const paths = entry.split(',').map(p => p.trim()).filter(p => p);
    for (const filePath of paths) {
      files.push(readAttachment(filePath));
    }
  }

  return files;
}

// Send email with file content
async function sendEmailWithContent(options) {
  if (options.attach) {
    options.attachments = processAttachments(options.attach);
  }

  return await sendEmail(options);
}

// Test SMTP connection
async function testConnection() {
  const transporter = createTransporter();

  try {
    await transporter.verify();
    const info = await transporter.sendMail({
      from: buildFromField(),
      to: process.env.SMTP_USER,
      subject: 'SMTP Connection Test',
      text: 'This is a test email from the IMAP/SMTP email skill.',
      html: '<p>This is a <strong>test email</strong> from the IMAP/SMTP email skill.</p>',
    });

    return {
      success: true,
      message: 'SMTP connection successful',
      messageId: info.messageId,
    };
  } catch (err) {
    throw new Error(`SMTP test failed: ${err.message}`);
  }
}

// ============ COMMAND HANDLERS ============

// Fetch email data from IMAP (for reply/forward)
async function getEmailForReplyForward(uid) {
  const { fetchEmail } = require('./imap.js');
  const result = await fetchEmail(uid, false);
  if (!result || result.length === 0) {
    throw new Error(`Message UID ${uid} not found`);
  }
  return result[0];
}

async function reply(options, positional) {
  if (!positional[0]) {
    throw new Error('UID required: node mail.js reply <uid>');
  }
  if (!options.body && !options['body-file']) {
    throw new Error('Missing --body or --body-file for reply');
  }

  // Fetch original email
  const original = await getEmailForReplyForward(positional[0]);

  // Extract original sender
  let toAddress;
  try {
    const fromMatch = original.from.match(/<?([^<>@\s]+@[^<>@\s]+\.[^<>@\s]+)>?/);
    toAddress = fromMatch ? fromMatch[1] : original.from;
  } catch {
    toAddress = original.from;
  }

  // Build subject with Re:
  const subject = original.subject
    ? (original.subject.match(/^Re:\s*/i) ? '' : 'Re: ') + original.subject
    : 'Re: (no subject)';

  // Build reply body (quote original)
  const quotedBody = options.body
    ? options.body + '\n\n--- Original Message ---\n' + (original.text || '(no text)')
    : options.body;

  const replyOptions = {
    ...options,
    to: toAddress,
    subject: subject,
    body: quotedBody,
  };

  // Use send handler
  await send(replyOptions, []);
  console.log(`\n- **Reply to:** ${toAddress}\n`);
}

async function forward(options, positional) {
  if (!positional[0]) {
    throw new Error('UID required: node mail.js forward <uid>');
  }
  if (!options.to) {
    throw new Error('Missing --to <email> for forward');
  }

  // Fetch original email
  const original = await getEmailForReplyForward(positional[0]);

  // Build subject with Fwd:
  const subject = original.subject
    ? (original.subject.match(/^Fwd:\s*/i) ? '' : 'Fwd: ') + original.subject
    : 'Fwd: (no subject)';

  // Build forward body (quote original)
  const forwardedBody = options.body
    ? options.body + '\n\n--- Forwarded Message ---\nFrom: ' + original.from + '\nDate: ' + original.date + '\nSubject: ' + original.subject + '\n\n' + (original.text || '(no text)')
    : '--- Forwarded Message ---\nFrom: ' + original.from + '\nDate: ' + original.date + '\nSubject: ' + original.subject + '\n\n' + (original.text || '(no text)');

  const forwardOptions = {
    ...options,
    subject: subject,
    body: forwardedBody,
  };

  // Use send handler
  await send(forwardOptions, []);
  console.log(`\n- **Forwarded to:** ${options.to}\n`);
}

async function send(options, positional) {
  if (!options.to) {
    throw new Error('Missing required option: --to <email>');
  }
  if (!options.subject && !options['subject-file']) {
    throw new Error('Missing required option: --subject <text> or --subject-file <file>');
  }

  if (options['subject-file']) {
    options.subject = fs.readFileSync(options['subject-file'], 'utf8').trim();
  }

  let bodyContent = null;
  let isBodyHtml = false;
  let isMarkdownDetected = false;

  if (options['body-file']) {
    bodyContent = fs.readFileSync(options['body-file'], 'utf8');
    const filename = options['body-file'];

    if (options.markdown || isMarkdown(bodyContent, filename)) {
      isMarkdownDetected = true;
      console.log('📝 Converting Markdown to HTML...');
      bodyContent = markdownToHtml(bodyContent);
      isBodyHtml = true;
    } else if (filename.endsWith('.html') || options.html) {
      isBodyHtml = true;
    }
  } else if (options['html-file']) {
    bodyContent = fs.readFileSync(options['html-file'], 'utf8');
    isBodyHtml = true;
  } else if (options.body) {
    bodyContent = options.body;
    if (options.html === true) {
      isBodyHtml = true;
    } else if (options.markdown || isMarkdown(bodyContent)) {
      isMarkdownDetected = true;
      console.log('📝 Converting Markdown to HTML...');
      bodyContent = markdownToHtml(bodyContent);
      isBodyHtml = true;
    }
  }

  if (bodyContent) {
    if (isBodyHtml) {
      options.html = bodyContent;
    } else {
      options.text = bodyContent;
    }
  }

  const result = await sendEmailWithContent(options);
  console.log('\n## Email Sent\n');
  console.log(`- **To:** ${result.to}`);
  console.log(`- **Message ID:** ${result.messageId}`);
  console.log();
}

async function test(options, positional) {
  const result = await testConnection();
  console.log('\n## SMTP Test\n');
  console.log(`- **Status:** ${result.success ? 'Success' : 'Failed'}`);
  console.log(`- **Message:** ${result.message}`);
  console.log(`- **Message ID:** ${result.messageId}`);
  console.log();
}

async function reply(options, positional) {
  if (!positional[0]) {
    throw new Error('UID required: mail.js reply <uid>');
  }

  // Fetch original email
  const { fetchEmail } = require('./imap.js');
  const [original, imap] = await fetchEmail(positional[0], false);
  if (!original) {
    imap.end();
    throw new Error(`Message UID ${positional[0]} not found`);
  }

  // Extract original sender for reply-to
  const replyTo = original.from;
  const subject = original.subject.startsWith('Re:') ? original.subject : 'Re: ' + original.subject;

  // Build quoted reply body
  const quotedBody = options.body
    ? options.body + '\n\n' + formatQuotedReply(original.text, original.from, original.date)
    : formatQuotedReply(original.text, original.from, original.date);

  // Apply markdown if needed
  let bodyContent = quotedBody;
  let isBodyHtml = false;

  if (options.markdown || isMarkdown(quotedBody)) {
    console.log('📝 Converting Markdown to HTML...');
    bodyContent = markdownToHtml(quotedBody);
    isBodyHtml = true;
  }

  const sendOptions = {
    to: replyTo,
    cc: options.cc,
    bcc: options.bcc,
    subject: subject,
    html: isBodyHtml ? bodyContent : undefined,
    text: isBodyHtml ? undefined : bodyContent,
    attachments: [],
  };

  const result = await sendEmailWithContent(sendOptions);
  imap.end();
  console.log('\n## Reply Sent\n');
  console.log(`- **To:** ${result.to}`);
  console.log(`- **Subject:** ${subject}`);
  console.log(`- **Message ID:** ${result.messageId}`);
  console.log();
}

async function forward(options, positional) {
  if (!positional[0]) {
    throw new Error('UID required: mail.js forward <uid>');
  }
  if (!options.to) {
    throw new Error('Missing required option: --to <email>');
  }

  // Fetch original email
  const { fetchEmail } = require('./imap.js');
  const [original, imap] = await fetchEmail(positional[0], false);
  if (!original) {
    imap.end();
    throw new Error(`Message UID ${positional[0]} not found`);
  }

  const subject = original.subject.startsWith('Fwd:') ? original.subject : 'Fwd: ' + original.subject;

  // Build forwarded content
  const forwardedBody = options.body
    ? options.body + '\n\n' + formatForwarded(original)
    : formatForwarded(original);

  let bodyContent = forwardedBody;
  let isBodyHtml = false;

  if (options.markdown || isMarkdown(forwardedBody)) {
    console.log('📝 Converting Markdown to HTML...');
    bodyContent = markdownToHtml(forwardedBody);
    isBodyHtml = true;
  }

  const sendOptions = {
    to: options.to,
    cc: options.cc,
    bcc: options.bcc,
    subject: subject,
    html: isBodyHtml ? bodyContent : undefined,
    text: isBodyHtml ? undefined : bodyContent,
    attachments: [],
  };

  const result = await sendEmailWithContent(sendOptions);
  imap.end();
  console.log('\n## Email Forwarded\n');
  console.log(`- **To:** ${result.to}`);
  console.log(`- **Subject:** ${subject}`);
  console.log(`- **Message ID:** ${result.messageId}`);
  console.log();
}

function formatQuotedReply(text, from, date) {
  const lines = (text || '').split('\n');
  const quoted = lines.map(line => '> ' + line).join('\n');
  const dateStr = formatDate(date);
  return `On ${dateStr}, ${from} wrote:\n\n${quoted}`;
}

function formatForwarded(original) {
  return `---------- Forwarded message ---------\nFrom: ${original.from}\nDate: ${formatDate(original.date)}\nSubject: ${original.subject}\n\n${original.text || ''}`;
}

function formatDate(date) {
  if (!date) return '';
  try {
    const d = new Date(date);
    return d.toLocaleString('en-US', {
      weekday: 'short', year: 'numeric', month: 'short', day: 'numeric',
      hour: '2-digit', minute: '2-digit'
    });
  } catch {
    return String(date);
  }
}

// Export handlers
module.exports.send = send;
module.exports.reply = reply;
module.exports.forward = forward;
module.exports.test = test;
module.exports.default = async (options, positional) => {
  console.error('\n## Error\n');
  console.error('Unknown command\n');
  console.error('### Available Commands\n');
  console.error('- `send` --to <email> --subject <text> [--body <text>] [--html] [--markdown] [--cc <email>] [--bcc <email>] [--attach <file>]');
  console.error('- `send` --to <email> --subject <text> --body-file <file> [--html-file <file>] [--attach <file>]');
  console.error('- `test` Test SMTP connection\n');
  process.exit(1);
};

// CLI entry point when run directly
if (require.main === module) {
  const { parseArgs } = require('.');
  const { command, options, positional } = parseArgs();
  const handler = module.exports[command] || module.exports.default;
  handler(options, positional).catch(err => {
    console.error('\n## Error\n');
    console.error('```\n' + err.message + '\n```\n');
    process.exit(1);
  });
}
