# CAD批量处理 - AutoCAD自动化工具

## 功能

满足室内设计师对CAD图纸批量处理需求：

### 1. 📥 读取/解析DWG/DXF
- 提取图层信息（名称/颜色/线型）
- 提取所有文字坐标内容
- 提取块和块属性
- 提取线段坐标
- 输出JSON格式方便后续处理

### 2. ✏️ 批量修改
- **批量文字替换**：文件夹内所有DXF替换指定文字（比如改项目名称、图框信息）
- **重命名图层**：批量修改图层名称
- **修改块属性**：修改图框块的属性值（项目名称、日期等）
- **修改图层颜色**：批量调整图层颜色

### 3. 📐 生成DXF
- 按指令添加墙线（支持指定厚度）
- 添加窗户
- 添加门（带开启弧线）
- 添加尺寸标注
- 添加文字标注
- 自动生成平面/立面DXF，可直接在AutoCAD打开编辑

### 4. 📦 批量处理
- **批量重命名**：按前缀+序号批量重命名
- **自动备份**：整个项目文件夹备份CAD文件
- **PDF添加水印**：给导出的PDF批量添加工作室水印
- **批量导出PDF**：框架已搭，可适配本地CAD命令行导出

## 安装依赖

```bash
pip install ezdxf
# 如果需要PDF水印功能，额外安装：
pip install PyPDF2 reportlab
```

## 使用方法

### 提取信息
```bash
# 提取所有信息到JSON
python cad_utils.py input.dxf output.json
```

### 批量修改
```bash
# 批量替换文字（整个文件夹）
python batch_modify.py text ./project "旧项目名" "新项目名"

# 重命名图层
python batch_modify.py layer drawing.dxf "旧层名" "新层名"

# 修改块属性
python batch_modify.py attr drawing.dxf "TitleBlock" "ProjectName" "新项目名称"

# 修改图层颜色
python batch_modify.py color drawing.dxf "WALL" 7
```

### 生成图纸
```python
from generate_dwg import CADGenerator
gen = CADGenerator()
# 添加外墙
gen.add_wall((0, 0), (6000, 0), 240)
gen.add_wall((0, 0), (0, 4000), 240)
# 添加窗
gen.add_window((2000, 4000), 2000)
# 添加门
gen.add_door((120, 1500), 900)
# 保存
gen.save("output.dxf")
```

### 批量处理
```bash
# 批量重命名
python batch_export.py rename ./dwg "项目名-" 1

# 自动备份
python batch_export.py backup ./项目 ./项目_backup

# PDF添加水印
python batch_export.py watermark input.pdf output.pdf "温州隐室空间设计"
```

## 适用场景

- 项目改名批量改图框文字
- 新项目快速生成基础平面
- 批量导出PDF给客户
- 项目归档自动备份重命名
- 整理图纸统一图层规范

## 作者

温州隐室空间设计 · 数字化项目部（铁臂）
