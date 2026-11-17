# 最小可用契约示例

`minimal.steel.json` 是手工构造 `cad-steel-geometry/v1` 的最小可用样本，可直接运行：

```bash
python3 scripts/steel_tonnage.py --check-deps
python3 scripts/steel_tonnage.py --validate examples/minimal.steel.json --report /tmp/minimal-health.json
python3 scripts/steel_tonnage.py --steel examples/minimal.steel.json --allow-manual --out-prefix /tmp/minimal-ton
```

`--check-deps` 只影响正式识图链路；本示例是文件/手工契约，必须显式加 `--allow-manual`，输出 `provenance=manual`、`formal_ledger_eligible=false`、`final_quantity=false`，不是正式量。`--validate` 可计算时退出 0、结构错误退出 2，且不写吨位文件。

## 必填字段

| 字段 | 要求 |
|---|---|
| `schema` | 必须是 `cad-steel-geometry/v1` |
| `sections[]` | 数组；每项含 `section_type` 与 `text`，建议带 `evidence` |
| `members[]` | 数组；每项含 `code` 或 `name`，长度证据写在 `evidence[].text` 的 `L=4500` / `长度4500` |
| `steel_geometry[]` | 数组；可为空，但字段必须存在；每段 `layer` + `geometry:[x0,y0,x1,y1]`（mm） |

`sections`、`members`、`steel_geometry` 三项不能同时为空，否则体检直接判 `error`；体检失败退出码 2，不写吨位文件。

## 可选字段

| 字段 | 用途 |
|---|---|
| `materials[]` | 牌号分档；`grade` 或 `raw/text` 带 Q235/Q355/Q460 等前缀 |
| `connections[]` | 螺栓/锚栓/栓钉/节点板/加劲肋计数；节点板要有厚宽长或板厚×面积证据 |
| `finishes[]` | 底漆/面漆/热浸镀锌/防火涂料面积 |
| `geometry_closure` | 识图层给出的圆/线段闭合校核结果，原样透传到 `geometry_closure_check` |

## 截面与构件怎么配对

三条任一命中即视为配对，多条命中取并集：

1. **文本**：截面 `text` 出现在构件证据文本里。比较时 `×`/`X` 统一成 `x`、去掉空格、忽略大小写。例：截面 `Φ1200x50` 能匹配构件证据 `Z1 Φ1200x50 L=4500`。
2. **同上下文**：两者 `file` 与 `sheet` 相同（都给出时）。
3. **空间邻近**：两者都有 `x`/`y` 时，平面距离 ≤ 1500 图纸单位（通常是 mm）。

配对不上就进复核清单，不会硬套截面。

## 坐标与单位

- 图纸坐标一律按 **mm** 写；本技能输出 `coord_unit="mm"`，不自动换算。
- `members[].x/y/z/rotation` 可选，但下游做吊装覆盖、堆场、分区分析时必须提供；缺失时 `location_status="missing"`。
- 块参照里的坐标要先展开成世界坐标再写入，不能直接用块定义内的 (0,0)。

## 图层名

国内图纸常见 `X-T-Cols&Wall-F3$0$dsptext_col` 这类嵌套图层名。契约里建议同时给原始 `layer` 和末段 `layer_leaf`（按 `$` 分段取最后一段）。

## 总吨位两个口径

- `total_t`：主口径。全部构件编号都有显式长度且单截面映射时取逐根台账求和并标“推荐”；否则退回分摊估算并标“分摊草稿，不是答案”。
- `total_t_allocated_estimate`：米重×标注次数分摊，仅草稿对照。
- `total_basis` 标明当前用的是 `member_level` 还是 `allocated_estimate`。
