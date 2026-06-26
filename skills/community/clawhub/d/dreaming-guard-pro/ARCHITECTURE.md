# OpenClaw Dreaming Guard Pro - 架构设计

> **版本**: v1.0.0
> **日期**: 2026-04-19
> **作者**: 高级架构工程师
> **目标**: 防止dreaming文件无限积累导致OOM崩溃，作为ClawHub skill发布

---

## 目录

1. [问题背景](#问题背景)
2. [架构总览](#架构总览)
3. [模块设计](#模块设计)
4. [数据流](#数据流)
5. [开发计划](#开发计划)
6. [部署方案](#部署方案)

---

## 问题背景

### 当前痛点

OpenClaw的dreaming机制会无限积累上下文文件（`memory/.dreams/`），导致：

| 问题 | 现状 | 影响 |
|------|------|------|
| 无限增长 | 文件大小无上限 | 内存占用持续增加 |
| OOM崩溃 | 进程因内存不足崩溃 | 服务中断，数据丢失 |
| 无预警 | 只有定时检查 | 发现问题时已经太晚 |
| 简单截断 | 丢弃数据 | 丢失有价值的上下文 |
| 无恢复 | 崩溃后手动处理 | 运维成本高 |

### 现有方案局限

```bash
# 现有 dreaming-guard.sh 的局限
- 定时检查（每小时），非实时
- 只看大小，不看增长趋势
- 简单截断，无智能归档
- 无进程保护机制
- 无自愈能力
- 无健康报告
```

### 目标

1. ✅ 实时监控增长趋势
2. ✅ 智能分级归档
3. ✅ 自动降级压缩
4. ✅ 进程保护干预
5. ✅ 崩溃自愈
6. ✅ 可配置策略
7. ✅ 健康报告

---

## 架构总览

### 系统架构图

```
┌─────────────────────────────────────────────────────────────────┐
│                     Dreaming Guard Pro                          │
│                                                                  │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐         │
│  │   Monitor   │───▶│  Analyzer   │───▶│  Decision   │         │
│  │  (监控器)   │    │  (分析器)   │    │  (决策器)   │         │
│  └─────────────┘    └─────────────┘    └──────┬──────┘         │
│         ▲                                      │                │
│         │                    ┌─────────────────┼─────────────┐  │
│         │                    │                 │             │  │
│         │            ┌───────▼──────┐  ┌──────▼──────┐ ┌────▼────┐
│         │            │   Archiver   │  │ Compressor  │ │Protector│
│         │            │  (归档器)    │  │  (压缩器)   │ │(保护器) │
│         │            └──────────────┘  └─────────────┘ └─────────┘
│         │                    │                 │             │
│         │                    └─────────────────┴──────┬──────┘
│         │                                         │
│         │                                    ┌────▼────┐
│         └────────────────────────────────────│ Healer  │
│                                              │(自愈器) │
│                                              └─────────┘
│                                                  │
└──────────────────────────────────────────────────┼──────────────┘
                                                   │
┌──────────────────────────────────────────────────▼──────────────┐
│                        支撑系统                                   │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌─────────────────┐ │
│  │  Config  │  │ Reporter │  │  Logger  │  │  State Manager  │ │
│  │(配置管理)│  │(报告器)  │  │ (日志)   │  │  (状态管理)     │ │
│  └──────────┘  └──────────┘  └──────────┘  └─────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

### 模块清单

| 模块名 | 文件 | 职责 | 代码量估算 |
|--------|------|------|-----------|
| Monitor | `monitor.js` | 实时监控dreaming文件变化 | ~150行 |
| Analyzer | `analyzer.js` | 分析增长趋势，预测风险 | ~200行 |
| Decision | `decision.js` | 决策引擎，触发行动 | ~150行 |
| Archiver | `archiver.js` | 智能归档策略 | ~250行 |
| Compressor | `compressor.js` | 上下文压缩降级 | ~200行 |
| Protector | `protector.js` | 进程保护，内存干预 | ~150行 |
| Healer | `healer.js` | 崩溃检测与自愈 | ~200行 |
| Config | `config.js` | 配置管理 | ~100行 |
| Reporter | `reporter.js` | 健康报告 | ~150行 |
| StateManager | `state.js` | 状态持久化 | ~150行 |
| Logger | `logger.js` | 日志系统 | ~100行 |
| **Index** | `index.js` | 主入口，模块协调 | ~150行 |

**总计**: ~1950行（符合<2000行要求）

---

## 模块设计

### 1. Monitor（监控器）

**文件**: `monitor.js`

#### 职责
实时监控dreaming目录的文件变化，收集原始数据。

#### 输入
```javascript
{
  watchPath: string,      // 监控路径，默认 ~/.openclaw/workspace*/memory/.dreams
  interval: number,       // 轮询间隔（毫秒），默认 5000
  filePatterns: string[]   // 文件匹配模式，默认 ['*.json', '*.jsonl']
}
```

#### 输出
```javascript
{
  timestamp: number,      // 采集时间戳
  files: [{
    path: string,         // 文件路径
    size: number,         // 文件大小（bytes）
    lines: number,        // 行数（jsonl文件）
    entries: number,      // 条目数（json文件）
    modified: number      // 最后修改时间
  }],
  totalSize: number,      // 总大小
  growthRate: number       // 增长速率（bytes/s）
}
```

#### 接口
```javascript
class Monitor {
  constructor(config) {}
  
  // 开始监控
  async start(): Promise<void>
  
  // 停止监控
  async stop(): Promise<void>
  
  // 获取当前状态
  getStatus(): MonitorStatus
  
  // 事件：检测到变化
  // emitter.on('change', (snapshot) => {})
  
  // 事件：达到阈值
  // emitter.on('threshold', (alert) => {})
}
```

#### 依赖
- `chokidar`（可选，用于文件系统事件）
- `events`（Node.js原生）

#### 实现策略
- **优先使用chokidar**：实时监听文件系统事件
- **降级使用轮询**：当chokidar不可用时，使用定时轮询
- **差分计算**：记录上一次状态，计算增长率

#### 复杂度
- **估算**: 3小时
- **风险**: 文件系统事件在不同平台行为可能不一致

---

### 2. Analyzer（分析器）

**文件**: `analyzer.js`

#### 职责
分析监控数据，识别增长模式，预测风险。

#### 输入
```javascript
{
  snapshots: MonitorSnapshot[],  // 监控快照历史
  windowSize: number              // 分析窗口大小，默认60（5分钟）
}
```

#### 输出
```javascript
{
  trend: 'stable' | 'growing' | 'critical',
  predictions: {
    timeToThreshold: number,     // 预计到达阈值的时间（秒）
    estimatedSize: number        // 预计大小
  },
  patterns: [{
    type: 'linear' | 'exponential' | 'burst',
    confidence: number,          // 置信度 0-1
    description: string
  }],
  risk: {
    level: 'low' | 'medium' | 'high' | 'critical',
    score: number,               // 0-100
    factors: string[]             // 风险因素
  }
}
```

#### 接口
```javascript
class Analyzer {
  constructor(config) {}
  
  // 添加快照数据
  addSnapshot(snapshot: MonitorSnapshot): void
  
  // 执行分析
  analyze(): AnalysisResult
  
  // 获取趋势
  getTrend(): Trend
  
  // 预测未来状态
  predict(secondsAhead: number): Prediction
  
  // 重置分析器
  reset(): void
}
```

#### 依赖
- 无外部依赖

#### 实现策略
- **移动平均**：计算短期和长期增长率
- **趋势检测**：线性回归判断增长趋势
- **异常检测**：标准差识别突发增长
- **时间预测**：基于当前增长率预测到达阈值时间

#### 复杂度
- **估算**: 4小时
- **风险**: 预测算法需要调优，避免误报

---

### 3. Decision（决策器）

**文件**: `decision.js`

#### 职责
根据分析结果，决定采取的行动。

#### 输入
```javascript
{
  analysis: AnalysisResult,    // 分析结果
  policies: Policy[],           // 策略配置
  currentState: StateSnapshot   // 当前系统状态
}
```

#### 输出
```javascript
{
  action: 'none' | 'archive' | 'compress' | 'intervene' | 'emergency',
  reason: string,
  params: object,              // 行动参数
  priority: number             // 优先级 0-10
}
```

#### 接口
```javascript
class DecisionEngine {
  constructor(config) {}
  
  // 执行决策
  decide(analysis: AnalysisResult): Decision
  
  // 注册策略
  registerPolicy(policy: Policy): void
  
  // 获取当前策略
  getPolicies(): Policy[]
  
  // 事件：决策触发
  // emitter.on('decision', (decision) => {})
}
```

#### 依赖
- `events`（Node.js原生）

#### 实现策略
- **规则引擎**：基于阈值和优先级的决策树
- **策略可配置**：用户可以自定义策略
- **冷却机制**：避免频繁触发同一行动

#### 复杂度
- **估算**: 3小时
- **风险**: 决策逻辑需要平衡灵敏度和稳定性

---

### 4. Archiver（归档器）

**文件**: `archiver.js`

#### 职责
智能归档dreaming文件，保留有价值数据。

#### 输入
```javascript
{
  sourcePath: string,        // 源目录
  archivePath: string,       // 归档目录
  strategy: ArchiveStrategy, // 归档策略
  dryRun: boolean            // 试运行，不实际执行
}

// ArchiveStrategy
{
  mode: 'time' | 'size' | 'relevance' | 'hybrid',
  retention: {
    keepRecent: number,      // 保留最近N条
    maxAge: number,          // 最大保留天数
    maxSize: number          // 最大归档大小
  },
  compression: 'none' | 'gzip' | 'lz4',
  indexing: boolean          // 是否创建索引
}
```

#### 输出
```javascript
{
  archived: [{
    source: string,          // 原文件路径
    archive: string,         // 归档路径
    size: number,            // 原大小
    compressedSize: number,  // 压缩后大小
    entries: number,         // 归档条目数
    kept: number              // 保留条目数
  }],
  totalSaved: number,        // 节省空间
  indexFile: string          // 索引文件路径
}
```

#### 接口
```javascript
class Archiver {
  constructor(config) {}
  
  // 执行归档
  async archive(options: ArchiveOptions): Promise<ArchiveResult>
  
  // 列出归档
  async listArchives(): Promise<ArchiveInfo[]>
  
  // 恢复归档
  async restore(archivePath: string, targetPath: string): Promise<void>
  
  // 清理过期归档
  async cleanup(): Promise<CleanupResult>
  
  // 搜索归档内容
  async search(query: string): Promise<SearchResult[]>
}
```

#### 依赖
- `archiver`（npm包，用于压缩）
- `fs-extra`（增强文件操作）

#### 实现策略
- **时间归档**：按时间戳分割
- **大小归档**：超过阈值时触发
- **相关性归档**：基于访问频率（需要额外数据）
- **混合策略**：结合多种因素

#### 归档格式
```
archive/
├── dreams-2026-04-19-1.tar.gz
├── dreams-2026-04-19-1.index.json
├── dreams-2026-04-19-2.tar.gz
└── dreams-2026-04-19-2.index.json

// index.json
{
  "archiveFile": "dreams-2026-04-19-1.tar.gz",
  "createdAt": "2026-04-19T10:30:00Z",
  "entries": [
    {"file": "events.jsonl", "lines": 150, "timeRange": ["2026-04-18T...", "2026-04-19T..."]},
    {"file": "short-term-recall.json", "entries": 45}
  ],
  "size": {"original": 102400, "compressed": 20480}
}
```

#### 复杂度
- **估算**: 5小时
- **风险**: 需要确保数据完整性，归档不丢失

---

### 5. Compressor（压缩器）

**文件**: `compressor.js`

#### 职责
压缩上下文，实现降级策略，而非直接丢弃。

#### 输入
```javascript
{
  sourcePath: string,        // 源文件路径
  mode: CompressMode,        // 压缩模式
  targetReduction: number    // 目标减少比例 0-1
}

// CompressMode
'lossless' | 'lossy' | 'aggressive'

// lossless: 只移除冗余（重复条目）
// lossy: 保留关键信息，移除细节
// aggressive: 激进压缩，只保留摘要
```

#### 输出
```javascript
{
  original: {
    size: number,
    entries: number
  },
  compressed: {
    size: number,
    entries: number
  },
  reduction: number,         // 实际减少比例
  method: string,            // 使用的压缩方法
  preserved: string[]        // 保留的关键字段
}
```

#### 接口
```javascript
class Compressor {
  constructor(config) {}
  
  // 压缩文件
  async compress(filePath: string, options: CompressOptions): Promise<CompressResult>
  
  // 分析可压缩性
  analyze(filePath: string): Promise<CompressAnalysis>
  
  // 恢复（从备份）
  async restore(backupPath: string): Promise<void>
  
  // 估算压缩效果
  estimate(filePath: string): Promise<EstimateResult>
}
```

#### 依赖
- 无外部依赖（纯JavaScript实现）

#### 实现策略

**JSONL文件压缩**:
```javascript
// events.jsonl 压缩策略
1. 去重：移除完全相同的条目
2. 时间窗口：合并短时间内相似事件
3. 重要性过滤：保留高重要性事件
```

**JSON文件压缩**:
```javascript
// short-term-recall.json 压缩策略
1. 按访问频率排序
2. 保留高频访问条目
3. 低频条目归档后移除
```

#### 降级流程
```
Level 1 (lossless): 移除重复条目 → 减少 10-20%
    ↓ 还不够？
Level 2 (lossy): 压缩文本内容，移除细节 → 减少 30-50%
    ↓ 还不够？
Level 3 (aggressive): 只保留摘要和关键索引 → 减少 70-90%
```

#### 复杂度
- **估算**: 4小时
- **风险**: 压缩算法需要确保不丢失关键信息

---

### 6. Protector（保护器）

**文件**: `protector.js`

#### 职责
监控进程内存，在危险时主动干预。

#### 输入
```javascript
{
  processName: string,       // 进程名，默认 'openclaw'
  memoryThreshold: number,   // 内存阈值（MB），默认 512
  checkInterval: number,     // 检查间隔（毫秒），默认 10000
  actions: ProtectionAction[]
}

// ProtectionAction
{
  trigger: 'warning' | 'critical' | 'emergency',
  action: 'alert' | 'throttle' | 'compress' | 'restart',
  params: object
}
```

#### 输出
```javascript
{
  timestamp: number,
  memory: {
    used: number,            // 已用内存（MB）
    total: number,           // 总内存（MB）
    percent: number,         // 使用百分比
    trend: 'stable' | 'rising' | 'falling'
  },
  action: ProtectionAction | null,
  message: string
}
```

#### 接口
```javascript
class Protector {
  constructor(config) {}
  
  // 开始保护
  async start(): Promise<void>
  
  // 停止保护
  async stop(): Promise<void>
  
  // 获取内存状态
  getMemoryStatus(): MemoryStatus
  
  // 手动触发干预
  async intervene(action: string): Promise<InterveneResult>
  
  // 事件：内存警告
  // emitter.on('warning', (status) => {})
  // emitter.on('critical', (status) => {})
  // emitter.on('emergency', (status) => {})
}
```

#### 依赖
- `systeminformation`（可选，获取详细系统信息）

#### 实现策略

**内存监控**:
```javascript
// 使用 process.memoryUsage() + os module
const os = require('os');
const usedMemory = os.totalmem() - os.freemem();
const percent = usedMemory / os.totalmem() * 100;
```

**干预策略**:
```
Warning (>70% memory):
  → 记录日志
  → 触发预防性归档

Critical (>85% memory):
  → 发送警报
  → 强制压缩dreaming文件
  → 触发垃圾回收

Emergency (>95% memory):
  → 紧急保存状态
  → 优雅重启OpenClaw进程
```

#### 复杂度
- **估算**: 3小时
- **风险**: 进程重启需要确保数据安全

---

### 7. Healer（自愈器）

**文件**: `healer.js`

#### 职责
检测崩溃，自动恢复到最近健康状态。

#### 输入
```javascript
{
  pidFile: string,           // PID文件路径
  healthCheckInterval: number, // 健康检查间隔（毫秒）
  maxRecoveryAttempts: number, // 最大恢复尝试次数
  recoveryPointPath: string   // 恢复点路径
}
```

#### 输出
```javascript
{
  status: 'healthy' | 'crashed' | 'recovering' | 'failed',
  lastCheck: number,
  lastRecovery: {
    timestamp: number,
    fromArchive: string,     // 从哪个归档恢复
    success: boolean,
    message: string
  }
}
```

#### 接口
```javascript
class Healer {
  constructor(config) {}
  
  // 开始监控
  async start(): Promise<void>
  
  // 停止监控
  async stop(): Promise<void>
  
  // 创建恢复点
  async createRecoveryPoint(): Promise<RecoveryPoint>
  
  // 执行恢复
  async recover(fromPoint?: RecoveryPoint): Promise<RecoveryResult>
  
  // 验证健康
  async healthCheck(): Promise<HealthStatus>
  
  // 事件：崩溃检测
  // emitter.on('crash', (info) => {})
  // emitter.on('recovery', (result) => {})
}
```

#### 依赖
- 无外部依赖

#### 实现策略

**崩溃检测**:
```javascript
// 方法1: PID文件检查
if (!fs.existsSync(pidFile)) { /* 进程停止 */ }

// 方法2: 进程存活检查
try {
  process.kill(pid, 0); // 不发送信号，只检查
} catch (e) {
  // 进程不存在
}
```

**恢复流程**:
```
1. 检测崩溃
2. 记录崩溃信息
3. 从最近恢复点加载状态
4. 恢复dreaming文件
5. 重启进程
6. 验证健康
```

**恢复点管理**:
```
recovery-points/
├── rp-2026-04-19-103000/
│   ├── dreaming-snapshot.tar.gz
│   ├── state.json
│   └── manifest.json
└── rp-2026-04-19-113000/
    └── ...
```

#### 复杂度
- **估算**: 4小时
- **风险**: 恢复点需要定期创建，不能太旧

---

### 8. Config（配置管理）

**文件**: `config.js`

#### 职责
管理用户配置，支持不同策略。

#### 输入
```javascript
// 配置文件: dreaming-guard.config.json
{
  "version": "1.0.0",
  "workspaces": [
    {
      "path": "~/.openclaw/workspace",
      "enabled": true,
      "thresholds": {
        "warning": 524288,    // 512KB
        "critical": 1048576,  // 1MB
        "emergency": 2097152  // 2MB
      }
    }
  ],
  "monitor": {
    "interval": 5000,
    "useFileWatcher": true
  },
  "archive": {
    "path": "~/.openclaw/archive/dreaming",
    "retention": {
      "keepRecent": 100,
      "maxAge": 7,
      "maxSize": 10485760
    },
    "compression": "gzip"
  },
  "protection": {
    "memoryThreshold": 512,
    "actions": {
      "warning": "alert",
      "critical": "compress",
      "emergency": "restart"
    }
  },
  "recovery": {
    "enabled": true,
    "maxAttempts": 3,
    "recoveryPointInterval": 3600000
  },
  "reporter": {
    "interval": 86400000,     // 每天报告一次
    "output": "~/.openclaw/logs/dreaming-health.log"
  }
}
```

#### 输出
```javascript
{
  config: Config,             // 配置对象
  userConfig: UserConfig,     // 用户配置（覆盖默认）
  merged: MergedConfig        // 合并后的配置
}
```

#### 接口
```javascript
class Config {
  constructor(configPath?: string) {}
  
  // 加载配置
  async load(): Promise<ConfigObject>
  
  // 保存配置
  async save(config: ConfigObject): Promise<void>
  
  // 获取配置项
  get(key: string): any
  
  // 设置配置项
  set(key: string, value: any): void
  
  // 验证配置
  validate(config: ConfigObject): ValidationResult
  
  // 重置为默认
  reset(): void
}
```

#### 依赖
- 无外部依赖

#### 复杂度
- **估算**: 2小时
- **风险**: 配置迁移和版本兼容

---

### 9. Reporter（报告器）

**文件**: `reporter.js`

#### 职责
生成健康报告，提供可视化的状态信息。

#### 输入
```javascript
{
  interval: number,          // 报告间隔（毫秒）
  output: string,            // 输出路径
  format: 'text' | 'json' | 'html'
}
```

#### 输出
```javascript
{
  timestamp: number,
  summary: {
    status: 'healthy' | 'warning' | 'critical',
    totalSize: number,
    totalEntries: number,
    growthRate: number,
    prediction: string
  },
  workspaces: [{
    path: string,
    status: string,
    size: number,
    trend: string,
    lastAction: string
  }],
  history: [{
    timestamp: number,
    action: string,
    result: string
  }],
  recommendations: string[]
}
```

#### 接口
```javascript
class Reporter {
  constructor(config) {}
  
  // 生成报告
  async generate(): Promise<Report>
  
  // 启动定期报告
  async start(): Promise<void>
  
  // 停止定期报告
  async stop(): Promise<void>
  
  // 输出到文件
  async writeReport(report: Report, format: string): Promise<void>
  
  // 获取历史报告
  getHistory(limit: number): Report[]
}
```

#### 依赖
- 无外部依赖

#### 报告示例
```
╔════════════════════════════════════════════════════════════╗
║         Dreaming Guard Pro - Health Report                 ║
║         Generated: 2026-04-19 10:30:00                     ║
╠════════════════════════════════════════════════════════════╣
║ Status: ✅ HEALTHY                                          ║
║                                                            ║
║ Workspaces:                                                ║
║ ├─ ~/.openclaw/workspace                                   ║
║ │  └─ Size: 44KB | Growth: +2KB/h | Status: OK             ║
║ ├─ ~/.openclaw/workspace-bilibili                          ║
║ │  └─ Size: 1.8MB | Growth: +50KB/h | Status: ⚠️ WARNING   ║
║ └─ ~/.openclaw/workspace-secretary                         ║
║    └─ Size: 1.1MB | Growth: stable | Status: OK            ║
║                                                            ║
║ Recent Actions:                                            ║
║ ├─ 10:15 - Archived 500KB from bilibili workspace          ║
║ └─ 09:30 - Compressed events.jsonl (20% reduction)         ║
║                                                            ║
║ Predictions:                                               ║
║ └─ bilibili workspace will reach 2MB in ~4 hours          ║
║                                                            ║
║ Recommendations:                                           ║
║ 1. Consider increasing archive frequency for bilibili      ║
║ 2. Review dreaming retention policy (current: 7 days)      ║
╚════════════════════════════════════════════════════════════╝
```

#### 复杂度
- **估算**: 3小时
- **风险**: 无重大风险

---

### 10. StateManager（状态管理器）

**文件**: `state.js`

#### 职责
持久化状态，支持崩溃恢复。

#### 输入
```javascript
{
  statePath: string,         // 状态文件路径
  autoSave: boolean,         // 自动保存
  saveInterval: number       // 保存间隔
}
```

#### 输出
```javascript
{
  lastUpdate: number,
  monitors: Map<string, MonitorState>,
  actions: ActionHistory[],
  recovery: RecoveryInfo
}
```

#### 接口
```javascript
class StateManager {
  constructor(config) {}
  
  // 加载状态
  async load(): Promise<State>
  
  // 保存状态
  async save(): Promise<void>
  
  // 更新状态
  update(key: string, value: any): void
  
  // 获取状态
  get(key: string): any
  
  // 回滚到指定时间点
  async rollback(timestamp: number): Promise<void>
  
  // 获取历史版本
  getHistory(): Promise<StateSnapshot[]>
}
```

#### 依赖
- 无外部依赖

#### 状态文件格式
```json
{
  "version": "1.0.0",
  "lastUpdate": 1713512345678,
  "monitors": {
    "~/.openclaw/workspace": {
      "lastSize": 45056,
      "lastCheck": 1713512345678,
      "growthRate": 0.5,
      "status": "healthy"
    }
  },
  "actions": [
    {
      "timestamp": 1713512300000,
      "type": "archive",
      "target": "workspace-bilibili",
      "result": "success",
      "saved": 512000
    }
  ],
  "recovery": {
    "lastRecoveryPoint": 1713500000000,
    "crashes": 0,
    "successfulRecoveries": 0
  }
}
```

#### 复杂度
- **估算**: 3小时
- **风险**: 需要确保状态文件不损坏

---

### 11. Logger（日志器）

**文件**: `logger.js`

#### 职责
统一日志管理，支持多级别、多输出。

#### 输入
```javascript
{
  level: 'debug' | 'info' | 'warn' | 'error',
  outputs: ('console' | 'file' | 'syslog')[],
  filePath: string,
  maxSize: number,           // 最大文件大小
  maxFiles: number           // 最大文件数
}
```

#### 输出
```javascript
// 日志条目
{
  timestamp: number,
  level: string,
  module: string,
  message: string,
  data: object
}
```

#### 接口
```javascript
class Logger {
  constructor(config) {}
  
  debug(message: string, data?: object): void
  info(message: string, data?: object): void
  warn(message: string, data?: object): void
  error(message: string, data?: object): void
  
  // 创建子logger
  child(module: string): Logger
  
  // 设置级别
  setLevel(level: string): void
}
```

#### 依赖
- 无外部依赖

#### 日志格式
```
[2026-04-19 10:30:00] [INFO] [monitor] Started monitoring workspace directory
[2026-04-19 10:30:05] [DEBUG] [monitor] Size change detected: +2KB
[2026-04-19 10:35:00] [WARN] [analyzer] Growth rate exceeds threshold: +50KB/h
[2026-04-19 10:35:00] [INFO] [decision] Triggering archive action for workspace-bilibili
[2026-04-19 10:35:05] [INFO] [archiver] Archived 500KB to dreams-2026-04-19.tar.gz
```

#### 复杂度
- **估算**: 2小时
- **风险**: 无重大风险

---

### 12. Index（主入口）

**文件**: `index.js`

#### 职责
模块协调，生命周期管理，ClawHub skill接口。

#### 接口
```javascript
class DreamingGuardPro {
  constructor(config?: ConfigObject) {}
  
  // 启动服务
  async start(): Promise<void>
  
  // 停止服务
  async stop(): Promise<void>
  
  // 获取状态
  getStatus(): SystemStatus
  
  // 手动触发归档
  async triggerArchive(workspace?: string): Promise<ArchiveResult>
  
  // 手动触发压缩
  async triggerCompress(workspace?: string): Promise<CompressResult>
  
  // 生成报告
  async generateReport(): Promise<Report>
  
  // 创建恢复点
  async createRecoveryPoint(): Promise<RecoveryPoint>
  
  // 事件
  on(event: string, listener: Function): void
}

// ClawHub skill 导出
module.exports = {
  name: 'dreaming-guard-pro',
  version: '1.0.0',
  description: 'Advanced dreaming context manager for OpenClaw',
  author: 'OpenClaw Community',
  
  // Skill接口
  activate: async (context) => {
    const guard = new DreamingGuardPro(context.config);
    await guard.start();
    return guard;
  },
  
  deactivate: async (guard) => {
    await guard.stop();
  },
  
  // 配置schema
  configSchema: {
    type: 'object',
    properties: {
      // ... 配置定义
    }
  }
};
```

#### 生命周期
```
初始化 → 加载配置 → 初始化模块 → 启动监控 → 运行 → 停止监控 → 清理 → 退出
```

#### 复杂度
- **估算**: 3小时
- **风险**: 需要确保优雅关闭

---

## 数据流

### 正常运行流程

```
┌─────────┐     ┌─────────┐     ┌─────────┐     ┌─────────┐
│ Monitor │────▶│Analyzer │────▶│Decision │────▶│Archiver │
└─────────┘     └─────────┘     └─────────┘     └─────────┘
     │               │               │               │
     │               │               │               │
     ▼               ▼               ▼               ▼
┌─────────────────────────────────────────────────────────┐
│                    State Manager                         │
└─────────────────────────────────────────────────────────┘
     │
     ▼
┌─────────┐
│Reporter │
└─────────┘
```

### 紧急情况流程

```
┌─────────┐     ┌─────────┐     ┌─────────┐
│Protector│────▶│Compressor│────▶│ Healer  │
└─────────┘     └─────────┘     └─────────┘
     │               │               │
     │               │               │
     ▼               ▼               ▼
┌─────────────────────────────────────────────────────────┐
│              Emergency State Save                        │
└─────────────────────────────────────────────────────────┘
```

### 数据流详细

```
1. Monitor 每5秒采集一次快照
   ↓
2. 快照数据存入 StateManager
   ↓
3. Analyzer 分析最近60个快照（5分钟窗口）
   ↓
4. Decision 根据分析结果决定行动
   ↓
5a. 如果需要归档 → Archiver 执行
5b. 如果需要压缩 → Compressor 执行
5c. 如果内存危险 → Protector 干预
5d. 如果崩溃 → Healer 恢复
   ↓
6. 所有行动记录到 StateManager
   ↓
7. Reporter 定期生成报告
```

---

## 开发计划

### 模块依赖关系

```
Level 0 (无依赖):
  ├─ Logger
  ├─ Config
  └─ StateManager

Level 1 (依赖Level 0):
  ├─ Monitor (Config, Logger)
  ├─ Archiver (Config, Logger, StateManager)
  ├─ Compressor (Config, Logger, StateManager)
  ├─ Protector (Config, Logger, StateManager)
  ├─ Healer (Config, Logger, StateManager)
  └─ Reporter (Config, Logger, StateManager)

Level 2 (依赖Level 1):
  ├─ Analyzer (Monitor, Logger)
  └─ Decision (Analyzer, Logger)

Level 3 (依赖Level 2):
  └─ Index (All modules)
```

### 开发顺序

| 阶段 | 模块 | 估算时间 | 累计时间 |
|------|------|----------|----------|
| **Phase 1: 基础设施** | | **7小时** | |
| 1.1 | Logger | 2h | 2h |
| 1.2 | Config | 2h | 4h |
| 1.3 | StateManager | 3h | 7h |
| **Phase 2: 核心功能** | | **12小时** | |
| 2.1 | Monitor | 3h | 10h |
| 2.2 | Archiver | 5h | 15h |
| 2.3 | Compressor | 4h | 19h |
| **Phase 3: 智能分析** | | **7小时** | |
| 3.1 | Analyzer | 4h | 23h |
| 3.2 | Decision | 3h | 26h |
| **Phase 4: 保护机制** | | **7小时** | |
| 4.1 | Protector | 3h | 29h |
| 4.2 | Healer | 4h | 33h |
| **Phase 5: 完善与集成** | | **6小时** | |
| 5.1 | Reporter | 3h | 36h |
| 5.2 | Index | 3h | 39h |
| **Phase 6: 测试与发布** | | **8小时** | |
| 6.1 | 单元测试 | 4h | 43h |
| 6.2 | 集成测试 | 2h | 45h |
| 6.3 | 文档与发布 | 2h | 47h |

**总估算**: 47小时（约6个工作日）

### 里程碑

- **M1 (Day 2)**: 基础设施完成，可以配置和记录日志
- **M2 (Day 4)**: 核心功能完成，可以监控和归档
- **M3 (Day 5)**: 智能分析完成，可以预测和决策
- **M4 (Day 6)**: 保护机制完成，可以保护和自愈
- **M5 (Day 7)**: 集成完成，可以生成报告
- **M6 (Day 8)**: 测试完成，准备发布

---

## 部署方案

### 作为ClawHub skill发布

```
dreaming-guard-pro/
├── package.json
├── README.md
├── SKILL.md                    # ClawHub skill定义
├── config/
│   └── default.config.json     # 默认配置
├── src/
│   ├── index.js                # 主入口
│   ├── monitor.js
│   ├── analyzer.js
│   ├── decision.js
│   ├── archiver.js
│   ├── compressor.js
│   ├── protector.js
│   ├── healer.js
│   ├── config.js
│   ├── reporter.js
│   ├── state.js
│   └── logger.js
├── test/
│   ├── monitor.test.js
│   ├── analyzer.test.js
│   └── integration.test.js
└── scripts/
    ├── install.sh              # 安装脚本
    └── migrate.sh              # 从dreaming-guard.sh迁移
```

### 安装

```bash
# 通过 ClawHub 安装
clawhub install dreaming-guard-pro

# 或手动安装
git clone https://github.com/openclaw/dreaming-guard-pro.git
cd dreaming-guard-pro
npm install
npm link
```

### 配置

```bash
# 复制默认配置
cp config/default.config.json ~/.openclaw/dreaming-guard.config.json

# 编辑配置
vim ~/.openclaw/dreaming-guard.config.json

# 或使用命令行工具
dreaming-guard config set monitor.interval 3000
```

### 运行

```bash
# 作为守护进程运行
dreaming-guard start

# 作为一次性检查运行
dreaming-guard check

# 生成报告
dreaming-guard report

# 手动触发归档
dreaming-guard archive --workspace=bilibili

# 查看状态
dreaming-guard status
```

### 与现有脚本兼容

```bash
# dreaming-guard.sh 可以作为后备方案
# dreaming-guard-pro 会检测并兼容现有归档

# 迁移脚本会导入现有配置
./scripts/migrate.sh
```

---

## 测试策略

### 单元测试

```javascript
// test/monitor.test.js
describe('Monitor', () => {
  it('should detect file changes', async () => {
    const monitor = new Monitor({ interval: 100 });
    const changes = [];
    monitor.on('change', (snapshot) => changes.push(snapshot));
    await monitor.start();
    // 模拟文件变化
    fs.writeFileSync(testFile, 'test');
    await sleep(200);
    expect(changes.length).toBeGreaterThan(0);
    await monitor.stop();
  });
});
```

### 集成测试

```javascript
// test/integration.test.js
describe('DreamingGuardPro', () => {
  it('should archive when threshold exceeded', async () => {
    const guard = new DreamingGuardPro({
      thresholds: { warning: 1024 } // 1KB for test
    });
    await guard.start();
    // 创建大文件
    fs.writeFileSync(testFile, 'x'.repeat(2048));
    await sleep(1000);
    // 验证归档触发
    const status = guard.getStatus();
    expect(status.lastAction.type).toBe('archive');
    await guard.stop();
  });
});
```

### 性能测试

```javascript
// test/performance.test.js
describe('Performance', () => {
  it('should handle 100 workspaces', async () => {
    const workspaces = generateTestWorkspaces(100);
    const guard = new DreamingGuardPro({ workspaces });
    const start = Date.now();
    await guard.start();
    await sleep(5000);
    await guard.stop();
    const elapsed = Date.now() - start;
    expect(elapsed).toBeLessThan(10000); // <10s
  });
});
```

---

## 风险与缓解

| 风险 | 影响 | 缓解措施 |
|------|------|----------|
| 文件系统事件不一致 | 监控可能遗漏 | 使用轮询作为后备方案 |
| 预测算法误报 | 频繁触发行动 | 添加冷却期和阈值缓冲 |
| 归档损坏 | 数据丢失 | 校验归档完整性，保留备份 |
| 进程重启失败 | 服务中断 | 多次重试，保留恢复点 |
| 配置错误 | 功能异常 | 配置验证，默认值保护 |
| 性能影响 | OpenClaw变慢 | 异步操作，节流控制 |
| 跨平台兼容 | Mac/Linux行为不一致 | 平台检测，条件分支 |

---

## 未来扩展

### v2.0 可能的功能

1. **机器学习预测**: 使用ML模型预测增长趋势
2. **分布式支持**: 多节点协调，避免冲突
3. **可视化仪表盘**: Web UI查看状态
4. **外部告警**: 集成邮件、Slack、企业微信
5. **API接口**: 提供REST API供外部调用
6. **插件系统**: 支持自定义归档/压缩策略

---

## 附录

### A. 配置完整示例

见上文 Config 模块部分。

### B. 日志完整格式

见上文 Logger 模块部分。

### C. 报告完整格式

见上文 Reporter 模块部分。

### D. 错误码定义

| 错误码 | 含义 | 处理建议 |
|--------|------|----------|
| E001 | 配置文件不存在 | 创建默认配置 |
| E002 | 配置验证失败 | 检查配置格式 |
| E003 | 监控启动失败 | 检查文件权限 |
| E004 | 归档失败 | 检查磁盘空间 |
| E005 | 压缩失败 | 检查文件格式 |
| E006 | 进程保护失败 | 检查进程权限 |
| E007 | 恢复失败 | 检查恢复点完整性 |
| E008 | 状态文件损坏 | 删除并重建 |

### E. 性能指标

| 指标 | 目标值 | 测试值 |
|------|--------|--------|
| 监控延迟 | <100ms | 待测 |
| 归档速度 | >10MB/s | 待测 |
| 压缩率 | >50% | 待测 |
| 内存占用 | <50MB | 待测 |
| CPU占用 | <5% | 待测 |
| 启动时间 | <2s | 待测 |

---

**文档版本**: 1.0.0
**最后更新**: 2026-04-19
**维护者**: OpenClaw Community