---
name: gemini-openai-chat-export-analyze
description: 当用户要导出并分析与 Gemini(Google)或 ChatGPT(OpenAI)网页版的全部聊天历史时,加载本 skill。典型触发:用户提到 "导出 gemini 对话"、"gemini 聊天记录"、"chatgpt 数据导出"、"OpenAI conversations.json"、"我和 gemini/chatgpt 聊过什么"、"chatgpt 历史记录" 等。注意:本 skill 覆盖 ChatGPT 网页版与 Gemini 网页版(含 gemini.google.com 和 aistudio.google.com),不包括 API 调用记录或第三方客户端。
---

# Gemini / ChatGPT 聊天历史导出与分析

## 适用边界

本 skill 覆盖两个产品:

| 产品 | 路径 | 产物 | 文件格式 |
|---|---|---|---|
| **ChatGPT**(OpenAI) | Settings → Data controls → Export | ZIP,内含 `conversations.json` 等 | **JSON** |
| **Gemini**(Google) | Google Takeout → Gemini Apps | ZIP,内含 `My Activity/Gemini/*.html` | **HTML**(不是 JSON) |

**关键差异:ChatGPT 给 JSON,Gemini 给 HTML**——本 skill 两套都要处理。

---

# Part A:ChatGPT(OpenAI)导出

## A.1 引导文案(可直接复制)

> 把跟 ChatGPT 的全部对话导出,大概走这几步:
>
> 1. 打开 https://chatgpt.com(或 chat.openai.com)并登录
> 2. 右上角点你的**头像** → **Settings**
> 3. 左侧菜单选 **Data controls**
> 4. 找到 **Export your data** 区域,点 **Request export**
> 5. 弹窗里**勾上"Include chat history"**(这是必须项),点 **Confirm request**
> 6. **等 1~48 小时**——OpenAI 会把下载链接发到你**注册邮箱**
> 7. 邮件点链接下 ZIP,**链接 7 天后失效**,别拖
> 8. ZIP 里找 `conversations.json`
>
> 文件可能 10MB~1GB+,别打开,告诉我解压后的完整路径。

## A.2 文件结构(校验用)

```bash
# 顶层是 array
jq 'type' /path/to/conversations.json
# → "array"

# 总数
jq 'length' /path/to/conversations.json

# 单条 session 字段(实测是这些,版本可能小变)
jq '.[0] | keys' /path/to/conversations.json
# 预期: ["create_time","default_model_slug","id","mapping","moderation_results","title","update_time","user_id"]
```

注意 ChatGPT 的结构和 Claude **完全不同**:
- ChatGPT 用 **`mapping`**(嵌套树)而不是 `chat_messages`(线性数组)
- 时间戳是 **Unix timestamp(秒)**,不是 ISO 字符串
- 消息角色在 `mapping.[id].message.author.role` 里,值是 `"user"` / `"assistant"` / `"tool"`

## A.3 把 mapping 拍平为线性 messages

```bash
# 提取所有 user/assistant 消息,按树遍历顺序
jq -r '
  .[] as $c
  | $c.id as $cid
  | $c.title as $title
  | $c.create_time as $ct
  | [
      ($c.mapping | to_entries[]
        | .value.message
        | select(. != null and .author.role != "tool")
        | {
            sender: (.author.role | if . == "user" then "human" else . end),
            text: ([.content.parts[]? | select(type == "string")] | join("\n")),
            created_at: (.create_time // null)
          })
    ] as $msgs
  | $cid + "|" + ($ct | tostring) + "|" + $title + "|" + ($msgs | length | tostring)
' /path/to/conversations.json
```

## A.4 常见的 4 类问题(参考 Claude skill 里的 A-G 模板)

| 用户问题 | 对应处理 |
|---|---|
| 找关键词对话 | 用 jq 配合 `test()` 过滤 `text` 字段 |
| 列总览 | 用上面的"拍平"输出,按 create_time 排序 |
| 找强建议 | 搜 "我建议\|建议你\|不应该" |
| 找最长对话 | 排序 mapping 节点数 |

完整命令模板参见 `claude-chat-export-analyze` skill——结构差异处理完,**jq 关键词搜索/时间线/主题提炼的逻辑完全通用**。

---

# Part B:Gemini(Google)导出

## B.1 引导文案(可直接复制)

> 把跟 Gemini 的全部对话导出,大概走这几步:
>
> 1. 打开 https://myaccount.google.com 并登录
> 2. 左上角菜单点 **数据和隐私**
> 3. 向下滚到 **数据下载**(或"下载你的数据")区域,点进入 **Google Takeout**
> 4. **取消全选**,只勾 **"我的活动"**(My Activity)
> 5. 点"我的活动"右边的下拉,**确认"Gemini Apps"子项已勾选**——只勾"Gemini"不一定包含完整对话
> 6. 点 **下一步**,选 **一次性导出**、**.zip 格式**、大小 1~2GB/卷
> 7. 点 **创建导出**
> 8. **异步处理,可能几小时到几天**,完成后 Google 邮箱会收到下载链接
> 9. 下载 ZIP,解压后看 `My Activity/Gemini/` 目录,里面是 **HTML 文件**(不是 JSON)
>
> 提示我解压后的目录路径(整目录,不只是单个文件)。

## B.2 文件结构(HTML 格式)

Gemini 导出的是 **HTML 不是 JSON**——这是最大的坑。

```bash
# 先看目录里有什么
ls /path/to/My\ Activity/Gemini/

# 典型:My\ Activity.html 是单文件聚合,或者 Gemini\ Apps.html 等分文件
# 文件结构:每个 <div class="outer-cell"> 是一个对话轮次
```

## B.3 HTML → 结构化文本

用 python 快速解析:

```python
from bs4 import BeautifulSoup
from pathlib import Path
import json, re

src = Path("/path/to/My Activity/Gemini")
out = []
for html_file in src.glob("*.html"):
    soup = BeautifulSoup(html_file.read_text(encoding="utf-8"), "html.parser")
    # 提取每条对话
    cells = soup.find_all("div", class_=re.compile(r"outer-cell|content-cell"))
    for cell in cells:
        text = cell.get_text("\n", strip=True)
        out.append({"file": html_file.name, "text": text})

print(json.dumps(out, ensure_ascii=False, indent=2))
```

或用 `html2text`:

```bash
html2text "/path/to/My Activity/Gemini/My Activity.html" > /tmp/gemini.txt
# 然后用 grep 搜
grep -n "我建议\|离职\|辞职" /tmp/gemini.txt
```

## B.4 Gemini 导出的局限

⚠️ 跟 ChatGPT / Claude 相比,Gemini 导出有**几个明显短板**:

1. **HTML 格式,不能直接 jq**——必须先解析
2. **没有结构化的 role 字段**——要靠 DOM 节点区分"用户问题"和"Gemini 回复"
3. **时间戳可能不准确**——Takeout 导出时区处理有时出问题
4. **附件/图片元信息缺失**——Google 通常把附件归到独立 Drive 文件,不在 Takeout 里

如果用户要做严肃分析(时间线/语义检索),**建议额外说明**这些局限,或让用户优先用 ChatGPT/Claude 那边。

---

# Part C:跨平台统一分析(用户同时导出了多个时)

如果用户同时给了 Claude + ChatGPT + Gemini 三份数据,做"跨平台时间线"时:

## C.1 把三家产物统一到同一份 JSONL

```python
import json, sys, re
from pathlib import Path
from datetime import datetime, timezone

def normalize(rec):
    """统一字段:sender, text, created_at, source, session_id, session_name"""
    return {
        "sender": "assistant" if rec["sender"] in ("assistant", "model", "gemini") else "human",
        "text": rec["text"],
        "created_at": rec["created_at"],
        "source": rec["source"],  # "claude" / "chatgpt" / "gemini"
        "session_id": rec["session_id"],
        "session_name": rec["session_name"],
    }

# 然后写出 jsonl
with open("/tmp/unified.jsonl", "w", encoding="utf-8") as f:
    for rec in records:
        f.write(json.dumps(normalize(rec), ensure_ascii=False) + "\n")
```

## C.2 跨平台查询

```bash
# 在所有平台上找"离职"相关
grep -E "离职|辞职|跳槽" /tmp/unified.jsonl | head -20

# 按平台分布
jq -r '.source' /tmp/unified.jsonl | sort | uniq -c

# 按月份聚合
jq -r '.created_at[0:7]' /tmp/unified.jsonl | sort | uniq -c
```

---

# Part D:安全与隐私(必须告知)

- ChatGPT 导出里**包含 user.json**,里面有用户邮箱、账号信息
- Gemini 导出里可能包含 Google 账户关联的**其他活动记录**(搜索、YouTube)
- 一律建议用户**导出任务完成后移出工作目录**
- 输出报告时**默认对邮箱/手机/身份证/银行卡打码**

---

# Part E:常见坑(踩过标这里)

- ❌ **ChatGPT 的 conversations.json 顶层是 array,但 mapping 字段是嵌套 dict**——别用 `.chat_messages[]` 这种 Claude 习惯的语法
- ❌ **ChatGPT 时间戳是 Unix 秒数,不是 ISO 字符串**——`1633072800` 这种,需要 `| todate` 转
- ❌ **Gemini 是 HTML,不是 JSON**——`jq` 没法直接处理,先转文本
- ❌ **ChatGPT 导出的 `message_feedback.json` 包含用户 thumbs up/down**——隐私敏感,不要 echo
- ✅ **三家产物的时区都是 UTC**——跨平台对照时统一换算到用户本地时区
- ✅ **如果文件 > 500MB,优先按时间窗口分片**——不要一次性 cat/jq
- ✅ **ChatGPT mapping 可能含 "current_node" 链,要把这条链的节点按顺序拍平,不是 to_entries 的字典序**
