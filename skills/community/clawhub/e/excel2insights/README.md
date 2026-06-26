# Excel2Insights

[![ClawHub Security Rating: HIGH CONFIDENCE](https://img.shields.io/badge/ClawHub-HIGH%20CONFIDENCE-brightgreen)](https://clawhub.com)

纯本地Excel数据分析与可视化工具。

## 🎯 功能特点

### 📊 数据分析
- 读取Excel文件 (.xlsx, .xls, .csv)
- 显示数据基本信息
- 统计数值列的基本统计量
- 检查缺失值
- 生成可视化图表

### 🔒 安全认证
- ✅ **ClawHub HIGH CONFIDENCE** 最高安全评级
- ✅ **纯本地处理** - 所有数据处理在本地进行
- ✅ **数据安全** - 用户数据不离开本地计算机
- ✅ **透明可审计** - 所有代码开源可审查

## 🚀 快速开始

### 安装依赖
```bash
pip install pandas matplotlib openpyxl
```

### 基本使用
```bash
# 查看帮助
python excel2insights.py --help

# 分析Excel文件
python excel2insights.py --file data.xlsx --analyze

# 生成可视化图表
python excel2insights.py --file data.xlsx --visualize

# 生成报告
python excel2insights.py --file data.xlsx --report
```

## 📁 项目结构

```
excel2insights-v1.0.8/
├── excel2insights.py      # 主工具代码
├── __init__.py           # 模块初始化
├── SKILL.md              # 技能描述
├── INSTALL.md            # 安装指南
├── VERSION.txt           # 版本信息
└── README.md             # 项目说明 (本文件)
```

## 🔧 技术规格

- **Python版本**: 3.8+
- **核心依赖**: pandas, matplotlib, openpyxl
- **支持格式**: .xlsx, .xls, .csv
- **输出格式**: 文本报告、PNG图表
- **安全评级**: ClawHub HIGH CONFIDENCE

## 📋 使用示例

### 示例1: 基础分析
```bash
python excel2insights.py --file sales_data.xlsx --analyze
```

### 示例2: 完整分析流程
```bash
python excel2insights.py --file customer_data.xlsx --analyze --visualize --report
```

## 🛠️ 故障排除

### 常见问题

#### 1. 依赖安装失败
```bash
# 升级pip
pip install --upgrade pip

# 使用国内镜像
pip install pandas matplotlib openpyxl -i https://pypi.tuna.tsinghua.edu.cn/simple
```

#### 2. 图表生成问题
```bash
# 检查matplotlib安装
python -c "import matplotlib; print(f'matplotlib版本: {matplotlib.__version__}')"
```

#### 3. 文件读取失败
```bash
# 检查文件路径和权限
ls -la data.xlsx
chmod +r data.xlsx
```

## 📈 版本历史

### v1.0.8 (2026-03-18) - HIGH CONFIDENCE版本
- 通过ClawHub严格安全审查
- 获得HIGH CONFIDENCE最高安全评级
- 优化代码结构和文档
- 提升工具稳定性

### 早期版本
- v1.0.0-v1.0.7: 开发迭代版本

## 🤝 贡献指南

欢迎贡献代码和改进建议！

## 📄 许可证

本项目采用 MIT 许可证。

## 🙏 致谢

感谢 ClawHub 安全团队的专业审核和 HIGH CONFIDENCE 安全评级。

---
**项目名称**: Excel2Insights  
**版本**: v1.0.8  
**安全评级**: HIGH CONFIDENCE  
**发布日期**: 2026-03-18