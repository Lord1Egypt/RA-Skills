# File Transfer Skill

## Overview
Context-aware file transfer skill for OpenClaw ecosystem. Intelligently transfers files based on conversation context with progress tracking.

## Features
- **Context-Aware**: Automatically detects group/private chat and infers transfer intent
- **File Validation**: MIME type checking, size limits, chunked reading
- **Telegram Support**: Full adapter with progress tracking (simulated)
- **Extensible**: Adapter pattern for adding new channels

## Installation
```bash
npm install file-transfer
```

## Usage

### Basic File Transfer
```javascript
import { FileTransferSkill } from 'file-transfer';

const skill = new FileTransferSkill({
  channels: { telegram: { enabled: true } }
});

const result = await skill.sendFileWithContext({
  file: '/path/to/document.pdf',
  caption: 'Team weekly report',
  context: { chatId: '-1003655501651' }
});
```

### Direct Adapter Usage
```javascript
import { TelegramAdapter } from 'file-transfer/src/adapters/telegram-adapter.js';

const adapter = new TelegramAdapter();
const result = await adapter.sendFile({
  filePath: '/path/to/file.pdf',
  chatId: '-1003655501651',
  caption: 'Document sharing'
});
```

## Tool Definitions

### sendFileWithContext
Transfers a file with intelligent context detection.

**Parameters:**
- `file` (string, required): Path to the file
- `caption` (string, optional): File description
- `context` (object, optional): Conversation context with `chatId`

**Returns:**
- `success` (boolean): Transfer success status
- `messageId` (string): Message ID
- `context` (object): Context analysis result (scenario, urgency, confidence)
- `stats` (object): Transfer statistics (size, duration, channel)

### getTransferHistory
Retrieves file transfer history.

**Parameters:**
- `options` (object, optional): Query options

**Returns:**
- `history` (array): Transfer history records
- `stats` (object): Transfer statistics

## Configuration

```javascript
const skill = new FileTransferSkill({
  contextEngine: {
    enableAI: false,
    maxHistoryLength: 10
  },
  file: {
    maxFileSize: 100 * 1024 * 1024,  // 100MB
    allowedMimeTypes: ['application/pdf', 'image/jpeg', ...]
  },
  channels: {
    telegram: {
      enabled: true,
      maxFileSize: 50 * 1024 * 1024  // 50MB
    }
  }
});
```

## Context Analysis

The ContextEngine analyzes file transfers and returns:

| Field | Values | Description |
|-------|--------|-------------|
| scenario | `share`, `backup`, `collaborate`, `archive` | Transfer intent |
| urgency | `low`, `medium`, `high`, `critical` | Priority level |
| confidence | 0.0 - 1.0 | Analysis confidence |
| fileCategory | `document`, `image`, `video`, `archive`, `code` | File classification |

## Current Limitations

- Telegram adapter uses simulated transfer (no real API integration yet)
- WhatsApp and Discord adapters are planned but not implemented
- Transfer history is not persisted

## Testing

```bash
npm test                  # All tests
npm run test:unit         # Unit tests
npm run test:integration  # Integration tests
```

## License

MIT License - see [LICENSE](LICENSE) for details.
