<div align="center">

# 📄 Laiye Agentic Document Processing (ADP)

**ADP (Agentic Document Processing)** is a next-generation platform based on Large Language Models and Vision Language Models, combined with agentic technology, to achieve end-to-end automated document processing.


[English](README.md) | [简体中文](README-CN.md)

</div>

---

## 🚀 About ADP

**Laiye Agentic Document Processing (ADP)** is built on the general understanding capabilities of large models, independent of rules and annotations, with universal understanding capabilities for multi-lingual, multi-modal, and multi-scenario contexts. With agentic autonomous planning and execution, it can understand task objectives, autonomously plan steps, call tools, and complete complex tasks. End-to-end business automation forms a complete loop from document input to business decisions and human-in-the-loop collaboration.

### 💡 Core Capabilities

ADP helps AI agents **understand and extract document data just like humans**, but with broader language support and higher accuracy. Whether processing invoices, extracting order details, or parsing receipts, ADP transforms messy unstructured documents into clean structured JSON that your AI can immediately use.

### 🎯 Target Audience

- **AI Agent Developers** building document processing capabilities
- **Enterprise Teams** automating invoice/receipt/order processing
- **FinTech & Accounting Applications** requiring financial data extraction
- **Logistics & Supply Chain** solutions processing shipping documents
- **RPA Platforms** integrating intelligent document understanding

---

## ✨ Core Features

### 📦 Out-of-the-Box Products

| Product | What It Extracts | Best For |
|---------|------------------|----------|
| **Invoice Processing** | Invoice number, date, vendor, line items, totals, tax | AP automation, expense management |
| **Order Processing** | PO number, items, quantities, prices, delivery info | Procurement, e-commerce integration |
| **Receipt Processing** | Merchant, date, amount, category, line items | Expense tracking, reimbursement |

### 🛠️ Technical Capabilities

- **10+ File Formats**: Supports PDF, PNG, JPG, JPEG, BMP, TIFF, DOC, DOCX, XLS, XLSX
- **Confidence Scoring**: Each field includes a 0-1 confidence score for quality validation
- **Sync & Async Modes**: All features exposed via both synchronous and asynchronous APIs
- **VLM + LLM Dual Engine**: Vision understanding + semantic extraction for maximum accuracy
- **Table Recognition**: Automatically extract complex tables and line items
- **Zero Configuration**: Professional models pre-trained on massive enterprise datasets
- **Enterprise Solutions**: We offer private deployment licensing for enterprise customers. For trials, contact: global_product@laiye.com

---

## 🌟 Product Advantages

### ✅ Production-Grade Accuracy
Achieves accuracy >91% for out-of-the-box overseas invoices, receipts, and order documents.

### ⚡ Zero Configuration
No template setup or training required. **ADP delivers truly out-of-the-box functionality for overseas invoices/receipts and order scenarios.**

### 🎯 Agentic-Friendly
ADP is built specifically for AI agent workflows. Structured JSON responses, confidence scoring, and error handling are designed for LLM consumption and decision-making.

### 🔒 Enterprise Security
- HTTPS encryption for transmission and storage
- Tenant-isolated processing environments
- Credential rotation support
- Clear data retention policies

### 🚀 Differential Highlights

| Feature | Generic OCR | ADP |
|---------|-------------|-----|
| Table Extraction | ❌ Struggles with complex tables | ✅ Advanced multi-table recognition |
| Confidence Scoring | ❌ Not available | ✅ Per-field confidence (0-1) |
| Semantic Understanding | ❌ Text-only | ✅ VLM + LLM for context |
| Zero Config | ❌ Requires templates | ✅ Works out of the box |
| Async Processing | ❌ Sync only | ✅ Built-in task queue |

---

## 🛠️ Supported Platforms

ADP Skill can be installed on any AI agent platform that supports custom skills:

- ✅ **Claude Code**
- ✅ **Manus**
- ✅ **Openclaw**
- ✅ **Coze**
- ✅ Any other OpenAI-compatible agent platform

---

## 📦 Installation

### Manual Installation (All Platforms)

1. **Download the Skill package**
   ```bash
   git clone https://github.com/laiye-ai-repos/adp-skill
   # Or download the ZIP from Releases
   ```

2. **Upload to Your Platform**
   - Navigate to your agent platform's Skills/Plugins marketplace
   - Select "Upload Custom Skill" or "Import from File"
   - Choose the `ADP Skill` folder or `SKILL.md` file

3. **Configure Credentials**
   ```bash
   # Get your API keys from: https://adp-global.laiye.com/?utm_source=github
   export ADP_ACCESS_KEY="your_access_key_here"
   export ADP_APP_KEY="your_app_key_here"
   export ADP_APP_SECRET="your_app_secret_here"
   ```

---

## 🎯 Quick Start

### Extract Data from an Invoice

```bash
curl -X POST "https://adp-global.laiye.com/open/agentic_doc_processor/laiye/v1/app/doc/extract" \
  -H "Content-Type: application/json" \
  -H "X-Access-Key: $ADP_ACCESS_KEY" \
  -H "X-Timestamp: $(date +%s)" \
  -H "X-Signature: $(uuidgen)" \
  -d '{
    "app_key": "'"$ADP_APP_KEY"'",
    "app_secret": "'"$ADP_APP_SECRET"'",
    "file_url": "https://example.com/invoice.pdf"
  }'
```

**Response Example:**
```json
{
  "status": "success",
  "extraction_result": [
    {
      "field_key": "invoice_number",
      "field_value": "INV-2024-001",
      "field_type": "text",
      "confidence": 0.95,
      "source_pages": [1]
    },
    {
      "field_key": "total_amount",
      "field_value": "1000.00",
      "field_type": "number",
      "confidence": 0.98,
      "source_pages": [1]
    }
  ]
}
```

---

## 📁 Project Structure

```
laiye-doc-processing/
├── README.md
├── README-CN.md
├── SKILL.md
├── package.json
└── _meta.json
```

### File Descriptions

| File | Purpose |
|------|---------|
| `README.md` | English: Product introduction, use cases, configuration guide |
| `README-CN.md` | Chinese: Product introduction, use cases, configuration guide |
| `SKILL.md` | ADP skill definition: Used by agent platforms to load the skill |
| `package.json` | Package metadata, keywords, required environment variables, API endpoints |
| `_meta.json` | Skill publication and version tracking internal metadata |

---

## 📋 Credential Setup

### Required Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `ADP_ACCESS_KEY` | Tenant-level access key | `c114c8*******63e358400` |
| `ADP_APP_KEY` | Application access key | `UbCdDJ5*******kYoAVqHB` |
| `ADP_APP_SECRET` | Application secret key | `wbGLBuL*******m4L90T8u` |

### Getting Your Credentials

1. Visit [ADP Portal](https://adp-global.laiye.com/?utm_source=github)
2. Register for a new account (100 free credits/month for new users)
3. Use out-of-the-box application API directly, or create a new custom application to get `APP_KEY`, `APP_SECRET`, and `ACCESS_KEY`

---

## 💰 Pricing

| Processing Stage | Cost |
|-----------------|------|
| Document Parsing | 0.5 credits/page |
| Purchase Order Extraction | 1.5 credits/page |
| Invoice/Receipt Extraction | 1.5 credits/page |
| Custom Extraction | 1 credit/page |

**New Users:** 100 free credits per month, no application restrictions.

---

## 🔐 Security & Privacy

### Data Handling

- **Encryption:** HTTPS encryption for transmission and storage
- **Processing:** Documents processed in isolated tenant environments
- **Retention:** Configurable data retention policies
- **Compliance:** Built following enterprise security standards

### Best Practices

```bash
# 1. Use environment variables (never hardcode credentials)
export ADP_ACCESS_KEY="your_key"
export ADP_APP_KEY="your_key"
export ADP_APP_SECRET="your_key"

# 2. Set restrictive file permissions
chmod 600 ~/.openclaw/openclaw.json

# 3. Rotate credentials regularly
# Recommended: Every 90 days

# 4. Never commit credentials to git
echo "*.env" >> .gitignore
echo "openclaw.json" >> .gitignore
```

---

## 📚 Related Documentation

- **API Reference:** [Complete API Documentation](https://laiye-tech.feishu.cn/wiki/S1t2wYR04ivndKkMDxxcp2SFnKd)


---

## 📜 License

**Commercial License Required**

This skill requires a commercial license for use. New users receive 100 free credits monthly to evaluate the service.

To purchase more credits, you can top up directly within the product. If you encounter payment issues, please contact:
- Email: global_product@laiye.com

---

## 📞 Support & Contact

- **ADP Product Manual:** [ADP Product Manual (SaaS)](https://laiye-tech.feishu.cn/wiki/OfexwgVUQiOpEek4kO7c7NEJnAe)
- **ADP API Documentation:** [Open API User Guide](https://laiye-tech.feishu.cn/wiki/S1t2wYR04ivndKkMDxxcp2SFnKd)
- **Issue Tracker:** [GitHub Issues](https://github.com/laiye-ai-repos/adp-skill/issues)
- **Email:** global_product@laiye.com
- **Website:** [Laiye Technology](https://laiye.com)

---

<div align="center">

**Built with ❤️ for the Agentic AI Future**

[⬆ Back to Top](#-laiye-agentic-document-processing-adp)

</div>
