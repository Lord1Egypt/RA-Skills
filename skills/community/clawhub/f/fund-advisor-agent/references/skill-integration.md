# 技能集成指南

本文档详细说明如何在 Fund Advisor Agent 中集成和使用各种技能。

## 技能概览

| 技能名称 | 功能描述 | 依赖包 | 使用场景 |
|---------|---------|--------|---------|
| **web-search** | 联网搜索 | coze-coding-dev-sdk | 基金数据查询、市场信息获取 |
| **document-generation** | 文档生成 | coze-coding-dev-sdk | PDF/DOCX/Excel 报告生成 |
| **knowledge** | 知识库 | coze-coding-dev-sdk | 基金投资知识管理 |
| **feishu-message** | 飞书消息 | requests | 投资提醒、预警通知 |

## web-search 技能集成

### 技能特点
- 实时联网搜索
- AI 驱动的摘要生成
- 支持多种搜索类型（网页、图片）
- 自动去重和相关性排序

### 适用场景
1. **基金数据查询**
   - 基金净值、涨跌幅
   - 历史业绩表现
   - 基金经理信息

2. **市场信息获取**
   - 指数估值（市盈率、市净率）
   - 市场温度
   - 行业动态

3. **新闻资讯**
   - 基金相关新闻
   - 市场热点
   - 政策解读

### 集成步骤

#### 1. 安装依赖
```bash
uv add coze-coding-dev-sdk
```

#### 2. 初始化客户端
```python
from coze_coding_dev_sdk import SearchClient
from coze_coding_utils.runtime_ctx.context import new_context

# 标准初始化（推荐）
ctx = new_context(method="fund_search")
client = SearchClient(ctx=ctx)

# 或使用请求上下文（保持链路追踪）
from coze_coding_utils.log.write_log import request_context
ctx = request_context.get() or new_context(method="fund_search")
client = SearchClient(ctx=ctx)
```

#### 3. 调用搜索
```python
# 基础搜索
response = client.web_search(
    query="易方达蓝筹精选 005827 净值",
    count=10
)

# 带摘要的搜索（推荐）
response = client.web_search_with_summary(
    query="沪深300指数 估值 市盈率",
    count=5
)

# 高级搜索
response = client.search(
    query="基金定投 策略",
    search_type="web",
    count=10,
    time_range="1m",  # 最近1个月
    sites="eastmoney.com,fund.eastmoney.com",  # 指定网站
    need_summary=True
)
```

#### 4. 处理响应
```python
# 检查结果
if response.web_items:
    for item in response.web_items:
        print(f"标题: {item.title}")
        print(f"来源: {item.site_name}")
        print(f"摘要: {item.snippet}")
        print(f"链接: {item.url}")
        if item.summary:
            print(f"AI摘要: {item.summary}")

# AI 生成的摘要
if response.summary:
    print(f"综合摘要: {response.summary}")
```

### 最佳实践

1. **查询构造**
   - 使用多个关键词提高准确性
   - 包含"基金"、"净值"等限定词
   - 指定数据来源网站

2. **结果处理**
   - 设置结果数量限制（max_results）
   - 提取关键信息格式化输出
   - 处理空结果情况

3. **错误处理**
   - 网络异常捕获
   - 超时处理
   - 返回友好错误提示

## document-generation 技能集成

### 技能特点
- 支持 Markdown/HTML 转 PDF/DOCX/Excel
- 自动上传 S3，返回下载 URL
- 24小时有效期的预签名链接
- 支持中文字体和复杂格式

### 适用场景
1. **投资报告生成**
   - 个性化配置方案
   - 组合业绩报告
   - 风险评估报告

2. **数据表格导出**
   - 基金配置明细
   - 业绩对比表格
   - 定投计划表

3. **文档存档**
   - 投资决策记录
   - 定期复盘报告
   - 合规文档

### 集成步骤

#### 1. 安装依赖
```bash
uv add coze-coding-dev-sdk
```

#### 2. 初始化客户端
```python
from coze_coding_dev_sdk import DocumentGenerationClient, PDFConfig, DOCXConfig, XLSXConfig

# 完整配置
client = DocumentGenerationClient(
    pdf_config=PDFConfig(page_size="A4"),
    docx_config=DOCXConfig(font_name="Noto Sans CJK SC", font_size=11),
    xlsx_config=XLSXConfig(header_bg_color="4472C4", auto_width=True)
)

# 简化配置
client = DocumentGenerationClient()
```

#### 3. 生成 PDF
```python
# Markdown 转 PDF
markdown_content = """
# 基金配置方案报告

## 一、投资者画像

| 项目 | 内容 |
|------|------|
| 风险等级 | 中低风险 |
| 投资期限 | 3年 |

## 二、配置建议

- 债券基金：70%
- 股票基金：30%
"""

# title 必须是英文！
url = client.create_pdf_from_markdown(markdown_content, "fund_portfolio_report")
print(f"PDF下载链接: {url}")  # 有效期24小时
```

#### 4. 生成 Excel
```python
# 从字典列表生成
data = [
    {"基金类型": "债券基金", "配置比例": "70%", "预期收益": "4%"},
    {"基金类型": "股票基金", "配置比例": "30%", "预期收益": "10%"},
]

url = client.create_xlsx_from_list(data, "fund_allocation", "配置明细")

# 从二维列表生成
data_2d = [
    ["基金名称", "净值", "涨幅"],
    ["易方达蓝筹精选", "1.7699", "-0.55%"],
    ["招商中证白酒", "0.9876", "1.23%"],
]

url = client.create_xlsx_from_2d_list(data_2d, "fund_comparison", "基金对比")
```

### 重要注意事项

#### ❌ 错误用法
```python
# title 包含中文
url = client.create_pdf_from_markdown(content, "基金配置报告")  # 错误！

# title 包含空格
url = client.create_pdf_from_markdown(content, "fund portfolio report")  # 错误！

# title 包含特殊字符
url = client.create_pdf_from_markdown(content, "report@2024")  # 错误！
```

#### ✅ 正确用法
```python
# 使用英文 title
url = client.create_pdf_from_markdown(content, "fund_portfolio_report")

# 使用下划线代替空格
url = client.create_pdf_from_markdown(content, "fund_portfolio_report_2024")

# 添加时间戳确保唯一性
from datetime import datetime
title = f"fund_report_{datetime.now().strftime('%Y%m%d')}"
url = client.create_pdf_from_markdown(content, title)
```

## knowledge 技能集成

### 技能特点
- 向量语义搜索
- 支持文本、URL、对象存储导入
- 可配置相似度阈值
- 自动分块处理

### 适用场景
1. **投资知识库**
   - 基金投资策略
   - 市场分析方法
   - 风险控制技巧

2. **业务规则库**
   - 配置方法论
   - 产品选择标准
   - 合规要求

3. **FAQ 系统**
   - 常见问题解答
   - 投资术语解释
   - 操作指南

### 集成步骤

#### 1. 安装依赖
```bash
uv add coze-coding-dev-sdk
```

#### 2. 初始化客户端
```python
from coze_coding_dev_sdk import KnowledgeClient, Config, KnowledgeDocument, DataSourceType

config = Config()
client = KnowledgeClient(config=config)
```

#### 3. 添加知识
```python
# 添加文本知识
documents = [
    KnowledgeDocument(
        source=DataSourceType.TEXT,
        raw_data="基金定投的核心原理是平均成本法..."
    )
]

response = client.add_documents(
    documents=documents,
    table_name="fund_investment_knowledge"
)

if response.code == 0:
    print(f"成功添加 {len(response.doc_ids)} 个文档")

# 添加 URL 知识
documents = [
    KnowledgeDocument(
        source=DataSourceType.URL,
        url="https://example.com/fund-guide",
        raw_data="基金投资入门指南"
    )
]

response = client.add_documents(
    documents=documents,
    table_name="fund_investment_knowledge"
)
```

#### 4. 搜索知识
```python
# 语义搜索
response = client.search(
    query="如何控制基金投资风险",
    top_k=5,  # 返回5条结果
    min_score=0.5  # 相似度阈值
)

if response.code == 0:
    for chunk in response.chunks:
        print(f"[相似度: {chunk.score:.2f}] {chunk.content}")
else:
    print(f"搜索失败: {response.msg}")
```

### 智能降级策略

当知识库为空时，自动降级到其他数据源：

```python
@tool
def search_fund_knowledge(query: str, top_k: int = 5) -> str:
    try:
        client = _get_knowledge_client()
        response = client.search(query=query, top_k=top_k, min_score=0.5)
        
        if response.code == 0 and response.chunks:
            return _format_knowledge_results(response.chunks)
        else:
            # 降级：使用网络搜索
            return _fallback_to_web_search(query)
            
    except Exception as e:
        # 降级：使用网络搜索
        return _fallback_to_web_search(query)
```

## feishu-message 技能集成

### 技能特点
- Webhook 推送，无需复杂配置
- 支持多种消息类型
- 可 @ 指定用户
- 实时通知

### 适用场景
1. **投资提醒**
   - 定投扣款提醒
   - 止盈止损通知
   - 组合调仓建议

2. **市场预警**
   - 估值极端位置提醒
   - 大幅涨跌预警
   - 行业异动通知

3. **定期报告**
   - 组合月度收益报告
   - 定投执行汇总
   - 市场周报

### 集成步骤

#### 1. 安装依赖
```bash
uv add requests
```

#### 2. 获取 Webhook URL
```python
def get_webhook_url() -> str:
    """获取飞书机器人 webhook URL"""
    from coze_workload_identity import Client
    import json
    
    client = Client()
    credential = client.get_integration_credential("integration-feishu-message")
    webhook_key = json.loads(credential)["webhook_url"]
    return webhook_key
```

#### 3. 发送文本消息
```python
import requests
import json

def send_text_message(text: str) -> dict:
    webhook_url = get_webhook_url()
    
    payload = {
        "msg_type": "text",
        "content": {"text": text}
    }
    
    response = requests.post(webhook_url, json=payload)
    return response.json()

# 发送
result = send_text_message("今日沪深300指数上涨2%，您的组合收益+1.5%")
```

#### 4. 发送富文本消息
```python
def send_rich_text(title: str, content: str) -> dict:
    webhook_url = get_webhook_url()
    
    payload = {
        "msg_type": "post",
        "content": {
            "post": {
                "zh_cn": {
                    "title": title,
                    "content": [
                        [
                            {"tag": "text", "text": content},
                            {"tag": "a", "text": "查看详情", "href": "https://example.com"}
                        ]
                    ]
                }
            }
        }
    }
    
    response = requests.post(webhook_url, json=payload)
    return response.json()
```

#### 5. 发送卡片消息
```python
def send_card(title: str, content: str, actions: list = None) -> dict:
    webhook_url = get_webhook_url()
    
    elements = [{
        "tag": "div",
        "text": {
            "tag": "lark_md",
            "content": content
        }
    }]
    
    if actions:
        elements.append({"tag": "action", "actions": actions})
    
    payload = {
        "msg_type": "interactive",
        "card": {
            "header": {
                "title": {
                    "tag": "plain_text",
                    "content": title
                }
            },
            "elements": elements
        }
    }
    
    response = requests.post(webhook_url, json=payload)
    return response.json()

# 示例
send_card(
    "📈 市场预警",
    "沪深300指数当前估值已进入高估区间（PE>15倍），建议适当减仓权益类资产。",
    actions=[
        {
            "tag": "button",
            "text": {"content": "查看详情", "tag": "plain_text"},
            "type": "primary",
            "url": "https://example.com/market"
        }
    ]
)
```

## 技能组合使用

### 场景：生成投资报告并发送通知

```python
@tool
def generate_and_notify_report(user_id: str, portfolio_data: str) -> str:
    """生成投资报告并发送飞书通知"""
    try:
        # 1. 查询最新数据
        fund_data = query_fund_data("沪深300指数基金")
        market_val = query_market_valuation("沪深300")
        
        # 2. 生成报告
        report_content = f"""
# 投资组合月度报告

## 市场概况
{fund_data}

## 估值分析
{market_val}

## 组合表现
{portfolio_data}
"""
        
        # 3. 生成 PDF
        client = _get_doc_client()
        url = client.create_pdf_from_markdown(report_content, "monthly_report")
        
        # 4. 发送通知
        message = f"""
📊 您的月度投资报告已生成

报告内容：
- 市场概况分析
- 估值水平判断
- 组合表现总结

📥 下载报告：{url}

*报告有效期24小时*
"""
        send_text_message(message)
        
        return f"✅ 报告已生成并发送通知！"
        
    except Exception as e:
        return f"❌ 操作失败: {str(e)}"
```

## 总结

遵循以上技能集成指南，可以确保：
- ✅ 技能调用规范高效
- ✅ 错误处理完善健壮
- ✅ 性能优化合理有效
- ✅ 用户体验流畅友好
- ✅ 代码维护简洁清晰
