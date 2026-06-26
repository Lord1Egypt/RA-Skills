# Stage 1：概念、剧本与物料生成

### 1.1 概念与大纲生成（须停机等待用户确认）

根据确定的体裁 (Genre)，使用对应的提示词框架生成内容大纲：

**对于 Genre X (叙事类)：**
> "请你从[指定领域]里，选择一个深度的概念。然后写一个寓言/历史故事，用间接的方式把这个概念讲清楚。不要一开始就说答案，到故事快结束时反转。最后解释概念及隐喻。"

**对于 Genre Y (分析类)：**
> "请你从[指定领域]里，挖掘一个反直觉的痛点现象。先描绘这个现象，然后拆解背后的核心矛盾/系统性崩溃原因，最后给出具有实操性的商业洞察或管理金句。"

**对于 Genre Z (宣发类)：**
> "请根据[产品/功能描述]，提取最核心的用户痛点和利益点，以短视频节奏输出一段极具转化率的宣发文案框架（痛点直击 -> 价值展示 -> CTA）。"

**去重检查**：生成前扫描工作空间内所有 `YYYYMMDD/视频脚本.md`，确保主题不与历史作品重复。

⛔ **此步完成后必须停机，将生成的大纲/故事完整展示给用户，等待明确确认。未经确认严禁继续。**

### 1.2 内容定档（用户确认大纲后立即执行）

在动手写剧本之前，必须先完成内容定档。这是防止「好内容变烂视频」的关键步骤。

**步骤：**

1. **标记不可删减要素**：逐段扫描用户确认的内容大纲，用以下标签标记（见 0.3）：
   - `[因果/逻辑]` — 逻辑链节点
   - `[转折/对比]` — 认知翻转或数据对比
   - `[核心金句]` — 结论闭环

2. **计算最低旁白字数**：将所有标记要素的文本合适，得出「不可压缩下限」。

3. **选档**：根据合计字数，在 §0.1 三档体系中选择对应档位。

4. **输出定档报告**（写入 `视频脚本.md` 头部）：
   ```markdown
   ## 内容定档
   - **原始内容字数**：{X} 字
   - **不可删减要素字数**：{Y} 字
   - **选定档位**：{S/M/L}
   - **预估旁白总字数**：{Z} 字
   - **预估视频时长**：{Z ÷ 3.5} 秒
   ```

⛔ **如果不可删减要素字数 > 450（S 档上限），严禁使用 S 档强行压缩。必须升档。**

### 1.3 剧本转化

将内容按选定档位的规格拆解为分镜剧本，写入 `YYYYMMDD/视频脚本.md`。

**内容完整性自检（剧本写完后必须执行，全部通过才能进入下一步）：**

- [ ] **盲测**：让一个没读过原文的人只看剧本旁白，能否独立理解核心价值（故事结局/分析结论）？如果不能，说明删多了。
- [ ] **因果/逻辑链完整**：每个「结论」都有对应的「事件/数据」作为铺垫，没有凭空冒出的道理。
- [ ] **Genre X 专属**：角色有动作有对话，不能只靠旁白概括。
- [ ] **Genre Y 专属**：痛点现象的铺垫是否足以推导出最终的解决方案和金句？

剧本格式模板：
```markdown
## 分镜 scene_cover — 封面/标题幕
- **情绪档位**：1
- **旁白**：{通常为视频标题或引导句}
- **画面描述**：{高吸引力、悬念感强的提示词}

## 分镜 {N} — {幕名}
- **时间（草稿估算）**：第 {X} ～ {Y} 秒
- **情绪档位**：{1/2/3/4}
- **旁白**：{中文30~80字}
- **画面描述**：{图片提示词，中英文均可}

## 分镜 scene_end — 结尾/升华幕
- **情绪档位**：4
- **旁白**：{点题金句，不超过 20 字}
- **画面描述**：{意境深远、呼应主题的提示词}
```

### 1.4 TTS 语音生成

**声纹选择（优先意识）：**
- **默认原则**：优先检查 `/语音模型/voxenv` 环境。若存在，**必须**使用用户的声纹克隆生成旁白。
- **降级方案**：仅在用户明确要求或克隆环境不可用时，才使用 Kokoro 等通用模型。

**语音节奏优化：**

VoxCPM2 的情绪输出相对平稳，需要在文本层面手动注入戏剧感。处理规则：

- 在核心关键词前插入 `……`，让模型自动降速放重音
- 超过 130 字的段落用 `|||` 在语气转折处手动分段
- 档位 4（沉默留白幕）的旁白每个词组之间都加 `……`

```
❌ 平铺直叙：
"你以为选出了战将，其实你只选出了最擅长残杀队友的屠夫。"

✅ 有停顿感的版本：
"你以为……选出了战将。|||其实，你只筛选出了——最擅长残杀队友的……屠夫。"
```

在项目目录下执行：

```bash
# 使用本地 VoxCPM2 模型生成语音（必须使用虚拟环境的 Python）
# 1. 复制并编辑生成脚本（每个项目独立一份）
cp /Users/lucas/Work/09.Antigravity/语音模型/generate_cantillon.py \
   /Users/lucas/Work/09.Antigravity/语音模型/generate_{project_name}.py
# 2. 编辑 TARGET_TEXT、OUTPUT_FILE 等变量
# 3. 运行
/Users/lucas/Work/09.Antigravity/语音模型/voxenv/bin/python3 \
  /Users/lucas/Work/09.Antigravity/语音模型/generate_{project_name}.py
```

### 1.5A 图片素材生成（模式 A）

> ℹ️ 仅模式 A（纯图片）执行此步。模式 B 跳转至 §1.5B。

按剧本中每幕的"画面描述"逐一生成图片，命名严格遵循 `scene1.png`、`scene2.png` ... `scene{N}.png`，保存至 `YYYYMMDD/assets/`。

**批量生成策略（应对 API 配额限流）：**

图片生成 API 通常有速率限制（如每窗口期 5 张）。为避免流程阻塞，采用以下策略：

1. **先批量准备提示词**：在生成前，将全部场景的提示词按风格圣经公式组装完毕，写入剧本。
2. **分批生成 + 穿插其他工作**：每批生成到限流后，立即切换到其他 Stage 的工作（如音频分析、HTML 搭建），不要干等。
3. **生成即归档**：每张图生成后立即 `cp` 到 `assets/` 目录并验证文件名，避免最后批量操作时遗漏。
4. **断点续传**：用 `ls assets/scene*.png | wc -l` 检查进度，只生成缺失的图片。

### 1.5B 视频 B-roll 素材采集与裁剪（模式 B）

> ℹ️ 仅模式 B（视频 + 文字叠加）执行此步。模式 A 跳转至 §1.5A。

**步骤 1 — B-roll 关键词策划：**

根据每幕的情绪和主题，在 `视频脚本.md` 中列出搜索关键词：
```markdown
## B-roll 素材规划
| 幕 | 情绪 | 搜索关键词 | 画幅偏好 |
|----|------|-----------|---------|
| scene1 | 压迫/悬疑 | dark office, laptop screen | 竖屏优先 |
| scene2 | 忙碌/混乱 | meeting room, people talking | 竖屏优先 |
| scene7 | 升华/开阔 | city night, aerial view | 横屏可接受 |
```

**步骤 2 — 素材探测（浏览器手动或自动）：**

在 Pexels (https://pexels.com/search/videos/) 搜索关键词，获取视频直链。优先选择：
- 竖屏 9:16（`_1080_1920_` 或 `_1440_2560_`）
- 时长 ≥ 10 秒（裁剪后留 ≤ 20 秒）
- 无水印、免版税

**步骤 3 — 编写自动化下载脚本 `download_and_process.py`：**

脚本必须包含以下能力（参考实现见 `20260518_org_slowdown/download_and_process.py`）：

```python
VIDEO_MAP = {
    "scene1.mp4": {"url": "https://videos.pexels.com/...", "is_vertical": True},
    "scene2.mp4": {"url": "https://videos.pexels.com/...", "is_vertical": False},
    # ...
}
```

**下载容错规范：**
- `curl -L -k --retry 5 --retry-delay 3 -H "User-Agent: Mozilla/5.0 ..."` — Pexels CDN 需要浏览器 UA，且 SSL 连接不稳定
- 若 curl 返回非零但文件通过 `ffprobe` 校验 → 视为下载成功（Cloudflare 常在传输末尾断开连接）
- 已存在的有效视频自动跳过（断点续传）

**FFmpeg 竖屏裁剪规范：**

| 原片画幅 | FFmpeg filter | 说明 |
|---------|--------------|------|
| 9:16 竖屏 | `scale=1080:1920` | 直接缩放 |
| 16:9 横屏 | `crop=ih*9/16:ih,scale=1080:1920` | 居中裁剪后缩放 |

所有视频统一参数：`-t 20 -c:v libx264 -crf 18 -an -y`（限时长 20s，去音轨）

**步骤 4 — 运行脚本：**
```bash
export PATH=./bin:$PATH
python3 download_and_process.py
```

### 1.6 纯文字海报生成（封面 scene_cover 与 封底 scene_end）

> ℹ️ 无论处于模式 A（纯图片）还是模式 B（视频B-roll），所有视频都必须具备静态的海报级封面与封底。如果你有 `image_generate` 或类似生图工具的权限，请带上 `aspect_ratio="portrait"` 等参数调用；否则，请输出 Prompt 引导用户在其他平台生成。

**通用设计铁律：所有封面与封底必须是纯文字排版，绝不配图、无图标、无装饰。**
- **满屏大标题** — 文字撑满整张画面，不留大片空白。
- **错落有致** — 多行错位、大小穿插，制造视觉节奏感。
- **留白呼吸** — 文字之间有空隙，不拥挤。
- **落款署名** — 严禁硬编码他人名字。生成前，**必须通过对话询问用户**：“请问您的海报落款署名要写什么？”；如果用户不便回答，使用通用占位符如 `—— [主理人]`。

**Style Slots (配色/字体风格矩阵)：**
根据视频话题，自动选择以下 10 套体系之一。详细说明请查阅 [视觉风格参考手册](file://./resources/style_bible.md)。

**Prompt 构建公式：**
`[Vertical portrait poster, ONLY Chinese typography filling the entire frame. No images...]` + `[配色/字体风格描述]` + `[标题与落款排版]`

*示例 Prompt (科技增长蓝封面)：*
`Vertical portrait poster, ONLY Chinese typography filling the entire frame. No images, no illustrations, no icons, no decorations. Pure text only. Modern tech aesthetic: deep blue gradient background, white and cyan (#00D7FF) characters. Clean, bold display font. Staggered layout with varying character sizes. Title "企业做AI千万不要一上来就全员铺工具" arranged in 3-4 lines with oversized and medium contrast. "—— [用户指定的IP名]" as small signature at bottom. High-impact, minimal.`

*封底 (End Card) 格式：*
排版内容固定为："👍 点赞 ⭐ 收藏 \n 🔔 加关注 \n\n 我们下期见！ \n —— [用户指定的IP名]"，配色必须与封面保持一致。

生成后，严格命名为 `scene_cover.png` 和 `scene_end.png` 保存至 `assets/` 目录。

**✅ Stage 1（素材）退出标准：**

模式 A：
- [ ] `assets/` 下场景图片数量 == 剧本分镜数
- [ ] 场景图片命名符合规范（scene1~N.png）

模式 B：
- [ ] `assets/` 下每幕对应的 `.mp4` 文件已就位且通过 `ffprobe` 校验
- [ ] 所有视频为 1080×1920 竖屏、无音轨、时长 ≤ 20s

通用（模式 A 与 B 都必须满足）：
- [ ] `scene_cover.png` 与 `scene_end.png` 已生成并就位。
- [ ] `assets/narration.wav` 已生成。

### 1.7 BGM 背景音乐匹配

BGM 是情绪的推手，必须在 Stage 2 之前完成匹配。

**BGM 匹配工作流：**
1. **情绪识别**：分析剧本中各幕的「情绪档位」，提取核心关键词（如：Suspense, Epic, Minimalist, Melancholic）。
2. **曲库搜索**：从免版税音乐库（如 Scott Buckley, Pixabay, Bensound）搜索并下载 1 首全局背景音。
3. **参数配置**：
   - `data-track-index`: 设为 `-1`（始终位于底层）。
   - `data-volume`: 默认设为 `0.15` ～ `0.25`（通过 preview 实时调整，严禁盖过旁白）。
4. **集成到 index.html**：
   ```html
   <audio id="bgm" src="assets/bgm.mp3" data-start="0" data-duration="{视频总长}" data-track-index="-1" data-volume="0.25"></audio>
   ```

**✅ Stage 1.7 退出标准：**
- [ ] `assets/bgm.mp3` 已就位。
- [ ] `视频脚本.md` 已补充 BGM 署名信息（含作者、链接及 CC 协议）。
