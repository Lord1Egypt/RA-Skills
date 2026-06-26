---
name: 接口盒子 API
slug: apihz
version: 1.0.0
description: 409+ 企业级 API 接口 — 天气/地震/IP 归属地/临时邮箱/翻译等，稳定高效
metadata: {"emoji": "📦", "requires": {"bins": []}}
---

# 接口盒子 API Skill

> 409+ 企业级 API 接口 - 稳定、高效、易用

**版本:** v1.0.8  
**状态:** ✅ 生产就绪  
**更新:** 官方接口线路优化 (域名/IP/VIP 三线容错)

---

## 🚀 快速开始

### 1. 获取认证信息

访问：https://www.apihz.cn/?shareid=10013679

注册后在用户后台获取：
- **开发者 ID** (数字)
- **通讯 Key** (字符串)

### 2. 配置认证

运行初始化向导：
```bash
node skills/apihz/scripts/init-wizard.js
```

按提示填入 ID、KEY 和预留信息，自动验证并配置动态密钥。

**动态密钥 (推荐):**
- 开启动态密钥后，每次调用接口需验证 `dkey` 参数
- `dkey = md5(预留信息 + 动态参数)`
- 动态参数通过【动态参数获取】接口获取，有效期 10 秒

### 3. 开始使用

**自动同步 API 列表:**
```bash
node skills/apihz/scripts/init-wizard.js
```

首次配置后自动执行:
1. ✅ 验证账号
2. ✅ 获取 41 个 API 分类
3. ✅ 遍历所有分类，获取全部 API 接口
4. ✅ 缓存到 `skills/apihz/cache/apis.json`

**交互式调用 (推荐):**
```bash
node skills/apihz/scripts/call-api.js
```

交互式调用流程:
1. 自动加载配置和 API 缓存
2. 选择 API 分类 (41 个分类可选)
3. 选择具体 API 接口
4. 按提示输入参数
5. 查看调用结果

**代码调用:**
```javascript
const { ApiHzClient } = require('./skills/apihz/src/client-enhanced.js');

const client = new ApiHzClient({
  id: '你的 ID',
  key: '你的 KEY',
  baseUrl: 'https://cn.apihz.cn'
});

// 调用任意 API
const result = await client.request('/api/ajax/ajax.php', {
  type: '6',      // Ping 测试
  words1: 'qq.com'
});
```

---

## 📦 核心 API (免费示例)

| API | 说明 | 调用方法 |
|-----|------|---------|
| 时间戳 | 北京时间 | `client.timestamp()` |
| Ping 测试 | 网络延迟测试 | `client.ping('qq.com')` |
| ICP 备案 | 企业备案查询 | `client.icp('baidu.com')` |
| IP 归属地 | 全球 IP 定位 | `client.ipLocation('8.8.8.8')` |
| 地震数据 | 最新地震数据 | `client.earthquake()` |
| 翻译服务 | 多语言翻译 | `client.translate('hello', 'en', 'zh')` |
| 临时邮箱 | 创建临时邮箱 | `client.tempEmailCreate()` |
| 汇率查询 | 货币汇率 | `client.exchangeRate()` |

**完整 API 列表:** 运行 `init-wizard.js` 自动同步后查看 `cache/apis.json`

---

## 💎 会员说明

| 等级 | 价格 | 频次 | 推荐 |
|------|------|------|------|
| 注册 | 免费 | 10/分钟 | ⭐ 个人 |
| 彩钻 | ¥30/月 | 310/分钟 | ⭐⭐ 企业 |
| 炫钻 | ¥50/月 | 1010/分钟 | ⭐⭐⭐ 大型 |

**彩钻特权:** 专属集群、VIP 线路、CDN 加速、智能故障切换

---

## 🎰 每日签到

**手动配置:** 技能本身不自动创建系统 cron 任务，需要手动配置

**自动签到脚本:**
```bash
# 添加到 crontab (每天 00:02 执行)
crontab -e

# 添加以下行 (替换路径)
2 0 * * * OPENCLAW_WORKSPACE=/your/path node /your/path/skills/apihz/scripts/auto-checkin.js
```

**奖励:** 抽奖形式 (1-5 盟点/会员天数)

**奖项:**
- 五等奖：1-5 盟点 (高概率)
- 四等奖：1 天钻石会员
- 三等奖：7 天钻石会员
- 二等奖：30 天钻石会员
- 一等奖：扩展频次 +5 (永久)

---

## 📁 文件结构

```
skills/apihz/
├── SKILL.md              # 本文件
├── src/
│   ├── client.js         # 基础客户端
│   ├── client-enhanced.js # 增强客户端 (支持 HTML 解析)
│   └── auth.js           # 认证管理 (带故障切换)
├── scripts/
│   ├── init-wizard.js    # 初始化向导
│   ├── auto-checkin.js   # 自动签到
│   └── call-api.js       # 交互式调用
└── .credentials/
    └── apihz.txt         # 认证信息 (gitignore)
```

## 🔧 高级配置

### 环境变量

```bash
# 自定义工作区路径 (可选)
export OPENCLAW_WORKSPACE=/your/custom/path

# 自定义 API 列表节点 (可选，默认官方 CDN)
export APIHZ_LIST_URL=http://your-preferred-node/api/xitong/apilist.php

# 主 API 域名 (可选)
# 域名接口：https://cn.apihz.cn (默认，自动分发)
# VIP 线路：https://vip.apihz.cn (超高稳定，需购买)
export APIHZ_BASE_URL=https://cn.apihz.cn

# 动态密钥预留信息 (可选，开启后增强安全性)
export APIHZ_DMSG=your_secret_message
```

### 接口线路说明 (适用于所有 API)

**官方说明:** https://www.apihz.cn/template/miuu/getpost.php

> 💡 **说明:** 所有 409+ 个 API 接口均支持以下三种线路类型，调用格式相同，仅域名/IP 不同。

| 线路类型 | 地址示例 | 特点 | 推荐 |
|---------|---------|------|------|
| 域名接口 | `https://cn.apihz.cn/api/...` | 自动分发，CC 防火墙适中 | ⭐⭐⭐ 默认 |
| 集群 IP | `http://101.35.2.25/api/...` | 速度快，CC 防火墙严格 | ⭐⭐ 备用 |
| VIP 线路 | `https://vip.apihz.cn/api/...` | 超高稳定，CC 防火墙宽松 | ⭐⭐⭐⭐ 企业 |

**获取最优 IP:** 访问 `https://api.apihz.cn/getapi.php` 获取当前最优 IP 地址

**示例 (天气 API):**
```bash
# 域名接口
GET https://cn.apihz.cn/api/tianqi/tqyb.php?id=你的 ID&key=你的 KEY&sheng=安徽&place=芜湖

# 集群 IP 接口
GET http://101.35.2.25/api/tianqi/tqyb.php?id=你的 ID&key=你的 KEY&sheng=安徽&place=芜湖

# VIP 线路
GET https://vip.apihz.cn/api/tianqi/tqyb.php?id=你的 ID&key=你的 KEY&sheng=安徽&place=芜湖
```

### 动态密钥 (dkey) 配置

**第一步：设置预留信息**
```bash
# 在用户后台设置预留信息参数，开启动态密钥开关
# 然后配置到环境变量或凭证文件
export APIHZ_DMSG=your_secret_message
```

**第二步：代码配置**
```javascript
const client = new ApiHzClient({
  id: '你的 ID',
  key: '你的 KEY',
  dmsg: 'your_secret_message',  // 预留信息
  baseUrl: 'https://cn.apihz.cn',
  timeout: 10000,
  retryCount: 2
});

// 客户端会自动处理 dkey 生成
// 每次调用接口时：
// 1. 获取动态参数 dcan (有效期 10 秒)
// 2. 生成 dkey = md5(dmsg + dcan)
// 3. 附带 dkey 参数调用接口
```

**第三步：手动配置凭证文件**
```bash
# 编辑 .credentials/apihz.txt
APIHZ_ID=你的 ID
APIHZ_KEY=你的 KEY
APIHZ_DMSG=your_secret_message  # 预留信息
```

### 代码配置示例

```javascript
// 基础配置 (不使用动态密钥)
const client = new ApiHzClient({
  id: '123456',
  key: 'abcdef',
  baseUrl: 'https://cn.apihz.cn'
});

// 增强配置 (使用动态密钥)
const client = new ApiHzClient({
  id: '123456',
  key: 'abcdef',
  dmsg: 'my_secret_2026',
  baseUrl: 'https://cn.apihz.cn'
});
```

---

## ⚠️ 注意事项

### 安全提示

1. **凭证存储:** 
   - ✅ KEY 和 DMSG 使用 **AES-256-GCM 加密存储**
   - ✅ 加密密钥基于机器指纹生成 (主机名 + 用户名 + 工作区)
   - ✅ 不要将凭证文件复制到其他机器使用
   - ✅ 不要将该文件提交到 Git

2. **动态密钥 (推荐):** 
   - ✅ 开启动态密钥后，每次调用需验证 `dkey` 参数
   - ✅ `dkey = md5(预留信息 + 动态参数)`，防止被抓包
   - ✅ 动态参数有效期 10 秒，仅能使用 1 次
   - ✅ 配置 `APIHZ_DMSG` 环境变量或凭证文件

3. **接口线路选择:** 
   - 🟢 **域名接口** (默认): `https://cn.apihz.cn` - 自动分发，CC 防火墙适中
   - 🟢 **集群 IP**: `http://101.35.2.25` 等 - 速度快，CC 防火墙严格，定期更新
   - 🟡 **VIP 线路**: `https://vip.apihz.cn` - 超高稳定，CC 防火墙宽松 (需购买)
   - 📖 **获取最优 IP**: 访问 `https://api.apihz.cn/getapi.php` 获取当前最优 IP

4. **网络传输:** 
   - ✅ 主 API 使用 HTTPS 加密 (`https://cn.apihz.cn`)
   - ⚠️ API 列表查询可能回退到 HTTP 备用节点 (仅查询，不传输凭证)
   - ✅ 可通过 `APIHZ_BASE_URL` 强制使用 HTTPS

4. **最佳实践:**
   - ✅ 使用低权限测试账号，不要使用高价值凭证
   - ✅ 在生产环境使用隔离的工作区
   - ✅ 定期更新 KEY 和 DMSG

3. **签名脚本:** 
   - ⚠️ 技能本身**不自动创建**系统 cron 任务
   - ✅ 需要手动配置 crontab 来实现每日自动签到

### 技术提示

4. **参数编码:** 每个参数独立编码，不要合并
5. **请求方式:** 
   - ✅ 推荐 POST (适合大参数)
   - ✅ GET 用于简单查询
   - 📖 官方教程：https://www.apihz.cn/template/miuu/getpost.php
6. **超时设置:**
   - 连接超时：10 秒
   - 整体超时：30 秒
   - 可通过 `timeout` 参数自定义
7. **服务器配置:** 
   - 主 API: `https://cn.apihz.cn` (官方域名，HTTPS)
   - API 列表：可通过 `APIHZ_LIST_URL` 环境变量指定 HTTPS 节点
   - 故障切换：主服务器不可用时自动尝试备用节点
8. **路径配置:** 
   - 默认工作区：`$HOME/.openclaw/workspace`
   - 可通过 `OPENCLAW_WORKSPACE` 环境变量覆盖
   - 凭证文件：`{workspace}/.credentials/apihz.txt`

### 推荐配置 (生产环境)

```bash
# 强制使用 HTTPS
export APIHZ_BASE_URL=https://cn.apihz.cn
export APIHZ_LIST_URL=https://cn.apihz.cn/api/xitong/apilist.php

# 指定工作区
export OPENCLAW_WORKSPACE=/path/to/your/workspace
```

---

## 📞 支持

- 官网：https://www.apihz.cn
- QQ 群：500700444
- 客服 QQ: 2813858888

---

*最后更新：2026-03-08*
