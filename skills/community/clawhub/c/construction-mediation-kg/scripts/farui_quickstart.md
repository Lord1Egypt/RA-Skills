# 通义法睿集成 - 快速开始指南

## 前置准备

### 1. 安装依赖
```bash
pip install dashscope
```

### 2. 获取API Key
1. 访问 [阿里云百炼平台](https://bailian.aliyun.com/)
2. 注册/登录账号
3. 创建API Key（免费额度有限，建议按需充值）

### 3. 配置环境变量
```bash
# Windows (PowerShell)
$env:DASHSCOPE_API_KEY = "your-api-key"

# Linux/Mac
export DASHSCOPE_API_KEY="your-api-key"
```

---

## 快速使用

### 方式一：便捷函数（推荐）

```python
from farui_integration import quick_legal_search, quick_case_analysis

# 法律检索 - 秒级返回
result = quick_legal_search("建设工程合同无效的法律后果")
print(result)

# 案件分析 - 结构化输出
result = quick_case_analysis("发包人拖欠工程款，承包人主张违约金及利息")
print(result)
```

### 方式二：完整功能调用

```python
from farui_integration import MediationFarui

# 初始化客户端
mediator = MediationFarui()

# 法律检索
result = mediator.legal_search("工程款优先受偿权的行使条件")

# 案件分析
result = mediator.analyze_case("""
案件背景：某房地产项目，发包人A公司拖欠承包人B公司工程款约800万元，
工期延误约60天，双方就付款金额和违约责任产生争议。
""")

# 文书生成
result = mediator.draft_document("调解协议书", {
    "甲方": "A公司",
    "乙方": "B公司",
    "调解金额": "800万元",
    "付款期限": "2026年6月30日前"
})

# 法律风险评估
result = mediator.calculate_legal_risk([
    "调解协议约定分期付款，但未约定违约责任",
    "未明确工程质量保修期内的责任划分",
    "未约定司法确认条款"
])
```

---

## 功能对照表

| 场景 | 函数 | 说明 |
|-----|------|-----|
| 法律检索 | `quick_legal_search()` | 法规、案例、司法解释 |
| 案件分析 | `quick_case_analysis()` | 争议焦点、法律关系、证据梳理 |
| 完整调用 | `MediationFarui` | 支持法律检索/案件分析/文书生成/风险评估 |

---

## 注意事项

1. **Token限制**：单次请求不超过12k tokens
2. **计费**：输入输出均20元/百万tokens
3. **隐私**：敏感信息建议脱敏后调用
4. **备用**：API不可用时，使用本地知识图谱作为备份

---

## 故障排查

| 问题 | 解决方案 |
|-----|---------|
| `InvalidApiKey` | 检查API Key是否正确配置 |
| `RateLimitExceeded` | 降低调用频率或升级配额 |
| `max_tokens` 不足 | 减少输入文本长度或分段调用 |
| 模块导入失败 | 确认已安装 dashscope |

---

## 扩展场景

结合本项目的其他Skill，可以实现更强的组合能力：

```python
# 造价 + 法律 + 调解
from cn_cost_control import calculate_dispute_amount
from farui_integration import quick_legal_search

# 计算争议工程造价
amount = calculate_dispute_amount(project_data)

# 获取法律依据
legal_basis = quick_legal_search(f"工程款{amount}万元的诉讼时效")
```

---

**更多信息**：请参阅 `farui_integration.py` 源码中的详细注释