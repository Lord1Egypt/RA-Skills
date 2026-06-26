---
name: sensors-analytics-doc-gen
description: "将神策（Sensors Analytics）分析手册转换为XX平台飞书使用说明文档。支持事件分析、留存分析、漏斗分析、分布分析、LTV分析、概览，元事件、用户分群、元数据管理等功能模块。自动按照标准文档框架生成，生成前让用户确认框架规范。触发词：生成使用说明、创建手册、文档生成，神策手册。"
---

# 神策分析手册转飞书文档生成器

将神策（Sensors Analytics）官方分析手册转换为XX平台飞书使用说明文档。

## 功能说明

根据用户提供的神策分析手册链接，自动抓取官方文档内容，并按照标准化的文档框架生成飞书文档。

### 支持的分析模块

| 模块 | 标签 | 说明 |
|------|------|------|
| 事件分析 | analysis | 用户行为事件分析 |
| 留存分析 | analysis | 用户留存数据分析 |
| 漏斗分析 | analysis | 转化漏斗分析 |
| 分布分析 | analysis | 用户行为分布分析 |
| LTV分析 | analysis | 用户生命周期价值分析 |
| 概览 | panel | 数据看板管理 |
| 元事件 | metadata | 元事件配置管理 |
| 用户分群 | audience | 用户群体划分 |
| 元数据管理 | metadata | 元事件、事件属性、虚拟属性、虚拟事件、维度表、物品属性 |

### 元数据管理包含功能

元数据管理是一个综合模块，一次性处理时包含以下6个功能：

| 功能 | 说明 |
|------|------|
| 元事件 | 业务含义的事件定义与管理 |
| 事件属性 | 事件相关属性的配置 |
| 虚拟属性 | 基于规则计算的派生属性 |
| 虚拟事件 | 组合多个事件的复合事件 |
| 维度表 | 外部数据关联与维度管理 |
| 物品属性 | 商品/物品相关属性配置 |

---

## 交互流程

### Step 1: 用户输入手册链接

用户需要提供神策分析手册的链接，格式如：
- `https://manual.sensorsdata.cn/sa/docs/guide_analytics_event`
- `https://manual.sensorsdata.cn/sa/docs/guide_analytics_retention`
- `https://manual.sensorsdata.cn/sa/docs/guide_analytics_funnel`
- `https://manual.sensorsdata.cn/sa/docs/guide_analytics_addiction`
- `https://manual.sensorsdata.cn/sa/docs/ltv/v0205`
- `https://manual.sensorsdata.cn/sa/docs/guide_pannel/v0205`
- `https://manual.sensorsdata.cn/sa/docs/guide_metadata_meta/v0205`
- `https://manual.sensorsdata.cn/sa/docs/User_Group_Create/v0205`

**元数据管理模块**：
用户可能一次性提供多个手册链接，需要整合处理。常见链接：
- `https://manual.sensorsdata.cn/sa/docs/guide_metadata_meta/v0205` (元事件)
- `https://manual.sensorsdata.cn/sa/docs/guide_metadata_event_property/v0205` (事件属性)
- `https://manual.sensorsdata.cn/sa/docs/guide_metadata_virtual_property/v0205` (虚拟属性)
- `https://manual.sensorsdata.cn/sa/docs/guide_metadata_virtual_event/v0205` (虚拟事件)
- `https://manual.sensorsdata.cn/sa/docs/guide_metadata_dimension/v0205` (维度表)
- `https://manual.sensorsdata.cn/sa/docs/guide_metadata_item_property/v0205` (物品属性)

### Step 2: 显示标准框架规范

在生成文档之前，必须先向用户展示标准框架规范，确认是否需要调整。

**标准框架规范：**

#### 一、快速入门（5分钟上手）

（一）准备工作：前置条件与环境准备（预留位置，根据实际场景填充）

（二）定义说明：核心概念解释（用高亮框突出）

（三）实际应用场景：表格化呈现

#### 二、核心功能详解

（一）基础全局功能：表格结构（功能名称、说明、截图），空白表格预留填充

（二）其他功能模块：每个二级目录都包含一个功能，使用表格化呈现，结构如下：

| 功能名称 | 说明 | 截图 |
|----------|------|------|
|          |      |      |
|          |      |      |

#### 三、常见问题解答（FAQ）

- 分类：使用相关、配置相关、数据相关

#### 四、文档维护

- 版本记录、使用建议、意见反馈

**关键注意事项：**
1. 标题格式：统一使用【XX】xxx使用说明
2. 高亮框标准：信息说明light-orange，截图标记light-yellow
3. 截图标记：使用📸 emoji标识
4. 截图提示：高亮块内开头固定语句"截图提示：截图可按需插在表格最后一列"，然后另起一行有序分点罗列截图建议

### Step 3: 确认框架规范

使用 `question()` 向用户确认：

```
question({
  questions: [{
    header: "文档框架确认",
    question: "以下是生成文档的标准框架规范，请确认是否需要调整：\n\n【当前标准】\n一、快速入门：准备工作 → 定义说明 → 实际应用场景\n二、核心功能：以基础全局功能模块（空白表格）开头，每个二级功能使用表格呈现\n三、表格格式：功能名称、说明、截图三列布局\n四、流程图：横向Mermaid流程图（graph LR）\n五、保存操作：统一使用"保存到概览"\n\n请确认：",
    options: [
      { label: "直接按此框架生成 (Recommended)", description: "不调整框架，直接生成文档" },
      { label: "调整框架规范", description: "修改部分框架内容后再生成" }
    ]
  }]
})
```

如果用户选择"调整框架规范"，则收集用户的具体调整需求，然后重新确认。

### Step 4: 抓取文档内容

#### 单模块处理
使用 `web_fetch` 工具获取神策手册内容：

```bash
web_fetch url="<用户提供的链接>" maxChars=50000
```

#### 元数据管理多模块处理
如果用户需要生成元数据管理文档，可能一次性提供多个手册链接。需要：
1. 依次抓取每个链接的内容
2. 整合所有内容
3. 按照元数据管理框架生成统一文档

```bash
# 抓取多个链接
web_fetch url="<链接1>" maxChars=50000
web_fetch url="<链接2>" maxChars=50000
# ... 以此类推
```

### Step 5: 生成飞书文档

使用 `feishu_create_doc` 工具创建文档：

```bash
feishu_create_doc title="【XX】<模块名称>使用说明" markdown="<生成的文档内容>"
```

---

## 文档生成标准

### 标题格式
- 事件分析：【XX】事件分析使用说明
- 留存分析：【XX】留存分析使用说明
- 漏斗分析：【XX】漏斗分析使用说明
- 分布分析：【XX】分布分析使用说明
- LTV分析：【XX】LTV分析使用说明
- 概览：【XX】概览使用说明
- 元事件：【XX】元事件管理使用说明
- 用户分群：【XX】用户分群使用说明
- 元数据管理：【XX】元数据管理使用说明

### 元数据管理文档结构

当处理元数据管理模块时，文档结构如下：

#### 一、快速入门（5分钟上手）

（一）准备工作

（二）定义说明：元事件、事件属性、虚拟属性、虚拟事件、维度表、物品属性的核心概念

（三）实际应用场景：表格化呈现

#### 二、核心功能详解

（一）基础全局功能

（二）元事件：功能名称、说明、截图表格

（三）事件属性：功能名称、说明、截图表格

（四）虚拟属性：功能名称、说明、截图表格

（五）虚拟事件：功能名称、说明、截图表格

（六）维度表：功能名称、说明、截图表格

（七）物品属性：功能名称、说明、截图表格

#### 三、常见问题解答（FAQ）

#### 四、文档维护

### 基础全局功能表格
每个文档的核心功能详解部分必须包含一个预留的空白表格，结构如下：

```
| 功能名称 | 说明 | 截图 |
|----------|------|------|
|          |      |      |
|          |      |      |
|          |      |      |
```

---

## 输出结果

生成文档成功后，向用户返回：
1. ✅ 文档链接
2. ✅ Doc ID
3. ✅ 文档符合的规范说明
4. ✅ 文档结构概览

---

## 常见问题

### Q: 用户提供的链接不是神策官网怎么办？
A: 提示用户需要提供神策官方手册链接，格式为 `https://manual.sensorsdata.cn/sa/docs/...`

### Q: 抓取内容失败怎么办？
A: 可能页面使用了JavaScript渲染，尝试使用其他方式获取内容，或告知用户手动复制文档内容

### Q: 需要生成不在支持列表中的模块怎么办？
A: 可以先接单，然后按照现有框架规范灵活调整生成

### Q: 元数据管理模块需要一次性处理多个手册怎么办？
A: 用户可能会一次性提供6个手册链接，需要依次抓取并整合内容，按照元数据管理统一框架生成一份完整的文档
