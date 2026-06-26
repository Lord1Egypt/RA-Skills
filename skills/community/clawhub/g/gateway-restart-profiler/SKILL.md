---
name: gateway-restart-profiler
description: OpenClaw Gateway 重启性能分析工具。分析 Gateway 重启速度、排查启动慢的原因、生成性能报告、诊断启动问题。支持 Windows (PowerShell) 和 Linux (Bash) 平台。触发场景包括：分析 gateway 重启、检查启动时间、gateway 太慢了、生成性能报告、诊断 gateway 启动问题、Gateway 启动优化、OpenClaw 性能分析。
---

# Gateway Restart Profiler

分析 OpenClaw Gateway 重启时的各阶段耗时，生成性能报告并给出优化建议。

## 支持平台

- **Windows**: PowerShell 5.0+
- **Linux**: Bash 4.0+, 需安装 `bc` 计算器

## 使用方法

### Windows

```powershell
powershell -ExecutionPolicy Bypass -File <skill>/scripts/gateway-profile.ps1
```

### Linux

```bash
bash <skill>/scripts/gateway-profile.sh
```

## 代理调用方式

当用户要求分析 Gateway 重启性能时，OpenClaw 代理应使用以下方式调用：

**Windows：**
```
exec(command="powershell -ExecutionPolicy Bypass -File <skill>/scripts/gateway-profile.ps1", elevated=true)
```

**Linux：**
```
exec(command="bash <skill>/scripts/gateway-profile.sh", elevated=true)
```

其中 `<skill>` 应替换为实际路径，例如：
- Linux: `/home/tstj/.openclaw/workspace/skills/gateway-restart-profiler`
- Windows: `C:\Users\<user>\.openclaw\workspace\skills\gateway-restart-profiler`

代理调用时会自动重启 Gateway（先 stop 再 start），监听日志解析各阶段耗时，生成 HTML 可视化报告和文本摘要。

## 输出内容

1. **实时日志监控** - 高亮显示各启动阶段
2. **HTML 可视化报告** - Chart.js 图表（柱状图 + 饼图）
3. **详细数据表** - 含耗时百分比和可视化进度条
4. **优化建议** - 自动识别超过30秒的阶段并给出建议
5. **文本摘要** - 保存到 temp 目录

## 分析的阶段

| 阶段 | 说明 |
|------|------|
| 配置加载 | 读取 openclaw.json |
| 身份验证 | 连接认证服务 |
| HTTP服务 | 启动 Web 服务 |
| Canvas | Canvas 挂载 |
| MCP服务 | MCP 协议服务 |
| 心跳服务 | 心跳监控 |
| 模型加载 | 加载 AI 模型 |
| 频道启动 | 启动 QQ/Telegram 等频道 |
| 插件系统 | 加载插件 |

## 优化建议解读

| 阶段耗时 | 可能原因 |
|---------|---------|
| 配置加载 > 30s | 配置文件过大或损坏 |
| 身份验证 > 30s | 网络问题或认证服务故障 |
| 模型加载 > 30s | Ollama 响应慢，建议换用 API 模式 |
| 频道启动 > 30s | QQ/Telegram 连接异常 |
| 插件系统 > 30s | npm 依赖缺失，需重新安装 |

## 日志文件位置

- **Windows**: `C:\Users\<user>\AppData\Local\Temp\openclaw\`
- **Linux**: `~/.openclaw/logs/`

## 示例输出

**HTML 报告（用浏览器打开）包含：**
- 📊 **耗时分布饼图** - 各阶段占总耗时比例
- 📈 **横向柱状图** - 按耗时排序，一目了然
- 📋 **详细数据表** - 毫秒/秒/占比/可视化进度条
- 💡 **优化建议** - 超过30秒的阶段高亮提示

**控制台同时输出：**
```
阶段耗时明细 (按耗时降序):
  频道启动           45000ms (45s)   ########################
  模型加载           32000ms (32s)   ################
  配置加载           12000ms (12s)   #########

优化建议:
  - [频道启动] 检查QQ/Telegram连接是否正常
  - [模型加载] Ollama响应慢，考虑换用API模式

[HTML图表报告已保存: ~/.openclaw/logs/gateway-profile-2026-04-12.html]
  → 用浏览器打开 HTML 文件查看可视化图表！
```
