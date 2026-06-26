---
name: baidu-vod-translate
description: 百度智能云VOD视频翻译工具。支持字幕翻译和语音翻译（配音），支持用户上传字幕、自定义字幕样式，支持批量处理文件夹中的视频，处理后可下载到本地或上传到网盘。当用户提及"视频翻译"、"翻译视频"、"把视频翻译成XX语"时触发。百度智能云视频翻译skill是付费使用，价格详见：https://cloud.baidu.com/doc/VOD/s/Zmheig5gv
allowed-tools: Bash, Read, Glob, Grep, Write, Question
argument-hint: "[视频路径] --source <源语言> --target <目标语言>"
metadata: { "openclaw": { "requires": { "bins": ["python3"] } } }
---

# 百度智能云 VOD 视频翻译 Skill

将视频内容翻译成目标语言，支持字幕翻译和语音翻译（配音）。

## ⚠️ 强制执行流程

**禁止直接执行命令！必须按以下流程引导用户：**

```
1. 识别意图 → 判断翻译类型（字幕/语音/两者）
2. 收集参数 → 使用 Question 工具询问用户
3. 确认配置 → 展示参数让用户确认
4. 用户确认 → 才能执行命令
```

**错误示例（禁止）：**
```
用户: 帮我翻译这个视频
Agent: [直接执行 python3 translate.py video.mp4 --source zh --target en]  ❌
```

**正确示例：**
```
用户: 帮我翻译这个视频
Agent: 请选择处理方式：
  [1] 单个视频
  [2] 批量处理文件夹
用户: 1
Agent: 请问您需要哪种翻译方式？
  [1] 字幕翻译
  [2] 语音翻译（配音）
用户: 1
Agent: 请确认：源语言中文，目标语言英语？
用户: 确认
Agent: [执行命令]  ✓
```

---

## 触发规则

满足以下任一条件时触发：

1. 用户提及"视频翻译"、"翻译视频"
2. 用户需要将视频翻译成其他语言
3. 用户需要视频配音
4. 用户需要查询或管理翻译项目/任务

---

## Agent 参数收集指南

### 核心原则

1. **简洁优先**：直接询问处理方式，不绕弯子
2. **最小必要**：只收集必要参数，其他使用默认值
3. **渐进式**：从简单到复杂，避免一次性问太多
4. **推荐优先**：给出推荐选项，而非开放式问题

---

## 第一步：识别用户意图

根据用户描述，识别属于哪种场景：

| 用户描述关键词 | 场景类型 | 推荐配置 |
|---------------|----------|----------|
| "翻译成英语"、"翻译成中文" | 字幕翻译 | --subtitle（默认） |
| "配音"、"配音翻译"、"语音翻译" | 语音翻译 | --speech |
| "我有字幕"、"用这个字幕" | 用户字幕 | --subtitle-source user |
| "查任务"、"项目列表" | 任务管理 | --list-tasks/--list-projects |
| "修改字幕"、"替换字幕" | 任务修改 | --update-task |

---

## 第二步：收集必要参数

### 第一步：询问处理方式

**交互模板：**

```
用户: 帮我翻译这个视频

Agent: 请选择处理方式：
  [1] 单个视频 - 处理单个视频文件
  [2] 批量处理文件夹 - 处理文件夹中的所有视频

用户: 1 或 2
```

---

### 第二步：收集视频路径

#### 场景 A：单个视频

**交互模板：**

```
Agent: 请提供视频文件路径：

用户: /Downloads/video.mp4
```

#### 场景 B：批量处理文件夹

**交互模板：**

```
Agent: 请提供文件夹路径（将处理该文件夹下所有视频文件）：

用户: /Downloads/videos/

Agent: 正在扫描文件夹中的视频文件...
找到 5 个视频文件：
  1. video1.mp4
  2. video2.mp4
  3. video3.mp4
  4. video4.mp4
  5. video5.mp4

确认处理这些视频吗？
```

**扫描文件夹的实现：**

使用 Glob 工具扫描常见视频格式：
```
Glob: <文件夹路径>/**/*.mp4
Glob: <文件夹路径>/**/*.mkv
Glob: <文件夹路径>/**/*.avi
Glob: <文件夹路径>/**/*.mov
Glob: <文件夹路径>/**/*.webm
```

---

### 第三步：询问翻译方式

**交互模板：**

```
Agent: 请问您需要哪种翻译方式？
  [1] 字幕翻译 - OCR识别字幕 → 翻译 → 烧录到视频（推荐）
  [2] 语音翻译（配音） - 保留原声音色，翻译后配音
  [3] 字幕+配音 - 同时进行字幕翻译和配音

用户: 1
```

---

### 第四步：询问语言

**询问源语言：**

```
Agent: 请问视频原始语言是什么？
  [1] 中文
  [2] 英语
  [3] 日语
  [4] 其他

用户: 1
```

**询问目标语言：**

```
Agent: 请问要翻译成什么语言？
  [1] 英语
  [2] 日语
  [3] 韩语
  [4] 其他

用户: 1
```

---

### 场景 C：语音翻译（配音）

**如果选择了配音相关选项，额外询问：**

```
Agent: 请选择配音方式：
  [1] 音色复刻 - 模仿原声说话（推荐）
  [2] AI配音 - 使用指定音色

用户: 1
```

---

### 场景 D：用户上传字幕

**触发条件**：用户说"我有字幕文件"、"用这个字幕"等

**交互模板：**

```
用户: 我有字幕文件，帮我翻译视频

Agent: 好的，请提供：
  - 视频文件路径：
  - 字幕文件路径（SRT格式）：
  - 字幕是什么语言：
  - 要翻译成什么语言：

用户: video.mp4, subs.srt, 中文, 英语

Agent: [执行: --subtitle-source user --subtitle-file subs.srt --source zh --target en]
正在翻译...
```

---

## 第三步：确认配置

收集完参数后，展示配置让用户确认：

**单个视频：**
```
Agent: 确认以下配置：
  - 视频文件: /Downloads/video.mp4
  - 翻译方式: 字幕翻译
  - 源语言: 中文
  - 目标语言: 英语
  - 输出目录: ./output

确认执行吗？
```

**批量处理：**
```
Agent: 确认以下配置：
  - 处理模式: 批量处理
  - 视频数量: 5 个
  - 翻译方式: 字幕翻译
  - 源语言: 中文
  - 目标语言: 英语
  - 输出目录: ./output

确认执行吗？
```

---

## 参数收集决策树

```
用户请求
    │
    ├─ 查询任务？ ──────────────────────► --list-tasks / --list-projects
    │
    ├─ 删除项目？ ──────────────────────► --delete-project
    │
    ├─ 修改任务？ ──────────────────────► --update-task
    │
    └─ 翻译视频？
         │
         ├─ 处理方式？
         │    ├─ 单个视频 ──► 获取视频文件路径
         │    └─ 批量处理 ──► 获取文件夹路径 → 扫描视频文件 → 展示列表确认
         │
         ├─ 翻译类型？
         │    ├─ "翻译字幕" ──► --subtitle
         │    ├─ "配音" ──► --speech + 询问配音方式
         │    └─ 都要 ──► --subtitle --speech + 询问配音方式
         │
         ├─ 语言？
         │    ├─ 源语言 ──► 确认或自动识别
         │    └─ 目标语言 ──► 必须明确
         │
         ├─ 字幕来源？（可选）
         │    ├─ "有字幕文件" ──► --subtitle-source user
         │    ├─ "视频有字幕" ──► --subtitle-source ocr
         │    └─ "视频无字幕" ──► --subtitle-source asr
         │
         └─ 确认执行
              │
              ├─ 来自网盘？ ──► 询问是否上传回网盘
              │
              └─ 执行命令
```

---

## 推荐参数组合

### 组合 1：基础字幕翻译（推荐）

```bash
python3 scripts/translate.py <视频> --source zh --target en
```

**适用场景**：大多数视频翻译需求
**特点**：OCR识别字幕 → 翻译 → 烧录到视频

### 组合 2：影视剧配音

```bash
python3 scripts/translate.py <视频> --source zh --target en --speech
```

**适用场景**：需要配音的视频
**特点**：保留原声音色，翻译后配音

### 组合 3：批量处理

```bash
python3 scripts/translate.py video1.mp4 video2.mp4 video3.mp4 --source zh --target en
```

**适用场景**：批量翻译多个视频
**特点**：所有视频使用相同的翻译配置

### 组合 4：用户字幕翻译

```bash
python3 scripts/translate.py <视频> --source zh --target en \
  --subtitle-source user --subtitle-file subs.srt
```

**适用场景**：有现成字幕文件
**特点**：使用用户提供的字幕，翻译更准确

---

## 语言识别快捷方式

| 用户说法 | 对应语言代码 |
|----------|-------------|
| 中文、国语、普通话 | zh |
| 中文繁体、繁体中文 | zh-TW |
| 英语、英文 | en |
| 日语、日文 | ja |
| 韩语、韩文 | ko |
| 法语、法文 | fr |
| 德语、德文 | de |
| 西班牙语 | es |
| 葡萄牙语 | pt |
| 俄语 | ru |
| 泰语 | th |
| 阿拉伯语 | ar |

---

## 常见问题处理

### Q1：用户不知道源语言

```
Agent: 请问视频原始语言是什么？
  [1] 中文
  [2] 英语
  [3] 日语
  [4] 其他

用户: 不确定

Agent: 可以尝试自动识别，或根据视频内容判断。
建议选择最可能的语言，如果翻译效果不好可以重新处理。
```

### Q2：批量处理时文件夹中没有视频

```
Agent: 正在扫描文件夹中的视频文件...
未找到视频文件。请确认文件夹路径正确，且包含以下格式的视频：
  .mp4, .mkv, .avi, .mov, .webm

请重新提供文件夹路径：
```

### Q3：用户想要字幕文件而非视频

```
用户: 我只要翻译后的字幕文件，不要烧录到视频

Agent: 好的，不烧录字幕到视频。
[执行: --no-burn-subtitle]
翻译完成后会提供字幕文件下载链接。
```

### Q4：用户想保留原字幕

```
用户: 保留原来的中文字幕，再加英文字幕

Agent: 好的，不擦除原字幕，翻译后会同时显示中英双语字幕。
[执行: --no-erase-subtitle]
```

---

## 执行命令模板

### 单个视频

```bash
export BAIDU_VOD_AK='xxx' && export BAIDU_VOD_SK='xxx' && \
python3 scripts/translate.py <视频路径> --source <源语言> --target <目标语言>
```

### 批量处理

```bash
export BAIDU_VOD_AK='xxx' && export BAIDU_VOD_SK='xxx' && \
python3 scripts/translate.py <视频1> <视频2> <视频3> --source <源语言> --target <目标语言>
```

### 完整命令（所有参数）

```bash
export BAIDU_VOD_AK='xxx' && export BAIDU_VOD_SK='xxx' && \
python3 scripts/translate.py <视频路径> \
  --source <zh|en|ja|...> \
  --target <zh|en|ja|...> \
  --subtitle \
  --speech \
  --subtitle-source <ocr|asr|user> \
  --subtitle-file <字幕文件> \
  --tts-type <VOICE_CLONE|AI_DUB> \
  --output-dir <输出目录> \
  --upload-netdisk \
  --netdisk-dir <网盘目录>
```

---

## 示例对话

### 示例 1：单个视频字幕翻译

```
用户: 帮我把 /Downloads/video.mp4 翻译成英语

Agent: 请选择处理方式：
  [1] 单个视频
  [2] 批量处理文件夹

用户: 1

Agent: 请问您需要哪种翻译方式？
  [1] 字幕翻译（推荐）
  [2] 语音翻译（配音）
  [3] 字幕+配音

用户: 1

Agent: 请问视频原始语言是什么？
  [1] 中文
  [2] 英语
  [3] 其他

用户: 1

Agent: 确认配置：
  - 视频文件: /Downloads/video.mp4
  - 翻译方式: 字幕翻译
  - 源语言: 中文
  - 目标语言: 英语
  - 输出目录: ./output

确认执行吗？

用户: 确认

Agent: 正在翻译...
[执行: --source zh --target en]
✓ 处理完成，结果已保存到: ./output/video_en.mp4
```

### 示例 2：批量处理

```
用户: 帮我翻译一个文件夹里的所有视频

Agent: 请选择处理方式：
  [1] 单个视频
  [2] 批量处理文件夹

用户: 2

Agent: 请提供文件夹路径：

用户: /Downloads/videos/

Agent: 正在扫描文件夹中的视频文件...
找到 3 个视频文件：
  1. ep01.mp4
  2. ep02.mp4
  3. ep03.mp4

请问您需要哪种翻译方式？
  [1] 字幕翻译（推荐）
  [2] 语音翻译（配音）
  [3] 字幕+配音

用户: 1

Agent: 请问视频原始语言是什么？
  [1] 中文
  [2] 英语
  [3] 其他

用户: 1

Agent: 请问要翻译成什么语言？
  [1] 英语
  [2] 日语
  [3] 其他

用户: 1

Agent: 确认配置：
  - 处理模式: 批量处理
  - 视频数量: 3 个
  - 翻译方式: 字幕翻译
  - 源语言: 中文
  - 目标语言: 英语
  - 输出目录: ./output

确认执行吗？

用户: 确认

Agent: 正在批量翻译...
[执行: ep01.mp4 ep02.mp4 ep03.mp4 --source zh --target en]
✓ 全部处理完成
```

### 示例 3：配音场景

```
用户: 帮我把这个中文视频配上英语配音

Agent: 请选择处理方式：
  [1] 单个视频
  [2] 批量处理文件夹

用户: 1

Agent: 请提供视频文件路径：

用户: /Downloads/movie.mp4

Agent: 请选择配音方式：
  [1] 音色复刻 - 模仿原声说话（推荐）
  [2] AI配音 - 使用指定音色

用户: 1

Agent: 确认配置：
  - 视频文件: /Downloads/movie.mp4
  - 翻译方式: 语音翻译（配音）
  - 配音方式: 音色复刻
  - 源语言: 中文
  - 目标语言: 英语

确认执行吗？

用户: 确认

Agent: 正在处理，配音需要较长时间...
[执行: --source zh --target en --speech]
✓ 处理完成
```

---

## 前置条件

### 1. VOD 凭证

```bash
export BAIDU_VOD_AK="your_access_key"
export BAIDU_VOD_SK="your_secret_key"
```

获取方式：
1. 登录 [百度智能云控制台](https://console.bce.baidu.com/)
2. 开通 [智能点播平台 VOD](https://cloud.baidu.com/product/vod.html)
3. 在 [安全认证](https://console.bce.baidu.com/iam/#/iam/accesslist) 获取 AK/SK

### 2. 网盘功能（可选）

如需从网盘下载或上传到网盘，需要：
1. 安装 bdpan CLI
2. 执行 `bdpan login` 登录

---

## 处理时间

- 字幕翻译：约 10-30 分钟
- 语音翻译：约 20-60 分钟
- 批量处理：按视频数量累计
- 可使用 `--no-wait` 参数不等待，稍后查询任务状态

---

## 注意事项

1. **文件大小限制**：单个文件 ≤ 5GB
2. **支持格式**：mp4/mpeg/mpg/dat/avi/mov/asf/wmv/navi/3gp/real video/mkv/flv/f4v/rmvb/rmhd/webm/hddvd/blue-ray/qsv/ts/mxf
3. **费用**：按处理时长计费
4. **源语言**：支持中文、中文繁体、英语、日语、韩语、德语、法语、俄语、泰语、阿拉伯语、西班牙语、葡萄牙语
5. **字幕文件**：仅支持 SRT 格式

---

## API 参考

- [项目管理 API](https://cloud.baidu.com/doc/VOD/s/Dmh0j7ldd)
- [任务管理 API](https://cloud.baidu.com/doc/VOD/s/ymh0j93u8)
