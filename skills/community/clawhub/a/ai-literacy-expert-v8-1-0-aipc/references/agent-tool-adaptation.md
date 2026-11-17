> **V7 兼容性说明**：本文件从 V6 完整继承。V7 保留所有 V6 能力，本文件内容完全有效。
> V7 新增 references 见 `references/edge-cloud-architecture.md` / `references/zero-upload-privacy.md` / `references/npu-scheduling-guide.md` / `references/edge-cloud-protocol.md` / `references/audit-report-v7.md`。
> 原始文件版本：V6 · 继承版本：V7 · 继承日期：2026-08-15

# Agent 工具标准化适配指南

> V6 新增 · 本地 AI 工具在 Agent 平台中的标准化接入规范

## 1. 概述

本地 AI 工具（OCR/ASR/TTS/RAG/数据分析）通过标准化 Skill 接口接入 Agent 平台（Qoder / QoderWork / TRAE Work），实现跨平台统一调用。

### 1.1 适配原则
- **统一接口**：所有本地 AI 工具遵循相同 JSON Schema
- **平台无关**：同一 Skill 可在 Qoder、WorkBuddy、TRAE Work 中运行
- **版本管理**：每个工具独立 semver 版本
- **健康检查**：启动时自动检测依赖服务可用性

## 2. Skill 接口规范

### 2.1 标准 Skill 结构

```json
{
  "skill_id": "local-ocr-v1",
  "skill_name": "本地OCR识别",
  "version": "1.0.0",
  "description": "基于 PaddleOCR + OpenVINO 的本地文字识别服务",
  "category": "ai_tool",
  "platform": ["qoder", "workbuddy", "trae_work"],
  "input_schema": {
    "type": "object",
    "properties": {
      "image": {
        "type": "string",
        "description": "图片 base64 或文件路径",
        "format": "base64|path"
      },
      "mode": {
        "type": "string",
        "enum": ["text", "table", "formula", "handwriting"],
        "default": "text"
      },
      "language": {
        "type": "string",
        "default": "ch"
      }
    },
    "required": ["image"]
  },
  "output_schema": {
    "type": "object",
    "properties": {
      "text": { "type": "string" },
      "confidence": { "type": "number" },
      "regions": {
        "type": "array",
        "items": {
          "type": "object",
          "properties": {
            "text": { "type": "string" },
            "bbox": { "type": "array", "items": { "type": "number" } },
            "confidence": { "type": "number" }
          }
        }
      }
    }
  },
  "health_check": {
    "endpoint": "http://localhost:8901/health",
    "method": "GET",
    "expected_status": 200,
    "timeout_ms": 3000
  },
  "error_codes": {
    "OCR_001": "图片格式不支持",
    "OCR_002": "识别超时",
    "OCR_003": "服务不可用",
    "OCR_004": "内存不足"
  }
}
```

### 2.2 Skill 注册表

```python
SKILL_REGISTRY = {
    "local-ocr-v1": {
        "name": "本地OCR识别",
        "port": 8901,
        "health": "/health",
        "endpoints": {
            "recognize": "/api/v1/ocr/recognize",
            "table": "/api/v1/ocr/table",
            "formula": "/api/v1/ocr/formula",
            "handwriting": "/api/v1/ocr/handwriting"
        }
    },
    "local-asr-v1": {
        "name": "本地语音识别",
        "port": 8902,
        "health": "/health",
        "endpoints": {
            "transcribe": "/api/v1/asr/transcribe",
            "stream": "/api/v1/asr/stream",
            "evaluate": "/api/v1/asr/evaluate"
        }
    },
    "local-tts-v1": {
        "name": "本地语音合成",
        "port": 8903,
        "health": "/health",
        "endpoints": {
            "synthesize": "/api/v1/tts/synthesize",
            "stream": "/api/v1/tts/stream",
            "voices": "/api/v1/tts/voices"
        }
    },
    "local-rag-v1": {
        "name": "本地知识检索",
        "port": 8904,
        "health": "/health",
        "endpoints": {
            "ingest": "/api/v1/rag/ingest",
            "query": "/api/v1/rag/query",
            "chat": "/api/v1/rag/chat"
        }
    }
}
```

## 3. 平台适配层

### 3.1 Qoder 适配

```python
# Qoder Skill 调用适配
class QoderSkillAdapter:
    """将本地 AI 工具注册为 Qoder Skill"""
    
    def __init__(self, skill_config):
        self.config = skill_config
        self.base_url = f"http://localhost:{skill_config['port']}"
    
    async def execute(self, params: dict) -> dict:
        """执行 Skill 调用"""
        # 1. 健康检查
        if not await self._health_check():
            return {"error": "service_unavailable", "code": f"{self.config['name']}_003"}
        
        # 2. 参数校验
        validated = self._validate_input(params)
        
        # 3. 调用服务
        async with aiohttp.ClientSession() as session:
            endpoint = self.config['endpoints'][validated.get('action', 'recognize')]
            async with session.post(f"{self.base_url}{endpoint}", 
                                    json=validated) as resp:
                return await resp.json()
    
    async def _health_check(self) -> bool:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.base_url}/health", 
                                       timeout=aiohttp.ClientTimeout(total=3)) as resp:
                    return resp.status == 200
        except Exception:
            return False
```

### 3.2 QoderWork 适配

```python
# QoderWork MCP 工具适配
class QoderWorkMCPAdapter:
    """将本地 AI 工具注册为 QoderWork MCP Tool"""
    
    def get_tool_definitions(self) -> list:
        """返回 MCP Tool 定义列表"""
        tools = []
        for skill_id, config in SKILL_REGISTRY.items():
            tool = {
                "name": skill_id,
                "description": config["name"],
                "inputSchema": self._build_schema(config),
                "handler": self._make_handler(config)
            }
            tools.append(tool)
        return tools
    
    def _build_schema(self, config: dict) -> dict:
        """构建 JSON Schema"""
        return {
            "type": "object",
            "properties": {
                "action": {"type": "string", "enum": list(config["endpoints"].keys())},
                "data": {"type": "object"}
            },
            "required": ["action", "data"]
        }
```

### 3.3 TRAE Work 适配

```python
# TRAE Work 适配
class TraeWorkAdapter:
    """将本地 AI 工具注册为 TRAE Work 插件"""
    
    def register_plugin(self, skill_id: str):
        config = SKILL_REGISTRY[skill_id]
        return {
            "plugin_id": skill_id,
            "display_name": config["name"],
            "api_base": f"http://localhost:{config['port']}",
            "auth": "none",  # 本地服务无需鉴权
            "retry": {"max_retries": 3, "backoff": "exponential"},
            "timeout": {"connect": 5, "read": 30}
        }
```

## 4. 统一错误处理

### 4.1 错误码体系

```python
ERROR_REGISTRY = {
    # 通用错误
    "COMMON_001": {"message": "参数校验失败", "http_status": 400},
    "COMMON_002": {"message": "服务不可用", "http_status": 503},
    "COMMON_003": {"message": "请求超时", "http_status": 504},
    
    # OCR 错误
    "OCR_001": {"message": "图片格式不支持", "http_status": 400},
    "OCR_002": {"message": "识别超时", "http_status": 504},
    "OCR_003": {"message": "OCR 服务不可用", "http_status": 503},
    
    # ASR 错误
    "ASR_001": {"message": "音频格式不支持", "http_status": 400},
    "ASR_002": {"message": "转写超时", "http_status": 504},
    "ASR_003": {"message": "ASR 服务不可用", "http_status": 503},
    
    # TTS 错误
    "TTS_001": {"message": "音色不可用", "http_status": 400},
    "TTS_002": {"message": "合成超时", "http_status": 504},
    "TTS_003": {"message": "TTS 服务不可用", "http_status": 503},
    
    # RAG 错误
    "RAG_001": {"message": "文档格式不支持", "http_status": 400},
    "RAG_002": {"message": "检索超时", "http_status": 504},
    "RAG_003": {"message": "RAG 服务不可用", "http_status": 503},
    "RAG_004": {"message": "知识库不存在", "http_status": 404}
}
```

### 4.2 降级策略

```python
class FallbackManager:
    """多平台降级策略管理"""
    
    FALLBACK_CHAIN = {
        "ocr": ["local-paddleocr", "cloud-baidu-ocr", "cloud-tencent-ocr"],
        "asr": ["local-whisper", "cloud-aliyun-asr", "cloud-tencent-asr"],
        "tts": ["local-fastspeech2", "cloud-edge-tts", "cloud-aliyun-tts"],
        "rag": ["local-chromadb", "cloud-elasticsearch"],
    }
    
    async def execute_with_fallback(self, tool: str, params: dict) -> dict:
        chain = self.FALLBACK_CHAIN.get(tool, [])
        for provider in chain:
            try:
                result = await self._call_provider(provider, params)
                if result.get("success"):
                    result["provider"] = provider
                    return result
            except Exception as e:
                logger.warning(f"{provider} failed: {e}")
                continue
        
        return {"success": False, "error": "all_providers_failed"}
```

## 5. 版本管理与兼容性

### 5.1 版本策略

```
语义化版本 (semver): MAJOR.MINOR.PATCH

MAJOR: 输入/输出 Schema 不兼容变更
MINOR: 新增功能，向后兼容
PATCH: Bug 修复，向后兼容
```

### 5.2 兼容性矩阵

| Skill | Qoder | QoderWork | TRAE Work | 最低 Python |
|-------|-------|-----------|-----------|-------------|
| local-ocr-v1 | ✅ | ✅ | ✅ | 3.9 |
| local-asr-v1 | ✅ | ✅ | ✅ | 3.9 |
| local-tts-v1 | ✅ | ✅ | ✅ | 3.9 |
| local-rag-v1 | ✅ | ✅ | ✅ | 3.9 |
| local-analysis-v1 | ✅ | ✅ | ✅ | 3.9 |

## 6. 质量门控

| 检查项 | 标准 | 验证方法 |
|--------|------|----------|
| 接口一致性 | 100% 符合 Schema | JSON Schema 校验 |
| 健康检查 | <3s 响应 | 启动时自动检测 |
| 错误码覆盖 | 所有异常有对应错误码 | 代码审查 |
| 降级可用 | 至少 1 个降级路径可用 | 故障注入测试 |
| 跨平台兼容 | 3 平台全部通过 | 集成测试 |
| 文档完整 | 每个端点有示例 | 文档检查 |
