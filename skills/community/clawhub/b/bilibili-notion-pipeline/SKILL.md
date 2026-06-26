---
name: bilibili-notion-pipeline
description: Skill-first Bilibili to Notion pipeline. Download a Bilibili/b23 video, transcribe audio, upload the mp4, create or update a Notion transcript page, write transcript blocks, then optionally append a Markdown summary. Use when the user wants B站内容整理进 Notion、字幕入库、下载链接回写、文后总结追加等流程。
---

# Skill-First Bilibili → Notion Pipeline

这个 skill 现在的定位是：

> **Skill-first，agent-enhanced。**

也就是说：

1. **Skill 是主体**
   - 下载视频
   - 抽音频
   - 转写文本
   - 上传视频
   - 创建/更新 Notion 页面
   - 写入正文 blocks
   - 清理临时文件

2. **Agent 是增强层**
   - 页面是新建还是更新
   - 是否替换旧正文
   - 文后总结怎么写
   - 需要给用户回报哪些进度
   - 出错时如何切换兜底路径

## 什么时候用

当用户提出类似请求时触发：

- “把这个 B 站视频整理进 Notion”
- “下载、转写、上传并写 Notion”
- “给这篇整理字幕页补结构梳理和核心观点”
- “把视频内容做成正文 + 文后总结”
- “把 B 站内容入库到 Notion，并保留下载链接”

## 为什么它首先是 Skill

因为这套流程的大部分工作，都是：

- 可重复
- 低自由度
- 易脚本化
- 需要稳定执行

所以优先应该交给 `scripts/`，而不是每次让 agent 临场重写。

## 标准流程

### 推荐：一键 `run`

```bash
python skill/bilibili-notion-pipeline/scripts/pipeline.py run \
  --url "<b23或BV链接>" \
  --cleanup-mode temp
```

如果已经有人写好了 Markdown 总结：

```bash
python skill/bilibili-notion-pipeline/scripts/pipeline.py run \
  --url "<b23或BV链接>" \
  --markdown-file /path/to/summary.md \
  --require-summary \
  --cleanup-mode temp
```

`run` 会按顺序执行：

1. 解析视频
2. 下载视频
3. 抽取音频
4. 转写正文
5. 上传视频
6. 创建 / 更新 Notion 页面
7. 写入正文 blocks
8. 可选追加 Markdown 总结
9. 回读校验页面结构
10. 清理本地中间文件

### 分步模式（需要人工插入总结时）

#### 1）执行 `prepare`

```bash
python skill/bilibili-notion-pipeline/scripts/pipeline.py prepare --url "<b23或BV链接>"
```

如果用户明确给了已有 Notion 页面：

```bash
python skill/bilibili-notion-pipeline/scripts/pipeline.py prepare \
  --url "<链接>" \
  --page-id "<notion_page_id>" \
  --replace-children
```

`prepare` 会输出 JSON，记下：

- `page_id`
- `notion_url`
- `transcript_path`
- `metadata_path`
- `download_url`

#### 2）阅读转写正文

用 `read` 读取 `transcript_path`，判断：

- 主题是否跑偏
- 识别质量是否可接受
- 是否需要人工干预
- 文后总结应该如何组织

#### 3）补文后总结

先按固定结构写 Markdown：

- `## 结构梳理`
- `## 核心观点`
- `## 关键概念`

可参考：

- `references/summary-template.md`
- `references/workflow.md`

#### 4）把总结追加到 Notion

```bash
python skill/bilibili-notion-pipeline/scripts/pipeline.py append-summary \
  --page-id "<page_id>" \
  --markdown-file "/path/to/summary.md"
```

#### 5）回读校验

```bash
python skill/bilibili-notion-pipeline/scripts/pipeline.py verify \
  --metadata "<metadata_path>" \
  --require-summary
```

#### 6）按需清理

默认建议删除：

- wav
- transcript txt

本地 mp4 是否删除，由用户决定：

```bash
python skill/bilibili-notion-pipeline/scripts/pipeline.py cleanup \
  --metadata "<metadata_path>" \
  --mode temp
```

如果用户明确不要保留视频：

```bash
python skill/bilibili-notion-pipeline/scripts/pipeline.py cleanup \
  --metadata "<metadata_path>" \
  --mode all
```

## 进度回报要求

长任务不要静默卡住。

至少在这些节点主动回报：

1. 已解析视频 / 已开始下载
2. 已开始转写
3. 已上传并拿到 `download_url`
4. 已写入 Notion 正文
5. 已补文后总结
6. 已完成回读校验
7. 已清理 / 保留了哪些本地文件

## 上传后端约定（简版）

这个 skill 把上传后端视为**可替换组件**，但当前自用实践里常见的是：

- `https://stor.pull.eu.org/`

执行时只需要关心它是否满足下面几件事：

1. 能上传 mp4 并返回公开 `download_url`
2. 最好支持较大的视频文件
3. 最好支持分片上传，降低长视频失败率
4. 如果带 WebDAV 或等价文件管理能力，会更利于整理、迁移和备份

当前这套能力受益于下列项目提供的思路与实现基础：

- `https://github.com/MarSeventh/CloudFlare-ImgBed`

如果后端底层依赖 Telegram 群组 / 频道这类平台型存储，要默认认为它是：

- **高性价比** 的工程方案
- 但**不是零风险永久存储**

因此执行这条流程时，仍建议：

- 本地保留 metadata / transcript
- 是否删除本地 mp4，必须按用户明确偏好处理
- 不要把远端外链当成唯一副本

## 注意事项

- 不要把真实 token、cookies、profile、日志提交到仓库
- 官方字幕不可靠，默认准备 ASR 兜底
- 如果转写质量明显跑偏，不要硬写总结，先告知用户
- 更新已有页面时，只有在用户明确要求替换旧正文时才用 `--replace-children`
- 对外介绍时，优先把它说成 **Skill 仓库**；agent 能力属于增强层，而不是唯一身份
