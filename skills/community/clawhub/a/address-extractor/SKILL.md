---
name: address-extractor
# 地址提取和标准化技能

description: 
  此技能应用于从任意文本中提取、清洗、标准化地址信息，并将其转换为结构化的省-市-区/县-乡镇/街道-村庄/社区-道路号POI格式。技能能够智能过滤特殊字符和无效备注文本，尽可能提取楼栋号和门牌号以实现精确定位，并通过高德地图API将标准化地址转换为精确的经纬度坐标。适用于文档处理、客户信息管理、物流配送、地理信息系统等需要从非结构化文本中获取准确位置信息的场景。
---

# 地址提取和标准化技能使用指南

## 技能概述

此技能提供完整的地址信息处理工作流程，将杂乱的文本地址转换为结构化的地理位置信息。技能集成了文本清洗、地址解析、层级标准化、精确位置提取和坐标转换等功能。

## 何时使用此技能

当遇到以下情况时应当使用此技能：
- 从客户资料、订单信息、文档记录中提取地址信息
- 需要处理包含地址的自然语言文本并转换为标准格式
- 需要将文本地址转换为GPS坐标以进行地图标注或导航
- 清理和标准化来自多个来源的地址数据
- 提取文本中的精确位置信息（包括楼栋号、门牌号）
- 过滤掉地址文本中的干扰信息（电话、备注、联系方式等）

## 如何使用此技能

### 基本使用流程

1. **准备输入文本**：收集包含地址信息的原始文本
2. **调用地址提取器**：使用`AddressExtractor`类处理文本
3. **获取处理结果**：接收包含清洗文本、地址组件、标准化地址和坐标的完整结果
4. **后续处理**：根据需要使用标准化地址或坐标信息

### 核心组件使用

#### 1. 初始化地址提取器

```python
from scripts.address_parser import AddressExtractor

# 初始化提取器（推荐配置API密钥）
extractor = AddressExtractor(amap_api_key="your-amap-api-key")

# 如不配置API密钥，仍可提取和标准化地址，但无法获取坐标
extractor_no_api = AddressExtractor()
```

#### 2. 执行完整地址提取流程

```python
# 输入包含地址的文本
text = "客户张三，电话13800138000，地址：北京市朝阳区建国门外大街1号国贸大厦A座1208室"

# 执行提取和标准化
result = extractor.extract_and_standardize(text)

# 检查结果
if result['success']:
    print(f"标准化地址: {result['standardized_address']}")
    print(f"坐标: {result['coordinates']}")
else:
    print(f"错误: {result['error']}")
```

#### 3. 单独使用各功能模块

**文本清洗：**
```python
cleaned = extractor.clean_text(raw_text)
```

**地址组件提取：**
```python
components = extractor.extract_address_components(cleaned_text)
```

**地址标准化：**
```python
standardized = extractor.standardize_address(components)
```

**坐标获取：**
```python
coordinates = extractor.get_coordinates_from_amap(query_address)
```

### 结果格式说明

技能返回一个包含以下字段的字典：

- `success`: 布尔值，表示处理是否成功
- `original_text`: 原始输入文本
- `cleaned_text`: 清洗后的文本
- `components`: 地址组件字典，包含：
  - `province`: 省份
  - `city`: 城市  
  - `district`: 区县
  - `town`: 乡镇街道
  - `village`: 村庄社区
  - `road`: 道路
  - `house_number`: 门牌号
  - `building`: 楼栋号
  - `poi`: 兴趣点
- `standardized_address`: 标准化的地址路径
- `query_address`: 用于API查询的地址字符串
- `coordinates`: 坐标信息（如可用）
  - `lng`: 经度
  - `lat`: 纬度
  - `formatted_address`: 格式化地址

### 高德地图API配置

要获取精确坐标，需要配置高德地图API密钥：

1. 访问[高德开放平台](https://lbs.amap.com/)注册账号
2. 创建应用并获取API Key
3. 在初始化时传入密钥：`AddressExtractor(amap_api_key="your-key")`

API密钥将用于调用高德地理编码API：`https://restapi.amap.com/v3/geocode/geo`

### 支持的地址格式

技能支持多种中文地址表达格式：
- 标准行政区划地址：省-市-区-街道-门牌号
- 商业建筑地址：大厦、广场、中心等POI名称
- 住宅小区地址：小区、花园、苑等居住区名称
- 混合格式：包含道路、楼栋、单元等详细信息

### 地址层级识别

技能按以下优先级识别和提取地址层级：
1. **省份**：直辖市、自治区、特别行政区
2. **城市**：地级市、副省级城市、直辖市
3. **区县**：市辖区、县、县级市、自治县
4. **乡镇街道**：镇、乡、街道办事处
5. **村庄社区**：村、社区、居委会
6. **道路**：路、街、大道、胡同、巷、弄
7. **门牌号**：数字+号、带中文描述的门牌
8. **楼栋号**：栋、号楼、幢、座、单元
9. **POI**：商业建筑、公共设施、地标建筑

### 文本清洗规则

自动过滤以下内容：
- 特殊符号：【】()（）[]{}<>《》""''「」『』等
- 无效备注：备注、说明、注意、联系、电话、手机等开头的描述
- 多余空白字符和标点符号
- 个人敏感信息：姓名、年龄、性别等非地址信息

### 错误处理

技能具备完善的错误处理机制：
- 无有效地址时的友好提示
- API调用失败的异常处理
- 网络请求的超时控制
- 编码问题的自动处理

## 最佳实践

1. **预处理**：尽量提供完整、清晰的地址文本
2. **API配置**：生产环境务必配置有效的高德API密钥
3. **结果验证**：对重要应用建议验证坐标结果的准确性
4. **批量处理**：可循环调用处理多条地址信息
5. **日志记录**：利用内置日志功能追踪处理过程

## 扩展和定制

可通过修改`address_parser.py`中的正则表达式模式来适配特定的地址格式需求。脚本支持灵活的组件扩展和定制化配置。