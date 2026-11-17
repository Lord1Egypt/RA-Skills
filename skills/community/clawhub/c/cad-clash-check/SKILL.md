---
name: cad-clash-check
slug: cad-clash-check
displayName: 跨专业碰撞校对·按轴定位
version: 0.3.4
platforms: [macos, windows, linux]
author: lis
license: CC-BY-NC-SA-4.0
description: "碰撞与属性冲突候选；不替代复核。触发词：碰撞候选、管线综合。"
---

# cad-clash-check · 跨专业碰撞校对

**用户视角一句话**：把图纸塞给它，它把各个专业碰撞、打架的地方标出来。

## 它做什么

1. **识图**：DWG/DXF → cad-file-reader 识图（文字+几何），自动判定专业
   （结构/建筑/市政/MEP[电气·暖通·给排水]，其他专业如实跳过并说明）；
2. **构件清单**：按专业走对应几何提取器 → 统一清单（就近轴号 / 坐标桶诚实分级；
   MEP 消费 route_segments/equipment/risers，建筑合并结构与门窗提取出 wall/opening）；
3. **两两比对**：
   - **空间碰撞**：不同专业构件图面同位（bbox 间隙 ≤ `--clash-tol`，默认 800）→
     碰撞候选，按位置桶归组（一根管穿一排梁合并为一条），给坐标 + 双方构件名/属性；
   - **属性冲突**：同 key 构件两侧属性不一致（如截面/管径矛盾）→ conflict；
   - 同专业对额外保留占位差 warn；跨专业对只留 conflict（占位差不构成冲突）；
4. **报告**：`.json`（机器可读）+ `.md`（人读）+ `*_construct_plan.json/md`（施工计划模板）；
   每条碰撞带 sheet / floor / axis / 专业A/B坐标 / 类型。
5. **洞口语义**（v0.2）：MEP × 门窗洞口 = 预留通道（opening_pass）；墙 × 洞口 =
   正常关系（wall_pass），不计碰撞；墙 × MEP = 潜在穿墙无洞 → 仍进候选提示复核。
   识图器没产墙/洞口时如实 degraded，不冒充 pass。
6. **轴格主判**（v0.3）：两侧产物含 cad-file-reader `axis_networks[]` 且能组成轴格时，
   先把 bbox 映射到轴格区间，只比较落入同轴格的异专业构件，坐标为佐证不单独成依据；
   一侧缺轴网/轴格不可用时如实降级回坐标判定并标 `axis_missing=degraded`，不冒充 pass。

## 用法

```bash
# 一条龙：图纸直进
python3 scripts/cad_clash_check.py 结构.dwg 室外管网.dwg -o 报告/clash

# 离线：已有识图产物（*.structural.json / *.municipal.json）
python3 scripts/cad_clash_check.py a.detail.municipal.json b.detail.structural.json -o 报告/clash

# 调参：--clash-tol 碰撞距离上限（图面单位）；--place-tol 一致性位置容差
```

依赖：`cad-file-reader`（识图引擎，显式依赖；找不到时设
`CAD_FILE_READER_HOME` 指向其 scripts 目录）。

## 跨图碰撞的两个前提（0.1.1+）

1. **坐标同源**：不同 DWG 的图面摆放互不相干，跨图碰撞前必须确认两图共用
   同一总图坐标（判断法：构件 bbox 区间互相包含/同数量级），否则先做图纸
   配准，碰撞结果会是全量漏报的假象。
2. **构件三分类**（0.1.2+）：line（管线/道路线段）/ label（components 文字
   标注——贴着被标注构件是正常图面行为，前置剔除）/ entity（真几何实体）。
   0.1.3 起 entity 落地：识图产物 `entities`（圆实体，cad-file-reader 0.39.0+
   `--with-geom` 自动提取）→ kind=entity 成员（bbox=圆外接框，名=类别/etype 构造）。
   碰撞候选只认 entity 参与；同系统/同名同位剔除计数
   （dup_pairs）；线×线平面交叉计数（line_line_pairs，正常关系不可判）。
   全量统计不截断（scan_clashes），明细最多 2000 项。

## 红线（与全套件一致）

- **2D 图面候选提示，非 BIM 碰撞检测**：无 3D 模型、无标高核实；碰撞位置必须人工复核；
- `final_quantity=false`：不输出工程量；
- 图纸数据只落本机，不上云。

## 与 cad-suite 的关系

碰撞引擎与适配器自 `cad-suite/cross/`（engine.py / adapt.py）移植为本 skill 的
`clash_engine.py` / `clash_adapt.py`（差异：线段 geometry 保留两端 bbox）；
cad-suite 侧为公共库形态，本 skill 为独立交付形态，行为以单测双向钉住。

## 测试

```bash
cd scripts && python3 -m unittest discover -s tests
```
