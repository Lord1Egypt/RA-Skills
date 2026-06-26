# CryptoFolio Skill for OpenClaw

通过自然语言对话管理你的加密资产，支持多设备云端同步。

## 功能

- 💼 **持仓管理** - 记录和追踪你的加密货币持仓
- 📈 **交易记录** - 买入/卖出自动联动持仓
- 🌱 **理财产品** - 质押、借贷、LP 等理财
- 💸 **流水记录** - 充值、提现、转账
- 🏦 **多账户** - 支持 CEX、DEX、钱包等
- ☁️ **云端同步** - 多设备共享数据
- 📊 **导出报告** - 一键导出 CSV/Excel

---

## 纯网页用户（不用 OpenClaw）

如果你只想用网页版管理资产，不需要安装任何东西：

### 第一步：部署 Cloudflare Worker

#### 1.1 注册/登录

打开 https://dash.cloudflare.com ，用邮箱注册或登录

#### 1.2 创建 Worker

1. 左侧菜单点击 **Workers & Pages**
2. 点击蓝色按钮 **Create**
3. 选择 **Create Worker**
4. 在 Name 输入一个名字，比如 `cryptofolio-api`
5. 点击 **Deploy**（先部署一个空的）

#### 1.3 编辑代码

1. 部署成功后，点击 **Edit code** 按钮
2. 把左边编辑器里的代码**全部删掉**
3. 复制下面这段代码粘贴进去：

```js
const TOKEN = 'REPLACE_WITH_YOUR_SECRET'; // ⚠️ 必须修改！

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const auth = request.headers.get('Authorization');
    const corsHeaders = {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type, Authorization',
    };
    if (request.method === 'OPTIONS') return new Response(null, { headers: corsHeaders });
    if (url.pathname === '/api/health') return Response.json({ ok: true }, { headers: corsHeaders });
    if (auth !== `Bearer ${TOKEN}`) return Response.json({ ok: false, error: 'Unauthorized' }, { status: 401, headers: corsHeaders });
    if (url.pathname === '/api/data' && request.method === 'GET') {
      const data = await env.KV.get('cryptofolio_data', 'json');
      return Response.json({ ok: true, data: data || { accounts: [], positions: [], trades: [], finance: [], transfers: [] } }, { headers: corsHeaders });
    }
    if (url.pathname === '/api/data' && request.method === 'POST') {
      await env.KV.put('cryptofolio_data', JSON.stringify(await request.json()));
      return Response.json({ ok: true }, { headers: corsHeaders });
    }
    return Response.json({ ok: false, error: 'Not found' }, { status: 404, headers: corsHeaders });
  },
};
```

4. **重要**：把第一行的 `REPLACE_WITH_YOUR_SECRET` 改成你自己的密码（至少16位，包含字母数字）
5. 点击右上角 **Deploy** 保存

#### 1.4 创建 KV 存储

1. 点击左上角返回，或左侧菜单点 **Workers & Pages**
2. 左侧菜单点击 **KV**
3. 点击 **Create a namespace**
4. 名字输入 `cryptofolio-data`
5. 点击 **Add**

#### 1.5 绑定 KV 到 Worker

1. 左侧菜单点 **Workers & Pages**
2. 点击你创建的 Worker（`cryptofolio-api`）
3. 点击 **Settings** 标签
4. 往下滚动找到 **Bindings** 区域
5. 点击 **Add**
6. 选择 **KV Namespace**
7. **Variable name** 填：`KV`（必须大写）
8. **KV Namespace** 选择 `cryptofolio-data`
9. 点击 **Deploy** 保存

#### 1.6 记下你的 URL

回到 Worker 概览页面，复制你的 URL，类似：
```
https://cryptofolio-api.你的用户名.workers.dev
```

### 第二步：打开网页使用

1. 访问 https://christinafanxy.github.io/CryptoFolio-Skill/
2. 点击右上角「☁️ 云端同步」按钮
3. 填入你的 Worker URL 和密码（Token）
4. 点击「测试连接」确认成功
5. 点击「保存」，开始使用

---

## OpenClaw 用户

### 第一步：安装 Skill

```bash
mkdir -p ~/.openclaw/workspace/skills
git clone https://github.com/ChristinaFanxy/CryptoFolio-Skill.git ~/.openclaw/workspace/skills/cryptofolio
```

### 第二步：部署 Cloudflare Worker

按照上面「纯网页用户」的 **第一步** 完成 Worker 部署，获得 URL 和密码。

### 第三步：配置云端连接

运行命令（替换成你的 URL 和密码）：

```bash
node ~/.openclaw/workspace/skills/cryptofolio/scripts/cryptofolio.mjs setup \
  --url "https://cryptofolio-api.xxx.workers.dev" \
  --token "你的密码"
```

验证配置：

```bash
node ~/.openclaw/workspace/skills/cryptofolio/scripts/cryptofolio.mjs cloud-status
```

### 第四步：开始使用

在 OpenClaw 中直接对话：

```
我在 Binance 充值了 10000 USDT
我用 5000 USDT 买了 0.1 BTC
显示我的资产
```

---

## 网页端使用

配置云端后，可以在任意设备（电脑、手机）访问：

https://christinafanxy.github.io/CryptoFolio-Skill/

首次使用需要配置云端同步（右上角 ☁️ 按钮），之后数据自动同步。

## 使用示例

| 说法 | 操作 |
|------|------|
| "充值 10000 USDT 到 Binance" | 充值并增加持仓 |
| "在 Binance 买了 0.1 BTC，价格 50000" | 买入 BTC，扣除 USDT |
| "卖出 0.05 BTC，价格 55000" | 卖出 BTC，增加 USDT |
| "质押 2 ETH，APY 4.5%" | 添加理财记录 |
| "显示资产" | 查看总览 |
| "打开可视化界面" | 启动本地 Web 界面 |
| "导出报告" | 导出 CSV |

## 数据存储

- **本地备份**：`~/.openclaw/data/cryptofolio.json`
- **云端存储**：Cloudflare KV（配置后自动同步）

## 默认账户

预设了三个常用账户：
- Binance (CEX)
- OKX (CEX)
- MetaMask (钱包)

可以通过对话添加更多账户。

## CLI 命令

```bash
# 查看资产
node scripts/cryptofolio.mjs overview

# 查看持仓
node scripts/cryptofolio.mjs list-positions

# 云端状态
node scripts/cryptofolio.mjs cloud-status

# 断开云端
node scripts/cryptofolio.mjs cloud-disconnect
```

## License

MIT
