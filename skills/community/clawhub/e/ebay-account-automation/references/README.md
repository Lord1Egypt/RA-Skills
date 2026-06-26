# eBay Account Automation

> eBay 卖家账号活跃自动化工具。通过 ADS Power 控制浏览器，模拟真实用户搜索、浏览、收藏、加购行为，维持账号活跃状态。

## 工作原理

```
[定时触发 / 手动运行]
        ↓
[从 ADS Power API 读取所有账号]
        ↓
[按索引轮换账号（状态文件记录断点）]
        ↓
[关闭旧浏览器] → [启动目标账号浏览器] → [获取 debug_port]
        ↓
[通过 WebSocket 连接浏览器，发送 CDP 命令]
        ↓
[执行行为模拟：搜索 → 浏览 → 收藏 → 加购]
        ↓
[30 分钟后关闭浏览器，切换下个账号]
```

## 安装

```bash
cd scripts
npm install
```

## 配置

复制 `config_local.js.example` 为 `config_local.js`，填入你的 ADS Power API Key：

```bash
cp config_local.js.example config_local.js
# 然后编辑 config_local.js 填入 API Key
```

或通过环境变量：

```bash
export ADS_API_KEY=your_key_here
export ADS_API_BASE=http://local.adspower.net:50325
```

## 运行方式

### 单账号轮换（默认，cron 使用这个）

```bash
node scheduler.js
```

### 全量覆盖所有账号（一次性跑完）

```bash
node scheduler.js --full
```

### 5分钟快速验证

```bash
node test_quick.js
```

### 诊断页面选择器

```bash
node diag_selectors2.js <user_id>
```

## 行为设计

每个账号运行时长 30 分钟，执行多轮以下流程：

1. 打开 eBay 首页，随机滚动
2. 从 `keywords.txt` 随机选一个词，搜索
3. 从搜索结果随机点进 2~4 个商品页
4. 每个商品页滚动浏览，随机执行：
   - 收藏商品（概率 60%）
   - 加入购物车（概率 35%）
5. 每轮之间随机休息 10~25 秒
6. 30 分钟内尽可能多做几轮搜索

## ADS Power 配额说明

ADS Power 对同时打开的浏览器数量有限流（每日限额），遇到以下错误时属于正常情况，等待恢复后再运行：

| 错误信息 | 含义 | 恢复时间 |
|---|---|---|
| `Exceeding open daily limit` | 每日浏览器打开次数超限 | 8小时 |
| `User_id is not open` | 账号未启用/同步中 | 等待同步 |
| `SunBrowser is updating` | 浏览器正在后台更新 | 10-30秒自动重试 |

## 关键词管理

编辑 `keywords.txt`，每行一个搜索词（英文 eBay 美国站）：

```
basketball jersey
football gloves
sports hoodies
```

## OpenClaw Cron 调度

```bash
openclaw cron add \
  --name ebay_account_cycler \
  --every-ms 1800000 \
  --session-target isolated \
  --payload-kind agentTurn \
  --payload-message "cd /path/to/skills/ebay-account-automation/scripts && node scheduler.js"
```
