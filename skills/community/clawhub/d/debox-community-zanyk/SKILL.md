---
name: debox-community
description: Manage DeBox communities, DAOs, and NFT groups. Use when you need to verify group membership, check voting/lottery participation, query group info, or validate user eligibility for DAO/NFT communities. Supports group info lookup, member verification, vote/lottery stats, and praise data queries. Ideal for DAO membership verification, NFT community access control, and community analytics.
---

# DeBox Community Management

Manage DeBox communities, verify membership, and analyze community engagement.

## Quick Start

### Configuration

Set the `DEBOX_API_KEY` environment variable:

```bash
export DEBOX_API_KEY="your-api-key"
```

Or add to `~/.openclaw/workspace/debox-community/config.json`:

```json
{
  "apiKey": "your-api-key",
  "defaultGroupId": "optional-default-group-id"
}
```

Get your API Key from https://developer.debox.pro

## Commands

### Personal Data Report (推荐)

查看你的 DeBox 个人数据报告：

```bash
node scripts/debox-community.js profile --user-id "abc123"
```

Returns: 昵称、用户ID、钱包地址、等级、点赞数据

**如何获取 user_id：**
1. 打开 DeBox App
2. 进入个人主页
3. 点击分享，复制链接
4. 链接中的 id 参数就是 user_id

### Group Info

Query group information:

```bash
node scripts/debox-community.js info --url "https://m.debox.pro/group?id=fxi3hqo5"
```

Returns: group name, member count, description, creator.

### Member Verification

Check if a user is in a group:

```bash
node scripts/debox-community.js check-member --wallet "0x2267..." --group-url "https://m.debox.pro/group?id=fxi3hqo5"
```

Returns: boolean membership status.

### User Profile

Get user profile information (nickname, avatar, wallet address):

```bash
node scripts/debox-community.js user-info --user-id "abc123"
```

Returns: user_id, nickname, avatar, wallet address.

**Note:** This API only supports user_id, not wallet address.

### Vote Stats

Query user's voting activity in a group:

```bash
node scripts/debox-community.js vote-stats --wallet "0x2267..." --group-id "fxi3hqo5"
```

Returns: vote count, recent votes.

### Lottery Stats

Query user's lottery participation:

```bash
node scripts/debox-community.js lottery-stats --wallet "0x2267..." --group-id "fxi3hqo5"
```

Returns: lottery count, win history.

### Praise Info

Get user's praise/like data:

```bash
node scripts/debox-community.js praise-info --wallet "0x2267..." --chain-id 1
```

Returns: total likes received, recent praise.

### Comprehensive Verification

Verify user eligibility with multiple criteria:

```bash
node scripts/debox-community.js verify --wallet "0x2267..." --group-url "..." --min-votes 5 --min-lotteries 1
```

Returns: pass/fail status with detailed breakdown.

## API Reference

See [references/api.md](references/api.md) for complete API documentation.

## Use Cases

### DAO Membership Verification

Verify if a user is a DAO member with voting history:

```bash
node scripts/debox-community.js verify --wallet "0xabc..." --group-url "https://m.debox.pro/group?id=dao123" --min-votes 1
```

### NFT Community Access

Verify NFT holder is in community group:

```bash
node scripts/debox-community.js check-member --wallet "0xabc..." --group-url "https://m.debox.pro/group?id=nft456"
```

### Whitelist Generation

Batch verify multiple wallets:

```bash
node scripts/debox-community.js batch-verify --file wallets.txt --group-url "..." --min-votes 3
```

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| `INVALID_API_KEY` | API key missing or invalid | Check configuration |
| `GROUP_NOT_FOUND` | Group ID/URL invalid | Verify group URL format |
| `USER_NOT_FOUND` | Wallet address not registered | Confirm user has DeBox account |
| `RATE_LIMIT` | Too many requests | Wait and retry |

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `DEBOX_API_KEY` | Yes | Your DeBox API key |
| `DEBOX_DEFAULT_GROUP` | No | Default group ID for commands |