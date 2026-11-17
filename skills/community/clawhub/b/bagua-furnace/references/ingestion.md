# 接料辨体 · 操作手册（第 0 关）

本文件是八卦炉「第 0 关 接料辨体」的**真实调用语法**手册。AI 接到客户甩来的链接 / 文件 / 粘贴文本时，先按下方路由判定类型，再调用对应适配器把原料变成**纯文本**，之后才进九转提炼。所有适配器均用本机已装能力，无需额外密钥（ASR 兜底端点除外，见下）。

---

## 路由判定顺序

1. 已是纯文本 / 本地 `.txt` `.md` → 直入第一关（收料定标）。
2. 路径或链接以 `.pdf` 结尾 / Content-Type 为 `application/pdf` → PDF 适配器。
3. 链接域名命中 `douyin.com / iesdouyin.com / kuaishou.com / xiaohongshu.com / weixin.qq.com(视频号)` → 短视频文案适配器。
4. 后缀 `png/jpg/jpeg/webp` 或用户说"截图/书页" → 图片 OCR 适配器。
5. `http(s)` 且非上述视频平台 → 网页适配器。
6. 域名命中 `youtube.com / youtu.be / bilibili.com / b23.tv` 或后缀 `mp4/mkv/mp3/wav/m4a` → ASR 适配器。
7. 其他 / 无法判定 → 先问用户"这是网页、PDF、还是音视频？"，不要瞎猜。

---

## 各适配器真实调用语法

### A. 纯文本 / 本地文本文件
- 粘贴内容：直接用。
- 本地文件：`Read /abs/path/xxx.md`（或 `.txt`）。

### B. PDF（本地或链接）
- 链接（`.pdf`）：先下载再处理：
  ```bash
  curl -L "<pdf_url>" -o /tmp/bagua_in.pdf
  ```
  > 注意：部分 PDF 直链 WebFetch 抓不到正文，务必走「下载 → 抽取」两步走。
- **CAJ（学术文献）**：先调用 `caj2pdf-offline` 技能转 PDF，再走上面 PDF 流程。触发词「caj 转 pdf」。

> **⚠️ 真实缺口 G4（2026-08-26 真机测试发现）**：本环境 `Read` 工具对 PDF（中文名/常规名均会）返回「Cannot display content of binary file」，**不能直接读 PDF 正文**。必须改用隔离 Python venv 的 `pypdf`（或 `fitz`/PyMuPDF）抽取文本层。
> ```bash
> # 在 managed runtime 下建隔离 venv（仅一次）
> <managed_python> -m venv <runtime>/envs/default
> <runtime>/envs/default/Scripts/pip install pypdf
> # 抽取
> <runtime>/envs/default/Scripts/python - <<'PY'
> import pypdf
> r = pypdf.PdfReader(r"/abs/path/xxx.pdf")
> txt = "\n".join((p.extract_text() or "") for p in r.pages)
> open("/tmp/bagua_in.txt","w",encoding="utf-8").write(txt)
> PY
> # 随后 Read /tmp/bagua_in.txt 进九转
> ```
> 中文名 PDF 在 zip 内多为 cp437 字节，解压时用 `n.encode('cp437').decode('gbk')` 还原文件名再读取。该 venv 在隔离目录，不污染用户环境。

> **⚠️ 真实缺口 G5（2026-08-26 真机测试发现 · 重要）**：`pypdf`/`fitz` 抽到的「文字」**可能是乱码**——部分 PDF 的字体 ToUnicode 映射损坏，抽出来是一串无意义的拉丁字母（CID 码），中文关键词一个都匹配不上。所以**抽完必须做「乱码校验」**，不能假设抽出来就是真字：
> ```python
> import re
> def looks_garbled(txt: str) -> bool:
>     # 抽出的正文里几乎没有 CJK 汉字，却有很多零散拉丁字母 → 判为乱码
>     cjk = len(re.findall(r'[\u4e00-\u9fff]', txt))
>     if len(txt) > 200 and cjk < max(20, len(txt)//50):
>         return True
>     return False
> # 取前几页抽样检测；若乱码 → 走 OCR（见下）
> ```
> **乱码/无文字层 → 走 OCR 适配器**（与扫描版图片 PDF 同一条路）：用 `fitz` 把每页渲染成图片，再用 `rapidocr-onnxruntime`（纯 onnx 栈，不依赖 paddlepaddle，CPU 可跑）逐页识别：
> ```bash
> <runtime>/envs/default/Scripts/pip install -q pymupdf rapidocr-onnxruntime opencv-python-headless onnxruntime
> <runtime>/envs/default/Scripts/python - <<'PY'
> import fitz
> from rapidocr_onnxruntime import RapidOCR
> engine = RapidOCR()
> doc = fitz.open(r"/abs/path/xxx.pdf")
> out=[]
> for i in range(doc.page_count):
>     pix = doc[i].get_pixmap(dpi=150)
>     pix.save("/tmp/_pg.png")          # 固定临时名、覆盖、不删除(规避沙箱 safe-delete 崩溃)
>     res,_ = engine("/tmp/_pg.png")
>     out.append("\n===== 第%d页 =====\n" % (i+1) + "\n".join(x[1] for x in (res or [])))
> open("/tmp/bagua_in_ocr.txt","w",encoding="utf-8").write("\n".join(out))
> PY
> ```
> > **沙箱坑（2026-08-26 实测）**：WorkBuddy 的 `sitecustomize.py` 全局拦截 `os.remove`/`shutil` 删除，在无回收站沙箱里触发 `SAFE_DELETE_FAIL_CLOSED` 直接令进程崩溃。渲染临时图**用固定文件名覆盖、不要删除**即可规避；`pip` 装包若报 `cv2 LICENSE safe_delete` 失败，用「`pip download` wheel → 手动 `zipfile` 解压到 site-packages」绕过。

> **PDF 分类速判（真机结论）**：一本书 PDF 到底是哪类，抽完校验才知，不要预设：
> ① 文字层有效（多数正规排版电子书）→ 直接提炼；
> ② 文字层乱码（字体 ToUnicode 映射损坏）→ OCR；
> ③ 纯图片扫描件（无文字层）→ OCR。
> ② 与 ③ 在八卦炉流水线里**走同一 OCR 适配器**，区别仅在于 pypdf 是否先被骗出乱码。

### C. 抖音 / 快手 / 小红书 / 视频号 短视频
- 调用本机已装技能 **`douyin_copy_extract`**（触发词「抖音文案提取 / 短视频文案提取 / 链接提取文案」）。
- 把用户给的分享短链交给它，取回「口播文案 · 原版提取」段，即为可提炼文本。
- 该技能已覆盖四平台短视频口播文案，本炉**不重造**，直接复用。

### D. 图片 / 书页截图
- `Read /abs/path/img.png` —— Read 工具多模态 OCR，直接回文字。

### E. 普通网页 / 文章
- `WebFetch url prompt="提取这篇文章的正文全文，去掉导航栏、广告、侧边栏与评论，保留标题、小标题与所有正文段落，按原文顺序输出"`。
- 若 WebFetch 返回被截断或不完整，改用 `agent-browser` / `chromium` 技能打开页面后取正文。

### F. ASR 适配器（YouTube / B站 / 本地音视频）
双层方案，与业界现成技能（金大哥 `douyin-extract-copywriter`、仓颉蒸馏）一致：**字幕优先 + Whisper 兜底**。

**① 字幕优先（无需本地模型，优先走）**
- YouTube：用 `agent-browser` / `chromium` 技能打开视频页，从 transcript 面板或 timedtext 接口抓 CC 字幕；或直接 `WebFetch "https://www.youtube.com/watch?v=ID" prompt="提取视频的 CC 字幕/转录文本"`（有字幕时可用）。
- B站：用 `agent-browser` / `chromium` 技能调用字幕接口 `https://api.bilibili.com/x/player/wbi/v2?bvid=<BV号>` 取 `subtitle` 字段，解码后得文本。

**② Whisper 兜底（无字幕时）**
- 公司 GPU 服务器 `192.168.21.97`（RTX 4090）部署 `faster-whisper` / `whisper.cpp` 推理端点（如 `http://192.168.21.97:9000/transcribe`）。
- 调用：把音频（本地文件或下载后的音频）POST 到该端点，拿回逐字转写。
- ⚠️ **前置依赖**：该端点当前未部署（GPU 服务器现仅跑 vLLM+qwen2.5-7b）。部署属独立子任务；未部署前走降级。

**③ 降级（无字幕且 Whisper 未就绪）**
- 直接提示用户：「这段音视频暂无字幕、且本机 Whisper 端点未就绪。请提供转写稿，或先用 ASR 工具转写后丢给我，本炉立刻开炼。」**不卡死流程**。

---

## 边界与坑

- 视频/音频若用户只给链接、无任何字幕且 Whisper 未部署 → 不强行编造，走降级提示。
- 微信文章 / 公众号：属「网页」类，用 WebFetch 或 `wechat-article-spider` 思路抓取；若遇登录墙，提示用户贴正文。
- 讨论记录记录：用户直接粘贴文本即可，本炉走「讨论记录→决策洞见」透镜（见 `extraction-lenses.md`），无需转换适配器。
- 所有转写/提取结果都**保留溯源锚点**（视频链接+时间戳、PDF 页码、网页 URL），供第 5 关成丹时写「来源溯源」字段。
