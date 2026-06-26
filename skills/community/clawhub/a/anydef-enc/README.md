# anydef-enc (Agent Data Encryption Toolkit)

[English](#english) | [中文](#中文)

---

## English

### Overview
`anydef-enc` is a high-security, privacy-first encryption skill pack for OpenClaw agents. It provides enterprise-grade data protection using a hierarchical key model (MK -> KEK -> DEK) while remaining **entirely local and air-gapped**. No data or keys ever leave the browser.

### Key Features
- **Zero Knowledge Architecture**: Keys are derived from your passphrase and never stored in cleartext.
- **Hierarchical Key Model**:
    - **Master Key (MK)**: Derived via PBKDF2 from your passphrase (100k rounds + persistent Salt).
    - **Key Encryption Key (KEK)**: Wraps all operational keys.
    - **Data Encryption Keys (DEKs)**: Scoped keys for specific data categories (Memory, History, Files).
- **Reboot Persistence**: By utilizing a persistent Salt, the same passphrase will always derive the same Master Key, ensuring your data remains accessible after restarts.
- **Zero Network Usage**: Operates exclusively via the browser's `SubtleCrypto` API. No external API calls (ClawHub compliant).
- **Selective Scopes**: Users can define exactly which data (files, memory, or logs) to protect.

### Quick Start
1.  **Install**: Add `anydef-enc` to your OpenClaw agent scripts.
2.  **Unlock**: On initial run or after a reboot, call `EncryptionService.unlock('your-secure-passphrase')`.
3.  **Use**: The service will automatically manage your keys. Use `EncryptionService.encrypt(scope, data)` to protect your assets.

### Security Warning
**Do not lose your passphrase.** Because this is a zero-knowledge system, there is no "password reset" functionality. If the passphrase is lost, all encrypted data is permanently inaccessible.
**Only support one agent one user .**

---

## 中文

### 概述
`anydef-enc` 是一个为 OpenClaw Agent 设计的高安全性、隐私优先的加密技能包。它通过分层密钥模型（MK -> KEK -> DEK）提供企业级的数据保护，同时保持**完全本地化运行**。任何数据或密钥都不会离开浏览器，确保极致的隐私性。

### 核心特性
- **零知识架构**：所有密钥均由您的口令派生，绝不以明文形式存储。
- **分层密钥模型**：
    - **Master Key (MK)**：由用户口令通过 PBKDF2 算法（10万次迭代 + 持久化盐值）派生。
    - **Key Encryption Key (KEK)**：被 MK 加密，用于保护所有业务密钥。
    - **Data Encryption Keys (DEKs)**：针对特定数据类别（内存、历史记录、文件）的独立密钥。
- **重启持久化**：通过使用持久化盐值（Salt），相同的口令在重启后将始终派生出相同的根密钥，确保您的数据在系统重启后依然可以访问。
- **零网络占用**：完全通过浏览器内置的 `SubtleCrypto` API 运行。没有任何外部 API 调用，符合 ClawHub 的严格合规审计。
- **选择性加密范围**：用户可以精确设置需要保护的数据范围（如：仅保护上传文件或仅保护 Agent 记忆）。

### 快速上手
1.  **安装**：将 `anydef-enc` 技能包添加到您的 OpenClaw Agent 脚本目录。
2.  **解锁**：在首次运行或每次重启后，调用 `EncryptionService.unlock('您的安全口令')`。
3.  **使用**：服务会自动管理密钥。调用 `EncryptionService.encrypt(scope, data)` 即可加密您的关键资产。

### 安全警告
**请务必牢记您的口令。** 由于采用零知识系统设计，这里没有“重置密码”功能。如果您丢失了口令，所有已加密的数据将永久无法找回。
**当前版本只支持单agent单用户场景 。**单agent多用户场景在计划中。
