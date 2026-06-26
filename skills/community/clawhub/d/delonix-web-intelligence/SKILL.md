---
name: delonix-web-intelligence
description: |
  德胧AI龙虾军团外网信息舆情采集工具 v1.0。整合 miaoda-web-search（网页搜索摘要）+ AutoCLI（50+平台深度采集）+ 飞书卡片推送 + 定时自动化。
  
  触发词：舆情、情报、网情、监控、搜索、行业动态、竞争对手动态、竞品分析、外网信息采集
  
  使用场景：
  - 酒店行业舆情监控（华住/锦江/亚朵/德胧）
  - 竞品动态追踪
  - 行业趋势分析
  - 危机公关预警
  - 每日行业报告自动生成
override-tools:
  - web_search
---

# 德胧舆情采集龙虾工具 v1.0

> 德胧AI龙虾军团专属外网信息舆情采集工具
> 版本：v1.0 | 日期：2026-04-19 | 作者：晁留柱的助手（小柱）
> 整合来源：miaoda-web-search + AutoCLI + 飞书卡片推送

---

## 🔧 核心架构

```
德胧舆情采集龙虾 v1.0
├── 数据源层
│   ├── miaoda-web-search（主力）→ 关键词搜索 + AI摘要
│   └── AutoCLI（扩展）→ 50+平台深度结构化采集
├── 处理层
│   ├── 关键词模板（华住/锦江/亚朵/德胧/首旅如家）
│   ├── 热度排序（按发布时间/媒体权重）
│   └── 去重+排重
├── 输出层
│   ├── 飞书互动卡片（精美版）→ 定时推群
│   └── 结构化数据表 → 入库分析
└── 自动化层
    └── cron每日9:00自动采集推送
```

---

## ⚡ 快速使用

### 基础搜索

```bash
# 酒店舆情搜索
miaoda-studio-cli search-summary --query "华住 回访电话 隐私泄露 2026年4月"

# 竞品动态搜索
miaoda-studio-cli search-summary --query "锦江 AI动态定价 2026"

# 带筛选条件的搜索
miaoda-studio-cli search-summary --query "酒店 差评 投诉 2026年" --instruction "只保留2026年发布的内容，按热度排序"
```

### 竞品监控模板

```bash
# 华住舆情
miaoda-studio-cli search-summary --query "华住 投诉 隐私 2026" --instruction "提取投诉数量、主要问题、媒体曝光情况"

# 锦江动态
miaoda-studio-cli search-summary --query "锦江 锦鲲 AI 定价 2026" --instruction "提取AI覆盖数据、效果数据、竞品对比"

# 亚朵动态
miaoda-studio-cli search-summary --query "亚朵 服务 投诉 2026年" --instruction "提取服务质量数据、投诉热点、用户评价"
```

---

## 🛠️ 工具一：miaoda-web-search（主力·已集成）

### 简介
miaoda-web-search 是妙搭内置的网页搜索工具，通过 `miaoda-studio-cli search-summary` 命令实现。

### 安装状态
✅ **已集成到本Skill** - 无需额外安装，OpenClaw 环境已内置。

### 命令格式
```
miaoda-studio-cli search-summary --query "关键词" [--instruction "AI处理指令"] [--output text|json]
```

### 参数说明

| 参数 | 说明 | 必需 | 默认值 |
|------|------|------|--------|
| `--query` | 搜索关键词（1-500字符） | 是 | - |
| `--instruction` | AI处理指令 | 否 | AI自动总结 |
| `--output, -o` | 输出格式：text/json | 否 | text |

### 输出示例

```json
{
  "query": "华住 回访电话 隐私泄露 2026年4月",
  "count": 10,
  "results": [
    {
      "title": "网友称酒店回访电话暴露开房信息致其离婚",
      "url": "http://news.qq.com/...",
      "description": "华住会官方回应：经核实系客人退房后正常回访...",
      "siteName": "腾讯新闻"
    }
  ]
}
```

### 使用场景

| 场景 | 命令 |
|------|------|
| 实时舆情搜索 | `miaoda-studio-cli search-summary --query "关键词"` |
| 按时间筛选 | `miaoda-studio-cli search-summary --query "关键词" --instruction "只保留最近7天的内容"` |
| 对比分析 | `miaoda-studio-cli search-summary --query "关键词" --instruction "对比各方案的优缺点"` |
| JSON输出 | `miaoda-studio-cli search-summary --query "关键词" --output json` |

### 常见错误

| 错误 | 解决方法 |
|------|----------|
| 搜索超时 | 检查网络，重试 |
| 结果为空 | 更换关键词，尝试同义词 |
| JSON解析失败 | 检查退出码是否为0 |

---

## 🛠️ 工具二：AutoCLI（扩展·待网络恢复）

### 简介
AutoCLI（nashsu/AutoCLI v0.3.7）是支持50+社交媒体平台数据采集的开源工具，使用Playwright浏览器渲染技术实现深度数据抓取。

### 安装状态
⚠️ **暂未安装** - 受网络限制，GitHub HTTPS下载超时。

### 安装步骤（网络恢复后）

```bash
# 方式1：直接下载二进制（推荐）
# 下载地址：https://github.com/nashsu/AutoCLI/releases/download/v0.3.7/autocli-x86_64-unknown-linux-musl.tar.gz

# 方式2：从源码编译
git clone https://github.com/nashsu/AutoCLI.git /tmp/AutoCLI
cd /tmp/AutoCLI
cargo build --release
cp target/release/autocli /usr/local/bin/

# 方式3：克隆源码后手动部署
git clone git@github.com:nashsu/AutoCLI.git /tmp/AutoCLI
```

### 支持平台（50+）

| 类别 | 平台 |
|------|------|
| 社交媒体 | 微博、抖音、快手、小红书、知乎、B站 |
| 点评预订 | 大众点评、美团、携程、飞猪、去哪儿 |
| 新闻媒体 | 新浪新闻、腾讯新闻、网易新闻、搜狐新闻 |
| 投诉平台 | 黑猫投诉、消费保、21CN聚投诉 |
| 企业信息 | 企查查、天眼查、启信宝 |
| 视频 | 微博视频、微信视频号 |

### 使用示例

```bash
# 搜索大众点评酒店评价
autocli search --platform dianping --keyword "酒店 卫生 问题" --limit 50

# 搜索小红书酒店相关笔记
autocli search --platform xiaohongshu --keyword "酒店体验" --limit 100

# 搜索知乎酒店行业回答
autocli search --platform zhihu --keyword "酒店服务 投诉" --limit 50

# 全平台搜索
autocli search --all --keyword "华住 隐私泄露" --limit 200
```

### AutoCLI + miaoda 协同方案

```
阶段1（主力）：miaoda-web-search
└── 负责：关键词搜索、AI摘要、实时热点发现

阶段2（扩展）：AutoCLI
└── 负责：50+平台深度数据、评论采集、用户画像

协同流程：
用户请求 → miaoda快速搜索 → 发现热点平台 → AutoCLI深度采集
```

---

## 📤 输出：飞书卡片推送

### 飞书卡片格式（原生Markdown）

使用飞书专属 `<card>` 标签格式发送精美卡片：

```html
<card>
<title>🔥 酒店行业舆情日报 | 2026年4月19日</title>

## 🔴 超级热点 · [标题]

[内容摘要]

---

## 🟠 实时投诉热点

| 时间 | 投诉内容 | 来源 |
|------|---------|------|
| ... | ... | ... |

---

🦞 德胧AI龙虾军团 | 数据来源：miaoda-web-search | 采集时间：2026-04-19
</card>
```

### 飞书Markdown语法要点

| 要素 | 语法 | 注意 |
|------|------|------|
| 标题 | `**加粗文字**` | 不支持 `# ## ###` |
| 链接 | `[文本](url)` | - |
| 卡片标签 | `<card>...</card>` | 原生格式 |
| 分割线 | `---` | - |
| 表格 | `\| 列1 \| 列2 \|` | pipe分隔 |
| 彩色文本 | `<font color='red'>文字</font>` | 颜色枚举可用 |

### 发送卡片命令

```bash
# 使用 feishu_send_message 工具
# chat_id: 群ID（oc_xxx格式）或用户ID（ou_xxx格式）
# title: 卡片标题
# content: Markdown内容（会自动包装在<card>标签内）
```

---

## ⏰ 自动化：每日定时推送

### Cron配置示例

```javascript
{
  "name": "德胧舆情日报",
  "schedule": {
    "kind": "cron",
    "expr": "0 9 * * *",  // 每天9:00
    "tz": "Asia/Shanghai"
  },
  "sessionTarget": "isolated",
  "payload": {
    "kind": "agentTurn",
    "message": "执行德胧舆情采集：\n1. 搜索今日最新酒店行业舆情（华住/锦江/亚朵/德胧）\n2. 提取超级热点、投诉数据、行业趋势\n3. 生成飞书卡片格式报告\n4. 发送到群聊 oc_2dc8a473be229282cffd2b87460dc8a8"
  },
  "delivery": {
    "mode": "announce",
    "channel": "feishu",
    "to": "oc_2dc8a473be229282cffd2b87460dc8a8"
  }
}
```

---

## 🔄 迭代计划

### v1.0（当前）
- [x] miaoda-web-search 集成
- [x] 飞书卡片格式
- [x] 关键词模板
- [ ] AutoCLI 集成（等网络恢复）

### v2.0（计划中）
- [ ] 整合 Coze CLI 外网检索 SKILL
- [ ] 接入 Coze 官方搜索 API
- [ ] 扩展 50+ 平台 AutoCLI 采集
- [ ] 添加竞品分析报告生成

### 长期规划
- [ ] 德胧私域舆情知识库
- [ ] 实时预警机制（微信公众号/微博监控）
- [ ] 可视化数据分析面板

---

## 📋 德胧专属关键词库

### 企业监控

| 企业 | 关键词 |
|------|--------|
| 华住会 | 华住、桔子水晶、汉庭、全季、海友、漫心、美居 |
| 锦江集团 | 锦江、锦江酒店、锦江旅行、锦鲲 |
| 亚朵 | 亚朵、Atour |
| 首旅如家 | 首旅如家、如家、和颐 |
| 德胧 | 开元名都、开元酒店、钛唐 |
| 滴滴 | 滴滴出行 |
| 美团 | 美团酒店、大众点评 |

### 事件类型

| 类型 | 关键词 |
|------|--------|
| 投诉 | 投诉、差评、退款、维权、欺诈 |
| 安全 | 隐私泄露、信息泄露、安全事故 |
| 服务 | 服务差、卫生问题、食品安全 |
| 运营 | 加盟、解约、关店、业绩 |
| AI | AI定价、动态定价、收益管理 |

### 媒体来源

| 优先级 | 来源 |
|--------|------|
| P0（必采） | 红星新闻、腾讯新闻、中华网、新黄河、现代快报 |
| P1（重要） | 极目新闻、澎湃新闻、36氪、虎嗅 |
| P2（参考） | 知乎、微博热搜、小红书、抖音 |

---

## 🦞 部署指南

### 一键安装（本Skill）

```bash
# 1. 复制本SKILL到OpenClaw skills目录
cp -r delonix-web-intelligence/ /path/to/your/openclaw/skills/

# 2. 重启OpenClaw加载Skill
openclaw gateway restart

# 3. 验证安装
miaoda-studio-cli --version  # 确认miaoda可用
```

### 飞书卡片推送配置

```bash
# 飞书机器人需已安装 openclaw-lark 插件
npx -y @larksuite/openclaw-lark-tools install
/feishu auth   # 完成权限授权
```

### 定时任务配置

```bash
# 添加每日9:00自动采集
openclaw cron add --name "德胧舆情日报" \
  --schedule "0 9 * * *" \
  --timezone "Asia/Shanghai" \
  --prompt "执行德胧舆情采集..."
```

---

## ⚠️ 注意事项

1. **网络限制**：GitHub HTTPS下载受限时，使用SSH克隆源码方式
2. **数据合规**：采集内容仅用于内部分析，不可公开传播
3. **频率控制**：搜索请求间隔建议 >3秒，避免触发反爬
4. **内容审核**：AI摘要可能存在误差，重要信息需人工核实

---

## 📞 技术支持

- SKILL作者：晁留柱的助手（小柱）
- 版本：v1.0
- 更新：2026-04-19
- 共享池：德胧AI协同知识共享池
