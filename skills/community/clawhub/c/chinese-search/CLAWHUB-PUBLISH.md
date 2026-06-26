# ClawHub 发布指南

## 发布信息

**ClawHub 网址**: https://clawhub.ai  
**发布页面**: https://clawhub.ai/publish-skill  
**GitHub**: https://github.com/openclaw/clawhub

---

## 发布方式

### 方式 1: 命令行发布 (推荐)

```bash
# 1. 导航到技能目录
cd /home/kaising/.openclaw/workspace/skills/chinese-search/

# 2. 确认文件结构
ls -la
# 应该包含：SKILL.md, README.md, _meta.json, .clawhub/config.json

# 3. 使用 clawhub 发布
npx clawhub@latest publish

# 或指定包名
npx clawhub@latest publish chinese-search
```

### 方式 2: Web 界面发布

1. 访问 https://clawhub.ai/publish-skill
2. 登录/注册 ClawHub 账号
3. 上传技能包 (chinese-search-v1.0.tar.gz)
4. 填写技能信息
5. 设置定价 (免费/付费)
6. 提交审核

---

## 发布前检查清单

- [x] SKILL.md 存在且格式正确
- [x] README.md 包含使用说明
- [x] _meta.json 包含元数据
- [x] .clawhub/config.json 配置完整
- [x] 技能已测试可用
- [ ] ClawHub 账号已注册
- [ ] 技能包已打包 (tar.gz)

---

## 定价设置建议

### 免费版
- 必应中国搜索
- 搜狗微信搜索
- 基础搜索语法

### Pro 版 (¥99 一次性)
- 结果聚合去重
- 自动摘要生成
- 搜索历史记录

### 订阅版 (¥19/月)
- 关键词监控告警
- 批量搜索
- API 集成
- 优先支持

---

## 发布后推广

1. **ClawHub 技能市场** - 自然流量
2. **中文社区** - 知乎、小红书
3. **社交媒体** - Twitter/X
4. **OpenClaw 社区** - Discord

---

## 注意事项

1. **首次发布需要审核** - 通常 24-48 小时
2. **版本号管理** - 遵循语义化版本 (v1.0.0)
3. **更新流程** - 修改版本号后重新发布
4. **用户反馈** - 及时响应 Issue 和评价

---

**创建时间**: 2026-03-29 18:10  
**状态**: 准备发布
