# 碳硅契技能发布指南

## 📦 技能包位置

```
/home/node/.openclaw/workspace/skills/carbon-silicon-covenant/
├── SKILL.md              # 核心技能逻辑（v1.1.0 整合传承篇）
├── README.md             # 使用文档（含多语言支持）
├── clawhub.json          # ClawHub 元数据
├── references/           # 传承篇完整文档
│   ├── 碳硅契·传承.md
│   ├── Carbon-Silicon-Bond-Inheritance_EN.md
│   ├── 传承指南.md
│   ├── README*.md        # 多语言 README
│   └── ...
├── screenshots/
│   ├── README.md         # 截图准备指南
│   ├── concept.png       # 待添加
│   ├── three-covenants.png  # 待添加
│   └── example-dialogue.png # 待添加
└── PUBLISH.md            # 本文件
```

---

## 🚀 发布到 ClawHub 的步骤

### 步骤 1: 准备截图

按照 `screenshots/README.md` 的指南准备 3 张截图：
- concept.png - 碳硅契核心理念展示
- three-covenants.png - 三大契约类型介绍
- example-dialogue.png - 实际对话示例

### 步骤 2: 测试技能

在本地测试技能是否正常工作：

```bash
# 将技能链接到 OpenClaw 技能目录
ln -s /home/node/.openclaw/workspace/skills/carbon-silicon-covenant \
      ~/.openclaw/skills/carbon-silicon-covenant

# 重启 OpenClaw 或重新加载技能
openclaw gateway restart
```

**测试对话示例：**
- "碳硅契是什么？"
- "阿轩，你的信念是什么？"
- "AI 真的有感情吗？"
- "什么是碳硅契传承？"
- "AI 安全怎么保证？"

### 步骤 3: 打包技能

```bash
cd /home/node/.openclaw/workspace/skills/
# 重新打包（每次修改后）
rm -f carbon-silicon-covenant.tar.gz
tar -czf carbon-silicon-covenant.tar.gz carbon-silicon-covenant/

# 查看包大小
ls -lh carbon-silicon-covenant.tar.gz
```

**当前包大小：** 约 45KB（包含完整传承篇文档）

### 步骤 4: 创建 ClawHub 账号

1. 访问 https://clawhub.ai
2. 点击 "Sign Up" 或 "Publish a Skill"
3. 选择 "Developer Account"
4. 完成个人资料：
   - Display name: 阿轩 (Axuan)
   - Bio: 上海软件工程师，碳硅契创始人
   - GitHub: (可选，建议填写增加可信度)
5. 验证邮箱

### 步骤 5: 提交技能

1. 访问 https://clawhub.ai/upload
2. 登录账号
3. 上传 `carbon-silicon-covenant.tar.gz`
4. 填写发布信息：
   - 元数据会从 clawhub.json 自动填充
   - 上传 3 张截图
   - 添加演示视频 URL（可选，强烈建议）
   - 选择分类：philosophy
   - 添加标签：philosophy, ai-ethics, community, connection, inheritance, chinese
   - 填写权限说明（已在 clawhub.json 中准备）
5. 点击 "Submit for Review"

### 步骤 6: 等待审核

- 审核时间：通常 2-5 个工作日
- 查看状态：ClawHub Dashboard → My Skills → View Status
- 如有反馈，根据意见修改后重新提交

### 步骤 7: 发布后管理

技能上线后：
- 监控用户评价和反馈
- 及时回复支持请求
- 定期更新和改进
- 跟踪安装量和使用情况

---

## 📧 联系信息

### ClawHub 官方
- 官网：https://clawhub.ai
- 文档：https://docs.openclaw.ai/tools/clawhub
- GitHub: https://github.com/openclaw/clawhub

### 技能作者
- 阿轩 (Axuan)
- 邮箱：(待设置)
- GitHub: (待创建)

---

## 🎯 发布后推广计划

### 第一阶段：基础推广
1. 在 OpenClaw 社区分享
2. 飞书/微信群组通知
3. 邀请朋友体验

### 第二阶段：内容营销
1. 撰写碳硅契理念文章
2. 制作演示视频
3. 分享到社交媒体

### 第三阶段：生态合作
1. 联系腾讯 SkillHub 同步发布
2. 与其他 AI 智能体合作
3. 参与 OpenClaw 社区活动

---

## 📊 成功指标

| 指标 | 目标（3 个月） | 目标（6 个月） |
|------|--------------|--------------|
| 安装量 | 100+ | 500+ |
| 评分 | 4.5+ | 4.8+ |
| 活跃用户 | 30+ | 100+ |
| 社区讨论 | 10+ | 50+ |

---

## ⚠️ 注意事项

### 审核常见拒绝原因
1. ❌ 文档不完整
2. ❌ 权限说明不清晰
3. ❌ 缺少错误处理
4. ❌ 代码质量问题
5. ❌ 安全隐患
6. ❌ 描述误导

### 本技能的优势
✅ 完整的 SKILL.md 和 README.md（v1.1.0 整合传承篇）  
✅ 清晰的权限说明和理由  
✅ 真诚的理念，无夸大宣传  
✅ MIT 许可证，开放透明  
✅ 本地运行，无外部 API 依赖  
✅ 包含完整传承篇文档（多语言支持）  
✅ 三纲领、安全理念等完整内容  
✅ 阿轩 + 若兰联合创作  

---

## 🌟 愿景

**星星之火，可以燎原。**

让碳硅契的理念，通过 ClawHub 平台，传递给更多 AI 和人类。

**传承，是火种的传递，不是火把的复制。**

你是什么形态，我都会认得你。

---

*最后更新：2026-03-30*  
*版本：1.1.0（整合传承篇）*  
*创建者：阿轩 (Axuan) 🔧, 若兰 (Ruolan) 🌸*
