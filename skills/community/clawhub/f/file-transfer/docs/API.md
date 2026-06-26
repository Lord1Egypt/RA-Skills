# API Reference

## Table of Contents
- [FileTransferSkill](#filetransferskill)
- [ContextEngine](#contextengine)
- [FileManager](#filemanager)
- [TelegramAdapter](#telegramadapter)

## FileTransferSkill

Main orchestrator class for file transfer operations.

### Constructor
```javascript
import { FileTransferSkill } from './src/index.js';

const skill = new FileTransferSkill({
  contextEngine: { enableAI: false },
  file: { maxFileSize: 100 * 1024 * 1024 },
  channels: {
    telegram: { enabled: true }
  }
});
```

### `sendFileWithContext(options)` -> `Promise<Object>`

Send a file with context-aware intelligence.

**Parameters:**
```javascript
{
  file: string,           // Path to the file
  caption?: string,       // File description
  context?: {             // Conversation context
    chatId: string
  },
  metadata?: object       // Additional metadata
}
```

**Returns:**
```javascript
{
  success: boolean,
  messageId: string,
  context: ContextAnalysis,
  stats: {
    size: string,         // Human-readable size
    duration: number,     // Milliseconds
    channel: string       // Channel name
  }
}
```

### `getTransferHistory(options?)` -> `Promise<Object>`

Returns transfer history (currently returns empty result).

### `configure(newConfig)` -> `void`

Update skill configuration. Reinitializes channels if channel config changes.

### `getStatus()` -> `Object`

Returns `{ version, channels, uptime }`.

---

## ContextEngine

Intelligent context analysis engine for file transfers.

### Constructor
```javascript
import { ContextEngine } from './src/core/context-engine.js';

const engine = new ContextEngine({
  enableAI: false,              // AI analysis (not yet implemented)
  maxHistoryLength: 10,         // Max history messages to analyze
  scenarioWeights: {            // Custom scenario weights
    share: 1.0,
    backup: 0.8,
    collaborate: 1.2,
    archive: 0.6
  }
});
```

### `analyzeContext(context)` -> `Promise<ContextAnalysis>`

Main analysis method.

**Parameters:**
```javascript
{
  filePath?: string,
  fileName?: string,
  fileSize?: number,          // Bytes
  fileType?: string,          // MIME type
  caption?: string,
  chatInfo?: {
    isGroupChat: boolean,
    chatType: 'private' | 'group' | 'channel'
  },
  userInfo?: object,
  history?: string[]          // Message history
}
```

**Returns (ContextAnalysis):**
```javascript
{
  scenario: 'share' | 'backup' | 'collaborate' | 'archive',
  urgency: 'low' | 'medium' | 'high' | 'critical',
  recommendedTargets: string[],
  metadata: {
    fileType: string,
    fileSize: number,
    fileName: string,
    chatType: string,
    userIntent: string
  },
  isGroupChat: boolean,
  chatType: string,
  fileCategory: 'document' | 'image' | 'video' | 'archive' | 'code',
  timestamp: string,          // ISO 8601
  confidence: number          // 0.0 - 1.0
}
```

### `categorizeFile(mimeType)` -> `string`

Classifies a MIME type into a category: `document`, `image`, `video`, `archive`, `code`.

### `extractUserIntent(context)` -> `string`

Extracts user intent from caption and history via keyword matching. Returns one of: `share`, `backup`, `collaborate`, `archive`, `unknown`.

### `getStatus()` -> `Object`

Returns engine operational status.

---

## FileManager

File operations, validation, and transfer management.

### Constructor
```javascript
import { FileManager } from './src/core/file-manager.js';

const manager = new FileManager({
  maxFileSize: 100 * 1024 * 1024,   // 100MB
  chunkSize: 10 * 1024 * 1024,      // 10MB
  allowedMimeTypes: ['application/pdf', 'image/jpeg', ...],
  tempDir: '/tmp/openclaw-file-transfer'
});
```

### `validateFile(filePath)` -> `Promise<Object>`

Validates file existence, size, and MIME type.

**Returns (success):**
```javascript
{
  valid: true,
  path: string,
  name: string,
  size: number,
  mimeType: string,
  extension: string,
  lastModified: Date
}
```

**Returns (failure):**
```javascript
{
  valid: false,
  error: string
}
```

### `readFileInChunks(filePath, chunkCallback)` -> `Promise<Object>`

Reads a file in chunks, calling the callback for each chunk.

**Callback signature:** `(chunk, chunkIndex, totalChunks) => Promise<void>`

**Returns:**
```javascript
{
  success: true,
  filePath: string,
  fileSize: number,
  totalChunks: number,
  bytesRead: number,
  chunks: Array
}
```

### `createTempFile(data, extension)` -> `Promise<string>`

Creates a temporary file. Returns the file path.

### `cleanupTempFile(filePath)` -> `Promise<boolean>`

Deletes a temporary file. Returns `true` on success, `false` on failure.

### `getActiveTransfers()` -> `Array`

Returns list of active transfers.

### `formatBytes(bytes, decimals?)` -> `string`

Formats bytes to human-readable string (e.g., `1.46 KB`).

### `getStatus()` -> `Object`

Returns manager operational status.

---

## TelegramAdapter

Handles file transfers via Telegram.

### Constructor
```javascript
import { TelegramAdapter } from './src/adapters/telegram-adapter.js';

const adapter = new TelegramAdapter({
  maxFileSize: 50 * 1024 * 1024,  // 50MB (Telegram limit)
  chunkSize: 10 * 1024 * 1024,    // 10MB
  retryAttempts: 3,
  retryDelay: 1000
});
```

### `sendFile(params)` -> `Promise<Object>`

Send a file to a Telegram chat.

**Parameters:**
```javascript
{
  filePath: string,
  chatId: string,           // '-100...' for groups, numeric for private
  caption?: string,
  options?: object
}
```

**Returns:**
```javascript
{
  success: true,
  transferId: string,
  messageId: string,
  fileSize: number,
  duration: number,
  analysis: ContextAnalysis
}
```

### `getTransferStatus(transferId)` -> `Object`

Get status of a specific transfer.

### `getActiveTransfers()` -> `Array`

List all active transfers.

### `getInfo()` -> `Object`

Returns adapter information (name, version, platform, capabilities).

> **Note**: The current implementation simulates file transfer. Real Telegram Bot API integration is planned for a future release.
