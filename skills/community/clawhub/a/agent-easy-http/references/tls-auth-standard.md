# HTTP 类 Skill TLS + 鉴权统一规范 v1.0

适用范围：`agent-easy-http`、`skill-to-http`、`skill-to-http-flash` 三个 HTTP 类 skill。

⚠️ **重要：本规范是「文档 + 代码模板 + 目录约定」三件套**，不是运行时共享代码模块。每个 skill **独立 copy 一份** `scripts/tls_auth.py` 到自己目录使用，避免跨 skill 隐式依赖。

---

## 1. 统一目录约定（K8s 容器友好）

所有 HTTP 类 skill 共用此根目录，存放证书和密钥。

### 路径探测优先级

| 优先级 | 路径 | 适用场景 |
|---|---|---|
| 1 | `$OPENCLAW_HTTP_ROOT`（环境变量） | Docker/K8s 显式指定 |
| 2 | `<workspace>/.http/` | OpenClaw 环境，跟 PVC 持久化（推荐） |
| 3 | `~/.http/` | 非 OpenClaw 环境兜底 |

> ⚠️ K8s Pod 场景下 `~/` 下非 workspace 目录可能不挂 PVC，容器重启会丢密钥。
> 优先级 2 把数据放到 workspace 内，跟着 PVC 一起持久化。

### 目录结构

```
<HTTP_ROOT>/                            # 自动探测的根目录
├── certs/                              # TLS 证书（三 skill 共用）
│   ├── server.crt                      # 自签证书
│   ├── server.key                      # 私钥（权限 0600）
│   └── openssl.cnf                     # 证书生成配置
└── secrets/                            # 鉴权密钥
    ├── api-keys/                       # API Key（各 skill 独立）
    │   ├── agent-easy-http.key         # 0600
    │   ├── skill-to-http.key
    │   └── skill-to-http-flash.key
    ├── agent-easy-http.hmac            # callback HMAC（各 skill 独立）
    ├── skill-to-http.hmac
    └── skill-to-http-flash.hmac
```

**目录权限**：
- 根目录 → 0755
- `secrets/` → 0700
- `secrets/api-keys/` → 0700
- 密钥/私钥文件 → 0600

### 各 skill 自己的数据目录

config.json、jobs.json、PID 文件等**各 skill 独立**：

| 数据 | 路径优先级 |
|---|---|
| skill 数据根 | `$<SKILL>_DATA_ROOT` > `<workspace>/.<skill>/` > `~/.<skill>/` |

例如 agent-easy-http：
- `$AGENT_EASY_HTTP_DATA_ROOT` > `<workspace>/.agent-easy-http/` > `~/.agent-easy-http/`

---

## 2. 配置 schema（YAML/JSON 字段名对齐）

所有三个 skill 的 config.json 中 TLS/鉴权部分字段名必须一致：

```json
{
  "tls_enabled": true,
  "cert_path": "<auto-detected>/certs/server.crt",
  "key_path": "<auto-detected>/certs/server.key",
  "api_key": "<32 位 url-safe 随机串>",
  "api_key_header": "X-API-Key",
  "callback_auth_enabled": true,
  "callback_secret": "<64 位 hex 随机串>",
  "callback_sig_header": "X-Callback-Sig",
  "callback_ts_header": "X-Callback-Ts"
}
```

**字段语义**：

| 字段 | 类型 | 默认值 | 说明 |
|---|---|---|---|
| `tls_enabled` | bool | `true` | 是否启用 HTTPS |
| `cert_path` | str | `<HTTP_ROOT>/certs/server.crt` | 证书绝对路径 |
| `key_path` | str | `<HTTP_ROOT>/certs/server.key` | 私钥绝对路径 |
| `api_key` | str | `""` → **必须 init 时生成** | 外部调用方鉴权 key |
| `api_key_header` | str | `X-API-Key` | 鉴权 header 名 |
| `callback_auth_enabled` | bool | `true` | 是否对回调做 HMAC 鉴权 |
| `callback_secret` | str | `""` → init 自动生成 | HMAC 密钥 |
| `callback_sig_header` | str | `X-Callback-Sig` | 签名 header |
| `callback_ts_header` | str | `X-Callback-Ts` | 时间戳 header（防重放） |

---

## 3. API Key 鉴权

### 协议
- 客户端每次请求带 `X-API-Key: <key>` header
- 服务端校验：不匹配返回 401
- `/health` 端点豁免鉴权（健康检查）
- `/callback/{job_id}` 端点不需要 API Key，但需要 HMAC（见下节）

### Key 生成规则
- 32 位 url-safe 随机字符串
- 用 `secrets.token_urlsafe(24)` 生成（base64 后约 32 字符）
- 持久化到 `~/.http/secrets/api-keys/<skill-name>.key`（0600）
- **用户可随时 `cat` 查回**，不要存内存丢失

### 强制要求
- `api_key` 字段**禁止为空**
- 启动时 `validate_config` 校验失败 → 直接拒绝启动并打印生成方法

---

## 4. Callback HMAC 鉴权

### 为什么需要
`/callback/{job_id}` 是给 agent sub-agent 回填结果用的内部端点。如果不鉴权，任何能访问服务端口的攻击者都能伪造回调注入假数据（job_id 只是 UUID，可被嗅探/枚举）。

### 签名算法
```
signature = HMAC-SHA256(secret, f"{job_id}.{timestamp}")
```
- `secret`：64 位 hex 字符串（`secrets.token_hex(32)`），持久化到 `~/.http/secrets/<skill>.hmac`
- `timestamp`：UNIX 秒级时间戳
- 输出 hex 字符串

### 协议
服务端在给 agent 的 prompt 里嵌入 callback URL + 签名 headers：
```
Headers:
  X-Callback-Sig: <hex signature>
  X-Callback-Ts: <unix timestamp>
```

服务端验证：
- 时间窗口：`abs(now - ts) <= 300s`（防重放）
- 签名：`hmac.compare_digest(expected, received)`
- 失败 → 401 + log warning

### 默认开启
`callback_auth_enabled: true` 是**默认值**，只在「监听 127.0.0.1 + 100% 信任本机」场景下可手动关闭。

---

## 5. TLS 证书规范

### 自签证书生成
- 用 `openssl genrsa + openssl req -x509` 一步到位
- 必须支持 SAN（Subject Alternative Names），通过 `[alt_names]` 段配置
- 默认 SAN 自动包含 `127.0.0.1` + `localhost`
- 用户可通过 `--san 192.168.1.10,myhost.local` 追加 IP/域名

### 有效期
- 默认 825 天（macOS Catalina+ 信任链上限）
- 到期需用户手动重新生成 + 重启服务

### 证书目录
- 共用 `~/.http/certs/`，三个 skill 共享一份证书
- 因为证书是按 SAN 列表绑定，不是按服务绑定

### 客户端信任
- 文档必须给出 curl / Python / 浏览器三种客户端的信任配置方法
- 不建议生产环境上自签证书 → 反代场景应该走 Let's Encrypt（reference 里另列）

---

## 6. 启动前硬校验（`validate_config`）

服务启动时必须做的校验（任一失败即拒绝启动）：

| 校验项 | 错误信息（示例） |
|---|---|
| `api_key` 非空 | "api_key 不能为空。请运行 init wizard 自动生成" |
| `callback_auth_enabled=true` 时 `callback_secret` 非空 | "callback_secret 为空" |
| `tls_enabled=true` 时 cert/key 文件存在 | "证书不存在：{path}，请运行 gen_cert.py" |

---

## 7. init wizard 规范

每个 skill 必须提供 `scripts/init_wizard.py`，引导用户：

1. 选择监听 host/port
2. 选择关联的 OpenClaw session（自动列 `openclaw sessions --json`）
3. 生成或复用 API Key（提示路径让用户可查回）
4. 生成或复用 HMAC secret
5. 引导生成 TLS 证书（自动嗅探本机 IP 作为 SAN 候选）
6. 配置 deny_skills（参考各 skill 自己的推荐清单）

---

## 8. 怎么 copy 到其他 HTTP skill

对 `skill-to-http` 或 `skill-to-http-flash` 做 TLS/鉴权改造时：

```bash
# 1. Copy 三个核心文件
cp ~/.openclaw/workspace/skills/agent-easy-http/scripts/tls_auth.py \
   ~/.openclaw/workspace/skills/<target-skill>/scripts/

cp ~/.openclaw/workspace/skills/agent-easy-http/scripts/gen_cert.py \
   ~/.openclaw/workspace/skills/<target-skill>/scripts/

cp ~/.openclaw/workspace/skills/agent-easy-http/scripts/init_wizard.py \
   ~/.openclaw/workspace/skills/<target-skill>/scripts/

# 2. 在 init_wizard.py 改 SKILL_NAME 常量
sed -i 's/SKILL_NAME = "agent-easy-http"/SKILL_NAME = "<target-skill>"/' \
    ~/.openclaw/workspace/skills/<target-skill>/scripts/init_wizard.py

# 3. 在 server.py 里 import tls_auth 并复用 build_app 模式
#    （参考 agent-easy-http/scripts/server.py）
```

### 不做共享 module 的原因
- 各 skill 装在不同目录，python path 不打通，import 路径不稳定
- skill 更新独立，避免一个改坏全坏
- 用户复制到其它机器时不漏文件

---

## 9. 不在本规范内的事

下列内容由每个 skill 自己决定，不强制统一：

- 业务端点（`/skills`、`/jobs` 等）的路径和 schema
- 并发模型（信号量 / 队列 / 线程池）
- Job 存储后端（内存 / JSON / SQLite）
- Skill 发现机制（静态扫描 / 动态注册）
- 监听端口默认值（agent-easy-http 7720、skill-to-http 7700、flash 7710）

---

## 10. 版本与升级

| 版本 | 日期 | 改动 |
|---|---|---|
| v1.0 | 2026-05-24 | 初版，含 TLS/API Key/HMAC/deny_skills 全套规范 |

升级规则：
- 字段名变更 → 主版本号 +1，提供 migrate 脚本
- 新增字段 → 次版本号 +1，向后兼容
- 仅文档 / 实现细节 → patch 版本号 +1
