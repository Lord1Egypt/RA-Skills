# content-monetizer

## 描述
内容变现助手 - 分析你的内容（文章/视频/代码），推荐最佳变现方式。适合：创作者、博主、开发者。

## 功能
- 内容价值评估（预计收入）
- 平台推荐（掘金/知乎/B站/YouTube）
- 变现方式建议（广告/付费/会员/咨询）
- 竞品对标分析
- SEO 优化建议

## 使用场景
1. 写文章前 - 先评估哪个平台收益最高
2. 内容复用 - 一篇内容多平台分发策略
3. 定价咨询 - 该收多少钱？
4. 流量分析 - 为什么没人看？

## 命令示例
```bash
# 分析单篇文章
openclaw run content-monetizer analyze article.md

# 推荐平台
openclaw run content-monetizer recommend --type article --topic "AI"

# 生成分发计划
openclaw run content-monetizer distribute article.md

# 竞品分析
openclaw run content-monetizer compare "AI 教程"

# 收入预测
openclaw run content-monetizer predict --views 10000 --topic "编程"
```

## 配置
在 `~/.openclaw/config/content-monetizer.json` 中设置：
```json
{
  "platforms": {
    "juejin": { "weight": 0.3 },
    "zhihu": { "weight": 0.25 },
    "bilibili": { "weight": 0.2 },
    "wechat": { "weight": 0.15 },
    "youtube": { "weight": 0.1 }
  },
  "contentTypes": ["article", "video", "code", "course"]
}
```

## 变现方式分析
```
📝 内容分析报告

主题：DeepSeek API 教程
字数：3000 字
预估价值：¥500-2000

推荐平台：
1. 掘金（⭐⭐⭐⭐⭐）
   - 受众匹配度高
   - 预计阅读：2000-5000
   - 潜在收入：¥100-500（广告/付费）

2. 知乎（⭐⭐⭐⭐）
   - 搜索流量大
   - 预计阅读：1000-3000
   - 潜在收入：¥50-200

3. 公众号（⭐⭐⭐）
   - 需要私域运营
   - 潜在收入：¥200-1000（咨询转化）

变现建议：
- 短期：掘金发布 + 接咨询
- 中期：整理成付费课程
- 长期：建立社群/会员

行动计划：
1. 今天：发布掘金，添加微信引流
2. 本周：知乎同步，回答相关问题
3. 本月：整理成电子书，定价 ¥29
```

## 注意事项
- 收入预测仅供参考
- 实际收益取决于内容质量和运营
- 建议配合 content-creator-cn 使用