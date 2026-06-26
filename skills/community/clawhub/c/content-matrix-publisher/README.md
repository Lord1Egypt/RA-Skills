# 智能内容矩阵分发 Combo

> **一站式内容矩阵解决方案**：从热点发现到多平台发布，自动化你的内容运营流程。

---

## 🎯 解决什么问题？

**内容创作者的三大痛点**：

1. **选题难** —— 不知道今天发什么，热点追踪不及时
2. **创作累** —— 同一内容要适配多个平台格式，重复劳动
3. **效率低** —— 发布流程繁琐，缺乏系统化运营

**本 Combo 解决方案**：将 **5 个 Skills** 编排成自动化工作流，实现：

```
热点搜索 → 内容提炼 → 原创创作 → 多平台适配 → 一键发布
```

---

## 📊 Skill 编排图谱

```
                        ┌─────────────────┐
                        │  agent-reach   │
                        │   (热点搜索)    │
                        └────────┬────────┘
                                 │
                                 ▼
                        ┌─────────────────┐
                        │   summarize     │
                        │   (内容提炼)     │
                        └────────┬────────┘
                                 │
                                 ▼
                        ┌─────────────────┐
                        │   本地创作引擎   │
                        │  (原创文案生成)   │
                        └────────┬────────┘
                                 │
              ┌──────────────────┼──────────────────┐
              │                  │                  │
              ▼                  ▼                  ▼
     ┌────────────────┐ ┌────────────────┐ ┌────────────────┐
     │ xiaohongshu-mcp│ │  card-renderer │ │    公众号助手   │
     │  (小红书发布)   │ │  (知识卡片)    │ │  (公众号文章)   │
     └────────────────┘ └────────────────┘ └────────────────┘
```

---

## 🚀 快速开始

### 安装依赖 Skills

```bash
# 安装所有依赖 Skills
openclaw skill install agent-reach
openclaw skill install summarize  
openclaw skill install xiaohongshu-mcp
openclaw skill install card-renderer
openclaw skill install wechat-article-pro
```

### 配置平台凭证

```yaml
# ~/.openclaw/config.yaml
xiaohongshu-mcp:
  web_session: "your_xiaohongshu_cookie"
  
wechat-article-pro:
  appid: "your_wechat_appid"
  secret: "your_wechat_secret"
```

### 执行工作流

```
用户: 帮我发布一篇关于"AI 编程助手"的内容到小红书和公众号
```

Agent 将自动执行：
1. 搜索相关热点
2. 提炼核心内容
3. 生成原创文案
4. 适配平台格式
5. 发布并返回链接

---

## 📝 使用示例

### 场景 1: 日常热点发布

```
用户: 今天有什么 AI 热点？帮我生成内容发到小红书

执行流程:
[agent-reach] 搜索小红书 AI 热点 TOP10
[summarize] 提炼 3 个核心话题
[创作引擎] 生成原创笔记
[card-renderer] 生成封面图
[xiaohongshu-mcp] 发布图文

返回: 发布成功！链接: https://xiaohongshu.com/note/xxx
```

### 场景 2: 深度选题创作

```
用户: 我要写一篇关于"大模型落地实践"的公众号文章

执行流程:
[agent-reach] 搜索知乎/B站相关内容
[summarize] 整理竞品分析和案例
[创作引擎] 生成 3000 字深度文章
[公众号助手] 自动配图 + 发布

返回: 文章已发布！链接: https://mp.weixin.qq.com/xxx
```

### 场景 3: 矩阵批量发布

```
用户: 帮我把这篇内容适配到小红书和公众号

执行流程:
[内容解析] 分析原始内容核心
[平台适配] 生成小红书版本 + 公众号版本
[card-renderer] 生成小红书封面
[并行发布] 同时发布到两个平台

返回: 
- 小红书: https://xiaohongshu.com/note/xxx
- 公众号: https://mp.weixin.qq.com/xxx
```

---

## ⚙️ 配置选项

### 工作流配置

```yaml
content-matrix-publisher:
  # 默认发布平台
  platforms:
    - xiaohongshu
    - wechat_official
  
  # 自动生成配图
  auto_image: true
  
  # 发布时间段（定时任务）
  publish_schedule:
    - "09:00"
    - "12:00"
    - "18:00"
  
  # 内容风格
  style:
    xiaohongshu: "轻松活泼 + emoji"
    wechat: "刘润风格 + 深度分析"
```

### 高级配置

```yaml
# 热点搜索配置
discovery:
  sources:
    - xiaohongshu
    - weibo
    - zhihu
  keywords: ["AI", "效率", "工具"]
  max_results: 10
  
# 内容创作配置  
creation:
  originality_check: true  # 原创性检查
  sensitive_filter: true   # 敏感词过滤
  word_count:
    xiaohongshu: 500
    wechat: 3000

# 发布配置
distribution:
  auto_publish: false      # 自动发布（需谨慎）
  save_draft: true         # 保存草稿
  retry_on_fail: true      # 失败重试
```

---

## 🔒 安全与合规

### 内容安全

- ✅ **原创性检测**：避免直接复制热点内容
- ✅ **敏感词过滤**：自动检测并替换敏感词
- ✅ **平台合规**：遵守各平台内容规范

### 发布策略

- ⚠️ **发布频率控制**：避免短时间大量发布
- ⚠️ **内容差异化**：确保不同平台内容有差异化
- ⚠️ **人工审核**：重要内容建议人工确认后发布

---

## 📈 数据追踪

发布后可追踪以下指标：

| 指标 | 小红书 | 公众号 |
|------|--------|--------|
| 阅读量 | ✅ | ✅ |
| 点赞数 | ✅ | ✅ |
| 收藏数 | ✅ | ✅ |
| 评论数 | ✅ | ✅ |
| 分享数 | ✅ | ✅ |

---

## 🔧 故障排除

| 问题 | 解决方案 |
|------|---------|
| 热点搜索失败 | 检查网络连接，或使用本地选题库 |
| 图片生成失败 | 使用预设模板图，或手动上传 |
| 发布限流 | 降低发布频率，等待冷却期 |
| 内容审核失败 | 检查敏感词，修改后重试 |

---

## 🚧 未来扩展

- [ ] B站视频脚本生成
- [ ] 抖音文案适配
- [ ] LinkedIn 专业文章
- [ ] Twitter/X 短内容
- [ ] 数据看板整合
- [ ] AI 选题推荐

---

## 📄 文件结构

```
content-matrix-publisher/
├── SKILL.md          # 主技能文件（当前文件）
├── workflow.json     # 工作流配置
├── README.md         # 使用文档
├── config/           # 配置模板
│   └── default.yaml
├── scripts/          # 辅助脚本
│   ├── discovery.sh  # 热点发现
│   └── publish.sh    # 发布脚本
└── templates/        # 内容模板
    ├── xiaohongshu.md
    └── wechat.md
```

---

## 📞 支持

- 问题反馈：在 OpenClaw 社区提 Issue
- 功能建议：欢迎 PR 贡献

---

**版本**: 1.0.0  
**更新日期**: 2026-03-25  
**维护者**: OpenClaw Community