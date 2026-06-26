/**
 * Shared utilities re-export
 */

// Load .env first
require('./env');

const { parseArgs } = require('./args');
const {
  formatDate,
  formatRelativeTime,
  decodeSubject,
  parseAddress,
  formatFlags,
  hasAttachments,
  isUnread,
  printMessagesTable,
  printError,
} = require('./format');

module.exports = {
  parseArgs,
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
