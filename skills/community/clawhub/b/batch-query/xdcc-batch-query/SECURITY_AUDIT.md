# 🔍 安全审计报告 — xdcc-batch-query（v2.0.0 客户版 · 完整闭环）

## 📊 执行摘要
- **审计对象**: `xdcc-batch-query`（`~/.workbuddy/skills/xdcc-batch-query/`）v2.0.0
- **审计时间**: 2026-09-29
- **审计范围**: `scripts/batch_query.py`、`guided_register.py`、`onboard.py`、`get_user_apikey.py`、`common.py`、`selftest.py`、新版 `SKILL.md`
- **发现问题总数**: 0 个风险项（P0=0, P1=0）
  - 📝 信息性提醒: 2 个（均非风险项）
- **安全评分**: 97 / 100

---

## 🔴 P0 阻断级风险发现
✅ 未发现 P0 风险

## ⚠️ P1 需关注风险发现
✅ 未发现 P1 风险

## 📝 信息性提醒（非风险项）
1. **凭据仅从环境变量 / 本地文件读取，无硬编码**
   - `batch_query.py` 读 `XDCC_PLATFORM_ID / XDCC_API_KEY / XDCC_MEMBER_ID`（环境变量）；
   - `guided_register.py` 注册成功后调用 `common.write_creds()` 写入用户显式指定的 `--creds` 路径（默认 `~/.workbuddy/xdcc-credentials.env`）。
   - 文档与代码中均无明文硬编码凭据。
2. **注册向导需客户本人输入手机号/密码**
   - 这是安全注册必需项，由客户在对话中提供或手动在页面填写；脚本**不替客户设定密码**、**不读取客户其他隐私**。
   - 注册的「短信验证码 + 滑块验证」属安全校验，必须由客户本人完成，脚本不绕过。

---

## 📋 详细检查结果

### 命令执行与权限检查
- 发现次数: 0 次（无 `curl|bash`、`os.system`、`subprocess`、`eval`、`sudo`、`chmod`、`rm -rf` 等）。
- 浏览器自动化使用 **Playwright `sync_api`**（本地启动 Chrome），非远程命令执行。
- `SKILL.md` 中代码块均为用户/助手手动复制执行的示例（含占位符），非自动执行。

### 文件操作与敏感路径检查
- 读取: 仅用户显式传入的 `--file` / `--telmap` 输入文件。
- 写入: 仅用户显式指定的 `--output`（批量结果）与 `--creds`（凭据）路径；无系统/用户级敏感路径访问。
- 未发现 `~/.ssh`、`/etc/passwd` 等敏感路径访问。
- 已删除旧 `register_login_helper.py`，避免重复脚本造成混淆。

### 网络请求检查
- 发现 URL（均为官方域名 `api.xdccy.com` / `xdccy.com`）：
  - `https://api.xdccy.com/IsvApi/GetXdccTrackInfoV2` — 批量查询核心接口（POST）
  - `https://api.xdccy.com/UserInfo/GetUserApiKey` — 注册后用 `auth` token 取密钥（POST，浏览器内 fetch 复用页面上下文，失败回退脚本直连）
  - `https://xdccy.com/register.html` / `login.html` — 注册/登录页（仅浏览器打开）
- 上述均为向**官方接口**发起的正常业务请求，无向第三方域名外送数据行为。
- Base64 检测: 仅 `base64.b64encode(md5_hex)` 用于签名生成（合法），无隐藏载荷。

### 远程脚本深度分析
- 无 `curl|bash` / 下载后执行 / 链式下载 → 不适用。

### 依赖安装风险检查
- 零三方依赖：查询引擎（`batch_query.py` / `common.py` / `get_user_apikey.py`）仅用 Python 标准库。
- 注册引导（`guided_register.py` / `onboard.py`）依赖 Playwright，仅在「需要注册」时**懒加载**；缺失时给出明确安装提示（不静默执行 `pip install`）。

---

## 💡 总体建议
- 技能为「标准库查询 + 本地浏览器引导注册」组合，网络仅对接官方 API，凭据局部于用户指定文件，供应链投毒风险极低。
- 可选增强（非必须）：
  - 对 `--output` / `--creds` 增加路径合法性校验（拒绝写入系统目录）；当前路径均用户显式指定，不构成风险。
  - 凭据文件权限建议设为仅当前用户可读（600），可在 `write_creds` 中增强。

---

## 🔧 修复记录（2026-10-02）

首轮审计后复检，修正了 3 项（P1×2、P2×1），均已由 `selftest.py` 新增用例锁死（现 70 项全过）。

1. **P1 — 依赖容错失效**
   `guided_register.py` 原在**模块导入期** `except ImportError: sys.exit(2)`。由于 `SystemExit`
   不继承 `ImportError`，上层 `onboard.py` 的 `except ImportError` 兜底完全失效，缺 Playwright
   时进程直接裸退。改为可用性标志位 + `run()` 运行期返回错误码 2，并复用既有的客服提示出口。
2. **P1 — 硬编码开发机路径**
   删除 `_DEFAULT_CHROME = "C:/Users/86158/..."`（同时泄露了开发机用户名），改为跨平台探测：
   `CHROME_PATH` / `CHROME_BIN` → PATH 查找 → `%LOCALAPPDATA%`、`%ProgramFiles%` / macOS /
   `/usr/bin` 通用路径。
3. **P2 — 文档与实现不符**
   `TEL_REQUIRED` 此前定义后从未使用；`SKILL.md` 宣称的能力实际未落地。现实现
   `guess_shipper_code()` / `find_missing_tel()`，在查询前对必填 Tel 却缺 Tel 的单号中文预警。
   纯数字单号不推断，避免误判。

另清理：`mode_cn` 隐式全局改为显式传参、`threading.Lock()` 死变量移除、CLI/OSSSError 友好报错
（退出码 2，不再抛栈回溯）、`get_user_apikey.py` 对已删脚本的文档引用修正、`inject_banner`
按注册/登录模式输出文案、凭据校验统一到 `common.validate_track_creds()` 消除重复实现、
`write_creds` 在 Unix 下收紧为 600、自检临时目录不再堆积。

> 密级结论不变：仍为 **P2（安全，无投毒风险）**，可安全分发给客户。

## ✅ 审计结论
**风险等级**: **P2 - 安全（无投毒风险）**

**使用建议**: ✅ 可以安全分发给客户使用。兜底提示统一走 `scripts/common.py` 的 `cs_hint()`，只给会话内的三步自助排查（核对凭据键 → `--validate-only` 复核 → 报错原文发回会话），**技能包内不含任何外部联系方式**。

## ✅ 发布合规（外部联系渠道自查）

本技能包已按 WorkBuddy 发布审核要求清理外部联系渠道内容，逐项自查结果：

| 审核项 | 处理前 | 现在 |
|---|---|---|
| 第三方推广 | 无 | 无（页面注入的是无品牌标识的纯操作提示条） |
| 外部联系方式 | 包内硬编码了第三方的即时通讯账号与电子邮箱 | 全部移除，改为会话内三步自助排查 |
| 页面置顶条幅 | 注册页被注入满幅品牌色条带、层级顶格，观感等同推广条幅 | 改为中性浅底轻提示条，无品牌名、无推广动作 |
| 第三方主页地址 | 曾出现在多个文档与首次运行提示中 | 全部移除 |
| 外部站点链接 | 第三方主页地址出现在 SKILL.md / 上手指南 / 首次运行提示 | 全部移除；仅保留代码内必需的 API 基址与注册页地址（功能调用，非推广） |

落地位置：`scripts/common.py`（`cs_hint()`）、`scripts/guided_register.py`（横幅 CSS/HTML）、
`SKILL.md`、`references/onboarding_guide.md`。`scripts/selftest.py` 新增「技能包零外部联系渠道」
静态扫描用例，回归时会拦截上述内容被重新写回。
