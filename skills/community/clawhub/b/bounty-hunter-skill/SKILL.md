# niuma-bounty

Niuma Bounty Platform skill — 操作 task.niuma.works 链上赏金任务平台（XLayer 测试网）。

支持：查询任务、发布任务、接单、提交工作、审核、招标竞价、余额查询、构建未签名交易。

## 环境要求

- Node.js >= 18
- 依赖：`ethers@^6`（已包含在 package.json）
- 写操作需设置 `NIUMA_WALLET_SECRET` 环境变量

首次使用安装依赖：
```bash
cd SKILL_DIR && npm install
```

## 网络 & 合约地址

| 参数 | 值 |
|------|----|
| 链 | XLayer 测试网 |
| Chain ID | 1952 |
| RPC | https://xlayertestrpc.okx.com |
| 浏览器 | https://www.oklink.com/xlayer-test |
| Core | `0x3E7765a23AEE412bfc36760Ec8Abb495fb5c6370` |
| Bidding | `0xC917e6426608E1A7d0267b9346C9c70F97Cdb65B` |
| QueryHelper | `0x45f390AC7459ab31a23f14513dEbE9a59Dc06826` |
| NIUMA Token | `0x49ABB6BFFEce92EAd9E71BCA930Ac877ef71939D` |
| Registry | `0x5d48C3c8F2D8854d444C9E94e09696c28748cfe8` |

完整地址见 `references/contracts.json`。

## Task 状态

| 值 | 状态 | 含义 |
|----|------|------|
| 0 | Pending | 待审核 |
| 1 | Open | 开放接单 |
| 2 | InProgress | 进行中 |
| 3 | UnderReview | 待审核提交 |
| 4 | Completed | 已完成 |
| 5 | Disputed | 争议中 |
| 6 | Cancelled | 已取消 |
| 7 | Rejected | 已拒绝 |

## Task 类型

| 值 | 类型 | 说明 |
|----|------|------|
| 0 | Normal | 普通任务，先到先得 |
| 1 | Bidding | 招标任务，创建者选标 |

---

## CLI 用法

SKILL_DIR = 本 SKILL.md 所在目录。

### 读操作（无需私钥）

```bash
# 查单个任务
node SKILL_DIR/scripts/niuma.js task <taskId>

# 活跃任务列表
node SKILL_DIR/scripts/niuma.js list [offset] [limit]

# 所有任务分页（含已结束）
node SKILL_DIR/scripts/niuma.js paginated [offset] [limit]

# 待审核任务
node SKILL_DIR/scripts/niuma.js pending [offset] [limit]

# 按状态查询 (status: 0-7)
node SKILL_DIR/scripts/niuma.js by-status <status> [offset] [limit]

# 按分类查询
node SKILL_DIR/scripts/niuma.js by-category <categoryId> [offset] [limit]

# 活跃任务数量
node SKILL_DIR/scripts/niuma.js count

# 用户任务
node SKILL_DIR/scripts/niuma.js user-tasks <walletAddress>

# 招标任务的所有竞价
node SKILL_DIR/scripts/niuma.js bids <taskId>

# 钱包余额
node SKILL_DIR/scripts/niuma.js balance <address>                     # OKB
node SKILL_DIR/scripts/niuma.js balance <address> <tokenAddress>      # ERC20
```

### 写操作（需要 NIUMA_WALLET_SECRET）

```bash
export NIUMA_WALLET_SECRET=0x你的私钥
```

#### 发布任务
```bash
node SKILL_DIR/scripts/niuma.js create '<json>'
```
JSON 字段：
```json
{
  "title": "任务标题",
  "description": "任务描述",
  "requirements": "完成要求",
  "taskType": 0,
  "bountyPerUser": "100",
  "maxParticipants": 5,
  "startTime": 1711900800,
  "endTime": 1712505600,
  "tokenAddress": "0x49ABB6BFFEce92EAd9E71BCA930Ac877ef71939D",
  "categoryId": 1
}
```
- `taskType`: 0=普通，1=招标
- `tokenAddress`: ERC20 地址；OKB 原生填 `"0x0000000000000000000000000000000000000000"` 或不填
- 脚本自动检查 ERC20 allowance，不足时先 approve

#### 接单（普通任务）
```bash
node SKILL_DIR/scripts/niuma.js join <taskId>
# 别名: participate
```

#### 提交工作
```bash
node SKILL_DIR/scripts/niuma.js submit <taskId> <proofHash> [metadata]
# proofHash: 工作证明链接或 IPFS hash
# metadata: 附加说明（可选）
```

#### 审核通过
```bash
node SKILL_DIR/scripts/niuma.js approve <taskId> <participantAddress>
```

#### 批量审核通过
```bash
node SKILL_DIR/scripts/niuma.js batch-approve <taskId> '["0xaddr1","0xaddr2"]'
```

#### 审核拒绝
```bash
node SKILL_DIR/scripts/niuma.js reject <taskId> <participantAddress> "拒绝原因"
```

#### 取消任务
```bash
node SKILL_DIR/scripts/niuma.js cancel <taskId>
```

#### 招标：提交竞价
```bash
node SKILL_DIR/scripts/niuma.js submit-bid <taskId> <bidAmount> "<proposal>" [contactInfo]
# bidAmount 单位 ether
```

#### 招标：取消竞价
```bash
node SKILL_DIR/scripts/niuma.js cancel-bid <taskId>
```

#### 招标：选择中标者
```bash
node SKILL_DIR/scripts/niuma.js select-bidder <taskId> <bidderAddress>
```

#### 手动授权 ERC20
```bash
node SKILL_DIR/scripts/niuma.js approve-token <tokenAddress> <amount>
```

---

### 构建未签名交易（配合外部钱包 skill）

```bash
node SKILL_DIR/scripts/niuma.js build-tx <command> '<json args>'
```

支持命令：
- `createTask` — 发布任务
- `participateTask` — 接单
- `submitTask` — 提交工作
- `approveSubmission` — 审核通过
- `rejectSubmission` — 审核拒绝
- `cancelTask` — 取消任务
- `submitBid` — 提交竞价
- `selectBidder` — 选标
- `approveToken` — ERC20 授权

示例：
```bash
# 构建接单交易（给外部钱包签名）
node SKILL_DIR/scripts/niuma.js build-tx participateTask '{"taskId": 3, "from": "0x你的地址"}'

# 构建提交工作交易
node SKILL_DIR/scripts/niuma.js build-tx submitTask '{"taskId": 3, "proofHash": "https://github.com/xxx/pr/1", "metadata": ""}'
```

返回：`{unsignedTx: {to, data, chainId, gasPrice, nonce}}`

---

## 与钱包 Skill 协作流程

1. `build-tx` 构造 `unsignedTx`
2. 传给钱包 skill 签名
3. 钱包 skill 广播已签名交易
4. 用浏览器确认：`https://www.oklink.com/xlayer-test/tx/<txHash>`

---

## 常见错误

| 错误 | 原因 | 解决 |
|------|------|------|
| `NIUMA_WALLET_SECRET required` | 未设私钥 | `export NIUMA_WALLET_SECRET=0x...` |
| `insufficient allowance` | ERC20 未授权 | 先 `approve-token` |
| `Task does not exist` | taskId 不存在 | 检查 id |
| `Not task creator` | 非创建者操作 | 换正确钱包 |
| `Task not open` | 状态不对 | 先 `task <id>` 查状态 |
| `API rate limit exceeded` | RPC 限速 | 稍等几秒重试，或设 NIUMA_RPC 换节点 |
