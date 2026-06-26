[🇺🇸 English](#english) · [🇨🇳 中文](#chinese)

---

<a name="english"></a>

# 🚀 DefiLlama Data Aggregator

> **Version**: 1.0.3
> **Update Date**: 2026-03-31
> **Description**: Professional DefiLlama data aggregator with security validation - DeFi TVL, protocols, chains, and yields data
> **Maintainer**: [AntalphaAI](https://github.com/AntalphaAI)

---

## 📊 Overview

DefiLlama Data Aggregator is a professional-grade command-line tool that provides unified access to DefiLlama's comprehensive DeFi data. It supports querying Total Value Locked (TVL), protocol data, chain statistics, and yield pool information with built-in security validation and error handling.

---

## 🎯 Features

- ✅ **DeFi TVL** - Total DeFi TVL and chain-level TVL
- ✅ **Protocol Data** - Protocol details, listings, and rankings
- ✅ **Chain Data** - Individual chain TVL and statistics
- ✅ **Yield Pools** - Yield rate queries and filtering
- ✅ **Health Monitoring** - API health status monitoring
- ✅ **Security Validation** - Input sanitization and error handling
- ✅ **Flexible Output** - Pretty/Table/JSON/CSV formats

---

## 📦 Installation

### Install via OpenClaw (Recommended)

```bash
openclaw skill install https://github.com/AntalphaAI/defillama-data-aggregator
```

### Prerequisites

- Node.js >= 16.0.0
- npm (comes with Node.js)

### Install Dependencies (Manual)

```bash
cd defillama-data-aggregator
npm install
```

### Create Symbolic Link (Optional)

```bash
npm link
```

This creates a global `defillama-data` command that you can use from anywhere.

---

## 🚀 Quick Start

### Basic Usage

```bash
# View version
defillama-data --version

# Get total DeFi TVL
defillama-data defillama tvl

# Get protocol TVL
defillama-data defillama protocol -n aave

# Get protocol rankings
defillama-data defillama protocols --limit 10 --sort tvl -f table

# Find high-yield pools
defillama-data defillama yields --min-apy 10 --limit 20 -f table

# Check API health
defillama-data health

# View system status
defillama-data status
```

---

## 📖 Commands

### 1. Get Total DeFi TVL

Get the total value locked across all DeFi protocols.

```bash
defillama-data defillama tvl [options]
```

**Options**:
- `-f, --format <type>`: Output format (json, table, csv, pretty) - Default: pretty

**Example**:
```bash
defillama-data defillama tvl
defillama-data defillama tvl -f json | jq '.totalTvl'
```

**Response**:
```json
{
  "totalTvl": 94518602394.26,
  "chains": [...],
  "timestamp": "2026-03-27T09:00:00.000Z"
}
```

---

### 2. Get Protocol TVL

Get TVL for a specific protocol.

```bash
defillama-data defillama protocol -n <name> [options]
```

**Required Options**:
- `-n, --name <name>`: Protocol name (e.g., aave, uniswap, compound)

**Options**:
- `-f, --format <type>`: Output format (json, table, csv, pretty) - Default: pretty

**Example**:
```bash
defillama-data defillama protocol -n aave
defillama-data defillama protocol -n uniswap -f json
```

**Validation Rules**:
- Only alphanumeric characters and hyphens allowed
- Length: 1-50 characters
- Automatically converted to lowercase

**Valid Examples**: `aave`, `uniswap-v3`, `compound-protocol`
**Invalid Examples**: `aave<script>`, `uni/swap`, `aave&x`

---

### 3. Get All Protocols

Get a list of all protocols with filtering and sorting.

```bash
defillama-data defillama protocols [options]
```

**Options**:
- `-c, --category <name>`: Filter by category (e.g., lending, dex)
- `--min-tvl <amount>`: Minimum TVL in USD
- `--limit <number>`: Limit results (1-500)
- `--sort <field>`: Sort by field (tvl) - Default: tvl
- `-f, --format <type>`: Output format (json, table, csv, pretty) - Default: pretty

**Example**:
```bash
# Get all protocols
defillama-data defillama protocols

# Sort by TVL, top 20
defillama-data defillama protocols --sort tvl --limit 20

# Filter lending protocols
defillama-data defillama protocols -c lending --min-tvl 100000000

# Combined filters
defillama-data defillama protocols -c lending --min-tvl 100000000 --limit 50 --sort tvl -f table
```

---

### 4. Get Chain TVL

Get TVL for a specific blockchain.

```bash
defillama-data defillama chain -n <name> [options]
```

**Required Options**:
- `-n, --name <name>`: Chain name (e.g., ethereum, solana, polygon)

**Options**:
- `-f, --format <type>`: Output format (json, table, csv, pretty) - Default: pretty

**Example**:
```bash
defillama-data defillama chain -n ethereum
defillama-data defillama chain -n solana -f json
```

---

### 5. Get Yield Pools

Get yield pool information with filtering.

```bash
defillama-data defillama yields [options]
```

**Options**:
- `--min-apy <number>`: Minimum APY percentage (0-1000)
- `--min-tvl <number>`: Minimum TVL in USD
- `--chain <name>`: Filter by chain name (e.g., ethereum, arbitrum)
- `--stablecoin`: Filter stablecoin pools only
- `--limit <number>`: Limit results (1-500)
- `-f, --format <type>`: Output format (json, table, csv, pretty) - Default: pretty

**Example**:
```bash
# Get all yield pools
defillama-data defillama yields

# High APY pools (APY > 10%)
defillama-data defillama yields --min-apy 10

# Ethereum high-yield pools
defillama-data defillama yields --chain ethereum --min-apy 5

# Combined filters
defillama-data defillama yields --min-apy 10 --chain ethereum --min-tvl 1000000 --limit 20 -f table
```

---

### 6. Health Check

Check API health status.

```bash
defillama-data health [options]
```

**Options**:
- `-q, --quiet`: Quiet mode (summary only)
- `--timeout <ms>`: Request timeout in milliseconds - Default: 5000

**Example**:
```bash
# Full health check
defillama-data health

# Quiet mode
defillama-data health --quiet

# Custom timeout
defillama-data health --timeout 10000
```

---

### 7. System Status

Display system status and available platforms.

```bash
defillama-data status
```

---

## 📤 Output Formats

All commands support multiple output formats:

### Pretty (Default)
Human-readable format with colored output.
```bash
defillama-data defillama tvl -f pretty
```

### Table
Structured table format for data comparison.
```bash
defillama-data defillama protocols --limit 10 -f table
```

### JSON
Machine-readable format for scripts and automation.
```bash
defillama-data defillama tvl -f json | jq '.totalTvl'
```

### CSV
Spreadsheet-friendly format for data export and analysis.
```bash
defillama-data defillama protocols --limit 50 -f csv > protocols.csv
```

---

## 🔒 Security Features

### Input Validation

All user inputs are validated and sanitized:

| Input Type | Validation Rules | Length Limit |
|-----------|-----------------|--------------|
| Protocol Name | Alphanumeric + hyphens only | 1-50 characters |
| Chain Name | Alphanumeric + spaces + hyphens | 1-50 characters |
| Category Name | Alphanumeric + spaces + hyphens | 1-50 characters |
| Limit | 1-500 | - |
| Min APY | 0-1000% | - |
| Min TVL | ≥ 0 | - |

### Error Handling

- API errors (4xx, 5xx) with status codes
- Network errors (timeout, connection refused)
- Validation errors with helpful messages
- Sanitized error messages to prevent information leakage

---

## 🛠️ Configuration

### Setup Configuration File (Optional)

```bash
# Copy example configuration
cp config/keys.example.js config/keys.js
```

### Configuration Example

```javascript
// config/keys.js
module.exports = {
  defillama: {
    baseUrl: 'https://api.llama.fi'
  },
  settings: {
    defaultCacheDuration: 300,  // Cache duration in seconds
    timeout: 30000,             // Request timeout in milliseconds
    maxRetries: 3,              // Maximum retry attempts
    retryDelay: 1000,           // Retry delay in milliseconds
    debug: process.env.DEBUG === 'true'  // Enable debug logging
  }
};
```

---

## 💡 Usage Examples

### Monitor Lending Protocols

```bash
# Get top 10 lending protocols by TVL
defillama-data defillama protocols -c lending --limit 10 --sort tvl -f table
```

### Find High-Yield Pools

```bash
# Find high-yield pools on Ethereum with APY > 10%
defillama-data defillama yields --chain ethereum --min-apy 10 --min-tvl 1000000 --limit 20 -f table
```

### Compare Chain TVL

```bash
# Compare TVL across multiple chains
for chain in ethereum solana polygon arbitrum avalanche; do
  echo "=== $chain ==="
  defillama-data defillama chain -n $chain -f json | jq '.tvl'
done
```

### Export Data for Analysis

```bash
# Export protocols to CSV
defillama-data defillama protocols --limit 100 -f csv > protocols.csv

# Export yields to CSV
defillama-data defillama yields --limit 100 -f csv > yields.csv
```

---

## 🧪 Testing

Run the test script to verify functionality:

```bash
node scripts/test.js
```

This will test:
- Version check
- Health check
- TVL query
- Protocol query
- Sorting functionality
- Input validation

---

## 📄 License

MIT License - Copyright (c) 2026 Antalpha

---

<a name="chinese"></a>

# 🚀 DefiLlama 数据聚合器

> **版本**: 1.0.3
> **更新日期**: 2026-03-31
> **描述**: 专业的 DefiLlama 数据聚合工具，内置安全验证 —— 提供 DeFi TVL、协议、链和收益池数据查询
> **维护方**: [AntalphaAI](https://github.com/AntalphaAI)

---

## 📊 概述

DefiLlama 数据聚合器是一款专业级命令行工具，提供对 DefiLlama 全面 DeFi 数据的统一访问接口。支持查询总锁仓量（TVL）、协议数据、链统计信息和收益池数据，内置安全验证与错误处理机制。

---

## 🎯 功能特性

- ✅ **DeFi TVL** — 查询全网 DeFi 总锁仓量及各链锁仓量
- ✅ **协议数据** — 协议详情、列表及排名
- ✅ **链数据** — 各公链 TVL 及统计信息
- ✅ **收益池** — 收益率查询与筛选
- ✅ **健康监控** — API 健康状态监控
- ✅ **安全验证** — 输入清洗与错误处理
- ✅ **多种输出格式** — 支持 Pretty / Table / JSON / CSV

---

## 📦 安装

### 通过 OpenClaw 安装（推荐）

```bash
openclaw skill install https://github.com/AntalphaAI/defillama-data-aggregator
```

### 环境要求

- Node.js >= 16.0.0
- npm（随 Node.js 一起安装）

### 手动安装依赖

```bash
cd defillama-data-aggregator
npm install
```

### 创建全局快捷命令（可选）

```bash
npm link
```

执行后可在任意目录使用 `defillama-data` 命令。

---

## 🚀 快速开始

### 基础用法

```bash
# 查看版本
defillama-data --version

# 获取 DeFi 总 TVL
defillama-data defillama tvl

# 查询协议 TVL
defillama-data defillama protocol -n aave

# 协议排名（前10，按 TVL 排序，表格格式）
defillama-data defillama protocols --limit 10 --sort tvl -f table

# 寻找高收益池
defillama-data defillama yields --min-apy 10 --limit 20 -f table

# 检查 API 健康状态
defillama-data health

# 查看系统状态
defillama-data status
```

---

## 📖 命令说明

### 1. 获取 DeFi 总 TVL

查询全网所有 DeFi 协议的总锁仓量。

```bash
defillama-data defillama tvl [选项]
```

**选项**：
- `-f, --format <type>`：输出格式（json、table、csv、pretty），默认：pretty

**示例**：
```bash
defillama-data defillama tvl
defillama-data defillama tvl -f json | jq '.totalTvl'
```

**返回示例**：
```json
{
  "totalTvl": 94518602394.26,
  "chains": [...],
  "timestamp": "2026-03-27T09:00:00.000Z"
}
```

---

### 2. 查询协议 TVL

获取指定协议的锁仓量。

```bash
defillama-data defillama protocol -n <协议名> [选项]
```

**必填选项**：
- `-n, --name <name>`：协议名称（如 aave、uniswap、compound）

**选项**：
- `-f, --format <type>`：输出格式，默认：pretty

**示例**：
```bash
defillama-data defillama protocol -n aave
defillama-data defillama protocol -n uniswap -f json
```

**验证规则**：
- 仅允许字母、数字和连字符
- 长度：1-50 个字符
- 自动转换为小写

**有效示例**：`aave`、`uniswap-v3`、`compound-protocol`
**无效示例**：`aave<script>`、`uni/swap`、`aave&x`

---

### 3. 获取所有协议列表

获取协议列表，支持筛选和排序。

```bash
defillama-data defillama protocols [选项]
```

**选项**：
- `-c, --category <name>`：按类别筛选（如 lending、dex）
- `--min-tvl <amount>`：最低 TVL（美元）
- `--limit <number>`：结果数量限制（1-500）
- `--sort <field>`：排序字段（tvl），默认：tvl
- `-f, --format <type>`：输出格式，默认：pretty

**示例**：
```bash
# 获取所有协议
defillama-data defillama protocols

# 按 TVL 排序，取前 20
defillama-data defillama protocols --sort tvl --limit 20

# 筛选借贷协议
defillama-data defillama protocols -c lending --min-tvl 100000000

# 组合筛选
defillama-data defillama protocols -c lending --min-tvl 100000000 --limit 50 --sort tvl -f table
```

---

### 4. 查询链 TVL

获取指定区块链的锁仓量。

```bash
defillama-data defillama chain -n <链名> [选项]
```

**必填选项**：
- `-n, --name <name>`：链名称（如 ethereum、solana、polygon）

**示例**：
```bash
defillama-data defillama chain -n ethereum
defillama-data defillama chain -n solana -f json
```

---

### 5. 查询收益池

获取收益池信息，支持多维筛选。

```bash
defillama-data defillama yields [选项]
```

**选项**：
- `--min-apy <number>`：最低 APY 百分比（0-1000）
- `--min-tvl <number>`：最低 TVL（美元）
- `--chain <name>`：按链筛选（如 ethereum、arbitrum）
- `--stablecoin`：仅显示稳定币池
- `--limit <number>`：结果数量限制（1-500）
- `-f, --format <type>`：输出格式，默认：pretty

**示例**：
```bash
# 获取所有收益池
defillama-data defillama yields

# 高 APY 收益池（APY > 10%）
defillama-data defillama yields --min-apy 10

# 以太坊高收益池
defillama-data defillama yields --chain ethereum --min-apy 5

# 组合筛选
defillama-data defillama yields --min-apy 10 --chain ethereum --min-tvl 1000000 --limit 20 -f table
```

---

### 6. 健康检查

检查 API 健康状态。

```bash
defillama-data health [选项]
```

**选项**：
- `-q, --quiet`：安静模式（仅显示摘要）
- `--timeout <ms>`：请求超时时间（毫秒），默认：5000

**示例**：
```bash
# 完整健康检查
defillama-data health

# 安静模式
defillama-data health --quiet

# 自定义超时
defillama-data health --timeout 10000
```

---

### 7. 系统状态

显示系统状态及可用平台信息。

```bash
defillama-data status
```

---

## 📤 输出格式

所有命令均支持以下输出格式：

### Pretty（默认）
适合人工阅读的彩色输出格式。
```bash
defillama-data defillama tvl -f pretty
```

### Table（表格）
结构化表格格式，便于数据对比。
```bash
defillama-data defillama protocols --limit 10 -f table
```

### JSON
适合脚本和自动化处理的机器可读格式。
```bash
defillama-data defillama tvl -f json | jq '.totalTvl'
```

### CSV
适合导出到电子表格进行数据分析。
```bash
defillama-data defillama protocols --limit 50 -f csv > protocols.csv
```

---

## 🔒 安全特性

### 输入验证

所有用户输入均经过验证和清洗：

| 输入类型 | 验证规则 | 长度限制 |
|---------|---------|---------|
| 协议名称 | 仅字母、数字和连字符 | 1-50 字符 |
| 链名称 | 字母、数字、空格和连字符 | 1-50 字符 |
| 类别名称 | 字母、数字、空格和连字符 | 1-50 字符 |
| 数量限制 | 1-500 | - |
| 最低 APY | 0-1000% | - |
| 最低 TVL | ≥ 0 | - |

### 错误处理

- API 错误（4xx、5xx）附带状态码
- 网络错误（超时、连接拒绝）
- 带提示信息的验证错误
- 净化错误消息，防止信息泄露

---

## 🛠️ 配置

### 配置文件设置（可选）

```bash
# 复制示例配置文件
cp config/keys.example.js config/keys.js
```

### 配置示例

```javascript
// config/keys.js
module.exports = {
  defillama: {
    baseUrl: 'https://api.llama.fi'
  },
  settings: {
    defaultCacheDuration: 300,  // 缓存时长（秒）
    timeout: 30000,             // 请求超时时间（毫秒）
    maxRetries: 3,              // 最大重试次数
    retryDelay: 1000,           // 重试间隔（毫秒）
    debug: process.env.DEBUG === 'true'  // 启用调试日志
  }
};
```

---

## 💡 使用示例

### 监控借贷协议

```bash
# 获取 TVL 前 10 的借贷协议
defillama-data defillama protocols -c lending --limit 10 --sort tvl -f table
```

### 寻找高收益池

```bash
# 寻找以太坊上 APY > 10% 的高收益池
defillama-data defillama yields --chain ethereum --min-apy 10 --min-tvl 1000000 --limit 20 -f table
```

### 对比各链 TVL

```bash
# 对比多条链的 TVL
for chain in ethereum solana polygon arbitrum avalanche; do
  echo "=== $chain ==="
  defillama-data defillama chain -n $chain -f json | jq '.tvl'
done
```

### 导出数据分析

```bash
# 导出协议数据为 CSV
defillama-data defillama protocols --limit 100 -f csv > protocols.csv

# 导出收益池数据为 CSV
defillama-data defillama yields --limit 100 -f csv > yields.csv
```

---

## 🧪 测试

运行测试脚本验证功能：

```bash
node scripts/test.js
```

测试内容包括：
- 版本检查
- 健康检查
- TVL 查询
- 协议查询
- 排序功能
- 输入验证

---

## 📄 许可证

MIT License - Copyright (c) 2026 Antalpha
