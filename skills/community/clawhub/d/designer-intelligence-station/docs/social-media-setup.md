# 社交平台热点信息源配置指南

本文档指导您配置社交平台热点信息源，以便设计师情报站能够抓取各平台热点内容。

---

## 📱 已添加的社交平台（8 个）

| ID | 平台 | 抓取方式 | 优先级 | 配置要求 |
|----|------|---------|--------|---------|
| SOC001 | X (Twitter) 趋势 | web | 高 | agent-reach twitter 通道 |
| SOC002 | 小红书热点 | api | 高 | xiaohongshu-mcp |
| SOC003 | 微博热搜 | web | 高 | 无需配置 |
| SOC004 | 抖音热点 | web | 高 | 无需配置 |
| SOC005 | Bilibili 热门 | web | 高 | 无需配置 |
| SOC006 | 知乎热榜 | web | 中 | 无需配置 |
| SOC007 | 即刻热点 | web | 中 | 无需配置 |
| SOC008 | 什么值得买 | web | 中 | 无需配置 |

---

## 🔧 配置步骤

### 方式一：使用 agent-reach skill（推荐）

如果您已经安装了 `agent-reach` skill，可以直接使用：

```bash
# 查看所有可用通道
agent-reach doctor

# 配置 Twitter/X
agent-reach configure twitter-cookies "auth_token=xxx; ct0=yyy"

# 或使用浏览器自动提取 cookies
agent-reach configure --from-browser chrome
```

### 方式二：手动配置 MCP

#### 1. 小红书热点配置

小红书需要使用 `xiaohongshu-mcp` 服务：

```bash
# Step 1: 检查服务是否运行
ps aux | grep xiaohongshu-mcp

# Step 2: 启动服务（如果未运行）
nohup ~/.openclaw/skills/agent-reach/scripts/xiaohongshu-mcp-linux-amd64 \
  -headless=false -bin /usr/bin/google-chrome \
  > /tmp/xiaohongshu-mcp.log 2>&1 &

# Step 3: 配置 mcporter
mcporter config add xiaohongshu http://localhost:18060/mcp

# Step 4: 登录小红书
~/.openclaw/skills/agent-reach/scripts/xiaohongshu-login-linux-amd64 \
  -bin /usr/bin/google-chrome
```

**验证配置**：
```bash
mcporter call 'xiaohongshu.check_login_status()'
mcporter call 'xiaohongshu.search_feeds(keyword: "设计趋势")'
```

#### 2. Twitter/X 配置

使用 `agent-reach` 的 xreach 工具：

```bash
# 安装依赖
pip install agent-reach

# 配置 Twitter cookies
agent-reach configure twitter-cookies "auth_token=xxx; ct0=yyy"

# 测试抓取趋势
xreach twitter trends
```

或者直接从浏览器提取：
```bash
agent-reach configure --from-browser chrome
```

---

## 📊 抓取策略

### 无需配置的平台（直接抓取）

以下平台使用 `web_fetch` 工具直接抓取公开页面：

| 平台 | 网址 | 更新频率 |
|------|------|---------|
| 微博热搜 | https://s.weibo.com/top/summary | 每 10 分钟 |
| 抖音热点 | https://www.douyin.com/hot | 实时 |
| Bilibili 热门 | https://www.bilibili.com/v/popular/all | 每日 |
| 知乎热榜 | https://www.zhihu.com/hot | 实时 |
| 即刻热点 | https://web.okjike.com/ | 实时 |
| 什么值得买 | https://www.smzdm.com/top/ | 实时 |

### 需要配置的平台

| 平台 | 配置方式 | 说明 |
|------|---------|------|
| X (Twitter) | agent-reach | 需要 Twitter 账号 cookies |
| 小红书 | xiaohongshu-mcp | 需要登录状态 |

---

## 🤖 在日报中使用社交平台数据

### 示例：抓取微博热搜

```python
from tools.web_fetcher import fetch_web

result = fetch_web('https://s.weibo.com/top/summary', extract_mode='markdown')
# 解析热搜榜单，提取前 10 条
```

### 示例：抓取小红书热点笔记

```python
import subprocess

# 调用 MCP 工具
result = subprocess.run([
    'mcporter', 'call', 
    'xiaohongshu.search_feeds(keyword: "设计趋势")'
], capture_output=True, text=True)

feeds = json.loads(result.stdout)
```

### 示例：抓取 Twitter 趋势

```python
import subprocess

result = subprocess.run([
    'xreach', 'twitter', 'trends'
], capture_output=True, text=True)

trends = json.loads(result.stdout)
```

---

## 📝 在日报中呈现社交平台热点

建议在日报中增加「🔥 社交平台热点」板块：

```markdown
### 🔥 社交平台热点

#### 微博热搜（科技/设计相关）
| 排名 | 话题 | 热度 |
|------|------|------|
| 3 | #苹果 WWDC26 定档# | 520 万 |
| 8 | #AI 设计师失业# | 280 万 |
| 15 | #大疆起诉影石# | 150 万 |

#### 小红书热点（设计类）
| 笔记 | 点赞 | 收藏 |
|------|------|--------|
| 2026 设计趋势预测 | 10k+ | 5k+ |
| Figma AI 技巧合集 | 8k+ | 3k+ |

#### X (Twitter) 趋势
| 话题 | 推文数 |
|------|--------|
| #AIAgent | 50k+ |
| #DesignSystem | 12k+ |
```

---

## ⚠️ 注意事项

### 1. 隐私与合规
- 仅抓取公开内容
- 不绕过付费墙
- 遵守各平台 robots.txt
- 尊重用户隐私

### 2. 频率限制
- 微博/抖音：每 10 分钟最多 1 次
- B 站/知乎：每 5 分钟最多 1 次
- Twitter：需要 cookies，频率更低
- 小红书：需要登录，建议每小时最多 1 次

### 3. 反爬措施
- 使用 User-Agent 轮换
- 添加请求延迟
- 使用代理（如需要）
- 失败时自动降级（web → RSS）

---

## 🛠️ 故障排查

### 问题：小红书抓取失败

```bash
# 检查服务状态
ps aux | grep xiaohongshu-mcp

# 查看日志
cat /tmp/xiaohongshu-mcp.log

# 重新登录
~/.openclaw/skills/agent-reach/scripts/xiaohongshu-login-linux-amd64
```

### 问题：Twitter 需要登录

```bash
# 从浏览器提取 cookies
agent-reach configure --from-browser chrome

# 或手动配置
agent-reach configure twitter-cookies "auth_token=xxx"
```

### 问题：微博热搜返回空

可能是反爬限制，尝试：
```bash
# 添加 User-Agent
curl -H "User-Agent: Mozilla/5.0 ..." https://s.weibo.com/top/summary
```

---

## 📚 相关资源

- [agent-reach 文档](https://github.com/Panniantong/agent-reach)
- [xiaohongshu-mcp](https://github.com/duanmingyu/xiaohongshu-mcp)
- [设计师情报站 SKILL.md](../SKILL.md)

---

*最后更新：2026-03-24 | 设计师情报站 v1.4.1*
