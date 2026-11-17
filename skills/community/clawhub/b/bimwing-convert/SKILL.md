---
name: bimwing-convert
description: 把本地 BIM / 三维模型或图纸（.rvt/.nwd/.ifc/.dwg/.skp/.obj/.fbx 等）上传到 BIMWing（垒知翼）做在线轻量化转换，生成可在浏览器直接在线浏览三维模型的分享链接。除上传外，还支持列出账号下全部模型、查看转码状态、为已有模型生成链接。需要 BIMWing 账号，会将账号密码以明文保存在本机 config.local.json（仅本机、gitignore）以便复用，且仅在你主动提供时保存。支持 API 直连（主）与 Playwright 浏览器自动化（兜底）。
agent_created: true
---

# BIMWing 上传转换 Skill

把用户给的本地 BIM / 三维模型或图纸文件，上传到 BIMWing（https://bimwing.letsgrp.com）做在线轻量化转换，
转换完成后生成可在浏览器里**直接在线浏览三维模型**的分享链接（shareUrl）返回给用户。

## 权限与隐私声明（使用须知）
本 skill 在运行时会用到以下本机能力与资源，请在使用前知悉：
- **读取环境变量**：`BIMWING_MOBILE` / `BIMWING_PASSWORD`（可选，用于提供账号，推荐方式，不落盘）。
- **读写本地文件**：读取你要上传的模型文件；在获得你明确同意后才把 BIMWing 账号密码写入本机 `config.local.json`（仅本机、gitignore，不随 skill 分享）。
- **发起网络请求**：调用 BIMWing 官方 API 完成登录、上传、转码查询、分享。
- **账号级读取**：`list` / `status` / `share <id>` 命令会读取你 BIMWing 账号下的**全部模型**信息，**仅在你明确要求时才执行**，不会默认扫描或枚举你的账号。
- **凭证保存说明（重要）**：BIMWing 目前仅支持「手机号 + 密码」登录，无 OAuth / 第三方授权。因此 skill 会在你**主动授权并确认**后，把账号密码以**明文**存入本机 `config.local.json`（文件权限已设为 `600`，仅当前用户可读写），用于后续复用、免去重复输入。
  - 删除 / 轮换：直接删除 `config.local.json` 即可清除；重新提供账号会覆盖。
  - 风险提示：明文存储存在被本机其他用户、备份或仓库误读的风险，**请勿在共享 / 公共机器上使用**；或改用环境变量方式提供凭证（不落盘，更安全）。

平台会在涉及凭证读取、文件上传、本机配置写入前向你确认。

## 触发场景
- 用户发来一个 BIM/图纸文件（路径或文件），并要求"上传到 BIMWing""转成 BIMWing 链接""生成分享链接"。
- 用户说"把这个模型放到垒知翼 / BIMWing 上转一下"。
- 用户明确要求"列出我的模型""查看模型状态""给某模型出链接"等账号级操作时才执行对应命令。
- 关键词：BIMWing、垒知翼、BIM 看模、在线浏览三维模型、模型轻量化、模型分享链接。

## 前置依赖
- Python 3.10+，安装 `requests`；兜底路径需要 `playwright` 及 chromium。
- 安装：`pip install requests`；浏览器兜底：`pip install playwright && playwright install chromium`

## 凭证配置（重要）
BIMWing 需要登录账号才能上传。凭证**不要写死在代码里**，按以下任一方式提供（优先级从高到低）：
1. 环境变量：`BIMWING_MOBILE`、`BIMWING_PASSWORD`
2. 本 skill 目录下的 `config.local.json`：`{"mobile":"<手机号>","password":"<密码>"}`
   （**gitignore，私有，不随 skill 分享**，仅存于你本机）
3. 本 skill 目录下的 `config.json`：分享模板，默认 `{"mobile":"","password":""}`，**不含真实凭证**，
   可直接随 skill 打包发给别人。

### 分享安全须知（务必遵守）
- **不要把 `config.local.json` 发出去**（已 gitignore）。它含你的真实账号密码。
- 分享时只发 `SKILL.md` + `bimwing_client.py` + `bimwing_browser.py` + 空的 `config.json` + `.gitignore`。
- 接收方首次使用时**不会**拿到你的账号：他们的机器上没有 `config.local.json`、
  `config.json` 是空的，于是会被要求**输入自己的 BIMWing 手机号和密码**（见工作流第 1 步）。

## 工作流（主：API 直连 / 兜底：浏览器自动化）
1. **确认凭证**：调用 `bimwing_client.load_credentials()`。
   - 若返回非空 → 直接用。
   - 若返回空（首次使用 / 分享给别人的机器）：**主动提示注册并索取凭证**：
     1. 先告知注册地址：`https://bimwing.letsgrp.com/sign-in`
        （也可调用 `bimwing_client.register_hint()` 打印）。用 AskUserQuestion 问用户：
        「是否已有 BIMWing 账号？没有的话请先到 <注册地址> 注册，注册完把手机号和密码发我」。
     2. 若用户**没有账号** → 给出注册地址 `https://bimwing.letsgrp.com/sign-in`，
        请其注册完成后再提供手机号和密码；不要继续执行上传。
     3. 若用户**已有账号** → 先明确告知：BIMWing 仅支持手机号+密码登录，
        skill 将把账号密码以**明文**保存在本机 `config.local.json`（权限已设为 `600`，
        仅本机、gitignore），用于后续复用、免去重复输入；并提示风险
        （共享/公共机器勿用、可随时删除该文件清除、或改用环境变量方式不落盘）。
        随后用 AskUserQuestion 索取其 BIMWing 手机号与密码，并在同一问题中请用户
        明确确认「已知悉明文存储风险并同意在本机保存凭证」。
        用户确认后，调用 `bimwing_client.save_credentials(mobile, password)`
        写入对方本机的 `config.local.json`（权限 600，仅本机、gitignore），之后复用，**不再追问**。
        **绝不在用户未确认前保存任何凭证。**
   - 绝不要假设对方用你的账号；绝不要把你的 `config.local.json` 随 skill 一起发。
2. 调用 `bimwing_client.py`：
   - `login()`：POST `/app-api/system/member/auth/login`，
     参数 `{"mobile":..., "password":..., "versionStatus":true}`，
     返回 `accessToken/refreshToken/userId`，后续请求头 `Authorization: Bearer <accessToken>`，
     401 时自动用 `refresh-token?refreshToken=<token>` 刷新。
   - `upload_model(path)`：POST `/app-api/business/model-file/modelUpload`
     （`multipart/form-data`），表单字段（来自前端 model 上传组件逆向）：
       · `files`：文件本体（字段名是 **files**，不是 file）
       · `mainFileName`：主文件名
       · `renderingMode`：渲染方式（默认 4）
       · `outerType`：0=模型
     上传成功时响应 `data` 即模型数字 id（整数），直接用于后续轮询与分享。
   - `wait_conversion(model_id)`：轮询 `GET /app-api/business/model-file/getProgress?id=<id>`
     （返回数字 0~100，100=完成）；同时用 `modelDetail` 的 `coverStatus` 判定失败（3=失败）。
   - `create_share(model_id)`：调用 `GET /app-api/business/model-file-share/get?cipherFileId=<cipher>&add=1`
     确保分享记录存在，然后**本地拼出**分享链接：
     `https://bimwing.letsgrp.com/share-view?shareId=<cipher>&type=<modelType>`
     其中 `cipher = AES-128-ECB(PKCS7, base64)`，密钥固定 `isjdhwngjskdiwjt`，明文=模型数字 id。
   - `make_open_page(share_url, title)`：写出一个**不含 iframe** 的本地 HTML「打开页」
     （一个大按钮，点击即在 WorkBuddy 内置浏览器预览面板打开分享链接），
     返回 HTML 文件路径。CLI 的 `share`/`preview`/上传命令都会自动写出它。
3. 若 API 直连失败（接口变动/字段不符/非预期错误），回退到
   `bimwing_browser.py`：用 Playwright 驱动网页登录→上传→等待转码→点分享→复制链接。
4. **把链接在 WorkBuddy 里打开给用户**：只要产生了分享链接，就调用
   `present_files` 工具传入该 HTML「打开页」路径（或直接传分享 URL），
   让链接以**可点击的卡片**出现在 WorkBuddy 预览面板，用户点一下即可在内置浏览器查看模型。
   不要只把纯文本 URL 丢给用户——必须 present_files 打开，确保「点击即可在 WorkBuddy 打开」。


## 可用命令（CLI 与 agent 调用）
`bimwing_client.py` 支持以下子命令（agent 也可直接调用同名客户端方法）：

- **上传并分享**：`python3 bimwing_client.py <模型文件路径>`
  → 上传 + 等待转码 + 返回分享链接（`convert_and_share`）。
- **列出当前账号模型**：`python3 bimwing_client.py list [页码]`
  → 显示每页（默认 20 个）模型的 id / 文件名 / **转码状态(含实时进度)** / 类型 / 上传时间；
  列表为分页，底部会提示「第 X/Y 页，共 N 个」以及「还有更多，可说第 N 页/下一页」（`list_models` / `format_models`）。
- **为已有模型生成分享链接**：`python3 bimwing_client.py share <模型id>`
  → 返回该模型的查看链接，并写出一个可点击的「打开页」HTML（`create_share` + `make_open_page`）。
- **生成可点击打开页**：`python3 bimwing_client.py preview <模型id>`
  → 仅为已有模型生成「打开页」HTML（不重新上传/转码），方便在 WorkBuddy 里点击打开。
- **查看模型转码状态**：`python3 bimwing_client.py status <模型id>`
  → 返回 id / 文件名 / 状态文本 / 进度% / 类型 / 上传时间（`model_status`）。

典型 agent 用法：
- 用户问"我账号里有哪些模型？" → 调 `list` 或 `format_models(page_no)`，展示第 1 页；
  **若底部提示还有更多页，主动问用户是否看「下一页 / 第 N 页」，或记住当前页处理用户的「下一页」请求**
  （用 `format_models(page_no+1)` / `list 2` 等）。
- 用户问"把某个模型（id=xxx）的链接发我" → 调 `share <id>` 或 `create_share(id)`，再用 `present_files` 打开其「打开页」。
- 用户问"xxx 模型转好了没？" → 调 `status <id>` 或 `model_status(id)`。
- **任何生成链接的场景**：产出后用 `present_files` 打开 HTML「打开页」(或直传 URL)，确保用户能一键在 WorkBuddy 内置浏览器查看。

## 已确认的 API 事实（前端逆向 + 实测验证）
- 根地址：`https://bimwing-api.letsgrp.com`；前端：`https://bimwing.letsgrp.com`
- 登录字段名是 `mobile`（手机号），不是 username。鉴权头：`Authorization: Bearer <token>`。
- 上传：`POST /app-api/business/model-file/modelUpload`（`multipart/form-data`）：
  字段 `files`(文件本体) + `mainFileName`(文件名) + `renderingMode`(默认4) + `outerType`(0=模型)。
  响应 `data` 即模型数字 id（整数）。
  ⚠️ 字段名是 **`files`**（复数），用 `file` 会被服务端 500 拒绝。
- 转码进度：`GET /app-api/business/model-file/getProgress?id=<id>` → 数字 0~100（100=完成）。
- 模型详情：`GET /app-api/business/model-file/modelDetail?id=<id>`（`coverStatus`: 2=可看, 3=失败）。
- 分享：分享记录由 `GET /app-api/business/model-file-share/get?cipherFileId=<cipher>&add=1` 生成；
  分享链接由前端用 `cipher=encrypt(id)` 拼出，**无需服务端返回 URL**。
- `cipher` 加密：AES-128-ECB / PKCS7 / base64，密钥 `isjdhwngjskdiwjt`（与前端 `KMe` 一致）。
  实测：id=12241 → cipher=`1ic6HhsdeSIOAlEe5InLvQ==` → 该 cipher 反查回 fileId=12241，链接 HTTP 200 可公开访问。
- 接口协议通过前端 JS 包逆向 + 运行时实测获得（官方 OpenAPI 仅管理员可见，普通账号无权获取）。
- 实测确认：构造的 `share-view?shareId=<cipher>&type=1` 链接**不跳登录、可直接看模**。

## 调用示例（对用户）
"把这个 /path/to/model.rvt 上传到 BIMWing 并给我分享链接"
→ 执行 `python3 bimwing_client.py /path/to/model.rvt` → 返回 shareUrl。
