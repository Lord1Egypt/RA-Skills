---
name: free-course-share
description: 发「免费课程/证书」笔记之前的那半小时，交给它——筛课、拼图、给证书打码、出竖版封面，一次做完。三件事：① 核实一个课程是不是真免费、值不值得发 ② 把课程截图拼成两列排版、证书上的姓名学号邮箱自动打码（中文 OCR） ③ 生成 3:4 竖版封面。适合「这课到底免不免费」「截图太乱想拼一张」「证书上有我的信息不敢发」。**默认不加水印推广、不生成短链、不替你发布**；打码在本地做完即弃。不负责文案撰写与违禁词检测（配 xiaohongshu-prohibited-words 一起用）。
metadata:
  version: 1.1.10
  openclaw:
    requires:
      bins:
        - python3
        - tesseract
version: 1.1.10
---

# 免费课程分享工作流

面向中文内容平台创作者，提供筛课、拼图、证书隐私打码、3:4 封面和文案草稿。所有产物默认仅保存为本地草稿。

## 安全与发布边界

以下能力一律**默认关闭**，不得根据历史账号、作者信息或模板自行开启：

1. **账号水印**：不添加固定账号或作者水印。只有用户明确确认“添加水印”并提供本次准确文案后才能添加。
2. **推广内容**：不自动写 CTA、主页引导、群聊、私信、下载或营销话术。`cover_vertical.py --cta` 仅在用户确认具体文案后传入。
3. **短链**：不生成、替换、嵌入或发布短链。只有用户明确确认目标 URL、短链服务和投放位置后才能执行。
4. **自动发布**：不登录平台、不提交、不定时发布、不置顶评论。先交付预览；仅在用户检查最终素材并对本次发布动作作出明确确认后，才可调用独立发布工具。

不得把“继续”“按默认来”解释为上述四项的授权。确认必须指出具体动作和内容；每次发布单独确认。

## 环境

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install pillow==12.1.0 numpy==2.3.5 \
  opencv-python-headless==4.13.0.92 pytesseract==0.3.13
```

OCR 中文语言包：

```bash
# macOS
brew install tesseract tesseract-lang

# Debian/Ubuntu（在具备管理员权限的终端中执行）
apt-get install -y tesseract-ocr tesseract-ocr-chi-sim
```

## 工作流

### 1. 筛课

按 `references/course-screening.md` 检查费用、时长、凭证类型、访问限制和时效。易变信息必须回到官方页面核验。

### 2. 拼图

```bash
python3 {baseDir}/scripts/stitch.py two-col 图1.png 图2.png 图3.png -o 拼图.png
```

脚本不会添加水印或推广。

### 3. 敏感信息打码

优先为每个敏感文本单独声明：

```bash
python3 {baseDir}/scripts/redact.py \
  --src 证书.png \
  --text "张三" \
  --text "EMP-88231" \
  --out 证书-打码.png
```

OCR 不可靠时，用文本到坐标的一一映射：

```bash
python3 {baseDir}/scripts/redact.py \
  --src 证书.png \
  --text "张三" \
  --text-box "张三=913,464,1002,514" \
  --out 证书-打码.png
```

`--text-box TEXT=x1,y1,x2,y2` 规则：

- `TEXT` 必须同时由 `--text TEXT` 声明。
- 坐标采用源图像素坐标，必须是四个整数。
- 必须满足 `0 <= x1 < x2 <= 宽`、`0 <= y1 < y2 <= 高`。
- 映射到目标图后的坐标也会校验；越界即失败。
- `--box` 只是额外打码框，不会把任何未命中的 `--text` 视为成功。

同步修复嵌套证书图：

```bash
python3 {baseDir}/scripts/redact.py \
  --src 证书.png \
  --text "张三" \
  --text-box "张三=913,464,1002,514" \
  --targets 封面.png 拼图.png \
  --out 证书-打码.png \
  --target-out 输出目录
```

安全语义：

- 任一 `--text` 未命中：默认退出非零，不写成功图片。
- 任一 target 匹配分低于 `--min-target-score`（默认 `0.85`）：默认退出非零，不写任何成功图片。
- target 打不开、匹配异常或映射越界：退出非零，不写成功图片。
- 失败时仍可写私有验证目录中的失败 manifest，供排障；这不是成功成品。
- `verification-manifest.json` 的 `targets` 为每个目标记录 `matched`、`low_score`、`error`、`written`、`skipped` 等状态。
- `--allow-low-score-targets` 仅在用户明确确认后使用；它只跳过低分目标，不会把低分目标保存或标记成功。
- `--allow-unmatched` 和 `--include-unredacted-verification` 同样是危险显式开关，默认关闭。

发布前必须逐张查看验证图。打码脚本是辅助工具，不保证删除图片元数据、文件名或 URL 中的个人信息。

### 4. 封面

```bash
python3 {baseDir}/scripts/cover_vertical.py \
  --out 封面.png \
  --theme dark \
  --title "课程标题" \
  --sub "课程信息" \
  --body 拼图.png \
  --points "4小时|课程时长" "1张|完成凭证"
```

默认不绘制 CTA。只有用户确认具体推广文案后才传 `--cta "..."`。脚本没有固定账号水印参数；如用户确认需要水印，应使用独立、可审阅的后处理步骤并使用用户提供的文本。

### 5. 文案草稿与交付

- 明确区分证书与徽章，不夸大免费范围、时效或官方关系。
- 文案只输出草稿，不默认加入推广、短链、账号名或发布时段。
- 交付前检查标题与图片信息一致、敏感信息已遮挡、来源与时效已核验。
- 默认到“本地草稿 + 预览”结束；发布必须另行明确确认。

## 测试

```bash
python3 -m unittest discover -s {baseDir}/tests -v
```
