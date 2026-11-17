"""排行榜抓取与榜源健康监控（L2#14/#15，拆分自 leaderboard.py）。

本模块只负责「怎么抓取、怎么记录健康」，不含编排逻辑：
- ``SOURCES`` / ``LB_CRITERIA``：多源池定义（每源带 region 标签，供 region 优先级排序）；
- ``_collect_source_results``：并行抓取全部榜源（ThreadPoolExecutor, max_workers=4）；
- ``_record_health``：把本次各榜源健康快照 append 到 leaderboard_health.jsonl。

区域优先级 / 快照兜底 / 周变化 / 选型结论等编排逻辑仍在 leaderboard.py。

依赖（均为叶子模块，无循环依赖）：aiweekly.utils（重试/代理）、aiweekly.leaderboard_sources（各源解析器）。
"""
import json
import logging
import time
import concurrent.futures
from datetime import datetime
from pathlib import Path

from aiweekly.utils import _retry_fetch
from aiweekly.leaderboard_sources import (
    LM_ARENA_URL, AA_URL, HF_LEADERBOARD_URL, DATALARNER_URL,
    LLMSTATS_URL, OC_LLM_URL, SV_GENERAL_URL, MS_MODELS_URL, HF_MIRROR_API,
    fetch_lmarena_ranking, fetch_aa_ranking, fetch_hf_open_ranking,
    fetch_llmstats_ranking, fetch_datalearner_ranking,
    fetch_opencompass_ranking, fetch_superclue_ranking, fetch_modelscope_ranking,
    fetch_hf_mirror_popular, NO_CN_MIRROR_SOURCES,
)

logger = logging.getLogger(__name__)

SKILL_DIR = Path(__file__).resolve().parents[2]
# 榜源健康监控（L2#15）：每次生成 append 一行 {ts,source,status,latency_ms,rows_count}
HEALTH_PATH = SKILL_DIR / "leaderboard_health.jsonl"

# S2(2026-09)：多源并行抓取的整体墙钟硬上限（秒）。个别慢源超过此值即标记 timeout 跳过，
# 确保「一个慢源拖垮整份周报生成」不会发生。单源自身 _http_get timeout 通常 40–120s，
# 重试上限约 3×75s=225s；此处取 180s 作为整体截止（单源隔离已兜底，整体再留余量）。
# 注：曾计划把上限提到 240s（R3）以给 LMArena/HF 慢源更大重试墙钟，暂未启用；
# 若实测慢源重试确实触顶，改此处常量值即可，下方 timeout 文案与日志均引用本常量，无需同步改动。
OVERALL_FETCH_CAP_S = 180

# 三榜各自的评分标准说明（渲染到页面「评分标准」行，数据驱动）；定义在多源池之前，
# 供 SOURCES 引用（模块级求值顺序要求）。
LB_CRITERIA = {
    "lmarena": ("评分标准：人类偏好 Elo（LMArena）。由真实用户对模型回答做匿名两两盲测、"
                "按「哪个回答更好」投票得出——衡量的是真实使用中的人类好感度（使用体感），"
                "并非某项知识 / 能力基准。分数越高代表越受人类偏好。"),
    "aa": ("评分标准：智能指数 Intelligence Index（Artificial Analysis）。综合多项权威能力基准"
           "归一化后的综合分（满分 100，越高越强），主要涵盖：MMLU-Pro（研究生级综合知识）、"
           "GPQA（研究生级科学问答）、Humanity's Last Exam / HLE（人类终极考试·极难跨学科学术题，逼近专家上限）。"),
    "ls": ("评分标准：LLM-Stats 综合分（LLM Stats Score）。基于多项公开基准归一化后的开源模型"
           "综合得分（满分 100，越高越强），主要涵盖：MMLU-Pro（研究生级综合知识）、GPQA（研究生级科学问答）、"
           "HumanEval（代码生成）、MATH（数学竞赛解题）、SWE-bench（软件工程实战·修复真实 GitHub issue）、"
           "HLE（人类终极考试）；同时标注许可证、上下文窗口与输入输出单价，便于自部署 / 商用评估。"),
    "dl": ("评分标准：DataLearner LLM Leaderboard 综合分（基于 HLE 等公开基准归一化）。"
           "DataLearner 开源榜以 HLE（人类终极考试·极难跨学科学术题，逼近专家上限）为主分，"
           "并标注「开源情况」（如 免费商用）与机构，便于自部署 / 商用评估；"
           "上下文窗口与单价由模型资料卡（model_profiles.json）兜底注入，未匹配家族一律留空（绝不编造）。"),
    "hf": ("评分标准：Hugging Face Open LLM Leaderboard 平均分（Average ⬆️）。在多项权威基准上的"
           "加权平均分（满分 100，越高越强），主要涵盖：MMLU-Pro（研究生级综合知识）、MATH（数学竞赛解题）、"
           "HumanEval（代码生成）、GPQA（研究生级科学问答）、MuSR（多步逻辑推理·长篇谜题 / 谋杀推理等需多步推演）、"
           "IFEval（指令遵循·严格按格式与约束执行）。仅收录可复现的开源权重模型，强调可复现性与社区验证。"),
}

# ---------- 多源池（每个榜源带 region 标签，供 region 优先级排序）----------
SOURCES = {
    "aa": {"region": "global", "board": "comprehensive", "key": "aa",
           "fn": lambda n: fetch_aa_ranking(n),
           "label": "Artificial Analysis · 智能指数", "url": AA_URL,
           "criteria": LB_CRITERIA["aa"]},
    "lm": {"region": "global", "board": "comprehensive", "key": "lm",
           "fn": lambda n: fetch_lmarena_ranking(n),
           "label": "LMArena · 人类偏好 Elo", "url": LM_ARENA_URL,
           "criteria": LB_CRITERIA["lmarena"]},
    "oc": {"region": "cn", "board": "comprehensive", "key": "oc",
           "fn": lambda n: fetch_opencompass_ranking(n),
           "label": "OpenCompass 司南 · LLM 综合榜", "url": OC_LLM_URL,
           "criteria": ("评分标准：OpenCompass 司南 LLM 综合榜。在知识/推理/数学/代码/智能体等多维度"
                        "权威基准上的加权平均均分（满分 100，越高越强）。")},
    "sv": {"region": "cn", "board": "comprehensive", "key": "sv",
           "fn": lambda n: fetch_superclue_ranking(n),
           "label": "SuperCLUE · 中文通用智能指数", "url": SV_GENERAL_URL,
           "criteria": ("评分标准：SuperCLUE 中文通用能力总排行榜。聚焦中文场景的综合能力复合分"
                        "（满分 100，越高越强）。")},
    "ls": {"region": "global", "board": "open_source", "key": "ls",
           "fn": lambda n: fetch_llmstats_ranking(n),
           "label": "LLM-Stats · 开源模型榜", "url": LLMSTATS_URL,
           "criteria": LB_CRITERIA["ls"]},
    "dl": {"region": "global", "board": "open_source", "key": "dl",
           "fn": lambda n: fetch_datalearner_ranking(n),
           "label": "DataLearner · 开源模型榜", "url": DATALARNER_URL,
           "criteria": LB_CRITERIA["dl"]},
    "hf": {"region": "global", "board": "open_source", "key": "hf",
           "fn": lambda n: fetch_hf_open_ranking(n * 2),
           "label": "Hugging Face · Open LLM Leaderboard", "url": HF_LEADERBOARD_URL,
           "criteria": LB_CRITERIA["hf"]},
    "ms": {"region": "cn", "board": "open_source", "key": "ms",
           "fn": lambda n: fetch_modelscope_ranking(n),
           "label": "ModelScope 魔搭 · 开源模型热度", "url": MS_MODELS_URL,
           "criteria": ("评分标准：ModelScope 魔搭社区开源模型热度（按下载量排序，数据取自官方 "
                        "openapi/v1/models）。反映国内开源生态活跃度，非能力基准。")},
    # 2026-09-09 新增：HF 原站在国内不可达（datasets-server 无可用镜像，实测 401），
    # 改由 hf-mirror.com 取热门开源模型，保证国内环境开源榜不空。
    "hm": {"region": "cn", "board": "open_source", "key": "hm",
           "fn": lambda n: fetch_hf_mirror_popular(n),
           "label": "HF 镜像 · 热门开源模型", "url": HF_MIRROR_API,
           "criteria": ("评分标准：Hugging Face 热门开源模型下载量（经 hf-mirror.com 国内镜像获取，"
                        "仅收录文本生成/对话类）。反映实际采用热度，非能力基准分；国内可直接访问。")},
}


def _collect_source_results(top_n: int, detected: str, proxy: str):
    """L2#14：并行抓取所有榜源（ThreadPoolExecutor, max_workers=4），
    返回 {source_key: {"rows":[...], "latency_ms":int, "status":str}}。

    单源失败不阻断其他源；并行执行器异常时整体回退顺序抓取，保证鲁棒性。
    `_retry_fetch` 已在每个源内部提供重试退避（P0#10）。
    """
    keys = list(SOURCES.keys())

    def _one(key):
        spec = SOURCES[key]
        t0 = time.monotonic()
        try:
            rows = _retry_fetch(lambda: spec["fn"](top_n))
            lat = int((time.monotonic() - t0) * 1000)
            return key, (rows or []), lat, ("ok" if rows else "empty")
        except Exception as e:  # noqa: BLE001  best-effort 单源容错
            lat = int((time.monotonic() - t0) * 1000)
            logger.warning("榜源抓取失败 [%s]: %s", spec["label"], e)
            return key, [], lat, f"error:{type(e).__name__}"

    # S2(2026-09)：硬上限总墙钟时间，避免个别慢源拖垮整份周报生成。
    # 并发 + 单源隔离已就位（见 _one 的 try/except）；此处补「整体截止」这最后一块：
    # 超过 OVERALL_FETCH_CAP_S 仍未完成的源标记为 timeout 并跳过；已运行线程由各自
    # _http_get timeout 兜底、后台静默结束，shutdown(wait=False) 不再阻塞主流程。
    results = {}
    ex = concurrent.futures.ThreadPoolExecutor(max_workers=4)
    try:
        futs = {ex.submit(_one, k): k for k in keys}
        done, not_done = concurrent.futures.wait(futs, timeout=OVERALL_FETCH_CAP_S)
        for fut in done:
            k, rows, lat, st = fut.result()
            results[k] = {"rows": rows, "latency_ms": lat, "status": st}
        for fut in not_done:
            k = futs[fut]
            results[k] = {"rows": [], "latency_ms": OVERALL_FETCH_CAP_S * 1000,
                          "status": "timeout"}
            logger.warning("榜源抓取超时(整体 %ds 上限) [%s]，本源跳过",
                           OVERALL_FETCH_CAP_S, SOURCES[k]["label"])
        logger.info("并行抓取完成：%d 源，命中 %d（%d 超时）",
                    len(results),
                    sum(1 for v in results.values() if v["rows"]),
                    sum(1 for v in results.values() if v["status"] == "timeout"))
    except Exception as e:  # noqa: BLE001  并行异常回退顺序
        logger.warning("并行抓取异常，回退顺序抓取: %s", e)
        results = {}
        for k in keys:
            k2, rows, lat, st = _one(k)
            results[k2] = {"rows": rows, "latency_ms": lat, "status": st}
    finally:
        # 不等待仍在运行的慢源线程（wait=False），未开始的取消（cancel_futures=True）。
        ex.shutdown(wait=False, cancel_futures=True)
    return results


def _record_health(results: dict, detected: str):
    """L2#15：把本次各榜源健康快照 append 到 leaderboard_health.jsonl。
    每行 {ts,source,source_key,board,region,status,latency_ms,rows_count}。
    写入失败不阻断主流程（best-effort）。
    """
    try:
        ts = datetime.now().astimezone().isoformat(timespec="seconds")
        lines = []
        for key, spec in SOURCES.items():
            out = results.get(key, {}) or {}
            lines.append(json.dumps({
                "ts": ts,
                "source": spec["label"],
                "source_key": key,
                "board": spec["board"],
                "region": spec["region"],
                "net_region": detected,
                "status": out.get("status", "unknown"),
                "latency_ms": out.get("latency_ms", -1),
                "rows_count": len(out.get("rows") or []),
            }, ensure_ascii=False))
        with HEALTH_PATH.open("a", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")
        logger.info("健康记录已写入 %s（%d 条）", HEALTH_PATH.name, len(lines))
    except Exception as e:  # noqa: BLE001  健康记录失败不阻断
        logger.warning("健康记录写入失败: %s", e)


def inject_open_source_ranks(os_board: dict):
    """L3#21 兜底：实时抓取的开源榜(ls/hf)行可能缺 rank 字段，
    按当前顺序补 1..n，避免前端渲染出 undefined。"""
    for _slot in ("ls", "hf"):
        for _i, _r in enumerate(os_board.get(_slot, {}).get("rows") or [], start=1):
            if _r.get("rank") is None:
                _r["rank"] = _i


__all__ = [
    "HEALTH_PATH", "LB_CRITERIA", "SOURCES",
    "_collect_source_results", "_record_health", "inject_open_source_ranks",
]
