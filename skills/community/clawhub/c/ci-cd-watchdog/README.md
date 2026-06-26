# 🐕 CI/CD 流水线智能运维助手 (ci-cd-watchdog)

> 开发者友好型故障诊断引擎 | 日志解析 → 根因定位 → 修复/回滚 → 复盘防复发

## 🎯 功能简介
面向 DevOps 工程师与研发团队，自动解析 CI/CD 失败日志，识别依赖冲突、权限错误、网络超时、配置漂移等高频问题，输出精准修复路径与安全回滚指令。附带 Post-Mortem 草稿与防复发 Checklist，大幅缩短故障恢复时间（MTTR）。

## 🚀 快速开始
### 1. 获取失败日志
- 在流水线控制台复制失败阶段前后 30-50 行关键日志（含时间戳/阶段标识/错误堆栈）
- 敏感信息（Token/密码/内网IP）请提前替换为 `[REDACTED]`

### 2. 配置调用
```json
{
  "skill": "ci_cd_watchdog",
  "inputs": {
    "pipeline_log": "<失败日志片段>",
    "ci_platform": "github",
    "repo_context": "myapp/main/commit_hash"
  }
}
