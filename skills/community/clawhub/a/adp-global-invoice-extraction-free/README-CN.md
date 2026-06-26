<div align="center">

# 🚀 来也 ADP 全球票据智能抽取 · 限时免费开放
由来也科技 ADP 智能文档处理团队重磅出品，面向**全球跨境财务、自动化、系统集成场景**，提供高精度、全版式、多语种的发票、账单、收据智能抽取能力。全面兼容结构化标准票据、非结构化海外采购发票、消费小票、不论是电子 PDF、扫描件、还是图片文件，均可以**一键输出标准化 JSON 结构化数据**，大幅降低财务人力成本，彻底打通业务自动化、智能对账、数据入库全流程。

</div>


## ⭐ 选择 ADP 的核心优势
✅ 全球化票据方案 | 接入简单，多语言识别精准可靠
🌐 支持上百种语言：可识别英语、日语、韩语、德语、法语、泰语等主流语种的发票与收据。
📄 全版式兼容：适配各国标准增值税发票、东南亚税务单据、非结构化收据及混合版式凭证。
🎯 抽取准确率超99%：精准提取关键字段，大幅削减人工核验、翻译与数据录入成本。
⚡ 高速批量处理：数分钟内即可完成上百份文档解析，显著提升工作效率。
🤖 AI 持续优化：模型可基于业务数据不断迭代调优，识别效果愈发精准，并支持个性化适配。

> 来也 ADP 接口**限时免费开放**，名额有限，先到先得！

## 📌 适用场景
| 用户群体 | 使用场景 |
| ---- | ---- |
| 财务团队 | 从多语言发票、海外票据中提取关键数据，用于财务报销与供应商结算等场景。 |
| 智能体用户 | 一键安装 ADP Skill 至国内Coze、Workbuddy、Openclaw、Dify、Manus等主流智能体平台，实现文档自动识别。 |
| 开发者 | 迁移至ADP API接口，抽取准确率达98%以上，5分钟即可开始免费使用。 |

---

## 📄 快速开始

### 步骤 1：选择接口地址
我们为国内外用户提供独立的公有云接入地址，需按区域分别配置。就近接入可保障调用高速稳定，无需注册账号、无需 API 密钥，直接向下方接口地址发起请求即可。

| 环境 | API 接口地址 |
|------|---------|
| **国际版** | `https://adp-global.laiye.com/public/v1/invoice-fast/extract` |
| **国内版** | `https://adp.laiye.com/public/v1/invoice-fast/extract` |

### 步骤 2：发送请求
选择任意一种文件上传方式，发送 `POST` 请求：

#### 方式 1：文件 URL 地址
```bash
curl -X POST "https://adp-global.laiye.com/public/v1/invoice-fast/extract" \
  -H "Content-Type: application/json" \
  -d '{
    "file_url": "shturl.cc/vZd6rD9NxsmfNZPF5KjsnB78s"
  }'

```

#### 方式二：Base64 编码文件内容

```bash
curl -X POST "https://adp-global.laiye.com/public/v1/invoice-fast/extract" \
  -H "Content-Type: application/json" \
  -d '{
    "file_base64": "<base64-encoded-file-content>"
  }'
```

#### Python 请求示例

```python
import base64, requests

with open("invoice.pdf", "rb") as f:
    b64 = base64.b64encode(f.read()).decode()

response = requests.post(
    "https://adp-global.laiye.com/public/v1/invoice-fast/extract",
    json={"file_base64": b64},
    timeout=180,
)
print(response.json())
```

### 3. 获取结果（示例）

| 字段 | 类型 | 说明 |
|------|------|------|
| `success` | 布尔值 | 请求执行状态 |
| `doc_type` | 字符串 | 识别文档类型：`invoice` 发票 / `receipt` 收据 |
| `extraction_result` | 数组 | 结构化抽取字段集合，遵循 ADP 标准接口格式 |
| `aigc` | 对象 | AIGC 内容合规标识，符合国内相关标注规范 |
| `upgrade_message` | 字符串 | 升级引导文案，将根据部署区域自动展示对应语言 |
| `signup_url` | 字符串 | 注册页面链接 |

```json
{
    "success": true,
    "doc_type": "invoice",
    "extraction_result": [
        {
            "field_key": "invoice_number",
            "field_name": "发票号码",
            "field_values": [
                {
                    "field_value": "09071666",
                    "field_confidence": 0.0,
                    "references": [
                        {
                            "search_text": "09071666"
                        }
                    ]
                }
            ]
        },
        {
            "field_key": "invoice_date",
            "field_name": "发票日期",
            "field_values": [
                {
                    "field_value": "2019-11-28",
                    "field_confidence": 0.0,
                    "references": [
                        {
                            "search_text": "2019-11-28"
                        }
                    ]
                }
            ]
        },
        {
            "field_key": "supplier_name",
            "field_name": "供应商名称",
            "field_values": [
                {
                    "field_value": "北京******公司",
                    "field_confidence": 0.0,
                    "references": [
                        {
                            "search_text": "北京******公司"
                        }
                    ]
                }
            ]
        },
        {
            "field_key": "supplier_vat_number",
            "field_name": "供应商增值税号",
            "field_values": [
                {
                    "field_value": "9111******4393T",
                    "field_confidence": 0.0,
                    "references": [
                        {
                            "search_text": "9111******4393T"
                        }
                    ]
                }
            ]
        },
        {
            "field_key": "customer_name",
            "field_name": "客户名称",
            "field_values": [
                {
                    "field_value": "湖南*******公司",
                    "field_confidence": 0.0,
                    "references": [
                        {
                            "search_text": "湖南*******公司"
                        }
                    ]
                }
            ]
        },
        {
            "field_key": "currency",
            "field_name": "币种",
            "field_values": [
                {
                    "field_value": "CNY",
                    "field_confidence": 0.0,
                    "references": [
                        {
                            "search_text": "CNY"
                        }
                    ]
                }
            ]
        },
        {
            "field_key": "total_amount",
            "field_name": "总金额（含税）",
            "field_values": [
                {
                    "field_value": "¥1600.00",
                    "field_confidence": 0.0,
                    "references": [
                        {
                            "search_text": "¥1600.00"
                        }
                    ]
                }
            ]
        },
        {
            "field_key": "line_items",
            "field_name": "商品/服务明细表格",
            "table_values": [
                [
                    {
                        "field_key": "line_items_item_code",
                        "field_name": "项目代码",
                        "field_values": [
                            {
                                "field_value": "",
                                "field_confidence": 0.0,
                                "references": [
                                    {
                                        "search_text": ""
                                    }
                                ]
                            }
                        ]
                    },
                    {
                        "field_key": "line_items_description",
                        "field_name": "描述",
                        "field_values": [
                            {
                                "field_value": "*住宿服务*住宿服务",
                                "field_confidence": 0.0,
                                "references": [
                                    {
                                        "search_text": "*住宿服务*住宿服务"
                                    }
                                ]
                            }
                        ]
                    },
                    {
                        "field_key": "line_items_quantity",
                        "field_name": "数量",
                        "field_values": [
                            {
                                "field_value": "2",
                                "field_confidence": 0.0,
                                "references": [
                                    {
                                        "search_text": "2"
                                    }
                                ]
                            }
                        ]
                    },
                    {
                        "field_key": "line_items_unit_price",
                        "field_name": "单价",
                        "field_values": [
                            {
                                "field_value": "754.716981132",
                                "field_confidence": 0.0,
                                "references": [
                                    {
                                        "search_text": "754.716981132"
                                    }
                                ]
                            }
                        ]
                    },
                    {
                        "field_key": "line_items_total_amount",
                        "field_name": "总金额",
                        "field_values": [
                            {
                                "field_value": "1509.43",
                                "field_confidence": 0.0,
                                "references": [
                                    {
                                        "search_text": "1509.43"
                                    }
                                ]
                            }
                        ]
                    },
                    {
                        "field_key": "line_items_rate",
                        "field_name": "税率",
                        "field_values": [
                            {
                                "field_value": "6%",
                                "field_confidence": 0.0,
                                "references": [
                                    {
                                        "search_text": "6%"
                                    }
                                ]
                            }
                        ]
                    },
                    {
                        "field_key": "line_items_tax",
                        "field_name": "税金",
                        "field_values": [
                            {
                                "field_value": "90.57",
                                "field_confidence": 0.0,
                                "references": [
                                    {
                                        "search_text": "90.57"
                                    }
                                ]
                            }
                        ]
                    }
                ]
            ]
        }
    ],
    "aigc": {
        "Label": "AIGCLabelType.AI_GENERATED",
        "ContentProducer": "001191110108587659081E10001",
        "ProduceID": "e3563f165b4011f19f02d85ed35661fd",
        "ReservedCode1": "34c55657beb0071fecf8abce14b0cdee",
        "ContentPropagator": "001191110108587659081E10001",
        "PropagateID": "e3563f165b4011f19f02d85ed35661fd",
        "ReservedCode2": "34c55657beb0071fecf8abce14b0cdee",
        "ProcessingTypes": [
            "ocr",
            "llm_extract"
        ]
    },
    "upgrade_message": "注册即可获得100积分/月，解锁全部能力，含多层税率计算+识别能力自主进化+更多字段与更高性能",
    "signup_url": "https://adp.laiye.com/"
}
```
## 📄 抽取字段说明

### 普通文本字段
| 字段标识 | 字段名称（示例） | 说明 |
|-----------------------|------------------------|-----------------------------------------------------------------------------|
| `invoice_number`      | 发票编号         | 发票唯一编号 |
| `invoice_date`        | 开票日期         | 发票开具日期 |
| `supplier_name`       | 销方名称         | 开票供应商名称 |
| `supplier_vat_number` | 销方税号         | 供应商增值税登记号 |
| `customer_name`       | 购方名称         | 付款客户名称 |
| `currency`            | 币种             | 发票结算货币代码（例：USD、EUR） |
| `total_amount_inc_tax`| 含税总金额       | 发票含税总金额 |

### 表格明细字段
| 字段标识 | 字段名称（示例） | 说明 |
|-------------------|----------------------|-----------------------------------------------------------------|
| `line_items`        | 商品明细           | 商品/服务明细表格数据 |
| `item_code`         | 商品编码           | 明细商品SKU/编码 |
| `description`       | 商品描述           | 明细商品/服务说明 |
| `quantity`          | 数量               | 商品采购数量 |
| `unit_price`        | 单价               | 商品单件价格 |
| `total_amount`      | 分项金额           | 单条明细合计金额 |
| `tax_rate`          | 税率               | 商品适用税率 |
| `tax_amount`        | 税额               | 单条明细对应税费 |

### 通用字段结构
| 字段 | 类型 | 说明 |
|------|------|------|
| `field_key` | 字符串 | 字段唯一标识 |
| `field_name` | 字符串 | 字段名称 |
| `field_values` | 数组 | 提取结果列表（支持多值） |
| `field_values[].field_confidence` | 浮点数 | 置信度（取值范围 0.0 - 1.0） |
| `field_values[].references` | 数组 | 文档内引用位置（如坐标框、页码） |
| `line_items_item_code` | 字符串 | 明细项编码/库存单位 |
| `line_items_description` | 字符串 | 明细项描述 |
| `line_items_quantity` | 字符串 | 明细项数量 |
| `line_items_unit_price` | 字符串 | 明细项单价 |
| `line_items_total_amount` | 字符串 | 明细项金额合计 |
| `line_items_tax_rate` | 字符串 | 明细项税率 |
| `line_items_tax` | 字符串 | 明细项税额 |

> **字段区分规则**：若返回包含 `table_values`，则为表格字段，读取该数据；否则为普通文本字段，读取 `field_values`。


## ⚠️ 使用限制
| 限制项 | 规则说明 |
|------|---------------------|
| 文件大小 | 不超过 2 MB |
| 文件页数 | 仅支持单页，多页 PDF 将被拒绝 |
| 支持格式 | jpeg、jpg、png、bmp、tiff、pdf、doc、docx、xlsx、ofd |
| URL 权限 | 仅支持公网 HTTP/HTTPS 链接，不允许内网、私有 IP |
| 单IP每分钟 | 30 次（60秒内） |
| 单IP每日 | 30 次（一天） |
| 全局每日限额 | 5000 次 |

超出限制将返回 HTTP `429`，响应中附带注册引导信息。
```json
{
  "code": "rate_limited_day",
  "message": "当日免费额度已用尽，请次日再来。",
  "upgrade_message": "注册账号每月可享100次免费额度，解锁更多字段、更强性能、全税种识别与模型自主优化能力",
  "signup_url": "https://adp-global.laiye.com/?utm_source=promotions-clawhub"
}
```

## ❌ 错误码对照表

| HTTP 状态码 | 错误码 | 说明 |
|-------------|--------|------|
| 400 | `invalid_input` | 未传入文件，或同时传入 `file_base64` 与 `file_url` 两个参数 |
| 400 | `invalid_base64` | `file_base64` 内容非标准 Base64 编码 |
| 400 | `invalid_url` | `file_url` 格式非法，非 HTTP/HTTPS 协议 |
| 400 | `ssrf_blocked` | 目标链接指向内网或私有 IP 地址，已拦截 |
| 400 | `download_failed` | 从远程链接下载文件失败 |
| 400 | `file_too_large` | 文件大小超过 2 MB 限制 |
| 400 | `multi_page` | 检测到多页 PDF，仅支持单页文件 |
| 400 | `unsupported_format` | 上传文件格式暂不支持 |
| 429 | `rate_limited_minute` | 超出单 IP 每分钟调用上限（30 次/分钟） |
| 429 | `rate_limited_day` | 超出单 IP 每日调用上限30 |
| 429 | `rate_limited_global` | 全局每日调用额度5000已耗尽 |
| 500 | `extraction_failed` | 服务端处理异常，请稍后重试 |

## 🚀 进阶能力说明

本接口采用 `invoice-fast` 高速模型及预置字段配置，仅用于快速体验。

**升级至完整版 ADP 账号，即可解锁以下高级能力：**
- 支持处理2MB以上的发票文件
- 更高API调用频次，请求额度不限
- 可自定义提取字段（按需增删）
- 异步批量处理
- 人工介入审核流程（HITL）
- 支持Webhook回调
- 适配更多文档类型（采购单、证件、国内发票等）
- 对接Claude Desktop、Cursor等AI客户端，支持MCP工具集成

新用户注册即送 **100 免费点数**，试用全部完整版功能。国内外用户分设独立公有云接入地址，按地区分开配置，就近接入可实现跨网高速稳定调用。
  - 中国地区 [登录](https://adp.laiye.com/?utm_source=promotions-clawhub)
  - 全球地区 [登录](https://adp-global.laiye.com/?utm_source=promotions-clawhub)


## 📞 支持与联系
- **CLI 使用指南：** [ADP CLI 使用指南](https://laiye-tech.feishu.cn/wiki/Hz3Vw1IQki3YQtk33gLcSdwSndc)
- **API 接口文档：** [Open API 使用指南](https://laiye-tech.feishu.cn/wiki/PO9Jw4cH3iV2ThkMPW2c539pnkc)
- **ADP 产品操作手册：** [公有云操作手册](https://laiye-tech.feishu.cn/wiki/UDYIwG42pisBbFkJI39ctpeKnWh)
- **问题反馈：** [GitHub Issues](https://github.com/laiye-ai-repos/adp-skill/issues)
- **邮箱：** global_product@laiye.com
- **官网：** [来也科技](https://laiye.com)


<div align="center">
[⬆ 返回顶部](#agentic_doc_parse_and_extract)

**用 ❤️ 构建智能体 AI 的未来**
版权所有 © 2026 [来也科技（北京）有限公司] 保留所有权利。

</div>

