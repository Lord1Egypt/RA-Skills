# openFDA API Key — 申请与配置 / Obtaining & Providing an openFDA API Key

> 该 key 是 **可选（optional）** 的。ct-safety 在**无 key** 时也能运行（匿名配额足够低频 / 小样本检索）。只有在**高吞吐**场景下才需要申请。
> / The key is **optional**. ct-safety runs **without** it (anonymous quota covers low-volume use). Apply for one only when you need high throughput.

---

## 1. 何时需要 key / When you need a key

| 模式 | 匿名（无 key） | 持 key |
|---|---|---|
| 速率上限（按**请求次数**，非条数） | 240 次/分钟、1,000 次/天（per IP） | 240 次/分钟、120,000 次/天（per key） |
| 适用场景 | 普通检索、单药信号检测、小样本个案下载（≤10000 条 ≈ 100 次请求，仅占匿名每日上限 ~10%） | 大批量个案翻页下载、并行高并发、超高频检索、CI 自动跑 |

> 经验法则：匿名配额足够 90%+ 的日常使用。只有当单个分析要发 **>1000 次请求/天**，或要 `--parallel` 高并发压测时，才需要 key。
> / Rule of thumb: anonymous quota covers 90%+ of daily use. Only request a key when a single analysis issues **>1,000 requests/day** or runs heavy `--parallel` concurrency.

---

## 2. 如何申请（免费，邮箱即注册）/ How to apply (free, email-only)

1. 打开注册页 / Open the registration page:
   **https://open.fda.gov/api/register/**
2. 填入任意有效邮箱 / Enter any valid email.
3. 收邮件，点击激活链接，页面即显示你的 **API key**（形如一长串字母数字）/ Click the activation link in the email; the page shows your **API key** (a long alphanumeric string).
4. **无需信用卡、无需审核** / No credit card, no review.

官方说明文档 / Official docs: https://open.fda.gov/apis/authentication/

> 与很多商业 API 不同，openFDA 的 key 仅是「提升速率上限」的身份标识，不绑定计费、不限制功能。
> / Unlike many commercial APIs, an openFDA key is only a rate-limit identifier — no billing, no feature gating.

---

## 3. 如何把 key 提供给技能 / How to provide the key

三种方式，**优先级从高到低** / Three ways, **highest priority first**:

### ① 命令行参数（一次性，最直白）/ CLI flag (one-off)
```bash
python scripts/ct_safety.py --drug "osimertinib" --event "PNEUMONITIS" --api-key YOUR_KEY --run --out-dir ./out
```

### ② 环境变量（推荐，跨脚本生效）/ Environment variable (recommended, applies to all scripts)
```bash
export OPENFDA_API_KEY="YOUR_KEY"   # Linux / macOS
# set OPENFDA_API_KEY=YOUR_KEY      # Windows PowerShell
python scripts/ct_safety.py --drug "osimertinib" --event "PNEUMONITIS" --run --out-dir ./out
```
脚本会自动读取 `OPENFDA_API_KEY`，无需每次传 `--api-key`。
/ The scripts auto-read `OPENFDA_API_KEY`; you never pass `--api-key` again.

### ③ 技能根目录 `.env` 文件（持久、不入包）/ Skill-root `.env` (persistent, never shipped)
在技能根目录（即含 `SKILL.md` 的目录）新建 `.env`：
/ Create a `.env` in the skill root (the dir containing `SKILL.md`):
```
OPENFDA_API_KEY=YOUR_KEY
```
该文件已被 `.gitignore` 与 `.clawhubignore` 排除，**不会随技能打包发布**，因此你的 key 不会泄漏。
/ This file is listed in `.gitignore` and `.clawhubignore`, so it is **never included in the published package** — your key cannot leak.
- 可选：`.env` 的值也支持 `obf:` 前缀的 XOR+base64 混淆 blob（混淆非加密，仅防明文被扫描命中），`resolve_api_key` 自动识别解码。 / Optional: the `.env` value may also be an `obf:`-prefixed XOR+base64 obfuscated blob (obfuscation, not encryption — only prevents plaintext from being scanned); the loader auto-detects and decodes.

> 优先级说明：显式 `--api-key` > 环境变量 `OPENFDA_API_KEY` > 技能根 `.env`。三者皆空时退回匿名配额。
> / Priority: explicit `--api-key` > env `OPENFDA_API_KEY` > skill-root `.env`. When all are empty, anonymous quota is used.

---

## 4. 安全红线 / Security red lines

- **不要把 key 写进任何会随技能发布的文件**（脚本、README、示例、`config.json` 等）。用上述 ①②③ 之一提供即可。
  / Never paste the key into any file that ships with the skill (scripts, README, examples, `config.json`). Use ①/②/③ above.
- **打包/发布时不要转移 key**：技能根已配 `.gitignore` + `.clawhubignore`，自动排除 `.env`/`*.key`/`*.secret`/凭证文件。若你手动打包，请确认这些文件未被纳入。
  / **Never transfer a key when packaging**: the skill root ships with `.gitignore` + `.clawhubignore` that exclude `.env`/`*.key`/`*.secret`/credential files. If you package manually, verify these are not included.
- key 仅影响速率上限，不影响数据可得性；丢失 key 不会损坏任何产出，重新申请即可。
  / A key only affects rate limits, not data availability; losing it damages nothing — just re-apply.
