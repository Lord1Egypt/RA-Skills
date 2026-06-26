---
name: dreaming-guard-pro
description: Smart prevention and auto-recovery for OpenClaw dreaming context overflow. Monitors growth trends, archives intelligently, compresses context, protects process memory, and self-heals after crashes. Zero external dependencies.
version: 1.0.0
metadata: { "openclaw": { "emoji": "🛡️" } }
---

# Dreaming Guard Pro

> 防止OpenClaw dreaming文件无限积累导致OOM崩溃的智能保护系统

## 触发词

- `dreaming`
- `context overflow`
- `OOM`
- `crash recovery`
- `memory protection`
- `dreaming guard`
- `健康报告`

## 功能描述

Dreaming Guard Pro 是一个智能保护系统，用于：

1. **实时监控** - 监控dreaming文件增长趋势和内存使用
2. **智能归档** - 三级归档策略（hot/warm/cold），保留有价值数据
3. **自动压缩** - 三级压缩策略（lossless/lossy/aggressive），减少空间占用
4. **进程保护** - 内存阈值分级保护，危险时主动干预
5. **崩溃自愈** - 自动检测崩溃并恢复到最近健康状态
6. **健康报告** - 定期生成可视化状态报告

## 安装

### 作为ClawHub Skill安装

```bash
cd ~/.openclaw/skills
mkdir dreaming-guard
cp -r /root/.openclaw/workspace/projects/dreaming-guard-pro/* dreaming-guard/
```

### 手动安装

```bash
cd projects/dreaming-guard-pro
npm install  # 无需外部依赖，纯Node.js实现
```

## 使用方式

### 作为Skill使用

在对话中使用触发词即可激活：

```
用户: 检查dreaming状态
助手: [调用Dreaming Guard Pro生成健康报告]
```

### 作为模块使用

```javascript
const Guard = require('dreaming-guard-pro/src/guard');

// 创建并启动守护进程
const guard = new Guard({
  loopInterval: 30000,      // 30秒检查一次
  reportInterval: 3600000,  // 1小时生成报告
  enableProtector: true,    // 启用进程保护
  enableHealer: true        // 启用崩溃自愈
});

await guard.start();

// 获取当前状态
const status = guard.getStatus();

// 手动触发动作
await guard.triggerArchive();
await guard.triggerCompress('lossy');

// 生成健康报告
const report = guard.getHealthReport('markdown');

// 停止守护
await guard.stop();
```

### 独立模块使用

```javascript
// 只使用监控器
const Monitor = require('dreaming-guard-pro/src/monitor');
const monitor = new Monitor({ interval: 30000 });
await monitor.start();

// 只使用压缩器
const Compressor = require('dreaming-guard-pro/src/compressor');
const compressor = new Compressor();
await compressor.compress('/path/to/dreams', 'lossy');

// 只使用归档器
const Archiver = require('dreaming-guard-pro/src/archiver');
const archiver = new Archiver();
await archiver.archive({ sourcePath: '/path/to/dreams' });
```

## 配置选项

### 主配置 (Guard)

| 选项 | 默认值 | 说明 |
|------|--------|------|
| `loopInterval` | 30000 | 主循环间隔（毫秒） |
| `reportInterval` | 3600000 | 报告生成间隔（毫秒） |
| `enableProtector` | true | 启用进程保护 |
| `enableHealer` | true | 启用崩溃自愈 |
| `enableReporter` | true | 启用报告生成 |
| `watchPath` | ~/.openclaw/workspace/memory/.dreams | 监控路径 |
| `logLevel` | 'info' | 日志级别 |

### 分析器配置 (Analyzer)

| 选项 | 默认值 | 说明 |
|------|--------|------|
| `thresholds.green` | 524288000 | 安全阈值（500MB） |
| `thresholds.yellow` | 1073741824 | 警告阈值（1GB） |
| `thresholds.red` | 2147483648 | 危险阈值（2GB） |
| `growthRate.low` | 10 | 低增长率阈值（KB/min） |
| `growthRate.medium` | 100 | 中增长率阈值（KB/min） |
| `growthRate.high` | 500 | 高增长率阈值（KB/min） |

### 保护器配置 (Protector)

| 选项 | 默认值 | 说明 |
|------|--------|------|
| `maxMemoryMB` | 512 | 最大内存限制（MB） |
| `thresholds.warning` | 0.70 | 预警阈值（70%） |
| `thresholds.critical` | 0.85 | 严重阈值（85%） |
| `thresholds.emergency` | 0.95 | 紧急阈值（95%） |
| `cooldown` | 60000 | 干预冷却时间（毫秒） |

### 压缩策略 (Compressor)

| 策略 | 减少目标 | 说明 |
|------|----------|------|
| `lossless` | 15% | 无损压缩，去除重复 |
| `lossy` | 40% | 有损压缩，摘要合并 |
| `aggressive` | 70% | 激进压缩，只保留关键 |

### 归档策略 (Archiver)

| 层级 | 保留时间 | 说明 |
|------|----------|------|
| `hot` | 7天内 | 最近数据，快速访问 |
| `warm` | 7-30天 | 中期数据，压缩存储 |
| `cold` | 30天以上 | 历史数据，深度压缩 |

## 报告格式

支持三种格式：

- `text` - 纯文本，适合终端查看
- `json` - JSON格式，适合程序解析
- `markdown` - Markdown格式，适合文档展示

示例报告（text格式）：

```
==================================================
Dreaming Guard Pro - Health Report
Generated: 2026-04-19T12:00:00.000Z
==================================================

[Overall Status]
  Status: HEALTHY
  Health Score: 95/100
  Risk Level: green

[Current State]
  Total Size: 128MB
  Total Files: 42
  Growth Rate: 5 KB/min

[Memory Usage]
  Process RSS: 64MB
  Process Heap: 32/48MB
  System: 2048/8192MB (25%)

[Recommendations]
  - Continue monitoring - system is healthy
  - No immediate action required
```

## 工作流程

主循环每30秒执行一次：

```
Monitor → Analyzer → Decision → Execute
   ↓          ↓          ↓          ↓
 采集数据   分析趋势   决策动作   执行动作
```

动作类型：

- `no_action` - 无需操作
- `notify` - 发送通知
- `archive` - 触发归档
- `compress` - 触发压缩
- `emergency` - 紧急处理（压缩+归档）

## 文件位置

| 文件 | 默认路径 |
|------|----------|
| 配置文件 | ~/.openclaw/dreaming-guard.json |
| 状态文件 | ~/.openclaw/dreaming-guard-state.json |
| 日志文件 | ~/.openclaw/logs/dreaming-guard.log |
| 归档目录 | ~/.openclaw/archive/dreaming/ |
| 健康报告 | ~/.openclaw/logs/health-report-*.log |

## 环境变量

可通过环境变量覆盖配置：

```bash
DREAMING_GUARD_MONITOR_INTERVAL=30000
DREAMING_GUARD_MEMORY_THRESHOLD=512
DREAMING_GUARD_ARCHIVE_PATH=~/.openclaw/archive
DREAMING_GUARD_THRESHOLD_WARNING=524288
DREAMING_GUARD_THRESHOLD_CRITICAL=1048576
DREAMING_GUARD_THRESHOLD_EMERGENCY=2097152
```

## 测试

```bash
cd projects/dreaming-guard-pro
npm test
```

或单独测试Phase 5：

```bash
node test/test-phase5.js
```

## API摘要

### Guard (主入口)

```javascript
guard.start()           // 启动守护
guard.stop()            // 停止守护
guard.getStatus()       // 获取状态
guard.runOnce()         // 执行一次循环
guard.getHealthReport() // 生成报告
guard.triggerAction()   // 手动触发动作
guard.triggerArchive()  // 手动归档
guard.triggerCompress() // 手动压缩
guard.healthCheck()     // 健康检查
```

### Reporter (报告生成)

```javascript
reporter.generate(format)      // 生成报告
reporter.getSummary()          // 获取摘要
reporter.formatReport(data, f) // 格式化数据
reporter.saveReport(report)    // 保存报告
```

## 技术规格

- **语言**: 纯Node.js
- **依赖**: 零外部依赖（仅使用内置模块）
- **兼容**: Node.js >= 16.0.0
- **测试**: 测试运行时间 < 10秒

## License

MIT

---

**开发者**: OpenClaw Community  
**版本**: 1.0.0  
**最后更新**: 2026-04-19