# Excel Batch Processor - Excel 批量处理工具

## 功能描述
批量处理 Excel 文件的自动化工具，支持合并、拆分、格式转换、数据清洗等操作。

## 使用场景
- 多个 Excel 文件合并为一个
- 大文件拆分为多个小文件
- Excel 与 CSV 互相转换
- 批量修改单元格格式
- 数据清洗和去重
- 公式批量填充

## 命令

### 合并文件
```
合并 Excel 文件列表=file1.xlsx,file2.xlsx,file3.xlsx 输出=merged.xlsx
```

### 拆分文件
```
拆分 Excel 文件=source.xlsx 按=工作表 输出目录=./output
```

### 格式转换
```
转换 Excel 到 CSV 文件=input.xlsx 输出目录=./output
```

### 数据清洗
```
清洗 Excel 文件=input.xlsx 操作=去重，删除空行 输出=cleaned.xlsx
```

### 批量填充
```
批量填充 Excel 文件=*.xlsx 单元格=A1 值=公司名称 输出目录=./output
```

## 输出格式
- Excel (.xlsx)
- CSV (.csv)

## 特性
- 支持通配符批量处理
- 保持原有公式和格式
- 大文件优化处理
- 错误自动跳过
