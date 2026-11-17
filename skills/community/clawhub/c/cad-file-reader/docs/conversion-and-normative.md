# cad-file-reader 转换与规范辅助命令

> 从 `SKILL.md` 外移，内容保持原样。触发条件：需要 DWG→DXF 转换、批量转换，或要做说明/构件规则/规范图集初解时读取本文件。

## DWG 转 DXF

```bash
scripts/convert_dwg.sh 图纸.dwg --out 图纸.dxf
scripts/convert_dwg.sh 图纸目录 --recursive --out 输出目录
```

默认输出已存在不覆盖；大文件有 200MB 入口闸和内存看门狗，必要时才显式放开。

## 说明、规范与图集辅助

```bash
# 1. 抽取说明文字、标注和图纸参数
scripts/cad_scan.sh 图纸.dwg --with-mtext --with-geom \
  --detail-json 图纸详情.json --format json -o 图纸扫描

# 2. 解读构件规则、引用目录和缺失输入
scripts/cad_interpret.sh --scan 图纸扫描.json --detail 图纸详情.json \
  --rules rules --format all -o 图纸解读

# 3. 定位规范/图集元数据、版本风险、参数冲突和资料入口
scripts/cad_normative.sh --scan 图纸扫描.json --detail 图纸详情.json \
  --rules rules --format all -o 规范辅助
```

规范辅助输出：已索引/未索引编号、现行/旧版/待确认状态、知识库相对路径或在线入口、缺少的设计输入、多参数冲突。`rules/standards.json`只保存编号、名称、专业、状态和资料入口元数据；条文适用性以图纸指定版本和授权全文为准。
