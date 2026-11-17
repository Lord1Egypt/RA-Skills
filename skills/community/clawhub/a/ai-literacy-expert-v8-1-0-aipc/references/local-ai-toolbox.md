> **V7 兼容性说明**：本文件从 V6 完整继承。V7 保留所有 V6 能力，本文件内容完全有效。
> V7 新增 references 见 `references/edge-cloud-architecture.md` / `references/zero-upload-privacy.md` / `references/npu-scheduling-guide.md` / `references/edge-cloud-protocol.md` / `references/audit-report-v7.md`。
> 原始文件版本：V6 · 继承版本：V7 · 继承日期：2026-08-15

# 本地 AI 教学工具箱

> V6 新增 · 能力七：本地 AI 教学工具箱集成指南

## 1. 概述

将 OCR、ASR、TTS、RAG 四大本地 AI 工具整合为统一的教学工具箱，教师可通过 p5.js 课件或 Agent 平台一键调用。

### 1.1 工具箱架构

```
┌──────────────────────────────────────────────────────┐
│                  教师操作界面（p5.js / Agent）          │
├──────────────────────────────────────────────────────┤
│                   统一调用网关（Gateway）               │
├────────┬────────┬────────┬────────┬──────────────────┤
│  OCR   │  ASR   │  TTS   │  RAG   │  数据分析         │
│ :8901  │ :8902  │ :8903  │ :8904  │  :8905           │
├────────┴────────┴────────┴────────┴──────────────────┤
│              OpenVINO 推理引擎（共享）                  │
├──────────────────────────────────────────────────────┤
│         CPU / GPU / NPU 异构硬件资源                   │
└──────────────────────────────────────────────────────┘
```

### 1.2 工具清单

| 工具 | 端口 | 模型 | 用途 |
|------|------|------|------|
| OCR | 8901 | PaddleOCR v4 + INT8 | 教材文字/表格/公式识别 |
| ASR | 8902 | Whisper-small + FP16 | 课堂录音转写/语音答题 |
| TTS | 8903 | FastSpeech2 + FP16 | 课件朗读/角色配音 |
| RAG | 8904 | BGE-small + INT8 | 教学知识库检索/智能问答 |
| 数据分析 | 8905 | Pandas + Plotly | 成绩分析/学情统计 |

## 2. 统一网关设计

### 2.1 Gateway 服务

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx
import time

app = FastAPI(title="AI Teaching Toolbox Gateway", version="1.0.0")

# 服务注册表
SERVICES = {
    "ocr": {"host": "localhost", "port": 8901, "name": "OCR识别"},
    "asr": {"host": "localhost", "port": 8902, "name": "语音识别"},
    "tts": {"host": "localhost", "port": 8903, "name": "语音合成"},
    "rag": {"host": "localhost", "port": 8904, "name": "知识检索"},
    "analysis": {"host": "localhost", "port": 8905, "name": "数据分析"},
}

class ToolboxRequest(BaseModel):
    tool: str
    action: str
    params: dict

class ToolboxResponse(BaseModel):
    success: bool
    tool: str
    data: dict
    latency_ms: float
    provider: str = "local"

@app.post("/api/v1/toolbox/execute")
async def execute_tool(req: ToolboxRequest):
    start = time.time()
    
    if req.tool not in SERVICES:
        raise HTTPException(400, f"Unknown tool: {req.tool}")
    
    svc = SERVICES[req.tool]
    url = f"http://{svc['host']}:{svc['port']}/api/v1/{req.tool}/{req.action}"
    
    try:
        async with httpx.AsyncClient(timeout=30) as client:
            resp = await client.post(url, json=req.params)
            resp.raise_for_status()
            
            latency = (time.time() - start) * 1000
            return ToolboxResponse(
                success=True,
                tool=req.tool,
                data=resp.json(),
                latency_ms=round(latency, 2)
            )
    except httpx.ConnectError:
        # 降级到云端
        return await _fallback_to_cloud(req.tool, req.action, req.params)
    except Exception as e:
        raise HTTPException(500, str(e))

@app.get("/api/v1/toolbox/health")
async def health_check():
    """全工具健康状态"""
    results = {}
    for name, svc in SERVICES.items():
        try:
            async with httpx.AsyncClient(timeout=3) as client:
                resp = await client.get(f"http://{svc['host']}:{svc['port']}/health")
                results[name] = {"status": "healthy" if resp.status_code == 200 else "degraded"}
        except Exception:
            results[name] = {"status": "offline"}
    return results

@app.get("/api/v1/toolbox/capabilities")
async def capabilities():
    """返回所有工具能力描述"""
    return {
        "ocr": {
            "name": "OCR 文字识别",
            "actions": ["recognize", "table", "formula", "handwriting"],
            "description": "识别教材、试卷、手写内容"
        },
        "asr": {
            "name": "ASR 语音识别",
            "actions": ["transcribe", "stream", "evaluate"],
            "description": "课堂录音转写、语音答题识别"
        },
        "tts": {
            "name": "TTS 语音合成",
            "actions": ["synthesize", "stream", "voices"],
            "description": "课件内容朗读、角色配音"
        },
        "rag": {
            "name": "RAG 知识检索",
            "actions": ["ingest", "query", "chat"],
            "description": "教学知识库问答、资料检索"
        },
        "analysis": {
            "name": "数据分析",
            "actions": ["analyze", "chart", "report"],
            "description": "成绩统计、学情分析、可视化"
        }
    }
```

## 3. p5.js 课件集成

### 3.1 工具箱面板 UI

```javascript
// p5.js 中调用本地 AI 工具箱
class AIToolbox {
  constructor(p5) {
    this.p5 = p5;
    this.gatewayUrl = 'http://localhost:8900/api/v1/toolbox';
    this.tools = {};
    this.activeTool = null;
  }
  
  async init() {
    // 检查工具箱健康状态
    try {
      const resp = await fetch(`${this.gatewayUrl}/health`);
      this.tools = await resp.json();
      console.log('AI 工具箱状态:', this.tools);
    } catch (e) {
      console.warn('AI 工具箱不可用，使用离线模式');
      this.tools = { ocr: {status:'offline'}, asr: {status:'offline'}, 
                     tts: {status:'offline'}, rag: {status:'offline'} };
    }
  }
  
  async callTool(toolName, action, params) {
    try {
      const resp = await fetch(`${this.gatewayUrl}/execute`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ tool: toolName, action, params })
      });
      return await resp.json();
    } catch (e) {
      console.error(`${toolName} 调用失败:`, e);
      return { success: false, error: e.message };
    }
  }
  
  // 快捷方法
  async recognizeText(imageBase64) {
    return this.callTool('ocr', 'recognize', { image: imageBase64 });
  }
  
  async transcribeAudio(audioBlob) {
    const formData = new FormData();
    formData.append('audio', audioBlob);
    // 使用 fetch 直接上传
    const resp = await fetch('http://localhost:8902/api/v1/asr/transcribe', {
      method: 'POST',
      body: formData
    });
    return resp.json();
  }
  
  async speakText(text, voice = 'xiaoxiao') {
    return this.callTool('tts', 'synthesize', { text, voice });
  }
  
  async queryKnowledge(question) {
    return this.callTool('rag', 'query', { question, top_k: 5 });
  }
}
```

### 3.2 教学场景示例

```javascript
// 场景：教材拍照 → OCR 识别 → 知识点提取 → RAG 检索相关教案
async function textbookToLesson(imageBase64) {
  const toolbox = new AIToolbox();
  await toolbox.init();
  
  // Step 1: OCR 识别教材内容
  const ocrResult = await toolbox.recognizeText(imageBase64);
  if (!ocrResult.success) return { error: 'OCR 识别失败' };
  
  const text = ocrResult.data.text;
  
  // Step 2: RAG 检索相关教学资源
  const ragResult = await toolbox.queryKnowledge(text);
  if (!ragResult.success) return { error: '知识库检索失败' };
  
  // Step 3: 组装教学建议
  return {
    textbook_content: text,
    related_resources: ragResult.data.results,
    teaching_suggestion: '基于识别内容，建议从以下角度展开教学...'
  };
}
```

## 4. 工具编排（Pipeline）

### 4.1 教学 Pipeline 定义

```python
class TeachingPipeline:
    """教学工具编排引擎"""
    
    PIPELINES = {
        "教材数字化": {
            "steps": [
                {"tool": "ocr", "action": "recognize", "desc": "识别教材文字"},
                {"tool": "ocr", "action": "table", "desc": "识别教材表格"},
                {"tool": "rag", "action": "ingest", "desc": "导入知识库"},
            ]
        },
        "课堂录音分析": {
            "steps": [
                {"tool": "asr", "action": "transcribe", "desc": "录音转写"},
                {"tool": "rag", "action": "query", "desc": "提取知识点"},
                {"tool": "analysis", "action": "analyze", "desc": "课堂互动统计"},
            ]
        },
        "有声课件生成": {
            "steps": [
                {"tool": "rag", "action": "query", "desc": "检索教学内容"},
                {"tool": "tts", "action": "synthesize", "desc": "生成语音"},
            ]
        },
        "学情分析报告": {
            "steps": [
                {"tool": "analysis", "action": "analyze", "desc": "成绩数据分析"},
                {"tool": "analysis", "action": "chart", "desc": "生成可视化图表"},
                {"tool": "rag", "action": "query", "desc": "检索改进建议"},
                {"tool": "analysis", "action": "report", "desc": "生成报告"},
            ]
        }
    }
    
    async def run(self, pipeline_name: str, initial_params: dict) -> dict:
        pipeline = self.PIPELINES.get(pipeline_name)
        if not pipeline:
            raise ValueError(f"Unknown pipeline: {pipeline_name}")
        
        results = []
        current_params = initial_params.copy()
        
        for step in pipeline["steps"]:
            result = await self._execute_step(step, current_params)
            results.append({
                "step": step["desc"],
                "tool": step["tool"],
                "result": result
            })
            # 将上一步输出作为下一步输入的一部分
            current_params[f"prev_{step['tool']}"] = result
        
        return {"pipeline": pipeline_name, "steps": results}
```

## 5. 安装与部署

### 5.1 一键安装脚本

```bash
#!/bin/bash
# install_ai_toolbox.sh - 本地 AI 教学工具箱安装脚本

echo "=== 安装本地 AI 教学工具箱 ==="

# 1. 检查 Python 环境
python --version || { echo "需要 Python 3.9+"; exit 1; }

# 2. 安装核心依赖
pip install fastapi uvicorn httpx openvino-runtime nncf
pip install paddleocr paddlepaddle  # OCR
pip install openai-whisper           # ASR
pip install edge-tts                 # TTS (备选)
pip install chromadb sentence-transformers  # RAG
pip install pandas plotly            # 数据分析

# 3. 转换模型（OpenVINO 优化）
python scripts/convert_models.py

# 4. 启动所有服务
python services/start_all.py

echo "=== 安装完成 ==="
echo "工具箱地址: http://localhost:8900"
echo "健康检查: http://localhost:8900/api/v1/toolbox/health"
```

### 5.2 Docker 部署（可选）

```yaml
# docker-compose.yml
version: '3.8'
services:
  gateway:
    build: ./gateway
    ports: ["8900:8900"]
    depends_on: [ocr, asr, tts, rag, analysis]
  
  ocr:
    build: ./services/ocr
    ports: ["8901:8901"]
    environment:
      - OPENVINO_DEVICE=GPU
  
  asr:
    build: ./services/asr
    ports: ["8902:8902"]
    environment:
      - OPENVINO_DEVICE=CPU
  
  tts:
    build: ./services/tts
    ports: ["8903:8903"]
  
  rag:
    build: ./services/rag
    ports: ["8904:8904"]
    volumes:
      - ./data/knowledge_base:/app/data
  
  analysis:
    build: ./services/analysis
    ports: ["8905:8905"]
```

## 6. 质量门控

| 检查项 | 标准 | 验证方法 |
|--------|------|----------|
| 工具可用性 | 5 个工具全部在线 | /health 端点检查 |
| 网关延迟 | <100ms（不含推理） | 压力测试 |
| 降级能力 | 单工具离线不影响其他 | 故障注入 |
| 并发支持 | 10 并发请求无错误 | 压力测试 |
| 日志完整 | 每次调用有完整日志 | 日志审计 |
| 安装简便 | 一键脚本 <5 分钟完成 | 安装测试 |
