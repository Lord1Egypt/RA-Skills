# 批量识图台账

## 批量识图台账（scripts/cad_batch.sh）

批量扫图输出候选级台账，复用 `cad_scan` 引擎：

```bash
scripts/cad_batch.sh 图纸目录 --out 台账 --glob "*.dwg;*.dxf" --recursive
scripts/cad_batch.sh 图纸目录 --out 台账 --resume        # 按 SHA-256 断点续跑
scripts/cad_batch.sh 图纸A.dwg 图纸目录 --out 台账 --glob "*.dxf" --cache-dir /tmp/cad-cache
```

- 输出 `<out>/识图台账.xlsx`：`识图台账` sheet 每候选一行，含 `复核原因 / 证据坐标 / 来源文件` 列，
  `review_required` / 置信度<0.5 / 复核原因非空的行黄底；每图一个 `汇总·图名` sheet 与整体 `图纸汇总` sheet
  （候选人 / 复核人 / 缺口）。
- 输出 `<out>/自检汇总.md`：逐图列出 可交付 / 需人工复核 / 失败跳过 / 缺输入。
- 单图失败不中断整批；`--resume` 用 `_state.json` 按源文件 SHA-256 跳过已成功图。
- 每图写入 `_contract/<图名>.json`（cad-file-reader/v0，逐候选 `final_quantity=false`），可 `scripts/cad_validate.sh 校验`。
- 大图仍走 `cad_scan` 的 `mem_guard`/时间预算；`--budget` 可调单图时间预算。

缓存键使用源文件 SHA-256 和影响证据内容的扫描参数档；`--roi`、`--sheet` 只做查询过滤。ROI 几何使用预归一化 bbox 索引，缓存写入先批量落库、延后建索引。JSON 的 `cache.hits/misses` 记录命中情况。局部结果只返回命中范围内的证据，不混入整图块统计。
缓存只保存识图证据，不保存最终工程量、扣减、材料量、造价或结算量。
JSON 汇总输出 `cache.read_ms/write_ms/db_files/db_bytes`；每个文件输出 `cache_read_ms/cache_write_ms/cache_bytes`。
缓存盘点/清理用 `scripts/cad_cache_admin.sh 缓存目录`：默认只读盘点；`--cleanup` 生成计划，`--apply` 才删除。temp/legacy 默认进入计划；corrupt/unknown 永不删除；current 默认保留，必须显式 `--include-current` 且提供 `--max-age-days` 或 `--max-total-mb`。

口径：`原文次数`不是根数；`--count-by auto`优先平法集中标注，缺集中标注退回标注位置去重。
`--with-geom`提供图面几何候选和证据；需要长度/面积/体积候选时再用 `cad_measure`，输出始终带 `final_quantity=false`。
