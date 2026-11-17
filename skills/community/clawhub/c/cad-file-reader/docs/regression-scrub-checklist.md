# cad-file-reader 真实图纸回归与发布脱敏清单

> 本清单不写任何具体项目路径/图号/公司名；真图清单 `--manifest` 由使用者放在技能包之外管理，禁止写入发布包。

## 1. 回归覆盖矩阵

| 专业包 | 入口脚本 | 验收最少计数键 | 真图来源类型 |
| --- | --- | --- | --- |
| 电气 | cad_electrical_geometry.sh | drawing_types, systems, route_segments, equipment, circuits, specs, fire_protection, weak_current, intelligent_building | 电气 DWG |
| 结构 | cad_structural_geometry.sh | drawing_types, systems, members, rebars, nodes, grids, structural_geometry | 结构 DWG |
| 总图/场地 | cad_site_geometry.sh | drawing_types, systems, components, references, site_geometry | 总图场地 DWG |
| 暖通/给排水 | cad_deep_geometry.sh --pack hvac_plumbing | drawing_types, systems, components, references, geometry | 安装 DWG |
| 精装修 | cad_deep_geometry.sh --pack interior_finish | 同上 | 精装修 DWG |
| 幕墙 | cad_deep_geometry.sh --pack curtain_wall | 同上 | 幕墙 DWG |
| 人防 | cad_deep_geometry.sh --pack civil_defense | 同上 | 人防 DWG |
| 预制装配 | cad_deep_geometry.sh --pack precast | 同上 | 装配式 DWG |
| SVG 几何 | cad_text_extract.sh | 文字/图示覆盖 | 基础识图 |
| PDF 分流 + OCR | cad_pdf_ocr.sh | 候选计数、review_required、图签栏 | 矢量/扫描/混合 PDF |

## 2. 回归执行方式

```bash
scripts/self_test.sh --manifest <本地真图清单>.json   # 三合一闭环：doctor + 自测 + 真图回归
```
真图回归单跑等价命令：
```bash
scripts/run_real_dwg_regression.sh --manifest <本地真图清单>.json --report-json <脱敏报告>.json
```

- 清单结构：`{"cases":[{"id":"...","name":"...","path":"/本地/介质/...","kind":"electrical|structural|site|...","expect":{...}}]}`
- **软件包本身不携带真图**；清单路径、图号、图纸字节一律不进入发布包。
- 每条 case 现在会先跑 `cad_scan`（含 mtext/insert/geom），再跑对应识图包 JSON，自动执行统一契约校验（`cad_contract.validate_contract_payload`），并在报告中输出 `contract_valid`。
- 验收：`report.total == report.passed`；每条结果 `contract_valid=true`；领域候选计数 ≥ expect；`review_items` 不为空或已说明。
- 报告只输出脱敏计数与状态，不含图纸内容。

## 2. 一键发布预检

```bash
scripts/run_preflight.sh                          # 全量自测 + 契约样例 + 脱敏扫描
scripts/run_preflight.sh --manifest 真图清单.json  # 再加上真实图纸回归
```
任一环节失败即视为未通过，禁止发布。

## 3. 发布前脱敏检查步骤（与 cad_release_scrub.py 一致）

1. 扫描发布范围：`python3 scripts/cad_release_scrub.py . --skip-dirs vendor,__pycache__,.git,node_modules,tests`
2. 五类敏感判定：绝对介质路径、文件摘要串、实测结果数值、标高数值、阶段产物名。
3. 白名单：语义版本号、接口版本 `v0.x`、耗时/内存标记、置信度阈值/规则权重/示例参数（代码常量不算实测）。
4. 发布前必须 0 命中；有命中先用 `--allow` 核对是否为例外，不是则就地打码后重新全量扫描。
5. PDF 示例、临时 `/tmp` 样例、缓存文件、`outputs/` 交付物不进发布包；只发布技能本体 + docs + scripts + packs + rules + schemas。

## 4. 回归通过判定

- 全量自测：`scripts/tests/*.py` 全部通过。
- 每项 P0 改动后跑一次对应单测 + 全量 `unittest discover`。
- 真图回归通过后，把脱敏报告路径记入本轮交付，不把原始图纸路径写进技能文档。
