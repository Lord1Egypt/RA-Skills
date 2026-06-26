# backendenc (Backend Data Encryption Toolkit)

[English](#english) | [中文](#中文)

---

## English

### Overview
`backendenc` is a high-security, privacy-first encryption skill pack designed for **Node.js/Backend** OpenClaw environments. It implements a hierarchical key model (MK -> KEK -> DEK) using the native `crypto` module, ensuring robust data protection for server-side agents.

### Key Features
- **Total Multi-tenant Isolation**: Full isolation for users, channels, and their persistent data.
- **Native Performance**:
- **Hierarchical Key Model**:
    - **Master Key (MK)**: Derived from your passphrase via PBKDF2 with a persistent Salt.
    - **KEK (Key Encryption Key)**: Wraps all operational keys, ensuring no keys are stored in plaintext.
    - **DEKs (Data Encryption Keys)**: Scoped keys for specific backend data (Logs, Memory, Cache).
- **Backend Persistence**: Designed to work with filesystem storage or custom database adapters.
- **Security Invariant**: The Master Key is only held in memory and must be re-derived using the passphrase after a server restart.

### Usage
```javascript
import { EncryptionService } from './scripts/encryption-service.js';

await EncryptionService.unlock(userId, channelId, 'passphrase');
// Automatically saves to an isolated path/key
await EncryptionService.save(userId, channelId, 'memory', 'myKey', 'data');
```

---

## 中文

### 概述
`backendenc` 是专为 **Node.js/后端** 环境下的 OpenClaw Agent 设计的高安全性加密技能包。它利用 Node.js 原生的 `crypto` 模块实现了分层密钥模型（MK -> KEK -> DEK），为后端 Agent 提供强有力的数据保护。

### 核心特性
- **全链路数据隔离**：完整支持多用户和多 Channel 的数据以及密钥隔离。
- **原生性能**：
- **分层密钥模型**：
    - **Master Key (MK)**：通过用户口令和持久化盐值（Salt）利用 PBKDF2 算法派生。
    - **Key Encryption Key (KEK)**：封装所有业务密钥，确保没有任何密钥以明文形式存储。
    - **DEKs (Data Encryption Keys)**：针对特定后端数据（日志、记忆、缓存）的独立密钥。
- **后端持久化**：专为文件系统存储或自定义数据库适配器设计。
- **安全一致性**：Master Key 仅驻留内存，服务器重启后必须重新提供口令以进行派生。

### 使用方法
```javascript
import { EncryptionService } from './scripts/encryption-service.js';

await EncryptionService.unlock(userId, channelId, '您的口令');
// 自动保存到隔离路径
await EncryptionService.save(userId, channelId, 'memory', 'myKey', '数据');
```
