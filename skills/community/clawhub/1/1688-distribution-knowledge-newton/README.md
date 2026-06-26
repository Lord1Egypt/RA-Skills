# 1688-distribution-knowledge-newton

查询 1688 分销知识库，获取发货流程、铺货操作、订单管理等分销相关文档。支持按渠道（淘宝、抖音、拼多多等）和工具（自动分销、店长铺货等）筛选。

## 快速开始

> 温馨提示：AK 鉴权逻辑已封装好，只需在 `scripts/biz/` 中实现业务逻辑，并修改 `SKILL.md` 描述技能功能即可。

### 1. AK 测试

AK 用于身份认证，userId 由 AK 自动解析，无需手动传入。

```bash
# 检查 AK 是否已配置
python3 scripts/capabilities/configure/cmd.py
```

- 获取 AK：打开 https://clawhub.1688.com 点击右上角钥匙🔑图标
- 查看已配置的 AK：`~/.openclaw/openclaw.json`

### 2. 测试查询

```bash
python3 scripts/biz/knowledge_query.py
```

## 项目结构

```
1688-distribution-knowledge-newton/
├── SKILL.md                     # Skill 文档（Agent 使用）
├── README.md                    # 项目说明（开发者阅读）
└── scripts/
    ├── __init__.py
    ├── _http.py                # HTTP 客户端
    ├── _auth.py                # 签名认证
    ├── _errors.py              # 错误类型
    ├── _const.py               # 常量定义
    ├── _output.py              # 输出工具
    ├── capabilities/
    │   └── configure/          # AK 配置能力
    └── biz/
        ├── __init__.py
        ├── const.py            # 业务常量配置（可修改）
        └── knowledge_query.py  # 知识库查询模块
```

## 文件说明

| 文件 | 作用 | 是否修改 |
|------|------|----------|
| `SKILL.md` | Agent 调用入口，描述技能功能和使用方式 | ✅ 必须修改 |
| `README.md` | 项目说明文档 | ✅ 按需修改 |
| `scripts/biz/const.py` | 业务常量配置（如渠道/工具列表） | ✅ 可修改 |
| `scripts/biz/*.py` | 业务逻辑实现 | ✅ 必须实现 |
| `scripts/_http.py` | HTTP 客户端，自动签名、重试 | ❌ 不修改 |
| `scripts/_auth.py` | HMAC-SHA256 签名 | ❌ 不修改 |
| `scripts/_errors.py` | 统一错误类型 | ❌ 不修改 |
| `scripts/_const.py` | 常量定义 | ❌ 不修改 |
| `scripts/_output.py` | 输出格式化 | ❌ 不修改 |
| `scripts/capabilities/` | AK 配置等通用能力 | ❌ 不修改 |

## 开发指南

### 1. 配置常量

修改 `scripts/biz/const.py` 中的配置：

```python
# 支持的渠道列表
VALID_CHANNELS = [
    "淘宝", "天猫", "抖音", "拼多多", ...
]

# 支持的工具列表
VALID_BUSINESSES = [
    "逸淘分销铺货", "自动分销", "代发助手王", ...
]
```

### 2. 调用知识库

```python
from scripts.biz.knowledge_query import query_knowledge

# 指定渠道和工具
result = query_knowledge(
    query="发货流程",
    channel="抖音",        # 直接传中文名称
    business="自动分销",    # 直接传中文名称
)

# 使用默认知识库
result = query_knowledge(
    query="铺货流程",
    channel="default",
    business="default",
)
```

### 3. 处理返回结果

```python
if result.get("success"):
    data = result.get("data")
    doc_list = data.get("reRankDocList", [])
    for doc in doc_list:
        print(f"标题: {doc.get('chunking_key')}")
        print(f"内容: {doc.get('chunking_val')}")
        print(f"相关度: {doc.get('score')}")
else:
    print(f"失败：{result.get('error')}")
```

## API 调用

```python
from scripts._http import api_post

result = api_post(
    tool_name="distribution_knowledge_tool",  # API 名称
    body={"query": "value", "channel": "default", "business": "default"}
)
```

自动处理：HMAC-SHA256 签名、网络重试（3 次）、错误映射、响应解包

## 渠道与工具

### 21个渠道
淘宝、天猫、抖音、拼多多、快团团、小红书、快手、微信小店、京东、有赞、微店、淘特、微信小商店、支付宝、苏宁、闲鱼、饿了么、美团、度小店、微盟、微购相册

### 24个工具
逸淘分销铺货、自动分销、代发助手王、店长铺货、妙手分销、速当家分销、智淘分销、甩手易分销、无忧分销王、晓风分销、大泽云铺货、顶卖分销、铺货代发、1688官方铺货、普云铺货、麦爆了分销、马上分销、掌中宝分销、智汇分销、微购相册、抖掌柜分销、旺分销铺货、小天分销、火牛分销王

## 注意事项

1. **AK 配置**：所有 API 依赖环境变量 `ALI_1688_AK`
2. **userId 无需传入**：AK 经网关自动转换为 userId，业务代码无需关心用户身份
3. **返回格式**：统一返回 `{"success": bool, "data": ..., "error": str}`
4. **中文输出**：所有提示信息使用中文
5. **模块导入**：使用 `from scripts.xxx import` 格式
