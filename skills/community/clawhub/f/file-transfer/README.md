# OpenClaw File Transfer Skill

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Node.js Version](https://img.shields.io/badge/node-%3E%3D18.0.0-brightgreen)](https://nodejs.org/)
[![OpenClaw Skill](https://img.shields.io/badge/OpenClaw-Skill-orange)](https://openclaw.ai)

A context-aware file transfer skill for the OpenClaw ecosystem. Intelligently transfers files based on conversation context (group chat vs private chat) with smart notifications and progress tracking.

## Features

- **Context-Aware Transfers**: Automatically detects group/private chat contexts and infers transfer intent
- **Smart File Validation**: MIME type checking, size limits, chunked reading for large files
- **Telegram Integration**: Full Telegram adapter with progress tracking and transfer status
- **Extensible Architecture**: Adapter pattern for adding new channels (WhatsApp, Discord planned)

## Installation

### From Source
```bash
git clone https://github.com/Ghostwritten/file-transfer.git
cd file-transfer
npm install
```

## Quick Start

### Using FileTransferSkill
```javascript
import { FileTransferSkill } from './src/index.js';

const skill = new FileTransferSkill({
  channels: {
    telegram: { enabled: true, maxFileSize: 50 * 1024 * 1024 }
  }
});

const result = await skill.sendFileWithContext({
  file: '/path/to/document.pdf',
  caption: 'Team weekly report',
  context: { chatId: '-1003655501651' }
});
```

### Using TelegramAdapter Directly
```javascript
import { TelegramAdapter } from './src/adapters/telegram-adapter.js';

const adapter = new TelegramAdapter({
  maxFileSize: 50 * 1024 * 1024,
  chunkSize: 10 * 1024 * 1024
});

const result = await adapter.sendFile({
  filePath: '/path/to/document.pdf',
  chatId: '-1003655501651',
  caption: 'Project document sharing'
});

console.log('Transfer ID:', result.transferId);
console.log('Context analysis:', result.analysis);
```

### Using Core Modules
```javascript
import { ContextEngine } from './src/core/context-engine.js';
import { FileManager } from './src/core/file-manager.js';

// Analyze context
const engine = new ContextEngine();
const analysis = await engine.analyzeContext({
  fileName: 'report.pdf',
  fileSize: 1024000,
  fileType: 'application/pdf',
  chatInfo: { isGroupChat: true, chatType: 'group' }
});

// Validate file
const manager = new FileManager();
const validation = await manager.validateFile('/path/to/file.pdf');
```

## Architecture

```
file-transfer/
├── src/
│   ├── index.js                   # Main entry - FileTransferSkill class
│   ├── core/
│   │   ├── context-engine.js      # Intelligent context analysis
│   │   └── file-manager.js        # File validation and management
│   ├── adapters/
│   │   └── telegram-adapter.js    # Telegram platform adapter
│   └── utils/
│       └── format.js              # Shared utilities (formatBytes)
├── tests/
│   ├── unit/                      # Unit tests
│   └── integration/               # Integration tests
├── docs/                          # Documentation
└── examples/                      # Usage examples
```

## Testing

```bash
# Run all tests
npm test

# Run unit tests only
npm run test:unit

# Run integration tests
npm run test:integration

# Generate coverage report
npm run test:coverage
```

## Documentation

- [API Reference](./docs/API.md)
- [Development Guide](./docs/DEVELOPMENT.md)
- [Contributing Guide](./docs/CONTRIBUTING.md)

## Current Status

**Version**: 0.2.0-beta

- ContextEngine and FileManager: fully implemented
- Telegram adapter: implemented (simulated transfer, no real API yet)
- WhatsApp and Discord adapters: planned
- 41 tests passing

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
