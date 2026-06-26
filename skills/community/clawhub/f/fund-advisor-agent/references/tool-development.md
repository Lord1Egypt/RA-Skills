# 工具开发规范

本文档详细说明 Fund Advisor Agent 中工具函数的开发规范和最佳实践。

## 工具设计原则

### 1. 单一职责原则
每个工具函数应专注于完成一个特定任务，避免功能过于复杂。

**✅ 正确示例：**
```python
@tool
def query_fund_data(fund_name_or_code: str) -> str:
    """查询基金净值和业绩数据"""
    # 专注于基金数据查询
    pass
```

**❌ 错误示例：**
```python
@tool
def query_fund_and_analyze(fund_name_or_code: str) -> str:
    """查询基金数据并进行分析"""
    # 功能过于复杂，应拆分为两个工具
    pass
```

### 2. 清晰的工具名称
工具名称应清晰表达功能，采用 snake_case 命名法。

**命名规范：**
- 查询类：`query_xxx`
- 分析类：`analyze_xxx`
- 计算类：`calculate_xxx`
- 生成类：`generate_xxx`
- 监控类：`monitor_xxx`
- 管理类：`create_xxx`, `update_xxx`, `delete_xxx`

### 3. 完整的文档字符串
每个工具必须有清晰的文档字符串，包含：
- 功能描述
- 参数说明（Args）
- 返回值说明（Returns）
- 使用示例

**标准模板：**
```python
@tool
def query_fund_data(fund_name_or_code: str) -> str:
    """
    查询指定基金的净值、业绩、排名等实时数据。
    
    基于 web-search 技能，使用 SearchClient 获取基金实时信息。
    
    Args:
        fund_name_or_code: 基金名称或基金代码，如"易方达蓝筹精选"、"005827"
        
    Returns:
        基金的实时数据，包括净值、涨跌幅、业绩排名等信息
        
    Example:
        >>> result = query_fund_data("005827")
        >>> print(result)
    """
    pass
```

## 技能集成规范

### web-search 技能使用

#### 客户端初始化
```python
from coze_coding_dev_sdk import SearchClient
from coze_coding_utils.runtime_ctx.context import new_context

def _get_search_client():
    """获取搜索客户端，优先使用请求上下文"""
    ctx = request_context.get() or new_context(method="fund_data.search")
    return SearchClient(ctx=ctx)
```

#### 标准调用模式
```python
@tool
def query_fund_data(fund_name_or_code: str) -> str:
    try:
        client = _get_search_client()
        
        # 构造搜索查询
        query = f"{fund_name_or_code} 基金净值 业绩 天天基金"
        response = client.web_search_with_summary(query=query, count=10)
        
        # 处理响应
        if response.summary:
            result += f"数据摘要：\n{response.summary}\n\n"
        
        result += "详细信息：\n"
        result += _parse_fund_search_results(response.web_items)
        
        return result
        
    except Exception as e:
        return f"查询基金数据失败: {str(e)}"
```

### document-generation 技能使用

#### 客户端初始化
```python
from coze_coding_dev_sdk import DocumentGenerationClient, PDFConfig, DOCXConfig, XLSXConfig

def _get_doc_client():
    """获取文档生成客户端"""
    return DocumentGenerationClient(
        pdf_config=PDFConfig(page_size="A4"),
        docx_config=DOCXConfig(font_name="Noto Sans CJK SC", font_size=11),
        xlsx_config=XLSXConfig(header_bg_color="4472C4", auto_width=True)
    )
```

#### 生成 PDF 报告
```python
@tool
def generate_portfolio_pdf_report(
    risk_level: str,
    investment_period: str,
    available_funds: str,
    expected_return: str,
    allocation_data: str
) -> str:
    try:
        client = _get_doc_client()
        
        # 生成报告内容（Markdown 格式）
        content = _generate_report_content(...)
        
        # 生成 PDF（title 必须是英文）
        url = client.create_pdf_from_markdown(content, "fund_portfolio_report")
        
        return f"✅ PDF报告已生成！\n\n下载链接：{url}"
        
    except Exception as e:
        return f"生成PDF报告失败: {str(e)}"
```

**重要提示：**
- `title` 参数**必须使用英文**
- 不允许包含空格和特殊字符
- 使用下划线替代空格

### knowledge 技能使用

#### 客户端初始化
```python
from coze_coding_dev_sdk import KnowledgeClient, Config, KnowledgeDocument, DataSourceType

KNOWLEDGE_TABLE_NAME = "fund_investment_knowledge"

def _get_knowledge_client():
    """获取知识库客户端"""
    ctx = request_context.get() or new_context(method="fund_knowledge.search")
    config = Config()
    return KnowledgeClient(config=config, ctx=ctx)
```

#### 搜索知识
```python
@tool
def search_fund_knowledge(query: str, top_k: int = 5) -> str:
    try:
        client = _get_knowledge_client()
        
        response = client.search(
            query=query,
            top_k=top_k,
            min_score=0.5
        )
        
        if response.code != 0:
            return f"知识库搜索失败: {response.msg}"
        
        result = f"【基金投资知识搜索结果】\n\n"
        for idx, chunk in enumerate(response.chunks[:top_k], 1):
            result += f"{idx}. [{chunk.score:.2f}] {chunk.content}\n\n"
        
        return result
        
    except Exception as e:
        return f"搜索知识库失败: {str(e)}"
```

#### 添加知识
```python
@tool
def add_fund_knowledge_text(content: str, knowledge_type: str = "投资策略") -> str:
    try:
        client = _get_knowledge_client()
        
        documents = [
            KnowledgeDocument(
                source=DataSourceType.TEXT,
                raw_data=content
            )
        ]
        
        response = client.add_documents(
            documents=documents,
            table_name=KNOWLEDGE_TABLE_NAME
        )
        
        if response.code == 0:
            return f"✅ 知识添加成功！\n文档ID: {response.doc_ids[0]}"
        else:
            return f"添加知识失败: {response.msg}"
            
    except Exception as e:
        return f"添加知识失败: {str(e)}"
```

### feishu-message 技能使用

#### 获取 Webhook URL
```python
def _get_webhook_url() -> str:
    """获取飞书机器人 webhook URL"""
    try:
        from coze_workload_identity import Client
        client = Client()
        credential = client.get_integration_credential("integration-feishu-message")
        webhook_url = json.loads(credential).get("webhook_url", "")
        return webhook_url
    except Exception:
        return ""
```

#### 发送文本消息
```python
@tool
def send_text_message(text: str) -> str:
    try:
        import requests
        
        webhook_url = _get_webhook_url()
        if not webhook_url:
            return "❌ 飞书 webhook 未配置"
        
        payload = {
            "msg_type": "text",
            "content": {"text": text}
        }
        
        response = requests.post(webhook_url, json=payload, timeout=10)
        
        if response.status_code == 200:
            return "✅ 消息发送成功"
        else:
            return f"❌ 消息发送失败: {response.text}"
            
    except Exception as e:
        return f"❌ 发送消息失败: {str(e)}"
```

## 错误处理规范

### 标准错误处理模式
```python
@tool
def query_fund_data(fund_name_or_code: str) -> str:
    try:
        # 业务逻辑
        client = _get_search_client()
        response = client.web_search_with_summary(...)
        
        # 数据验证
        if not response.web_items:
            return "⚠️ 未找到相关基金数据，请检查输入是否正确"
        
        # 正常返回
        return _format_result(response)
        
    except ConnectionError as e:
        # 网络错误
        return f"🌐 网络连接失败，请检查网络后重试: {str(e)}"
    except TimeoutError as e:
        # 超时错误
        return f"⏱️ 请求超时，请稍后重试: {str(e)}"
    except Exception as e:
        # 未知错误
        return f"❌ 系统错误: {str(e)}"
```

### 错误消息友好化
- 避免暴露技术细节
- 提供重试建议
- 使用表情符号增强可读性

## 性能优化

### 1. 避免重复调用
```python
# ❌ 错误：重复调用
def query_fund_data(fund_code):
    data = _fetch_from_api(fund_code)
    # 做一些处理
    return data

def analyze_fund(fund_code):
    data = query_fund_data(fund_code)  # 重复调用
    # 分析数据
    return analysis
```

```python
# ✅ 正确：复用数据
def analyze_fund(fund_code):
    data = query_fund_data(fund_code)
    # 直接使用数据进行深入分析
    return analysis
```

### 2. 限制返回数据量
```python
def _parse_fund_search_results(web_items, max_results: int = 10) -> str:
    """限制返回结果数量"""
    results = []
    for idx, item in enumerate(web_items[:max_results], 1):
        # 格式化结果
        results.append(f"{idx}. {item.title}")
    return "\n".join(results)
```

### 3. 使用缓存
```python
from functools import lru_cache

@lru_cache(maxsize=100)
def query_market_temperature() -> str:
    """市场温度使用缓存，避免频繁查询"""
    # 查询逻辑
    pass
```

## 测试规范

### 单元测试
```python
import pytest

def test_query_fund_data():
    """测试基金数据查询"""
    result = query_fund_data("005827")
    assert "净值" in result or "Error" in result
    assert "❌" not in result or "失败" in result  # 允许失败，但要有友好提示

def test_search_client_initialization():
    """测试搜索客户端初始化"""
    client = _get_search_client()
    assert client is not None
```

### 集成测试
```python
def test_fund_query_flow():
    """测试完整的基金查询流程"""
    # 1. 查询基金数据
    data_result = query_fund_data("005827")
    assert "净值" in data_result
    
    # 2. 查询基金经理
    manager_result = query_fund_manager("张坤")
    assert "经理" in manager_result or "Error" in manager_result
    
    # 3. 生成报告
    report_result = generate_portfolio_pdf_report(...)
    assert "下载链接" in report_result or "Error" in report_result
```

## 文档维护

### 工具注册
所有工具必须在 `src/agents/agent.py` 中注册：

```python
from tools.fund_data_tool import (
    query_fund_data,
    query_fund_performance,
    query_fund_manager
)

# 在 build_agent 函数中注册
tools = [
    query_fund_data,
    query_fund_performance,
    query_fund_manager,
    # ... 其他工具
]
```

### 配置更新
工具列表必须在 `config/agent_llm_config.json` 中更新：

```json
{
    "tools": [
        "query_fund_data",
        "query_fund_performance",
        "query_fund_manager",
        // 新增工具
    ]
}
```

## 总结

遵循以上规范可以确保：
- ✅ 工具代码清晰易维护
- ✅ 技能调用规范高效
- ✅ 错误处理友好完善
- ✅ 性能优化合理有效
- ✅ 测试覆盖全面可靠
