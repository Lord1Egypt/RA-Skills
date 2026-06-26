# fanqie-novel-auto-publish
# 番茄小说创作发布一条龙技能

整合 `open-novel-writing`（AI 创作）+ `fanqie-publisher`（番茄发布），从想法一键生成到发布到番茄小说。

## 完整流程

```
想法 → 设定 → 大纲 → 生成多章 → 评审修订 → 自动发布到番茄小说
```

## 工作原理

技能目录下包含两个核心模块：

| 模块 | 文件 | 说明 |
|------|------|------|
| `novel_generator` | `novel_generator.py` | 调用 AI 生成小说章节 |
| `fanqie_publisher` | `fanqie_publisher.py` | 调用 fanqie-publisher 发布章节 |
| `auto_publish` | `auto_publish.py` | 编排完整工作流 |

## 使用方式

### 命令行发布

```bash
cd ~/.openclaw/skills/fanqie-novel-auto-publish/scripts
python auto_publish.py --check          # 检查状态
python auto_publish.py --works          # 列出作品
python auto_publish.py -w "作品名" -f "章节.md"   # 发布单章
```

### Python 调用

```python
import sys
sys.path.insert(0, "~/.openclaw/skills/fanqie-novel-auto-publish/scripts")

from auto_publish import AutoPublishWorkflow

workflow = AutoPublishWorkflow()

# 检查状态
status = workflow.check_status()

# 发布章节
result = workflow.publish_chapter(
    work_title="诡异系统：我在规则世界卡BUG",
    chapter_file="C:/path/to/chapter.md"
)
```

## 依赖

- `open-novel-writing` 技能（生成小说内容）
- `fanqie-publisher` 技能（发布到番茄小说）

这两个技能需要先安装并配置好。

## 工作目录

- 小说输出：`~/.openclaw/skills/novel-generator/output/`
- 记忆文件：`~/.openclaw/skills/novel-generator/.learnings/`
- Cookie 文件：`~/.openclaw/skills/fanqie-publisher/scripts/fanqie_cookies.json`

---

企业开发·定制技能请联系Wx：CChenJ_
