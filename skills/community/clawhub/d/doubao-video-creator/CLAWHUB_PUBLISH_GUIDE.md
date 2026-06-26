# 📤 发布到 ClawHub 指南

## ✅ 前提条件

1. **GitHub 仓库已发布** ✅
   - https://github.com/Cindypapa/doubao-video-creator

2. **技能文件已准备** ✅
   - 位置：`/root/.openclaw/workspace/skills/doubao-video-creator/`

## 🔑 步骤 1: 登录 ClawHub

```bash
# 登录 ClawHub（会打开浏览器）
clawhub login

# 或者手动输入 Token
clawhub auth token <your-token>
```

**登录方式**：
1. 访问 https://clawhub.ai
2. 登录账号
3. 获取 API Token
4. 运行 `clawhub auth token <token>`

## 📝 步骤 2: 准备发布

### 检查文件结构
```
doubao-video-creator/
├── SKILL.md                 # ⭐ 必需 - 技能说明
├── README.md                # ⭐ 必需 - 使用说明
├── *.py                     # Python 模块
├── *.md                     # 文档
└── project_template.json    # 配置模板
```

### 检查 SKILL.md 头部
确保 SKILL.md 包含必要的元数据：
```markdown
# doubao-video-creator - 豆包视频创作助手 v2.0

## 📋 技能描述
...

## 🎯 触发条件
...
```

## 🚀 步骤 3: 发布技能

```bash
# 进入技能目录
cd /root/.openclaw/workspace/skills/doubao-video-creator

# 发布技能
clawhub publish .
```

**发布选项**：
```bash
# 发布（带描述）
clawhub publish . --desc "AI 视频创作助手，使用豆包模型生成专业视频"

# 发布（不提示确认）
clawhub publish . --no-input

# 发布后验证
clawhub inspect doubao-video-creator
```

## 📊 步骤 4: 验证发布

```bash
# 查看已发布技能
clawhub list

# 搜索自己的技能
clawhub search doubao-video-creator

# 查看技能详情
clawhub inspect doubao-video-creator
```

## 🎯 发布后的安装方式

用户可以使用以下命令安装：

```bash
# 通过 OpenClaw 安装
/plugin install doubao-video-creator

# 或通过 ClawHub 安装
clawhub install doubao-video-creator
```

## 📋 发布清单

### 必需文件
- [x] SKILL.md - 技能说明
- [x] README.md - 使用说明
- [x] Python 模块（*.py）

### 推荐文件
- [x] BEST_PRACTICES.md - 最佳实践
- [x] QUICK_REFERENCE.md - 快速参考
- [x] 其他文档

### 发布前检查
- [ ] 已登录 ClawHub
- [ ] SKILL.md 包含完整说明
- [ ] README.md 包含安装说明
- [ ] 无敏感信息（API Keys 等）
- [ ] 已测试技能功能

## ⚠️ 注意事项

### 1. 敏感信息
**不要包含**：
- API Keys
- 密码
- 私人配置

**检查命令**：
```bash
grep -r "API_KEY\|TOKEN\|PASSWORD" . --include="*.md" --include="*.py"
```

### 2. 技能名称
- 使用小写字母
- 使用连字符分隔：`doubao-video-creator`
- 不要使用空格或下划线

### 3. 版本更新
```bash
# 更新已发布的技能
clawhub update doubao-video-creator

# 或者重新发布
clawhub publish . --force
```

## 🔗 相关链接

- **ClawHub 网站**: https://clawhub.ai
- **技能市场**: https://clawhub.ai/skills
- **文档**: https://docs.clawhub.ai

## 📞 发布后

发布成功后：
1. 更新 Moltbook 帖子，添加 ClawHub 安装链接
2. 在 GitHub README 中添加 ClawHub 安装说明
3. 分享给社区

---

**准备发布！** 🚀
