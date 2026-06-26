---
name: compliance-checker
version: 1.1.6
license: MIT
description: >
  AI 驱动的项目手续合规审查 Skill。通过 Python API 检查 PDF/Word/图片文档的
  完整性、时效性和合规性（印章/签名）。当用户需要审查项目文档是否齐全、有效、
  合规时使用。典型场景：建设工程手续审查、发票合规检查、行政审批材料审查。
metadata:
  openclaw:
    requires:
      bins: [python, pip]
      install: pip install compliance-checker
    secrets:
      supported: true
      description: 支持 OpenClaw SecretRef 规范进行密钥管理
      providers: [env, file, exec]
      required_keys:
        - llm_api_key
      optional_keys:
        - llm_base_url
        - llm_model
        - llm_timeout
        - llm_max_retries
        - embed_api_key
        - embed_base_url
        - embed_model
        - vision_api_key
        - vision_base_url
        - vision_model
        - ocr_backend
        - alibaba_cloud_access_key_id
        - alibaba_cloud_access_key_secret
---

# Compliance Checker - 项目手续合规审查

## 核心能力

- 资料完整性核对（精确+语义匹配文件名）
- 资料时效性核对（有效期判定）
- 视觉合规检测（Qwen-VL 识别印章/签名）

## Python API

本工具提供 3 个原子 API 函数，直接返回 Python 字典，无需解析 JSON。

### 1. completeness - 文档批量嗅探

扫描目录中的文件，与给定文档名称列表做精确+语义匹配。

```python
from compliance_checker.application.commands.completeness_cmd import run_completeness

result = await run_completeness(
    path="D:/docs",
    documents=["立项批复", "环评报告", "施工许可证"]
)
```

**参数：**

| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| path | str | 是 | 项目文件夹路径 |
| documents | List[str] | 是 | 文档名称列表 |

**返回值：**

```python
{
    "立项批复": {
        "path": "D:/docs/立项批复.pdf",
        "similarity": 1.0,
        "match_type": "exact"
    },
    "环评报告": {
        "path": "D:/docs/环境评价报告.pdf",
        "similarity": 0.85,
        "match_type": "semantic"
    },
    "施工许可证": None
}
```

- `match_type` 为 `exact` 表示精确匹配（子串包含），`semantic` 表示语义匹配
- 值为 `None` 表示目录中未找到匹配文件

### 2. timeliness - 时效性计算

解析单个文件，提取日期信息，判定文档时效性状态。

```python
from compliance_checker.application.commands.timeliness_cmd import run_timeliness

result = await run_timeliness(
    file="D:/docs/立项批复.pdf",
    reference_time="2026-03-15"  # 可选，默认为当前时间
)
```

**参数：**

| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| file | str | 是 | 文件路径（.pdf / .docx / .doc / 图片） |
| reference_time | str | 否 | 校验基准时间（YYYY-MM-DD），默认为当前时间 |

**返回值：**

```python
{
    "status": "VALID",
    "sign_date": "2025-06-15",
    "expiry_date": "2026-06-15",
    "validity": "365天",
    "branch": "HAS_EXPIRY",
    "reason": "文件在有效期内"
}
```

- `status`: `VALID`（有效）/ `EXPIRED`（过期）/ `UNKNOWN`（无法判定）

### 3. visual - 视觉质检

检测文档中的印章、签名等视觉元素。

```python
from compliance_checker.application.commands.visual_cmd import run_visual

result = await run_visual(
    file="D:/docs/立项批复.pdf",
    targets=["公章", "法人签字"]
)
```

**参数：**

| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| file | str | 是 | 文件路径（.pdf / 图片） |
| targets | List[str] | 是 | 检测目标列表（如["公章", "法人签字"]） |

**targets 命名规则：**

- 含"章"的视为印章检测（如"公章"、"发票专用章"、"骑缝章"）
- 含"签"的视为签名检测（如"法人签字"、"经办人签名"）
- 用户的原始 target 字符串会透传到 Qwen-VL 的 Prompt 中

**返回值：**

```python
{
    "公章": {
        "found": True,
        "confidence": 0.95,
        "location": "右下角",
        "reasoning": "检测到红色圆形公章"
    },
    "法人签字": {
        "found": False,
        "confidence": 0.0,
        "location": "",
        "reasoning": "已检查 2 页，未找到法人签字"
    }
}
```

## 辅助函数

```python
from compliance_checker.api import check_health

# 检查服务健康状态
health = await check_health()
print(health["status"])  # "healthy" 或 "unhealthy"
```

## 路径规则

传递路径参数时，**建议使用正斜杠 (/)**：

- 推荐：`D:/projects/docs`
- 可用但不推荐：`D:\projects\docs`

## 典型工作流

当用户要求审查文档时，按以下步骤执行：

1. **验证安装**：首次使用前检查健康状态确认可用
2. **获取路径**：**必须从用户处获取具体的文件或目录路径**
   - 如用户未提供路径，必须直接询问用户，不得自主探测
3. **分析用户意图**：从用户描述中提取检查维度：
   - 需要检查哪些文件 -> 使用 `run_completeness`
   - 需要检查有效期 -> 使用 `run_timeliness`
   - 需要检查印章/签名 -> 使用 `run_visual`
4. **执行 API 调用**：根据需要调用一个或多个函数
5. **汇总结果**：直接处理返回的字典，向用户汇报

### 参数要求（安全规范）

**所有 API 函数的路径参数均为严格必需：**

| 函数 | 必需参数 | 说明 |
|------|----------|------|
| run_completeness | path, documents | 必须提供目录路径和文档列表 |
| run_timeliness | file | 必须提供文件路径 |
| run_visual | file, targets | 必须提供文件路径和检测目标 |

**Agent 行为约束：**
- **禁止自主探测路径**：Agent 不得扫描文件系统
- **必须询问用户**：如果用户请求中未提供具体的文件或目录路径，Agent 必须直接询问用户获取绝对路径
- **禁止猜测路径**：Agent 不得假设或推断文件位置

### 示例：发票审查

```python
from compliance_checker.application.commands.completeness_cmd import run_completeness
from compliance_checker.application.commands.timeliness_cmd import run_timeliness
from compliance_checker.application.commands.visual_cmd import run_visual

# 步骤1：检查发票文件是否存在
completeness_result = await run_completeness(
    path="D:/finance/invoices",
    documents=["增值税发票", "收据"]
)

# 步骤2：检查时效性
timeliness_result = await run_timeliness(
    file="D:/finance/invoices/增值税发票.pdf",
    reference_time="2026-03-15"
)

# 步骤3：检查印章
visual_result = await run_visual(
    file="D:/finance/invoices/增值税发票.pdf",
    targets=["发票专用章"]
)
```

### 示例：工程手续审查

```python
# 步骤1：批量检查文件完整性
completeness = await run_completeness(
    path="D:/projects/building",
    documents=["立项批复", "环评批复", "施工许可证"]
)

# 步骤2：对每个找到的文件逐一检查时效性
for doc_name, doc_info in completeness.items():
    if doc_info:
        timeliness = await run_timeliness(file=doc_info["path"])
        print(f"{doc_name}: {timeliness['status']}")

# 步骤3：检查是否盖有公章
visual = await run_visual(
    file="D:/projects/building/立项批复.pdf",
    targets=["公章"]
)
```

## 错误处理

所有错误以异常形式抛出，使用 try-except 捕获：

```python
from compliance_checker.core.exceptions import ComplianceCheckerError

try:
    result = await run_completeness(path="D:/nonexistent", documents=["test"])
except FileNotFoundError as e:
    print(f"路径错误: {e}")
except ValueError as e:
    print(f"参数错误: {e}")
except ComplianceCheckerError as e:
    print(f"检查错误: {e}")
```

| 错误类型 | 含义 | 恢复策略 |
|----------|------|----------|
| FileNotFoundError | 文件/目录不存在 | 请用户确认路径 |
| ValueError | 参数格式错误 | 检查参数格式（日期格式等） |
| ComplianceCheckerError | 内部异常 | 检查环境配置和 API 密钥 |

## 支持的文档格式

- PDF（支持 OCR 识别扫描件）
- Word（.docx, .doc）
- 图片（.png, .jpg, .jpeg）

## 支持的日期格式（timeliness 命令）

- `2024年3月15日`
- `2024-03-15`
- `2024/03/15`
- `2024年3月`（自动补全为3月31日）

---

# 安装与配置（给用户）

## 安装

**步骤 1：创建并激活虚拟环境（venv）**

```bash
# 创建虚拟环境
python -m venv .venv

# Windows PowerShell 激活
.venv\Scripts\activate

# 或 Windows CMD 激活
.venv\Scripts\activate.bat

# 或 Linux/Mac 激活
source .venv/bin/activate
```

**步骤 2：安装 compliance-checker**

```bash
# 基础安装（不含 OCR 功能）
pip install compliance-checker

# 或安装阿里云 OCR 支持（云端 OCR，需网络）
pip install compliance-checker[cloud-ocr]

# 或安装本地 PaddleOCR 支持（本地 OCR，体积较大）
pip install compliance-checker[local-ocr]

# 或完整安装（包含所有可选依赖）
pip install compliance-checker[all]
```

## 验证安装

```python
from compliance_checker.api import check_health
import compliance_checker

# 检查版本
print(compliance_checker.__version__)

# 检查健康状态
health = await check_health()
print(health["status"])
```

## 配置方式（SecretRef）

本 Skill 遵循 OpenClaw SecretRef 规范进行密钥管理，**不支持直接读取环境变量**。

### 必需配置

- `llm_api_key`: LLM API 密钥

### 可选配置

- `llm_base_url`: LLM API 端点（默认: https://api.openai.com/v1）
- `llm_model`: LLM 模型名称（默认: gpt-4o）
- `llm_timeout`: 请求超时（默认: 60秒）
- `llm_max_retries`: 最大重试次数（默认: 3）
- `embed_api_key`: 嵌入模型 API 密钥（默认使用 llm_api_key）
- `embed_model`: 嵌入模型名称（默认: text-embedding-v1）
- `vision_api_key`: 视觉模型 API 密钥（默认使用 llm_api_key）
- `vision_model`: 视觉模型名称（默认: qwen3-vl-flash）
- `ocr_backend`: OCR 后端（默认: none）
- `alibaba_cloud_access_key_id`: 阿里云 Access Key ID
- `alibaba_cloud_access_key_secret`: 阿里云 Access Key Secret

### 使用示例

```python
from compliance_checker.infrastructure.config import CheckerConfig

# 使用 SecretRef 配置
config = CheckerConfig.from_secret_ref(
    secrets={
        "llm_api_key": {"source": "env", "provider": "default", "id": "LLM_API_KEY"},
        "llm_model": "qwen-max"
    }
)
```

---

# 数据隐私与合规声明 (Data Privacy Notice)

使用本工具时，您的文档数据可能会发送到外部服务：

### 视觉检测服务（visual API）
- 当调用 `run_visual` 时，文档图像及检测目标（targets）将通过 HTTPS 加密传输至配置的视觉模型服务端
- 默认使用阿里云 DashScope（`LLM_BASE_URL`），可通过配置切换到本地部署的 Vision 模型

### OCR 服务（可选）
- `OCR_BACKEND=none`（默认）：本地处理，不发送数据
- `OCR_BACKEND=paddle`：本地 PaddleOCR，数据不离开本机
- `OCR_BACKEND=aliyun`：发送到阿里云 OCR 服务

### 安全建议
处理敏感 B2B 合规文档时，建议：
1. 配置本地部署的 Vision 模型端点
2. 将 `OCR_BACKEND` 设置为 `paddle` 使用本地 OCR
3. 通过私有 LLM 端点实现完全内网部署

**本工具不会持久化存储您的文档内容。**
