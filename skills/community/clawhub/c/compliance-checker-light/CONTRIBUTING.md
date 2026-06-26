# 贡献指南

感谢您有兴趣为 Compliance Checker MCP Service 做出贡献！本文档将帮助您了解如何参与项目开发。

## 目录

- [贡献流程](#贡献流程)
- [开发环境设置](#开发环境设置)
- [项目结构](#项目结构)
- [代码规范](#代码规范)
- [项目特定说明](#项目特定说明)

## 贡献流程

### 提交 Issue

在提交 Issue 之前，请先搜索现有 Issue 确保问题未被报告。

**Bug 报告请包含：**
- 问题描述和复现步骤
- 预期行为与实际行为
- 环境信息（Python 版本、操作系统、OCR 配置等）
- 相关日志或错误信息

**功能请求请包含：**
- 功能描述和使用场景
- 预期的 API 或配置方式
- 是否愿意提交 PR 实现

### 提交 Pull Request

1. **Fork 并克隆仓库**
   ```bash
   git clone https://github.com/evob-z/compliance_checker_light.git
   cd compliance_checker_light
   ```

2. **创建功能分支**
   ```bash
   git checkout -b feature/your-feature-name
   # 或
   git checkout -b fix/your-bug-fix
   ```

3. **进行开发**
   - 遵循[代码规范](#代码规范)
   - 添加必要的测试
   - 更新相关文档

4. **提交代码**
   ```bash
   git add .
   git commit -m "feat: 添加新功能描述"
   git push origin feature/your-feature-name
   ```

5. **创建 Pull Request**
   - 填写 PR 模板，描述变更内容
   - 关联相关 Issue
   - 等待代码审查

## 开发环境设置

### 环境要求

- Python 3.10+
- pip 或 uv 包管理器
- Git

### 依赖安装

**基础开发环境：**
```bash
# 克隆仓库
git clone https://github.com/evob-z/compliance_checker_light.git
cd compliance_checker_light

# 创建虚拟环境
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# 或
.\.venv\Scripts\activate  # Windows

# 安装基础依赖
pip install -r requirements.txt

# 安装开发依赖
pip install -e ".[dev]"
```

**带 OCR 支持的开发环境：**
```bash
# 本地 OCR（PaddleOCR，体积大）
pip install -e ".[local-ocr]"

# 云端 OCR（阿里云，轻量）
pip install -e ".[cloud-ocr]"

# 完整安装
pip install -e ".[all]"
```

### 环境变量配置

复制示例配置并修改：
```bash
cp .env.example .env
```

**必需配置：**
```bash
LLM_API_KEY=your-api-key
LLM_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
LLM_MODEL=qwen-max
```

**可选配置：**
```bash
# 嵌入模型
EMBED_MODEL=text-embedding-v1

# 视觉模型
VISION_MODEL=qwen3-vl-flash

# OCR 后端：none（默认）/ paddle / aliyun
OCR_BACKEND=none
```

### 本地调试

**运行测试：**
```bash
# 运行所有测试
pytest

# 运行特定测试文件
pytest tests/test_completeness.py -v

# 运行测试并显示覆盖率
pytest --cov=compliance_checker tests/
```

**运行 MCP Server：**
```bash
# 直接运行
python -m compliance_checker.server

# 或使用入口脚本
compliance-checker
```

**运行示例脚本：**
```bash
python run_check.py
```

## 项目结构

```
compliance_checker/
├── src/compliance_checker/          # 源代码
│   ├── server.py                    # MCP Server 入口
│   ├── skill.py                     # Skill 主模块（自然语言接口）
│   ├── skill_formatter.py           # 结果格式化
│   │
│   ├── core/                        # 核心数据模型
│   │   ├── checker_base.py          # 检查器基类
│   │   ├── checker_registry.py      # 检查器注册表
│   │   ├── document.py              # 文档数据模型
│   │   ├── checklist_model.py       # 清单数据模型
│   │   └── result_model.py          # 结果数据模型
│   │
│   ├── checkers/                    # 检查器实现
│   │   ├── completeness_checker.py  # 完整性检查器
│   │   ├── timeliness_checker.py    # 时效性检查器
│   │   ├── compliance_checker.py    # 合规性检查器
│   │   └── visual_checker.py        # 视觉检查器
│   │
│   ├── engine/                      # 声明式执行引擎
│   │   └── declarative_engine.py    # 声明式检查引擎
│   │
│   ├── llm/                         # LLM 客户端
│   │   ├── client.py                # OpenAI 兼容客户端
│   │   └── config.py                # LLM 配置
│   │
│   ├── parsers/                     # 文档解析器
│   │   ├── pdf_parser.py            # PDF 解析
│   │   ├── ocr_engine.py            # OCR 引擎（多后端）
│   │   └── docx_parser.py           # Word 解析
│   │
│   ├── prompts/                     # LLM 提示词
│   │   └── checklist_generator.py   # 清单生成提示词
│   │
│   ├── tools/                       # MCP 工具实现
│   │   ├── checklist.py             # load_checklist
│   │   ├── parser.py                # parse_documents
│   │   ├── completeness.py          # check_completeness
│   │   ├── timeliness.py            # check_timeliness
│   │   ├── compliance.py            # check_compliance
│   │   └── visual.py                # visual_inspection
│   │
│   └── visual/                      # 视觉检测模块
│       ├── qwen_client.py           # Qwen-VL API 封装
│       ├── region_detector.py       # OCR 区域定位
│       └── screenshot.py            # PDF 截图工具
│
├── requirements.txt                 # 基础依赖清单
├── pyproject.toml                   # 项目配置（含可选依赖）
├── Dockerfile                       # Docker 构建文件
└── .env.example                     # 环境变量示例
```

### 模块依赖关系

```
skill.py (入口)
    ├── llm/client.py (清单生成)
    ├── parsers/ (文档解析)
    │   └── ocr_engine.py (OCR 后端)
    └── engine/declarative_engine.py (检查引擎)
        └── checkers/ (检查器实现)
            └── visual/qwen_client.py (视觉检测)
```

## 代码规范

### Python 代码风格

项目使用 **black** 进行代码格式化：

```bash
# 格式化代码
black src/

# 检查格式
black --check src/
```

**代码风格要求：**
- 行长度限制：100 字符
- 使用 4 空格缩进
- 遵循 PEP 8 规范

### 提交信息格式

使用 [Conventional Commits](https://www.conventionalcommits.org/) 格式：

```
<type>(<scope>): <subject>

<body>

<footer>
```

**类型（type）：**
- `feat`: 新功能
- `fix`: Bug 修复
- `docs`: 文档更新
- `style`: 代码格式调整（不影响功能）
- `refactor`: 代码重构
- `test`: 测试相关
- `chore`: 构建/工具变更

**示例：**
```
feat(checkers): 添加批量文档检查支持

- 支持并行处理多个文档
- 添加进度回调接口

Closes #123
```

### 文档注释规范

**模块文档字符串：**
```python
"""模块简述

详细描述模块功能和用法。

Example:
    >>> from compliance_checker.skill import ComplianceSkill
    >>> skill = ComplianceSkill()
"""
```

**函数文档字符串：**
```python
def check_completeness(
    documents: List[Document],
    checklist: Checklist
) -> CompletenessResult:
    """检查文档完整性
    
    Args:
        documents: 待检查的文档列表
        checklist: 检查清单
    
    Returns:
        CompletenessResult: 包含缺失文档和匹配结果的检查结果
    
    Raises:
        ValueError: 当清单为空时抛出
    """
```

### 类型注解

项目使用 Python 类型注解：

```python
from typing import List, Dict, Optional, Any

async def process_documents(
    file_paths: List[str],
    options: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    ...
```

## 项目特定说明

### OCR 后端配置

项目支持三种 OCR 后端，通过环境变量 `OCR_BACKEND` 配置：

| 值 | 说明 | 依赖安装 | 适用场景 |
|---|------|---------|---------|
| `none` | 无 OCR（默认） | 无需额外依赖 | 仅处理可编辑 PDF |
| `paddle` | PaddleOCR 本地引擎 | `pip install -e ".[local-ocr]"` | 离线环境、大量扫描件 |
| `aliyun` | 阿里云 OCR | `pip install -e ".[cloud-ocr]"` | 轻量部署、低频使用 |

**开发时注意事项：**
- OCR 后端在 [`src/compliance_checker/infrastructure/llm/ocr_engine.py`](src/compliance_checker/infrastructure/llm/ocr_engine.py) 中实现，需实现 Core 层的 `OCREngineProtocol`。
- 阿里云分支使用官方 SDK 的 **RecognizeGeneral** 接口；返回体中 `Data` 为 JSON 字符串，解析逻辑见 `_parse_recognize_general_data`（优先 `content`，否则拼接 `prism_wordsInfo` 中的 `word`）。
- 可选环境变量 **`ALIBABA_CLOUD_OCR_ENDPOINT`**：未设置时默认 `ocr-api.cn-hangzhou.aliyuncs.com`。
- 使用延迟导入避免未安装依赖时报错

### Docker 构建参数

Dockerfile 支持通过 `--build-arg` 选择 OCR 配置：

```bash
# 无 OCR（最小化镜像）
docker build -t compliance-checker:latest .

# 本地 OCR（体积大）
docker build --build-arg OCR_BACKEND=local -t compliance-checker:local-ocr .

# 云端 OCR（轻量）
docker build --build-arg OCR_BACKEND=cloud -t compliance-checker:cloud-ocr .
```

**构建参数说明：**
- `OCR_BACKEND`: OCR 后端类型，默认 `none`
- 条件安装逻辑在 Dockerfile 的 `RUN if` 语句中实现

### MCP 协议开发

本项目基于 MCP（Model Context Protocol）协议：

**工具暴露规范：**
- 使用 `@mcp.tool()` 装饰器暴露工具
- 工具函数返回类型为 `List[Dict]` 或 `Dict`
- 提供清晰的 docstring 作为工具描述

**示例：**
```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("compliance-checker")

@mcp.tool()
async def check_completeness(
    project_path: str,
    requirements: str
) -> List[Dict]:
    """检查文档完整性
    
    Args:
        project_path: 项目文档路径
        requirements: 检查要求描述
    
    Returns:
        检查结果列表
    """
    ...
```

**MCP Server 入口：**
- 定义在 `server.py` 中
- 使用 `python -m compliance_checker.server` 启动
- 支持 stdio 通信模式

### 视觉模型配置

视觉检测使用 Qwen-VL 系列：

**默认配置：**
- 模型：`qwen3-vl-flash`
- 端点：OpenAI 兼容模式（`/compatible-mode/v1`）
- 自动复用 `LLM_API_KEY` 和 `LLM_BASE_URL`

**独立配置：**
```bash
VISION_API_KEY=your-vision-key
VISION_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
VISION_MODEL=qwen3-vl-flash
```

---

## 获取帮助

- 提交 Issue：[GitHub Issues](https://github.com/evob-z/compliance_checker_light/issues)
- 阅读文档：[README.md](README.md)

感谢您的贡献！
