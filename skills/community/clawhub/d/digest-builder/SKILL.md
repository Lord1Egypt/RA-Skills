---
name: digest-builder
description: "将聚合池中的原始候选内容转换为可判断的 Digest：优先从 FreshRSS 的未读列表经 Google Reader API 拉取候选，再执行 URL 去重、相似事件聚类、正文抓取检查、噪音过滤、摘要生成与初步排序。用于需要把一批原始 feed 条目或 FreshRSS 未读条目整理成结构化候选文档的场景。"
---

# Digest Builder

以简体中文工作。目标是把原始候选整理成干净、结构化、适合快速判断的候选池，而不是直接产出日报终稿。若工作区已经配置 FreshRSS，则默认先从 FreshRSS API 拉取未读列表，再进入 Digest 预处理。

## 核心任务

- 通过 FreshRSS Google Reader API 拉取未读列表
- 读取配置中的 `api_password`
- URL 精确去重
- 相似事件聚类
- 正文抓取可用性检查
- 噪音过滤
- 摘要生成
- 标签补全
- 初步排序

## 处理顺序

1. 若已配置 FreshRSS，先通过 Google Reader API 完成登录并拉取未读列表。
2. 默认按“昨天”这个自然日窗口切片未读条目；只有用户明确指定其他日期时才覆盖。
3. 先做 URL 归一和精确去重。
4. 再识别同一事件的相似条目，进行聚类或合并。
5. 检查正文是否可抓取、是否存在明显质量问题。
6. 剔除标题党、无正文、广告型、明显重复价值不足的内容。
7. 为保留条目生成 2 到 5 行摘要。
8. 补充主题标签、风险标签、行动价值标签。
9. 按公共重要性、个人相关性、来源可靠度做初排序。

## 去重硬约束

- Digest 必须严格去重，禁止同一事件、同一结论、同一新闻变体重复出现。
- 去重分三层执行：
  - URL 层：相同链接、归一化后等价链接、追踪参数不同但正文相同的链接只保留一条。
  - 事件层：同一事件的多来源只保留信息增量最高的一条为主条目，其余仅作为参考来源存在，不再生成独立摘要。
  - 摘要层：若两条候选的摘要核心信息高度重合，必须重写或合并，确保每段摘要独立且有辨识度。
- 不能依赖标题不同就视为不同条目；必须按事件事实和信息增量判断。

## 英文文章处理

- 所有英文文章必须生成中文摘要。
- 中文摘要必须准确覆盖原文核心信息、关键观点和重要结论，不能只翻译标题。
- 语言要求简洁、逻辑清晰，不遗漏影响判断的关键信息。
- 若原文是英文但正文无法完整访问，必须明确标记“英文原文未完整获取”，不能假装已完整总结。

## 链接格式

- 所有链接统一使用 Markdown 格式：`[标题文本](链接)`
- 标题文本必须简洁且能精准对应目标内容。
- 禁止直接裸露 URL 作为最终输出主格式，除非是调试或原始抓取产物。

## FreshRSS 配置约定

优先读取配置文件，其次读取环境变量。

推荐配置项：

- `base_url`
- `username`
- `api_password`
- `output_json`
- `output_md`
- `limit`
- `include_read`

若既没有配置文件，也没有环境变量，不要假装已读取 FreshRSS，必须明确指出缺失项。

## FreshRSS API 约定

- API 地址：`<base_url>/api/greader.php`
- 登录接口：`accounts/ClientLogin`
- 未读列表接口：`reader/api/0/stream/contents/reading-list?xt=user/-/state/com.google/read&output=json`
- 已读标记接口：`reader/api/0/edit-tag`
- 认证方式：`Authorization: GoogleLogin auth=<Auth>`

默认优先输出两份原始产物：

- `digests/raw-freshrss.json`
- `digests/raw-freshrss.md`

然后默认继续输出“昨天窗口”切片：

- `digests/freshrss-yesterday.json`
- `digests/freshrss-yesterday.md`

再基于昨天窗口产物进入去重、聚类和摘要阶段。

## 已读回写状态

- 当前默认流程不回写 FreshRSS 已读状态。
- 生成 `Daily Review`、上传知识库、写入笔记后，也不要自动把源条目标记为已读。
- 只有用户明确要求回写已读时，才允许进入该分支。
- 若未来恢复该能力，也必须按“处理时间窗口”精确回写，不能清空整个原始未读池。
- 需要人工触发时可使用 `scripts/mark_freshrss_read.py`，但默认流程禁止调用。

## 输出格式

每条候选至少包含：

- 条目 ID
- 标题
- 来源
- 时间
- 链接（Markdown 格式）
- 原始摘要或内容片段
- 摘要
- 主题标签
- 聚类标记
- 排序理由

## 排序原则

- 公共重要性优先于个人偏好。
- 个人相关性只作为弱信号。
- 同一事件的多来源不应占满前排。

## 输出风格

- 摘要尽量具体，避免空话。
- 每段摘要必须与其他条目明显区分，禁止模板化重复表述。
- 排序理由要可解释。
- 若正文不可用，明确标记，不要装作已读过全文。

## 反例禁区

- 只整理标题，不检查正文质量。
- 摘要变成泛泛改写标题。
- 多条摘要重复表达同一结论，却未合并或改写。
- 用个人偏好压过公共重要性事件。
- 还没做聚类就直接排序，导致同一事件反复出现。

## 参考文件

- Digest 字段和过滤规则：`references/digest-spec.md`
- FreshRSS Google Reader API 流程：`references/freshrss-google-reader.md`
- FreshRSS 抓取脚本：`scripts/fetch_freshrss_unread.py`
- FreshRSS 日期切片脚本：`scripts/slice_freshrss_by_date.py`
- Digest 构建脚本：`scripts/build_digest.py`
- FreshRSS 已读回写脚本：`scripts/mark_freshrss_read.py`
- FreshRSS 配置样板：`scripts/freshrss.config.example.json`

