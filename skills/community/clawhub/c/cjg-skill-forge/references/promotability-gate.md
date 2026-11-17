# S8 可推广闸门 · 详细检查表与参考（纪律 16）

> 配套 `SKILL.md` 纪律 16。S8 在 S7（清晰化）之后、发布前强制运行，**以 S7 清晰化产物为 Convention 维度达标证据，不重复清晰化**。
> 来源：腾讯 SkillHub《10万+Skill 背后》的 TRACE 质量坐标 + 分发坐标。

---

## 一、TRACE 维度映射（锻造炉已覆盖，S8 做交叉核对不重复建设）

| TRACE | 平台关心 | 锻造炉对应 | S8 动作 |
|---|---|---|---|
| T Trust | 元数据真实、声明=实现、安全 | 纪律10/13 | 交叉核对 description 与实现一致、无夸大、无蹭品牌 |
| R Reliability | 异常处理、运行稳定 | 纪律6 真机 | 已覆盖，不重复 |
| A Adaptability | 能力边界、触发清晰 | 纪律7 | 核对 find-skill 触发友好 |
| C Convention | 文档质量、渐进披露 | 模式D/S7 | **S8 以 S7 产物为已达标证据** |
| E Effectiveness | 开箱即用度 | 纪律6 | 核对开箱即用 / 需 API Key 标注 |
| ★ 分发坐标 | 分类对、被搜到、介绍可复用 | **本闸门新增** | 检查项 4/5/6 |

---

## 二、S8 检查清单（每项 ✅/⚠️/❌；任一分发相关 ❌ 或 ⚠️ → 回退 S7/S2）

1. **T 可信（交叉核对）**：description 与实现一致（无夸大"最牛/第一"）、无蹭品牌 Logo、国内可运行（依赖/API 国内可达或已标注）、安全红线在。
2. **A 触发 find-skill 友好**：description 含 "Use when..." + 中文触发关键词；能力边界显式（纪律7）。
3. **E 开箱即用度**：零配置能用 → 标注"开箱即用"；需 API Key/账号 → 显式声明"需要 API Key"并在安装须知写清配置步骤（对应 SkillHub "需要 API Key" 系统标签）。
4. **★ 分类映射**：依技能类型+功能，建议 SkillHub 受控分类（见下方 12 一级类目），落成 `references/discovery.md`（分发就绪卡：建议分类 + needs_api_key + 一句话定位 + find-skill 触发词）。
5. **★ 元数据真实**：name/slug/version 规范、slug 与目录同名、displayName 不蹭品牌、发布前确认 slug 未被占。
6. **★ 跨平台介绍文案（≤1024 字符）**：技能须有一份适配**豆包 / Claude / 其他平台**的简短介绍 `references/intro.md`，纯介绍、≤1024 字符（含标点与空格，UTF-8 计）。说清"做什么 / 适合谁 / 怎么用"三件事；不依赖 SkillHub 专有术语；与 description 不冲突但可更口语化；中文为主、可双语。

---

## 三、SkillHub 12 一级类目参考（建议分类时对照）

> 落 `discovery.md` 时，从以下选 1 个一级 + 1-3 个二级 + 必要时行业类目 + 系统标签 `needs_api_key`。

1. 开发工具（Development）— 编程/调试/脚手架/CI
2. 效率工具（Productivity）— 日程/笔记/自动化/文件
3. 内容创作（Content）— 写作/绘图/视频/翻译
4. 数据分析（Data）— 统计/可视化/报表/BI
5. 学术研究（Research）— 文献/科研方法论/学术写作
6. 教育培训（Education）— 教学/陪练/出题
7. 设计创意（Design）— UI/UX/品牌/3D
8. 营销增长（Marketing）— 文案/投放/社群/SEO
9. 办公协作（Collaboration）— 邮件/会议/文档/项目管理
10. 生活助手（Lifestyle）— 健康/出行/购物/美食
11. 金融财税（Finance）— 记账/投资/报销/税务
12. 行业垂直（Industry）— 医疗/法律/电商/制造/政务

系统标签：`needs_api_key`（需 API Key/账号才能用）、`needs_network`（需联网）、`local_only`（纯本地）。

---

## 四、discovery.md 模板（随包分发，对用户有用）

```markdown
# 分发就绪卡 · Discovery

- 一句话定位：<用一句人话说明这个技能做什么、适合谁>
- 建议分类：<一级> / <二级1, 二级2> / [行业]  （参考 SkillHub 12 一级类目）
- 系统标签：needs_api_key=<true|false> / needs_network=<true|false> / local_only=<true|false>
- find-skill 触发词：<中文触发词1>、<中文触发词2>、<场景短语>
- 开箱即用：<是/否，若否写清需配置什么>
```

## 五、intro.md 规范（≤1024 字符，跨平台复用）

```markdown
# <技能名> 是什么

<第1段：做什么——一句话说清功能>
<第2段：适合谁——典型用户/场景>
<第3段：怎么用——最小上手步骤（1-3 句）>

（纯介绍，不含 SkillHub 专有术语；豆包/Claude/其他平台详情页与社区帖直接复用）
```

- 字符计：UTF-8 下含标点与空格 ≤1024。中文按字符数计（非字节）。
- 与 frontmatter `description` 不冲突：description 偏"触发场景"，intro 偏"口语化介绍"，二者互补。
