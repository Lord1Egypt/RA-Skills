---
name: douyin-scraper
description: 爬取抖音爆款视频和文案数据，支持自然语言搜索请求（如"搜索一下海鲜视频"），通过浏览器自动化或脚本获取数据。
---

# 抖音爆款爬虫 Skill

## 自然语言入口

当用户发出类似以下请求时，本 skill 自动激活：

- "搜索一下海鲜视频"
- "看看抖音热榜有什么"
- "找一些海鲜售卖相关的视频文案"
- "帮我搜抖音上关于XX的内容"

## 工作流程

### Step 1: 解析意图

从用户自然语言中提取：
- **操作类型**: `search`（关键词搜索）| `hot`（热榜）| `video`（单个视频链接）
- **关键词**: 从请求中提取搜索词（如"海鲜视频" → keyword="海鲜"）
- **数量**: 默认 10 条，用户指定则用指定值

### Step 2: 执行搜索

#### 方式 A：浏览器自动化（推荐，需用户已登录抖音）

使用 OpenClaw `browser` tool（profile="user"，使用用户已登录的浏览器）：

```
1. browser open → https://www.douyin.com/search/{keyword}?type=video
   （如需登录态，用 profile="user"）
2. browser snapshot → 获取页面结构
3. 从 snapshot 中提取视频卡片数据
4. 整理结果返回
```

**重要提示：**
- 抖音会检测自动化访问，未登录时大概率触发验证码
- 使用 `profile="user"` 可复用用户已有的登录态，大幅降低风控概率
- 如果遇到验证码页面，告知用户需要手动验证，或改用脚本 mock 模式

#### 方式 B：脚本命令行（备选）

```bash
# Python 版本 — mock 模式（不启动浏览器，返回示例数据）
python3 scripts/scraper.py search --keyword "海鲜" --limit 10 --mock

# Python 版本 — 真实爬取（需 Playwright + 浏览器可用）
python3 scripts/scraper.py search --keyword "海鲜" --limit 10

# Node.js 版本
node scripts/douyin_scraper.js search "海鲜" 10
```

> ⚠️ 脚本在无可用浏览器或被拦截时自动降级为 mock 数据，会打印提示。

### Step 3: 返回结果

将结果整理为可读格式：

```
🔍 搜索"海鲜"结果（共 N 条）：

1. 🎬 标题 | 👤 作者 | ▶️ 播放量 | ❤️ 点赞数
   🔗 链接
   📝 描述/标签

2. ...
```

如果是 mock 数据，需明确标注：
```
⚠️ 以下为示例数据（未获取到真实结果，可能原因：验证码拦截/浏览器不可用）

1. 🎬 海鲜相关视频 1 | 👤 作者1 | ▶️ 10,000 | ❤️ 1,000
   🔗 https://www.douyin.com/search/海鲜
```

## 热榜获取

```
browser open → https://www.douyin.com/hot
browser snapshot → 提取热榜条目
```

或脚本：`python3 scripts/scraper.py hot --limit 20 --mock`

## 单视频信息

用户提供视频链接时，用 browser 打开链接提取详情。

## 脚本说明

| 脚本 | 语言 | 说明 |
|------|------|------|
| `scripts/scraper.py` | Python | 支持 `--mock` 标志，无浏览器时自动降级 |
| `scripts/douyin_scraper.js` | Node.js | 依赖 Playwright，无浏览器时返回 mock |

## 输出格式

JSON:
```json
[{"title": "视频标题", "author": "作者", "play_count": 1000000, "like_count": 50000, "url": "https://...", "tags": ["标签1"]}]
```

## 注意事项

1. **遵守平台规则** — 合理使用，避免频繁请求
2. **登录态** — 推荐使用 `profile="user"` 浏览器，避免验证码
3. **请求间隔** — 连续操作间至少 2 秒
4. **数据用途** — 仅供学习研究
5. **风控** — 未登录访问抖音搜索/热榜大概率触发验证码，属正常现象

## 故障排除

| 问题 | 解决方案 |
|------|----------|
| 验证码拦截 | 使用 profile="user" 浏览器，或告知用户需手动验证 |
| 浏览器超时 | 检查网络，增加等待时间 |
| 脚本返回 mock | 正常（浏览器不可用），改用 browser tool |
| 页面结构变化 | 更新 snapshot 选择器 |
