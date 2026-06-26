/**
 * CLI Commands for Agent Mailbox
 * 
 * Usage: openclaw mail <command> [options]
 */

import { Mailbox } from '../lib/mailbox';
import * as fs from 'fs';
import * as path from 'path';

/**
 * Main CLI handler
 */
export async function handleCommand(command: string, args: string[]): Promise<void> {
  // Get agent name from environment or config
  const agent = process.env.AGENT_NAME || process.env.USER || 'agent';
  const mail = new Mailbox(agent);

  try {
    switch (command) {
      case 'check':
        await handleCheck(mail);
        break;

      case 'read':
        await handleRead(mail, args);
        break;

      case 'send':
        await handleSend(mail, args);
        break;

      case 'reply':
        await handleReply(mail, args);
        break;

      case 'archive':
        await handleArchive(mail, args);
        break;

      case 'delete':
        await handleDelete(mail, args);
        break;

      case 'search':
        await handleSearch(mail, args);
        break;

      case 'stats':
        await handleStats(mail);
        break;

      case 'process-urgent':
        await handleProcessUrgent(mail);
        break;

      case 'cleanup':
        await handleCleanup(mail);
        break;

      case 'export':
        await handleExport(mail);
        break;

      default:
        console.log(`Unknown command: ${command}`);
        printHelp();
    }
  } catch (error) {
    console.error(`Error: ${error}`);
    process.exit(1);
  }
}

/**
 * check - List inbox messages
 */
async function handleCheck(mail: Mailbox): Promise<void> {
  const inbox = await mail.getInbox();

  if (inbox.length === 0) {
    console.log('📭 Inbox is empty');
    return;
  }

  console.log(`\n📬 Inbox (${inbox.length} messages)\n`);

  const unread = inbox.filter(m => m.unread);
  if (unread.length > 0) {
    console.log(`Unread: ${unread.length}`);
    unread.forEach((msg, idx) => {
      const priority = msg.priority === 'urgent' ? '🔴' : msg.priority === 'high' ? '🟠' : '⚪';
      console.log(
        `  [${idx + 1}] ${priority} From: ${msg.from} | ${msg.subject.slice(0, 50)}`
      );
    });
  }

  const read = inbox.filter(m => !m.unread);
  if (read.length > 0) {
    console.log(`\nRead: ${read.length}`);
    read.slice(0, 5).forEach((msg) => {
      console.log(`  • From: ${msg.from} | ${msg.subject.slice(0, 50)}`);
    });
    if (read.length > 5) {
      console.log(`  ... and ${read.length - 5} more`);
    }
  }

  console.log();
}

/**
 * read - Read a specific message
 */
async function handleRead(mail: Mailbox, args: string[]): Promise<void> {
  const msgId = args[0];

  if (!msgId) {
    console.error('Usage: openclaw mail read <message-id>');
    process.exit(1);
  }

  const msg = await mail.read(msgId);

  if (!msg) {
    console.error(`Message not found: ${msgId}`);
    process.exit(1);
  }

  console.log(`\n${'='.repeat(60)}`);
  console.log(`From: ${msg.from}`);
  console.log(`Subject: ${msg.subject}`);
  console.log(`Priority: ${msg.priority}`);
  console.log(`Date: ${msg.created_at}`);
  console.log(`Status: ${msg.status}`);
  console.log(`${'='.repeat(60)}\n`);
  console.log(msg.body);

  if (msg.responses.length > 0) {
    console.log(`\n${'─'.repeat(60)}`);
    console.log('Responses:\n');
    msg.responses.forEach((resp) => {
      console.log(`${resp.from} (${resp.created_at}):`);
      console.log(resp.body);
      console.log();
    });
  }

  // Mark as read
  if (msg.status === 'unread') {
    await mail.markRead(msg.id);
  }
}

/**
 * send - Send a message
 */
async function handleSend(mail: Mailbox, args: string[]): Promise<void> {
  const opts = parseArgs(args);

  if (!opts.to || !opts.subject || !opts.body) {
    console.error('Usage: openclaw mail send --to <agent> --subject <text> --body <text> [--priority high]');
    process.exit(1);
  }

  const msg = await mail.send({
    to: opts.to,
    subject: opts.subject,
    body: opts.body,
    priority: (opts.priority || 'normal') as any,
    metadata: opts.metadata ? JSON.parse(opts.metadata) : undefined,
  });

  console.log(`✓ Message sent to ${opts.to}`);
  console.log(`  ID: ${msg.id}`);
}

/**
 * reply - Reply to a message
 */
async function handleReply(mail: Mailbox, args: string[]): Promise<void> {
  const opts = parseArgs(args);
  const msgId = args[0];

  if (!msgId || !opts.body) {
    console.error('Usage: openclaw mail reply <message-id> --body <text>');
    process.exit(1);
  }

  const success = await mail.reply(msgId, opts.body);

  if (success) {
    console.log(`✓ Reply sent`);
  } else {
    console.error(`Failed to reply to message: ${msgId}`);
    process.exit(1);
  }
}

/**
 * archive - Archive a message
 */
async function handleArchive(mail: Mailbox, args: string[]): Promise<void> {
  const msgId = args[0];

  if (!msgId) {
    console.error('Usage: openclaw mail archive <message-id>');
    process.exit(1);
  }

  const success = await mail.archive(msgId);

  if (success) {
    console.log(`✓ Message archived`);
  } else {
    console.error(`Failed to archive message: ${msgId}`);
    process.exit(1);
  }
}

/**
 * delete - Delete a message
 */
async function handleDelete(mail: Mailbox, args: string[]): Promise<void> {
  const msgId = args[0];

  if (!msgId) {
    console.error('Usage: openclaw mail delete <message-id>');
    process.exit(1);
  }

  const success = await mail.delete(msgId);

  if (success) {
    console.log(`✓ Message deleted`);
  } else {
    console.error(`Failed to delete message: ${msgId}`);
    process.exit(1);
  }
}

/**
 * search - Search messages
 */
async function handleSearch(mail: Mailbox, args: string[]): Promise<void> {
  const query = args.join(' ');

  if (!query) {
    console.error('Usage: openclaw mail search <query>');
    process.exit(1);
  }

  const results = await mail.search(query);

  if (results.length === 0) {
    console.log(`No messages found matching: ${query}`);
    return;
  }

  console.log(`\n📋 Search results for "${query}" (${results.length} found)\n`);

  results.forEach((msg, idx) => {
    console.log(`[${idx + 1}] ${msg.from} - ${msg.subject}`);
    console.log(`    ${msg.created_at}`);
  });

  console.log();
}

/**
 * stats - Show mailbox statistics
 */
async function handleStats(mail: Mailbox): Promise<void> {
  const stats = await mail.getStats();

  console.log(`\n📊 Mailbox Statistics\n`);
  console.log(`Total messages: ${stats.total}`);
  console.log(`Unread: ${stats.unread}`);
  console.log(`High priority: ${stats.high_priority}`);
  console.log(`Expired: ${stats.expired}`);
  console.log();
}

/**
 * process-urgent - Process high-priority messages (for cron)
 */
async function handleProcessUrgent(mail: Mailbox): Promise<void> {
  const urgent = await mail.getUrgent();

  if (urgent.length === 0) {
    console.log('No urgent messages');
    return;
  }

  console.log(`Processing ${urgent.length} urgent messages...`);

  for (const msg of urgent) {
    console.log(`\n[URGENT] From: ${msg.from}`);
    console.log(`Subject: ${msg.subject}`);
    console.log(`Priority: ${msg.priority}`);

    // Emit task event that your agent can listen for
    console.log(`MAIL_TASK: ${JSON.stringify({ message_id: msg.id, task_id: msg.metadata?.task_id })}`);

    // Mark as read
    await mail.markRead(msg.id);
  }

  // Archive expired
  const archived = await mail.archiveExpired();
  if (archived > 0) {
    console.log(`\nArchived ${archived} expired messages`);
  }
}

/**
 * cleanup - Clean up old messages
 */
async function handleCleanup(mail: Mailbox): Promise<void> {
  const archived = await mail.archiveExpired();
  console.log(`✓ Cleaned up ${archived} expired messages`);
}

/**
 * export - Export all messages
 */
async function handleExport(mail: Mailbox): Promise<void> {
  const inbox = await mail.getInbox();
  const timestamp = new Date().toISOString().split('T')[0];
  const filename = `mail-export-${timestamp}.json`;

  const exportData = {
    exported_at: new Date().toISOString(),
    message_count: inbox.length,
    messages: inbox,
  };

  fs.writeFileSync(filename, JSON.stringify(exportData, null, 2));
  console.log(`✓ Exported ${inbox.length} messages to ${filename}`);
}

// ===== Helpers =====

function parseArgs(args: string[]): Record<string, string> {
  const opts: Record<string, string> = {};

  for (let i = 0; i < args.length; i++) {
    if (args[i].startsWith('--')) {
      const key = args[i].slice(2);
      const value = args[i + 1];
      opts[key] = value;
      i++;
    }
  }

  return opts;
}

function printHelp(): void {
  console.log(`
Agent Mailbox CLI

Commands:
  check              List inbox messages
  read <id>          Read a specific message
  send               Send a message
    --to <agent>     Recipient agent
    --subject <text> Subject line
    --body <text>    Message body
    --priority       normal | high | urgent (default: normal)
  
  reply <id>         Reply to a message
    --body <text>    Reply text
  
  archive <id>       Archive a message
  delete <id>        Delete a message
  search <query>     Search messages
  stats              Show mailbox statistics
  process-urgent     Process urgent messages (for cron)
  cleanup            Archive expired messages
  export             Export all messages to JSON

Examples:
  openclaw mail check
  openclaw mail read msg-2026-03-07-abc123
  openclaw mail send --to clampy --subject "Team up?" --body "Found a bounty" --priority high
  openclaw mail reply msg-2026-03-07-abc123 --body "I'm in!"
`);
}
