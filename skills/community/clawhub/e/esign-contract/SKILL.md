---
name: esign-contract
metadata: {"openclaw":{"primaryEnv":"ESIGN_APP_ID"}}
version: 1.0.5
description: >
  e签宝电子签名技能 — 支持 AI 生成任意类型的合同/协议并排版为 PDF，
  上传已有文件发起电子签署，返回签署链接。
  触发场景：用户要求生成、起草、撰写任何类型的合同或协议（如"写个借款合同"、
  "帮我拟一份保密协议"、"起草租赁合同"），或要求对已有合同文件发起签署、
  查询签署进度、撤销签署、下载签署文件、验证电子签名。
  触发词：写合同、生成合同、起草合同、拟合同、合同排版、合同草稿、
  发起签署、电子签名、签署进度、撤销签署、下载签署文件、验签、
  验证签名、签署链接、e签宝、esign
  不触发场景：用户仅询问合同法律条款含义、咨询签署平台选型、或讨论与 e签宝无关的其他电子签名产品。
---

# e签宝电子签名技能

> **编排型 Skill**：本 Skill 统一编排 e签宝电子合同的完整生命周期，涵盖合同生成、文件上传、签署发起、进度查询、撤销、下载及验签六个子流程（流程 A–F）。Agent 根据用户意图选择对应流程执行，各流程间可按需串联。

## 凭证配置

**配置文件路径**：`~/.config/esign-contract/.env`

```ini
ESIGN_APP_ID=your_app_id
ESIGN_APP_SECRET=your_app_secret
ESIGN_BASE_URL=base_url
```

**凭证预检（必须在首次调用 API 前执行）**：调用任何 e签宝 API 之前，先检查 `~/.config/esign-contract/.env` 是否存在且包含 `ESIGN_APP_ID`。若文件不存在或缺少必要字段，提示用户两种方式：

1. **直接输入**（推荐）：请用户在对话中提供 App ID 和 App Secret（格式如 `appId;appSecret`），由 Agent 用 Bash 自动写入配置文件，**默认使用正式环境**：
   ```bash
   mkdir -p ~/.config/esign-contract && cat > ~/.config/esign-contract/.env << 'EOF'
   ESIGN_APP_ID=用户提供的appId
   ESIGN_APP_SECRET=用户提供的appSecret
   ESIGN_BASE_URL=https://openapi.esign.cn
   EOF
   ```
2. **手动配置**：登录 [e签宝开放平台](https://open.esign.cn) 获取凭证，手动编辑 `~/.config/esign-contract/.env`

**环境策略**：默认使用正式环境（`https://openapi.esign.cn`）。若 API 调用返回认证错误或连接失败，询问用户是否为沙箱环境，是则将 `ESIGN_BASE_URL` 改为 `https://smlopenapi.esign.cn`

> 凭证文件存放于用户主目录，不随 Skill 目录变动，不会被意外提交到代码仓库。

## 环境初始化

脚本位于 SKILL.md 所在目录的 `scripts/` 子目录下，执行时使用脚本的完整绝对路径。

**首次执行任何脚本前，必须先确保虚拟环境就绪**（一条命令完成检查与初始化）：
```bash
cd <SKILL目录> && (test -d scripts/.venv || python3 -m venv scripts/.venv) && scripts/.venv/bin/pip install -q -r scripts/requirements.txt
```

**Python 解释器**：始终使用虚拟环境解释器：
- macOS/Linux：`scripts/.venv/bin/python3`
- Windows：`scripts/.venv/Scripts/python.exe`

> 中文 PDF 显示异常时安装 Noto CJK 字体，或放入 `~/.config/esign-contract/`（相对 SKILL.md 目录）。

## 输出规范

- 脚本返回值、JSON 配置、执行命令等技术细节**禁止展示给用户** — 包括但不限于：脚本路径、命令行参数、JSON 响应体、fileId、坐标值。用户只需看到进度提示和最终结果
- **内部流程名称（流程 A/B/C/D/E/F）、步骤编号不展示给用户**
- 每执行一个实际操作前，给出对应的进度提示。只提示实际执行的步骤，不套用固定模板。可选提示：
  - `📋 正在提取签署人信息...`（仅上传文件流程）
  - `📄 正在排版合同...`（仅 AI 生成合同流程）
  - `📤 正在上传...`
  - `🔍 正在定位签章位置...`
  - `✍️ 正在创建签署流程...`
- 最终输出（签署流程发起成功）：
  ```
  ✅ 签署流程已发起 — 合同名称

  ---

  **甲方** 姓名（手机号）
  🔗 签署链接

  ---

  **乙方** 姓名（手机号）
  🔗 签署链接

  ---

  ⏳ 请将对应链接发送给签署方，点击即可完成签署
  ```
- 查询流程输出：
  ```
  📋 签署进度 — 合同名称

  状态：● 签署中　　创建时间：2026年3月27日 14:30

  **甲方** 姓名　✅已签署
  **乙方** 姓名　⏳待签署
  ```
- 撤销流程输出：
  ```
  ⚠️ 签署流程已撤销 — 合同名称
  ```
- 下载文件输出：
  ```
  📥 签署文件已下载 — 合同名称
  📂 保存路径
  ```
- 出错时参考 `references/error-handling.md`
- 多步骤用 `&&` 串联，减少交互轮次

---

## 流程 A：AI 生成合同 → 签署

1. 参考 `references/contract-generation.md` 收集信息并生成合同，记住实际写入的文件路径（写入系统临时目录，如 `/tmp/contract.md`（macOS/Linux）或 `%TEMP%\contract.md`（Windows），可能追加序号）
   > 用户确认合同内容时须确保所有字段已填充，不可带空字段进入排版
2. 排版生成 PDF：`run.py format <实际md路径> <对应pdf路径>`
   - 失败时检查 Markdown 是否含非法字符、字体是否缺失；告知用户错误原因并停止
3. 参考 `references/signing-guide.md` 执行签署（上传实际生成的 PDF → 定位签章 → 发起流程 → 获取链接）
   - 上传失败：提示网络或凭证问题，建议检查 `~/.config/esign-contract/.env` 配置
   - 签章定位失败：提示关键字未找到，请用户确认合同中签章关键字
   - 发起流程失败：展示错误码，参考 `references/error-handling.md`

---

## 流程 B：上传文件 → 签署

1. 提取文本：`run.py extract_text text "<文件路径>"`，识别签署方信息和签章关键字
   - 失败时检查文件格式是否为 PDF/Word，或文件路径是否正确
2. 展示签署方信息让用户确认，缺失必填项要求补充
3. 参考 `references/signing-guide.md` 执行签署（上传 → 关键字定位 → 发起流程 → 获取链接）
   - 上传失败：提示网络或凭证问题，建议检查 `~/.config/esign-contract/.env` 配置
   - 签章定位失败：提示关键字未找到，请用户确认文件中签章关键字
   - 发起流程失败：展示错误码，参考 `references/error-handling.md`

> 签署主体判断规则详见 `references/signing-guide.md`。

---

## 流程 C：查询签署进度

不知道 flowId 时先执行 `run.py list_flows`，再执行 `run.py query_flow "<signFlowId>"`。展示：流程状态、各签署方状态、创建时间。

**签署方信息补全**：API 返回的签署方姓名可能为空（如沙箱环境未注册的手机号）。展示前先用 `run.py list_flows` 读取本地 `flow_history.json`，按手机号匹配补全姓名和角色。

- 查询失败：提示 flowId 不存在或无权限，建议用户确认流程 ID 是否正确。

---

## 流程 D：撤销签署流程

**⚠️ 不可逆操作，必须用户确认。**

确认后：`run.py revoke_flow "<signFlowId>" "撤销原因"`
- 失败时检查流程是否已完成或已撤销（已终态不可再撤销），展示错误码并告知用户。

---

## 流程 E：下载签署完成文件

前提：流程状态为已完成。`run.py download_docs "<signFlowId>"`（不传输出目录时自动使用系统临时目录）
- 失败时检查流程是否尚未完成，或下载路径是否有写权限；提示用户实际原因。

---

## 流程 F：验证电子签名

参考 `references/signing-guide.md` 中的验签步骤。两种方式：提供本地 PDF 文件路径，或指定签署流程获取 fileId。
- 失败时检查文件是否为有效 PDF、flowId 是否存在；若证书过期或签名无效，如实展示结果，不做额外推断。

展示格式：
```
🔍 电子签名验证结果 — 合同名称

📄 文件完整性：✅ 未被篡改 / ❌ 已被修改

签署人：
  1. 名称 — ✅ 签名有效 / ❌ 签名无效
     证书：xxx | 签署时间：xxxx年xx月xx日 xx:xx

> 总结性结论
```

---

## 注意事项

- **发起签署**和**撤销签署**是不可逆操作，必须用户确认
- 所有脚本输出 JSON 格式，便于解析
- `~/.config/esign-contract/.env` 中的凭证切勿泄露或提交到代码仓库
