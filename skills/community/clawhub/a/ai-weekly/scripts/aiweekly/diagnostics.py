"""运行告警的「人话翻译」——可靠性·异常提示友好化（SkillHub 评测 R·异常处理）。

背景（SkillHub 评测原文）：
    「大多数错误会有提示告知原因……不过有些情况下提示比较专业，
      普通用户可能不太容易理解具体该怎么解决」

对策：**分两层输出**
  1. 底层 logger / print 保持专业技术细节——排障时必须有；
  2. 生成结束后追加一段「💡 给你的提示」，把告警翻译成「为什么 + 下一步怎么办」。

设计要点：
  * 纯展示层，不参与生成逻辑，失败也不影响报告产出（best-effort）；
  * 规则表驱动（USER_HINT_RULES），加新提示只需加一行，不改流程代码；
  * 同类告警只提示一次（按规则关键词去重），避免刷屏。

从 generate_site.py 拆出：主入口有 500 行硬守护（validate_report.py 的
source_module_size），提示规则表体积大，必须独立成模块。
"""
from __future__ import annotations

import re

# 每条规则：(匹配关键词正则, 一句话原因, 下一步建议)。按顺序匹配，命中即停。
USER_HINT_RULES: list[tuple[str, str, str]] = [
    ("榜源抓取超时",
     "某个模型排行榜网站响应太慢，本次跳过了它",
     "不影响其它榜。想让它下次必出：单独重跑一次；"
     "国内环境可直接依赖「HF 镜像 / ModelScope」两个国内可连榜"),
    ("ModelScope 抓取失败",
     "魔搭（ModelScope）模型榜没取到",
     "国内网络通常可直接访问；若持续失败，多半是该站接口临时变更，等下次刷新即可"),
    ("抓取失败",
     "某个数据排行榜没取到数据",
     "报告已用其它源或历史快照兜底，不会空白。想看实时榜可稍后重跑"),
    ("排行榜抓取异常|暂无实时数据",
     "本次没拿到实时模型排行榜",
     "报告会显示「暂无实时数据」而**不会编造**名次。稍后重跑即可；"
     "若持续如此，说明该源在当前网络下不可达，属预期内的降级"),
    ("翻译|Ollama",
     "英文报道的中文翻译没全部完成",
     "不影响报告生成，未翻译的会保留英文原文。需完整翻译请先启动本地 Ollama"),
    ("读取.*失败|解析失败",
     "某个本地文件读取或解析出错",
     "检查该文件路径与 JSON 格式是否正确；脚本已跳过它继续生成"),
    ("requests|feedparser|beautifulsoup4|依赖",
     "缺少运行所需的 Python 依赖包",
     "执行 pip install -r requirements.txt 后重跑；"
     "或用统一启动器 run_report.sh（会自动用受管 venv）"),
    ("超时|timeout|timed out",
     "网络请求超时",
     "多为临时网络抖动，重跑一次通常就好。若本机网络架构要求全部出站流量"
     "经统一代理（如企业内网），可通过标准环境变量 HTTPS_PROXY 提供"),
    ("连接|Connection|DNS|Name or service",
     "网络连不上目标网站",
     "确认本机网络连通性。LMArena / Artificial Analysis 没有国内镜像源，"
     "不可达时报告会自动降级到国内榜与历史快照，属预期行为"),
]


def build_user_hints(messages: list[str]) -> list[tuple[str, str]]:
    """把告警原文列表翻译成 [(原因, 建议), ...]；同类只保留一条。

    纯函数、无副作用，便于单测。
    """
    seen: set[str] = set()
    hits: list[tuple[str, str]] = []
    for msg in messages or []:
        for kw, why, todo in USER_HINT_RULES:
            if kw in seen:
                continue
            try:
                matched = re.search(kw, msg)
            except re.error:  # 规则表写错时不要让生成流程崩掉
                matched = None
            if matched:
                seen.add(kw)
                hits.append((why, todo))
                break
    return hits


def print_user_hints(messages: list[str]) -> None:
    """打印「💡 给你的提示」段落（无告警时静默）。"""
    try:
        hits = build_user_hints(messages)
    except Exception:  # noqa: BLE001  展示层失败绝不能影响报告产出
        return
    if not hits:
        return
    print("\n💡 **给你的提示**（上面那些警告是什么意思、要不要紧）：")
    for i, (why, todo) in enumerate(hits, 1):
        print(f"  {i}. {why}")
        print(f"     → 怎么办：{todo}")
    print("     以上都不影响报告已生成的部分——数据取不到时技能会留空或标注，不会编造。")


__all__ = ["USER_HINT_RULES", "build_user_hints", "print_user_hints"]
