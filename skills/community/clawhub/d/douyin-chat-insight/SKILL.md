---
name: douyin-chat-insight
version: 0.2.1
description: "分析用户自备的群聊/私聊导出（含抖音群），生成单页会话价值报告（硬事实、矛盾、需求原话、动作）。零 IM 登录、不强制云 Key。触发：douyin-chat-insight、抖音聊天转知识库、群聊洞察、chat export insight。"
---

# Douyin Chat Insight（抖音聊天转知识库）

## 一句话

把**用户已经拥有**的聊天导出，变成一页可执行情报（Chat → Insight）。

## 何时使用

- 用户提供群聊/私聊 **JSONL / JSON / 文本导出**，要提炼价值、需求、矛盾、待办
- 社群主理人要「需求原话墙」而不是凭感觉运营
- 与公开作品分析（creator-insight）对照：主页承诺 vs 群里真实问题

## 何时不要使用（路由）

| 用户意图 | 去向 |
|----------|------|
| 公开抖音主页 / 作品结构 | `douyin-creator-insight` |
| 主页批量视频文案 | `douyin-video-analyst` / `douyin-workflow` |
| **静默登录拉群 / 要采集凭据** | **拒绝**；说明边界；指向 how-to-get-exports（可选自备） |
| 单条分享视频 ASR | 可选端口说明 → `references/optional-douyin-link-asr.md` |

## 硬边界

- **不**在 skill 内登录 IM、扫码、读 cookie、启 Docker 导出器
- **不**把第三方导出器打进安装依赖
- 主路径：**零阿里百炼 AppKey**
- 若检测到兄弟 skill 或 `DASHSCOPE_API_KEY`：只展示，不读取收藏账本、不抢 browser profile、不强制复用
- **可选 ASR 端口**：聊天中的抖音链接默认只识别；用户要转写时给配置指导，不在核心 `run.py` 强制云调用

## 状态机（必须遵守）

```
输入路径
  → load_export
  → inventory（概况表）
  → 【停止】等待用户指定：会话# / 会话名 / 人物
  → 仅当显式 --conv（或等价指定）才 analyze
  → quality_gate
  → 写 HTML / MD / JSON
```

**没有会话对象，禁止直接深挖全库「假装已完成」。**

## 标准命令

```bash
python3 scripts/doctor.py
python3 scripts/setup.py
python3 scripts/setup.py --check --json
python3 scripts/run.py -i <导出文件或目录>
python3 scripts/run.py -i <导出> --conv 1 --owner-alias '群主昵称'
python3 scripts/run.py -i <导出> --conv 1 --person '某人' --json
```

报告默认目录：`output/douyin-chat-insight/`（可用 `-o` 改）。
人类终端会打印「本机打开」绝对路径；**JSON 内路径已脱敏**。

## Agent 话术

**首次：**

> 我可以分析你自备的聊天导出，生成需求原话与动作清单。请给我文件路径。
> 不需要登录聊天软件，也不需要阿里百炼 Key（除非你还要对消息里的抖音链接做转写）。

**仅有路径、用户未指定会话：**

> 先出概况表。请回复要深挖的会话编号，例如：会话 #1。

**用户要爬群：**

> 我不能替你登录或静默采集。你可以自己导出后把文件给我；可选工具说明见 references/how-to-get-exports.md。

**用户要分析抖音链接：**

> 文字四块报告不依赖百炼。链接转写是可选增强，见 references/optional-douyin-link-asr.md。

## 质量门

- inventory 会话非空
- 深挖必须显式会话对象
- 四块不能全空
- 不在报告/仓库写入 cookie、token、私人绝对路径

发布前本机：`python3 scripts/doctor.py`（期望 `RESULT: READY`）。

## 输出约定

- `hard_facts` / `open_contradictions` / `demand_quotes` / `actions`
- `optional_enhancements`：抖音链接端口状态与中文指导
- `meta.note`：启发式草稿，须终审

## 版本

v0.1.5 · MIT · 源码 https://github.com/tars1230/douyin-chat-insight
