---
subdomain: code-comment
version: 1
updated: 2026-11-17
---

# code-comment — 代码注释

## 定位与心智模型

代码注释是「代码无法自含的信息」的最小化投放载体，不是代码的解说词。Google 官方注释谱系（本域权威框架）[官方文档](https://google.github.io/styleguide/docguide/best_practices.html)：

1. **meaningful names**：好命名让代码自身传达信息——官方表述 "allows the code to convey information that would otherwise be relegated to comments"（本可沦为注释的信息由命名承担，否则才轮到注释）
2. **inline comments**：行内注释提供**代码无法包含的信息**，典型如 why（决策、约束、坑）
3. **method/class API 文档**：方法/类级文档是**契约**——what / how / gotchas / exceptions；官方明确 **"Why" explanations are for inline comments**（why 归行内注释，API 文档归契约）
4. **README → docs**：项目级说明与文档站

核心判据：改好代码后仍然需要的信息才配成为注释；其余交给命名、结构、类型、VCS 与文档体系。

适用边界：本子域覆盖行内注释、文件头、TODO/FIXME 标记与各语言文档注释惯例定位；公共 API 文档标签体系（TSDoc 等）细节归 `api-doc-gen`；设计决策记录归 `adr-changelog`；注释的文风术语纪律归 `doc-quality`。

操作化工具：what / how / why / context 四分法（价值排序 why > context > how > what）——官方谱系的应用层变体，非权威分类学（映射关系见「冲突消解记录」）[模型经验]。

## 法则

**CC-1 [GLOBAL]** **MUST**: 注释写代码表达不了的——why > context > how > what。决策、约束、外部关联是注释的本职；what 复读是噪音；能进命名/结构/类型的信息不写注释。
- 违反后果: what 复读噪音淹没高价值信息，读者对注释建立「可忽略」惯性，真正要紧的 why 守卫也被跳过。
- 溯源: [官方文档](https://google.github.io/styleguide/docguide/best_practices.html)（inline comments 提供代码无法包含的信息，如 why）+ [模型经验]（elicited/01、02、07-laws）。

**CC-2 [GLOBAL]** **NEVER**: why 无源不写。决策理由、版本历史、issue 号、规范条款号是事实数据；无源时只能写「待确认」，不得用社区最优解释填补项目私有决策。
- 违反后果: 后人以编造的错误前提重构；issue 号/条款号幻觉让读者查证失败，注释从资产变误导源。
- 溯源: [模型经验]（elicited/05-ai-comment-mistakes）；与官方「行为文档化须有测试佐证」的事实纪律精神一致 [官方文档](https://google.github.io/styleguide/docguide/best_practices.html)。

**CC-3** **MUST**: 求注释先跑决策序——改名 > 提函数 > 重结构 > 写注释。注释恰当性测试：重构到最佳状态后仍有信息量的注释才配存在。
- 违反后果: 用注释补偿坏命名/长函数，噪音随代码膨胀；结构问题被注释掩盖，函数继续变长。
- 溯源: [官方文档](https://google.github.io/styleguide/docguide/best_practices.html)（命名层 "allows the code to convey information that would otherwise be relegated to comments"——好命名让代码自身传达信息，否则才轮到注释）+ [模型经验]（elicited/02）。

**CC-4** **MUST**: 好注释是幂律分布。多数代码零注释，少数关键处（反直觉代码/外部约束/算法/修复说明）浓注释；「每函数至少一条」与「逐行注释」都是反模式。
- 违反后果: 均匀分布稀释信噪比；review 盲区扩大，漂移注释成倍产生。
- 溯源: [模型经验]（elicited/02、05）。

**CC-5** **MUST**: 反直觉代码必须有 why 守卫。看似多余/怪异的代码（无操作垫片、多余断言、重复初始化）没有 why 注释活不过两次重构——「看不懂就删」是后人理性行为，守卫是作者义务。
- 违反后果: 兼容垫片被后人「清理」，隐藏 bug 复活，事故重演。
- 溯源: [模型经验]（elicited/01 深度轮）。

**CC-6** **MUST**: 代码变更与注释同步。改代码必查周边注释；注释与代码矛盾时注释必错（代码是事实）；修复 bug 时更新而非删除仍有效的旧约束注释。
- 违反后果: 注释漂移成误导性文档，读者按旧注释理解新代码；失修文档比没有文档更糟。
- 溯源: [官方文档](https://google.github.io/styleguide/docguide/best_practices.html)（Update Docs with Code：文档与代码同一 CL 变更；Minimum Viable Documentation：新鲜准确优先）+ [模型经验]（elicited/01、05）。

**CC-7** **NEVER**: 僵尸代码删，历史归 VCS。注释掉的代码、注释里的版本史/作者/日期一律删除——git 记录一切；「以防万一」是不信任 VCS 的心理缺陷。
- 违反后果: 注释块僵尸代码存活数年造成双份维护心智；文件膨胀，读者疑惑哪份是真相。
- 溯源: [模型经验]（elicited/01）；删除原因归 commit message——格式参照 [官方文档](https://cbea.ms/git-commit)（Google 官方推荐的 commit message 写法）。

**CC-8** **MUST**: TODO 最小完备三要素——责任人 + 可行动描述 + 追踪引用。`TODO(owner): 动作 (#issue)`；裸 TODO 视为 lint 违例；FIXME 带严重度意识，HACK 必须写「正确做法是什么」。
- 违反后果: 裸 TODO 无主无号永不清偿，「待办」变「永久装饰」；`grep TODO` 出数百条无法转成工作项。
- 溯源: [模型经验]（elicited/03；社区惯例，无官方标准）。

**CC-9** **MUST**: 标记必须清偿。定期 TODO 审查（做/删/降级）；issue 关闭时同步清理关联标记；修复成本低于上下文切换成本时禁止用标记逃避。
- 违反后果: 标记只增不减等于没有机制；致命缺陷与美化项混排，前者被淹没。
- 溯源: [模型经验]（elicited/03）。

**CC-10** **MUST**: 文件头 ≤5 行有效信息，四职责为限——模块角色/架构约束/ADR 指针/版权。变更历史、教程、API 参考禁止入文件头；深论证抽 ADR 外链（文件头是指针层不是存储层）；文件名自明时头注释可为零。
- 违反后果: boilerplate 长头注释成视觉盲区，重构后最先过期，读者被误导。
- 溯源: [模型经验]（elicited/04-file-header-scope）。

**CC-11** **MUST**: 骨架生成的未实现处集中声明，不撒裸 TODO。未实现点用显式抛错（`NotImplementedError` 等）+ 集中清单声明，不逐点撒 `TODO: implement`；责任人名/追踪号无真实来源不写。
- 违反后果: 散装 `TODO: implement` 无主化；虚构 owner/issue 号污染追踪系统。
- 溯源: [模型经验]（elicited/03、05）。

**CC-12** **MUST**: 入乡随俗——原则跨语言，惯例按语言。JSDoc/TSDoc、Python docstring（三派系选一）、Go doc comment（极简叙事/紧贴声明）、Rust doc（`///` + doctest）各按生态惯例；写文档注释的前提是提取工具链在位（写了无渲染 = 带格式的普通注释）；monorepo 共享原则层（CC-1~CC-11），惯例层按语言。
- 违反后果: 跨语言套用自家惯例（Python 写 JSDoc 标签）——工具不识别，渲染为纯文本噪音。
- 溯源: [模型经验]（elicited/06-language-comment-styles）；各语言惯例细节以 [官方文档](https://google.github.io/styleguide/) 对应指南为准（索引确认在位，正文未逐语言抓取）。

## 核心概念速览

| 概念 | 一句话定义 |
|---|---|
| 官方注释谱系 | names → inline comments → method/class API 文档 → README → docs 的信息分层投放框架 [官方文档](https://google.github.io/styleguide/docguide/best_practices.html) |
| 四分法（what/how/why/context） | 注释内容四层价值模型，why > context > how > what；官方谱系的操作化变体 [模型经验] |
| 注释恰当性测试 | 重构这段代码到最佳状态后仍有信息量的注释才配存在 [模型经验] |
| 自文档化代码 | 用命名/结构/类型让代码自明，注释退居代码外信息 [官方文档](https://google.github.io/styleguide/docguide/best_practices.html) |
| 幂律分布 | 好注释形态：多数代码零注释，少数关键处浓注释 [模型经验] |
| why 守卫 | 反直觉代码上方的决策/约束注释，防止后人误删 [模型经验] |
| 注释漂移 | 代码变更后注释未同步，注释成为错误文档 [模型经验] |
| 僵尸代码 | 注释掉的代码块留存「以防万一」——应删，历史归 VCS [模型经验] |
| TODO/FIXME/HACK/XXX | 代码内待办标记，社区惯例无官方标准 [模型经验] |
| 文档注释（docstring） | 服务于工具提取（godoc/rustdoc/Sphinx/TypeDoc）的结构化注释 [模型经验] |
| ADR 指针层 | 文件头只指向 ADR 不存储 ADR [模型经验] |
| Minimum Viable Documentation | 官方文档哲学：小而新鲜准确 > 大而失修 [官方文档](https://google.github.io/styleguide/docguide/best_practices.html) |

## 最佳实践

### 场景 1：被要求「给这段代码加注释」

推荐路径（源于 [CC-3]）：
1. 先跑决策序：注释解释命名 → 改命名；注释块分节 → 提函数；结构混乱 → 重结构。
2. 仍有代码外信息（决策/约束/坑/外部关联）→ 写行内注释，只写代码表达不了的层（[CC-1]）。
3. 拒绝均匀分布：不为「每函数至少一条」补注释（[CC-4]）。

```ts
// ✗ don't：what 复读 + 注释补偿坏命名
// 获取数据
function procData2(u) { /* ... */ }

// ✓ do：改名自明；仅保留代码外信息（why/context）
function fetchActiveUsers() { /* ... */ }

// 入参已在上游做 XSS 清洗，此内部接口不再校验
function renderRawProfile(html: string) { /* ... */ }
```

边界条件：正则、位掩码、复杂表达式等「代码无法自明的域转换」允许 what/how 层注释。
来源：[官方文档](https://google.github.io/styleguide/docguide/best_practices.html) + [模型经验]（elicited/01、02）。

### 场景 2：写反直觉代码（垫片/绕过/看似多余）

推荐路径（源于 [CC-5]、[CC-2]）：
1. 在代码上方写 why 守卫：决策 + 约束 + 追踪引用。
2. why 内容无真实来源时写 `// 原因待确认`，不得编造。
3. 引用只到可验证粒度（issue 号/文档级），不凭记忆写条款号。

```ts
// ✗ don't：裸怪代码，活不过两次重构
await new Promise(r => setTimeout(r, 0));

// ✓ do：why 守卫
// 事件循环让位：等 React 提交批次完成再读 DOM，否则断言读到旧树 (#3284)
await new Promise(r => setTimeout(r, 0));
```

边界条件：守卫内容必须是项目事实；社区通用解释（「性能更好」）不可冒充决策记录。
来源：[模型经验]（elicited/01、05）。

### 场景 3：当下做不完，要留标记

推荐路径（源于 [CC-8]、[CC-9]、[CC-11]）：
1. 判断修复成本：低于上下文切换成本 → 当下修，不留标记。
2. 留标记则写三要素：`TODO(owner): 可行动描述 (#issue)`。
3. issue 关闭时同步清理关联标记；定期 TODO 审查（做/删/降级）。

```python
# ✗ don't：裸 TODO
# TODO 优化
def refresh(self): ...

# ✓ do：三要素齐全，无源不编
# TODO(zhang): 缓存失效策略上线后移除全量刷新 (#1423)
def refresh(self): ...
```

边界条件：骨架生成的未实现处用显式抛错 + 集中清单声明（[CC-11]）；owner/issue 号无真实来源不写。
来源：[模型经验]（elicited/03、05；社区惯例，无官方标准）。

### 场景 4：写文件/模块头注释

推荐路径（源于 [CC-10]）：
1. 按四职责自检（模块角色/架构约束/ADR 指针/版权），逐项问「文件名说得清吗」。
2. 有效信息 ≤5 行；文件名+导出名自明时头注释可为零（除版权行）。
3. 深论证抽 ADR，文件头只留一句指针。

```ts
// ✗ don't：boilerplate + 变更历史
// Author: ...
// 2024-06-14 zhang 修改
// 2025-02-01 li 修改
// 本模块负责……

// ✓ do：角色一句 + 约束 + ADR 指针
// 状态持久层：仅被 store 层导入，不依赖 DOM。
// 状态方案决策：/docs/adr/0012-state-management.md
```

边界条件：能被工具强制的约束（依赖规则）优先用架构约束测试（dependency-cruiser 类）而非注释——注释是弱约束层。
来源：[模型经验]（elicited/04）。

### 场景 5：为公共方法/类写文档注释

推荐路径（源于 [CC-12]）：
1. API 文档层写契约：what / how / gotchas / exceptions。
2. why 不进 API 文档——官方明确 "Why" explanations are for inline comments；why 写在实现处行内。
3. 惯例按语言：先读目标语言工具产出（godoc/rustdoc/Sphinx/TypeDoc 渲染结果）再定格式；确认提取工具链在位。

```ts
/**
 * 分页拉取用户列表。
 * 契约：按 createdAt 倒序返回；page 越界返回空数组而非报错（gotcha）。
 * 标签体系细节见 api-doc-gen 子域。
 */
export function fetchUsers(page: number): Promise<User[]>;
```

边界条件：无提取工具链的项目，文档注释只是带格式的普通注释——先补工具链或降级为普通注释。
来源：[官方文档](https://google.github.io/styleguide/docguide/best_practices.html) + [模型经验]（elicited/06）。

### 场景 6：修 bug / 重构时的注释维护

推荐路径（源于 [CC-6]、[CC-7]）：
1. 改代码时同步查周边注释；矛盾时以代码为准修注释。
2. 修 bug 时更新而非删除仍有效的旧约束注释。
3. 删除死代码不留注释残骸；删除原因写进 commit message（参照 [官方文档](https://cbea.ms/git-commit)，Google 官方推荐）。

```ts
// ✗ don't：僵尸代码 + 注释历史
// const oldParser = new Parser(); // 2024 旧方案，留着以防万一

// ✓ do：删除 + commit message 记录原因
// （代码删除；commit: "remove legacy parser: superseded by streaming parser (#987)"）
```

边界条件：官方 Update Docs with Code 原则——文档与代码同一 CL 变更，reviewer 有权要求同步；对注释同样适用。
来源：[官方文档](https://google.github.io/styleguide/docguide/best_practices.html) + [模型经验]（elicited/01）。

### 场景 7：多语言 monorepo 的注释纪律

推荐路径（源于 [CC-12]）：
1. 原则层跨语言统一：CC-1~CC-11 全语言适用。
2. 惯例层按语言：JS/TS 用 JSDoc/TSDoc 标签；Python 三派系选一（Google/reST/NumPy）全局统一；Go 极简紧贴；Rust `///` + doctest。
3. 惯例例外清单显式写进贡献指南。

边界条件：不为省力跨语言强推统一模板；各语言惯例细节以 [官方文档](https://google.github.io/styleguide/) 对应指南为准。
来源：[模型经验]（elicited/06）。

## 高频坑点（速查）

### Top 1：why 编造（AI 本域最高危）

- 症状：`// 使用 IntersectionObserver 而非 scroll 事件，因为性能更好`（项目真实决策可能是兼容性/包体）；`// 见 #1234`（编号不存在）；`// 注意：此函数不能在 SSR 中调用`（并非真实约束）。
- 根因：AI 用「社区最优解释」填补未知的项目私有决策；why 是最高价值层同时也是模型最无知的层；issue 号/条款号是幻觉重灾区（文档存在性记忆 > 章节号记忆 > 条款号记忆）。
- 修复：why 无源只写 `// 原因待确认`；追踪号/条款号是事实数据，无源不写；项目约束须有源（测试/文档/报错记录），通用危险模式进文档或 lint 不进注释。
- 法则：[CC-2]

### Top 2：逐行 what 复读

- 症状：被要求「加注释」后每行配直译（`// 定义变量` `// 遍历数组`）；每函数至少一条注释。
- 根因：「注释率=质量」错误 KPI + 逐行注释生成模式 + 教学欲（给代码配解说；注释读者是维护者不是学生）。
- 修复：先跑决策序（改名 > 提函数 > 重结构 > 写注释）[CC-3]；只写代码表达不了的层 [CC-1]；接受幂律分布 [CC-4]。
- 法则：[CC-1] [CC-3] [CC-4]

### 速查表

| 症状 | 根因 | 修复 | 法则 |
|---|---|---|---|
| 注释描述与代码行为矛盾 | 改代码未同步注释（注释在 review 中是视觉盲区） | 代码为准，更新/删除注释；改代码必查周边 | [CC-6] |
| 注释掉的代码存活数年 | 不信任 VCS | 删除；原因写进 commit message | [CC-7] |
| `grep TODO` 数百条无法转工作项 | 裸 TODO 缺三要素 | `TODO(owner): 动作 (#issue)` + 定期清偿 | [CC-8] [CC-9] |
| issue 已关但 TODO 还在 | 标记与追踪脱钩 | issue 关闭时同步清理关联标记 | [CC-9] |
| 文件头 15 行 boilerplate 与首屏代码重复 | 模板复制；版权需求与文档需求混同 | 压缩到四职责 ≤5 行；文件名自明时为零 | [CC-10] |
| 文件头塞 3 屏设计论证 | 决策无处安放（无 ADR 机制） | 一句指针外链 ADR | [CC-10] |
| Python 项目出现 `@param` 标签 | 跨语言套用自家惯例（肌肉记忆迁移） | 先读目标语言工具产出再写 | [CC-12] |
| Go 注释与声明间有空行，文档脱离归属 | 惯例无知（空行 = 不属于该声明） | 紧贴声明，无空行 | [CC-12] |
| Python 三派系（Google/reST/NumPy）混用 | 团队未选派 | 选一派全局统一，写进贡献指南 | [CC-12] |
| 写了 docstring 但无渲染（Sphinx/godoc 未跑） | 工具链不匹配 | 确认提取→渲染路径可走通，否则降级 | [CC-12] |
| `// 见 RFC 7234 §5.3` 章节号错误 | 引用幻觉（格式先验强、细节记忆弱） | 只引到文档级，或验证后精确引用 | [CC-2] |
| 注释里教语言基础（`// Array.map 会遍历数组`） | 教程腔 | 删除；注释读者是维护者 | [CC-1] [CC-4] |
| 骨架代码撒满 `TODO: implement` | 无主化倾向 | 显式抛错 + 集中清单声明 | [CC-11] |
| 版权行逐年手动追加 | 手工维护 | 工具自动或仅写定年份 | [CC-10] |

## API 速查表

### 注释类型决策表

| 情形 | 放置层 | 动作 |
|---|---|---|
| 命名/提函数/重结构能自明 | — | 改代码，不写注释 [CC-3] |
| 决策、约束、坑（代码永远表达不了） | 行内注释 | 写 why/context，引来源 [CC-1] |
| 公共方法/类的契约（what/how/gotchas/exceptions） | docstring/TSDoc | API 文档层；why 不进此层（官方 "Why" explanations are for inline comments）[官方文档](https://google.github.io/styleguide/docguide/best_practices.html) |
| 深层设计论证 | ADR | 一句指针外链，不内联 [CC-10] |
| 历史/作者/日期 | VCS | 不写注释；commit message 参照 [官方文档](https://cbea.ms/git-commit) [CC-7] |
| 待办/已知缺陷/临时绕过 | 标记注释 | TODO/FIXME/HACK 三要素格式 [CC-8] |
| 模块角色/架构约束 | 文件头 | ≤5 行四职责 [CC-10] |

### TODO/FIXME/HACK/XXX 标记格式表

| 标记 | 语义 | 最小格式 | 附加要求 |
|---|---|---|---|
| TODO | 待做（功能未完/待补） | `TODO(owner): 可行动描述 (#issue)` | 追踪引用可检索可排期 [CC-8] |
| FIXME | 已知缺陷待修 | `FIXME(owner): 缺陷描述 (#issue)` | 带严重度意识，致命缺陷与美化项分级 [CC-8] |
| HACK | 临时绕过，明知不优雅（欠技术债） | `HACK(owner): 绕过内容 + 正确做法 (#issue)` | 必须写「正确做法是什么」[CC-8] |
| XXX | 危险/需警示（语义最不统一） | 团队约定（多数团队弃用或与 FIXME 混同） | 无官方标准，纯团队约定 [模型经验] |

清偿纪律：定期 TODO 审查（做/删/降级）；issue 关闭同步清理；修复成本低于上下文切换成本时禁止用标记逃避 [CC-9]。

### 各语言 docstring 惯例对照表

> 细节以 [google.github.io/styleguide](https://google.github.io/styleguide/) 对应指南为准（tsguide/jsguide/pyguide/go 等索引确认在位，正文未逐语言抓取）；Rust 不在 Google style guide 覆盖范围，其列标注 [模型经验] 待 rust-lang 官方文档验证。

| 维度 | JS/TS（JSDoc/TSDoc） | Python（docstring） | Go（doc comment） | Rust（doc） |
|---|---|---|---|---|
| 位置 | 注释块贴声明上方 | 声明下方字符串字面量 | 声明上方紧贴（无空行） | `///` 贴条目；`//!` 模块级 |
| 格式 | 结构化标签（@param 等；TSDoc 标签体系见 api-doc-gen） | 三派系选一：Google `Args:` / reST `:param x:` / NumPy 下划线节 | 纯文本极简叙事，以标识符名开头（`// Foo returns ...`） | Markdown + `# Examples` 节 |
| 工具 | TypeDoc 等 | Sphinx / pydoc | godoc（标准库内置） | rustdoc（工具链内置） |
| 示例/测试 | `@example` | doctest 嵌入（`>>>` 可执行） | 缩进代码块 | `# Examples` 代码块默认编译测试 |
| 首句惯例 | 首句完整摘要（索引/tooltip 显示） | 同左 | 同左 | 同左 |

跨语言共性内核 [模型经验]（elicited/06）：文档注释服务于工具提取；首句摘要惯例普适；惯例是生态协议不是个人风格——跨语言套用是协议违例。

## 版本注意

- 各语言注释规范以对应官方风格指南为准：索引 [官方文档](https://google.github.io/styleguide/)（tsguide/jsguide/pyguide/go 等各语言指南 + Markdown Style Guide + docguide，ingest 确认在位）。
- ingest 未抓取各指南正文与版本信息——本文件不引用任何指南版本号；使用前以指南现文为准。
- 语言注释惯例慢变，但提取/lint 工具链演进较快：写文档注释前确认项目工具链状态（是否跑 Sphinx/godoc/TypeDoc）——这是项目事实，不得假设「写了就会渲染」[模型经验]（elicited/06）。
- TODO/FIXME/HACK/XXX 无官方标准版本可言（纯团队约定）[模型经验]（elicited/03）。

## 与其他子领域的集成要点

- **api-doc-gen**：公共 API 契约文档（TSDoc 标签体系、@param/@returns 等）完整规则归该域 kb；本域只管分层定位——what/how/gotchas/exceptions 归契约层，why 归行内层 [官方文档](https://google.github.io/styleguide/docguide/best_practices.html)。
- **doc-quality**：注释的中英文、术语统一、口吻风格遵循该域风格纪律；本域 CC-1 的「噪音」判定与其「信息密度」标准同源。
- **adr-changelog**：注释中的版本史、变更记录、深论证一律迁出——历史归 changelog/VCS，决策归 ADR；文件头是 ADR 的指针层不是存储层（[CC-7] [CC-10]）。
- **kb/laws.md**：CC-1、CC-2 为 [GLOBAL] 候选，与 DT-12/AD-1/AD-2「编造零容忍」族查重合并。
- **kb/ai-mistakes.md**：本域 AI 典型错误（why 编造、issue 号幻觉、逐行复读等 Top 15，见 elicited/05）汇入。
- **kb/gotchas.md**：what 复读、why 编造为跨域高频坑候选。

## 来源索引

官方文档（ingest 抓取，2026-11-17）：
- https://google.github.io/styleguide/ — Google 风格指南索引（各语言指南 + Markdown Style Guide + docguide）
- https://google.github.io/styleguide/docguide/best_practices.html — 文档最佳实践全文（官方注释谱系、命名层表述、API 文档契约、"Why" explanations are for inline comments、Minimum Viable Documentation、Update Docs with Code、Delete Dead Documentation、行为文档化即测试义务）
- https://cbea.ms/git-commit — commit message 写法（Google 官方推荐链接）

模型经验（阶段 1 萃取）：
- elicited/01-comment-taxonomy.md — 四分法、缺陷 Top 10
- elicited/02-good-comment-criteria.md — 决策序、必须写/不该写清单
- elicited/03-todo-fixture-discipline.md — 标记三要素、清偿机制
- elicited/04-file-header-scope.md — 文件头四职责、≤5 行
- elicited/05-ai-comment-mistakes.md — AI 系统性错误 Top 15
- elicited/06-language-comment-styles.md — 四语言惯例对比（置信度中，细节以官方指南为准）
- elicited/07-laws.md — 法则化 CC-1~CC-12

推断（不进入五大区块）：
- 四分法与官方谱系的层间映射（why/context ↔ inline comments 层；what/how ↔ 命名自明层 + API 契约层）——登记于「冲突消解记录」。
- XXX 标记在多数团队弃用/与 FIXME 混同的判断（置信度低，社区实践分散）。

## 冲突消解记录

| # | 模型原认知 | 文档事实 | 采用结论 |
|---|---|---|---|
| 1 | what/how/why/context 四分法是注释分类的权威框架（elicited/01） | Google 官方为「谱系说」：meaningful names → inline comments（提供代码无法包含的信息，如 why）→ method/class API 文档（契约：what/how/gotchas/exceptions；"Why" explanations are for inline comments）→ README → docs；四分法无单一官方出处 | 官方谱系为权威框架，四分法降级为操作化变体（价值排序工具）；「定位与心智模型」以谱系为骨架，四分法显式标注为应用层；映射关系标 [推断] |
| 2 | 「注释不是用来补偿坏代码」出处不明（疑为《Clean Code》立场变体，elicited/02 边界轮） | Google 官方等价表述：命名层 "allows the code to convey information that would otherwise be relegated to comments" | 以 Google 官方措辞为锚（CC-3 溯源），避免与《Clean Code》立场合并失真 |
| 3 | 四语言惯例对比表细节可直接采信（elicited/06 置信度中） | ingest 仅确认 google.github.io/styleguide 各语言指南存在（tsguide/pyguide/go 等），正文未逐语言抓取；Rust 不在 Google style guide 覆盖范围 | 对照表保留为速查，细节标注「以对应指南为准」；Rust 列标 [模型经验] 待 rust-lang 官方文档验证 |
| 4 | TODO/FIXME/HACK/XXX 有约定俗成的标准语义（elicited/03） | 无官方标准，纯团队约定；XXX 语义最混乱（多数团队弃用或与 FIXME 混同） | 标定「社区惯例」；CC-8 格式为工程共识而非官方规则；lint 强制格式（no-warning-comments 类）属工具细节，使用前以工具文档为准 |
