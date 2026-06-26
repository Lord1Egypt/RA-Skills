# 数据存储方案

本文档详细说明 Fund Advisor Agent 的数据存储架构、策略和最佳实践。

## 存储架构概览

### 存储类型

| 存储类型 | 用途 | 持久性 | 容量 | 适用场景 |
|---------|------|--------|------|---------|
| **内存存储** | 对话历史 | 临时 | 受限 | Agent 短期记忆 |
| **文件系统** | 用户数据 | 持久 | 大 | 配置、计划、日记 |
| **云存储 (S3)** | 报告文件 | 持久 | 无限 | PDF/DOCX/Excel |
| **知识库** | 专业知识 | 持久 | 大 | 投资知识管理 |

### 存储层次

```
┌─────────────────────────────────────────┐
│           用户数据层                      │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐   │
│  │用户画像 │ │投资日记 │ │定投计划 │   │
│  └────┬────┘ └────┬────┘ └────┬────┘   │
│       └───────────┴───────────┘         │
│                 │                       │
│                 ▼                       │
│  ┌─────────────────────────────────┐    │
│  │         文件系统 (/tmp)          │    │
│  │  user_profiles/                 │    │
│  │  investment_diary/              │    │
│  │  sip_plans/                    │    │
│  │  market_alerts/                │    │
│  └─────────────────────────────────┘    │
│                 │                       │
│                 ▼                       │
│  ┌─────────────────────────────────┐    │
│  │       云存储 (S3)                │    │
│  │  reports/                       │    │
│  │  attachments/                   │    │
│  └─────────────────────────────────┘    │
└─────────────────────────────────────────┘
```

## 内存存储 (Memory)

### LangChain MemorySaver

使用 `langgraph.checkpoint.memory.MemorySaver` 存储对话历史。

```python
from langgraph.checkpoint.memory import MemorySaver

# 全局初始化（避免重复创建导致记忆丢失）
_checkpointer = MemorySaver()

def get_memory_saver():
    """获取记忆存储"""
    return _checkpointer
```

### 滑动窗口策略

控制对话历史长度，避免上下文过长。

```python
from typing import Annotated
from langgraph.graph.message import add_messages

MAX_MESSAGES = 40  # 保留最近 20 轮对话 (40 条消息)

class AgentState(MessagesState):
    """Agent 状态"""
    messages: Annotated[list[AnyMessage], _windowed_messages]

def _windowed_messages(old, new):
    """滑动窗口: 只保留最近 MAX_MESSAGES 条消息"""
    return add_messages(old, new)[-MAX_MESSAGES:]
```

### 使用示例

```python
from langchain.agents import create_agent

def build_agent():
    return create_agent(
        model=llm,
        tools=tools,
        checkpointer=get_memory_saver(),  # 启用记忆
        state_schema=AgentState,
    )

# 运行 Agent（自动保存对话历史）
agent = build_agent()

response = agent.invoke({
    "messages": [("user", "我想配置基金组合")]
})

# 再次调用（可以访问之前的对话历史）
response = agent.invoke({
    "messages": [("user", "请继续刚才的配置")]
})
```

## 文件系统存储

### 目录结构

```
/tmp/
├── user_profiles/           # 用户画像数据
│   └── {user_id}.json
├── sip_plans/              # 定投计划
│   └── {user_id}_sip_{plan_id}.json
├── market_alerts/          # 市场预警配置
│   └── {user_id}_alerts.json
├── fund_alerts/            # 基金异动监控
│   └── {user_id}_fund_alerts.json
├── notifications/          # 消息通知配置
│   └── {user_id}_notifications.json
└── investment_diary/       # 投资日记
    └── {user_id}_diary_{date}.json
```

### 基础工具函数

```python
import os
import json
from datetime import datetime

# 数据目录
DATA_DIR = "/tmp"
USER_PROFILES_DIR = os.path.join(DATA_DIR, "user_profiles")
SIP_PLANS_DIR = os.path.join(DATA_DIR, "sip_plans")
INVESTMENT_DIARY_DIR = os.path.join(DATA_DIR, "investment_diary")

def _ensure_dir(dir_path: str):
    """确保目录存在"""
    if not os.path.exists(dir_path):
        os.makedirs(dir_path, exist_ok=True)

def _save_json(file_path: str, data: dict):
    """保存 JSON 数据"""
    _ensure_dir(os.path.dirname(file_path))
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def _load_json(file_path: str) -> dict:
    """加载 JSON 数据"""
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}
```

### 用户画像存储

```python
@tool
def save_user_profile(
    user_id: str,
    risk_level: str,
    investment_period: str,
    available_funds: str,
    expected_return: str
) -> str:
    """
    保存用户投资偏好画像
    
    Args:
        user_id: 用户ID
        risk_level: 风险承受能力
        investment_period: 投资期限
        available_funds: 可用资金
        expected_return: 预期收益
        
    Returns:
        保存结果
    """
    try:
        file_path = os.path.join(USER_PROFILES_DIR, f"{user_id}.json")
        
        profile = {
            "user_id": user_id,
            "risk_level": risk_level,
            "investment_period": investment_period,
            "available_funds": available_funds,
            "expected_return": expected_return,
            "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        _save_json(file_path, profile)
        
        return f"✅ 用户画像已保存\n\n文件路径: {file_path}"
        
    except Exception as e:
        return f"❌ 保存失败: {str(e)}"

@tool
def get_user_profile(user_id: str) -> str:
    """
    获取用户投资偏好画像
    
    Args:
        user_id: 用户ID
        
    Returns:
        用户画像信息
    """
    try:
        file_path = os.path.join(USER_PROFILES_DIR, f"{user_id}.json")
        profile = _load_json(file_path)
        
        if not profile:
            return "⚠️ 未找到用户画像，请先使用 save_user_profile 保存"
        
        return f"""【用户画像】

- 用户ID: {profile.get('user_id', 'N/A')}
- 风险等级: {profile.get('risk_level', 'N/A')}
- 投资期限: {profile.get('investment_period', 'N/A')}
- 可用资金: {profile.get('available_funds', 'N/A')}
- 预期收益: {profile.get('expected_return', 'N/A')}
- 更新时间: {profile.get('updated_at', 'N/A')}
"""
        
    except Exception as e:
        return f"❌ 获取失败: {str(e)}"
```

### 定投计划存储

```python
@tool
def create_sip_plan(
    user_id: str,
    fund_code: str,
    fund_name: str,
    monthly_amount: float,
    investment_period: str,
    start_date: str
) -> str:
    """
    创建定投计划
    
    Args:
        user_id: 用户ID
        fund_code: 基金代码
        fund_name: 基金名称
        monthly_amount: 每月定投金额
        investment_period: 投资期限
        start_date: 开始日期
        
    Returns:
        创建结果
    """
    try:
        plan_id = f"SIP{datetime.now().strftime('%Y%m%d%H%M%S')}"
        file_path = os.path.join(SIP_PLANS_DIR, f"{user_id}_{plan_id}.json")
        
        plan = {
            "plan_id": plan_id,
            "user_id": user_id,
            "fund_code": fund_code,
            "fund_name": fund_name,
            "monthly_amount": monthly_amount,
            "investment_period": investment_period,
            "start_date": start_date,
            "status": "active",
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "executions": []
        }
        
        _save_json(file_path, plan)
        
        return f"""✅ 定投计划创建成功！

计划ID: {plan_id}

📋 计划详情:
- 基金: {fund_name} ({fund_code})
- 每月金额: {monthly_amount}元
- 投资期限: {investment_period}
- 开始日期: {start_date}
- 状态: 运行中
"""
        
    except Exception as e:
        return f"❌ 创建失败: {str(e)}"

@tool
def record_sip_execution(
    user_id: str,
    plan_id: str,
    execution_date: str,
    amount: float,
    nav: float,
    shares: float
) -> str:
    """
    记录定投执行
    
    Args:
        user_id: 用户ID
        plan_id: 计划ID
        execution_date: 执行日期
        amount: 投入金额
        nav: 净值
        shares: 购买份额
        
    Returns:
        记录结果
    """
    try:
        file_path = os.path.join(SIP_PLANS_DIR, f"{user_id}_{plan_id}.json")
        plan = _load_json(file_path)
        
        if not plan:
            return f"❌ 未找到计划: {plan_id}"
        
        # 添加执行记录
        execution = {
            "date": execution_date,
            "amount": amount,
            "nav": nav,
            "shares": shares
        }
        
        plan["executions"].append(execution)
        plan["total_invested"] = plan.get("total_invested", 0) + amount
        plan["total_shares"] = plan.get("total_shares", 0) + shares
        
        _save_json(file_path, plan)
        
        return f"""✅ 定投执行记录已保存

日期: {execution_date}
投入金额: {amount}元
净值: {nav}
购买份额: {shares:.2f}

累计投入: {plan['total_invested']}元
累计份额: {plan['total_shares']:.2f}
"""
        
    except Exception as e:
        return f"❌ 记录失败: {str(e)}"
```

### 投资日记存储

```python
@tool
def create_investment_diary(
    user_id: str,
    title: str,
    content: str,
    mood: str = "平静",
    market_view: str = "中性",
    tags: list = None
) -> str:
    """
    创建投资日记
    
    Args:
        user_id: 用户ID
        title: 日记标题
        content: 日记内容
        mood: 投资心情
        market_view: 市场观点
        tags: 标签列表
        
    Returns:
        创建结果
    """
    try:
        diary_id = f"D{datetime.now().strftime('%Y%m%d%H%M%S')}"
        date_str = datetime.now().strftime("%Y%m%d")
        file_path = os.path.join(INVESTMENT_DIARY_DIR, f"{user_id}_diary_{diary_id}.json")
        
        diary = {
            "diary_id": diary_id,
            "user_id": user_id,
            "title": title,
            "content": content,
            "mood": mood,
            "market_view": market_view,
            "tags": tags or [],
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        _save_json(file_path, diary)
        
        return f"""✅ 投资日记创建成功！

日记ID: {diary_id}

📝 {title}
- 心情: {mood}
- 市场观点: {market_view}
- 标签: {', '.join(tags) if tags else '无'}
- 时间: {diary['created_at']}

内容:
{content}
"""
        
    except Exception as e:
        return f"❌ 创建失败: {str(e)}"

@tool
def get_investment_diary(
    user_id: str,
    date: str = None,
    limit: int = 10
) -> str:
    """
    查询投资日记
    
    Args:
        user_id: 用户ID
        date: 查询日期 (YYYYMMDD)
        limit: 返回数量
        
    Returns:
        日记列表
    """
    try:
        diary_dir = INVESTMENT_DIARY_DIR
        _ensure_dir(diary_dir)
        
        # 获取所有日记文件
        files = [f for f in os.listdir(diary_dir) if f.startswith(f"{user_id}_diary_")]
        files.sort(reverse=True)
        
        # 筛选日期
        if date:
            files = [f for f in files if date in f]
        
        # 限制数量
        files = files[:limit]
        
        if not files:
            return "📝 暂无投资日记记录"
        
        results = []
        for file in files:
            file_path = os.path.join(diary_dir, file)
            diary = _load_json(file_path)
            
            results.append(f"""【{diary['title']}】
- ID: {diary['diary_id']}
- 时间: {diary['created_at']}
- 心情: {diary['mood']}
- 标签: {', '.join(diary['tags']) if diary['tags'] else '无'}
- 内容: {diary['content'][:100]}...
---
""")
        
        return f"📝 共找到 {len(results)} 篇日记\n\n" + "\n".join(results)
        
    except Exception as e:
        return f"❌ 查询失败: {str(e)}"
```

## 云存储 (S3)

### 报告文件存储

使用 document-generation 技能生成报告，自动上传 S3。

```python
from coze_coding_dev_sdk import DocumentGenerationClient

@tool
def generate_portfolio_pdf_report(
    risk_level: str,
    investment_period: str,
    available_funds: str,
    expected_return: str,
    allocation_data: str
) -> str:
    """
    生成基金配置方案 PDF 报告
    
    Args:
        ... (参数说明)
        
    Returns:
        PDF 报告下载链接
    """
    try:
        client = DocumentGenerationClient()
        
        # 生成报告内容
        content = _generate_report_content(...)
        
        # 生成 PDF（自动上传 S3）
        url = client.create_pdf_from_markdown(content, "fund_portfolio_report")
        
        return f"""✅ PDF 报告已生成！

📥 下载链接: {url}

⏰ 链接有效期: 24小时

📋 报告包含:
- 投资者画像分析
- 配置比例建议
- 选基逻辑说明
- 风险控制策略
- 投资建议与提示
"""
        
    except Exception as e:
        return f"❌ 生成失败: {str(e)}"
```

### S3 链接管理

```python
import boto3
from datetime import datetime, timedelta

# S3 客户端
s3_client = boto3.client('s3')

def generate_presigned_url(bucket: str, key: str, expiration: int = 86400) -> str:
    """
    生成预签名 URL
    
    Args:
        bucket: S3 桶名
        key: 文件键
        expiration: 过期时间（秒），默认24小时
        
    Returns:
        预签名 URL
    """
    try:
        url = s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': bucket, 'Key': key},
            ExpiresIn=expiration
        )
        return url
    except Exception as e:
        print(f"生成预签名 URL 失败: {e}")
        return None
```

## 知识库存储

### 知识导入

```python
from coze_coding_dev_sdk import KnowledgeClient, KnowledgeDocument, DataSourceType, ChunkConfig

KNOWLEDGE_TABLE_NAME = "fund_investment_knowledge"

@tool
def add_fund_knowledge_batch(
    knowledge_list: str,
    knowledge_type: str = "投资策略"
) -> str:
    """
    批量添加基金投资知识
    
    Args:
        knowledge_list: 知识列表（JSON 格式）
        knowledge_type: 知识类型
        
    Returns:
        添加结果
    """
    try:
        client = KnowledgeClient()
        
        # 解析知识列表
        import json
        items = json.loads(knowledge_list)
        
        # 构建文档
        documents = [
            KnowledgeDocument(
                source=DataSourceType.TEXT,
                raw_data=item["content"]
            )
            for item in items
        ]
        
        # 分块配置
        chunk_config = ChunkConfig(
            separator="\n\n",
            max_tokens=1000,
            remove_extra_spaces=True
        )
        
        # 导入知识库
        response = client.add_documents(
            documents=documents,
            table_name=KNOWLEDGE_TABLE_NAME,
            chunk_config=chunk_config
        )
        
        if response.code == 0:
            return f"""✅ 批量知识导入成功！

导入数量: {len(items)} 条
文档ID: {response.doc_ids}
知识类型: {knowledge_type}
"""
        else:
            return f"❌ 导入失败: {response.msg}"
            
    except Exception as e:
        return f"❌ 系统错误: {str(e)}"
```

### 知识搜索

```python
@tool
def search_fund_knowledge(
    query: str,
    top_k: int = 5,
    min_score: float = 0.5
) -> str:
    """
    搜索基金投资知识
    
    Args:
        query: 搜索查询
        top_k: 返回结果数量
        min_score: 最低相似度
        
    Returns:
        搜索结果
    """
    try:
        client = KnowledgeClient()
        
        response = client.search(
            query=query,
            top_k=top_k,
            min_score=min_score
        )
        
        if response.code != 0:
            return f"❌ 搜索失败: {response.msg}"
        
        if not response.chunks:
            return "⚠️ 未找到相关知识"
        
        results = []
        for idx, chunk in enumerate(response.chunks, 1):
            score_info = f"[相似度: {chunk.score:.2f}]"
            results.append(f"{idx}. {score_info}\n   {chunk.content}\n")
        
        return f"""【基金投资知识搜索结果】

查询: {query}

{chr(10).join(results)}
"""
        
    except Exception as e:
        return f"❌ 搜索失败: {str(e)}"
```

## 数据安全与合规

### 1. 数据加密
```python
from cryptography.fernet import Fernet

# 生成密钥（实际应从密钥管理服务获取）
key = Fernet.generate_key()
cipher = Fernet(key)

def encrypt_data(data: str) -> str:
    """加密敏感数据"""
    return cipher.encrypt(data.encode()).decode()

def decrypt_data(encrypted_data: str) -> str:
    """解密数据"""
    return cipher.decrypt(encrypted_data.encode()).decode()
```

### 2. 访问控制
```python
import os

def check_file_access(file_path: str, user_id: str) -> bool:
    """检查文件访问权限"""
    # 文件名应包含 user_id
    if user_id not in file_path:
        return False
    
    # 检查文件存在
    if not os.path.exists(file_path):
        return False
    
    return True
```

### 3. 数据备份
```python
import shutil
from datetime import datetime

def backup_user_data(user_id: str):
    """备份用户数据"""
    backup_dir = f"/tmp/backups/{user_id}"
    _ensure_dir(backup_dir)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # 备份用户画像
    profile_src = f"/tmp/user_profiles/{user_id}.json"
    if os.path.exists(profile_src):
        shutil.copy(
            profile_src,
            f"{backup_dir}/profile_{timestamp}.json"
        )
    
    # 备份投资日记
    diary_dir = f"/tmp/investment_diary"
    for file in os.listdir(diary_dir):
        if file.startswith(f"{user_id}_diary_"):
            shutil.copy(
                os.path.join(diary_dir, file),
                f"{backup_dir}/{file}"
            )
    
    return f"✅ 用户数据已备份到: {backup_dir}"
```

## 存储优化策略

### 1. 自动清理
```python
import time

def cleanup_old_files(dir_path: str, days: int = 30):
    """清理过期文件"""
    now = time.time()
    cutoff = now - (days * 86400)  # 30天前
    
    for file in os.listdir(dir_path):
        file_path = os.path.join(dir_path, file)
        
        if os.path.getmtime(file_path) < cutoff:
            os.remove(file_path)
            print(f"已删除过期文件: {file}")
```

### 2. 数据压缩
```python
import gzip
import shutil

def compress_file(file_path: str) -> str:
    """压缩文件"""
    compressed_path = f"{file_path}.gz"
    
    with open(file_path, 'rb') as f_in:
        with gzip.open(compressed_path, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    
    return compressed_path

def decompress_file(compressed_path: str) -> str:
    """解压文件"""
    decompressed_path = compressed_path.replace('.gz', '')
    
    with gzip.open(compressed_path, 'rb') as f_in:
        with open(decompressed_path, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    
    return decompressed_path
```

### 3. 存储监控
```python
def get_storage_usage() -> dict:
    """获取存储使用情况"""
    dirs = [
        "user_profiles",
        "sip_plans",
        "investment_diary",
        "market_alerts"
    ]
    
    usage = {}
    total_size = 0
    
    for dir_name in dirs:
        dir_path = os.path.join("/tmp", dir_name)
        if os.path.exists(dir_path):
            size = sum(
                os.path.getsize(os.path.join(dir_path, f))
                for f in os.listdir(dir_path)
            )
            usage[dir_name] = size
            total_size += size
    
    usage["total"] = total_size
    
    return usage
```

## 总结

本数据存储方案提供：
- ✅ **多层存储**: 内存 + 文件系统 + 云存储 + 知识库
- ✅ **灵活持久化**: JSON 文件存储用户数据
- ✅ **自动管理**: 预签名 URL 自动过期
- ✅ **安全合规**: 加密、访问控制、备份机制
- ✅ **性能优化**: 缓存、压缩、清理策略

通过合理使用不同层次的存储，可以实现数据的高效管理和安全持久化。
