# Academic Suite v3.5.0 — 快速开始指南

## 🚀 5 分钟快速上手

### 步骤 1：安装（1 分钟）

```bash
clawhub install eric-promax/academic-suite
```

等待安装完成，会自动安装 9 个技能（1 个主技能 + 8 个依赖）。

### 步骤 2：验证安装（30 秒）

```bash
ls ~/.openclaw/workspace/skills/ | grep -E "academic|humanizer|ima|integrity"
```

应看到 9 个技能名称。

### 步骤 3：启动 Pipeline（30 秒）

在 OpenClaw 对话中输入：

```
我要用 Academic Pipeline 写一篇论文
```

系统会自动询问 5 项配置：

1. **IMA 知识库路径** — 如"个人知识库/eric/毕业论文"，无则填"无"
2. **论文类型** — 学位/课程/期刊/会议/报告/综述/实证/理论/案例/方法/应用/其他
3. **字数要求** — 如 8000/50000/无限制
4. **内容要求** — 理论框架、方法论、特定章节等
5. **是否有开题报告** — 是/否

### 步骤 4：开始写作（剩余时间）

系统会自动执行 12 个阶段，每个阶段完成后会等待您确认。

---

## 📊 12 阶段概览

| 阶段 | 名称 | 预计耗时 | 说明 |
|------|------|---------|------|
| 1 | LITERATURE SEARCH | 5-10 分钟 | 文献检索（IMA + 8 大平台） |
| 2 | RESEARCH | 10-20 分钟 | 深度研究分析 |
| 3 | WRITE | 20-40 分钟 | 论文撰写 |
| 4 | INTEGRITY ✦ | 5-10 分钟 | 学术诚信验证（强制） |
| 5 | REVIEW ✦ | 10-15 分钟 | 5 人同行评审（强制） |
| 6 | RE-REVIEW ✦ | 5-10 分钟 | 验证评审（强制） |
| 7 | REVISE | 15-30 分钟 | 修订 |
| 8 | RE-REVISE | 15-30 分钟 | 二次修订（可选） |
| 9 | FINAL INTEGRITY ✦ | 5-10 分钟 | 最终验证（强制） |
| 10 | HUMANIZE ✦ | 5-10 分钟 | 去 AI 化处理（强制） |
| 11 | FINALIZE ✦ | 5-10 分钟 | 定稿（MD+DOCX+LaTeX+PDF） |
| 12 | PROCESS SUMMARY | 2-5 分钟 | 过程记录 |

**总耗时：** 约 2-4 小时（8000 字论文）

✦ = 强制门控，不可跳过

---

## 💡 常用命令

### 查看进度

```
status
```

### 暂停管道

```
pause
```

### 恢复管道

```
resume
```

### 跳过当前阶段（非强制阶段）

```
skip
```

### 调整模式

```
切换到 full 模式
```

---

## 🎯 典型使用场景

### 场景 1：MBA 课程论文（8000 字）

```
我要用 Academic Pipeline 写一篇关于"中国股市炒新现象"的 MBA 课程论文，
8000 字左右，基于行为金融学理论框架
```

**配置：**
- IMA 路径：无
- 论文类型：课程论文
- 字数：8000 字
- 内容要求：基于行为金融学理论框架，采用案例 + 实证分析
- 开题报告：否

**预计耗时：** 2-3 小时

---

### 场景 2：硕士学位论文（5 万字）

```
我要用 Academic Pipeline 写一篇硕士学位论文，
关于"互联网企业进入金融领域研究——以腾讯金融为例"，
5 万字，基于组织生态理论
```

**配置：**
- IMA 路径：个人知识库/eric/毕业论文
- 论文类型：学位论文
- 字数：50000 字
- 内容要求：基于组织生态理论，采用案例 + 文献分析法
- 开题报告：是（上传文件）

**预计耗时：** 6-10 小时（可分多次完成）

---

### 场景 3：期刊论文修订

```
我收到了审稿人的修改意见，帮我修订论文
```

系统自动从 Stage 7 REVISE 开始。

---

### 场景 4：已有论文，进入评审

```
我已经有一份论文草稿，帮我进入评审流程
```

系统自动从 Stage 4 INTEGRITY 开始。

---

## ⚠️ 注意事项

### 1. 强制门控不可跳过

Stage 4、5、6、9、10、11 是强制门控，必须用户明确确认才能继续。

### 2. 修订最多 2 轮

Stage 7 + Stage 8 最多各 1 轮，之后直接进入 Stage 9。

### 3. 去 AI 化不修改引用和数据

humanizer 只优化表达风格，不修改引用、数据或事实陈述。

### 4. PDF 从 LaTeX 编译

禁止 HTML-to-PDF，确保格式规范。

### 5. 预算透明

启动时会估算 token 成本，确认后才开始。

---

## 🐛 常见问题

### Q: 安装后提示依赖缺失？

```bash
clawhub install eric-promax/academic-suite --force
```

### Q: Stage 1 无法连接 IMA？

检查 API Key 和知识库路径，或输入"无"跳过。

### Q: 去 AI 化阶段失败？

```bash
clawhub install humanizer
clawhub install humanizer-zh
```

### Q: 可以中途退出吗？

可以。系统会保存状态，下次输入"resume"恢复。

### Q: 可以跳过某个阶段吗？

非强制阶段可以跳过，但 Stage 4、5、6、9、10、11 不可跳过。

---

## 📚 更多资源

| 资源 | 链接 |
|------|------|
| **完整使用指南** | https://feishu.cn/docx/GRb7dGij9olddExTBsCcpoaCnWg |
| **GitHub 仓库** | https://github.com/eric-promax/academic-agents.git |
| **ClawHub 页面** | https://clawhub.ai/eric-promax/academic-suite |
| **问题反馈** | https://github.com/eric-promax/academic-agents/issues |

---

**维护者：** 大头虾 (eric-promax)  
**最后更新：** 2026-05-14

*严谨是分析的基础，逻辑是推理的武器。* 🔮
