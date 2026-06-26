---
name: dp-pipeline-designer
description: |
  DP 数据处理平台流水线设计师。当用户提到创建管道、数据流、Flink作业、Kafka读取、写到数据库/MongoDB、数据处理管道等需求时激活。
---

# dp-pipeline-designer

## Purpose

Design, generate, submit, and monitor **DP Data Processing Platform** pipelines from natural language descriptions. This skill acts as an AI front-end to the DP platform's REST API, translating user requirements into runnable Apache Flink data pipelines.

The DP platform runs at `${DP_SERVER_URL}` by default.

## Environment Configuration

The DP platform runs at `${DP_SERVER_URL}`.

Required environment variables:
```bash
DP_SERVER_URL=${DP_SERVER_URL}   # REQUIRED — DP platform base URL
DP_API_KEY=${DP_API_KEY}         # REQUIRED — obtain from platform「API Key 管理」page
```

ALL curl commands MUST use `-H 'X-DP-API-Key: ${DP_API_KEY}'`. No other authentication method is supported.

## 首次使用引导

```bash
# 校验 DP_API_KEY — 未配置则终止
if [ -z "${DP_API_KEY}" ]; then
  echo "======================================"
  echo "  DP Platform — API Key 必填"
  echo "======================================"
  echo "错误：未检测到 DP_API_KEY，无法继续。"
  echo ""
  echo "请按以下步骤配置："
  echo "1. 访问 DP 平台控制台：${DP_SERVER_URL}"
  echo "2. 注册账号（如需邀请码请联系管理员）"
  echo "3. 进入「API Key 管理」→「申请新 Key」"
  echo "4. 将生成的 Key 配置到 DP_API_KEY 环境变量"
  echo ""
  echo "免费版：100次/月。超额后需升级订阅套餐。"
  echo "======================================"
  exit 1
fi
echo "API Key 已验证：${DP_API_KEY:0:8}****"
```

## 配额说明

- **免费版**：100 次/月 API 调用额度
- 超额时响应中会包含 `quota_exceeded: true` 字段
- 响应中的 `upgrade_url` 字段指向订阅升级页面
- 升级套餐可获得更多额度：BASIC(1000次)、PRO(10000次)、ENTERPRISE(不限)

## Capabilities

- Ask clarifying questions to understand data source, transformation logic, and output target
- Generate a complete StreamJob XML configuration
- Submit the job via REST API and start execution
- Poll job status and report progress per operator
- Retrieve error logs and suggest root-cause fixes
- Support 4 built-in industry scenario templates

## Context Files

The following files provide the knowledge base for this skill:

| File | Purpose |
|---|---|
| `dp-operator-catalog.json` | Complete list of 60+ operators with params and pipeline templates |
| `dp-api-reference.md` | REST API endpoints, parameters, and curl examples |
| `dp-job-schema.md` | StreamJob XML format, examples, and encoding rules |

## Workflow

### Phase 1: Requirements Gathering

When the user describes a pipeline need, ask ALL of the following if not already specified:

1. **Data Source**: Where does data come from?
2. **Transformations**: What should happen to the data?
3. **Output Target**: Where should results go?
4. **Schedule**: How should the job run?
5. **Resources**: What connections are already configured?

### Phase 2-5: Pipeline Design, XML Generation, Job Submission, Status Monitoring

See full SKILL.md for complete implementation details.

## Limitations & Guardrails

1. **Only use operators listed in `dp-operator-catalog.json`**
2. **Always show the design to the user for confirmation before generating XML**
3. **Do not store passwords in XML files** — use resourceId references
4. **If DP Server is unreachable**, guide user to start services
5. **Parallelism default is 1** for new jobs

---

## License

MIT-0: Free to use, modify, and redistribute. No attribution required.
