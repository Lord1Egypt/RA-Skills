
<div align="center">

# 🚀 Laiye ADP Global Invoice Extraction · Free for Limited Time

Developed by the Laiye ADP (Agentic Document Processing) team, this solution delivers high-precision, full-format and multi-language intelligent extraction for invoices, bills and receipts, tailored for **global cross-border finance, automation and system integration scenarios**. Compatible with standard structured documents and unstructured overseas purchase invoices & receipts, it supports electronic PDFs, scanned files and images. All files can generate **standardized structured JSON data** with one click, effectively cutting financial labor costs and enabling full-process capabilities including business automation, intelligent reconciliation and data entry.

</div>

## ⭐ Why choose ADP?
✅ Global Invoice Solution  
🌐 Supports 100+ languages for invoices & receipts  
📄 Adapts to various invoice, receipt and voucher formats  
🎯 99%+ data extraction accuracy  
⚡ Fast batch processing for high efficiency  
🤖 AI continuously optimized with your business data  

> Laiye ADP APIs are **100% free** for a limited time. Limited quota available, first come, first served!

## 📌 Target Scenarios
| User Group | Usage Scenario |
| ---- | ---- |
| Finance Teams | Extract key data from multi-language invoices & overseas receipts for financial reimbursement and supplier settlement. |
| Agent Users | Install ADP Skill with one click on OpenAI GPTs, Anthropic Claude, Google Gemini Agent Builder, Microsoft Copilot Studio and Hermes for automated document parsing. |
| Developers | Call our APIs with 98%+ extraction accuracy. Migrate to our service in just 5 minutes and get started for free. |

## 📄 Quick Start Guide

### Step 1: Select Base URL
We offer dedicated public cloud access endpoints for domestic and international users, with separate regional configurations. Connecting to the nearest node ensures fast and stable network calls. No account registration or API Key is required — you may send requests directly to the endpoints listed below.  

| Environment | API Endpoint |
|------|---------|
| **Global** | `https://adp-global.laiye.com/public/v1/invoice-fast/extract` |
| **China** | `https://adp.laiye.com/public/v1/invoice-fast/extract` |

### Step 2: Send Request
Choose one file transfer method and send a `POST` request:

#### Method 1: File URL
```bash
curl -X POST "https://adp-global.laiye.com/public/v1/invoice-fast/extract" \
  -H "Content-Type: application/json" \
  -d '{
    "file_url": "shturl.cc/vZd6rD9NxsmfNZPF5KjsnB78s"
  }'
```

#### Method 2: Base64 Encoded File Content
```bash
curl -X POST "https://adp-global.laiye.com/public/v1/invoice-fast/extract" \
  -H "Content-Type: application/json" \
  -d '{
    "file_base64": "<base64-encoded-file-content>"
  }'
```
#### Request Example in Python:
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

### Step 3: Result Example

| Field | Type | Description |
|------|------|------|
| `success` | boolean | Request status |
| `doc_type` | string | Identified document type: `invoice` or `receipt` |
| `extraction_result` | array | List of extracted fields and values |
| `aigc` | object | Metadata about the AIGC processing, including labels, producer info, and processing types |
| `upgrade_message` | string | Message prompting users to register for enhanced features |
| `signup_url` | string | URL for user registration to unlock full features |

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

## 📄 Extraction Field Reference

## Text Fields
| field_key             | field_name (example)   | Description                                                                 |
|-----------------------|------------------------|-----------------------------------------------------------------------------|
| `invoice_number`      | Invoice Number         | Unique identifier of the invoice.                                           |
| `invoice_date`        | Invoice Date           | Date when the invoice was issued.                                           |
| `supplier_name`       | Supplier Name          | Name of the issuing supplier.                                               |
| `supplier_vat_number` | Supplier VAT Number    | VAT registration number of the supplier.                                    |
| `customer_name`       | Customer Name          | Name of the billed customer.                                                |
| `currency`            | Currency               | Currency code of the invoice (e.g., USD, EUR).                              |
| `total_amount_inc_tax`| Total Amount (Inc. Tax)| Total invoice amount including tax.                                         |

## Table Fields
| field_key         | field_name (example) | Description                                                     |
|-------------------|----------------------|-----------------------------------------------------------------|
| `item_code`         | Item Code            | Code/SKU of the line item.                                      |
| `description`       | Description          | Description of the line item.                                   |
| `quantity`          | Quantity             | Quantity of the line item.                                      |
| `unit_price`        | Unit Price           | Unit price of the line item.                                    |
| `total_amount`      | Total Amount         | Total amount of the line item.                                  |
| `tax_rate`          | Tax Rate             | Applicable tax rate for the item (full coverage).               |
| `tax_amount`        | Tax Amount           | Tax amount for the line item (full coverage).                   |

## Common Field Structure
| Field | Type | Description |
|------|------|------|
| `field_key` | string | Field identifier |
| `field_name` | string | Field name |
| `field_values` | array | List of extracted values (supports multiple values) |
| `field_values[].field_confidence` | float | Confidence score (0.0 - 1.0) |
| `field_values[].references` | array | List of reference points in the document (e.g., bounding boxes, page numbers) |
| `line_items_item_code` | string | Code/SKU of the line item |
| `line_items_description` | string | Description of the line item |
| `line_items_quantity` | string | Quantity of the line item |  
| `line_items_unit_price` | string | Unit price of the line item |
| `line_items_total_amount` | string | Total amount of the line item |
| `line_items_tax_rate` | string | Tax rate for the line item |
| `line_items_tax` | string | Tax amount for the line item |


> **How to distinguish field types:** If `table_values` is present → table field, read from `table_values`; otherwise → regular field, read from `field_values`.


## ⚠️ Usage Limits

| Item | Requirement / Limit |
|------|---------------------|
| File Size | Less than 2 MB |
| Page Count | Single page only. Multi-page PDF files will be rejected |
| Supported Formats | jpeg, .jpg, .png, .bmp, .tiff, .pdf, .doc, .docx, .xlsx, .ofd |
| URL Accessibility | Publicly accessible HTTP/HTTPS URL. Private network or internal IP addresses are not supported |
| Per IP per minute | 30 requests (within any consecutive 60 seconds) |
| Per IP per day | 30 requests |
| daily pool | 5,000 requests |

When the limit is exceeded, the API returns HTTP `429` with registration guidance included in the response.  
```json
{
  "code": "rate_limited_day",
  "message": "Daily free usage limit has been used up. Please come back tomorrow.",
  "upgrade_message": "Sign up for 100 monthly free credits, more fields, higher performance, multi-tax support & self-optimization",
  "signup_url": "https://adp-global.laiye.com/?utm_source=promotions-clawhub"
}
```

## ❌ Error Codes
| HTTP Status Code | code | Description |
|-------------|------|------|
| 400 | `invalid_input` | No file provided, or both `file_base64` and `file_url` are passed simultaneously |
| 400 | `invalid_base64` | The content of `file_base64` is not valid Base64 encoding |
| 400 | `invalid_url` | Invalid `file_url` format (not HTTP/HTTPS) |
| 400 | `ssrf_blocked` | `file_url` points to an internal network or private IP address |
| 400 | `download_failed` | Failed to download file from `file_url` |
| 400 | `file_too_large` | File size exceeds 2 MB |
| 400 | `multi_page` | Multi-page PDF detected. Only single-page files are supported |
| 400 | `unsupported_format` | Unsupported file format |
| 429 | `rate_limited_minute` | Exceeded per-IP minute limit (30 requests within 60 seconds) |
| 429 | `rate_limited_day` | Exceeded per-IP daily limit (30 requests) |
| 429 | `rate_limited_global` | Exceeded global daily limit (5,000 requests) |
| 500 | `extraction_failed` | Server processing failed. Please try again later |

## 🚀 Advanced Usage

This API uses the fixed `invoice-fast` (high-speed) model with preset field configurations, designed exclusively for a quick experience.

**Upgrade to the full ADP account to unlock these premium capabilities:**
- Process invoice files larger than 2MB
- Higher API call frequency & unlimited request quotas
- Customizable extraction fields (add or remove fields on demand)
- Asynchronous batch processing
- Human-in-the-loop (HITL) review workflow
- Webhook callback support
- Support for more document types (purchase orders, ID cards, domestic invoices, etc.)
- MCP tool integration for AI clients (Claude Desktop, Cursor, etc.)

New users will receive **100 free credits** upon registration to experience all full-function features.We provide independent Public Cloud access addresses fr domestic and international users, which need to be configured separately by region. Accessing from a nearby location can better ensure high-speed and stable invocation across the network.
  - Users in Chinese Mainland [Log in](https://adp.laiye.com/?utm_source=promotions-clawhub)
  - Users outside Chinese Mainland [Log in](https://adp-global.laiye.com/?utm_source=promotions-clawhub)


## 🛠️ Support & Contact
- **CLI User Guide:** [ADP CLI User Guide](https://laiye-tech.feishu.cn/wiki/YIaawiK2DimisZk5KfDc8a8cnLh)
- **API Documentation:** [Open API User Guide](https://laiye-tech.feishu.cn/wiki/S1t2wYR04ivndKkMDxxcp2SFnKd)
- **ADP Product Manual:** [Public Cloud Manual](https://laiye-tech.feishu.cn/wiki/OfexwgVUQiOpEek4kO7c7NEJnAe)
- **Issue Tracker:** [GitHub Issues](https://github.com/Laiye-ADP/adp-skills/issues)
- **Email:** global_product@laiye.com
- **Website:** [Laiye ADP](https://laiye.com/en/product/adp-platform)


<div align="center">
[⬆ Back to Top](#agentic_doc_parse_and_extract)

**Build the Future of Agentic AI with ❤️**
Copyright © 2026 [Laiye Technology (Beijing) Co., Ltd.] All rights reserved.

</div>
