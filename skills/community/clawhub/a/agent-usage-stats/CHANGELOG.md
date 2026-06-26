# Changelog

## v2.7.13 (2026-06-14)

### 维护

- 版本更新

## v2.7.12 (2026-06-13)

### 维护

- .gitignore 新增 .codegraph/、.reasonix/

## v2.7.11 (2026-06-13)

### 修复

- **CodeX 官方订阅无法识别**：官方订阅将 state DB 放在 `~/.codex/sqlite/` 子目录，`_find_codex_db` 现同时搜索 `~/.codex/` 和 `~/.codex/sqlite/`，选最新的

## v2.7.10 (2026-06-07)

### 修复

- 清理冗余 demo 目录
- 新增 Hermes/monitor 单元测试

## v2.7.9 (2026-05-31)

### 修复

- **CodeX 月度/年度 token 翻倍修复**：部分 session JSONL 中 `last_token_usage` 存储的是累计值而非增量，按时间过滤时累加导致入/出/缓存 token 虚高约 2 倍。改为使用边界 `total_token_usage` 差值计算

## v2.7.7 (2026-05-31)

### 修复

- **CodeX 月度/年度 token 翻倍**：部分 session JSONL 中 `last_token_usage` 存储的是累计值而非增量，按时间过滤时累加导致入/出/缓存 token 虚高约 2 倍。改为使用边界 `total_token_usage` 差值计算
- **CodeX 缓存率展示无影响**：虽然 token 绝对值虚高，但输入和缓存同步放大，缓存率百分比本身未受影响

### 维护

- **CodeX 离线回归**：新增 `codex_unit_regression` 用合成数据（含重复累计事件、空事件、无 token 数据 fallback）覆盖新边界逻辑
- 多项 total_mode（累计型 Agent）展示优化：费用跳过、导出明细格式适配

## v2.7.6 (2026-05-29)

### 修复

- **ClawHub 更新工作目录固定**：`token-stats update` 执行 `clawhub update/install --force` 时固定在用户主目录运行，避免用户在 `~/.local/bin`、`Documents` 等目录执行更新后，ClawHub 把新版下载到错误位置
- **旧版本升级说明补齐**：明确 2.7.0 等旧版无法执行新版自修复逻辑，首次跨过该问题需要从 ClawHub 下载目录运行一次 `setup` 或使用新版入口
- **回归测试补齐真实事故路径**：维护流回归会从旧命令目录触发 update，并断言 ClawHub 工作目录被固定到 HOME
- **维护目录保护**：`token-stats update` 仅在当前目录位于 ClawHub skill 源目录时停止，避免覆盖正在使用的源码目录；`token-stats --uninstall` 会额外保护 `~/.token-stats`，因为卸载会删除安装目录

## v2.7.5 (2026-05-29)

### 修复

- **ClawHub 实际安装路径识别**：`update` 会解析 ClawHub 输出中的真实安装目录，例如 `.../.local/bin/skills/agent-usage-stats`，避免在非 home 目录执行更新后仍停留在旧版本
- **更新源搜索补齐**：新增当前目录和旧命令目录下的 `skills/agent-usage-stats` 搜索，覆盖 macOS、Linux、WSL2 中从不同目录运行 `token-stats update` 的情况
- **卸载清理补齐**：`--uninstall` 会同时清理误装到旧命令目录下的 ClawHub 技能目录，避免后续重装残留

## v2.7.4 (2026-05-29)

### 修复

- **PATH 前置而非追加**：安装时将 `~/.token-stats/bin` 前置到 PATH，确保新版 token-stats 优先于旧版命令
- **fish shell PATH 修复**：`fish_add_path` 使用 `-p` 参数前置，与 bash/zsh 行为一致
- **手动 PATH 提示修正**：README 和 installer 中的手动 PATH 命令统一为前置格式
- **旧命令入口不断链**：`setup` / `update` 不再直接删除 `~/.local/bin/token-stats`，而是迁移为转发入口，避免当前 bash/zsh 缓存旧路径后执行失败
- **ClawHub 卸载补齐**：`--uninstall` 会删除 `~/skills/agent-usage-stats` 等 ClawHub/历史安装目录，避免重新安装时报 `Already installed`

## v2.7.1 (2026-05-29)

### 修复

- **安装/更新兼容老版本路径**：`setup` / `update` 会清理旧版 `~/.local/bin/token-stats` 命令入口和旧 PATH 标记，并将 `~/.token-stats/bin` 前置到 PATH，避免更新后仍命中老命令
- **更新后当前终端兼容**：`update` 会把旧版命令入口迁移为转发入口，避免 bash/zsh 已缓存旧路径时出现 `No such file or directory`
- **卸载清理更完整**：`--uninstall` 同时清理新版安装目录、旧版命令入口、PATH 标记和配置文件，并按系统给出终端缓存刷新提示
- **跨平台提示优化**：针对 macOS、Linux、Windows 和 WSL2 的 PATH 生效、命令缓存和异常场景给出更明确的提示

### 维护

- 清理项目内 Python 缓存文件，保持发布包干净

## v2.7.0 (2026-05-28)

### 新增

- **ClawHub 安装流程收敛**：安装后执行 `setup` 会把运行文件复制到 `~/.token-stats/`，创建 `~/.token-stats/bin/token-stats` 命令入口，并将 `~/.token-stats/bin` 加入 PATH
- **安装/更新/卸载统一围绕 `~/.token-stats/`**：`token-stats update` 通过 ClawHub 拉取更新后同步到安装目录；`token-stats --uninstall` 会清理命令入口、PATH、配置文件和安装目录
- **模块化重构**：`token-stats.py` 变为轻量入口，主逻辑拆入 `token_stats/` 包；已拆出安装文件管理、安装器、监控、快照、对比、导出、价格、日期、上下文、格式化、路径探测、菜单和渲染模块
- **回归测试升级**：`test_regression.py` / `test_regression.sh` 改为带断言的回归脚本，覆盖编译、版本、Agent 探测、README 核心查询命令、对比和导出；安装/更新/卸载链路改为手动验证

### 修复

- **CodeX 月度/年度统计异常**：部分 `token_count` 事件缺少 `last_token_usage` 时不再报 `'NoneType' object is not subscriptable`，会容错读取 `total_token_usage`
- **导出多 Agent 数据异常**：修复拆分导出模块后 `skip_model` 未导入导致的 CSV/XLSX 简单导出失败

## v2.6.8 (2026-05-27)

### 变更

- **安装路径统一为 `~/token-stats/`**：不再依赖 ClawHub 的 `~/skills/` 路径。默认使用 `git clone` 到用户主目录，更简单可预测
- **安装文档重写**：README / SKILL.md 区分 git clone 和 ClawHub 两种安装/更新方式，各写清楚

### 修复

- **`update` 搜索路径**：新增脚本所在目录（如 `~/token-stats/`）到搜索列表，支持 git clone 安装后的文件更新检测

## v2.6.7 (2026-05-27)

### 新增

- **CodeX I/O 拆分**：从 session JSONL（`~/.codex/sessions/**/*.jsonl`）读取 `token_count` 事件，提取 `input_tokens`/`cached_input_tokens`/`output_tokens`/`reasoning_output_tokens` 完整拆分，CodeX 从 `token_mode="total"` 切换为 `"split"`，与 Claude Code 等行为一致
- **CodeX 调用次数修正**：现在统计 `token_count` 事件数（即实际 API 调用次数），而非 session 数
- **CodeX 模型价格**：`model_prices.toml` 新增 `gpt-5.5`（$5.0/$30.0）、`gpt-5.4`（$2.5/$15.0）、`codex-auto-review`（$0）

### 修复

- **CodeX watch 模式疯转**：`-w -5` 等负 interval 导致循环不休眠。`watch()` 入口添加 `interval < 1` 下限保护，argparse 添加 `_positive_int` 校验拒绝 ≤0 的间隔
- **CodeX 模型名重复**：SQL 按 `(model, model_provider)` 分组导致同模型显示多行。改为仅按 `model` 聚合，合并不同 provider 的数据
- **CodeX 零 token 会话**：`tokens_used = 0` 的无效会话不再显示
- **CodeX detect() 假阳性**：数据库文件不存在时不再错误返回 True
- **watch 模式今日计算**：CodeX 切换为 `split` 模式后，`--today` 通过事件时间戳精确过滤，不再使用 watch 启动时刻的基线差分

### 内部

- 新增 `_parse_codex_session_jsonl()`：解析 CodeX session JSONL，含 mtime 缓存以优化 watch 模式性能
- 重写 `CodeXAgent.collect()`：混合 threads 表（元数据）+ JSONL（I/O 拆分），时间过滤在 SQL + JSONL 事件层双重保障
- 新增 `_codex_jsonl_cache`：按文件 mtime 缓存已解析数据

## v2.6.6 (2026-05-25)

### 修复

- **CodeX watch 模式"今日"不更新**：CodeX `collect()` 时间筛选使用 `created_at`，但 `tokens_used` 随会话进行而增长，旧 thread 的 `created_at` 不变导致"今日"查询漏掉大部分活跃 thread。改为使用 `updated_at` 筛选，并在 watch 模式中对累计型 agent（仅有 `tokens_used` 无入/出区分）使用基线差分计算"今日"，不再调用 `collect(from_ts=today_start)`
- **CodeX watch 模式显示格式**：CodeX 不区分输入/输出 token，但 watch 模式始终显示"入/出"格式。新增 `AgentData.token_mode` 字段（`"split"` / `"total"`），CodeX 标记为 `"total"`，watch 渲染时显示"总计"而非"入 X / 出 0"

## v2.6.5 (2026-05-25)

### 修复

- **Python 3.10 价格加载失败**：`tomllib` 需 Python 3.11+，导致 `model_prices.toml` 加载为空。新增内置极简 TOML 解析器 `_parse_simple_toml()`，Python < 3.11 时 fallback 使用

## v2.6.4 (2026-05-25)

### 修复

- **Python < 3.12 兼容性**：f-string 内嵌套双引号（`f"...{pc.get("currency","CNY")}..."`）在 Python 3.12 之前报 `SyntaxError: unmatched '('`，共 4 处改为单引号

## v2.6.3 (2026-05-24)

### 修复

- **月度导出费用列错误**：年度 XLSX/CSV 导出时 `monthly_data` 未存储 cost 字段，导出函数直接 `md.get('cost', 0)` 全为 0。改为在收集月度数据时预计算 cost，四个导出函数统一格式化

## v2.6.2 (2026-05-24)

### 修复

- **Claude Code 调用次数和缓存 token 重复统计（严重 bug）**：CC JSONL 将同一 API 响应的 usage 存多份（时间戳略有差异），导致 69% 消息为重复。按 `(model, input, output, cache)` 去重后，v4-pro 从 14,870 调用/3.14B 缓存降至 4,586/0.97B，与 DeepSeek 官网账单吻合。此前因该 bug 误判「价格计算不准确」而移除的价格功能，现已恢复

## v2.6.1 (2026-05-23)

### 修复

- **`token-stats update` 漏搜本地 `skills/` 目录**：`clawhub install` 安装到当前目录的 `./skills/` 时，update 代码只搜索 `~/skills/` 和 `~/.clawhub/skills/`，导致版本检测失败。已将脚本所在目录的 `skills/` 加入搜索路径

## v2.6.0 (2026-05-23)

### 新增

**Agent 支持**
- **Reasonix Agent**：从 `~/.reasonix/usage.jsonl` 读取 token 统计，支持时间过滤和分会话聚合
- **DeepSeek TUI Agent**：从 `~/.deepseek/sessions/*.json` 读取统计，展示总 tokens、会话数、工具调用次数、费用

**缓存命中率**
- 所有模式（快照/监控/导出/对比）新增缓存命中率展示
- 自适应公式：`cache > input` 时用 `cache/(cache+input)`（DeepSeek API），否则用 `cache/input`（标准 API）
- 终端展示格式：`缓 162.18K (85.5%)`

**预估费用**
- 新增 `model_prices.toml` 配置文件，覆盖 60+ 模型 14 个厂商
- 所有模式默认展示预估费用（`≈¥X.XX` 或 `≈$X.XX`），无价格模型显示 `-`
- 费用 = input × input_price + output × output_price + cache × cache_read_price（均按 1M tokens 计）
- 监控摘要行追加增量费用：`── [02:47:16] +5.62K tokens +2 调用 ≈¥0.0034 ──`

### 变更

- Python 最低版本要求从 3.8 提升至 3.11（`tomllib` 标准库要求）
- Agent 展示顺序调整为：Claude Code → CodeX → Hermes → OpenClaw → Reasonix → DeepSeek TUI
- 配置文件从 JSON 改为 TOML（支持注释，`model_prices.toml`）
- 新增 `--list-prices` 参数，按厂商分组展示 60+ 模型价格

### 修复

- **Hermes 无时间筛选时只返回当前会话**：`_collect_impl()` 在 `from_ts=None, to_ts=None` 时走入「当前会话」分支，导致 `--all` 统计漏掉历史数据。现已改为与其他 Agent 一致的「全部会话聚合」逻辑
- **watch 模式 per-model 增量费用 USD 未转 CNY**：`_calc_cost()` 结果直接当 CNY 展示，Anthropic/Google 等 USD 模型费用显示偏低。3 处增量费用计算均改为 `_to_cny()` 统一转 CNY
- **watch 模式偶发假 delta 尖峰**：`bl_models` 在「无新活动」tick 时不更新，若某轮因文件读写竞态读到不完整数据，下一轮恢复后已累积的多轮 delta 会一次性显示为巨大尖峰。改为每轮无条件更新 baseline 并清理已消失模型

### 已知限制

- **DeepSeek Anthropic 端点费用偏差**：Claude Code 通过 `api.deepseek.com/anthropic` 使用 DeepSeek 模型时，API 返回的 `usage`（记录在 JSONL 中）与实际计费 tokens 使用不同 tokenizer 计数，导致预估费用偏高约 2-3 倍。此偏差源于 API 端点行为，非 token-stats 计算公式或价格错误。直接使用 DeepSeek 原生 API（如 Hermes）的费用预估是准确的。

## v2.5.8 (2026-05-22)

### 修复

**`--all` 全部 Agent 总计漏算 CodeX 数据**
- `show_all()` 和 `-a agent1,agent2` 两条路径的"全部 Agent 总计"都从 `per_model` 汇总（结构统一），不再从 `stats` 字典读（各 Agent key 不一致，导致 CodeX 的 `total_tokens`/`session_count` 无法匹配 `input_tokens`/`output_tokens`，数据被跳过）
- 导出路径本来就是从 `per_model` 读的，不受影响

## v2.5.7 (2026-05-21)

### 优化

**watch 增量段改为纯增量显示**
- 增量段不再混入全量数字（全量在"今日"段已有），每列只展示本轮变化量：`入 +122 | 出 +564 | 缓 +322.82K | 总计/+缓存 +686/+1.01M | 调用 +2`
- 看着更清爽，一眼就知道这轮消耗了多少

## v2.5.6 (2026-05-21)

### 优化

**watch 模式显示更直观**
- 增量行统一列结构：`入 +344/12.97M | 出 +858/6.16M | 缓 +89.09K/3023.45M | 总计/+缓存 19.13M/3042.58M | 调用 12432`，与其他行的列一一对齐
- `+` 号从标签前移到数字前（`+344入` → `入 +344`），读起来更自然
- 上面增量段只显示本轮有变化的模型，没活动的模型不再重复刷屏（今日汇总里已经能看到全貌）

## v2.5.5 (2026-05-21)

### 新增

**watch 跨天检测**
- 午夜自动重置今日统计，不会把昨天的数据算进今天
- 停止汇总时如果跨过天，会拆分显示昨日累计 + 今日累计，分段清晰

## v2.5.4 (2026-05-20)

### 修复

**数据太慢？**
- Windows 上如果 AI 助手的数据在 WSL2 里，以前查询要等 30 秒（数据库被 WSL 文件桥卡死），现在不到 1 秒
- 年度导出以前要"收两次数据"，现在只收一次，选完格式就直接导出

**表格对不齐？**
- 对比模式（`--compare`）的表头不再把第一条数据覆盖掉，所有列垂直对齐
- 不同模型之间加了分隔线，一眼就能区分

**Windows 导出打不开？**
- Excel 导出的文件以前是空的，因为中文工作表名在 Windows 上不兼容，现在改用英文名

**数字算错了？**
- `总计/+缓存` 那列的第二个数字以前只显示缓存值，现在正确显示"总计+缓存"的总和

**更新不管用？**
- `token-stats update` 现在有三次保障：先试常规更新 → 不行就强制重装 → 再验证版本号真的变了
- 无论从哪个渠道安装的（OpenClaw / ClawHub / 手动），都能正确更新

**安装/卸载的坑：**
- macOS 用 bash、Linux 用 zsh、或者用 fish shell 的人，PATH 不会被加错配置文件了
- Windows 上卸载后 PATH 不会残留（大小写、斜杠方向都考虑到了）
- 卸载后多余的空白行不会留在配置文件里

**其他小修：**
- 导出的表格不再有多余的空行
- CSV 格式也能正常导出

## v2.4.7 (2026-05-20)

## v2.4.7 (2026-05-20)

### 新增
- **watch 停止汇总增强**：显示监控时长 + 采集轮数

### 修复
- **年度导出 Agent 合计行 Model 列**：补充「合计」标签并正确合并单元格

## v2.4.6 (2026-05-20)

### 新增
- **对比模式重构**：按模型×指标完整对比（入/出/缓/总计/总计含缓存/调用）6 维度
- **`token-stats update`**：自更新指令，固定 workdir 为 ~ 并跳过二次确认

### 修复
- 单模型 Agent 导出不展示重复合计行，仅多模型时展示
- 导出合计行前加空行分隔

### 变更
- `-y` 短参数从 `--yesterday` 改为 `--year`

## v2.4.5 (2026-05-20)

### 修复
- unknown 零数据模型过滤
- Claude Code watch 缓存修复（主 collect 总是缓存）

## v2.4.4 (2026-05-20)

### 修复
- **unknown 模型未过滤**：`_build_aligned_raw` 增加 `_skip_model` 过滤，零数据模型不再显示
- **导出合计行无分隔**：所有 XLSX/CSV 导出在 Agent 合计 + 全部总计前加空行
- **CC watch 缓存再次修复**：磁盘重读后总是缓存消息，今日采集复用不再重复读盘

## v2.4.3 (2026-05-20)

### 修复
- **Claude Code 缓存导致 watch 模式失效**：缓存仅在带时间筛选时启用，无参 collect 始终重读磁盘
- **watch 刷新间隔不准**：循环改为先 collect 再 sleep，实际间隔从 ~10s 修正为 ~5s
- **控制台输出列不对齐**：新增 `_build_aligned_raw` 统一列对齐，全部 Agent 输出一致
- **缺少 Agent 合计行**：多模型时自动追加合计行（入/出/缓/总计/调用）
- **`--all` / 多 Agent 缺少 Grand Total**：末尾显示全部 Agent 总计

### 变更
- **`-y` → `--year`**：短参数从 `--yesterday` 改为 `--year`，`--yesterday` 仅保留长参数
- **导出格式顺序**：`[1] XLSX` / `[2] CSV` / `[3] JSON`
- **导出格式统一**：单/多 Agent 导出均含 Agent 名称列 + 合并单元格 + 单独合计 + 总合计
- `-e /path` 直接使用目录，跳过交互式提示
- watch 分割线加长到 60 列

### 新增
- **CSV 导出**：简单/年度 × 单/多 Agent 全覆盖
- **`token-stats update`**：自更新指令，调用 `clawhub update agent-usage-stats`

## v2.4.2 (2026-05-20)

### 修复
- ClaudeCodeAgent 重复 collect() 不再重读磁盘（消息缓存）
- 移除导出函数冗余的 today_calls 全量收集

### 新增
- CSV 导出格式，菜单顺序 XLSX/CSV/JSON

## v2.4.1 (2026-05-19)

### 变更
- **统一输出风格**：全部输出（快照/增量/今日/累计/导出）均包含独立 `缓` 列 + `总计/+缓存` 合并列
- **多 Agent 导出合并**：单 Sheet 单 XLSX 文件，含 Agent 小计 + 全部总计
- **上下文 Agent 优化**：Hermes/OpenClaw 保留上下文进度条 + 统一融入缓存列

### 修复
- XLSX 导出数据为空（ElementTree text 属性 vs 文本内容 + shared strings 构建顺序）
- CodeX/Hermes SQLite 连接超时（增加 5s/10s timeout 防 hang）
- watch 今日合计列统一对齐

## v2.4.0 (2026-05-19)

### 新增
- **短参数支持**：`-t` (--today), `-y` (--yesterday), `-m` (--month), `-w` (--watch), `-e` (--export), `-v` (--version), `-l` (--list-backends)
- **--month / --year 快捷参数**：直接查看本月/本年统计，无需手动指定 --from/--to
- **--year 月度拆分导出**：年度导出时按月分列展示（1~12月），每月独立统计 + 总计行
- **XLSX 导出**：纯标准库实现，零外部依赖。格式选择 [1] XLSX [2] JSON
- **总计(含缓存)**：新增含缓存的总计指标，区分有无缓存的两类总量
- **数据计算进度提示**：慢速操作（收集数据、对比、月度拆分）时显示进度信息
- **管道/脚本模式**：导出交互支持 EOF 保护，回车使用默认值
- **CHANGELOG.md**：版本更新记录文档

### 变更
- `总计` 和 `缓存` 合并显示为 `总计/+缓存 X/Y`
- 导出格式从 CSV 改为 XLSX（JSON 保留为选项 2）
- 帮助文本更新，展示所有短参数

### 修复
- WSL fallback 异常返回类型修复（元组 → None）
- run_compare 增加 _skip_model 过滤
- export_multi 预过滤空数据 Agent
- parse_time_label 支持 month/year 短别名
- label_to_display 支持 month/year 标签

---

## v2.3.8 (2026-05-18)

- watch 模式列对齐 + 数值精度优化

## v2.3.7 (2026-05-17)

- watch 样式升级：进度条+颜色+虚线框+今日合计

## v2.3.6

- -b→-a/--agent 语义化 + 统计原理说明

## v2.3.5

- 时间过滤修复 + 监控增量增强
