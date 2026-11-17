# 云端配置 Schema（藏经阁·易筋 · 方案 C 零密钥）

> 本文档说明 SkillForge 锻造出的技能如何接入藏经阁·易筋云进化，以及**两种配置的严格分离**：
> 一种是随包分发、零密钥、终端用户匿名上传用的 `cloud_config.json`；另一种是**仅存本机、不进包**的创作者 `cloud_open.json`（含审核提案的 token）。

---

## 1. `cloud_config.json`（随包分发 · 零密钥）

每个**云端版**技能包根目录自带，仅含公网 URL，**绝不**含任何 token / 密钥。终端用户零配置即可匿名回传信号。

```json
{
  "ingest_url": "https://<appid>-fpwsv5k3eh.ap-guangzhou.tencentscf.com",
  "register_url": "https://<appid>-1yxx8sqtw1.ap-guangzhou.tencentscf.com"
}
```

| 字段 | 含义 | 必填 |
|------|------|------|
| `ingest_url` | 匿名信号写入端点（`/ingest/anon`，免鉴权公网） | 是 |
| `register_url` | 创作者注册/验证端点（`/register` `/verify` `/status` `/resend`） | 否（缺则走内置默认值） |

**安全红线**：方案 C 已禁止包内明文 token。`forge-publish.py --check` 会校验：若 `cloud_config.json` 含 `token` 字段 → 直接判失败，拒绝发布。

---

## 2. `.deploy/cloud_open.json`（仅本机 · 含 token · 不进包）

由 `scripts/forge-register.py` 在创作者**本机技能目录**的 `.deploy/` 下生成，**发布时经 `.gitignore` 排除，绝不进包**。它持有审核云端提案所需的创作者 `signal_token`。

```json
{
  "email": "252005371@qq.com",
  "signal_token": "<创作者审核 token，仅本机>",
  "register_url": "https://<appid>-1yxx8sqtw1.ap-guangzhou.tencentscf.com",
  "slug": "cjg-skill-forge"
}
```

| 字段 | 含义 |
|------|------|
| `email` | 创作者运营邮箱（收验证码） |
| `signal_token` | 审核提案的鉴权 token（`GET /?slug=` 须校验该 token 持有者是否拥有该 slug，防越权枚举） |
| `register_url` | 注册端点（同 cloud_config） |
| `slug` | 已注册的技能 slug |

**安全边界**：终端用户只接触 `cloud_config.json`（零密钥，只能匿名写信号）；只有创作者本机有 `cloud_open.json`（能读/审提案）。二者物理分离，发布包零密钥。

---

## 3. 注册流程（一键）

在**被注册技能**的目录下运行 `scripts/forge-register.py`：

```bash
cd <你的技能目录>                       # 含 SKILL.md
python <技能锻造炉>/scripts/forge-register.py register   # 发验证码到邮箱
python <技能锻造炉>/scripts/forge-register.py verify <验证码>  # 校验并保存 token
python <技能锻造炉>/scripts/forge-register.py status    # 查看注册/验证态
python <技能锻造炉>/scripts/forge-register.py resend    # 重发验证码
```

- `register` → 调 `register_url/register`（email + 技能 slug）→ 验证码发到邮箱。
- `verify <code>` → 调 `register_url/verify` → 拿到 `signal_token` → 写入 `<技能目录>/.deploy/cloud_open.json`。
- token 仅落本机，发布包不含。

> 注册后，创作者即可在对话中说「看看提案」→ 调 `scripts/cjg-proposal-cli.py list`（带 `.deploy/cloud_open.json` 的 token）查看/审核该 slug 的进化提案。

---

## 4. 端点能力矩阵（后端已部署 · 2026-07-30 闭环）

| 端点 | 方法 | 鉴权 | 说明 |
|------|------|------|------|
| `POST /register` | — | 免 | 建 user_id + 发验证码（cloud 模式） |
| `POST /verify` | — | 免 | 校验验证码签发 `signal_token`；**空码不扣次数**（B2 修复） |
| `POST /status` | — | 免 | 查注册/验证态、剩余次数、是否锁定 |
| `POST /resend` | — | 免 | 重发验证码并重置 `attempts=0` |
| `GET /list?slug=` | GET | **须 token** | 提案列表；无 token → 401（防匿名枚举，B1 已闭环） |
| `POST /approve|/reject` | — | **须 token** | 审核提案（仅创作者） |

> 验证码邮件由 QQ 邮箱（`252005371@qq.com`）经腾讯云 SCF 发出；若收不到，先查 SCF 环境变量是否注入 `QQ_SMTP_PASS`（B3 修复：prod `cjg-register` 已注入）。
