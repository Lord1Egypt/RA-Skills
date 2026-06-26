# 地址智能分类器 (Address Classifier)

## 功能简介

将中国地址按照行政区划进行智能分类，支持以下分类维度：

1. **本省本市**：目标城市（如贵州省贵阳市）下辖的所有区县
2. **本省外市**：同一省份（如贵州省）内其他城市/自治州
3. **外省**：其他省份及直辖市
4. **地址不全**：信息缺失无法分类的地址

## 分类规则详解

### 1. 本省本市（贵州省贵阳市）
- **主城区**：南明区、云岩区、观山湖区、花溪区、乌当区、白云区、小河区
- **下辖县市**：开阳县、息烽县、修文县、清镇市（这些虽然名为县/市，但属于贵阳市管辖）
- **输出格式**：`贵州贵阳{区县}`，例如：`贵州贵阳南明`、`贵州贵阳开阳`

### 2. 本省外市（贵州省其他市州）
- **地级市**：遵义市、安顺市、毕节市、铜仁市、六盘水市
- **自治州**：黔东南州、黔南州、黔西南州
- **识别逻辑**：通过市州名或下辖县区名自动识别
- **输出格式**：`贵州{市州}`，例如：`贵州遵义市`、`贵州毕节市`

### 3. 外省
- **完整地址**：直接提取省份名
- **不完整地址**：通过内置搜索补全库识别（如"西河镇新四村"→重庆市）
- **输出格式**：`外省{省份}`，例如：`外省四川省`、`外省重庆市`

### 4. 地址不全
- 仅有省市名无具体区县（如"河南省焦作市"）
- 地址长度过短（少于8个字符）
- 有乡镇村名但无省市信息且无法补全

## 安装依赖

```bash
pip install -r requirements.txt
```

## 快速开始

### 方式一：命令行使用

```python
from src.address_classifier import AddressClassifier

# 初始化分类器（使用默认配置）
classifier = AddressClassifier()

# 处理文件
stats = classifier.process_file(
    input_path="examples/sample_data.txt",
    output_path="output/result.txt"
)

print(f"处理完成，共处理 {stats['total']} 条记录")
```

### 方式二：批量处理

```python
addresses = [
    ("202020001", "贵州省贵阳市南明区沙冲南路226号..."),
    ("202020018", "西河镇新四村11组32号"),
    ("202020032", "贵州省仁怀市长岗镇丰岩村..."),
]

results = classifier.batch_classify(addresses)
for result in results:
    print(f"{result.id}: {result.classified_result} ({result.category})")
```

### 方式三：自定义配置

```python
config = {
    'target_province': '贵州省',
    'target_city': '贵阳市',
    'target_city_short': '贵阳',
    'output_format': 'csv',  # 支持 txt/csv/json
    'enable_search_completion': True,
    'log_level': 'DEBUG'
}

classifier = AddressClassifier(config)
classifier.process_file("input.txt", "output.csv")
```

## 配置文件说明

配置文件位于 `config/config.yaml`，包含以下主要配置项：

### target_region（目标区域）
定义"本省本市"的范围：
- `province`: 目标省份全称
- `city`: 目标城市全称
- `city_short`: 输出时使用的简称
- `counties`: 目标城市下辖的县/县级市映射

### province_cities（省内其他城市）
定义省内其他市州及其下辖县区，用于自动识别归属。

### search_completion（搜索补全）
定义不完整地址的补全规则：
- `enabled`: 是否启用
- `mappings`: 关键字到归属地的映射

### output（输出配置）
- `format`: 输出格式（txt/csv/json）
- `encoding`: 文件编码
- `delimiter`: 分隔符（仅txt格式）

## 输入输出格式

### 输入格式
制表符分隔的文本文件，包含两列：
```
id	地址
202020001	贵州省贵阳市南明区沙冲南路226号3栋3单元3楼1号
202020002	贵州省贵阳市南明区红岩冲57号
```

### 输出格式（TXT）
```
id	原地址	分类结果	大类标识	省份	城市	区县	备注
202020001	贵州省贵阳市南明区沙冲南路...	贵州贵阳南明	本省本市	贵州省	贵阳市	南明	
202020018	西河镇新四村11组32号	外省重庆市	外省				通过搜索补全：实际归属为重庆市铜梁区西河镇
```

### 输出格式（CSV）
包含以下列：id, 原地址, 分类结果, 大类标识, 省份, 城市, 区县, 是否完整, 备注

## 项目结构

```
address_classifier_skills/
├── src/
│   └── address_classifier.py    # 核心分类器代码
├── config/
│   └── config.yaml              # 配置文件
├── examples/
│   └── sample_data.txt          # 示例数据
├── requirements.txt             # 依赖列表
└── README.md                    # 本文件
```

## 扩展与定制

### 添加新的搜索补全规则

在 `config.yaml` 的 `search_completion.mappings` 中添加：

```yaml
search_completion:
  mappings:
    新的关键字: ["完整归属", "输出分类"]
    示例镇示例村: ["江苏省苏州市昆山市示例镇", "外省江苏省"]
```

### 修改目标城市

在 `config.yaml` 的 `target_region` 中修改：

```yaml
target_region:
  province: "广东省"
  city: "深圳市"
  city_short: "深圳"
  counties:
    龙华区: "龙华"
```

### 添加新的省内城市

在 `config.yaml` 的 `province_cities` 中添加新的市州及其下辖县区。

## 日志与调试

日志级别可在配置中设置：
- `DEBUG`: 输出详细调试信息
- `INFO`: 输出处理统计信息（默认）
- `WARNING`: 仅输出警告和错误
- `ERROR`: 仅输出错误

## 许可证

MIT License
