/**
 * Email helper for agent send/receive operations.
 * 
 * Provides:
 *   sendEmail(to, subject, text, html?) — Send via Resend
 *   getInbox() — List unprocessed emails
 *   getEmail(id) — Read specific email
 *   ackEmail(id) — Mark as processed
 * 
 * Required secrets:
 *   RESEND_API_KEY — Full-access Resend API key
 *   RESEND_FROM — Default from address (e.g., "Agent <agent@domain.com>")
 * 
 * Required environment:
 *   BACKEND_URL — Base URL of the backend (e.g., http://localhost:3001)
 */
const RESEND_API = 'https://api.resend.com';

async function sendEmail(to, subject, text, html) {
  const apiKey = process.env.RESEND_API_KEY;
  if (!apiKey) throw new Error('RESEND_API_KEY not configured');

  const from = process.env.RESEND_FROM || 'Agent <agent@localhost>';
  const body = { from, to: Array.isArray(to) ? to : [to], subject, text };
  if (html) body.html = html;

  const res = await fetch(`${RESEND_API}/emails`, {
    method: 'POST',
    headers: { 'Authorization': `Bearer ${apiKey}`, 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });

  if (!res.ok) throw new Error(`Resend error ${res.status}: ${await res.text()}`);
  return res.json();
}

async function getInbox() {
  const base = process.env.BACKEND_URL || 'http://localhost:3001';
  const res = await fetch(`${base}/api/inbound-email`);
  const data = await res.json();
  return data.emails || [];
}

async function getEmail(id) {
  const base = process.env.BACKEND_URL || 'http://localhost:3001';
  const res = await fetch(`${base}/api/inbound-email/${id}`);
  return res.json();
}

async function ackEmail(id) {
  const base = process.env.BACKEND_URL || 'http://localhost:3001';
  await fetch(`${base}/api/inbound-email/${id}/ack`, { method: 'POST' });
}

module.exports = { sendEmail, getInbox, getEmail, ackEmail };
