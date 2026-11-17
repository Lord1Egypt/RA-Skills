# 批次工作区与输出规范

本文件是工作区结构、正式文件去向和用户交付消息的唯一详细规范。`SKILL.md`
只保留执行入口；Zotero 文档只说明文献管理器操作。

## 固定位置

主工作区固定在 Skill 内部：

```text
academic-pdf-translation/
└── Workspace/
```

每次用户提出一项翻译请求，就创建一个批次子目录。一次请求包含十篇论文时，
十篇共用一个批次；后续的新请求创建新批次，不混入旧目录。

批次名称：

```text
YYYYMMDD-HHMMSS_<数量>篇_<标题>
```

例如：

```text
20260726-183500_10篇_{批次标题}
```

数量由实际输入 PDF 计算，不由 Agent 手填。标题概括本次用户请求，不使用完整
提示词，也不加入质量档位、模型名或内部状态。

## 批次内部

```text
20260726-183500_10篇_{批次标题}/
├── input/
├── output/
└── .work/
    ├── batch.json
    └── jobs/
        ├── 论文A-<原文哈希前十位>/
        └── 论文B-<原文哈希前十位>/
```

Finder 默认只显示 `input/` 和 `output/`：

- `input/` 保存本批次原文副本，文件名尽量保持不变；
- `output/` 只保存通过用户所选质量档位验收的正式译本；
- `.work/` 保存翻译单元、复杂页载荷、候选 PDF、检查证据、对照图和历史版本。

不要在批次根目录放 PDF、报告或零散 JSON。不要把候选、审查报告、源译对照图
和“为什么翻译本文”等说明放进 `output/`。

## 创建批次

在 Skill 根目录运行：

```bash
python3 scripts/workspace.py create \
  --title "{批次标题}" \
  /path/to/paper-01.pdf \
  /path/to/paper-02.pdf
```

脚本完成四件事：

1. 在 `Workspace/` 下创建带时间、数量和标题的批次；
2. 把原文复制到 `input/`，不修改用户原文件；
3. 创建隐藏的 `.work/jobs/`；
4. 在 `.work/batch.json` 记录原路径、输入路径和 SHA-256。

相同文件不能在同一批次重复。不同来源存在同名 PDF 时，输入副本自动追加序号。

## 初始化单篇作业

对 `input/` 中每篇 PDF 运行：

```bash
python3 scripts/init_job.py \
  /path/to/Workspace/<批次>/input/paper-01.pdf \
  --workspace /path/to/Workspace/<批次> \
  --target-language zh-Hans \
  --review balanced \
  --producer-id producer-agent-01
```

作业固定写入该批次的 `.work/jobs/`。相同原文再次初始化时恢复已有作业，不创建
第二份。`job.json.workspace` 保存批次、输入、输出、隐藏过程和当前作业的绝对
路径，Agent 在上下文恢复后以这里为准。

旧项目已经存在独立作业目录时，可以继续使用兼容入口：

```bash
python3 scripts/init_job.py \
  /path/to/source.pdf \
  /path/to/job \
  --job-root /path/to/all-jobs
```

不要为了符合新目录而迁移已经在处理或已经验收的旧作业。

## 正式输出

只有作业达到 `accepted` 后，才把唯一正式译本复制到本批次 `output/`，并把
绝对路径和文件哈希写入该作业的 `finalization.json`。带工作区记录的新作业，
正式译本位于 `output/` 之外时不能进入 `finalized`。

文件名保留原文完整文件名前缀，并追加目标语言与质量档位：

- 简体中文快速档：`_中文译版.pdf`
- 简体中文平衡档：`_中文译版_审校版.pdf`
- 简体中文精细档：`_中文译版_精校版.pdf`
- 其他语言：使用稳定语言后缀，并保持同一批次一致

批次可以部分完成。此时 `output/` 只放已经验收的译本，未完成原因留在
`.work/`，不能用失败候选占位。

交付前运行：

```bash
python3 scripts/workspace.py outputs \
  /path/to/Workspace/<批次>
```

该命令列出 `output/` 中正式 PDF 的数量和绝对路径。Agent 用它核对最终回复，
不依赖记忆手写路径。

## 用户交付消息

最终回复必须同时交付文件和路径，使用以下最小结构：

```text
已完成：<已完成数>/<输入总数>
输出目录：<output 绝对路径>

文件：
- <正式译本文件名>：<正式 PDF 绝对路径>
```

在支持本地文件链接的客户端中，文件名必须链接到对应正式 PDF。多篇任务逐篇
列出，不用“其余同上”省略。存在未完成项时，再列出文件名和原因；不能只报一个
总数。

不要把 `.work/` 路径、内部 JSON、候选 PDF 或检查报告当成用户交付物。用户
明确要求检查材料时，再单独提供对应路径。
