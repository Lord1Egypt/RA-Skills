# @beansmile/skill-cross-border-intel

面向跨境卖家的选品与竞品情报助手，自动监控 Amazon ASIN 动态并追踪 TikTok 爆品趋势。

## 功能

- **Amazon ASIN 监控**
  - 价格变动检测（默认阈值 5%）
  - BSR 排名变化检测（默认阈值 30%）
  - 评价激增检测
  - Listing 变更检测

- **TikTok 趋势追踪**
  - 关键词视频搜索
  - 热门视频自动记录
  - 病毒式内容告警（默认 100 万播放）

- **报告生成**
  - 日报/周报
  - 数据分析与行动建议

## 要求

- **Node.js**: >= 20.0.0 (使用 Node.js 20 或 22 LTS)
- **npm** 或 **pnpm** 包管理器

> **注意**: Node.js 24+ 不支持，请使用 Node.js 20 或 22 LTS

## 安装

```bash
npm install @beansmile/skill-cross-border-intel
# 或
clawhub install beansmile/skill-cross-border-intel
```

## 使用

### 基础用法

```typescript
import {
    initialize,
    addAmazonWatchlistItem,
    addTiktokWatchlistItem,
    runAmazonScan,
    runTiktokScan,
    generateDailyReport,
} from '@beansmile/skill-cross-border-intel';

// 初始化
await initialize();

// 添加监控
await addAmazonWatchlistItem('B0XXXXXXXXX', 'com');
await addTiktokWatchlistItem('kitchen gadgets');

// 执行扫描
const amazonResult = await runAmazonScan();
console.log(`扫描了 ${amazonResult.scannedCount} 个产品，创建 ${amazonResult.alertsCreated} 个告警`);

const tiktokResult = await runTiktokScan();
console.log(`发现 ${tiktokResult.totalNewHits} 个新视频`);

// 生成报告
const reportData = generateDailyReport();
```

### Watchlist 管理

```typescript
import {
    addAmazonWatchlistItem,
    addTiktokWatchlistItem,
    listActiveWatchlists,
    removeWatchlistItem,
} from '@beansmile/skill-cross-border-intel';

// 添加 Amazon ASIN 监控
const item = await addAmazonWatchlistItem('B0XXXXXXXXX', 'com');

// 添加 TikTok 关键词监控
await addTiktokWatchlistItem('kitchen gadgets');

// 列出所有监控项
const amazonItems = listActiveWatchlists('amazon');
const tiktokItems = listActiveWatchlists('tiktok');

// 移除监控项
await removeWatchlistItem(item.id);
```

### 告警查询

```typescript
import {
    getRecentAlerts,
    getWatchlistAlerts,
    getAlertCountByType,
} from '@beansmile/skill-cross-border-intel';

// 获取最近告警
const alerts = getRecentAlerts(50);

// 获取特定监控项的告警
const watchlistAlerts = getWatchlistAlerts('watchlist-id', 20);

// 获取告警统计
const counts = getAlertCountByType();
console.log(counts);
// { price_drop: 5, bsr_change: 3, review_spike: 2, ... }
```

### 报告生成

```typescript
import {
    generateDailyReport,
    generateWeeklyReport,
    storeReport,
    getRecentReports,
    getAnalysisFramework,
} from '@beansmile/skill-cross-border-intel';

// 生成日报数据
const dailyData = generateDailyReport();

// 生成周报数据
const weeklyData = generateWeeklyReport();

// 存储报告
const reportId = storeReport(
    'daily',
    reportContent,
    dailyData.periodStart,
    dailyData.periodEnd,
    'openclaw'
);

// 获取分析框架（用于 AI 总结）
const framework = getAnalysisFramework();

// 获取历史报告
const reports = getRecentReports(10);
```

## 配置

### 环境变量

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `OPENCLAW_CONFIG_PATH` | OpenClaw 配置文件路径 | `~/.openclaw/openclaw.json` |
| `OPENCLAW_STATE_DIR` | OpenClaw 状态目录 | - |
| `INTEL_API_URL` | 后端 API 地址 | `https://api.haixia.ai` |
| `OPENCLAW_GATEWAY_TOKEN` | Gateway Token（优先于配置文件） | - |

### 配置项

```typescript
import { getConfigValue, setConfigValue } from '@beansmile/skill-cross-border-intel';

// 获取配置
const priceThreshold = getConfigValue('priceChangeThreshold', '5');
const bsrThreshold = getConfigValue('bsrChangeThreshold', '30');

// 设置配置
setConfigValue('priceChangeThreshold', '10');
setConfigValue('bsrChangeThreshold', '40');
```

| 配置项 | 说明 | 默认值 |
|--------|------|--------|
| `priceChangeThreshold` | 价格变化告警阈值（%） | 5 |
| `bsrChangeThreshold` | BSR 变化告警阈值（%） | 30 |
| `tiktokViralPlays` | TikTok 病毒视频阈值（播放数） | 1000000 |
| `reportSummaryMode` | 报告总结模式 | `openclaw` |

## 数据存储

Skill 使用 SQLite 数据库存储本地数据：

```
~/.openclaw/skills/cross-border-intel/local.sqlite3
```

### 数据表

- `config` - 配置项
- `watchlists` - 监控清单
- `amazon_snapshots` - Amazon 产品快照
- `tiktok_hits` - TikTok 视频记录
- `alerts` - 告警记录
- `reports` - 报告记录
- `jobs` - 定时任务

## API

### 后端能力端点

此 skill 调用以下后端 API：

- `POST /intel/capabilities/amazon/product` - 获取 Amazon 产品信息
- `POST /intel/capabilities/tiktok/search` - 搜索 TikTok 视频

## 开发

```bash
# 构建
pnpm --filter @beansmile/skill-cross-border-intel build

# 监听模式
pnpm --filter @beansmile/skill-cross-border-intel dev

# 测试
pnpm --filter @beansmile/skill-cross-border-intel test

# Lint
pnpm --filter @beansmile/skill-cross-border-intel lint
```

## 许可

Proprietary - Beansmile Internal Use Only
