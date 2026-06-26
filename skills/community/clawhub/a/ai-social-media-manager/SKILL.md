# AI-Social-Media-Manager Skill

AI 驱动的社交媒体管理技能，自动化内容创作、发布和优化。

## 功能

- 📅 **内容日历自动生成** - 基于行业趋势和受众分析生成月度内容计划
- ⏰ **最佳发布时间推荐** - 分析受众活跃度，推荐最优发布时段
- 💬 **自动回复和互动** - 智能回复评论、私信，提升互动率
- 📊 **表现分析和优化** - 追踪关键指标，提供优化建议

## 支持平台

- Twitter/X
- 小红书
- 微博
- LinkedIn
- Instagram
- 微信公众号

## 安装

```bash
clawhub install ai-social-media-manager
```

## 使用示例

### 生成内容日历

```bash
ai-smm calendar generate --platform xiaohongshu --month 2026-03 --topic "科技产品评测"
```

### 获取最佳发布时间

```bash
ai-smm schedule best-time --platform weibo --audience "18-35 岁科技爱好者"
```

### 自动回复评论

```bash
ai-smm engage auto-reply --post-id "xxx" --tone "友好专业"
```

### 分析表现

```bash
ai-smm analytics report --period "last_30_days" --platforms "xiaohongshu,weibo"
```

## 配置

在 `TOOLS.md` 中添加社交媒体账号配置：

```markdown
### Social Media

- xiaohongshu: {username: "xxx", cookie: "xxx"}
- weibo: {username: "xxx", password: "xxx"}
- twitter: {api_key: "xxx", api_secret: "xxx"}
```

## 定价

$99/月 - 包含所有平台无限次使用

## API 参考

详见 `src/README.md`
