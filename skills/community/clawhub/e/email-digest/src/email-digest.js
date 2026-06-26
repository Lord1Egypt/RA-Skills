/**
 * EmailDigest — Daily Email Summary for Agents
 * Categorizes and summarizes emails. Works with himalaya IMAP or raw mailbox data.
 * @author @TheShadowRose
 * @license MIT
 */
const fs = require('fs');

class EmailDigest {
  constructor(options = {}) {
    this.prioritySenders = (options.prioritySenders || []).map(s => s.toLowerCase());
    this.urgencyKeywords = options.urgencyKeywords || ['urgent', 'asap', 'deadline', 'expires', 'emergency', 'payment due'];
    this.actionKeywords = options.actionKeywords || ['please review', 'action required', 'needs your', 'can you', 'could you', 'approve'];
    this.ignoreSenders = (options.ignoreSenders || []).map(s => s.toLowerCase());
  }

  categorize(emails) {
    const urgent = [], action = [], fyi = [], ignored = [];

    for (const email of emails) {
      const from = (email.from || '').toLowerCase();
      const subject = (email.subject || '').toLowerCase();
      const body = (email.body || email.snippet || '').toLowerCase();
      const text = subject + ' ' + body;

      if (this.ignoreSenders.some(s => s.includes('*') ? from.includes(s.replace(/\*/g, '')) : from.includes(s))) {
        ignored.push(email);
        continue;
      }
      if (this.prioritySenders.some(s => from.includes(s)) || this.urgencyKeywords.some(k => text.includes(k))) {
        urgent.push(email);
      } else if (this.actionKeywords.some(k => text.includes(k))) {
        action.push(email);
      } else {
        fyi.push(email);
      }
    }

    return { urgent, action, fyi, ignored };
  }

  format(categorized) {
    const lines = [`📬 Email Digest — ${new Date().toLocaleDateString()}\n`];
    if (categorized.urgent.length > 0) {
      lines.push(`URGENT (${categorized.urgent.length}):`);
      for (const e of categorized.urgent) lines.push(`• ${e.subject} — from ${e.from}`);
      lines.push('');
    }
    if (categorized.action.length > 0) {
      lines.push(`ACTION NEEDED (${categorized.action.length}):`);
      for (const e of categorized.action) lines.push(`• ${e.subject}`);
      lines.push('');
    }
    if (categorized.fyi.length > 0) {
      lines.push(`FYI (${categorized.fyi.length}):`);
      for (const e of categorized.fyi.slice(0, 10)) lines.push(`• ${e.subject}`);
      if (categorized.fyi.length > 10) lines.push(`  ...and ${categorized.fyi.length - 10} more`);
    }
    if (categorized.ignored.length > 0) lines.push(`\nFiltered: ${categorized.ignored.length} messages`);
    return lines.join('\n');
  }

  digest(emails) {
    const cats = this.categorize(emails);
    return { ...cats, formatted: this.format(cats), total: emails.length };
  }
}

module.exports = { EmailDigest };
