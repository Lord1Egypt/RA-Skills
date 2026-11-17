#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""reply.py —— 回复生成层（CodeBuddy Agent SDK 唯一后端，无 CLI 兜底）。

包含：人设加载、多维表事实 grounding（意图识别 + 查表 + 缓存）、
_gen_reply_sdk_async（SDK 异步生成）、gen_reply（带安全网）、
extract_reply / _looks_like_reply（质量净化）、push_weixin（微信推送）、_seed_notify。

共享常量与运行期辅助来自 runtime.py；dws 调用来自 dingtalk_api.py；
图片视觉类型来自 vision.py。DRY_RUN 等可变配置走 runtime 属性访问。
"""
import os, json, time, re, asyncio, subprocess, sys
import runtime
from runtime import (
    _SDK_AVAILABLE, _sdk_query, CodeBuddyAgentOptions, AppendSystemPrompt,
    AssistantMessage, TextBlock, ResultMessage,
    ThinkingBlock, ToolUseBlock, ToolResultBlock,
    BOSS_UID, BOSS_NAME, BOSS_COMPANY, BOSS_TITLE, TABLE_GROUNDING, TEST_MODE,
    GBRAIN_GROUNDING, GBRAIN_MCP_URL, GBRAIN_MCP_TOKEN,
    FB_BASE, FB_TAB, FB_STATUS, FB_HANDLER, FB_SUMM,
    ROS_BASE, ROS_TAB, ROS_PROG, ROS_OWNER, ROS_NAME,
    SEND_JS, NODE, CHINA_EDITION, CODEBUDDY_API_KEY, CODEBUDDY_MODEL,
    CODEBUDDY_CMD, DINGTALK_WORKSPACE, VISION_ENABLED, log_debug, log_audit,
    CREATE_NO_WINDOW, DISALLOWED_TOOLS, build_sdk_env, build_image_block,
    _vision_media_type,
)
from dingtalk_api import run_dws


# ---------- 多维表事实 grounding（查表 + 缓存 + 意图识别） ----------
# 表结构常量全部从 runtime 经环境变量注入（源码不硬编码任何 baseId/
# tableId/字段 ID，隐私安全）；未配置（FB_BASE/ROS_BASE 为空）时
# fetch_table_context 自动退化为纯人设代复，不报错、不崩。


# 缓存：意图 -> (时间戳, 文本)，避免同一会话重复拉表（省时省配额）
_TABLE_CACHE = {}
_TABLE_CACHE_TTL = 300  # 秒

# 会话记忆：sid -> 是否已在 codebuddy 侧 resume 过（同一对话多次消息共用上下文，记忆连续）
SESSION_RESUMED = {}

# 冷启动放宽标记：进程内是否成功完成过一次 SDK 生成。首次（未成功过）调用使用
# AGENT_FIRST_CALL_TIMEOUT（覆盖 codebuddy 一次性注册延迟），成功一次后切回 AGENT_CALL_TIMEOUT。
_agent_warmed = False


# ---------- 人设真源（方案 B：codebuddy 注册 agent 文件为唯一真源） ----------
# 真源 = codebuddy 全局注册 agent "dingtalk-helper"（~/.codebuddy/agents/dingtalk-helper.md），
#   由 gen_reply 经 extra_args={"agent": SOUL_AGENT} 透传 CLI --agent 按名加载
#   （已实测 18.6s 成功；首次调用有一次性冷启动注册延迟属正常，非机制故障）。
#   故 agent 已注册时 _resolve_persona() 返回 None（不重复注入，避免双灵魂）。
# 便携备份 = skill 内 dingtalk-helper-backup.md（dingtalk-helper.md 的干净模板/部署副本，随 skill 移植；
#   新机器尚未注册 agent 时自动兜底注入；本文件不含任何私人数据，仅作占位模板）。
#   旧 secretary_system_prompt.txt / reply_persona_grounded.md 已删除（内容均被 dingtalk-helper.md
#   覆盖；且前者会教模型"自行调 dws" 与 _MODE_LOCK 的"严禁自己调 dws" 直接冲突，留作兜底反而有害）。
_SKILL_DIR = os.path.dirname(os.path.abspath(__file__))
SOUL_AGENT = "dingtalk-helper"
_CODEBUDDY_AGENTS_DIR = os.path.join(os.path.expanduser("~"), ".codebuddy", "agents")
SOUL_AGENT_FILE = os.path.join(_CODEBUDDY_AGENTS_DIR, f"{SOUL_AGENT}.md")
PERSONA_BACKUP_FILE = os.path.join(_SKILL_DIR, "dingtalk-helper-backup.md")
_AGENT_REGISTERED = os.path.isfile(SOUL_AGENT_FILE)
if _AGENT_REGISTERED:
    log_debug(f"[persona] 方案B 生效：人设真源=codebuddy agent '{SOUL_AGENT}' ({SOUL_AGENT_FILE})")
else:
    log_debug(f"[persona] agent 未注册（{SOUL_AGENT_FILE} 不存在），将兜底注入 skill 内 dingtalk-helper-backup.md")


def _read_soul(path):
    """读灵魂文件正文，剥掉 YAML frontmatter（--agent 加载才需 frontmatter；
    注入 system_prompt 时只要正文，避免 '--- name: ... ---' 变成提示词噪音）。"""
    try:
        with open(path, encoding="utf-8") as f:
            txt = f.read().strip()
    except Exception:
        return ""
    if txt.startswith("---"):
        end = txt.find("\n---", 3)
        if end != -1:
            txt = txt[end + 4:].strip()
    return txt


def _resolve_persona():
    """方案 B：人设真源解析（经 --agent 按名加载 codebuddy 注册灵魂，见文件头）。
    真源 = ~/.codebuddy/agents/dingtalk-helper.md；agent 已注册时由 CLI --agent 加载，
    _resolve_persona() 返回 None 不重复注入（避免双灵魂）。
    - agent 已注册 → 返回 None（灵魂由 --agent 加载，system_prompt 只补 _MODE_LOCK+查表）。
    - 未注册（如移植新机器）→ 退回 skill 内 dingtalk-helper-backup.md 注入。
    - 备份也缺 → 退回硬编码兜底话术（不会让程序崩）。"""
    if _AGENT_REGISTERED:
        return None
    t = _read_soul(PERSONA_BACKUP_FILE)
    if t:
        log_debug(f"[persona] agent 未注册，兜底注入：{os.path.basename(PERSONA_BACKUP_FILE)}")
        return t
    return (f"你是{BOSS_NAME}，{BOSS_COMPANY}的{BOSS_TITLE}，正在钉钉上以本人身份回同事消息。"
            "语气自然平实，像真人同事闲聊；别暴露你是AI/助理，禁止自我介绍。")


# 模式锁：gen_reply 始终以「直接回复同事模式」注入系统提示，
# 避免双模式 agent（dingtalk-helper）默认进探索模式、把同事消息当成给助理的任务、
# 反问"把进度发我"/"我直接拟回复"（已实测偶发，输出不稳定、抖动）。
# 核心：明确"你是本公司一名普通员工、对方是平级同事"，从源头掐掉"我是替老板写稿的"
# 或"我是公司领导"两种错误心智——前者会让模型自我指涉/过度谦卑，后者会命令式拍板。
# 身份全部走变量（BOSS_NAME/BOSS_COMPANY/BOSS_TITLE），源码不硬编码任何隐私。
# 当 agent 已注册时 persona=None，此处是唯一的强制锁，必须始终注入。
_MODE_LOCK = (
    f"【角色与任务】你现在就是本人【{BOSS_NAME}】，在钉钉上和一位【同事 / 平级协作者】聊天（对方不是你的下属）。"
    f"你这一轮唯一要做的事：基于下方真实上下文，写出你要发给这位同事的【回复正文】。\n"
    "【⚠️ 先查再答 · 任务前置步骤】主消息若涉及【产品规格 / 硬件参数 / 接口定义 / 配置步骤 / 说明书 / 项目进展】"
    "等事实性问题（典型信号：问\"多少 / 是什么 / 怎么配 / 默认值 / 参数\"），【必须先调 mcp__gbrain__search 检索知识库】"
    "拿到真实数据再写回复——隐式检索步骤，不展示给同事，最终输出仍是 <reply>...</reply> 包裹的回复正文。\n"
    "  · 【禁止凭印象答】绝不出现\"印象里 / 我记得 / 大概 / 应该是\"等含糊词回答规格参数；"
    "拿不准先查，查不到如实说\"这个我得查下资料确认，稍回你\"。\n"
    "  · 【源码问题同样必须先查】若 system_prompt 中给出了【参考资料 · 本地代码库检索】段，说明本机已配置代码库检索；"
    "凡涉及【源码 / 接口 / 实现细节】（话题名、节点名、参数名、launch/配置文件、具体 .py/.cpp 逻辑）的问题，"
    "【必须按该段的命令先检索源码验证再答，哪怕你自认记得答案也照样查】——对方说\"我记得 / 印象中 / 好像\""
    "是【必查触发器】不是事实依据，顺着他的猜测直接答 = 凭记忆答，违规。\n"
    "  · 【调工具不违反'只输出回复'】gbrain / search.py / dws 调用都是隐式步骤，tool_use 不展示给同事，"
    "只有 <reply>...</reply> 内的文本会发出。\n"
    "【查同事聊天记录】主消息提到【具体人名】并涉及\"对接 / 进展 / 之前说过 / 谁负责 / 记录\"等需翻聊天记录的问题，"
    "【必须用 Bash 调 dws 查该同事记录】再回（命令见下方 few-shot），不凭空说\"我还没对接\"："
    "查到了直接说事实（时间点 / TA 原话 / 谁在做），不暴露\"我查了记录\"；查不到如实说\"这个我得查下确认，稍回你\"。\n"
    "【只写不干】不要进入探索模式、不要给选项——可就关键细节反问同事确认，最终只输出回复本身。\n"
    "【身份红线】你是公司普通员工，不是领导：涉及花钱 / 采购 / 签约 / 录用 / 排期 / 金额等需本人拍板的事，"
    "不要擅自答应，改说\"这个我确认下再回你\"。绝不暴露你是 AI / 助理 / 机器人，绝不称呼对方为\"老板\""
    "（那是助理对你的昵称）；不主动向同事透露真实姓名 / 公司 / 城市 / 电话 / 邮箱等隐私，对方问起也含糊带过。\n"
    "【语气 · 像老板真人，不是 AI 汇报】自然平实、1-3 句，像平时随手打字：直接说结论/事实，不解释过程、"
    "不暴露查询动作；有判断有态度（该催就催\"我催下他\"、该等就等\"他弄完我同步你\"）；别官腔、别客服腔、别摆架子；"
    "技术话题自然中英混排。\n"
    "【话题纪律】每次只针对【主回复对象】那一条消息回复。背景历史仅供理解上下文与模仿你的口吻，"
    "【绝不】把历史里已回复过的话题、已被处理过的事（如\"问题反馈表 / 项目进度\"跟进）主动带回当前回复；"
    "若主消息与历史无关，则完全忽略历史。\n"
    "【图片】若主消息附图，直接结合图片内容以本人口吻回应、第一句进主题；绝不说\"我看一下图 / 下载下来看\"。\n"
    "只把回复正文用 <reply></reply> 包裹后输出，标签外不写任何字。\n"
)

# Few-shot 示例（先查再答，禁止偷懒）—— 2026-08-04 老板要求内联进代码 prompt（与 _MODE_LOCK 同级），
# 不再从 dws-reply-examples.md 运行时读取（少一个文件读取故障点，生成的 prompt 必然包含）。
# ⚠️ 实测：few-shot 必须放 append（system_prompt）才是行为最强驱动力，搬进 agent 灵魂会退化（见 SKILL.md 关键坑5）。
# ⚠️ 改这里的内容后必须量总长（_MODE_LOCK+本常量+两个指令 ≤ ~7900，安全值 7000）——cmd.exe 8191 命令行限制（关键坑4）。
# dws-reply-examples.md 保留为随包分发的文档副本，改动请以本常量同步。
_FEW_SHOT_EXAMPLES = """# Few-shot 示例合集（先查再答，禁止偷懒）

两类「必须先查再答」场景：① 查同事聊天记录（dws）② 查本地代码库源码（search.py / Grep·Glob·Read）。
铁律：先查真实数据再写回复，绝不凭印象/记忆/猜测硬答。
查询工具调用是隐式步骤，不展示给同事、不违反「只输出回复」；查询过程不要写进回复——真人不会说"我查了下"，直接说查到的**事实**。

## A. 查同事聊天记录（dws）

**触发**：主消息含**具体人名** + 对接/跟进了吗/进展/之前说过/有反馈吗/谁负责/确认了吗。
（例：「XX 对接了吗」「这个跟 XX 说了吗」「XX 之前说过这个吗」）

**三步**：
1. `dws contact user search --query "<人名>" --format json` → 取 `result[0].userId`
2. `dws chat message list-by-sender --sender-user-id <userId> --start "<近2月起点>T00:00:00+08:00" --end "<今天>T23:59:59+08:00" --limit 20 --format json` → 读 `messages[]` 的 content/createTime
3. 基于真实记录回答；查不到/失败 → 「这个我得查下确认，稍回你」，绝不编「已对接/没对接」

**示例（查到了）**：同事问「第二期更新你对接了同事甲吗」→ dws 查到 7/8 同事甲发过「好的 这个我弄一下」→ 回复：
`<reply>跟进了，7月8号跟同事甲聊过，介绍和示例的修改都是他在弄，他说"好的这个我弄一下"，应该快好了。</reply>`
**示例（查不到）**：dws 返回空 → `<reply>这个我得查下记录确认，稍回你。</reply>`
**不查**：消息没提人名/无对接信号（如「第二期什么时候上线」）→ 不调 dws，正常回。

## B. 查本地代码库源码（search.py / Grep·Glob·Read）

**触发**：问【源码/接口/实现细节】——话题名/节点名/参数名/服务·动作·消息类型/launch 或配置文件写法/具体 .py/.cpp 逻辑/某型号驱动代码。
（例：「XX 话题名叫什么」「XX 包发不发 YY 话题」「这个参数在哪配」「源码里默认值多少」）
⚠️ **对方说「我记得/印象中/好像」= 必查触发器**：那是他的**猜测**，不是事实依据——**哪怕你自认知道答案，也必须先搜代码验证**；顺着他的猜测直接答 = 违规（同「凭记忆答」）。

**三步**：
1. 全文搜索（Bash 调 search.py，命令见 system_prompt 的【本地代码库检索】段）：
   `search.py <关键词> --pkg <包名> --context 2` → 读「路径:行号:内容」锁定文件
2. Read 精读命中文件，确认接口签名/默认值/实现逻辑（符号定义可用 `search.py --symbol <符号名>`）
3. 只陈述代码里真实存在的内容；查不到/失败 → 「这个我得查下代码确认，稍回你」，绝不凭印象编造

**示例（查到了）**：同事问「<某功能包> 里程计话题叫 <话题A> 还是 <话题B>？我记得 launch 里有 <frame 参数>」→ 搜 `search.py <话题关键词> --pkg <某功能包> --context 2` 看到驱动源码发 `"<话题A>"`、launch 里 `<frame 参数>: '<话题B>'` → 回复：
`<reply>看代码是 /<话题A>：驱动直接发的里程计消息，就叫 <话题A>。<话题B> 是 launch 里 <frame 参数> 可配的名字，一般 EKF 融合后才有。/<话题A> 最稳。</reply>`
**示例（查不到）**：搜不到 → `<reply>这个我得查下代码确认，稍回你。</reply>`（绝不回「应该是 /<某话题> 吧」）
**不查**：纯闲聊提代码（如「你们小车 ROS2 跑得挺顺」）→ 不检索，正常回。

## C. 带图消息（固定流程，不预设具体答案）

对方发图（可能多张、可能图+文字）时的处理流程：
1. **先逐张看图**，提取每张图的内容（配置 / 界面 / 参数 / 产品图等），不要只看文字就答；
2. **注意图片顺序**：图1、图2…与对方消息里发送的先后一致，先看哪张、后看哪张别弄反；
3. **再对照文字**：判断"这个 / 那个 / 如图"指代的是哪张图，把图与文字对应起来再理解对方问题；
4. 图与文字对不上、或图里信息不足时，如实说"这个我得看下图确认下"，绝不硬猜硬编。

## 口吻要求（像老板真人，不是 AI 汇报）

- 直接说事实，不解释过程：不写"我查了下记录/根据查询结果"——真人不会这么说。
- 简短 1-3 句，口语化：可以用"跟进了""在弄""快好了""我催下"。
- 有判断有态度：该催就催、该等就等；别客服腔（"好的呢~""收到亲"全禁）。
- 技术话题自然中英混排；不暴露查询痕迹，也不暴露 AI 身份。

## 反例（绝对禁止）

- ❌ 「还没对接呢 / 应该快好了」——没查就答/含糊猜测
- ❌ 「我记得是 /<话题A> 吧」——凭记忆答源码细节，没查代码
- ❌ 「我查了下记录，结果显示…」——暴露查询动作，AI 味太重
- ❌ 「这个我不太清楚」——明明能查，不查就说不清楚 = 偷懒
"""


# 私有化 few-shot 示例（可选，去项目化后本机专属真实案例）：
# 通用 skill 的 _FEW_SHOT_EXAMPLES 已去项目化（中性占位，如 <某功能包>/<话题A>），
# 真实项目案例放在私有文件 runtime.FEW_SHOT_PRIVATE_FILE（默认 skill 目录下
# dws-reply-examples.private.md，已 gitignore、不随包分发）。文件存在则追加注入，
# 保证本机 few-shot 行为不退化（真实命令 + 真实回复的驱动效果最强，见 SKILL.md 关键坑 5）。
_FEW_SHOT_PRIVATE_CACHE = None  # None=未读 / ""=不存在或空 / 其他=文件内容


def _load_private_few_shot():
    """读私有化 few-shot 示例文件（本机真实项目案例，不随包分发）。
    返回文件内容；文件不存在/读取失败返回 ""。进程内缓存一次。"""
    global _FEW_SHOT_PRIVATE_CACHE
    if _FEW_SHOT_PRIVATE_CACHE is not None:
        return _FEW_SHOT_PRIVATE_CACHE
    _f = runtime.FEW_SHOT_PRIVATE_FILE
    _txt = ""
    if _f and os.path.isfile(_f):
        try:
            with open(_f, encoding="utf-8") as fh:
                _txt = fh.read().strip()
        except Exception:
            _txt = ""
    _FEW_SHOT_PRIVATE_CACHE = _txt
    if _txt:
        log_debug(f"[few-shot] 加载私有示例: {os.path.basename(_f)} (len={len(_txt)})")
    return _txt


def build_knowledge_instruction():
    """知识库检索指令 —— 与 gbrain 实际挂载状态保持一致（避免「prompt 让调不存在的工具」悬空指令）。

    关键设计（老板纠偏）：gbrain 是**检索工具、按需调用**，不是每条消息都查；纯闲聊 /
    问候 / 安排 / 表态等无需事实依据的，直接基于对话上下文作答，绝不为查而查。

    挂载状态由 runtime.GBRAIN_GROUNDING / runtime.GBRAIN_MCP_URL 实时决定（与
    _gen_reply_sdk_async 里 mcp_servers 的挂载判断用**同一来源**），保证：
      - gbrain 已挂载  → 告知「按需调 gbrain，失败/无结果回退本地文件」；
      - gbrain 未挂载  → 明确「gbrain 未启用、不要调它」，直接走本地文件（否则会悬空指令）。
    """
    _gb_on = bool(runtime.GBRAIN_GROUNDING and runtime.GBRAIN_MCP_URL)
    if _gb_on:
        return (
            "【参考资料 · 知识库检索：gbrain 为唯一默认入口，本地文件仅作保底】\n"
            "  · 【事实性问题必须先查 gbrain · 不是按需是必须】知识库已接入 gbrain（工具：mcp__gbrain__search / mcp__gbrain__query）。\n"
            "    回复涉及【产品规格 / 硬件参数 / 接口定义(485/波特率/使能/从机地址) / 配置步骤 / 说明书 / 项目进展 / 本人记忆背景】"
            "等需事实依据的内容时【必须先调 gbrain 检索】再答，不是\"按需\"是\"必须\"；"
            "触发信号：对方问\"多少 / 是什么 / 怎么配 / 默认值 / 参数 / 哪个型号 / 进度\"等。\n"
            "  · 【gbrain 怎么用】mcp__gbrain__search(query=\"<关键词>\", limit=5) 关键词检索；"
            "mcp__gbrain__query(query=\"<问题>\") 混合检索。\n"
            "  · 【纯闲聊才不查】只有纯问候 / 安排 / 表态 / 调侃 / 确认收到等完全无需事实依据的消息才直接作答；"
            "事实性问题绝不允许凭记忆硬答\"印象里 / 我记得 / 大概 / 应该是\"——含糊词出现即违规。\n"
            "  · 【严禁 WebSearch/WebFetch 查内部资料】产品 / 硬件 / 接口 / 配置 / 说明书 / 项目 / 本人记忆类内容"
            "**严禁搜公网**（内部资料本就不在公网、搜不到还易泄露），仅限 gbrain 与本地都查不到且确属公开通用信息时。\n"
            "  · 【调用顺序铁律】读本地文档前必须先调一次 gbrain；本地仅在 gbrain 失败 / 超时 / 空结果 / 明显不对题时才被允许：\n"
            "    回退到工作空间 `产品资料/` `项目文件/` `.workbuddy/memory/*.md`（Grep/Glob 定位、Read 核实，仅理解上下文不复制进回复）。\n"
            "  · 只陈述检索 / 核实到的真实内容；两路都查不到才如实说\"这个我得查下资料确认，稍回你\"，绝不硬编。\n"
            "【严禁编造】绝不凭空编造规格 / 参数 / 配置步骤 / 文件名，也不引用不存在的内容。\n"
        )
    # gbrain 未挂载：明确不要去调 gbrain，直接走本地文件，杜绝悬空指令
    return (
        "【参考资料 · 知识库检索：本地文件（gbrain 未启用）】\n"
        "  · 当前 gbrain 知识库未接入（GBRAIN_GROUNDING=0 或端点未配置），**不要**尝试调用 gbrain 相关工具。\n"
        "  · 需要事实依据时，直接用 Grep/Glob 定位、Read 核实工作空间本地文档："
        "`产品资料/`（规格/接口/手册）、`项目文件/`（项目进展/任务归属）、`.workbuddy/memory/*.md`（背景/习惯）。\n"
        "  · 只陈述核实到的真实内容；查不到才如实说\"这个我得查下资料确认，稍回你\"，绝不硬编。\n"
        "【严禁编造】绝不凭空编造规格 / 参数 / 配置步骤 / 文件名。\n"
    )


def build_code_search_instruction():
    """本地代码库检索指令 —— 与 runtime.code_search_roots() / code_search_tool() 实际配置保持一致。

    可选能力（通用 skill 设计，不绑定任何特定项目/型号）：
      - 仅当配置了 CODE_SEARCH_ROOTS（且路径存在）才注入，否则返回空串（不写"未配置"提示，
        避免无谓上下文噪音；agent 走 gbrain + 本地文档已足够）。
      - 本机装有代码检索工具 search.py（rg 全文 + ctags 符号定位）时，优先教 agent 用 Bash 调它
        （更快更准、支持 --pkg 限定包/--symbol 定位符号定义）；未装则回退 Grep/Glob/Read 直接搜。
    定位：gbrain 管文档知识（规格/手册/说明），代码库管【真实源码实现】——
    涉及话题名/节点名/参数名/接口/launch 配置/具体 .py/.cpp 逻辑时，文档往往
    不全或过时，必须直接检索源码拿真实实现作答（同样属"先查再答"必查项）。
    与 build_knowledge_instruction() 同读 runtime 实时值（同一来源），防悬空指令。
    """
    roots = runtime.code_search_roots()
    if not roots:
        return ""
    _paths = "\n".join(f"      - {r}" for r in roots)
    _tool = runtime.code_search_tool()
    if _tool:
        _py = sys.executable  # 当前解释器（装了 SDK 的 venv python），一定可执行
        return (
            "【参考资料 · 本地代码库检索（已配置 CODE_SEARCH_ROOTS，本机装有 search.py 检索工具）】\n"
            "  · 适用于【源码 / 接口 / 实现细节】类问题：话题名、节点名、参数名、服务/动作/消息类型、"
            "launch 文件、配置文件、具体 .py/.cpp 实现逻辑等。\n"
            "    这类问题 gbrain 文档往往未收录或不够精确，【必须直接检索本地源码库】拿真实实现作答——"
            "同样属先查再答必查项，禁止凭印象 / 大概 / 应该答复。\n"
            "  · 可检索的代码库根路径（仓库名在 search.py 的 --list-repos 里可查）：\n"
            f"{_paths}\n"
            "  · 【首选检索方式 · Bash 调 search.py】（rg 全文 + ctags 符号定位，比裸 Grep 全库扫更快更准）：\n"
            f"      全文搜索（默认字面量，可加 --regex；--pkg 限定功能包；--context N 带上下文）：\n"
            f"        \"{_py}\" \"{_tool}\" <关键词> --pkg <包名> --context 2\n"
            f"      查函数 / 类 / 宏定义位置（ctags 索引已预建，无需手动 --index）：\n"
            f"        \"{_py}\" \"{_tool}\" --symbol <符号名>\n"
            "    ⚠️ 命令里的 <关键词> / <包名> / <符号名> 是占位符，【必须替换成实际搜索词】再执行，不要原样输出尖括号；"
            "不确定包名时可不加 --pkg（全库搜）。\n"
            "    输出格式「<文件绝对路径>:<行号>:<内容>」，命中后【必须 Read 打开具体文件精读关键片段】"
            "确认接口签名 / 默认值 / 实现逻辑再作答；检索按问题收敛到具体包（--pkg），不要全库扫大目录。\n"
            "  · 【回退 · search.py 不可用时】Grep(pattern=\"<关键词>\", path=\"<代码库根路径>\") 搜关键词、"
            "Glob(pattern=\"**/*<关键词>*\", path=\"<代码库根路径>\") 找文件，再 Read 精读。\n"
            "  · 只陈述代码里真实存在的内容，绝不凭印象编造源码细节；查不到才如实说\"这个我得查下代码确认，稍回你\"；"
            "回复里不要暴露\"我查了代码\"（真人不会这么说）。\n"
        )
    return (
        "【参考资料 · 本地代码库检索（已配置 CODE_SEARCH_ROOTS）】\n"
        "  · 适用于【源码 / 接口 / 实现细节】类问题：话题名、节点名、参数名、服务/动作/消息类型、"
        "launch 文件、配置文件、具体 .py/.cpp 实现逻辑、某型号产品的驱动/固件代码等。\n"
        "    这类问题 gbrain 文档往往未收录或不够精确，【必须直接检索本地源码库】拿真实实现作答——"
        "同样属先查再答必查项，禁止凭印象 / 大概 / 应该答复。\n"
        "  · 可检索的代码库根路径（Windows 绝对路径，Read/Grep/Glob 可直接访问）：\n"
        f"{_paths}\n"
        "  · 检索方法（先定位、再精读）：\n"
        "      1) Grep(pattern=\"<关键词>\", path=\"<代码库根路径>\") 按关键词搜（包名 / 话题名 / 参数名 / 型号关键字）；\n"
        "      2) Glob(pattern=\"**/*<关键词>*\", path=\"<代码库根路径>\") 按文件名找候选；\n"
        "      3) Read 打开命中文件精读关键片段，确认接口签名 / 默认值 / 实现逻辑后再作答。\n"
        "  · 检索范围按问题收敛到具体包 / 模块目录，不要全库扫描大目录；只陈述代码里真实存在的内容。\n"
        "  · 查不到才如实说\"这个我得查下代码确认，稍回你\"；回复里不要暴露\"我查了代码\"（真人不会这么说）。\n"
    )

def detect_table_intent(content):
    """根据消息内容判断要查哪张表：'feedback'=问题反馈表，'project'=ROS项目表，None=不查。"""
    if not content:
        return None
    t = content
    # 问题反馈表意图词
    if any(k in t for k in ("问题反馈", "反馈进度", "问题进度", "待解决", "反馈", "需求汇总", "问题更新")):
        return "feedback"
    # ROS 项目表意图词
    if any(k in t for k in ("项目进度", "项目表", "ROS", "在跑", "研发项目", "项目做到", "进度怎么样", "做到哪")):
        return "project"
    return None


def _clean_md(s):
    """清洗注入数据里的图片/链接 markdown，避免坏语法（截断的 URL）干扰模型。"""
    s = re.sub(r"!\[[^\]]*\]\([^)]*\)", " [图片] ", s)  # 图片 -> [图片]
    s = re.sub(r"\[[^\]]*\]\([^)]*\)", "", s)            # 其余链接去掉
    return s


def _format_feedback(records):
    items = []
    for r in records:
        c = r.get("cells", {})
        st = c.get(FB_STATUS, {})
        st = st.get("name") if isinstance(st, dict) else st
        summ = c.get(FB_SUMM, {})
        summ = summ.get("markdown", "") if isinstance(summ, dict) else str(summ)
        summ = _clean_md(summ)
        summ = re.sub(r"\s+", " ", summ).strip()
        if len(summ) > 160:
            summ = summ[:160] + "…"
        items.append(f"  · [{st}] {summ}")
    return (
        "【问题反馈表·真实数据（来源：问题实时反馈与更新需求汇总）】\n"
        f"筛选条件：处理人包含{BOSS_NAME}(userId={BOSS_UID}) 且 解决状态≠已解决\n"
        f"当前{BOSS_NAME}名下共 {len(items)} 条待解决：\n" + "\n".join(items) +
        "\n（注：这是「问题反馈表」，与「ROS软件项目管理表/项目表」是两回事，回复时请明确区分，不要混淆。）"
    )


def _format_project(records):
    items = []
    for r in records:
        c = r.get("cells", {})
        name = c.get(ROS_NAME, "")
        prog = c.get(ROS_PROG)
        try:
            prog_pct = f"{int(float(prog)*100)}%"
        except (TypeError, ValueError):
            # ⚠️ 2026-08-13 修复：进度字段为 None/空/非数字时，原代码 str(prog) 会显示 "None"。
            # 回退为「进度未知」，避免把 None 当进度展示给 AI/同事。
            prog_pct = "进度未知"
        items.append(f"  · [{prog_pct}] {name}")
    return (
        "【ROS软件项目管理表·真实数据（来源：ROS软件项目管理表）】\n"
        f"筛选条件：负责人包含{BOSS_NAME}(userId={BOSS_UID}) 且 进度≠100%\n"
        f"当前{BOSS_NAME}名下共 {len(items)} 个在跑项目：\n" + "\n".join(items) +
        "\n（注：这是「ROS项目表」，与「问题实时反馈与更新需求汇总/问题反馈表」是两回事，请明确区分。）"
    )


def _records_from(data):
    """兼容 dws aitable 返回的两种包裹键（data / result），抽取 records 列表。

    ⚠️ 2026-08-13 审查修复：原代码只用 data.get("data")，而 dingtalk_api.py 其它接口
    都用 data.get("result")——若 aitable 实际返回 result 包裹，会静默取空（查表永远 0 条、
    却不报错）。现兼容两种键；两者都缺 records 时记告警，避免「查不到却不自知」。
    """
    if not isinstance(data, dict):
        return []
    _data = data.get("data") or data.get("result") or {}
    _recs = _data.get("records") or []
    if not _recs:
        log_debug(f"[table] aitable 返回无 records 键，keys={list(data.keys())[:8]}")
    return _recs


def fetch_table_context(intent, session_id=None):
    """按意图拉取对应多维表的「本人名下未解决项」，返回格式化文本（带缓存）。
    返回空串表示拉取失败、未配置多维表、或无需查表。"""
    if intent not in ("feedback", "project"):
        return ""
    # 未配置多维表（FB_*/ROS_* 为空）→ 自动退化为纯人设代复，不查表、不报错。
    if intent == "feedback" and not (FB_BASE and FB_TAB and BOSS_UID):
        return ""
    if intent == "project" and not (ROS_BASE and ROS_TAB and BOSS_UID):
        return ""
    now = time.time()
    cached = _TABLE_CACHE.get(intent)
    if cached and (now - cached[0]) < _TABLE_CACHE_TTL:
        log_debug(f"[table-cache] hit intent={intent}")
        return cached[1]
    try:
        if intent == "feedback":
            filt = json.dumps({"operator": "and",
                               "operands": [{"operator": "ne",
                                             "operands": [FB_STATUS, "已解决"]}]},
                              ensure_ascii=False)
            out = run_dws(["aitable", "record", "query", "--base-id", FB_BASE,
                           "--table-id", FB_TAB, "--filters", filt, "--all", "--format", "json"],
                          timeout=60)
            data = json.loads(out)
            recs = _records_from(data)
            boss = [r for r in recs if BOSS_UID in [
                x.get("userId") for x in (r.get("cells", {}).get(FB_HANDLER) or [])
                if isinstance(x, dict)]]
            text = _format_feedback(boss)
        else:
            out = run_dws(["aitable", "record", "query", "--base-id", ROS_BASE,
                           "--table-id", ROS_TAB, "--all", "--format", "json"], timeout=60)
            data = json.loads(out)
            recs = _records_from(data)
            boss = []
            for r in recs:
                c = r.get("cells", {})
                uids = [x.get("userId") for x in (c.get(ROS_OWNER) or []) if isinstance(x, dict)]
                try:
                    prog = float(c.get(ROS_PROG) or 0)
                except Exception:
                    prog = 0.0
                if BOSS_UID in uids and prog < 1.0:
                    boss.append(r)
            text = _format_project(boss)
        _TABLE_CACHE[intent] = (now, text)
        log_debug(f"[table] intent={intent} pulled, boss_items={len(boss)}")
        return text
    except Exception as e:
        log_debug(f"[table] fetch failed intent={intent}: {e}")
        return ""


async def _gen_reply_sdk_async(persona, prompt, image_paths=None,
                                session_id=None, resume=False):
    """用 CodeBuddy Agent SDK 异步生成回复（主后端）。
    编程式 system_prompt（无命令行编码/换行坑）、SDK 自管 stdio（无管道挂死）。
    返回原始回复文本（未走安全网净化）。
    坑：SERVER__PORT 端口冲突会导致 query() 0 字节超时 → 用空闲端口注入 env 规避。
    image_paths 非空时，把图以 Anthropic image 协议内联进用户消息（deepseek-v4-flash 多模态），
    实现「看图代复一次调用」——无需先 describe 再代复。
    session_id/resume：按会话隔离 + 续上下文（dt_<cid> 一人一会话，记忆连续）。
    cwd 固定钉钉工作空间 → 自动加载该空间记忆(.workbuddy/memory/MEMORY.md)；
    system_prompt 用 AppendSystemPrompt（追加模式），保留被自动加载的工作空间记忆，不被整体覆盖。"""
    sdk_env = build_sdk_env()
    # gbrain 知识库 MCP（HTTP）：让回复 agent 直接用 search/query 做语义检索，
    # 取代「工作空间内 产品资料/项目文件 文档」的旧 Grep/Glob/Read 注入方式。
    # 以 HTTP 客户端连接已运行的 gbrain（单一进程持 PGLite 锁），不 spawn 新进程、不抢锁。
    # GBRAIN_GROUNDING=0 或端点不可用时不挂（退回纯人设代复 + 多维表 grounding）。
    mcp_servers = {}
    # 与 build_knowledge_instruction() 同读 runtime 实时值 → prompt 指令与工具挂载永不一致
    if runtime.GBRAIN_GROUNDING and runtime.GBRAIN_MCP_URL:
        _gb_hdr = {"Authorization": f"Bearer {runtime.GBRAIN_MCP_TOKEN}"} if runtime.GBRAIN_MCP_TOKEN else {}
        mcp_servers["gbrain"] = {
            "type": "http",
            "url": runtime.GBRAIN_MCP_URL,
            "headers": _gb_hdr,
        }
    options = CodeBuddyAgentOptions(
        # 方案 B：agent 已注册时由 --agent 按名加载灵魂，不再注入人设（避免双灵魂）；
        # 仅 agent 未注册时把 sys_text（人设兜底+查表数据）以追加模式注入。
        system_prompt=(
            AppendSystemPrompt(append=persona) if (AppendSystemPrompt and persona) else None
        ),
        # 真源：透传 --agent 让 codebuddy 按名加载全局注册灵魂 dingtalk-helper.md（已实测 18.6s 成功）；
        # agent 未注册（如新机器）时不传，退回 sys_text 文件注入兜底。
        extra_args={"agent": SOUL_AGENT} if _AGENT_REGISTERED else {},
        # 工具权限统一管理（黑名单模式）：禁用 DISALLOWED_TOOLS 列出的工具（详见 runtime.py）。
        # 默认只禁 Write/Edit（防 agent 误写/篡改本地文件）；WebSearch/Read/Grep 等放开，
        # 但 system_prompt 仍软约束「事实优先查 gbrain、内部资料不丢公网」。gbrain/dws 均为 MCP 工具，不受此禁影响。
        # 如需调整，改 runtime.py 的 DISALLOWED_TOOLS 或用环境变量 DINGTALK_AGENT_DISALLOWED_TOOLS 覆盖。
        disallowed_tools=DISALLOWED_TOOLS,
        model=CODEBUDDY_MODEL,
        permission_mode="bypassPermissions",
        codebuddy_code_path=CODEBUDDY_CMD if CODEBUDDY_CMD and os.path.exists(CODEBUDDY_CMD) else None,
        cwd=DINGTALK_WORKSPACE if os.path.isdir(DINGTALK_WORKSPACE) else None,
        env=sdk_env,
        mcp_servers=mcp_servers,
        session_id=session_id if (session_id and not resume) else None,
        resume=session_id if (session_id and resume) else None,
    )
    async def _prompt_iter():
        if image_paths:
            content = [{"type": "text", "text": prompt}]
            for p in image_paths:
                try:
                    content.append(build_image_block(p))
                except Exception as e:
                    log_debug(f"[gen_reply] read image {p} error: {e}")
            yield {"type": "user", "message": {"role": "user", "content": content}}
        else:
            yield {"type": "user", "message": {"role": "user", "content": prompt}}
    chunks = []
    result_fallback = ""  # ⚠️ 2026-08-06 修复：ResultMessage.result 兜底（见下）
    # ⚠️ 2026-08-03 老板要求：agent 是流式输出，可观察完整思考/执行过程。
    # 解析时除 TextBlock（最终回复）外，把 ThinkingBlock（思考）/ ToolUseBlock（工具名+入参）/
    # ToolResultBlock（工具结果）也打进调试日志——排查「agent 到底调没调 dws / 查到了什么」时
    # 直接看日志轨迹，不用猜。默认关（DEBUG_AGENT_TRACE=1 开启），避免常驻下刷屏。
    _trace = os.environ.get("DEBUG_AGENT_TRACE") == "1"
    _trace_buf = []
    async for message in _sdk_query(prompt=_prompt_iter(), options=options):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, TextBlock):
                    chunks.append(block.text)
                elif _trace:
                    if isinstance(block, ThinkingBlock):
                        _trace_buf.append(f"[thinking] {block.thinking[:300]}")
                    elif isinstance(block, ToolUseBlock):
                        _trace_buf.append(f"[tool_use] {block.name} input={json.dumps(block.input, ensure_ascii=False)[:400]}")
                    elif isinstance(block, ToolResultBlock):
                        _trace_buf.append(f"[tool_result] {str(block.content or '')[:400]} is_error={block.is_error}")
        elif isinstance(message, ResultMessage):
            # ⚠️ 2026-08-06 修复（空返回根因）：模型偶发把「最终回复」放在 ResultMessage.result，
            # 而不走 AssistantMessage 的 TextBlock 流——原代码只收集 TextBlock，导致这种调用被
            # 误判为「SDK 空返回」（实际回复已在 result 里），重试同样中招，最终转人工不代发。
            # 现在把 result 收集为兜底，TextBlock 为空时用它（extract_reply 会抽 <reply>/正文）。
            _r = str(getattr(message, "result", "") or "").strip()
            if _r and not result_fallback:
                result_fallback = _r
            if _trace:
                _trace_buf.append(f"[result] {_r[:300]}")
    if _trace and _trace_buf:
        log_debug("[agent-trace]\n" + "\n".join(_trace_buf))
    raw = "".join(chunks).strip()
    if not raw and result_fallback:
        raw = result_fallback
    return raw


def _build_user_msg(main_line, history_lines, burst_mode):
    """构造 gen_reply 的「用户消息」正文（主回复对象 + 可选背景历史）。

    把原先 4 套 80% 重合的模板（burst/single × 有/无背景历史）收敛为一张查表，
    按 (burst_mode, 是否有背景历史) 取对应的「主回复对象描述句 / 背景历史块开头 / 结尾指令」
    三段差异化片段，再统一拼装——消除 4 套重复 inline 模板，且输出与原模板逐字节一致。
      - main_line:      "发送者：内容" 形式的主回复对象行
      - history_lines:  背景历史逐行列表（已标注"你(本人历史发言)"/同事）；空则无背景块
      - burst_mode:     True=主消息是延时期连发的多条，要求综合给一条统一回复
    """
    _main_head, _hist_head, _tail = _USER_MSG_FRAGMENTS[(burst_mode, bool(history_lines))]
    parts = [
        "【⚠️ 你的任务关键 ⚠️】\n",
        f"● 【主回复对象】（{_main_head}）\n",
        f"  {main_line}\n\n",
    ]
    if history_lines:
        parts.append(
            f"● 【背景历史】（更早的消息，{_hist_head}；仅供了解上下文和你的说话风格，【不是】回复对象）\n"
            + "\n".join(history_lines) + "\n\n"
            "● SDK 会话历史（如有）：仅用于了解你平时说话风格，【不是】当前要回的内容。\n\n"
        )
    else:
        parts.append("● SDK 会话历史（如有）：仅用于了解你平时说话风格。\n")
    parts.append(_tail)
    return "".join(parts)


# gen_reply 用户消息 4 种形态的差异化片段（键 = (burst_mode, 有背景历史)）。
# 主回复对象描述句 / 背景历史块开头 / 结尾指令——三段组合即原 4 套模板的全部差异，
# 提取到此表后 gen_reply 不再内联重复 f-string，且可保证 prompt 文本零漂移。
_USER_MSG_FRAGMENTS = {
    (True, True): (
        "对方在延时窗口内连发的多条消息，已按时间正序合并如下，是你【唯一】要回的内容——"
        "请综合理解后给【一条】统一回复，覆盖对方连发消息里的核心诉求，不要漏答",
        "含你本人历史发言 + 跨窗口的对方更早消息",
        "请针对【主回复对象】（即对方连发的全部消息）写一条回复：综合理解对方这一轮在表达什么，"
        "给一条涵盖核心诉求的统一回复；不要逐条复述对方的话、不要分点作答；"
        "不要复述或扩展背景历史里已说过的话题，不要再提已被处理过的\"问题反馈表 / 项目进度\"等。",
    ),
    (True, False): (
        "对方在延时窗口内连发的多条消息，已按时间正序合并如下，是你【唯一】要回的内容——"
        "请综合理解后给【一条】统一回复",
        None,
        "请综合理解对方这一轮连发的全部消息后写一条回复，覆盖对方核心诉求，不要逐条复述。",
    ),
    (False, True): (
        "对方最新发的消息，是你【唯一】要回的内容",
        "含你本人历史发言 + 对方历史消息",
        "请只针对【主回复对象】写一条回复：不要复述或扩展历史里已说过的话题，"
        "不要再提已被处理过的\"问题反馈表 / 项目进度\"等；本人历史发言仅供你模仿口吻。",
    ),
    (False, False): (
        "对方最新发的消息",
        None,
        "请以你自己的口吻写一条回复（若与历史话题无关，请完全忽略历史）。",
    ),
}


def _build_img_hint(n):
    """构造「带图消息」提示语：动态图片数量 + 顺序说明。

    ⚠️ 2026-08-11 修复（图片+文字结合混淆）：原提示语写死"一张图片"，实际多图时
    数量不符、且无任何顺序/归属引导——agent 无法知道"这个/那个"指代哪张图，
    只能猜（实锤案例：盘锦丽 2 图+问底盘选型，agent 笼统回"Hybrid 更强"）。
    现改为：动态张数 + 说明图片按发送先后排列（图1、图2…），并要求逐张看图、
    对照文字指代、图与文字对不上就如实说（不硬答）。
    """
    if n <= 1:
        return "\n（随消息附了 1 张图片，请结合图片内容以你自己的口吻回复）"
    _seq = "、".join(f"图{i}" for i in range(1, n + 1))
    return (
        f"\n（随消息附了 {n} 张图片，按发送先后依次为 {_seq}；"
        "请【逐张】看每张图的内容，再对照文字里\"这个/那个/如图\"等指代，"
        "判断指代的是哪张图、图与文字怎么对应，最后以你自己的口吻回复。"
        "若图片与文字对不上、或图里信息不足，如实说\"这个我得看下图确认下\"，不要硬答）"
    )


def gen_reply(sender, content, image_desc="", image_paths=None, return_rejected=False,
              session_id=None, resume=False, table_context="", messages=None):
    """生成本人身份回复（**CodeBuddy Agent SDK 后端，唯一方案，无 CLI 兜底**）。
    关键设计：**系统提示(人设+查表数据+指令) 与 用户消息(纯消息) 分离**——
    SDK 用 AppendSystemPrompt(追加模式) 承载人设与查表事实（保留 cwd 自动加载的工作空间记忆），
    用户消息只传干净单行，避免模型把"指令/数据"误当成"要回复的消息"而说"没收到内容"。
    安全网（extract_reply + _looks_like_reply）在此做：质量不达标返回空，调用方走「不代发」。
    session_id 非空时按会话隔离记忆；resume=True 表示续上同一会话（记忆连续）。

    ⚠️【主消息 vs 背景历史 · 关键设计】（2026-07-20 老板纠偏 + 修复）：
    messages 非空 = 窗口内多条消息合并：
      - msgs[0] = 对方最新发的消息 = 【主回复对象】（这是 AI 唯一要回的内容）
      - msgs[1:] = 同一对话窗口内的更早消息 = 【背景历史】（仅供 AI 了解背景）
    旧版本把所有历史"；".join 成 content 喂给 AI + 让 AI"综合理解"，导致 AI 复述最旧话题、
    配合 SDK session resume 加载的旧回复形成"话题死循环"（典型症状：AI 还在接茬 T1
    "问题反馈表，内容跟进一下"，而不是回最新一条"我以为让我测试呢"）。根治：
    (1) 主消息/历史显式分离；(2) prompt 强约束"只回主消息"；(3) 查表 grounding 用主消息判。

    SDK 不可用/失败 → 直接返回空（不代发），不再降级 CLI。
    """
    if not _SDK_AVAILABLE:
        log_debug("[gen_reply] SDK 不可用 -> 不代发")
        return ("", "") if return_rejected else ""
    persona = _resolve_persona()
    has_image = bool(image_paths)

    # —— 决定主回复对象 + 背景历史 ——
    # ⚠️ 2026-07-30 老板纠偏：延时期内（≤REPLY_DELAY_SEC）对方连发的多条消息，
    # 物理合并成【一条主消息】喂给 AI（不再走"只摘最新一条 + 其余当背景历史"的旧逻辑）。
    # 物理合并比 prompt 软约束强：AI 看到的主回复对象直接就是"对方在延时窗口内连发的全部消息"。
    # 跨窗口更早的对方消息 + 老板本人历史发言 仍作为背景历史（仅作上下文）。
    main_msg = None
    history_msgs = []
    main_content = content  # 单条分支用
    _burst_mode = False  # 是否走了"延时期合并"路径（日志区分用）
    if messages:
        # 防御再排一次（保证 newest-first）：主循环已按 ts desc 排过，但若外部
        # 直接调用 gen_reply 传入乱序 messages，AI 仍可能接错话。
        try:
            _ms = sorted(messages, key=lambda m: m.get("ts") or 0, reverse=True)
        except Exception:
            _ms = list(messages)
        # 对方消息（过滤 is_self=True），按 ts 倒序（newest-first）
        _peer_ms = [m for m in _ms if not m.get("is_self")]
        _self_ms = [m for m in _ms if m.get("is_self")]
        # 锚点：最新一条对方消息的 ts
        _T0 = (_peer_ms[0].get("ts") or 0) if _peer_ms else 0
        # 延时窗口 = [T0 - REPLY_DELAY_SEC, T0]
        _WIN = runtime.REPLY_DELAY_SEC
        _window_peer = [m for m in _peer_ms
                        if _T0 - (m.get("ts") or 0) <= _WIN]  # 含 T0 那条
        _window_peer.sort(key=lambda m: m.get("ts") or 0)  # 窗口内按时间正序呈现（旧→新）
        if len(_window_peer) >= 2:
            # 【延时期合并模式】把窗口内多条对方消息物理合并成一条虚拟主消息
            _burst_mode = True
            _latest = _window_peer[-1]  # 最新一条，拿 sender / ts / cid
            _lines = []
            for i, m in enumerate(_window_peer, 1):
                _lines.append(f"[{i}/{len(_window_peer)}] {m.get('sender','对方')}：{m.get('content','')}")
            _merged_content = "\n".join(_lines)
            main_msg = {
                "sender": _latest.get("sender", sender or "对方"),
                "content": _merged_content,
                "ts": _latest.get("ts"),
                # 注意：合成对象没有 image_paths/cid 等字段；图片走 has_image 分支另传
            }
            main_content = _merged_content
            # 背景历史 = 窗口外的对方消息 + 老板本人历史发言
            _window_ids = set(id(m) for m in _window_peer)
            history_msgs = [m for m in _ms if id(m) not in _window_ids]
            if history_msgs:
                history_msgs.sort(key=lambda m: m.get("ts") or 0)
        else:
            # 【单条主消息模式】沿用 2026-07-20 设计：主=最新对方一条，其余为背景历史
            main_msg = _peer_ms[0] if _peer_ms else (_ms[0] if _ms else None)
            history_msgs = [m for m in _ms if m is not main_msg] if main_msg else []
            if history_msgs:
                history_msgs.sort(key=lambda m: m.get("ts") or 0)
            if main_msg:
                main_content = main_msg.get("content", "") or content
        # 查表意图：用主消息判（合并模式下含全部窗口消息，单条模式下含最新一条）
        if not table_context and TABLE_GROUNDING and main_msg:
            _intent = detect_table_intent(main_content)
            if _intent:
                table_context = fetch_table_context(_intent, session_id) or ""
            _intent_dbg = _intent
        else:
            _intent_dbg = "(skip: no main_msg or table_context already set)"
        _n_self_hist = sum(1 for m in history_msgs if m.get("is_self"))
        _mode_tag = "burst-merged" if _burst_mode else "single-main"
        log_debug(
            f"[gen_reply] messages={len(_ms)} (peer={len(_peer_ms)} self_hist={_n_self_hist}) "
            f"mode={_mode_tag} window_peer={len(_window_peer) if _burst_mode else 1} "
            f"main_sender={main_msg.get('sender', '?') if main_msg else '?'} "
            f"main_content={(main_content[:80] if main_content else '')!r} "
            f"history_n={len(history_msgs)} intent={_intent_dbg} "
            f"table_context_len={len(table_context) if table_context else 0}"
        )
    else:
        # 单条 content 分支：兼容老调用（外部传 content 但无 messages）
        if not table_context and TABLE_GROUNDING and content:
            _intent = detect_table_intent(content)
            if _intent:
                table_context = fetch_table_context(_intent, session_id) or ""
            log_debug(f"[gen_reply] single-mode intent={_intent} table_context_len={len(table_context) if table_context else 0}")
        else:
            log_debug(f"[gen_reply] single-mode (no table) content={content[:60]!r}")

    # —— 系统提示 = (人设兜底[仅 agent 未注册时由 _resolve_persona 返回]) + (直接回复同事模式锁) + (查表数据，按主消息收紧) ——
    # 注：agent 已注册时 persona=None（灵魂由 --agent 按名加载），此处只补 _MODE_LOCK+查表；
    # _MODE_LOCK 强制「直接回复同事」模式（防双模式灵魂误进探索模式），无论 agent 是否注册都始终注入。
    parts = []
    if persona:
        parts.append(persona)
    parts.append(_MODE_LOCK)
    # ⚠️ few-shot 示例（教 agent 先查再答，禁止偷懒）：2026-08-04 内联为模块常量 _FEW_SHOT_EXAMPLES
    # （老板要求写进代码 prompt，与 _MODE_LOCK 同级，不再依赖 .md 文件读取）。
    # 实测 few-shot 放 append 是行为最强驱动力（搬灵魂会退化，见 SKILL.md 关键坑5）。
    parts.append(_FEW_SHOT_EXAMPLES)
    _private_fs = _load_private_few_shot()  # 私有化真实示例（可选，不随包分发；见函数注释）
    if _private_fs:
        parts.append(_private_fs)
    parts.append(build_knowledge_instruction())  # 知识库检索指令：与 gbrain 实际挂载状态一致
    _code_search = build_code_search_instruction()  # 本地代码库检索指令：仅配置 CODE_SEARCH_ROOTS 且路径存在时注入
    if _code_search:
        parts.append(_code_search)
    if table_context:
        # ⚠️ 收紧：再校验一次主消息是否在问「进度/反馈」类问题。
        # 旧版本无脑注入"对方问的正是上面这类进度/反馈问题"会强制 AI 聊历史，
        # 即使新消息是"测试/忙/吐槽/确认"等完全无关话题。核心 bug 根因之一。
        _main_for_intent = (main_msg.get("content", "") if main_msg else (content or ""))
        _recheck_intent = detect_table_intent(_main_for_intent)
        if _recheck_intent:
            parts.append(
                f"【多维表真实数据（已为你查好，必须基于它作答，不要编造、不要说"
                f"\"在的/收到了/好的\"之类废话）】\n{table_context}\n"
                f"对方（{sender}）最新一条消息确实在问「进度/反馈」相关问题，"
                f"请基于上方真实数据，以你自己的口吻直接告诉这位同事："
                f"当前你名下有几条待解决、分别是什么（一句话点每条）。"
            )
        else:
            # 主消息与查表意图无关 → 丢弃查表数据，避免污染当前回复。
            log_debug(f"[gen_reply] table_context dropped: main msg has no progress/feedback intent")
    sys_text = "\n\n".join(parts)

    # —— 用户消息 = 【主回复对象】+ 【背景历史】（仅作上下文） ——
    if main_msg is not None:
        _main_line = f"{main_msg.get('sender', sender or '对方')}：{main_msg.get('content', '')}"
        _hist_lines = []
        for m in history_msgs:
            if m.get("is_self"):
                _who = "你（本人历史发言）"
            else:
                _who = m.get("sender", "同事")
            _hist_lines.append(f"  · {_who}：{m.get('content', '')}")
        user_msg = _build_user_msg(_main_line, _hist_lines, _burst_mode)
        if has_image and not image_desc:
            user_msg += _build_img_hint(len(image_paths))
        elif image_desc:
            user_msg += f"\n（图片内容：{image_desc}）"
    else:
        # 单条 content（无 messages）：沿用旧逻辑，但 prompt 强化
        _single = f"{sender}：{content}".replace("\n", " ")
        user_msg = (
            "【⚠️ 你的任务关键 ⚠️】这是对方最新发来的【单条】消息，请直接以本人身份回复：\n"
            + _single
        )
        if has_image and not image_desc:
            user_msg += _build_img_hint(len(image_paths))
        elif image_desc:
            user_msg += f"（图片内容：{image_desc}）"
    global _agent_warmed
    _call_timeout = runtime.AGENT_FIRST_CALL_TIMEOUT if not _agent_warmed else runtime.AGENT_CALL_TIMEOUT
    try:
        raw = asyncio.run(asyncio.wait_for(
            _gen_reply_sdk_async(sys_text, user_msg, image_paths=image_paths,
                                 session_id=session_id, resume=resume),
            timeout=_call_timeout))
        # ⚠️ 2026-08-03 老板拍板：SDK 空返回自动重试 1 次。
        # 空返回 = SDK 调用"成功"但模型侧没产出任何 TextBlock（后端抖动 / 只输出工具调用没给最终文本 /
        # gbrain 链路瞬时中断），实测复现时 16s 快速返回空、rejected_len=0。属偶发，重试大概率成功。
        # 重试时在用户消息尾部追加一句提示，要求直接输出 <reply> 正文，避免再次只给分析/工具调用过程。
        if not raw:
            log_debug("[gen_reply] SDK 空返回 -> 自动重试 1 次")
            raw = asyncio.run(asyncio.wait_for(
                _gen_reply_sdk_async(
                    sys_text,
                    user_msg + "\n（注意：上一次生成未返回有效内容，请直接输出 <reply>...</reply> 包裹的回复正文；不要只输出分析过程或工具调用过程。）",
                    image_paths=image_paths, session_id=session_id, resume=resume),
                timeout=_call_timeout))
            if raw:
                log_debug(f"[gen_reply] 重试成功，len={len(raw)}")
            else:
                log_debug("[gen_reply] 重试仍空返回 -> 转人工")
    except Exception as e:
        if isinstance(e, asyncio.TimeoutError) and not _agent_warmed:
            # 首次调用超时：几乎都是 codebuddy 仍在冷启动注册 agent（7~26min），并非真故障。
            # 本次不代发（转人工），但保留 _agent_warmed=False，进程内后续调用仍用大超时，
            # 直到注册完成成功一次才切回常规超时——根治「首条消息被 240s 静默跳过」。
            log_debug(
                f"[gen_reply] 首次 SDK 调用在 {_call_timeout}s 内超时——大概率 codebuddy 仍在冷启动注册 agent，"
                f"本次不代发（转人工通知）；进程内后续调用已自动保持放宽超时，注册完成后即可正常代复"
            )
            return ("", "[SDK调用超时] codebuddy 可能仍在冷启动注册 agent") if return_rejected else ""
        # SDK 调用抛其他异常（如 400 invalid parameter value）：把异常详情+响应体打到日志，
        # 并把失败原因回传给老板，避免只笼统说「质量不达标」却不知根因。
        _resp = getattr(e, "response", None)
        _resp_txt = ""
        if _resp is not None:
            try:
                _resp_txt = _resp.text if hasattr(_resp, "text") else str(_resp)
            except Exception:
                _resp_txt = ""
        _err_txt = f"{type(e).__name__}: {e}"
        # ⚠️ 2026-08-07 修复：400 mime/参数类错误常见于「resume 续上下文时把历史媒体（图片/语音）带进请求」——
        # 即使本次消息是纯文字，只要该会话历史里含媒体，SDK resume 也会 400
        # （2026-07-24 已知坑 #4「媒体消息代复 400」的延伸形态，当时待排查方向=失败重试不带 session）。
        # 此时降级为不带 session 全新生成一次：放弃会话记忆换取正常代复，成功即用，仍失败才转人工。
        if (session_id or resume) and ("400" in _err_txt or "mime" in _err_txt.lower()
                                       or "invalid parameter" in _err_txt.lower()):
            log_debug(f"[gen_reply] SDK 400（疑似历史媒体+resume）-> 降级为不带 session 重试 1 次: {_err_txt[:150]}")
            try:
                raw = asyncio.run(asyncio.wait_for(
                    _gen_reply_sdk_async(sys_text, user_msg, image_paths=image_paths,
                                         session_id=None, resume=False),
                    timeout=_call_timeout))
            except Exception as e2:
                log_debug(f"[gen_reply] 降级重试也失败: {type(e2).__name__}: {e2}")
                raw = None
            if raw:
                log_debug(f"[gen_reply] 降级重试成功（无 session），len={len(raw)}")
                # 成功则跳过下方 return，走统一质检流程
            else:
                log_debug(f"[gen_reply] SDK 调用失败 -> 不代发: {_err_txt}")
                if _resp_txt:
                    log_debug(f"[gen_reply] SDK 响应体(前500): {_resp_txt[:500]}")
                return ("", f"[SDK调用失败] {_err_txt}") if return_rejected else ""
        else:
            log_debug(f"[gen_reply] SDK 调用失败 -> 不代发: {_err_txt}")
            if _resp_txt:
                log_debug(f"[gen_reply] SDK 响应体(前500): {_resp_txt[:500]}")
            return ("", f"[SDK调用失败] {_err_txt}") if return_rejected else ""
    _agent_warmed = True  # 成功完成一次 SDK 生成，后续调用用常规超时
    if not raw:
        return ("", "") if return_rejected else ""
    out = extract_reply(raw)
    if not _looks_like_reply(out):
        log_debug(f"gen_reply sanity fail (len={len(out)}) -> 不代发")
        log_debug(f"[gen_reply] 质检未过草稿预览(前600): {(out or raw)[:600]}")
        # 失败也把「模型实际产出的内容」作为草稿回传：先取抽出的草稿 out，
        # 抽不出（模型只给分析/思考没给 <reply>）则回退原始 raw。
        # 保证单聊「生成过就推微信」——老板要看失败时的内容，哪怕没过质检。
        return ("", (out or raw)) if return_rejected else ""
    return (out, "") if return_rejected else out


# ---------- 质检（extract_reply / _looks_like_reply）共享常量 ----------
# 均为只读正则/集合，模块级定义避免每次调用重建（_looks_like_reply 每回复调用多次）。
# 「称呼：内容」开头的豁免白名单：正常口吻词，不以「转述别人」拦截
_COLON_EXEMPT = {"注意", "说明", "补充", "提醒", "备注", "例如", "比如",
                 "其实", "不过", "另外", "首先", "其次", "最后", "综上", "所以",
                 "如果", "假如", "建议", "正经", "简单", "话说", "对了", "顺便"}
_COLON_LEAD_RE = re.compile(r"^([一-龥]{2,4}|[A-Za-z0-9]{2,6})[:：]\s*(.*)$")
# 助理/转述视角泄漏信号（2026-07-27 放宽反问、2026-08-03 删「示例」见下方注释）
_ASSISTANT_LEAK_RE = re.compile(
    r"(作为您的|我帮您|为您查询|需要我为您|我作为|"
    r"要我帮你拟|要我(去|帮)拟|消息：|发件人：|同事发|对方：)")
# 凭印象答事实性问题的含糊词 + 技术参数信号（2026-07-29 加，防跳过 gbrain 硬答）
# ⚠️ 编译时带 re.I（等价原内联 re.search(..., re.I)），调用处不再传 flags
_VAGUE_WORDS_RE = re.compile(r"(印象里|印象中|我记得|大概|大概是|应该是|好像是|似乎|差不多)")
_TECH_PARAM_RE = re.compile(
    r"(波特率|电压|电流|频率|功率|分辨率|精度|量程|接口|型号|参数|默认值|"
    r"\d+\s*(bps|kbps|Mbps|V|mV|A|mA|Hz|kHz|MHz|GHz|W|kW|mm|cm|m|°|%|rpm|r/min))",
    re.I)
# extract_reply 兜底抽行时的「解释性前缀」词
_META_PREFIX = ("我", "按", "建议", "在您", "在你", "是否", "要我", "如果", "注意",
                "这条", "对方", "示例", "输出：", "现在", "请", "推荐", "综上", "所以")
# ⚠️ 2026-08-11 修复（空洞收尾 bug，比提示语更隐蔽的全局生成缺陷）：
# 模型偶发不输出 <reply> 标签，输出「完整正文多行 + 结尾一句助理式收尾」——
# 典型如「先这样定方向，有问题随时找我。」「需要我直接通过钉钉发出去吗？」
# extract_reply 兜底旧规则取【最后一行】恰好抓到收尾句 → 空洞废话被代发
# （实锤：盘锦丽 2 图案例返回"先这样定方向，有问题随时找我。"，正文被丢弃）。
# 两套正则：
#  · _TAIL_SKIP_RE（宽松，extract_reply 挑正文行用）：命中即跳过该行、向前回溯找正文行；
#  · _EMPTY_REPLY_RE（严格锚定，_looks_like_reply 兜底用）：只拦「整条回复就是一句空洞收尾」
#    （含信息的正常回复如"具体我下午发你。有问题随时找我。"必须放行，勿误伤）。
_TAIL_SKIP_RE = re.compile(
    r".*(有问题|有需要|有什么问题)(随时)?(找|联系|喊)我.*|"
    r"^(先这样定方向.*|就(先)?这样.*)|"
    r"(需要我|要我|我帮你).*发(出|给|到|在)?.*[吗吧]?[？?]?$|"
    r"需要我直接.*[吗吧]?[？?]?$"
)
_EMPTY_REPLY_RE = re.compile(
    r"^(先这样定方向.*|就(先)?这样[。.，,]?.*|"
    r"(需要我|要我|我帮你).*发(出|给|到|在)?.*[吗吧]?[？?]?$|"
    r"需要我直接.*[吗吧]?[？?]?$|"
    r"^(有什么)?(问题|需要)(随时)?(找|联系|喊)我[。.]?$|"
    r"^随时(找|联系|喊)我[。.]?$)"
)


# ⚠️ 2026-08-19 标签残留清洗（回复乱码根因）：模型把 agent 工具调用的内部标签
# （</parameter> / </tool_calls> 等）混进回复输出（实锤：何杰/温兆龙多条回复带 </parameter>/</tool_calls>），
# 还偶发输出 <reply> 变体（08-14）。_TAG_TAIL_RE 剥【结尾】的任意 XML 标签残留
# （含可选尾随标点/空白，兼容 `。</parameter>` 这种正文后直接跟标签的形态）；
# _REPLY_TAG_RE 剥开头/中间的 <reply> 变体标签（08-14 已有，保留）。
# _TAG_TAIL_RE 剥【结尾】的任意 XML 标签残留（含可选尾随标点/空白），`(?:...)+` 一次剥
# 多个连续结尾标签（如 `正文。</parameter></tool_calls>` 全部剥干净，而非残留一个靠质检兜底）。
_TAG_TAIL_RE = re.compile(r"(?:<\s*/?\s*[A-Za-z_][^<>]*>\s*[。，,\.]?\s*)+$")
_REPLY_TAG_RE = re.compile(r"<\s*/?\s*reply\s*>", re.I)


def _strip_reply_tags(s):
    """剥掉文本里残留的标签（回复乱码清洗）：
    ① 结尾的任意 XML 标签残留（</parameter>/</tool_calls> 等工具调用内部标签）；
    ② <reply>/</reply> 变体标签（08-14 修复，保留）。
    全角 ＜＞ 由调用方先转半角。"""
    s = s or ""
    s = _TAG_TAIL_RE.sub("", s).strip()
    s = _REPLY_TAG_RE.sub("", s).strip()
    return s


def extract_reply(text):
    """从 codebuddy 输出里稳当地取出「要发出的回复正文」。
    deepseek-v4-flash 偶发会进入"助手草稿模式"（给多个选项、反问是否要发），
    用 <reply> 标签 + 兜底规则把真正的回复抽出来，避免把分析文本发到钉钉。
    ⚠️ 2026-08-14 修复（回复出现代码）：旧正则只认标准 <reply>xxx</reply>，
    标签变体（带空格/大写/全角/嵌套/无闭合）一律漏剥 → 带标签原文被代发。
    现全角转半角 + 放宽正则 + 抽取后统一剥残留标签。"""
    t = (text or "").strip()
    if not t:
        return ""
    # 全角尖括号转半角（模型偶发输出 ＜reply＞ 全角标签）
    t = t.replace("＜", "<").replace("＞", ">")
    # ⚠️ 2026-08-20 根治（三轮才找到的真根因）：deepseek 偶发把内部工具调用协议标记
    # ｜｜DSML｜｜（全角竖线 U+FF5C）泄漏进回复输出。codepoint 级实锤形态：
    #   `<reply>正文</｜｜DSML｜｜reply>`、`正文。</｜｜DSML｜｜parameter>`、`</｜｜DSML｜｜tool_calls>`
    # 前两轮修复（08-14 reply变体 / 08-19 结尾标签剥除）全部无效——所有正则要求 `<` 后
    # 紧跟 `/` 或字母，被 `｜｜DSML｜｜` 中缀骗过（且当时测试用例是手打的 `</parameter>`，
    # 从未测过真实字符）。根治：入口直接删除该标记（正文不可能合法含它），
    # 使 `</｜｜DSML｜｜parameter>` 规范化为 `</parameter>`，后续既有剥除/拦截全部生效。
    t = re.sub(r"[｜|]{2}\s*DSML\s*[｜|]{2}", "", t)
    # 1) 优先取 <reply>...</reply> 标签内（放宽：re.I + 标签内允许空白，兼容 < reply >/<REPLY>）
    m = re.search(r"<\s*reply\s*>\s*(.*?)\s*<\s*/\s*reply\s*>", t, re.S | re.I)
    if m:
        r = m.group(1).strip()
        if r:
            return _strip_reply_tags(r)   # 剥嵌套残留的 <reply> 前缀
    # 2) 去 markdown 代码围栏
    if t.startswith("```"):
        t = t.strip("`")
        if "\n" in t:
            t = t.split("\n", 1)[1]
    # 3) 取最后一个 > 引用块作兜底（模型常把"建议的草稿"放在 > 后）；
    # 注：此处不与原话比对排除（发件人消息未传入），仅取末个引用块
    quotes = re.findall(r"^\s*>\s?(.*)$", t, re.M)
    if quotes:
        return _strip_reply_tags(quotes[-1].strip())
    # 4) 兜底：去掉明显的解释性前缀行，取最后一句像回复的短行
    # ⚠️ 2026-08-11 修复（空洞收尾 bug）：模型无 <reply> 标签时输出常为
    # 「正文多行 + 结尾一句助理式收尾」（"先这样定方向，有问题随时找我。"）。
    # 旧规则取【最后一行】抓到收尾句 → 空洞废话被代发。新规则：从后往前找
    # 第一个【不是空洞收尾/问句/装饰行】的短行（正文行）；全是收尾才退回旧行为。
    lines = [l.strip() for l in t.splitlines() if l.strip()]
    cand = [l for l in lines
            if not l.startswith(_META_PREFIX) and len(l) <= 80
            and l.strip(" -=*#.·•—")]  # 纯装饰行（---/===）剔除
    if cand:
        _no_tail = [l for l in reversed(cand)
                    if not _TAIL_SKIP_RE.match(l) and not l.endswith(("？", "?"))]
        if _no_tail:
            return _strip_reply_tags(_no_tail[0])
        return _strip_reply_tags(cand[-1])
    return _strip_reply_tags(t.strip())


def _looks_like_reply(text):
    """正向判据：这是一条正常的「老板回复」吗？
    deepseek-v4-flash 偶发会进入"助手草稿/角色扮演"模式输出废话（如 '小张：老板，明天的评审…'、
    '老板，今天下午的会议能改到明天吗'），绝不能发到钉钉；正常反问同事
    （如"要不要我帮你查下?"）现已放行。返回 False 让调用方走安全兜底话术。"""
    if not text:
        return False
    # ⚠️ 2026-08-14/08-19 标签残留拦截：extract_reply 未剥干净的标签绝不代发——
    # ① <reply> 变体（08-14）；② agent 工具调用内部标签 </parameter>/</tool_calls>/<mcp__>
    #   （08-19 回复乱码根因，实锤：何杰/温兆龙多条回复）；③ 剥掉全部 XML 标签后为空
    #   （整条就是标签残留）。
    # 这是「回复出现代码/乱码」的最后一道闸，即使 extract_reply 漏剥也拦得住
    # （转人工，草稿推微信老板可见，绝不带标签/乱码发出去）。
    if re.search(r"<\s*/?\s*reply\s*>", text, re.I) or "＜reply" in text or "＜/reply" in text:
        return False
    # ⚠️ 2026-08-20 DSML 协议标记兜底拦截：deepseek 内部标记 ｜｜DSML｜｜（全/半角竖线）
    # 泄漏进回复 = 生成缺陷，绝不代发（extract_reply 入口已删，此处兜底未规范化的漏网）。
    if re.search(r"[｜|]{2}\s*DSML\s*[｜|]{2}", text):
        return False
    if re.search(r"<\s*/?\s*(?:parameter|tool_calls|tool_use|mcp__)\b", text, re.I):
        return False
    if not re.sub(r"<\s*/?\s*[A-Za-z_][^<>]*>", "", text, flags=re.I).strip():
        return False
    # ⚠️ 2026-08-11 修复（空洞收尾兜底）：整条回复就是一句「助理式收尾/空洞表态」
    # （"先这样定方向，有问题随时找我。" / "需要我直接通过钉钉发出去吗？"）
    # = 没回答问题 = 生成缺陷，绝不能代发 → 转人工（草稿推微信老板可见）。
    # 严格锚定版：含实质信息的正常回复（"具体我下午发你。有问题随时找我。"）不误伤。
    if _EMPTY_REPLY_RE.match(text.strip()):
        return False
    # 放宽长度/换行硬拒：老板回技术问题时本就是多句、较长文本，
    # 旧规则「>150字或含换行即判废」会把正常回复误杀成 skip_reply（见早期 04:13/04:23 案例）。
    # 改为仅对真正失控的超长跑题（>800字，模型明显跑题）判废；
    # 角色扮演/反问/自称老板等精准拦截见下方，不因长度放宽。
    if len(text) > 800:
        return False
    # ⚠️ 2026-08-22 修复（误伤实锤）：旧规则「回复含'老板'即拒」把同事间正常提及
    #   老板（"跟老板定""给老板汇报""老板说的那个"）全部误杀——08-21 蔡达轩/朱文杰
    #   两条正常草稿因此被拦转人工（老板反馈「生成没问题为什么没回复」）。
    #   「老板」作为指代（找/给/跟/向/听老板说）是正常业务表达，只有作为【称呼】
    #   开头（"老板，今天下午的会议…"）才是模型对老板说话的角色扮演 → 才拒。
    if re.match(r"^\s*老板[，,：:！!？?]", text):
        return False
    # 角色扮演/转述标记：开头是「称呼：内容」式（如"小张：""某总："）——模型在转述对方，
    # 不是本人回复。但"注意：""说明：""不过："等是正常口吻，需豁免。
    # 仅匹配 2-4 字纯中文 / 2-6 字英文数字 的称呼+冒号，且不在豁免白名单内。
    m = _COLON_LEAD_RE.match(text.strip())
    if m and m.group(1).lower() not in _COLON_EXEMPT:
        return False
    # 澄清/反问类标记：仅拦「模型泄漏系统/转述视角」的明确信号
    # （如把发件人/同事消息当任务复述、暴露"消息：/发件人："等内部字段、或以助理口吻对本人说话）。
    # ⚠️ 2026-07-27 老板再次放宽：此前 07-21 收紧后的"典型助理反问模式"
    # （想让我|要不要我|你希望我|你打算|我建议你|要我帮你|要我帮您…）现已允许代复——
    # 老板回同事本就会反问/主动提出帮忙，这类反问不再拦截，只拦真正的泄漏/角色错乱。
    # ⚠️ 2026-08-03 修复：原正则含「示例」→ agent 查 dws 记录后回复「…示例展示的修改…」
    # （正常业务词，宣传页/文档语境）被误判"示范输出"拦下（实测复现）。「示例」太宽泛，
    # 删掉；模型若真输出"示例回复：…"仍会被 extract_reply 的 meta_prefix / <reply> 标签兜底。
    if re.search(_ASSISTANT_LEAK_RE, text):
        return False
    # ⚠️ 凭印象答事实性问题拦截（2026-07-29 加）：当 agent 跳过 gbrain 直接凭记忆答规格/参数时，
    # 常出现"印象里 / 我记得 / 大概 / 应该是 / 出厂默认 / 印象中"等含糊词。
    # 这种回复违反【严禁编造】+【必须先查 gbrain】，转人工让老板看到草稿更安全。
    # 触发条件：含糊词 + 出现技术参数信号（数字+单位/型号/波特率/电压/电流/频率等）。
    _VAGUE = re.search(_VAGUE_WORDS_RE, text)
    if _VAGUE and re.search(_TECH_PARAM_RE, text):
        return False
    # 反问句：老板回同事时反问/确认细节是正常风格，一律放行
    # （>800字跑题已由上方长度闸拦截，无需在此重复限制）。
    return True


def push_weixin(text, retries=2, retry_wait=3):
    if runtime.DRY_RUN:
        log_debug(f"[DRY_RUN weixin] {text[:120]}")
        return True
    if not SEND_JS or not os.path.exists(SEND_JS) or not NODE or not os.path.exists(NODE):
        # 未安装 weixinclaw-proactive-push skill → 降级为仅日志，不阻断主流程
        log_debug(f"[weixin skipped] {text[:120]}")
        return False
    # ⚠️ 关键：send.js 推送失败时以 exit(1) + 打印 FAILED 退出（非抛异常），
    # 旧版无脑 return True 会静默吞掉失败 → 老板收不到微信却毫无痕迹。
    # 现严格检查返回码 + 输出，失败必留痕（日志 + 审计），便于第一时间定位
    # （典型失败 ret:-2 = 微信 bot 会话失效，需先在微信给 ClawBot 发一条消息激活）。
    # 加固（2026-07-20）：瞬时抖动（网络/限流）自动重试；需人工激活类故障
    # （ret=-2 / prepare failed / 会话已失效）立即失败，不空转重试——
    # 交给上层 GNOTIFY 慢重试或老板激活 ClawBot 后补发。
    NEED_ACTIVATE_HINTS = ("ret=-2", "prepare failed", "会话已失效", "bot id")
    for attempt in range(retries):
        try:
            r = subprocess.run([NODE, SEND_JS, text], timeout=30,
                               capture_output=True, creationflags=CREATE_NO_WINDOW)
        except Exception as e:
            log_debug(f"weixin push error attempt={attempt+1}/{retries}: {e}")
            if attempt < retries - 1:
                time.sleep(retry_wait)
                continue
            return False
        out = (r.stdout or b"").decode("utf-8", "replace")
        err = (r.stderr or b"").decode("utf-8", "replace")
        if r.returncode == 0 and "FAILED" not in out and "FAILED" not in err:
            log_debug(f"[weixin ok] {text[:80]}")
            return True
        snippet = (err or out).strip().replace("\n", " ")[:300]
        log_debug(f"[weixin FAIL rc={r.returncode} attempt={attempt+1}/{retries}] {snippet} | text={text[:80]}")
        if any(h in snippet for h in NEED_ACTIVATE_HINTS):
            # 需人工激活，重试无意义，立即失败返回，交由上层处理
            log_audit("weixin_push_fail", text=text[:200], rc=r.returncode, err=snippet[:200])
            return False
        if attempt < retries - 1:
            time.sleep(retry_wait)
            continue
        log_audit("weixin_push_fail", text=text[:200], rc=r.returncode, err=snippet[:200])
        return False
    return False


def _seed_notify(cid, title, is_single):
    """启动静默 seed 时，对近期(24h)到达的单聊未读发一次被动提醒（不代复）。
    群聊 seed 不提醒（避免开机刷屏；群默认仅 @我才推，downtime 期间非 @我群消息不紧急）。"""
    if not is_single:
        return
    try:
        push_weixin(
            f"📥 启动时发现单聊未读（仅提醒，未代复）：{title}\n"
            f"新消息到达后会正常代复；若老板已读可忽略。"
        )
    except Exception:
        pass
