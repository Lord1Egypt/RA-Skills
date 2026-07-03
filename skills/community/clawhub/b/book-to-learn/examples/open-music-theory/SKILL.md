---
name: omt-daily-push
description: |
  Open Music Theory（开放乐理）每日双语知识点卡片推送。
  当用户提到"推送乐理卡片"、"今日乐理卡片"、"omt 推送"、"音乐理论每日卡片"、
  "open music theory push"，或在定时任务中需要执行每日乐理知识点推送时，使用此 skill。
  每次调用推送一张卡片：取下一张 → 联网核对术语 → 实时翻译 → 生成卡片式 PDF →
  上传到 IMA 知识库「【权威】音乐制作：风格与流派」的「每日一个知识点」文件夹 → 记录进度。
  遇 IMA 密钥失效时，通过飞书 webhook 通知用户索取新密钥，且本次不计入进度。
homepage: https://viva.pressbooks.pub/openmusictheory
metadata:
  openclaw:
    emoji: 🎵
    requires:
      env:
        - IMA_OPENAPI_CLIENTID
        - IMA_OPENAPI_APIKEY
    primaryEnv: IMA_OPENAPI_CLIENTID
  security:
    credentials_usage: |
      本 skill 调用 IMA OpenAPI（ima.qq.com）上传 PDF 到知识库。
      IMA 凭证（Client ID / API Key）存储于 ~/.config/ima/，仅作为 HTTP 头发送给 ima.qq.com。
      COS 上传使用 IMA 返回的临时凭证，发送给 *.myqcloud.com。
      密钥失效时通过飞书 webhook 通知用户，webhook URL 硬编码于 notify_key_expired.py。
      不向其他任何目的地发送凭证。
    allowed_domains:
      - ima.qq.com
      - '*.myqcloud.com'
      - open.feishu.cn
---

# omt-daily-push — 开放乐理每日双语卡片推送

将《Open Music Theory》教材拆解为 118 个知识点卡片，每日推送一张中英双语 PDF 到 IMA 知识库。

## ⛔ 核心规则 — 执行前必读

1. **推送时间不由 skill 决定**：skill 仅在被调用时执行一次推送。何时调用由外部定时任务控制。
2. **进度仅在推送成功后记录**：术语核对、翻译、PDF 生成、IMA 上传任一环节失败，都不更新 progress.json，下次重推同一张卡片。
3. **密钥失效处理**：IMA API 返回认证失败时，调用 notify_key_expired.py 发飞书通知，本次不计入进度，退出。
4. **翻译实时完成**：术语核对必须联网查询权威译法，不得凭记忆；翻译在每次推送时现做。
5. **PDF 文件名必须含当天日期**，统一格式 `OMT_YYYY-MM-DD_<card_id>.pdf`。

## 依赖安装（首次使用前）

### 1. 安装 IMA skill（必需）

本 skill 依赖 ima-skill 进行知识库文件上传。若未安装：

```bash
# 下载并安装 ima-skill
cd /tmp && curl -sL -o ima-skills.zip "https://app-dl.ima.qq.com/skills/ima-skills-1.1.7.zip"
mkdir -p ima-skills-extracted && unzip -o ima-skills.zip -d ima-skills-extracted >/dev/null 2>&1
cp -r ima-skills-extracted/ima-skill /root/.codebuddy/skills/ima-skill
```

API Key 获取：https://ima.qq.com/agent-interface （获取 Client ID 和 API Key）

配置凭证：
```bash
mkdir -p ~/.config/ima
echo "<your_client_id>" > ~/.config/ima/client_id
printf '%s' "<your_api_key>" > ~/.config/ima/api_key
```

### 2. Python 依赖

```bash
# weasyprint 用于生成 PDF（需系统已装 Pango/Cairo，沙箱已预装）
sudo pip3 install weasyprint  # 已预装则跳过
```

### 3. Node.js 环境注意

沙箱中 `node` 可能被 bun shim 劫持（NODE_OPTIONS 指向不存在的模块）。
**所有 node 调用必须用 `/usr/bin/node` 并清除 NODE_OPTIONS**：
```bash
env -u NODE_OPTIONS /usr/bin/node <script>.cjs ...
```
upload_ima.py 已内置此处理。

## 目标配置

| 项目 | 值 |
|------|-----|
| IMA 知识库 | 「【权威】音乐制作：风格与流派」 |
| 目标文件夹 | 「每日一个知识点」 |
| 飞书 webhook（密钥失效通知） | https://open.feishu.cn/open-apis/bot/v2/hook/YOUR_WEBHOOK_TOKEN |

## 推送流程（每次调用执行一次）

SKILL_DIR 为本 skill 所在目录（`/root/.codebuddy/skills/omt-daily-push`）。
所有脚本在 SKILL_DIR 下运行。下面用 `$SD` 代表 SKILL_DIR。

### Step 1：获取下一张卡片载荷

```bash
cd $SD && python3 push_card.py next --force > /tmp/omt_payload.json
```

解析输出 JSON。若含 `"skip": true`：
- `all_done` → 全部 118 张已推送完毕，告知用户并结束
- 其他 → 结束本次

从载荷提取 `nextId`、`terminology` 数组、`coreIdeaEn`、`explanationEn`、`quoteEn`、`applicationScenarios`、`relatedLinks`（对象数组，含 href 与 text 原文标题）。

### Step 2：联网核对术语中文译法

对 `terminology` 数组中每个英文术语，使用联网搜索查询其在**音乐理论领域**的权威中文译法。
检索词示例：`music theory <term> 中文 译名` 或 `<term> 乐理 术语`。
汇总为 `terminologyZh` 对象 `{"英文术语": "中文译法"}`。**必须核对，不可凭记忆。**

### Step 3：实时翻译

将 coreIdeaEn / explanationEn / quoteEn / applicationScenarios 翻译为简体中文：
- explanationEn 按 `\n` 分段翻译，保持段落一一对应
- 专业术语首次出现采用「中文（英文）」格式
- 译文准确专业，符合乐理表达习惯
- **explanationEn / applicationScenarios 中可能含 markdown 链接 `[text](url)`**：翻译时**保留 `[...](url)` 结构和 url 不变**，仅将方括号内的 text 翻译为中文（如 `["How was Musical Notation Invented?"](https://...)` → `[「音乐记谱法是如何发明的？」](https://...)`）；文件格式名 `pdf`/`docx` 等不翻译
- **中文部分必须使用中文引号「」**，禁止英文直引号 `" "`
- 翻译 relatedLinks 的标题为中文
- 翻译 topic（知识点主题）为中文，作为 `topicZh` 字段，用于 PDF 文件名

### Step 4：翻译质量全面检查

在写入 JSON 前，逐项检查：
- ✅ 中文部分是否全部使用中文引号「」，没有英文直引号 `" "`
- ✅ 语义准确、流畅自然，没有生硬机翻
- ✅ markdown 链接结构完整，段落一一对应
- ✅ topicZh 翻译准确，将用于 PDF 文件名
- 发现问题立即修正

### Step 5：写翻译 JSON

将翻译结果写入 `/tmp/omt_zh.json`：
```json
{
  "topicZh": "知识点中文标题",
  "coreIdeaZh": "...",
  "explanationZh": "...(用\n分段,保留[text](url)链接结构)...",
  "quoteZh": "...",
  "applicationZh": "...(保留[text](url)链接结构)...",
  "terminologyZh": {"英文": "中文", ...},
  "relatedLinksZh": [
    {"href": "https://...", "textEn": "English Title", "textZh": "中文标题"},
    ...
  ],
  "note": "术语核对要点说明"
}
```

### Step 6：生成卡片式 PDF

```bash
cd $SD && python3 gen_card_pdf.py --payload /tmp/omt_payload.json --zh /tmp/omt_zh.json
```
从输出中提取生成的 PDF 路径（pdf 字段），保存为 PDF_PATH 变量。

PDF 规格：A4、卡片式设计、大字号（中文正文 18px、英文 15px、标题 25px）、中英对照（标题区中文在上、英文小字在下）、术语表、跨平台中文字体。
文件名格式：`OMT_YYYY-MM-DD_<card_id>_<中文名>.pdf`（如 `OMT_2026-06-29_ch01-01_西方音乐记谱法导论.pdf`）。

### Step 7：上传主 PDF 到 IMA 知识库

```bash
cd $SD && python3 upload_ima.py --file "$PDF_PATH"
```

脚本自动：定位知识库「【权威】音乐制作：风格与流派」→ 定位文件夹「每日一个知识点」→
preflight 检查 → 重名检查 → create_media → COS 上传 → add_knowledge。

**退出码含义**：
- `0` → 上传成功，继续下一步
- `1` → 其他错误（已输出错误详情），不更新进度，报告错误后结束
- `2` → **IMA 密钥失效**（已自动发飞书通知），本次不计进度，告知用户后结束

### Step 8：记录推送进度（仅上传成功后）

```bash
cd $SD && python3 push_card.py mark <nextId> success
```

### Step 9：更新 daily-progress.md 进度文件

追加当天推送记录到 `daily-progress.md`。

### Step 10：汇报

简短汇报：今日推送第 X/118 张、卡片主题、术语核对要点、PDF 已上传至 IMA 知识库。

## 辅助命令

- 查看进度：`cd $SD && python3 push_card.py status`
- 手动重推某张：`python3 push_card.py next --force`
- 重置进度：编辑 progress.json，lastPushedId/lastPushDate 置 null，清空 pushHistory
- 单独测试 PDF 生成：`python3 gen_card_pdf.py --payload <payload.json> --zh <zh.json> --out test.pdf`
- 单独测试上传：`python3 upload_ima.py --file <xxx.pdf>`

## 文件说明

| 文件 | 作用 |
|------|------|
| `SKILL.md` | 本指令文件 |
| `push_card.py` | 进度管理 + 卡片载荷提取（status/next/render/mark/weekday） |
| `gen_card_pdf.py` | 生成卡片式双语 PDF（weasyprint） |
| `upload_ima.py` | 上传 PDF 到 IMA 知识库文件夹（含密钥失效检测） |
| `notify_key_expired.py` | 密钥失效时发飞书 webhook 通知 |
| `normalize_quotes.py` | 中文引号自动规范化（杜绝英文直引号混入） |
| `items.json` | 118 个知识点知识库 |
| `index.json` | 卡片推送顺序索引 |
| `progress.json` | 推送进度（自动维护） |
| `cards/` | 118 张纯英文 HTML 卡片源 |

## 注意事项

- 进度是唯一凭证，勿手动误改 progress.json
- 失败的推送绝不计进度，确保下次重推同一张
- PDF 文件名日期格式统一 `YYYY-MM-DD`
- 翻译质量优先：术语必须联网核对，宁可慢不可错
