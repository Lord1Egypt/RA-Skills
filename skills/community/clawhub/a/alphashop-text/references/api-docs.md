# AlphaShop 文本处理 API 参考文档

Base URL: `https://api.alphashop.cn`

所有接口均为 POST，Content-Type: application/json，Authorization: Bearer JWT token。

---

## 1. 大模型文本翻译

**POST** `/ai.text.translate/1.0` （同步）

| 字段 | 类型 | 必填 | 描述 |
|------|------|------|------|
| sourceLanguage | String | Y | 源语种 ISO code，未知可传 "auto" |
| targetLanguage | String | Y | 目标语种 ISO code |
| sourceTextList | List\<String\> | Y | 待翻译内容列表，不超过50个对象 |

**响应：**

| 字段 | 类型 | 描述 |
|------|------|------|
| detectedLanguage | String | 识别语种 |
| translatedText | List\<String\> | 翻译结果列表 |

---

## 2. 生成商品多语言卖点

**POST** `/ai.text.generateMultiLanguageSellingPoint/1.0` （同步）

| 字段 | 类型 | 必填 | 描述 |
|------|------|------|------|
| productName | String | Y | 商品名称或简短描述，≤500字符 |
| productCategory | String | Y | 商品所属类目 |
| targetLanguage | String | Y | 目标语言代码（见语言代码表） |
| productKeyword | List\<String\> | N | SEO关键词或核心卖点词 |
| itemSpec | String | N | 商品属性（键1: 值1, 键2: 值2） |
| productDescription | String | N | 商品详细描述/卖点信息 |

**响应：**

| 字段 | 类型 | 描述 |
|------|------|------|
| result | List\<String\> | 卖点集合 |

---

## 3. 生成商品多语言标题

**POST** `/ai.text.generateMultiLanguageTitle/1.0` （同步）

| 字段 | 类型 | 必填 | 描述 |
|------|------|------|------|
| productName | String | Y | 商品名称或简短描述，10~500字符 |
| productCategory | String | Y | 商品所属类目 |
| targetLanguage | String | Y | 目标语言代码（见语言代码表） |
| productKeyword | List\<String\> | N | SEO关键词或核心卖点词 |
| itemSpec | String | N | 商品属性 |
| productDescription | String | N | 商品详细描述 |
| generateCounts | Integer | Y | 生成数量 1-6，默认1 |

**响应：**

| 字段 | 类型 | 描述 |
|------|------|------|
| result | List\<String\> | 生成的标题列表 |

### 支持的源语言→目标语言对

中文→英/西/法/葡/韩/日/越/泰/土/印尼/德/意/马来/俄/荷
英语→西/法/葡/韩/日/越/泰/土/印尼/德/意/马来/俄/荷

---

## 语言代码表

| 语言代码 | 语言 | | 语言代码 | 语言 |
|----------|------|-|----------|------|
| ar | 阿拉伯语 | | lv | 拉脱维亚语 |
| bn | 孟加拉语 | | lt | 立陶宛语 |
| bg | 保加利亚语 | | mk | 马其顿语 |
| zh | 中文简体 | | ms | 马来西亚语 |
| zh-tw | 中文繁体 | | pl | 波兰语 |
| hr | 克罗地亚语 | | pt | 葡萄牙语 |
| cs | 捷克语 | | ro | 罗马尼亚语 |
| da | 丹麦语 | | ru | 俄语 |
| nl | 荷兰语 | | sr | 塞尔维亚语 |
| en | 英语 | | si | 僧伽罗语 |
| et | 爱沙尼亚语 | | sk | 斯洛伐克语 |
| fi | 芬兰语 | | sl | 斯洛文尼亚语 |
| fr | 法语 | | es | 西班牙语 |
| de | 德语 | | sv | 瑞典语 |
| el | 希腊语 | | tl | 塔加洛语 |
| he | 希伯来语 | | th | 泰语 |
| hu | 匈牙利语 | | tr | 土耳其语 |
| is | 冰岛语 | | uk | 乌克兰语 |
| id | 印尼语 | | ur | 乌尔都语 |
| it | 意大利语 | | uz | 乌兹别克语 |
| ja | 日语 | | vi | 越南语 |
| kk | 哈萨克语 | | | |
| ko | 韩语 | | | |
