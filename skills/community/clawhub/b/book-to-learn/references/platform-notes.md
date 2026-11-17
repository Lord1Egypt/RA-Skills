# 平台适配注意事项

> 本 skill 的设计原则：**除「选用的推送渠道」之外，不依赖任何平台**。
> 默认产物落本地目录；只有用户明确选择 IMA / 飞书时，才需要读对应小节。
> 本文件是**可选的适配参考**——核心规则与踩坑已内嵌在 `SKILL.md` 与任务目录的 `GUIDE.md` 里。

## 一、通用（任何平台都适用）

1. **产物落工作目录**：工作目录是持久层，skill 目录只放能力。任务数据/文档都写工作目录。
2. **脚本自定位**：一律 `os.path.dirname(os.path.abspath(__file__))`，不要写死安装路径。
3. **凭据走环境变量**，不写进任何 config/data 文件；报错时提示「可退回 `local`」。
4. **开工先体检**：`python setup_verify.py` 会分别报告
   渲染核心 / 光栅化通道 / CJK 字体 / 破折号兜底字体 / 拆卡引擎 五块。
5. **数据根目录可重定向**：模式 A/B 的数据默认在 `<skill目录>/books/`。若 skill 目录不是持久层
   （容器/沙箱常会重置 `/root`、`~/.<agent>/skills`），用环境变量把数据指到工作目录：
   ```bash
   export B2L_DATA_DIR="$PWD/b2l-data"
   ```
   `book_setup.py` / `push_card.py` / `docs_layer.py` / `fetch_site.py` / `validate.py` 统一读取。
   模式 C（拆卡）的数据本来就在工作目录的任务文件夹里，无需设置。
6. **光栅化优先 PyMuPDF**（`pip install pymupdf`，纯 wheel，无系统库依赖）；
   `pdf2image + poppler` 只作回退。换机器最容易在这里翻车。
7. **中文字体**：Linux 需 `apt-get install -y fonts-noto-cjk`；macOS/Windows 一般自带。
   探测不到时脚本会明确报错，**不要让它静默出方块**。
8. **容器/沙箱类环境**（如各类 agent sandbox）：
   - `/root` 等系统目录常被重置 → 依赖（weasyprint/numpy…）需重装；
   - 把脚本与数据都放**持久化的工作目录**，关键中间产物每轮改完立即验证文件内容；
   - 重置后先重跑 `setup_verify.py` 再继续。
9. **node 环境**：部分沙箱 node 被 bun shim 劫持 → 用 `/usr/bin/node` 并清空 `NODE_OPTIONS`。
10. **临时目录**：`/tmp` 在 Windows 不可用，用平台临时目录（`%TEMP%`）。

## 二、IMA（腾讯 ima.copilot）—— 选用 IMA 推送/归档时才需要

### 1. 装 ima-skill（可选组件）
```bash
cd /tmp && curl -sL -o ima-skills.zip "https://app-dl.ima.qq.com/skills/ima-skills-1.1.7.zip"
mkdir -p ima-skills-extracted && unzip -o ima-skills.zip -d ima-skills-extracted >/dev/null 2>&1
cp -r ima-skills-extracted/ima-skill ~/.codebuddy/skills/ima-skill   # 或 ~/.openclaw / ~/.claude / ~/.agents
```
`upload_ima.py` 会自动在 `~/.codebuddy`、`~/.openclaw`、`~/.claude`、`~/.copilot`、`~/.agents`
下查找 ima-skill；也可用 `IMA_SKILL_DIR` 显式指定。

### 2. 凭据
- 环境变量 `IMA_OPENAPI_CLIENTID` / `IMA_OPENAPI_APIKEY`（**不要落盘**）。
- Key 获取：https://ima.qq.com/agent-interface
- 调用前先列知识库让用户选（`kb_id`），再定位/新建目标文件夹（`folder_id`）。

### 3. 上传与命名
```bash
python3 upload_ima.py --file "<产物>" --config books/<slug>/config.json --book-dir books/<slug>
```
- 退出码：`0`=成功；`2`=密钥失效（已发通知，不计进度并结束）；`1`=其他错误（不更新进度）。
- 拆卡模式归档：把 `out/*.png` + 文本稿一起放进目标文件夹。

### 4. ⚠️ IMA 没有删除接口（必须提前设计好）
- 重推同名文件会被自动加后缀，越堆越多。
- **做法**：重推前先把旧文件**改名**为 `【旧版N-可删除】…` 腾出干净名，再上传新版；
  并**明确告知用户需要手动清理哪些旧文件**（API 删不掉，只能客户端手删）。
- 文件夹同样**不能改名/删除/移动**（只能建），所以命名与层级规划要在建之前想好；
  建错了只能请用户手动清理。

### 5. 长文本写入会被网关（WAF）拦截
- 现象：追加长内容（尤其含表格 `|` 或反斜杠 `\`）时请求被拦截（返回网关验证码页）。
- **做法**：长内容改走「写文件 → 对象存储上传拿 key → 带 key 追加」的路径，避开在 JSON body 里塞长文本；
  或拆小片、避开发力于转义的字符。

### 6. 笔记类操作
- 新建/追加笔记走平台笔记 API；**超长笔记的「读取」会被降级为加工摘要**
  （标注 `[generated, not original text]`），**不要据此判断行数或追加是否成功**；
  核验要导出原文再比对。

### 7. 上传工具的路径约定
- 某些上传工具要求传「相对工作目录」的路径（传绝对路径会被拼接而报不存在）。
- 统一做法：调用前确认该工具的路径约定，**跟随工具文档**，不要想当然。

## 三、飞书（选用飞书渠道时才需要）

- 凭据走环境变量：`FEISHU_APP_ID` / `FEISHU_APP_SECRET` / `FEISHU_CHAT_ID`。
- 两种方式：
  - **Webhook**（`send_feishu.py`）：交互卡片；图片需外链（会用 catbox.moe 图床，失败则降级为文字提示）。
  - **Open API**（`send_feishu_api.py`）：自建应用直发会话，支持**原生图片/文件**，无需图床。
- 应用需开通 `im:message` / `im:message:send_as_bot` / `im:resource`，并把机器人加进目标会话。
- 卡片 header **禁止 emoji**（平台不兼容）。

## 四、仅本地（`pushMethod: local`，默认）

- 产物写在工作目录，不推送、无需任何凭据——**跨平台零依赖**，也是所有渠道失败时的回退方案。

## COS 临时凭据经 argv 传递的已知限制（upload_ima.py）

`cos-upload.cjs`（ima-skill 内置脚本）只接受命令行参数，因此 COS 临时凭据
（secret-key/token，均为**短期临时凭据**）会出现在进程启动参数里，本机其他用户
理论上可通过 `ps` 观察。v1.6.1 已做两层缓解：子进程任何异常（超时/可执行文件缺失）
都不再抛 traceback（原先会把完整 argv 打进错误日志）；错误输出只含异常类型与消息。
若你的运行环境是多用户共享主机，建议改用单用户容器/沙箱，或向 ima-skill 上游
反馈支持环境变量传参。
