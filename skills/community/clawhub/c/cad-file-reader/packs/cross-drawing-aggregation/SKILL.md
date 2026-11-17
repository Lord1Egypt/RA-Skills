# 跨图聚合与钢筋牌号

## 跨图聚合 / 图纸关系 / 钢筋牌号（识图之后的成表能力）

单张图只能回答「这张图有什么」。下面三个脚本把多张图的候选变成能直接看的表，仍是提取而非工程量。

| 脚本 | 作用 | 输出 |
|---|---|---|
| `scripts/drawing_relation.py` | 按项目目录聚类单体、楼层序列与缺口、专业判定、同层跨专业配对、**配对后轴网核对** | `clusters` / `floor_series` / `pairs`（含 `grid_check`），缺建筑图记 `missing_architecture` |
| `scripts/cad_axis_net.py` | **几何轴网提取**：按轴线实体还原轴网（方向/轴数/总跨/开间序列），供跨专业核对 | 被 `cad_structural_geometry` 写入 `axis_nets`；也可单独跑 `--inputs scan/*_detail.json` |
| `scripts/cad_axis_networks.py` | **可选 `axis_networks[]`（轴号+轴线→轴格区间）**：从 text_records 的 AXIS/轴号/轴标/轴网/定位 文字取轴号（数字轴/字母轴），在轴号坐标附近找同方向长线段作几何佐证，按 sheet 输出 axis_id/pos/grid.spans。**坐标只是佐证**；无轴网如实 `missing/degraded` | 复用已解析 `cad_scan` 详情 JSON，`--inputs scan/*_detail.json`；可并入 cad-file-reader/v0 contract（可选字段，向后兼容） |
| `scripts/project_aggregate.py` | 楼层×分区×类别×规格归并构件；按直径×牌号归并钢筋；楼层×直径交叉表 | `aggregate.json/.md/.csv`，`count` 即原始候选重复次数 |
| `scripts/rebar_grade.py` | 从本批图纸说明表反解「符号→牌号」，回填到钢筋型号 | `rebar-legend.json/.md` |

轴网核对的口径（重要，别说成「已证明是同一栋楼」）：

- **只认几何，不认文字**。轴号在天正转出的图里基本抓不到（实测轴网图层上 0 条文字），
  但轴线实体一直在——等长、平行、等距重复的直线就是它。
- **判据是「结构侧覆盖」**：结构柱网通常只是建筑轴网的子集（建筑多出外墙/门窗定位轴），
  所以看结构图的开间有多少能在建筑图里找到，不看两侧最大值。
- **开间支持「段和」匹配**：结构一个 3300 开间，建筑图可能被隔墙定位轴拆成 1650+1650。
- **能证明「不一致」，不能证明「是同一栋」**：同户型不同楼栋共用同一套轴网，
  间距会完全一致。核对结论为「轴网一致」只说明两图描述同一类平面，仍需人工确认楼栋/范围。

用法：

```bash
python3 scripts/rebar_grade.py --inputs scan/*_detail.json --out legend.json --md-out legend.md
python3 scripts/project_aggregate.py --inputs structural/*.json --legend legend.json --out aggregate.json --md-out aggregate.md
python3 scripts/drawing_relation.py --inputs structural/*.json --out relation.json
python3 scripts/cad_axis_networks.py --inputs scan/*_detail.json --out axis_networks.json
```

钢筋牌号这块有三条硬规矩：

1. **牌号只能来自本批图纸的说明表**。本批没有说明表就全部保持 `unknown`，不套国标默认值——不同项目图例可能自定义。
2. **映射不跨项目串用**。聚合层比对图纸名，来源不符直接弃用并记 `legend_source_mismatch`。跨项目套用会得出「全部 HRB400」这种看着完整实则错误的结果，比 unknown 更危险。
3. **两种依据分层**：说明表直接定义（`direct`，可核对原文）与按 CAD 字体尾号外推（`bridged`，`%%132` 与 `U+E532` 同尾号）。外推只到 `inferred_candidate`，表格里逐行标注，不混为一谈。

牌号回填需要 `detail` 产物（说明表是整段文字，只在 `text_records` 里）；只给 `structural` 时映射为空，会明确报出来而不是静默给 unknown。
