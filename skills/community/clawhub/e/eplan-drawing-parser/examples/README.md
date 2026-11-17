# Examples · 使用示例

## 示例1：解析 EPLAN 矢量 PDF（全部页）

```bash
# 精简输出（每页：导线数、文本数、拓扑节点、元件位号清单）
python3 scripts/extract_geom.py --input 燃料电池直流输出柜8-20.pdf --output out.json

# 完整输出（含所有文字 + 坐标）
python3 scripts/extract_geom.py --input drawing.pdf --output full.json --full
```

## 示例2：定位某一页的关键元件

解析后，`components` 字段给出每页的元件位号（含 FCM/断路器/熔断器/浪涌等），可直接用于核对 BOM 与图纸数量是否一致。

## 示例3：重建导线拓扑（识别串并联/流向）

调用顶层接口时，`num_wires` 和 `topology_nodes` 反映电路的复杂度和连接簇数量；结合 `knowledge/eplan_symbols.md` 可判断主功率线和信号线。

## 示例4：图纸 ↔ 清单核对（UL证书 / BOM）

将 EPLAN 图纸与 Excel 物料清单交叉核对位号/型号/数量，并检查无 UL 档案号条目：

```bash
# 自动识别含 "UL" 的 sheet
python3 scripts/check_bom.py --pdf 燃料电池直流输出柜0821.pdf --xlsx 清能3mw项目清单-08-21.xlsx

# 指定 sheet + 自定义导出路径
python3 scripts/check_bom.py \
    --pdf 燃料电池直流输出柜0821.pdf \
    --xlsx 清能3mw项目清单-08-21.xlsx \
    --sheet "UL证书汇总" \
    --out 核对结果.xlsx

# 只打印不导出
python3 scripts/check_bom.py --pdf a.pdf --xlsx b.xlsx --no-export
```

输出：控制台报告 + 彩色 xlsx（含「位号核对」「无UL档案号」两个 sheet）。

> 提示：若清单含多个柜（控制柜/供电柜/直流柜），而图纸只画了部分柜，"图纸缺失位号"会包含未画出的柜的位号，属正常；核对时聚焦目标柜即可。

## 输入要求

- **必须是 EPLAN/CAD 矢量 PDF**（含文本层 + 矢量线）
- 扫描件/图片 PDF 本 Skill 不处理（无文本层），需其他 OCR 流程

## 已知边界

- 布置图（如元件剪影图）导线数量会异常多（如页16 有 99799 条），但文本位号仍准确提取
- 跨页连接（至AGHxx）需结合多页结果人工/程序关联
