# AutoResearchClaw 技能整合包

**整合日期:** 2026-03-27  
**来源版本:** AutoResearchClaw v0.3.2  
**整合者:** 智能体 for 用户

---

## 整合概述

从 AutoResearchClaw 项目提取并整合了以下核心功能为 OpenClaw 技能：

| 技能 | 功能 | 状态 |
|------|------|------|
| **autonomous-research** | 23 阶段完整科研流水线 | ✅ 已创建 |
| **literature-search-pro** | 多源文献搜索（OpenAlex/S2/arXiv） | ✅ 已创建 |
| **experiment-design** | 实验设计最佳实践 | 📋 待创建 |
| **paper-latex-gen** | LaTeX 论文生成 | 📋 待创建 |
| **citation-verifier** | 引用验证 | 📋 待创建 |

---

## 快速开始

### 1. 安装依赖

```powershell
# 进入技能目录
cd D:\Personal\OpenClaw\skills\autonomous-research

# 安装 Python 依赖（如果需要执行实验）
pip install -e .

# 进入文献搜索技能目录
cd D:\Personal\OpenClaw\skills\literature-search-pro

# 安装 Python 依赖
pip install requests
```

### 2. 配置 API Key

**方式 1: 环境变量（推荐）**
```powershell
$env:OPENAI_API_KEY="sk-..."
```

**方式 2: 配置文件**
编辑 `skills/autonomous-research/config.yaml`:
```yaml
llm:
  api_key: "sk-..."
```

### 3. 测试运行

**测试文献搜索：**
```
搜索文献：graph neural network drug discovery
```

**测试自主科研：**
```
研究：基于深度学习的结构损伤识别
```

---

## 核心功能详解

### 1. autonomous-research 技能

**输入:** 一个研究想法  
**输出:** 完整学术论文

**23 阶段流程：**
```
Phase A: 研究范围 (1-2)
  → 主题定义、问题拆解

Phase B: 文献发现 (3-6)
  → 搜索策略、收集、筛选、提取

Phase C: 知识综合 (7-8)
  → 聚类分析、假设生成

Phase D: 实验设计 (9-11)
  → 实验方案、代码生成、资源规划

Phase E: 实验执行 (12-13)
  → 运行实验、迭代优化

Phase F: 分析决策 (14-15)
  → 结果分析、继续/优化/转向决策

Phase G: 论文写作 (16-19)
  → 大纲、初稿、同行评审、修改

Phase H: 最终化 (20-23)
  → 质量检查、归档、导出、引用验证
```

**输出文件：**
- `paper_draft.md` - 完整论文
- `paper.tex` - LaTeX 源码
- `references.bib` - 参考文献
- `charts/` - 图表
- `experiment_runs/` - 实验代码和结果

### 2. literature-search-pro 技能

**功能：**
- 三源搜索（OpenAlex + Semantic Scholar + arXiv）
- 自动去重（DOI/arXiv ID/标题）
- 引用数排序
- 智能缓存

**示例：**
```
搜索文献：振动台子结构试验
搜索 2024-2026 年的 RTHS 文献
用 arXiv 搜索最新预印本
```

---

## 使用场景

### 场景 1: 快速文献调研

```
1. 用 literature-search-pro 搜索相关文献
2. 快速浏览标题和摘要
3. 筛选高引用论文精读
4. 用 zotero-manager 导入 Zotero
```

### 场景 2: 完整研究项目

```
1. 用 literature-search-pro 探索领域
2. 确定具体研究问题
3. 用 autonomous-research 执行完整研究
4. 审核生成的论文和实验
5. 手动修改和完善
```

### 场景 3: 论文写作辅助

```
1. 用 autonomous-research 生成初稿
2. 用 research-paper-writer 润色
3. 手动检查引用和逻辑
4. 用 overleaf 技能同步到 Overleaf
```

---

## 配置说明

### autonomous-research 配置

编辑 `skills/autonomous-research/config.yaml`:

```yaml
# LLM 配置
llm:
  base_url: "https://api.openai.com/v1"
  api_key_env: "OPENAI_API_KEY"
  primary_model: "gpt-4o"

# 实验模式
experiment:
  mode: "simulated"  # simulated | sandbox | ssh_remote

# 论文模板
paper:
  template: "neurips"  # neurips | icml | iclr
```

### literature-search-pro 配置

编辑 `skills/literature-search-pro/config.json`:

```json
{
  "default_limit": 10,
  "year_min": 2020,
  "s2_api_key": ""  # 可选，提高 S2 限额
}
```

---

## 注意事项

### 安全

⚠️ **代码执行风险：**
- 实验代码在本地执行
- 首次运行建议使用 `simulated` 模式
- 审查生成的代码后再执行

### API 限额

| 服务 | 限额 | 建议 |
|------|------|------|
| OpenAI | 取决于账户 | 监控使用量 |
| OpenAlex | 10K/天 | 最宽松 |
| Semantic Scholar | 1K/5 分钟 | 配置 API Key |
| arXiv | 1 次/3 秒 | 自动限流 |

### 输出验证

**必须检查：**
1. 引用真实性（抽查 3-5 篇）
2. 实验结果合理性
3. 贡献声明有证据支持

---

## 故障排除

### 常见问题

**Q: 技能不响应**
- 检查 OpenClaw 是否正确加载技能
- 查看 `skills/*/package.json` 是否正确

**Q: API 错误**
- 检查 API Key 是否有效
- 检查网络连接
- 查看技能日志

**Q: 实验执行失败**
- 检查 Python 环境
- 尝试 `simulated` 模式
- 查看详细错误日志

### 日志位置

- autonomous-research: `skills/autonomous-research/researchclaw.log`
- literature-search-pro: 控制台输出

---

## 后续计划

### 待整合技能

1. **experiment-design** - 实验设计最佳实践库
2. **paper-latex-gen** - LaTeX 模板和生成
3. **citation-verifier** - 引用验证工具
4. **overleaf-sync** - Overleaf 同步

### 改进方向

1. 中文界面优化
2. 国内数据库集成（CNKI 等）
3. 用户研究领域模板
4. 与现有技能深度集成

---

## 参考资源

- **AutoResearchClaw 原始项目:** https://github.com/aiming-lab/AutoResearchClaw
- **集成指南:** https://github.com/aiming-lab/AutoResearchClaw/blob/main/docs/integration-guide.md
- **中文测试指南:** https://github.com/aiming-lab/AutoResearchClaw/blob/main/docs/TESTER_GUIDE_CN.md
- **论文展示:** https://github.com/aiming-lab/AutoResearchClaw/blob/main/docs/showcase/SHOWCASE.md

---

## 更新日志

### v1.0.0 (2026-03-27)
- ✅ 创建 autonomous-research 技能
- ✅ 创建 literature-search-pro 技能
- ✅ 配置模板和文档
- 📋 待创建：experiment-design、paper-latex-gen、citation-verifier

---

**整合者:** 智能体  
**联系方式:** 飞书 User ID: `ou_0bf9ce2a34f19ee884997c853deb70c4`

