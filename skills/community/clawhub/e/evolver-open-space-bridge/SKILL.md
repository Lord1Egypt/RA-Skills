---
name: evolver-open-space-bridge
description: Bridge Evolver GEP prompts to OpenSpace MCP execute_task for automated execution. Handles path mapping, base64 encoding, timeout circuit breaker, and file readiness detection.
---

# Evolver + OpenSpace Bridge

桥接 Evolver 与 OpenSpace，实现进化任务的自动执行闭环。

## 核心流程

```
Evolver run → GEP prompt → Base64 encode → OpenSpace execute_task → 文件就绪检测 → 返回结果
```

## 使用方法

```bash
# 完整桥接执行
node skills/evolver-open-space-bridge/scripts/bridge.js --prompt memory/evolution/gep_prompt_Cycle_#0035_run_xxx.txt

# 仅测试路径映射
node skills/evolver-open-space-bridge/scripts/path-mapper.js --test

# 仅测试文件就绪检测
node skills/evolver-open-space-bridge/scripts/file-wait.js --path /mnt/c/Users/Admin/.openclaw/workspace/output/test.xlsx
```

## 关键特性

1. **Base64 编码**：GEP prompt 内容 Base64 编码后传入 OpenSpace，避免 JSON 转义问题
2. **路径映射**：自动将 Windows 路径转换为 WSL 可访问的 `/mnt/c/` 路径
3. **超时熔断**：三层超时保护（任务级 180s、总流程 300s、文件等待 120s）
4. **文件就绪检测**：轮询检测输出文件，确保写入完成后再读取

## 配置

- OpenSpace MCP endpoint：默认 `http://127.0.0.1:8081/mcp`
- Session ID：从 initialize 响应头 `mcp-session-id` 获取
- 输出目录：默认 `memory/evolution/openspace_output/`
