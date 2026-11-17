# 文档生命周期与生成流水线（docs-writer 增量方法论）

> 四个子技能各自负责一种文档（README / Changelog / API / 图表）。本文档补它们**装不下**的编排层：
> 一个真实项目该按什么顺序产出哪些文档、什么该自动生成、什么必须手写、跨文档怎么保持一致。

## 1. 决策树：这个项目需要哪些文档？

```text
新项目 / 文档缺失
├─ 是否对外提供代码或库？
│   ├─ 是 ↓
│   │   ├─ 有 HTTP/RPC 接口？ → API 文档（api-doc-generator）
│   │   └─ 有内部结构需讲解？ → 架构图（diagram-architect）
│   └─ 否 → 跳过对外文档
├─ 是否版本发布？
│   ├─ 是 → Changelog（changelog-writer）
│   └─ 否 → 可省
└─ 始终需要 → README（readme-generator）作为入口
```

**铁律**：README 是门面，永远先有；其余按「是否有接口 / 是否发布」决定是否生成，别为文档而文档。

## 2. 文档类型选型矩阵

| 项目特征 | 必产文档 | 可选 | 原因 |
|----------|----------|------|------|
| 开源库 | README + API + Changelog | 架构图 | 用户要能装、能懂接口、能看变更 |
| 内部工具 | README | 架构图 | 团队上手即可，接口少 |
| 微服务 | README + 架构图 + API | Changelog | 跨服务调用需图，接口需文档 |
| 纯前端 SPA | README + 架构图 | — | 无后端接口，重交互说明 |
| 一次性脚本 | README（简版） | — | 不值得全套文档 |

## 3. 生成顺序（避免返工）

```text
1. README 骨架（项目定位、安装、使用）
2. 代码结构分析 → 识别接口与模块
3. API 文档（若有接口）
4. 架构图（基于模块关系）
5. Changelog（发布时，从 commit 生成）
```

> 顺序很重要：先 README 定调，再 API/图补全细节，最后 Changelog 收尾。反向会导致重复劳动。

## 4. 自动生成 vs 手写（决策矩阵）

| 内容 | 自动生成 | 手写 | 判据 |
|------|----------|------|------|
| API 端点列表 | ✅ 从路由提取 | ❌ | 结构化的，机器比人准 |
| 安装/使用步骤 | ⚠️ 模板 + 人工补 | ✅ 关键步骤 | 命令固定但需场景说明 |
| 架构决策理由 | ❌ | ✅ | 含主观权衡，AI 编不出 |
| Changelog 条目 | ✅ 从 commit 分类 | ⚠️ 润色亮点 | 事实来自历史，表述需人 |
| 图表布局美化 | ❌ | ✅（或工具） | 自动布局常需调 |

**易错**：把「能自动生成」等同于「生成完就交付」。自动产出是草稿，人工润色关键段落（使用场景、坑）才是价值。

## 5. 跨文档一致性检查清单

文档之间互相引用，最容易出现漂移：

- [ ] README 里的「安装命令」与 API 文档示例的 base URL 一致
- [ ] 架构图里的模块名与代码目录名一致
- [ ] Changelog 的版本号与 git tag / README  badges 一致
- [ ] API 文档的鉴权方式与 README「认证」段一致
- [ ] 所有文档链接存活（用 [scripts/check_md_links.py](../scripts/check_md_links.py) 自动核查）

```bash
# 提交前批量核查仓库内所有 .md 的死链与残留待办标记
python3 scripts/check_md_links.py docs/ README.md
# 核查代码块是否已标注语言
python3 scripts/check_code_blocks.py docs/ README.md
```

## 6. 典型坑与规避

1. **README 写成功能清单**：用户要「怎么装怎么用」，不是「我们做了什么」——先场景后特性。
2. **API 文档与实现漂移**：代码改了接口文档没更 → 把 api-doc-generator 接进 CI，每次改路由重生成。
3. **Changelog 手填漏记**：依赖人记忆必漏 → 用 changelog-writer 从 Conventional Commits 生成。
4. **图表过度复杂**：一张图塞 20 个节点没人看得懂 → 按受众拆多张（概览图 + 细节图）。
5. **死链累积**：文档改了标题，旧链接变死链 → check_md_links.py 定期扫。
6. **代码块无语言标注**：渲染器无法高亮，且暴露作者疏忽 → check_code_blocks.py 强制标注。

## 7. 发布前文档速查

```text
README 存在且入口清晰？
├─ 有接口 → API 文档与实现一致？
├─ 有模块 → 架构图与目录一致？
├─ 要发布 → Changelog 与版本号一致？
└─ 全部链接存活、代码块已标注？（脚本核查通过）
```

## 8. 实战：为一个 Express 服务产出文档集

```bash
# 1) README 骨架（readme-generator 识别为 Node 项目）
python3 -m skills.readme_generator .

# 2) 从路由生成 OpenAPI（api-doc-generator 扫描 express 路由）
python3 -m skills.api_doc_generator --scan ./src/routes --out openapi.yaml

# 3) 架构时序图（diagram-architect，基于模块调用）
python3 -m skills.diagram_architect --flow login --out docs/login-seq.puml

# 4) 发布时生成 Changelog（changelog-writer 从 commit）
python3 -m skills.changelog_writer --since v1.0.0 --out CHANGELOG.md

# 5) 一致性核查
python3 scripts/check_md_links.py README.md openapi.yaml docs/
python3 scripts/check_code_blocks.py README.md
```

> 注意：上面的命令是示意，实际调用走各子技能。关键是**顺序与收尾核查**，而非具体 CLI。

## 9. CI 集成（文档门禁）

把链接与代码块核查接进 PR 检查，防止文档回归：

```yaml
# .github/workflows/docs.yml
name: docs-check
on: [pull_request]
jobs:
  lint-md:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: python3 scripts/check_md_links.py README.md docs/
      - run: python3 scripts/check_code_blocks.py README.md docs/
```

规则文件 [assets/markdown-lint-rules.json](../assets/markdown-lint-rules.json) 是脚本的唯一事实来源，团队调整「允许协议/必检 token」只改它一处。

## 10. 典型坑与规避（续）

7. **文档与代码同仓但不同步**：代码改接口，文档 PR 另开 → 用上面的 CI 在改路由的 PR 里也跑 api 生成。
8. **Changelog 把内部提交暴露给用户**：`chore`/`refactor` 不该进用户向 Release Notes → changelog-writer 按类型过滤。
9. **架构图用中文节点名但渲染器乱码**：PlantUML 需声明 `skinparam` 字体；Mermaid 在 GitHub 原生支持中文。
10. **README 堆截图**：截图易过期且不可检索 → 用文字+代码块，图只放架构类。

## 11. 可勾选清单

- [ ] 按项目特征选定文档集合（不盲产全套）
- [ ] 生成顺序正确：README → 分析 → API/图 → Changelog
- [ ] 自动产出已人工润色关键场景段落
- [ ] 跨文档命名/版本/URL 一致
- [ ] 死链与残留待办标记已用脚本扫清
- [ ] 代码块全部标注语言
- [ ] 复杂图表已按受众拆分
- [ ] 发布前跑 check_md_links / check_code_blocks
- [ ] 文档核查已接入 CI（PR 级）
- [ ] Changelog 已过滤内部提交类型

## 12. 受众分层：同一项目给不同的人看不同文档

| 受众 | 关注点 | 主文档 | 写法 |
|------|--------|--------|------|
| 新贡献者 | 怎么跑起来、代码结构 | README + 架构图 | 步骤化、少术语 |
| API 调用方 | 端点、参数、示例 | API 文档 | 请求/响应示例优先 |
| 维护者 | 变更、风险、决策 | Changelog + ADR | 事实 + 理由 |
| 决策者 | 价值、范围 | README 摘要 | 一句话价值主张 |

> 一份 README 同时服务前三类会顾此失彼。用 README 做入口与导航，把深层内容分流到 API/图/Changelog，再用内部链接串起来（链接存活由脚本保障）。

## 13. 怎么判断文档「够好」

不靠字数，靠可操作性：

- 新人按 README 能在 10 分钟内跑通「安装→使用」最小路径
- API 文档每个端点都有可复制的请求示例（curl/SDK）
- 改任一接口后，对应文档在 CI 里被重新生成且通过核查
- 死链/未标注代码块在 PR 阶段被拦截，不进 main

达到这四条，文档质量即达标；否则回到第 4-6 节补对应环节。

## 相关子技能与层次边界

本文是 docs-writer 的**编排层**方法论：子技能各自负责「怎么生成单类文档」，本文负责「一个真实项目该按什么顺序产出哪些文档、什么自动/什么手写、跨文档如何保持一致」。

- 直接服务子技能：
  - [skills/readme-generator/](../skills/readme-generator/SKILL.md)（文档入口，生成顺序第 1 步；受众分层主文档）
  - [skills/changelog-writer/](../skills/changelog-writer/SKILL.md)（发布环节，生成顺序第 5 步；版本号一致性）
  - [skills/api-doc-generator/](../skills/api-doc-generator/SKILL.md)（生成顺序第 3 步；与实现一致性）
  - [skills/diagram-architect/](../skills/diagram-architect/SKILL.md)（生成顺序第 4 步；与代码目录一致性）
- 兄弟参考（同层增量方法论，按需交叉阅读）：
  - [references/api-doc-authoring-playbook.md](api-doc-authoring-playbook.md)（API 文档撰写质量）
  - [references/diagram-selection-guide.md](diagram-selection-guide.md)（图表选型与绘制）
- 配套确定性资产（根 SKILL.md 内置脚本/模板）：
  - [scripts/check_md_links.py](../scripts/check_md_links.py) — 跨文档死链/残留核查（第 5/9 节）
  - [scripts/check_code_blocks.py](../scripts/check_code_blocks.py) — 代码块语言标注核查（第 5/9 节）
  - [assets/markdown-lint-rules.json](../assets/markdown-lint-rules.json) — 上述脚本的规则唯一事实来源
  - [assets/readme-template.md](../assets/readme-template.md) — README 标准模板（锚点/代码块合规范本）
