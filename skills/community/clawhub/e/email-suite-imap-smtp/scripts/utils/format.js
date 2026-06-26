/**
 * Shared formatting utilities
 */

function formatDate(dateStr) {
  if (!dateStr) return '';
  try {
    const date = new Date(dateStr);
    const now = new Date();
    const isToday = date.toDateString() === now.toDateString();
    const isThisYear = date.getFullYear() === now.getFullYear();

    if (isToday) {
      return date.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' });
    }
    if (isThisYear) {
      return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' }) + ' ' +
             date.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' });
    }
    return date.toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric' });
  } catch {
    return String(dateStr).slice(0, 20);
  }
}

function formatRelativeTime(isoString) {
  if (!isoString) return 'never';
  const past = new Date(isoString);
  const now = new Date();
  const diffMs = now - past;
  const diffMins = Math.floor(diffMs / 60000);
  if (diffMins < 1) return 'just now';
  if (diffMins < 60) return `${diffMins}m`;
  const diffHours = Math.floor(diffMins / 60);
  if (diffHours < 24) return `${diffHours}h`;
  const diffDays = Math.floor(diffHours / 24);
  return `${diffDays}d`;
}

function decodeSubject(subject) {
  if (!subject) return '(no subject)';
  try {
    return subject.replace(/=\?([\w-]+)\?B\?([^?]+)\?=/gi, (match, charset, text) => {
      return Buffer.from(text, 'base64').toString('utf-8');
    });
  } catch (e) {
    return subject;
  }
}

function parseAddress(addr) {
  if (!addr) return 'Unknown';
  const match = addr.match(/"?([^"]*)"?\s*<?([^>]*)>?/);
  if (match) {
    const name = match[1].trim();
    const email = match[2].trim();
    return name || email.split('@')[0];
  }
  return addr;
}

function formatFlags(flags) {
  if (!flags) return '';
  const flagArray = Array.isArray(flags) ? flags : (flags instanceof Set ? Array.from(flags) : []);
  const parts = [];
  if (!flagArray.includes('\\Seen')) parts.push('unread');
  if (flagArray.includes('\\Flagged')) parts.push('flagged');
  if (flagArray.includes('\\Answered')) parts.push('replied');
  return parts.join(', ');
}

function hasAttachments(email) {
  return email.attachments && email.attachments.length > 0;
}

function isUnread(flags) {
  if (!flags) return false;
  const flagArray = Array.isArray(flags) ? flags : (flags instanceof Set ? Array.from(flags) : []);
  return !flagArray.includes('\\Seen');
}

function printMessagesTable(messages, showUnreadOnly = false, stats = null) {
  if (!messages || messages.length === 0) {
    console.log('\nNo messages found\n');
    return;
  }

  let filtered = messages;
  if (showUnreadOnly) {
    filtered = messages.filter(m => isUnread(m.flags));
  }

  const unreadCount = messages.filter(m => isUnread(m.flags)).length;
  const title = showUnreadOnly ? 'Unread' : 'Inbox';

  console.log(`\n## ${title}\n`);

  if (stats) {
    let parts = [];
    if (stats.newCount > 0) parts.push(`**${stats.newCount}** new`);
    parts.push(`**${filtered.length}** messages`);
    console.log(parts.join(', ') + '\n');
    if (stats.lastSync) {
      console.log(`_synced ${formatRelativeTime(stats.lastSync)} ago_\n`);
    }
  } else {
    console.log(`**${filtered.length}** messages\n`);
  }

  console.log('| UID | 📎 | Flags | Subject | From | Date |');
  console.log('|-----|-----|-------|---------|------|------|');
  filtered.forEach(m => {
    const attach = m.hasAttachments ? '📎' : '';
    const flags = formatFlags(m.flags);
    const flags_md = flags ? `\`${flags}\`` : '';
    const subject = decodeSubject(m.subject || '').replace(/\|/g, '\\|');
    const from = parseAddress(m.from || '').replace(/\|/g, '\\|');
    const date = formatDate(m.date);
    console.log(`| ${m.uid || '-'} | ${attach} | ${flags_md} | ${subject} | ${from} | ${date} |`);
  });
  console.log();
}

function printError(message) {
  console.error('\n## Error\n');
  console.error('```\n' + message + '\n```\n');
}

module.exports = {
  formatDate,
  formatRelativeTime,
  decodeSubject,
  parseAddress,
  formatFlags,
  hasAttachments,
  isUnread,
  printMessagesTable,
  printError,
};
