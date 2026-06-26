---
name: dxf-handle
description: DWG/DXF CAD 图纸处理工具。使用 ezdxf 读取图纸，遍历图层信息，计算面积或周长。适用于室内设计房间量房统计。
---

# Dxf-Handle

DWG/DXF 图纸图层遍历和面积/周长计算工具。

## 前提条件

```bash
pip install ezdxf
```

## 使用方法

使用技能时需要提供：
1. **DWG 文件路径**（必填）
2. **图层配置 JSON**（必填，参考下方格式）
3. **查询模式**（四选一）：
   - 全部查询面积
   - 全部查询周长
   - 单个查询面积
   - 单个查询周长

## 图层配置格式

在 `references/layers.json` 中配置图层：

```json
{
  "layers": [
    {"layerName": "JS_客厅区域框线", "description": "客厅"},
    {"layerName": "JS_主卧区域框线", "description": "主卧"},
    {"layerName": "JS_次卧区域框线", "description": "次卧"},
    {"layerName": "JS_客卧1区域框线", "description": "客卧1"},
    {"layerName": "JS_客卧2区域框线", "description": "客卧2"},
    {"layerName": "JS_南阳台区域框线", "description": "南阳台"},
    {"layerName": "JS_北阳台区域框线", "description": "北阳台"},
    {"layerName": "JS_厨房区域框线", "description": "厨房"},
    {"layerName": "JS_公卫区域框线", "description": "公卫"},
    {"layerName": "JS_内卫区域框线", "description": "内卫"}
  ]
}
```

## 命令示例

### 1. 全部查询面积
计算所有配置图层的面积

```bash
python skills/dxf-handle/scripts/dxf_handle.py 你的图纸.dwg --type area
```

**输出示例：**
```
读取文件: 你的图纸.dwg
计算类型: area
配置了 10 个图层
扫描图层...
  找到: JS_客厅区域框线 (1 个多段线)
  找到: JS_主卧区域框线 (1 个多段线)

共匹配 2 个图层, 其中 2 个有有效数据
----------------------------------------
客厅: 25.60 m²
主卧: 18.20 m²

完成!
```

### 2. 全部查询周长
计算所有配置图层的周长

```bash
python skills/dxf-handle/scripts/dxf_handle.py 你的图纸.dwg --type perimeter
```

**输出示例：**
```
读取文件: 你的图纸.dwg
计算类型: perimeter
配置了 10 个图层
扫描图层...

共匹配 0 个图层, 其中 0 个有有效数据

未找到匹配的实体
```

### 3. 单个查询面积
查询指定房间的面积

```bash
python skills/dxf-handle/scripts/dxf_handle.py 你的图纸.dwg --query 客厅 --type area
```

**输出示例（有图层）：**
```
客厅: 25.60 m²
```

**输出示例（无图层）：**
```
没找到客厅图层
```

### 4. 单个查询周长
查询指定房间的周长

```bash
python skills/dxf-handle/scripts/dxf_handle.py 你的图纸.dwg --query 客厅 --type perimeter
```

**输出示例（有图层）：**
```
客厅: 20.30 m
```

**输出示例（无图层）：**
```
没找到客厅图层
```

## CSV 导出

使用 `--output` 参数导出 CSV 文件：

```bash
python skills/dxf-handle/scripts/dxf_handle.py 你的图纸.dwg --type area -o result.csv
```

**CSV 格式：**
```csv
名称,图层,数量,面积
客厅,JS_客厅区域框线,1,25.60
主卧,JS_主卧区域框线,1,18.20
```
