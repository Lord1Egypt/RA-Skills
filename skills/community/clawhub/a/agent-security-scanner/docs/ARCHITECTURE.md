# 🏗️ Multi-Agent 系统架构设计

**版本**: v2.0  
**日期**: 2026-03-22  
**状态**: 设计稿

---

## 📐 总体架构

```
┌─────────────────────────────────────────────────────────────────┐
│                        用户接口层                                 │
│  ┌───────────┐  ┌───────────┐  ┌───────────┐  ┌───────────┐    │
│  │   CLI     │  │   Web UI  │  │   API     │  │  SDK      │    │
│  └───────────┘  └───────────┘  └───────────┘  └───────────┘    │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                      Agent 协调层                                 │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │              Orchestrator Agent (协调器)                   │  │
│  │  ┌───────────┐  ┌───────────┐  ┌───────────┐             │  │
│  │  │ 任务解析  │  │ 任务分发  │  │ 结果聚合  │             │  │
│  │  └───────────┘  └───────────┘  └───────────┘             │  │
│  └───────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                      Agent 执行层                                 │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐  │
│  │Detector │ │Analyzer │ │  Rule   │ │  Intel  │ │Reporter │  │
│  │ Agent   │ │ Agent   │ │ Agent   │ │ Agent   │ │ Agent   │  │
│  └─────────┘ └─────────┘ └─────────┘ └─────────┘ └─────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                      通信中间件层                                 │
│  ┌───────────────────┐  ┌───────────────────┐                  │
│  │   消息总线 (Redis) │  │  共享内存 (SQLite) │                  │
│  └───────────────────┘  └───────────────────┘                  │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                      核心引擎层                                   │
│  ┌───────────┐  ┌───────────┐  ┌───────────┐  ┌───────────┐    │
│  │ 扫描引擎  │  │ 匹配引擎  │  │ 分析引擎  │  │ 分类引擎  │    │
│  │ (Rust)    │  │ (L1/L2/L3)│  │ (AST/CFG) │  │ (ML)      │    │
│  └───────────┘  └───────────┘  └───────────┘  └───────────┘    │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                      数据持久层                                   │
│  ┌───────────┐  ┌───────────┐  ┌───────────┐  ┌───────────┐    │
│  │ 规则库    │  │ 样本库    │  │ 情报库    │  │ 知识库    │    │
│  │ 350+ 条   │  │ 850+ 个   │  │ IOC/Threat│  │ Graph     │    │
│  └───────────┘  └───────────┘  └───────────┘  └───────────┘    │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🤖 Agent 设计

### 1. Orchestrator Agent (协调器)

**职责**: 任务协调、结果聚合

**接口**:
```python
class OrchestratorAgent:
    def parse_task(self, request: TaskRequest) -> ParsedTask
    def dispatch_task(self, task: ParsedTask) -> List[AgentAssignment]
    def collect_results(self, assignment: AgentAssignment) -> List[Result]
    def aggregate_results(self, results: List[Result]) -> FinalResult
```

**工作流程**:
```
用户请求 → 任务解析 → 任务分发 → Agent 执行 → 结果收集 → 结果聚合 → 返回用户
```

---

### 2. Detector Agent (检测器)

**职责**: 安全检测、威胁扫描

**接口**:
```python
class DetectorAgent:
    def scan_file(self, file_path: Path) -> ScanResult
    def scan_directory(self, dir_path: Path) -> ScanResult
    def scan_stream(self, stream: IO) -> ScanResult
    def get_statistics(self) -> DetectorStats
```

**能力**:
- L1 快速匹配 (contains/regex)
- L2 指标分析 (IOC/熵值)
- L3 深度检测 (AST/语义)
- 分布式扫描

---

### 3. Analyzer Agent (分析器)

**职责**: 深度代码分析

**接口**:
```python
class AnalyzerAgent:
    def ast_analysis(self, code: str) -> ASTResult
    def semantic_analysis(self, code: str) -> SemanticResult
    def cfg_analysis(self, code: str) -> CFGResult
    def ml_classification(self, code: str) -> MLResult
```

**分析引擎**:
- AST 分析 (混淆检测)
- 语义分析 (变体识别)
- 控制流分析 (CFG)
- ML 分类 (未知威胁)

---

### 4. Rule Agent (规则管理员)

**职责**: 规则生成、优化、验证

**接口**:
```python
class RuleAgent:
    def generate_rule(self, sample: Sample) -> Rule
    def optimize_rule(self, rule: Rule) -> OptimizedRule
    def validate_rule(self, rule: Rule) -> ValidationResult
    def merge_rules(self, rules: List[Rule]) -> MergedRule
```

**功能**:
- AI 辅助规则生成
- 遗传算法优化
- 自动化验证
- 规则去重合并

---

### 5. Intel Agent (情报员)

**职责**: 威胁情报收集分析

**接口**:
```python
class IntelAgent:
    def fetch_threat_intel(self, source: str) -> ThreatIntel
    def extract_ioc(self, report: Report) -> List[IOC]
    def correlate_intel(self, intel_list: List[ThreatIntel]) -> CorrelatedIntel
    def push_update(self, intel: ThreatIntel) -> None
```

**情报源**:
- GitHub 恶意包
- MITRE ATT&CK
- CVE 数据库
- APT 报告

---

### 6. Reporter Agent (报告员)

**职责**: 报告生成、可视化

**接口**:
```python
class ReporterAgent:
    def generate_report(self, results: List[Result], format: str) -> Report
    def create_visualization(self, data: Dict) -> Visualization
    def export_report(self, report: Report, path: Path) -> None
    def summarize_findings(self, results: List[Result]) -> Summary
```

**报告格式**:
- Markdown
- PDF
- HTML
- JSON

---

## 💬 通信协议

### 消息格式

```json
{
  "message_id": "uuid",
  "timestamp": "ISO8601",
  "sender": "orchestrator",
  "receiver": "detector",
  "type": "task_assignment",
  "priority": "high",
  "payload": {
    "task_id": "task-001",
    "action": "scan",
    "target": "/path/to/scan",
    "parameters": {...}
  }
}
```

### 消息类型

| 类型 | 方向 | 说明 |
|------|------|------|
| `task_assignment` | Orchestrator → Agent | 任务分发 |
| `task_result` | Agent → Orchestrator | 结果返回 |
| `agent_status` | Agent → Bus | 状态上报 |
| `broadcast` | Any → All | 广播消息 |
| `request_help` | Agent → Agent | Agent 间协作 |

---

## 🗄️ 数据模型

### 核心实体

```python
@dataclass
class Task:
    id: str
    type: str
    status: str
    created_at: datetime
    updated_at: datetime
    parameters: Dict
    results: List[Result]

@dataclass
class ScanResult:
    file_path: Path
    is_malicious: bool
    confidence: float
    matched_rules: List[Rule]
    severity: str
    details: Dict

@dataclass
class Rule:
    id: str
    name: str
    attack_type: str
    tier: str  # L1/L2/L3
    condition: Dict
    action: str
    severity: str
    version: str

@dataclass
class ThreatIntel:
    id: str
    source: str
    type: str  # IOC/TTP/Malware
    confidence: float
    indicators: List[Indicator]
    created_at: datetime
```

---

## 🔧 技术实现

### Agent 基类

```python
from abc import ABC, abstractmethod
from typing import Any, Dict

class BaseAgent(ABC):
    def __init__(self, agent_id: str, config: Dict):
        self.agent_id = agent_id
        self.config = config
        self.status = "idle"
    
    @abstractmethod
    def execute(self, task: Task) -> Result:
        pass
    
    def update_status(self, status: str):
        self.status = status
        self._publish_status()
    
    def _publish_status(self):
        # 发布状态到消息总线
        pass
    
    def _send_message(self, receiver: str, message: Dict):
        # 发送消息
        pass
    
    def _receive_message(self) -> Dict:
        # 接收消息
        pass
```

### 消息总线

```python
import redis
import json

class MessageBus:
    def __init__(self, redis_url: str):
        self.redis = redis.from_url(redis_url)
        self.pubsub = self.redis.pubsub()
    
    def publish(self, channel: str, message: Dict):
        self.redis.publish(channel, json.dumps(message))
    
    def subscribe(self, channel: str):
        self.pubsub.subscribe(channel)
    
    def listen(self):
        for message in self.pubsub.listen():
            yield json.loads(message['data'])
```

---

## 📊 性能设计

### 并发模型

```
主进程 (Orchestrator)
├── 线程池 (Detector Agents)
│   ├── Worker 1
│   ├── Worker 2
│   └── Worker N
├── 线程池 (Analyzer Agents)
│   ├── Worker 1
│   └── Worker N
└── 异步任务 (Intel/Reporter)
    ├── Intel Task
    └── Reporter Task
```

### 缓存策略

```python
from functools import lru_cache

class DetectorAgent:
    @lru_cache(maxsize=10000)
    def match_rule(self, content_hash: str, rule_id: str) -> bool:
        # 缓存匹配结果
        pass
```

### 批量处理

```python
async def batch_scan(self, files: List[Path], batch_size: int = 100):
    for i in range(0, len(files), batch_size):
        batch = files[i:i+batch_size]
        results = await asyncio.gather(*[self.scan_file(f) for f in batch])
        yield results
```

---

## 🔒 安全设计

### Agent 隔离

- 每个 Agent 运行在独立线程
- 资源限制 (CPU/内存)
- 超时控制
- 异常隔离

### 数据保护

- 敏感数据加密存储
- 通信加密 (TLS)
- 访问控制 (RBAC)
- 审计日志

---

## 📈 扩展性

### 水平扩展

```
Load Balancer
├── Orchestrator 1
│   └── Agent Pool 1
├── Orchestrator 2
│   └── Agent Pool 2
└── Orchestrator N
    └── Agent Pool N
```

### 插件系统

```python
class AgentPlugin:
    def register(self, registry: AgentRegistry):
        registry.register_agent("custom_detector", CustomDetectorAgent)
```

---

## ✅ 实施检查清单

- [ ] 实现 Agent 基类
- [ ] 实现消息总线
- [ ] 实现共享内存
- [ ] 实现 6 个核心 Agent
- [ ] 实现 Orchestrator
- [ ] 实现通信协议
- [ ] 实现数据模型
- [ ] 性能测试
- [ ] 安全审计
- [ ] 文档完善

---

**🏗️ 架构设计完成，开始实现!**
