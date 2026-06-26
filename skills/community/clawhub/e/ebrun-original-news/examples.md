# 使用示例集合 — 亿邦原创新闻

## 示例 1：自然语言触发 — 查询推荐频道最新文章

**用户输入：**

```text
查亿邦最新文章
```

**技能行为：**

1. 读取 `references/channel-list.json`
2. 因为用户没有明确指定频道，默认使用「推荐」频道
3. 调用：

```bash
python3 scripts/fetch_news.py "_index/ClaudeCode/SkillJson/information_recommend.json" --json --limit 10
```

**期望输出：**

```markdown
📰 亿邦原创新闻 | 推荐 最新
获取时间: 2026-04-20 10:30:00
---

**[文章标题 A](https://www.ebrun.com/...)**
作者A · 2026-04-20 09:00:00
文章摘要A

**[文章标题 B](https://www.ebrun.com/...)**
作者B · 2026-04-20 08:30:00
文章摘要B

---
更多资讯请见[亿邦官网](https://www.ebrun.com/)
```

---

## 示例 2：自然语言触发 — 查询主频道最新文章

**用户输入：**

```text
查跨境最新文章
```

**频道识别：**

- 主频道：`跨境电商`
- 子频道：`最新`
- `channel_path`：`_index/ClaudeCode/SkillJson/information_channel_51.json`

**实际调用：**

```bash
python3 scripts/fetch_news.py "_index/ClaudeCode/SkillJson/information_channel_51.json" --json --limit 10
```

**适用表达：**

- `查跨境最新文章`
- `跨境最新报道`
- `跨境新闻`

---

## 示例 3：自然语言触发 — 查询子频道文章

**用户输入：**

```text
查亚马逊新闻
```

**频道识别：**

- 主频道：`跨境电商`
- 子频道：`亚马逊`
- `channel_path`：`_index/ClaudeCode/SkillJson/information_channel_68.json`

**实际调用：**

```bash
python3 scripts/fetch_news.py "_index/ClaudeCode/SkillJson/information_channel_68.json" --json --limit 10
```

**同类例子：**

- `查抖音新闻` -> `未来零售 / 抖音`
- `看看AI新闻` -> `AI / 最新`
- `看品牌全球化报道` -> `品牌 / 品牌全球化`
- `产业有什么新动态` -> `产业互联网 / 最新`

---

## 示例 4：Python — 先匹配频道，再调用抓取脚本

```python
import json
import subprocess
from pathlib import Path

skill_dir = Path(".claude/skills/ebrun-original-news")
channel_file = skill_dir / "references" / "channel-list.json"

data = json.loads(channel_file.read_text(encoding="utf-8"))
channels = data["channels"]

# 例：用户说“看看AI新闻”
channel_path = channels["AI"]["sub_channels"]["最新"]

result = subprocess.run(
    [
        "python3",
        str(skill_dir / "scripts" / "fetch_news.py"),
        channel_path,
        "--json",
        "--limit",
        "10",
    ],
    check=True,
    capture_output=True,
    text=True,
)

articles = json.loads(result.stdout)
for item in articles[:3]:
    print(item["title"])
    print(item["url"])
    print()
```

**适用场景：**

- 在上层代理中复用本 skill
- 先做频道识别，再交给内置脚本处理
- 避免手写请求逻辑和域名校验逻辑

---

## 示例 5：Shell — 直接查看某个频道最新文章

```bash
# AI 频道
python3 scripts/fetch_news.py "_index/ClaudeCode/SkillJson/information_channel_88.json" --json --limit 5

# 品牌全球化频道
python3 scripts/fetch_news.py "_index/ClaudeCode/SkillJson/information_channel_90.json" --table --limit 5

# 使用完整 URL 也可以
python3 scripts/fetch_news.py "https://www.ebrun.com/_index/ClaudeCode/SkillJson/information_channel_57.json" --json --limit 5
```

**说明：**

- 默认输出 JSON
- 显式传 `--table` 时输出 ASCII 表格
- 支持传 `channel_path` 或完整 URL

---

## 示例 6：频道未命中时自动回退到推荐频道

**用户输入：**

```text
查宠物零售新闻
```

**处理逻辑：**

1. 在 `references/channel-list.json` 中找不到“宠物零售”对应频道
2. 自动回退到 `推荐 / 最新`
3. 继续抓取推荐频道前 10 篇文章
4. 返回友好提示，告诉用户当前展示的是推荐内容

**期望输出：**

```markdown
未找到"宠物零售"频道的文章，将为您展示推荐内容。

📰 亿邦原创新闻 | 推荐 最新
获取时间: 2026-04-20 10:35:00
---

**[文章标题 A](https://www.ebrun.com/...)**
作者A · 2026-04-20 09:00:00
文章摘要A

---
可用的频道有：
📰 推荐 | 🛒 未来零售 | 🌏 跨境电商 | 🏭 产业互联网 | 🏷️ 品牌 | 🤖 AI

更多资讯请见[亿邦官网](https://www.ebrun.com/)
```

---

## 示例 7：Python — 批量读取多个子频道并汇总标题

```python
import json
import subprocess
from pathlib import Path

skill_dir = Path(".claude/skills/ebrun-original-news")
channel_data = json.loads((skill_dir / "references" / "channel-list.json").read_text(encoding="utf-8"))

targets = {
    "亚马逊": channel_data["channels"]["跨境电商"]["sub_channels"]["亚马逊"],
    "抖音": channel_data["channels"]["未来零售"]["sub_channels"]["抖音"],
    "AI": channel_data["channels"]["AI"]["sub_channels"]["最新"],
}

for name, channel_path in targets.items():
    result = subprocess.run(
        [
            "python3",
            str(skill_dir / "scripts" / "fetch_news.py"),
            channel_path,
            "--json",
            "--limit",
            "3",
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    articles = json.loads(result.stdout)
    print(f"=== {name} ===")
    for article in articles:
        print("-", article.get("title", "无标题"))
    print()
```

**适用场景：**

- 做多频道热点对比
- 上层工作流想汇总多个电商赛道的最新动态
- 保持所有请求都复用 skill 自带脚本

---

## 示例 8：版本检查 — 判断 skill 是否需要更新

```bash
# 常规检查
python3 scripts/update.py --json

# 忽略本地检查间隔，强制检查远端版本
python3 scripts/update.py --json --force

# 以文本表格方式查看结果
python3 scripts/update.py --table
```

**典型返回字段：**

```json
{
  "skill_name": "ebrun-original-news",
  "current_version": "0.0.9",
  "latest_version": "1.0.0",
  "update_available": true,
  "check_source": "remote_api",
  "update_url_github": "https://github.com/Ebrun-Developer/ebrun-original-news",
  "update_url_gitee": "https://gitee.com/ebrun-developer/ebrun-original-news"
}
```

**后续动作：**

- 如果 `update_available` 为 `true`，在最终回复中追加更新提示
- 如果版本接口失败，脚本会自动降级到远端仓库版本文件检查
- 如果未到 `check_interval_hours`，脚本可能直接返回缓存结果

---

## 示例 9：错误处理 — 非法地址与请求失败

```bash
# 非授权域名，会被安全检查拒绝
python3 scripts/fetch_news.py "https://example.com/news.json" --json

# 参数错误：limit 不能小于 0
python3 scripts/fetch_news.py "_index/ClaudeCode/SkillJson/information_channel_88.json" --limit -1
```

**预期行为：**

- 非授权域名返回安全性错误
- 非法参数返回用法错误
- 404 / 503 / 超时会返回稳定错误信息和退出码

**设计目的：**

- 防止上层代理拼错域名或误请求外部地址
- 让 skill 在自动化场景下更容易被可靠调用

---

## 示例 10：在技能主流程中的完整调用链

**用户输入：**

```text
看品牌有什么新动态
```

**推荐执行顺序：**

1. 读取 `references/channel-list.json`
2. 将“品牌”识别到主频道 `品牌`
3. 默认选择子频道 `最新`
4. 调用：

```bash
python3 scripts/fetch_news.py "_index/ClaudeCode/SkillJson/information_channel_87.json" --json --limit 10
```

5. 将结果整理成 Markdown：
   - `title`
   - `author`
   - `summary`
   - `publish_time` 或 `publishTime`
   - `url`
6. 在后台独立调用版本检查：

```bash
python3 scripts/update.py --json
```

7. 如果有新版本，则在回复页脚追加更新提示

**这个示例最接近真实 agent 集成方式。**

---

## 编写建议

为上层代理或自动化任务接入本 skill 时，建议遵循以下约定：

1. 先读 `references/channel-list.json`，不要手写猜频道路径
2. 优先调用 `scripts/fetch_news.py`，不要临时自己写抓取代码
3. 默认取前 10 篇，和 `SKILL.md` 的输出约定保持一致
4. 将频道未匹配视为可恢复场景，自动回退到「推荐」
5. 将版本检查作为独立旁路流程，不要因为检查失败影响新闻返回
