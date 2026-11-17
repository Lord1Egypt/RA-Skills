# FAQ · agent-analytics-report 常见问题

这里汇总使用本技能时最容易撞上的问题。按「安装 → 生成 → 计价 → 自定义模型 → 标记与合并 → 数据源与隐私 → 分类与异常 → 排查」排列，单篇自足，不用再翻 SKILL.md 和 README。

> 适用版本：**v1.7.2**（核对 `config.json` / `metadata.json`）。**已适配 WorkBuddy / Claude Code / Codex CLI / 千问办公 四个数据源。**

---

## 一、适用与安装

**Q1. 除了 WorkBuddy，还支持别的 Agent 吗？**
支持四个数据源，用 `--source` 切换：`workbuddy`（默认，能力最全）、`claude-code`、`codex`、`qwenwork`（千问办公）。千问办公的用法与口径见 Q49 / Q50 / Q51。
Trae 等仍未实现——能力边界一律以 `docs/ADAPTERS.md` 的表格为准，别对外声称已兼容。计价库里除 WorkBuddy 官方接口单价外，只有 Claude / OpenAI 系列的**折算估算价**，不是通用市场价。

**Q2. 怎么装？**
两种方式：

```bash
# 方式一（推荐）：SkillHub 搜索 agent-analytics-report 一键安装

# 方式二：手动
git clone <your-repo-url> ~/.workbuddy/skills/agent-analytics-report
```

手动装完重启 WorkBuddy 生效。

**Q3. `skillhub upgrade` 会不会冲掉我的配置？**
不会，前提是你把自定义内容写在 `scripts/pricing.local.json`。这个文件被 `.gitignore` 排除、不在发布包里，升级时发布版 `pricing.json` 被整目录覆盖重写，但 `pricing.local.json` 永远不会被碰——你填的单价自动保留，不用备份。**反过来，写进 `pricing.json` 的东西升级就会丢。**

**Q4. 报告没数据，是不是少开了什么？**
Token 数据来自 traces 目录，需要在 WorkBuddy 里启用 trace 记录。没开就没数据，报告会是空的。

---

## 二、生成报告

**Q5. 最省事的用法是什么？**
直接对 Agent 说一句就行，不用记参数：「生成周报」「帮我出一份本月的 token 消耗报告」「统计下这个月花了多少」。Agent 会自动跑采集 + 渲染。

**Q6. 支持哪些时间粒度？**

| 参数 | 含义 |
|------|------|
| `--period day` | 今天（单日） |
| `--period week`（默认） | 最近 7 天 |
| `--period month` | 最近 30 天 |
| `--period year` | 最近 365 天（滚动窗口，会跨年） |
| `--days N` | 自定义滚动 N 天 |
| `--start` + `--end` | 绝对日期范围 |

**优先级：绝对日期 > `--days` > `--period`。** 三个脚本（`collect_usage_data.py` / `generate_report.py` / `analyze_tokens.py`）都支持。

**Q7. 我想统计「2026 年 7 月」，用 `--period month` 对吗？**
不对。`--period` 是**滚动**窗口（最近 30 天），会跨月。想要自然月/自然年，用绝对日期：

```bash
python scripts/generate_report.py --start 2026-07-01 --end 2026-07-31 --output 七月报告.md
python scripts/generate_report.py --start 2026-01-01 --end 2026-08-03 --output 年报.md
```

采集器会自动识别周期类型，报告头部「报告类型」行显示成 `月报 · 2026年7月` / `年报 · 2026年（年初至今）`。

**Q8. 三种输出格式怎么选？**

```bash
python scripts/generate_report.py data.json --output report.md    --format markdown  # 默认，适合阅读
python scripts/generate_report.py data.json --output report.html  --format html      # 交互图表 + 浅深色自适应
python scripts/generate_report.py data.json --output report.json  --format json      # 适合程序处理
```

不传 `data_file` 就直接实时采集：`python scripts/generate_report.py --period week --output report.md`。

**Q9. 报告标题怎么没有「周报」两个字？**
故意的。三个格式的标题统一是 `Workbuddy使用情况报告`，周期信息改由报告头部的「**报告类型**」行用日历日期呈现（`周报 · 2026 年第32周（2026-07-27 至 2026-08-03）`）。这样 md / html / json 四方一致，不会因为文件名改变而对不上。

---

## 三、成本与计价（最容易产生疑问的部分）

**Q10. 报告里的花费和 WorkBuddy 后台对不上？**
先确认三件事：

1. **口径**：报告按「实际计费模型」（`exec_model`）+ 接口通道聚合，这和后台一致；
2. **单价**：报告用的是公开刊例价估算。若某模型单价没配，或你走的是 `custom-local` 自建接口，实际账单以接口方为准；
3. **缓存**：报告主口径是「实际消耗（计费等效）」，比原始 token 小很多（见 Q14），别拿原始数字去对账单。

**Q11. 我想改单价，改哪个文件？**

| 文件 | 用途 | 会不会被升级覆盖 |
|------|------|------------------|
| `scripts/pricing.json` | 发布版：WorkBuddy 官方内置模型 + `auto` | **会** |
| `scripts/pricing.local.json` | 本地覆盖：你自己的第三方/自建模型 | **不会** |

两份都缺时，回退到 `collect_usage_data.py` 里的内置 `MODEL_PRICING` 常量。单位是**元 / 每百万 tokens，输入按缓存未命中价**。

截至 v1.3.0，发布版已配价的官方模型共 17 项（完整清单以 `scripts/pricing.json` 为准）：

另：自动路由器的三档**档位**（快速 / 均衡 / 极致，即 `fast-model` / `balanced-model` / `extreme-model`）走独立 `mode_rates` 段配置，不在上面这份「模型」清单里——它们按积分倍率计费，报告单设 §3.4 维度展示，详见 Q36 / Q37。

`auto`（路由别名）· `hy3` / `hy3-x` · `hy4-preview` / `hy4-preview-x` · `glm-5.3` / `glm-5.3-flash` / `glm-5.2` / `glm-5.2-x` / `glm-5.1` / `glm-5v-turbo` · `minimax-m3` · `kimi-k3` / `kimi-k2.7-code` / `kimi-k2.6` · `deepseek-v4-flash` / `deepseek-v4-pro`

其中 `hy3` 限时免费至 2026-10-31、`hy4-preview` 限时免费至 2026-09-10。已下架的历史官方模型单独放在 `delisted` 段（报告里标 🗄️），不在上面这份清单里。

**Q12. 报告显示「未配置」怎么办？**
报告 **§3.3** 会列出本期所有缺失单价的模型名，并给出可直接复制的 `pricing.local.json` 补写片段。照着贴进本地文件、重跑即可。未配置的模型不计入成本总额，也不会污染占比。

嫌手改麻烦，直接把模型名和单价告诉 Agent，让它照 `references/add-custom-models.md` 写。

**Q13. `auto` 的花费是怎么算的？**
`auto` 是智能路由入口，没有单一单价（配置里恒为 `null`）。采集器取「本周期内所有已配置且单价 > 0 的模型的均价」做代表性估算，报告里标 ℹ️ 注明是估算值。想要精确值，可以在 `pricing.local.json` 里给 `auto` 直接填 `{"input": .., "output": ..}` 覆盖。

**Q14. 「原始 Token」和「实际消耗」差好多，哪个是真的？**
两个都是真的，用途不同：

- **原始总 Token** = `totalTokens` = 输入 + 输出，其中缓存命中（`cached_tokens`）是**输入 token 的子集**；
- **实际消耗（计费等效）** = 原始总量 − 缓存命中 ×(1 − 0.1)，即缓存命中只按 10% 计入（`CACHE_DISCOUNT = 0.1`）；
- **缓存占比** = `cached_tokens / input_tokens`，越高说明在反复复用同一段上下文——数字看着吓人，实际很便宜。

报告里所有排名（任务类型、Top 任务、每日趋势、成本）都用**实际消耗**作主口径。

**Q15. 限免期为什么显示 ¥0？**
`pricing.json` 的 `timed_free` 段记录了限时免费模型及截止日（含当天），命中期内调用记 ¥0。比如 `hy3` 限免至 2026-10-31、`hy4-preview` 限免至 2026-09-10。这段时间别只看钱——报告 §4 会插入免责声明，提示优先看 **§4.3 Token 口径**（始终运行）和缓存占比。

**Q16. 我走自建接口（custom-local），钱算得准吗？**
按你在 `pricing.local.json` 的 `custom_local` 段填的单价算。没填则回退到同名官方模型价；没有同名官方模型就显示「未配置」。数字仅供参考，准确账单请看接口方网站——报告表格末尾也附了这条免责备注。

---

## 四、自定义模型（BYOM）

**Q17. 怎么把我的自建 / 第三方模型加进报告？**
最简单：把模型名和单价用大白话告诉 Agent。

> 我新加了俩自定义模型：`custom-local:deepseek-r1`（自建，输入 2 / 输出 8）和 `custom-local:qwen3-235b`（自建 vLLM，输入 1 / 输出 2）。都帮我写进 agent-analytics-report 的 pricing.local.json。

Agent 会找到文件、去前缀转小写、只追加不改动官方条目、改完回显给你确认。完整 Prompt 模板见 `references/add-custom-models.md`。

**下载后想一次性补齐所有用过的自定义模型**，用 `references/on-download-inject.md` 里的扫描 Prompt。

**Q18. 带 `custom-local:` 前缀和裸名，分别写哪一段？**

| 你的模型长什么样 | 写进哪一段 | 键名规则 |
|------------------|-----------|----------|
| `custom-local:deepseek-r1`（WorkBuddy 里配成 OpenAI 兼容端点） | `custom_local` | 去掉 `custom-local:` 前缀、转小写 → `deepseek-r1` |
| `deepseek-r1`（trace 里就是裸名） | `models` | 原名小写 |

```json
{
  "custom_local": { "deepseek-r1": {"input": 2.0, "output": 8.0} },
  "models":       { "my-own-model": {"input": 1.0, "output": 2.0} }
}
```

**Q19. OpenRouter 的 `:free` 模型要登记吗？**
不用。以 `:free` 结尾的模型走 `openrouter-free` 通道，自动记 ¥0，报告里正常显示「免费」。只有当你确认某个 `:free` 变体是 WorkBuddy 曾官方提供、现已下架的，才需要把**完整模型名（含 `:free` 后缀）**写进 `delisted` 段。

**Q20. 本地 Ollama 模型怎么算？**
零 API 成本，强制归零并标 🏠，不计入账单总额。它会优先于「外部自定义」识别，绝不会误标成官方下架。

---

## 五、模型标记与合并

**Q21. 报告里那些小图标什么意思？**

| 标记 | 含义 |
|------|------|
| 🔀 | 智能路由 / 聚合网关（OpenRouter、Groq 等），一次调用可能落到不同模型，单价仅供参考 |
| 🏠 | 本地推理（Ollama / localhost:11434），零 API 成本 |
| 🔧 | 用户自定义外部 API（自己接的第三方端点） |
| 🗄️ | WorkBuddy 官方曾提供、现已下架（历史调用仍需计价，不进 §3.3 缺失清单） |
| ℹ️ | 估算值（如 `auto` 路由均价） |

**Q22. 我的官方模型怎么被标成 🔧 外部自定义了？**
采集器运行时会读本机 `~/.workbuddy/models.json`，凡被配成自定义/外部端点（`vendor=custom` 或 url 含 openrouter）或本地 Ollama 的模型，无论 trace 通道记成什么，一律优先判为自定义。这是为了治「撞名官方模型但走外部端点」的误识别。如果你确实是走官方通道，检查一下 `models.json` 里这个模型是不是被配成了外部端点。

**Q23. 为什么 `hy4-preview` 和 `hy4-preview-x` 在报告里合并成一行了？费用怎么算？**
这是 `display_merge` 干的。WorkBuddy 对同一模型会提供两个入口：**免费额度版**（trace 记 `hy4-preview`）和**免费额度用尽后的收费版**（trace 记 `hy4-preview-x`）。报告里合并成一行更好读。

**合并只改显示分组，不碰钱**：每一条 trace 仍按它自己实际执行的模型单独计价——免费额度版记 ¥0，收费版按刊例价（hy4 是 6/18，hy3 是 1/4）。所以合并行的花费，就等于其中**收费版那部分**的用量费用。实测开关 `display_merge` 对照，两个维度（§3.1 账单口径、§3.2 入口视图）总金额都完全不变。

`hy3` / `hy3-x` 同理。

**Q24. 我不想合并 / 想加新的合并对，在哪改？**
改 `scripts/pricing.json`（或本地 `pricing.local.json`）的 `display_merge` 段，键是要被合并掉的变体名，值是合并后显示的基础模型名：

```json
"display_merge": {
  "hy4-preview-x": "hy4-preview",
  "hy3-x": "hy3"
}
```

删掉某条就不合并了；照格式加新的即可，不用改 Python 代码。

---

## 六、数据源与隐私

**Q25. 数据从哪来？**

| 数据源 | 路径 | 内容 |
|--------|------|------|
| Traces | `~/.workbuddy/traces/` | Token 消耗、模型信息、会话时长 |
| SQLite | `~/.workbuddy/workbuddy.db` | 会话元数据、自动化运行、信用消耗 |
| Usage Log | `~/.workbuddy/usage-log.json` | 技能使用记录、活跃天数 |
| 会话目录 | `~/WorkBuddy/` | 产出文件、记忆日志 |

各源字段结构见 `references/data_sources.md`。

**Q26. 会不会上传数据 / 联网？**
分两个阶段看：

**采集阶段——只做本机只读采集**，全部本机读取、本地渲染，不调用任何外部 API，数据不上传。与联网有关的参数只有 3 个，**全部需要你显式传参、都不内置任何默认端点**；其中 `--lookup-pricing online` 只在本地拼字符串、**并不出网**，所以真正会发出网络请求的只有前2 个：

| 参数 | 行为 |
|------|------|
| 不传（默认） | **零网络** |
| `--pricing-api <URL>` | 请求**你自己**的定价镜像端点拉价（URL 只来自命令行，不从 trace / 会话内容派生）；拉到的价一律标 🌐 网络估算价，**不计入**任何成本总额 |
| `--task-classifier llm` + `--task-llm-endpoint <URL>` | 请求**你自己**的 OpenAI 兼容端点做任务分类；失败自动回退启发式 |
| `--lookup-pricing online` | **不发起任何网络请求**——只是本地用 `urllib.parse.quote` 拼出 DuckDuckGo 搜索链接给你自己点 |

**配置阶段——仅在你明确确认单价后**，才可能写你自己下载副本里的 `scripts/pricing.local.json`（补自定义模型单价，不进发布包、升级不会被覆盖）与 `scripts/task_rules.json`（调任务分类权重，**属发布资产、升级会覆盖，改前请备份**）。除此之外本技能不写任何其它文件，采集器打开 SQLite 用的是只读连接。完整清单见 SKILL.md「隐私与联网行为（完整清单）」。

**Q27. 删掉的对话还算钱吗？**
算。已删除对话消耗掉的 token 和成本仍然计入总量（避免低估真实开销），但归属到「其他 / 未关联」，不会按会话明细展示。即便产物文件物理删除了，transcript 里的 `ImageGen`/`VideoGen` 调用记录和 `trackedFileBackups` 键名仍然保留，任务类型分类照样能用得上。

---

## 七、分类与异常

**Q28. 任务类型是怎么判定的？分错了怎么办？**
关键词启发式匹配，顺序命中即返回。判定顺序是：后台自动化优先 → 内容生成 → 代码开发 → …… 完整 11 类顺序表在 SKILL.md 的「任务类型分类规则」。

候选文本 = 对话内容（剥离 `<system-reminder>` 后）+ 生成物指纹（含已删除）+ 会话标题。因为是启发式，**误分类是正常现象**，命不中就归「其他」。要调整就得改 `collect_usage_data.py` 的 `classify_task`。

**Q29. 异常检测为什么有两套口径？**
因为限免期会拉低成本口径，导致真实 Token 峰值被漏报。所以报告同时跑：

- **💰 成本口径**——仅在确有真实成本时启用；
- **📊 Token 口径**——**始终运行**。

免费主导期（免费 Token 占比 ≥ 80% 或总成本为 0）会在 §4 顶部插免责声明，提示成本类洞察参考有限。

**Q30. 「幽灵调用 / 未解析调用」警告是什么？**
早期 WorkBuddy trace 可能同时缺 `sessionId` 和 `modelInfo`，被兜底记成 `default`、token 全 0，无法归属到任何模型或会话。报告会显式警告并单独统计，不影响可计费数据。

---

## 八、故障排查

**Q31. 报告空空如也 / 全是 0？**
按顺序排查：① trace 功能是否启用（Q4）；② 时间范围是否对（`--period` 是滚动窗口，要自然月请用 `--start/--end`）；③ `~/.workbuddy/` 下 traces 目录是否有数据。

**Q32. 报告各章节的金额对不上？**
§3.1（账单口径）直接汇总 trace 级成本，必然与概览头条、每日表对账一致。§3.2（入口视图）是按入口单价**重算**的估算口径，与 trace 级有极小的浮点差异（约 0.0001 元量级），这是设计如此，不是 bug。

**Q33. 想跑测试 / 改代码，怎么上手？**

```bash
cd agent-analytics-report
python -m venv .venv && .venv/Scripts/python.exe -m pip install -r requirements-tests.txt
.venv/Scripts/python.exe -m pytest tests/ -v --alluredir=allure-results

# 无需 Java 的自包含 HTML 仪表盘
.venv/Scripts/python.exe tools/render_allure_html.py --results-dir allure-results --output allure-report.html
```

当前 **11 个测试文件、312 用例**。全部使用合成 fixture 数据，不含任何真实用量或个人资料，可安全公开。用例按 marker 分层（`smoke` / `unit` / `integration` / `regression` / `golden` / `metadata` / `privacy`），可用 `pytest -m regression` 过滤。

注意：`pytest.ini` 的 `addopts` 里带 `--alluredir`，若环境没装 `allure-pytest` 插件，跑测试要加 `-o addopts=""` 绕过。

**Q34. `tests/test_channel_attribution.py` 单独跑会崩？**
这个文件有近 190 个参数化集成用例，每个参数都要建临时 SQLite 和 traces 目录，本机资源不够时进程会被系统杀掉（表现为无任何输出、退出码 1）。**不是用例失败**。建议用 `-k` 分批跑，例如 `pytest tests/test_channel_attribution.py -k "hy3 or hy4"`。CI 上资源充足时可以全量跑。

**Q35. 我在用另一个类似 WorkBuddy 的工具，想用这个Skill，但目前只支持 WorkBuddy，可以怎样做？**
请参考 [ADAPTERS.md](../docs/ADAPTERS.md) 中的适配器说明。

---

## 九、档位维度（快速 / 均衡 / 极致）

**Q36. 报告 §3.4 的「档位」是什么？为什么单价是估算值？**
WorkBuddy 的 `auto` 自动路由下还有三档可选档位，按**积分消耗倍率**区分：

| 档位 | 别名（trace 字面量） | 积分倍率 |
|------|----------------------|----------|
| 快速 | `fast-model` | 0.21x |
| 均衡 | `balanced-model` | 0.65x |
| 极致 | `extreme-model`（配置缓存规范 id 为 `deep-model`，报告已归一） | 1.20x |

**这些是估算单价，不是真实账单价**：WorBuddy 只对档位做积分倍率计费，trace 里从不记录档位背后实际落地的底层模型，因此按档位直接算「花费」在概念上不成立。报告用「倍率锚定法」估算——按已知模型的官方倍率线性外推档位 ¥ 单价（快速 ≈¥1.91/7.64、均衡 ≈¥6.58/23.04、极致 ≈¥12.15/42.51），**仅用于横向对比档位间的相对成本**，章节内明确标注为估算值，且与 §3.1（账单口径）/ §3.2（入口视图）的真实计费完全解耦——改档位定价不影响任何真实金额。

想调估算单价只改 `pricing.json`（或 `pricing.local.json`）的 `mode_rates` 段，不用动代码。

**Q37. 为什么 §3.4 看不到档位背后的真实模型？**
因为 WorkBuddy 的计费语义就是「按档位积分倍率」而非「按底层模型 token」。trace 里只有档位别名（`fast-model` 等），底层模型对调用方不可见，所以本报告只能做**纯档位聚合**，无法像 §3.2 那样展开成具体模型。这不是采集器漏采，而是上游数据本身就不包含该信息。若你确实需要「某档位跑了哪些模型」，只能从 WorkBuddy 后台按档位账单查证，本报告无法还原。

---

## 十、适用边界与兼容性

**Q38. 支持哪些操作系统？**
当前版本在以下环境测试通过：
- Windows 10/11（64-bit）
- macOS 10.15+（Catalina 及以上）
- Ubuntu 20.04 / 22.04 LTS（Debian 系）

依赖项：Python 3.12+、SQLite（系统自带）、标准库 `json`/`sqlite3`/`pathlib` 等。若你的工作区使用非标准路径（如 `/mnt/c/Users/...` WSL 双路径），请确认 `~/.workbuddy/` 在本机可访问。

**Q39. 数据量上限是多少？大用户会不会慢？**
实测规模：
- **数万条 trace**（~1 个月活跃用户）：采集 + 报告生成约 5-15 秒，正常响应。
- **10 万条以上 trace**：可能触发内存压力，建议分段采集（用 `--start/--end` 按月切分后合并）。
- **超 50 万条**：未做压力测试，行为未定义，建议联系开发者评估。

**Q40. 不同 WorkBuddy 版本的 trace 格式兼容性如何？**
当前适配 schema a / schema b 两套 trace 格式（见 `ca_sources.py`）。WorkBuddy 升级后若引入新字段或变更 schema，本报告会：
- 新字段：忽略，不影响既有统计
- 关键字段缺失（如 `sessionId`、`modelInfo`）：按孤儿 trace 处理并打警告
- 结构大变（schema c+）：需升级技能，旧版采集器可能解析失败

若你遇到解析异常，先升级技能到最新版；仍不行则在 GitHub issue 提交一份样例 trace 供开发者适配。**⚠️ 提交前请注意：GitHub issue 可能公开，请先脱敏——移除凭据、个人 / 私有 URL、模型端点、路径与任何会话原文，优先用最小合成复现或脱敏后的 schema 示例，确认无敏感信息后再提交。**

**Q41. 自定义模型是怎么自动发现的？**
当你显式涉及自建模型（custom-local）时，聚合层才按需读取 `~/.workbuddy/models.json`（WorkBuddy 的模型配置文件）做自动识别（非报告默认流程、不越权读取），识别两类自定义模型：
- **本地模型（🏠）**：`vendor=ollama` 或 `url` 含 `localhost:11434` 的模型。零 API 成本，报告强制归零并标 🏠，不计入账单。
- **外部模型（🔧）**：`vendor=custom` 或 `url` 含 `openrouter` 的模型。可能仍有费用，需你在 `pricing.local.json` 配置单价。

若 `models.json` 不存在或解析失败，采集器会安全回退到 `pricing.local.json` 的 `user_custom_models` 人工列表。

**Q42. 我的模型没被自动发现怎么办？**
三种手动兜底方式：
1. **检查 models.json**：确认 WorkBuddy 里该模型已配置（`~/.workbuddy/models.json`），且 `vendor` 字段正确。
2. **手动写入 pricing.local.json**：按 [Q18 的表](#q18-带-custom-local-前缀和裸名分别写哪一段) 把模型加进 `custom_local` 或 `models` 段。
3. **告诉 Agent**：直接用大白话让 Agent 帮你写进 `pricing.local.json`（见 [Q17](#q17-怎么把我的自建--第三方模型加进报告)）。

以上三种方式可组合使用——自动发现优先，手动写入覆盖。
**Q43. 能统计 Claude Code 的用量吗？**
能。用 `--source claude-code` 切换数据源：
```bash
python scripts/collect_usage_data.py --source claude-code --period week -o data.json
python scripts/generate_report.py data.json --output report.html --format html
```
采集器会读取 `~/.claude/projects/**/*.jsonl`（每个文件是一次会话），解析每轮 assistant 消息的 `usage` 字段得到输入 / 输出 / 缓存 token，再按 `pricing.json` 里的 Claude 模型单价折算成本。

若你的 Claude Code 数据不在默认位置，用环境变量指向：
```bash
CLAUDE_PROJECTS_DIR=/path/to/projects python scripts/collect_usage_data.py --source claude-code ...
```

**Q44. Claude Code 报告为什么没有技能调用和自动化运行？**
因为 Claude Code 的会话日志里**没有这两类数据**——它只记录每轮对话的 token 与消息内容，不落盘「调用了哪个技能」「自动化任务跑了几次」。所以该数据源下报告只呈现 token、成本、任务类型、每日趋势、Top 任务与模型对比，技能与自动化两节为空。这是数据源的客观限制，不是采集失败。

**Q45. Claude 模型的单价准吗？**
是**估算值**。`pricing.json` 里的 Claude 单价由 Anthropic 美元刊例价按约 7.2 汇率折算成人民币（Opus 4 108/540、Sonnet 4 21.6/108、Haiku 4 5.76/28.8，单位元/百万 tokens）。两点要注意：
- 汇率与官方调价都会变，请以 Anthropic 官网最新定价为准；
- 若你用的是 **Max 订阅**而非按量 API，实际边际成本为 0，报告里的金额只反映「按刊例价折算的等效价值」，不是真实账单。

想改成自己的口径，在 `scripts/pricing.local.json` 覆盖对应模型即可（见 [Q18](#q18-带-custom-local-前缀和裸名分别写哪一段)）。

**Q46. 任务分类的规则是什么？为什么有的会话分得不准？**
分类按「对话内容 + 生成物指纹 + 会话标题」做**加权评分**（v1.4.1 起）：11 个任务类型全部参与打分，取总分最高者。每条关键词有权重——强信号（如 `skillhub install`、`imagegen`）一条顶多条，弱信号（如「了解」「对比」）要好几条叠加才能定类型。不准确的常见原因：
- 会话内容太短或被截断，信号不足 → 归「其他」或低置信类型；
- 多个类型信号混杂（既写了代码又提了周报）→ 取总分最高者，可看会话数据里的 `_task_confidence` 字段判断可信度（低于 0.25 表示两个类型几乎打平）。

你可以直接编辑 `scripts/task_rules.json` 调整关键词和权重（文件缺失或写坏会自动回退内置规则，不会崩）。⚠️ 注意它是**发布资产**（进发布包），`skillhub upgrade` 升级时会被覆盖，没有本地覆盖机制——改之前请自行备份。

**Q47. 能用大模型来分类任务吗？**
能，作为**可选增强**：
```bash
python scripts/collect_usage_data.py --task-classifier llm \
    --task-llm-endpoint http://localhost:11434/v1 \
    --task-llm-model qwen2.5:7b --period week -o data.json
```
要点：
- 端点由**你自己提供**（本地 Ollama 的 `http://localhost:11434/v1`，或自有 OpenAI 兼容服务），本技能不内置、也不默认调用任何第三方商业 API；
- 不配置就完全离线（默认 `heuristic` 启发式，零网络依赖）；
- LLM 对某条会话分类失败（网络断、响应异常）会自动回退启发式，不影响采集；
- 隐私提示：LLM 模式会把会话文本（截断至 1500 字符）发到你指定的端点。本地 Ollama 不出本机，第三方端点请自行评估。

**Q48. 模型单价会自动更新吗？过期了怎么知道？**
本技能**不自动抓取厂商网页**（合规与稳定性考虑），提供 `scripts/fetch_pricing.py` 半自动更新：
```bash
# 拉取你自备的定价镜像（URL 或本地 JSON），校验后产出候选，不直接落盘
python scripts/fetch_pricing.py --url https://your-mirror/pricing.json
# 产出 scripts/pricing.candidate.json + pricing-diff.md（接受/拒绝明细）
# 审核无误后：
python scripts/fetch_pricing.py --file ./new-prices.json --apply   # 自动备份原文件
```
安全机制：单价必须是非负数字；与现价偏差超过 5 倍的条目拒绝（确认无误加 `--force`）；`pricing.local.json` 本地覆盖永不被覆盖。

CI 场景用 `--check --stale-days 30`：定价超过 30 天没更新（看 `pricing.json` 的 `_pricing_rules.updated`）就退出码 1，流水线可以据此提醒你更新。

**Q52. 千问办公报告里的技能调用、交付物、自动化任务分别是从哪来的？**
三个维度的落点跟 WorkBuddy 完全不一样，都是**实测本机数据**后定的（机制详见
[ADAPTERS.md](../docs/ADAPTERS.md) §4.6）：
- **技能调用**：会话转录里的 `tool_use name="Skill"` → `input.skill`，每次调用都带时间戳和
  会话 ID，所以能按窗口过滤、能归因到会话。⚠️ **不用 `~/.qwenworkcn/skill-usage.json`**：
  它只记累计 `usageCount`，本机实测只有 2 条记录、而转录里实到 17 次调用（低估约 8.5 倍），
  拿它统计会严重少报。
- **交付物**：`present_files` 工具调用里列出的路径（语义=「已作为交付物交给你」）**并上**
  `~/.qwenworkcn/workspace/<chatId>/outputs/` 目录扫描，按归一化路径去重；磁盘扫描会跳过
  `.bak` / `.tmp` / `~$` 与隐藏文件。`Write`/`Edit` 改过的文件**不混进清单**（本机 Edit 有
  3305 次，混入会把清单淹掉），只作为「改动过的文件」单独计数。
- **自动化任务**：`agents.db` 的 `scheduled_tasks` ⟕ `task_run_logs`。你本机这两张表是空的，
  所以报告里「自动化任务运行 0 次」是**真 0**，不是没采——将来建了定时任务会自动出现。
  另外千问办公有一类**后台自动运行**（记忆整理 / 反思，来自 `nudge_logs`），它的会话归因率只有
  约 8%，因此不混进 §八，只在 §一 用一行交代次数与失败数，失败率过高时 §十一 会提示。

**Q49. 能统计千问办公（QwenWork）的用量吗？**
能，用 `--source qwenwork`：
```bash
python scripts/collect_usage_data.py --source qwenwork --period week -o data.json
python scripts/generate_report.py data.json --output 千问办公_周报.html --format html
```
它会读三处本机数据：会话转录 `~/.qwenworkcn/projects/<slug>/<sessionId>.jsonl`、逐次调用日志
`~/.qwenworkcn/logs/runs/<run>/qodercli.log`、业务库 `%APPDATA%/QwenWorkCN/data/agents.db`（只读打开，
读不到就自动降级为纯 JSONL 口径）。路径可用 `QWENWORK_HOME` / `QWENWORK_DB` 覆盖。
**在千问办公里让 Agent 出报告时记得带这个参数**——默认源是 WorkBuddy，本机没装它会采到 0 条数据。

**Q50. 千问办公报告里为什么没有金额？**
因为拿不到可靠的单价：千问办公是**积分订阅制**，没有公开的单 token 刊例价，`pricing.json` 里
**故意不配** `flash` / `pro` 这些档位——编一个数就是假数据。这种情况下报告**自动切到
`tokens_only` 计价模式**：成本货币化、花费速览、省钱杠杆、最贵模型、档位与缓存可省测算整章撤掉，
模型表退化成「模型 / 调用次数 / 实际消耗Token」三列，§四 变成「Token 与调用深度分析」。
藏起来比摆一排 `¥0.00` 更诚实——后者容易被读成「这月免费」或「采集坏了」。

想看到金额，在 `scripts/pricing.local.json`（不进发布包）里按裸档位名补价，重跑即自动回到 priced：
```json
{"flash": {"input": 1.2, "output": 4.8}, "pro": {"input": 7.2, "output": 28.8}}
```
也可显式指定：`--cost-mode tokens-only` 强制隐藏金额，`--cost-mode priced` 强制保留现状。
注意限免 / 本地模型那种 `¥0.00` 是**已配置单价算出的真实结果**，不会被 auto 误判成 tokens_only。

另外该源**没有 L1 真值通道**：`--import-official` 只对 WorkBuddy 可用（千问办公的账号级积分
无法归因到单个会话），混用会直接退出码 2。

**Q51. 千问办公的 token 数字能信吗？**
当趋势看，别拿去对账。千问办公**服务端不回传 token 用量**（本机实测 1167 条
`model.response.completed` 的四个 token 字段全是 0，转录里 `message.usage` 恒为 `null`），
所以 token 是本地按字符估算的：CJK 1 字 ≈ 1 token、其余 4 字符 ≈ 1 token，输入按逐请求
「上下文重发」累加，system prompt 不落盘故不计（实际 input 略高于估算）。
不受影响的**真实值**有：调用次数、每次请求端到端耗时、模型档位、会话真名、活跃天数、任务分类。
一旦上游开始回传真实 token，适配器会自动改用真值（`_tokens_estimated` 变 `false`），无需改代码。
