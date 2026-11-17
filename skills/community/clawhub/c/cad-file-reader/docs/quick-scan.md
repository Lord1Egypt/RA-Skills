# 快速读取命令集

原 SKILL.md 章节，按需查阅。

## 快速读取

```bash
# 大图优先：构件编号、图层、关键词、图框
scripts/cad_scan.sh 图纸.dwg --only 梁,板,柱,墙 --cluster 1500 --format md -o 图纸扫描

# 关键词与原文证据
scripts/cad_scan.sh 图纸.dwg --search "板厚|C30|抗震等级|保护层|22G101"

# 需要识图几何和详情时
scripts/cad_scan.sh 图纸.dwg --only 梁,板,柱,墙 --with-mtext --with-geom \
  --cluster 1500 --detail-json 图纸详情.json --format all -o 图纸扫描

# 大图首次全量扫描并建本机证据缓存
scripts/cad_scan.sh 图纸.dwg --with-geom --with-geom-layer \
  --cache-dir /tmp/cad-file-reader-cache --format all -o 图纸扫描

# 同图重复查询：命中缓存后按图面矩形局部读取
scripts/cad_scan.sh 图纸.dwg --with-geom --with-geom-layer \
  --cache-dir /tmp/cad-file-reader-cache --roi 0,0,30000,20000 --format json -o 局部读取

# 省 Token：精简输出（默认完整；显式 --concise 精简候选主干，--full/--with-evidence 恢复完整）
scripts/cad_scan.sh 图纸.dwg --concise --format json -o 图纸精简

# 交付常用：同一结果同时导出 Markdown/JSON/CSV/Excel/Word
scripts/cad_scan.sh 图纸.dwg --only 梁,板,柱,墙 --cluster 1500 \
  --detail-json 图纸详情.json --format all -o 图纸扫描
# 单独导出 Excel 或 Word（需 --out 指定前缀）
scripts/cad_scan.sh 图纸.dwg --only 梁,板,柱,墙 --format xlsx -o 图纸扫描
scripts/cad_scan.sh 图纸.dwg --only 梁,板,柱,墙 --format docx -o 图纸扫描
# 同图重复查询：命中缓存后按图框编号局部读取
scripts/cad_scan.sh 图纸.dwg --with-geom --with-geom-layer \
  --cache-dir /tmp/cad-file-reader-cache --sheet 1 --format json -o 图框读取
```

