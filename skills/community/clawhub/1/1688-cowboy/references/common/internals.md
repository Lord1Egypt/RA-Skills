# 内部实现（仅供研发 / 运维参考，Agent 无需读取）

> 本文件记录的全部是部署、签名、埋点等"幕后"细节。
> 这些内容不会出现在与商家的对话里，主 Agent 在执行命令时也不需要理解它们。
> 如果只是想知道某个能力对外行为，请回到 `SKILL.md` 主文件 / `references/capabilities/<command>.md`。

---

## 1. 目录与代码结构

```
1688-cowboy/
├── SKILL.md                       # 主入口，Agent 唯一行为契约
├── cli.py                         # CLI 统一入口，按白名单加载 capability
├── references/
│   ├── capabilities/<cmd>.md      # 每个对外命令的参数 / 接口定义
│   └── common/                    # 通用规则（错误处理 / 内部实现）
└── scripts/
    ├── _auth.py                   # AK 提取 + HMAC-SHA256 签名
    ├── _http.py                   # 网关 POST 封装 + 重试 + 错误映射
    ├── _errors.py                 # SkillError 体系
    ├── _output.py                 # 统一 JSON 输出 {success, markdown, data}
    ├── _tracker.py                # skill 调用埋点
    ├── settings.py                # 配置常量 + 路径 + AK fallback 路径
    └── capabilities/<cmd>/        # 每个 CLI 命令的 cmd.py + service.py
```

`cli.py` 启动时通过 `_discover_capabilities()` 扫描 `scripts/capabilities/<name>/cmd.py`，但只暴露 **白名单** 内的命令。白名单未列入的目录视为历史代码残留，不对外可见。

---

## 2. 命令白名单（与 SKILL.md 命令速查保持一致）

| 命令 | 后端目录 | 上线状态 |
|------|----------|----------|
| `daily_report` | `scripts/capabilities/daily_report/` | ✅ |
| `knowledge_query` | `scripts/capabilities/knowledge_query/` | ✅ |
| `knowledge_answer` | `scripts/capabilities/knowledge_answer/` | ✅ |
| `configure` | `scripts/capabilities/configure/` | ✅ |

> `hire-reception` 是主 Agent 内部流程编排（5 步剧情），不走 CLI，没有对应后端目录。
>
> `quote_*` / `score` / `skill_*` 目录为历史能力残留，不在白名单内，CLI 不会暴露；可在后续清理迭代中删除目录与对应 references。

---

## 3. 网关与签名

- **网关地址**：`https://skills-gateway.1688.com/`（见 `scripts/_http.py` `BASE_URL`）
- **签名算法**：HMAC-SHA256，规范见 `scripts/_auth.py` `build_signature`
- **请求头**：
  - `x-csk-ak` / `x-csk-time` / `x-csk-nonce` / `x-csk-content-md5` / `x-csk-version`
  - `x-csk-sign`（基于 method + content-md5 + content-type + timestamp + 规范化请求头 + 规范化资源路径计算）
- **重试策略**：仅对 `ConnectionError` / `Timeout` / 502 / 504 重试，最多 3 次，指数退避（封顶 10s）
- **错误映射**：401→`AuthError("签名无效")`、429→`RateLimitError("限流")`、400→`ParamError`、其他 5xx→`ServiceError`

---

## 4. AK 读取与 fallback

读取顺序见 `scripts/_auth.py` `get_ak_from_env`：

1. 环境变量 `ALI_1688_AK`（OpenClaw 注入）
2. 配置文件 `${OPENCLAW_CONFIG_DIR:-~/.openclaw}/openclaw.json` 中 `skills.entries["1688-reception-assistant"].apiKey`（Gateway 未重启时 fallback）
3. 都没有 → 返回 `None`，调用方抛 `AuthError("AK 未配置")`

`extract_ak_keys` 约定：原始字符串前 32 位是 `AccessKeySecret`，第 33 位起是 `AccessKeyID`；输入若是 base64url 编码会先解码再切。

---

## 5. 接口路径常量（`scripts/settings.py`）

| 常量 | 路径 |
|------|------|
| `DAILY_REPORT_PATH` | `api/CowboyDailyReport/1.0.0` |
| `KNOWLEDGE_QUERY_PATH` | `api/CowboyKnowledgeQuery/1.0.0` |
| `KNOWLEDGE_ANSWER_PATH` | `api/CowboyKnowledgeAnswer/1.0.0` |

> `SKILL_LIST_PATH` / `SKILL_CREATE_PATH` / `SKILL_TOGGLE_PATH` / `QUOTE_LIST_PATH` / `QUOTE_CONFIRM_PATH` / `SCORE_PATH` 仍保留在常量里以兼容旧脚本，但 CLI 不再暴露对应命令。

---

## 6. 埋点上报（`scripts/_tracker.py`）

- 时机：`cli.py main()` 命令执行完毕后异步触发 `report_skill_usage()`
- 接口：`POST /api/reportSkillsUsage/1.0.0`
- 上报字段：`skillsName=niuzai-receptionist` / `version=settings.SKILL_VERSION` / `scene=CLI` / `channel=${SKILL_CHANNEL:-clawhub}`
- **失败静默**，不影响主流程；只记 `logger.debug`

---

## 7. 环境变量一览

| 变量 | 默认值 | 用途 |
|------|--------|------|
| `ALI_1688_AK` | — | 必需，AK 鉴权（OpenClaw 注入） |
| `OPENCLAW_CONFIG_DIR` | `~/.openclaw` | AK fallback 配置目录 |
| `COWBOY_API_TIMEOUT` | `30` | 网关接口超时秒数 |
| `SKILL_CHANNEL` | `clawhub` | 埋点 channel 字段 |

---

## 8. 输出契约（`scripts/_output.py`）

所有 capability 最终通过统一的 JSON 打印：

```json
{"success": true, "markdown": "...", "data": {...}}
```

- `markdown`：直接给商家看的可读内容
- `data`：结构化字段，供主 Agent 做二次解读 / 分析
- `success=false` 时 `markdown` 必须自带可读错误描述；Agent 处理见 `references/common/error-handling.md`
