const { parseArgs, printError } = require('./utils');
const IMAP = require('./utils/imap.js');
const SMTP = require('./utils/smtp.js');

const IMAP_COMMANDS = new Set([
  'check', 'fetch', 'read', 'search', 'stats', 'mark-read', 'mark-unread', 'seen', 'unseen',
  'delete', 'del', 'download', 'list-mailboxes', 'sync', 'clear-cache'
]);
const SMTP_COMMANDS = new Set(['send', 'test', 'reply', 'forward']);

function showHelp() {
  console.log(`
## Mail CLI - Email Management

### Usage
  node scripts/mail.js <command> [options]

### IMAP Commands (Reading)
  check [--all|--limit N]     Show inbox (cached by default)
  sync                        Check server for new messages
  fetch <uid>                 Read email by UID
  search --from "x"           Search by sender (cached)
  search --subject "x"        Search by subject (cached)
  search --server --from "x"  Search on server
  seen <uid>                  Mark as read
  unseen <uid>                Mark as unread
  delete <uid>                Delete email
  download <uid>              Download attachments
  list-mailboxes              List all mailboxes
  stats                       Email statistics

### SMTP Commands (Sending)
  send --to <email> --subject "Subj" --body "Text"
  send --to <email> --body-file file.md    # Markdown supported
  send --to <email> --attach file.pdf
  test                        Test SMTP connection
  reply <uid> --body "Text"
  forward <uid> --to <email>

### Options
  --help, -h                  Show this help

### Examples
  node scripts/mail.js check
  node scripts/mail.js fetch 123
  node scripts/mail.js send --to user@example.com --subject "Hi" --body "Hello"
`);
}

async function main() {
  const { command, options, positional } = parseArgs();

  if (!command || command === '--help' || command === '-h' || command === 'help') {
    showHelp();
    process.exit(0);
  }

  if (options.help || options.h) {
    showHelp();
    process.exit(0);
  }

  if (IMAP_COMMANDS.has(command)) {
    const handler = IMAP[command] || IMAP.default;
    await handler(options, positional);
  } else if (SMTP_COMMANDS.has(command)) {
    const handler = SMTP[command] || SMTP.default;
    await handler(options, positional);
  } else {
    console.error('\n## Error\n');
    console.error(`Unknown command: ${command}\n`);
    console.error('### IMAP Commands\n');
    console.error('- check, fetch, read, search, stats');
    console.error('- mark-read, mark-unread, seen, unseen');
    console.error('- delete, download, list-mailboxes, sync, clear-cache\n');
    console.error('### SMTP Commands\n');
    console.error('- send, test, reply, forward\n');
    process.exit(1);
  }
}

main().catch(err => {
  printError(err);
  process.exit(1);
});
