# Academic Suite v3.5.0 — 发布说明

## 📦 发布信息

| 项目 | 内容 |
|------|------|
| **技能包名称** | academic-suite |
| **版本** | 3.5.0 |
| **发布日期** | 2026-05-14 |
| **作者** | eric-promax |
| **许可证** | MIT |
| **ClawHub 页面** | https://clawhub.ai/eric-promax/academic-suite |

---

## 🎯 发布内容

### 元技能包（Meta-Skill Package）

academic-suite 是一个元技能包，用于一键安装完整的 Academic Pipeline 生态系统。

### 包含技能（9 个）

| # | 技能 | 版本 | 用途 |
|---|------|------|------|
| 1 | academic-pipeline | v3.5 | 12 阶段全流程编排器 |
| 2 | ima-skills | v1.0+ | IMA 知识库 API 调用 |
| 3 | academic-search | v1.2.0 | 8 大平台文献检索 |
| 4 | deep-research | v2.0 | 深度研究（13-Agent） |
| 5 | academic-paper | v2.0 | 论文写作（12-Agent） |
| 6 | academic-paper-reviewer | v1.1 | 同行评审（5 人评审团） |
| 7 | humanizer | v1.0 | 英文去 AI 化（24 模式） |
| 8 | humanizer-zh | v1.0 | 中文去 AI 化（23 模式） |
| 9 | integrity_verification_agent | - | 学术诚信验证 |

---

## 📁 文件结构

```
academic-suite/
├── SKILL.md              # 主技能定义文件（9.3 KB）
├── README.md             # 项目说明文档（4.5 KB）
├── QUICKSTART.md         # 快速开始指南（5.1 KB）
├── clawhub.json          # ClawHub 元数据（1.8 KB）
├── install.sh            # 一键安装脚本（2.9 KB）
├── publish.sh            # 发布脚本（2.2 KB）
├── LICENSE               # MIT 许可证（1.1 KB）
└── RELEASE_NOTES.md      # 发布说明（本文件）
```

**总计：** 约 27 KB

---

## 🚀 安装方式

### 方式 1：ClawHub 命令（推荐）

```bash
clawhub install eric-promax/academic-suite
```

### 方式 2：运行安装脚本

```bash
cd ~/.openclaw/workspace/skills/academic-suite
bash install.sh
```

### 方式 3：手动安装

```bash
# 克隆或下载本目录到 ~/.openclaw/workspace/skills/academic-suite
# 然后运行
clawhub install .
```

---

## ✨ v3.5.0 新特性

### 1. 元技能包首次发布

- 一键安装 9 个技能（1 个主技能 + 8 个依赖）
- 自动处理依赖关系
- 提供安装验证

### 2. 阶段编号统一

- 从旧编号（0.5, 1, 2, 2.5, 3, 3', 4, 4', 4.5, 4.7, 5, 6）
- 统一为新编号（1-12 连续整数）

### 3. 启动配置增强

新增 5 项必填配置询问：
1. IMA 知识库路径
2. 论文类型（12 种可选）
3. 字数要求
4. 内容要求
5. 是否有开题报告

### 4. Stage 10 HUMANIZE

- 集成 humanizer + humanizer-zh
- 英文 24 种去 AI 化模式
- 中文 23 种去 AI 化模式
- 不修改引用、数据或事实陈述

### 5. 完善文档

- 飞书完整使用指南（15,000 字）
- README.md 项目说明
- QUICKSTART.md 快速开始指南
- 本发布说明

---

## 🔧 使用脚本

### 安装脚本（install.sh）

功能：
- 检查 clawhub 是否安装
- 检查登录状态
- 自动安装 8 个依赖技能
- 安装 academic-pipeline 主技能
- 验证安装结果

用法：
```bash
bash install.sh
```

### 发布脚本（publish.sh）

功能：
- 检查 clawhub 是否安装
- 检查登录状态
- 验证必要文件
- 执行发布到 ClawHub

用法：
```bash
bash publish.sh
```

---

## 📊 与单技能安装对比

| 特性 | academic-suite | 单独安装 |
|------|----------------|---------|
| 安装命令数 | 1 条 | 9 条 |
| 依赖处理 | 自动 | 手动 |
| 安装验证 | 自动 | 手动 |
| 文档完整性 | 完整 | 分散 |
| 适合用户 | 新手/快速部署 | 高级用户/定制 |

**推荐：** 90% 用户应使用 academic-suite

---

## 🎯 目标用户

### 适合使用 academic-suite 的用户

- ✅ 第一次使用 Academic Pipeline
- ✅ 希望快速部署完整环境
- ✅ 不想手动处理依赖关系
- ✅ 需要完整文档支持

### 适合单独安装的用户

- ✅ 已安装部分依赖技能
- ✅ 只需要特定技能（如只用 humanizer）
- ✅ 需要定制配置
- ✅ 高级用户

---

## 📝 发布检查清单

发布前请确认：

- [ ] SKILL.md 版本号正确（3.5.0）
- [ ] clawhub.json 版本号正确（3.5.0）
- [ ] 所有依赖技能列出完整（8 个）
- [ ] README.md 链接正确
- [ ] QUICKSTART.md 示例可用
- [ ] install.sh 可执行权限已设置
- [ ] publish.sh 可执行权限已设置
- [ ] LICENSE 文件存在
- [ ] 本地测试安装成功
- [ ] ClawHub 登录状态正常

---

## 🚀 发布流程

### 步骤 1：本地验证

```bash
cd ~/.openclaw/workspace/skills/academic-suite
bash install.sh
```

确认所有 9 个技能安装成功。

### 步骤 2：发布到 ClawHub

```bash
bash publish.sh
```

按提示确认发布。

### 步骤 3：验证发布

访问：https://clawhub.ai/eric-promax/academic-suite

确认页面显示正确信息。

### 步骤 4：测试安装

在新环境中测试：

```bash
clawhub install eric-promax/academic-suite
```

确认安装成功且所有依赖正确安装。

### 步骤 5：更新文档

- 更新飞书文档的"版本信息"章节
- 更新 GitHub 仓库的 README
- 在 ClawHub 讨论区发布发布说明

---

## 🐛 已知问题

### 问题 1：依赖技能版本冲突

**症状：** 安装的依赖技能版本过低

**解决：** 使用 `--force` 标志强制更新

```bash
clawhub install eric-promax/academic-suite --force
```

### 问题 2：ClawHub 未登录

**症状：** 发布或安装时提示未登录

**解决：** 先登录

```bash
clawhub login
```

### 问题 3：发布权限不足

**症状：** publish.sh 执行失败，提示权限不足

**解决：** 确认 clawhub.json 中的 author 字段与登录用户一致

---

## 📞 支持渠道

| 渠道 | 链接 |
|------|------|
| **GitHub Issues** | https://github.com/eric-promax/academic-agents/issues |
| **ClawHub 讨论** | https://clawhub.ai/eric-promax/academic-suite/discussions |
| **飞书文档评论** | https://feishu.cn/docx/GRb7dGij9olddExTBsCcpoaCnWg |

---

## 📅 后续计划

### v3.6.0（计划中）

- [ ] 支持多语言界面
- [ ] 增加更多论文类型模板
- [ ] 优化并行化执行
- [ ] 增加进度保存/恢复功能

### v4.0.0（长期计划）

- [ ] 支持协作写作（多人同时编辑）
- [ ] 集成更多学术数据库
- [ ] 增加图表自动生成
- [ ] 支持 LaTeX 模板定制

---

## 📄 许可证

MIT License

---

**发布人：** 大头虾 (eric-promax)  
**发布日期：** 2026-05-14  
**版本：** 3.5.0

*严谨是分析的基础，逻辑是推理的武器。* 🔮
