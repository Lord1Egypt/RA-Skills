# FXAI Skills（FXAI）

基于 [BNB Chain MCP](https://docs.bnbchain.org/showcase/mcp/skills/) 的 AI 技能：
- 创建 V5 代币（0税/有税，四档分配）
- 创建时可选 **USDT 池子** / **BNB 池子**
- 买入支持 **USDT / BNB**
- 卖出支持按数量或按比例，换回 **USDT / BNB**

**FlapSkill 合约（BSC）**：`0x8f059fEb5f34031EfFA024e9EB8C9968BfFE516a`

---

## 依赖

- 连接 BNB Chain MCP：`npx @bnb-chain/mcp@latest`
- 在 MCP `env` 中配置 `PRIVATE_KEY`

## 安全与外部请求说明

- 本技能发送链上交易时，依赖 BNB Chain MCP 里的 `PRIVATE_KEY` 完成签名；未配置则无法创建、买入或卖出代币
- `scripts/upload-token-meta.js` 会读取你提供的本地图片，并把图片、简介、官网等元数据上传到 Flap API `https://funcs.flap.sh/api/upload`
- `scripts/find-vanity-salt.js` 仅在本地计算代币地址尾号所需的 `_salt`，不会上传私钥

---

## 安装

### Cursor / Claude

```bash
npx skills add flapxai/fxai
```

全局：

```bash
npx skills add flapxai/fxai -g
```

### OpenClaw

```bash
npm i -g clawhub
clawhub install fxai-skills
```

---

## 使用

在对话中输入「FXAI」触发。

### 创建代币示例（BNB池）

```text
FXAI 创建代币
名称：FXAI
符号：FXAI
池子：BNB

税点：3%
税收地址：0x...
营销税点：40%
持币分红税点：30%
回购销毁税点：20%
LP回流税点：10%
最低持币数量：10000

头像：文件位置
官网：https://github.com/
简介：这是一个FXAI的代币测试
```

### 买入示例

```text
FXAI 买入 100 U 0x代币地址
FXAI 买入 0.2 BNB 0x代币地址
```

### 卖出示例

```text
FXAI 卖出 30% 到 USDT 0x代币地址
FXAI 卖出 10000 个代币 到 BNB 0x代币地址
```

完整参数与 ABI 见：`SKILL.md` 与 `references/contract-abi.md`。
