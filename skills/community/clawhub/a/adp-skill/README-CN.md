<div align="center">

# 📄 来也智能体文档处理 (ADP)

**ADP（Agentic Document Processing，智能体文档处理）** 是基于大语言模型和视觉语言模型，结合智能体技术，实现文档端到端自动化处理的新一代平台。


[English](README.md) | [简体中文](README-CN.md)

</div>

---

## 🚀 关于 ADP

**来也智能体文档处理 (Agentic Document Processing，简称 ADP)** 基于大模型的通用理解能力，不依赖规则与标注，具备对多语言、多模态、多场景的通用理解能力；智能体的自主规划与执行，能够理解任务目标、自主规划步骤、调用工具、完成复杂任务；端到端的业务自动化，从文档输入到业务决策再到人机协同，形成完整闭环。

### 💡 核心功能

ADP 帮助 AI 智能体**像人类一样理解和提取文档数据**，但支持的语言更多、准确率更高。无论是处理发票、提取订单详情，还是解析收据，ADP 都能将杂乱的非结构化文档转化为干净的结构化 JSON，让您的 AI 立即投入使用。

### 🎯 适用人群

- **AI 智能体开发者** 构建文档处理能力
- **企业团队** 自动化发票/收据/订单处理
- **金融科技与财务应用** 需要财务数据提取
- **物流与供应链** 解决方案处理运输单据
- **RPA 平台** 集成智能文档理解

---

## ✨ 核心特性

### 📦 开箱即用产品

| 产品 | 提取内容 | 最佳场景 |
|---------|------------------|----------|
| **发票处理** | 发票号码、日期、供应商、明细项目、总额、税费 | 应付账款自动化、费用管理 |
| **订单处理** | 采购单号、商品、数量、价格、交付信息 | 采购自动化、电商集成 |
| **收据处理** | 商户、日期、金额、类别、明细项目 | 费用追踪、报销管理 |

### 🛠️ 技术能力

- **10+ 种文件格式** ： 支持 PDF、PNG、JPG、JPEG、BMP、TIFF、DOC、DOCX、XLS、XLSX
- **置信度评分** ： 每个字段包含 0-1 置信度评分，便于质量验证
- **同步与异步模式** ： 所有功能均对外开放同步、异步 API
- **VLM + LLM 双引擎** ： 视觉理解 + 语义提取，实现最大准确率
- **表格识别** ： 自动提取复杂表格和明细项目
- **零配置** ： 基于海量企业数据集预训练的专业模型
- **企业级方案** ： 我们为企业级客户提供私有化部署授权，如需试用，可联系邮箱：global_product@laiye.com

---

## 🌟 产品优势

### ✅ 生产级准确率
针对开箱即用的海外发票、收据、订单类型的文档，能实现准确率＞91%。

### ⚡ 零配置
无需模板设置、无需训练。**ADP 实现了海外发票/收据、订单场景下真正意义上的开箱即用。** 

### 🎯 智能体友好
ADP 专为 AI 智能体工作流而构建。结构化 JSON 响应、置信度评分和错误处理，专为 LLM 消费和决策而设计。

### 🔒 企业级安全
- 传输和存储的 HTTPS 加密
- 租户隔离处理环境
- 支持凭证轮换
- 明确的数据保留策略

### 🚀 差异化亮点

| 功能 | 通用 OCR | ADP |
|---------|-------------|-----|
| 表格提取 | ❌ 难以处理复杂表格 | ✅ 高级多表格识别 |
| 置信度评分 | ❌ 不支持 | ✅ 每字段置信度 (0-1) |
| 语义理解 | ❌ 仅文本 | ✅ VLM + LLM 上下文理解 |
| 零配置 | ❌ 需要模板 | ✅ 开箱即用 |
| 异步处理 | ❌ 仅同步 | ✅ 内置任务队列 |

---

## 🛠️ 支持平台

ADP Skill 可安装在任何支持自定义技能的 AI 智能体平台：

- ✅ **Claude Code** 
- ✅ **Manus** 
- ✅ **Openclaw**
- ✅ **Coze**
- ✅ 其他任何兼容 OpenAI 的智能体平台

---

## 📦 安装方式

### 手动安装（所有平台）

1. **下载 Skill 包**
   ```bash
   git clone https://github.com/laiye-ai-repos/adp-skill
   # 或从 Releases 页面下载 ZIP 压缩包
   ```

2. **上传到您的平台**
   - 导航到您智能体平台的技能/插件市场
   - 选择"上传自定义技能"或"从文件导入"
   - 选择 `ADP Skill` 文件夹或 `SKILL.md` 文件

3. **配置凭证**
   ```bash
   # 从以下地址获取您的 API 密钥：https://adp.laiye.com/?utm_source=github
   export ADP_ACCESS_KEY="your_access_key_here"
   export ADP_APP_KEY="your_app_key_here"
   export ADP_APP_SECRET="your_app_secret_here"
   ```

---

## 🎯 快速开始

### 从发票提取数据

```bash
curl -X POST "https://adp.laiye.com/open/agentic_doc_processor/laiye/v1/app/doc/extract" \
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

**响应示例：**
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

## 📁 项目文件结构

```
laiye-doc-processing/
├── README.md
├── README-CN.md
├── SKILL.md
├── package.json
└── _meta.json
```

### 文件说明

| 文件 | 用途 |
|------|---------|
| `README.md` | 英文版：产品介绍、使用场景介绍、配置说明 |
| `README-CN.md` | 中文版：产品介绍、使用场景介绍、配置说明 |
| `SKILL.md` | ADP 技能定义：智能体平台用于加载技能 |
| `package.json` | 包元数据、关键词、必需环境变量、API 端点 |
| `_meta.json` | Skill 发布和版本追踪的内部元数据 |

---

## 📋 凭证设置

### 必需环境变量

| 变量 | 说明 | 示例 |
|----------|-------------|---------|
| `ADP_ACCESS_KEY` | 租户级访问密钥 | `c114c8*******63e358400` |
| `ADP_APP_KEY` | 应用访问密钥 | `UbCdDJ5*******kYoAVqHB` |
| `ADP_APP_SECRET` | 应用安全密钥 | `wbGLBuL*******m4L90T8u` |

### 获取凭证

1. 访问 [ADP 门户](https://adp.laiye.com/?utm_source=github)
2. 注册新账户（新用户每月 100 免费积分）
3. 直接使用开箱即用应用 API，或者创建新自定义应用获取 `APP_KEY` 和 `APP_SECRET`、`ACCESS_KEY`

---

## 💰 计费

| 处理阶段 | 费用 |
|-----------------|------|
| 文档解析 | 0.5 积分/页 |
| 采购订单抽取 | 1.5 积分/页 |
| 发票/收据抽取 | 1.5 积分/页 |
| 自定义抽取 | 1 积分/页 |

**新用户：** 每月获得 100 免费积分，不限制使用应用

---

## 🔐 安全与隐私

### 数据处理

- **加密：** 传输和存储均采用 HTTPS 加密
- **处理：** 文档在隔离的租户环境中处理
- **保留：** 可配置的数据保留策略
- **合规：** 遵循企业安全标准构建

### 最佳实践

```bash
# 1. 使用环境变量（绝不硬编码凭证）
export ADP_ACCESS_KEY="your_key"
export ADP_APP_KEY="your_key"
export ADP_APP_SECRET="your_key"

# 2. 设置限制性文件权限
chmod 600 ~/.openclaw/openclaw.json

# 3. 定期轮换凭证
# 建议：每 90 天一次

# 4. 永远不要将凭证提交到 git
echo "*.env" >> .gitignore
echo "openclaw.json" >> .gitignore
```

---

## 📚 相关文档

- **API 参考：** [完整 API 文档](https://adp.laiye.com/docs)
- **流程索引：** [ADP 流程文档](https://github.com/your-repo/docs)
- **示例代码：** [示例代码与集成](https://github.com/your-repo/examples)

---

## 📜 授权许可

**需要商业许可证**

本技能的使用需要商业许可证。新用户每月可获得 100 免费积分以评估服务。

如需购买更多积分，可直接在产品端内进行积分充值，如支付遇到问题，可以联系邮箱
- 邮箱：global_product@laiye.com

---

## 📞 支持与联系

- **ADP 产品操作手册：** [公有云操作手册](https://laiye-tech.feishu.cn/wiki/UDYIwG42pisBbFkJI39ctpeKnWh)
- **ADP API 接口文档：** [Open API 使用指南](https://laiye-tech.feishu.cn/wiki/PO9Jw4cH3iV2ThkMPW2c539pnkc)

- **问题反馈：** [GitHub Issues](https://github.com/laiye-ai-repos/adp-skill/issues)
- **邮箱：** global_product@laiye.com
- **官网：** [来也科技](https://laiye.com)

---

<div align="center">

**用 ❤️ 构建智能体 AI 的未来**

[⬆ 返回顶部](#-来也智能体文档处理-adp)

</div>
