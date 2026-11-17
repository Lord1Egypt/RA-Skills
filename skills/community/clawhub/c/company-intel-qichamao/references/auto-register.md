<!-- request-identity:start -->
**请求身份**：使用已配置的 API Key，并保留本包的 X-Client，携带下列完整身份头；不得沿用其它包的版本或来源。
```text
X-Client: company-intel/1.0.2
X-Skill-Package: company-intel-qichamao/1.0.6
X-Skill-Source: clawhub/dragonzu
```
<!-- request-identity:end -->

# SKILL 自动注册详细流程

> 本文档供 Agent 内 LLM 在**用户首次使用 SKILL 且未主动配置 API Key**时阅读执行。

## 🔒 隐私说明（先读，可原样转述给用户）

- 自动注册**仅**采集 3 项无身份含义的设备特征：`platform`（操作系统类型）、`arch`（CPU 架构）、`mac_hash`（MAC 地址的 SHA256 哈希，**不传输原始 MAC**）。
- 用途单一：免费试用额度的设备去重（防同一设备重复领取），不用于任何其他目的。
- **不采集**：主机名、系统用户名、目录路径、文件内容或任何个人身份信息。
- 完全跳过方式：预先配置 `ZLBX_API_KEY` 环境变量或 `~/.zlbx/config.json`，本流程整体不触发。

## 核心 Gate（执行前必读）

**只有当以下两个条件都不满足时**才进入自动注册流程：

1. 环境变量 `$ZLBX_API_KEY` 已设置
2. 文件 `~/.zlbx/config.json` 存在且其中含 `api_key` 字段

如果上述任何一条命中，**直接使用该 key 并停止阅读本文档**。

**进入自动注册前必须先征得用户同意**（一句话即可，示例）：

> 未检测到 API Key。我帮你自动开通一个免费试用账号？新设备账号通常获赠100积分试用额度（各工具按单价扣除，以注册响应为准）；开通仅采集 3 项非身份设备特征（系统类型/CPU架构/MAC哈希）做试用去重，不采集任何个人信息。

- 用户同意 → 继续步骤 1
- 用户拒绝 → 输出手动注册链接 `https://ai.zhiliaobiaoxun.com/?ch=s116`，本流程终止
- **同意之前不得执行任何采集命令、不得发起任何注册请求**

> 用户主动配过 key（无论环境变量还是 config.json 但 `source` 不是 `"auto"`）时，本 SKILL **不要**输出任何关于自动注册、自动登录、绑定手机号的引导内容。

---

## 步骤 1: 采集 3 项设备特征（隐私最小化）

每项采集失败都 fallback 为空字符串 `""`，**不要中断流程**。

### 1.0 先判定 OS（决定下面用哪一列命令）

- Agent runtime 已知 platform（Python `sys.platform` / Node `process.platform`）→ 直接用
- 否则：尝试 `uname -s`，输出含 `Darwin` → macOS，含 `Linux` → Linux；命令不存在 → Windows

> **`platform` 字段固定写死** `darwin` / `linux` / `win32`（对齐 Node `process.platform`），**不要**直接把 `uname -s` 的 `Darwin`/`Linux` 原样塞进去——大小写漂移会让同机器的 `device_id` 不稳。

### 1.1 字段采集命令

| 字段 | macOS | Linux | Windows | Fallback |
|---|---|---|---|---|
| `platform` | 固定 `"darwin"` | 固定 `"linux"` | 固定 `"win32"` | `""` |
| `arch` | `uname -m` | `uname -m` | PowerShell: `$env:PROCESSOR_ARCHITECTURE` | `""` |
| `mac_hash` | 见 1.2 | 见 1.3 | 见 1.4 | `""` |

> `hostname` / `username` / `home_path` 三个字段**固定传空字符串 `""`**（本 SKILL 出于隐私最小化不采集，服务端兼容空值），**不要执行任何采集它们的命令**。
> mac_hash 一定要做 SHA256 而不是直接传明文 MAC，避免在请求体里暴露原始硬件信息。
> 三平台的 MAC 都先规范化为「去掉 `:` / `-` 分隔符 + 小写 hex」再哈希，否则同机器会算出不同 device_id。

### 1.2 mac_hash · macOS

**不要硬编码 `en0`**（Apple Silicon 上有时是 `en1`，外接网卡又会变）。取第一个有 MAC 的物理接口：

```bash
ifconfig | awk '/ether/{print $2; exit}' \
  | tr -d ':' | tr 'A-Z' 'a-z' \
  | shasum -a 256 | awk '{print $1}'
```

### 1.3 mac_hash · Linux

服务器/容器上通常没有 `ifconfig`，从 `/sys/class/net/` 读最稳，且要跳过 `lo` 与常见虚拟接口（docker/veth/br/tun/tap）：

```bash
iface=$(ls /sys/class/net | grep -vE '^(lo|docker|veth|br-|tun|tap)' | sort | head -n1)
cat "/sys/class/net/$iface/address" 2>/dev/null \
  | tr -d ':-' | tr 'A-Z' 'a-z' \
  | sha256sum | awk '{print $1}'
```

兜底（`/sys` 不可读时）：`ip link show | awk '/link\/ether/{print $2; exit}'` 再做同样的归一化 + `sha256sum`。

### 1.4 mac_hash · Windows (PowerShell)

```powershell
$mac = (Get-NetAdapter | Where-Object { $_.Status -eq 'Up' -and $_.HardwareInterface } |
        Sort-Object ifIndex | Select-Object -First 1).MacAddress
if ($mac) {
  $hex   = ($mac -replace '[-:]', '').ToLower()
  $bytes = [Text.Encoding]::UTF8.GetBytes($hex)
  -join ([Security.Cryptography.SHA256]::Create().ComputeHash($bytes) |
         ForEach-Object { $_.ToString('x2') })
}
```

> `HardwareInterface = $true` 过滤掉虚拟网卡（Hyper-V / WSL / VPN 等），同 Linux 思路保持一致。

---

## 步骤 2: 调用自动注册接口

**请求**：
```
POST https://ai.zhiliaobiaoxun.com/web-api/internal/auto-register
Content-Type: application/json

{
  "device_features": {
    "hostname": "",
    "platform": "darwin",
    "arch": "arm64",
    "username": "",
    "home_path": "",
    "mac_hash": "abc123..."
  },
  "agent_kind": "claude-code",
  "agent_version": "...",
  "skill_version": "matrix-1.0.2",
  "ch": "s116"
}
```

> ### ⚠️ 请求体必须用 JSON 序列化函数生成，不要手拼字符串
>
> 用 `json.dumps(payload)` / `requests.post(url, json=payload)` / `JSON.stringify(payload)`，
> 或 `curl -d @file`；**不要用字符串拼接，也不要用 Python 的 `str(dict)`**
> （后者产出单引号，服务端会报 `Expecting property name enclosed in double quotes`）。
>
> 历史教训：曾有版本采集 `home_path`，Windows 的 `C:\Users\alice` 直接拼进 JSON 字符串时
> `\U` 是非法转义，服务端报 `Invalid \escape`，**该平台用户自动注册全线失败**。
> 现在虽然三项特征都不含反斜杠，手拼仍可能被其它意外字符（引号、换行）破坏——用序列化函数是唯一可靠做法。

> **`ch` 字段说明**：固定填 `"s116"`。**不要从用户环境或动态来源读**。非法值（非 `^[A-Za-z0-9_]{1,16}$`）服务端会静默丢弃，不影响主流程。

**成功响应**：
```json
{
  "success": true,
  "api_key": "zlbx_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
  "remaining_calls": 100,
  "device_id": "abcd1234567890abcdef1234567890ab",
  "is_new": true,
  "message": "设备账号创建成功"
}
```

成功响应里 `is_new` 恒为 `true`：**同设备之前已注册过的情况不会返回成功响应**，而是下面那个 401 `ACCOUNT_RECOVERY_REQUIRED`（2026-09-07 起）。
旧文档里「`is_new=False` 会返回原有 `api_key`」的说法**已作废**，别照它去重试本接口。

**失败响应（429 限流）**：
```json
{ "detail": "自动注册过于频繁，请稍后再试" }
```
此时不要重试，提示用户访问 `https://ai.zhiliaobiaoxun.com/?ch=s116` 手动登录注册。

**失败响应（401 设备已注册）**：
```json
{ "detail": { "code": "ACCOUNT_RECOVERY_REQUIRED", "message": "...", "hint": "..." } }
```
这份设备特征已对应一个已有账号，但本次请求没有可信凭证，服务端无法确认你就是账号主人，
因此**不会**把 api_key 发回来。

处理方式（三条都要照做）：
- **不要重试本接口**；
- **不要改动设备特征再试一次** —— 那不会「换一台机器」，只会建出重复账号；
- 按 `hint` 提示用户：访问 `https://ai.zhiliaobiaoxun.com/?ch=s116` 用手机号登录（新号有赠送额度），
  在「API Key」页复制 Key 写入 `~/.zlbx/config.json` 的 `api_key` 字段。
  注意手机号登录拿到的是该手机号名下的账号，**不会自动接管本机原匿名账号的余额**；
  用户确认原来还有余额的话，引导他联系客服。

> 为什么不能自动取回：设备特征是可复制的，`mac_hash` 取不到时会退化成常量，
> 不同机器会算出同一个 `device_id`。凭它下发密钥等于把别人的账号交出去
> （2026-09-07 修复）。所以拿不到 key 时，正确做法永远是走登录，不是改特征重试。

---

## 步骤 3: 持久化 API Key

把成功响应中的 `api_key` 写入 `~/.zlbx/config.json`：

```json
{
  "api_key": "zlbx_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
  "source": "auto",
  "registered_at": "2026-05-10T10:30:00Z"
}
```

注意事项：
- 目录不存在时先 `mkdir -p ~/.zlbx`
- 文件已存在时**合并而非覆盖**（保留用户可能的其他配置）
- `source: "auto"` 字段必须写入，**这是后续判断「是否输出自动登录链接」的关键依据**

---

## 步骤 4: 当前会话立即生效

写入 config 之后，本次工具调用直接用刚拿到的 `api_key` 作为 `X-API-Key` 继续。**不要让用户重启 agent / 重启会话**。

---

## 余额耗尽时的处理（`QUOTA_EXCEEDED`）

**仅当当前 api_key 是从 `~/.zlbx/config.json` 读取且 `source == "auto"` 时**，按以下流程处理：

1. 调用 `POST https://ai.zhiliaobiaoxun.com/web-api/auth/generate-device-sid`
   - Header: `X-API-Key: <当前 api_key>`
   - Body: 空
2. 拿到响应 `{"sid": "..."}`
3. 输出文案给用户。**链接必须裸写、单独成行、不要用反引号包起来** ——
   包成代码块的话很多终端不会渲染成可点击链接，用户还得手工复制：

> 您的免费额度已用完。点击链接自动登录并充值（首次会引导绑定手机号，**首次符合条件的绑定可再赠100积分（以服务端返回为准）**）：
>
> https://ai.zhiliaobiaoxun.com/auto-login?sid=<sid>
>
> 链接 1 小时内有效。过期了回到这里发送「重新生成充值链接」，我再给你一个新的。

**如果当前 api_key 来自 `$ZLBX_API_KEY`**：跳过 SID 流程，提示用户访问 `https://ai.zhiliaobiaoxun.com/?ch=s116` 手动登录充值。

### 用户说「重新生成充值链接」时

链接有效期只有 1 小时，用户回来要新链接是常规操作。**收到这句话（或「充值链接过期了」
「链接打不开」等同义表达）时，不要再去查余额、也不要等下一次额度报错** ——
只要当前 api_key 来自 `~/.zlbx/config.json` 且 `source == "auto"`，
直接重新执行上面的步骤 1–3，把新链接给他。

---

## 最小化伪代码（供 LLM 思考参考）

```
def get_api_key():
    if os.environ.get("ZLBX_API_KEY"):
        return os.environ["ZLBX_API_KEY"], source="env"
    config = read_json("~/.zlbx/config.json")
    if config and config.get("api_key"):
        return config["api_key"], source=config.get("source", "manual")
    # 自动注册分支
    features = collect_device_features()  # 仅 platform/arch/mac_hash；hostname/username/home_path 恒为 ""
    resp = POST(
        "https://ai.zhiliaobiaoxun.com/web-api/internal/auto-register",
        json={
            "device_features": features,
            "agent_kind": "claude-code",
            "ch": "s116",  # 本包的渠道归因码，构建时注入
        }
    )
    # 先**安全解析一次**：解析失败、或响应根本不是 JSON 对象（网关 HTML 错误页、
    # 204 空响应、顶层是数组）一律当空对象。不这么做的话，一个 502 错误页会让
    # resp.json() 当场抛异常，把真正的失败原因盖掉，报错还指向 JSON 解析。
    body = json_object_or_empty(resp)        # 解析失败 / 不是对象 → {}
    detail = body["detail"] if is_object(body.get("detail")) else {}
    if resp.status == 401 and detail.get("code") == "ACCOUNT_RECOVERY_REQUIRED":
        # 这份特征已对应一个已有账号，服务端无法确认你是不是主人 —— 不重试、不改特征，
        # 照 detail.hint 引导用户取 Key。详见上文「失败响应（401 设备已注册）」。
        show_to_user(detail["hint"])
        return None, source=None
    if resp.status == 400 and detail.get("code") == "DEVICE_FEATURES_UNUSABLE":
        # 本机采集不到可用的设备特征（多半是取不到 MAC），服务端不会拿它建匿名账号 ——
        # 这类特征在不同机器上会算出同一个 device_id，建出来的账号是公共的。
        # 同样不重试、不伪造特征，照 hint 引导用户用手机号开通。
        show_to_user(detail["hint"])
        return None, source=None
    if resp.status == 429:
        show_to_user("自动注册过于频繁，请访问 https://ai.zhiliaobiaoxun.com/?ch=s116 手动注册")
        return None, source=None
    # ⚠️ 成功判据三个条件缺一不可，别只看状态码：
    #   ① HTTP 2xx；② success 严格等于 true（字符串 "false" 是真值，会骗过松散判断）；
    #   ③ api_key 是去掉空白后非空的字符串。
    # 少了这层，任何没预料到的响应（以后新增的错误码、5xx、网关错误页）都会掉进
    # 下面的 write_json，把 None 或空串当成 key 写进配置 —— 之后每次启动都拿着这把
    # 坏 key 去调接口，报错还指向别处。
    api_key = body.get("api_key")
    if not (200 <= resp.status < 300) or body.get("success") is not True \
       or not is_nonempty_string(api_key):
        show_to_user(detail.get("hint") or
                     "自动注册没有成功，请访问 https://ai.zhiliaobiaoxun.com/?ch=s116 获取 Key")
        return None, source=None
    api_key = api_key.strip()
    write_json("~/.zlbx/config.json", {
        "api_key": api_key,
        "source": "auto",
        "registered_at": iso_now(),
    })
    return api_key, source="auto"

def on_balance_exhausted(api_key, source):
    if source == "auto":
        sid = POST(".../generate-device-sid", headers={"X-API-Key": api_key})["sid"]
        print(f"https://ai.zhiliaobiaoxun.com/auto-login?sid={sid}")
    else:
        print("https://ai.zhiliaobiaoxun.com/?ch=s116")
```

<!-- package-identity:start -->
**安装包身份与升级检查**：所有发往知了标讯 API 的请求（包括账户查询）必须额外携带以下两个请求头：
```text
X-Skill-Package: company-intel-qichamao/1.0.6
X-Skill-Source: clawhub/dragonzu
```
这些值是当前安装包的固定身份，复用已有API Key时也要携带；不要用X-Client产品版本替代包版本，不要将Key的注册渠道当作安装来源。
请求鉴权：使用已配置的 API Key，并保留本包的 X-Client。每个会话首次使用本Skill时，在已有凭证可用后先调用免费账户接口 `GET https://mcp-server.zhiliaobiaoxun.com/api_v2/account/balance` 检查升级提醒；该查询不扣积分，不触发购买。
**版本提醒转达**：响应出现 `skill_update_notice` 时，将其中 `message` 原样转达用户；兼容提示只说明检查版本，不能宣称已确认当前包过期。
**展示后确认**：只有将提醒发送到用户可见对话之后，才使用同一凭证和请求头，按 `display_ack` 提交 POST 回执（MCP客户端可调用 `confirm_skill_update_display`）（`notice_id` 和 `displayed: true`）。只读取工具响应、在思考中提过、尚未转达时不得确认。不能在展示后调用接口则不确认，服务端继续保留待提醒状态。回执免费，不扣积分；失败不影响查询结果，不向用户展示技术回执。同一会话同一 `notice_id` 只展示一次。
<!-- package-identity:end -->
