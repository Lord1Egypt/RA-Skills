# Changelog

## v2.6.1 (2026-05-23)

### 修复

- **`agent-usage-stats update` 漏搜本地 `skills/` 目录**：`clawhub install` 安装到当前目录的 `./skills/` 时，update 代码只搜索 `~/skills/` 和 `~/.clawhub/skills/`，导致版本检测失败。已将脚本所在目录的 `skills/` 加入搜索路径

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

- **DeepSeek Anthropic 端点费用偏差**：Claude Code 通过 `api.deepseek.com/anthropic` 使用 DeepSeek 模型时，API 返回的 `usage`（记录在 JSONL 中）与实际计费 tokens 使用不同 tokenizer 计数，导致预估费用偏高约 2-3 倍。此偏差源于 API 端点行为，非 agent-usage-stats 计算公式或价格错误。直接使用 DeepSeek 原生 API（如 Hermes）的费用预估是准确的。

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
- `agent-usage-stats update` 现在有三次保障：先试常规更新 → 不行就强制重装 → 再验证版本号真的变了
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
- **`agent-usage-stats update`**：自更新指令，固定 workdir 为 ~ 并跳过二次确认

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
- **`agent-usage-stats update`**：自更新指令，调用 `clawhub update ai-agent-usage-stats`

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
