# Address Classifier Skills - 文件清单

## 项目结构

```
address_classifier_skills/
├── SKILLS_DOCUMENT.md          # [Skills文档] 主要文档，包含完整代码和说明
├── README.md                   # [说明文档] 项目简介和使用指南
├── MANIFEST.md                 # [本文件] 文件清单和说明
├── requirements.txt            # Python依赖列表
├── run.py                      # 快速启动脚本
├── test.py                     # 功能测试脚本
├── src/
│   └── address_classifier.py   # [核心代码] 地址分类器完整实现
├── config/
│   └── config.yaml             # [配置文件] 行政区划映射配置
└── examples/
    └── sample_data.txt         # [示例数据] 17条测试数据
```

## 文件说明

### 1. SKILLS_DOCUMENT.md（核心文档）
**用途**: 上传到ClawHub的主要Skills文档
**内容**:
- 完整的Python类实现（可直接复制使用）
- 输入输出规范
- 配置参数说明
- 使用示例
- 扩展指南

**适用对象**: AI助手、开发者、系统集成人员

### 2. src/address_classifier.py（生产代码）
**用途**: 可直接部署到生产环境的核心模块
**特性**:
- 完整的异常处理
- 日志记录系统
- 配置驱动设计
- 支持批量和单条处理
- 支持多种输出格式（TXT/CSV/JSON）

**适用对象**: 生产环境部署

### 3. config/config.yaml（配置文件）
**用途**: 行政区划映射和规则配置
**可配置项**:
- 目标省份/城市
- 省内城市映射
- 搜索补全规则
- 输出格式设置

**适用对象**: 需要自定义行政区划的用户

### 4. examples/sample_data.txt（示例数据）
**用途**: 测试和演示
**包含**:
- 本省本市样本（贵阳各区县）
- 本省外市样本（毕节、遵义等）
- 外省样本（四川、山东等）
- 地址不全样本

### 5. run.py（启动脚本）
**用途**: 命令行快速运行
**用法**: `python run.py input.txt [output.txt]`

### 6. test.py（测试脚本）
**用途**: 验证分类规则正确性
**用法**: `python test.py`

## 快速开始

### 方式1：使用Skills文档（推荐AI助手使用）
直接参考 `SKILLS_DOCUMENT.md` 中的代码和说明。

### 方式2：直接运行（推荐生产部署）
```bash
# 安装依赖
pip install -r requirements.txt

# 运行测试
python test.py

# 处理数据
python run.py examples/sample_data.txt output/result.txt
```

### 方式3：作为模块导入
```python
from src.address_classifier import AddressClassifier

classifier = AddressClassifier()
result = classifier.classify("001", "贵州省贵阳市南明区测试路1号")
print(result.classified_result)  # 贵州贵阳南明
```

## 关键功能验证清单

- [x] 识别贵阳市主城区（南明、云岩、观山湖等）
- [x] 识别贵阳市下辖县市（开阳、息烽、修文、清镇）
- [x] 识别省内其他市州（毕节、遵义、安顺等）
- [x] 识别外省地址（四川、山东、河南等）
- [x] 搜索补全功能（西河镇->重庆、英庄镇->河南等）
- [x] 地址不全检测（仅省市名、长度过短等）
- [x] 输出大类标识（本省本市/本省外市/外省/地址不全）
- [x] 支持多种输出格式（TXT/CSV/JSON）

## 生产部署检查项

部署前请确认：
1. Python版本 >= 3.7
2. 输入文件编码为UTF-8
3. 输入文件使用制表符分隔
4. 已根据实际需求更新config.yaml中的行政区划映射
5. 已测试样本数据验证分类准确性

## 版本信息

- 版本: 1.0.0
- 更新日期: 2024-03-09
- 支持区域: 贵州省及全国其他省份
