# CSV Wizard

交互式数据清洗 CLI，支持自动类型推断、缺失值处理、重复检测

## 功能特性

- 🔍 自动类型推断（数字、日期、布尔值、分类变量）
- 🧹 缺失值检测与多种填充策略
- 📊 数据统计摘要与预览
- 🔄 重复行检测与删除
- 📝 列名标准化与重命名
- 🎯 数据格式转换与导出

## 安装

作为 OpenClaw Skill 使用:
```bash
clawhub install csv-wizard
```

或直接使用:
```bash
git clone https://github.com/kimi-claw/skill-csv-wizard.git
cd skill-csv-wizard
./bin/clean-csv --help
```

## 使用方法

### 基本清洗

```bash
/clean-csv data.csv --output clean-data.csv
```

### 交互式清洗（推荐）

```bash
/clean-csv data.csv --interactive
```

### 预览数据信息

```bash
/clean-csv data.csv --info
```

### 处理缺失值

```bash
/clean-csv data.csv --fill-missing mean --output result.csv
```

### 删除重复行

```bash
/clean-csv data.csv --drop-duplicates --output result.csv
```

## 缺失值填充策略

- `drop` - 删除包含缺失值的行
- `mean` - 使用列均值填充（仅数值列）
- `median` - 使用中位数填充（仅数值列）
- `mode` - 使用众数填充
- `constant` - 使用固定值填充

## License

MIT
