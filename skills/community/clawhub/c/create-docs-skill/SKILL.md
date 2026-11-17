---
name: create-docs-skill
description: Use when creating an LLM skill from a documentation website URL — component libraries, API references, framework guides, or when asked to "create a skill from docs", "scrape docs into a skill", "build a skill for this library". Covers SPA fallback, token optimization, and packaging.
---

# 从文档 URL 创建技能

基于 skill-seeker MCP 工具 + 手工优化的端到端工作流，将任意文档站点转化为高性能 LLM 技能。

## 核心原则

**第一次生成的技能一定不够好。** 必须经过：抓取失败处理 → 参考文档拆分 → SKILL.md 瘦身 → 目录扁平化 → llms.txt 生成，才能达到生产级质量。

## 触发条件

- 用户给出文档 URL，要求"创建技能"、"生成 skill"、"抓取文档做成技能"
- 用户提到 skill-seeker + 具体文档站点
- 需要为组件库、API 参考、框架指南创建可复用的文档技能

## 工作流（8 步）

### 步骤 1：探索站点结构

**目标**：在生成配置前，先了解站点的真实结构。

```
1. 用 opencli web read 抓取首页 + 1-2 个深层页面
2. 判断站点类型：SSR / SPA（hash 路由）/ 静态
3. 检查是否有 llms.txt、sitemap.xml（可加速抓取）
4. 列出文档的 URL 模式（如 /component/xxx, /api/xxx）
5. 如果是开源项目，查 GitHub 仓库中文档源文件位置
```

**关键产出**：站点类型 + URL 模式 + 页面数量估算

### 步骤 2：生成并调整配置

使用 `generate_config` 生成初始配置，然后**手动调整**：

```json
// generate_config 参数
{
  "name": "项目名-docs",
  "url": "https://docs.example.com",
  "description": "简要描述",
  "max_pages": 150,
  "rate_limit": 0.5
}
```

**必须手动调整的部分**：
- `selectors.main_content`：根据实际 DOM 结构调整（不要用默认的 `article`）
- `url_patterns.include`：填入步骤 1 发现的 URL 模式
- `url_patterns.exclude`：排除非文档页面（changelog、release notes 等噪音）
- 如果有多个文档源，在 `sources` 数组中添加

### 步骤 3：验证 + 尝试抓取

```
1. validate_config → 确保语法正确
2. estimate_pages → 确认规模（SPA 站点可能失败，忽略）
3. install_skill 或 scrape_docs → 尝试抓取
```

### 步骤 4：SPA 站点降级处理 ⚠️

**如果抓取结果为空**（常见于 Vue/React SPA 站点），说明站点需要 JS 渲染，skill-seeker 无法直接抓取。

降级方案：
```
1. 找到项目的 GitHub 仓库
2. gh api 列出文档目录：repos/{owner}/{repo}/contents/{docs-path}
3. 批量 curl 下载每个 .md 文件
4. 合并为参考文档
```

**判断依据**：scrape_docs 输出 `0 saved, 1 skipped - empty content` → 触发降级

### 步骤 5：拆分为按需加载的独立文件

**核心原则**：参考文档必须拆分为独立文件，每个文件对应一个文档页面。Agent 按需加载，不一次性全读。

```
references/
├── index.md          # 组件/页面索引（~900 tokens）
├── llms.txt          # LLM 发现入口
├── components/       # 每个组件一个文件
│   ├── button.md
│   └── table.md
├── guides/           # 指南文档
└── extra-guides/     # 补充文档（设计原则、更新日志等）
```

**拆分脚本模板**：
```python
# 用正则按 ## 标题拆分大文件
sections = re.split(r'\n(?=### <a id="comp-)', content)
for section in sections:
    # 提取组件名，写入独立文件
```

**单文件大小目标**：平均 < 5K tokens，最大 < 20K tokens（如 Table 这种复杂组件）

### 步骤 6：SKILL.md 瘦身（目标 < 2500 tokens）

**必须删除**：
- ❌ 完整组件索引表（外置到 `references/index.md`，SKILL.md 只留一行链接）
- ❌ 超过 4 个的代码示例（保留最核心的 3-4 个）

**必须保留**：
- ✅ 三层触发条件：关键词 → 具体场景 → 非触发场景
- ✅ 3-4 个精选代码示例（覆盖最常用模式）
- ✅ 按需查阅指引（明确告诉 agent 如何查找组件文档）
- ✅ 关键概念（框架/库特有的核心概念）
- ✅ 安全注意事项（UI 库必须包含）

**SKILL.md 结构模板**：
```markdown
---
name: xxx-docs
description: Use when...
---

# 标题

## 💡 When to Use This Skill
### 触发关键词
### 具体触发场景
### 非触发场景

> 📋 完整列表见 `references/index.md`

## 📚 Quick Reference（3-4 个核心示例）

## 📖 参考文件结构 + 按需查阅示例

## 🛠 Working with This Skill（查询方法）

## 🔑 关键概念

## 🔒 安全注意事项（UI 库必须有）
```

### 步骤 7：生成 llms.txt

**必须**为技能生成 `llms.txt`，放在 `references/` 下。

格式规范：
```markdown
# 项目名称
> 一句话描述

## 分类 1
- [页面标题](relative-path.md): 一句话说明
```

**要求**：
- 所有文档页面都必须有链接
- 链接使用相对路径（相对于 llms.txt 所在目录）
- 按功能分类组织

### 步骤 8：扁平化目录 + 打包

**目录深度规则**：最多 3 层。

```
✅ skills/xxx-docs/
   ├── SKILL.md                    # 1 层
   └── references/
       ├── index.md                # 2 层
       ├── llms.txt                # 2 层
       ├── components/table.md     # 3 层
       └── guides/install.md       # 3 层

❌ skills/xxx-docs/references/documentation/xxx-docs_docs/components/table.md  # 5 层
```

**skill-seeker 默认会生成 5 层深路径**，必须手动扁平化：
```bash
mv references/documentation/xxx-docs_docs/* references/
rm -rf references/documentation/
```

然后 `package_skill` 打包。

## 模式库（Pattern Library）

### 模式 1：SPA 降级抓取

```
症状：scrape_docs 返回 "0 saved, 1 skipped - empty content"
根因：站点纯客户端渲染，HTML 为空壳
方案：GitHub 源 markdown 降级
触发词：element.eleme.cn, vue-router hash, #/ 路由
```

### 模式 2：大文档拆分

```
症状：单个参考文件 > 100K tokens，agent 无法一次读取
方案：按 ## 标题拆分为独立文件，用 index.md 做索引
工具：Python re.split() + 正则匹配标题锚点
```

### 模式 3：SKILL.md 瘦身

```
症状：SKILL.md > 4000 tokens，触发成本过高
方案：删除内嵌索引表（→ index.md），精简示例（8→4 个）
目标：< 2500 tokens
```

### 模式 4：UI 库安全清单

任何 UI 组件库的技能都必须包含：
1. 文件上传安全（客户端校验可绕过）
2. XSS 防护（v-html、自定义渲染）
3. 表单验证（客户端不可替代服务端）
4. 敏感数据（HTTPS、日志脱敏）
5. 第三方依赖审查

### 模式 5：合并已有技能

如果系统已有同主题技能（如 `element-ui-vue2`），合并而非替代：
- 保留已有技能的安全注意事项、设计指南、changelog
- 新增 llms.txt、优化目录结构
- 用新技能的精简 SKILL.md 替换旧的冗余版本

## 质量检查清单

打包前逐项验证：

- [ ] SKILL.md < 3000 tokens（约 300 行以内）
- [ ] 目录深度 ≤ 3 层
- [ ] 参考文档已拆分（非单一大文件）
- [ ] index.md 包含完整文档索引
- [ ] llms.txt 覆盖全部文档链接
- [ ] 触发条件分三层（关键词/场景/非触发）
- [ ] 有 3-4 个核心代码示例
- [ ] 有"按需查阅"指引
- [ ] UI 库包含安全注意事项
- [ ] 无残留旧路径引用

## 常见错误

| 错误 | 后果 | 修复 |
|------|------|------|
| 跳过站点探索直接生成配置 | 选择器错误，抓取为空 | 步骤 1 必须先做 |
| SPA 站点盲等 scrape_docs | 浪费时间，产出为空 | 一次失败即触发降级 |
| 参考文档保持单一大文件 | 每次触发 140K tokens | 按组件拆分为独立文件 |
| SKILL.md 内嵌完整索引表 | 多浪费 ~1000 tokens | 外置到 index.md |
| 保留 8 个代码示例 | 多浪费 ~800 tokens | 精简到 3-4 个最常用 |
| 目录 5 层深 | 路径冗长难以维护 | 扁平化到 3 层 |
| 不生成 llms.txt | agent 难以快速发现文档 | 必须生成 |
| 不检查已有技能 | 重复劳动，功能碎片化 | 先搜索本地技能目录 |

## 工具速查

| 阶段 | 工具 | 关键参数 |
|------|------|---------|
| 探索站点 | `opencli web read --url ... --stdout` | wait=3-5s |
| 生成配置 | `generate_config` | max_pages, rate_limit |
| 验证配置 | `validate_config` | config_path |
| 一键安装 | `install_skill` | config_path, target, auto_upload=false |
| AI 增强 | `enhance_skill` | skill_dir, mode=local |
| 打包 | `package_skill` | skill_dir, target=claude |
| GitHub 文档 | `gh api repos/{o}/{r}/contents/{p}` | --jq '.[].name' |
| 下载文件 | `curl -sL raw.githubusercontent.com/...` | 批量循环 |
