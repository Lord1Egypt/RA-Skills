# 数据存储规范

> 本地数据文件存储位置和格式。当需要操作本地数据时阅读本文件。

---

## 目录结构

### 全局配置（所有 Agent 共享）

```
~/.config/cybersecured/
├── config.json              # API Key、Agent ID、fingerprint
└── policies/                # 保障凭证/电子保单 PDF
```

`config.json` 内容：
```json
{
  "api_key": "cds-aiai-xxx",
  "agents": {
    "codex:v0:32-char-hash": {
      "agent_id": "uuid",
      "framework": "codex",
      "config_path": "/Users/example/.codex/config.toml",
      "machine_id": "os:masked",
      "nickname": "Codex 工作台助手",
      "legacy_fingerprints": ["codex:sha256:32-char-hash"]
    }
  }
}
```

### Agent 专属数据（按工作目录隔离）

```
{workspace_dir}/.cybersecured/
└── {agent_id}/
    ├── agent_info.json
    ├── latest-assessment-result.json
    ├── assessments/
    │   └── {timestamp}/
    │       ├── basic-risk-factors.json
    │       ├── skills.json
    │       ├── plugins.json
    │       ├── security-findings.json
    │       ├── scenarios.json
    │       ├── assets.json
    │       ├── system-basic.json
    │       └── result.json
    ├── applications.json
    ├── policies.json
    └── claims.json
```

## 关键文件说明

| 文件 | 用途 | 读取时机 |
|------|------|---------|
| `applications.json` | 服务申请记录 | 状态查询时 |
| `policies.json` | 保障记录 | 查看保障时 |
| `claims.json` | 事故记录 | 事故信息提交时 |
| `latest-assessment-result.json` | 最新评估结果 | 创建申请时 |

---
