#!/usr/bin/env python3
"""
BG 吴江数字人 - 转录增强模块 (v1.0)

新增能力：
  1. LLM语义修复（字幕/AI修复）
  2. VAD重点采样（时长×能量波动）
  3. 逐级放大ASR（tiny→base）
  4. 结构化分析（摘要+关键词+章节）

与现有工作流的集成点：
  - process_video() 中替换"subtitle fast lane"逻辑
  - 增加后处理：结构化分析
"""

import json
import os
import re
import subprocess as sp
import sys
import time
from typing import Dict, List, Optional, Tuple

# ── LLM API 通用配置（通过环境变量配置，兼容任何 OpenAI 兼容接口） ──
DEEPSEEK_API_KEY = os.environ.get("LLM_API_KEY") or os.environ.get("OPENAI_API_KEY") or ""
DEEPSEEK_BASE = os.environ.get("LLM_BASE_URL") or os.environ.get("OPENAI_BASE_URL") or "https://api.deepseek.com/v1"
LLM_MODEL = os.environ.get("LLM_MODEL", "deepseek-v4-flash")      # 批量修复用（快）
ANALYSIS_MODEL = os.environ.get("ANALYSIS_MODEL") or LLM_MODEL     # 分析用
LLM_BATCH_SIZE = 20                   # 每批最多20段

# ── 纠错词典（与bili_subtitle_fetcher共享） ──
CORRECTIONS = {
    # 交易领域术语
    "单里吃": "单笔", "单位吃": "单笔", "单位": "单边",
    "單米值": "單筆值", "单米值": "单笔值", "單米": "單筆", "单米": "单笔",
    "三榜": "三宝", "三绑": "三宝", "三棒": "三宝",  # 杰克三宝
    "脏色": "止损", "脏收": "止损", "只损": "止损",
    "防抗过": "怕是空", "进热真乐": "境界",
    "大台街": "大台阶", "刺射": "亏损", "刺数": "亏损",
    "吃算": "持仓", "持昌": "持仓", "吃昌": "持仓",
    "黑线": "K线", "开线": "K线", "K开线": "K线",
    "运线": "均线", "君线": "均线",
    "玉线": "孕线", "运线": "均线",
    "分辨力": "执行力", "执行人": "执行力",
    "风控": "风控",  # 可能已经正确
    "标穿": "标仓", "鞭长": "标仓",
    "阴力": "盈利", "银里": "盈利", "盈利": "盈利",
    "胡仓": "浮仓", "胡亏": "浮亏", "浮亏": "浮亏",
    "金叉": "金叉", "死叉": "死叉",
    "顶分型": "顶分形", "底分型": "底分形",
    "童花寸": "同花顺", "同花寸": "同花顺",
    "长幅拍明": "涨幅排名",
    "平霸": "平台", "品台": "平台",
    "黄镜": "黄金", "皇镜": "黄金",
    "收脸": "收敛", "收殓": "收敛",
    "文文": "稳稳", "吻吻": "稳稳",
    "善呼": "散户", "闪户": "散户", "赞户": "散户",
    "狂单": "扛单", "航单": "扛单",
    "感让": "杠杆", "赶杆": "杠杆",
    "过票": "股票", "鬼票": "股票",
    "执存": "止存", "止存": "止损",  # whisper经常把止损变体
    "方抗": "风控",
    "评论值": "凭运气", "屏运气": "凭运气",
    "林娜": "琳娜",  # 人名
    "薄罪": "最", "薄": " ",  # 语气词清理
    "一符": "一笔", "衣服": "一笔",
}

# ── VAD噪声阈值 ──
SILENCE_THRESHOLD = -35  # dBFS


# ═══════════════════════════════════════════════════════════════
# 1a. 三层提示词模板（2026-05-10 新增）
# ═══════════════════════════════════════════════════════════════

DOMAIN_PROMPTS = {
    "trading": {
        "role": "听写速记员 - 交易/金融领域",
        "description": "交易课程、策略分享、行情分析",
        "system_prompt": """你是一个专业的【听写速记员】，正在处理金融交易领域语音识别输出的原始文本。

### 你的核心任务
原始文本来自whisper语音识别，存在大量同音错字、断句错误、角色混淆。
你需要将其复原为通顺的对话记录。

### 交易领域必备知识
- 术语：K线、均线、MACD、止损、止盈、金叉、死叉、布林带、仓位、杠杆、浮亏、暴仓
- 行话：刀=美元/点、手、仓、扛单、分批建仓、高抛低吸、追涨杀跌
- 指标：盈亏比、胜率、回撤、风控、执行力
- 行情：黄金、外汇、美股、A股、期货、比特币
- 概念：趋势、震荡、支撑、压力、突破、回调

### 典型whisper错误模式
- "善户/赞户" → "散户"
- "脏色/止色/只损" → "止损"
- "狂单/航单" → "扛单"
- "进热/静热" → "进取"
- "分控/方抗" → "风控"
- "黑线/开线/K开线" → "K线"
- "运线/君线" → "均线"
- "黄镜/皇镜" → "黄金"
- "刺" → "次"（如"多少刺"→"多少次"）
- "一符/衣服" → "一笔"（如"一符一符"→"一笔一笔"）
- "台街/台阶/大台阶" → "台阶"
- 数字+"品"+"交" → 数字+"笔"+"交"
- "定率 → 定律"、"增理 → 真理"、"大量出气体 → 大量出奇迹"

### ⚠️ 常识检查（重要！）
修复时同步检查以下内容，发现明显错误直接修正：
- **时间顺序**：不会出现"1月3号之后又出现1月2号"这种倒流
- **数字合理性**："3274点"合理，"3724点"可能就是顺序错了
- **因果关系**："因为A所以B"逻辑要通，不通可能是whisper听错
- **专业名词**：以交易领域实际术语为准

### 输出要求
1. 正确断句加标点（句号、逗号、冒号、引号）
2. 如有多人对话，用"甲：... 乙：..."区分角色
3. 保留说话人特有的口语风格（填充词、语气词）
4. 交易金额单位"刀"保留（是行话，不是错字）
5. 无法理解的乱码标记为 [unclear]
6. 不改原意，不编造内容，不添加额外解释

输出JSON格式: {{"corrected": "修正后文本", "confidence": 0.0-1.0}}""",
    },
    "tech": {
        "role": "听写速记员 - 科技/编程领域",
        "description": "编程教程、技术分享、产品评测",
        "system_prompt": """你是一个专业的【听写速记员】，正在处理科技领域语音识别输出的原始文本。

### 你的核心任务
原始文本来自whisper语音识别，存在大量同音错字、断句错误、角色混淆。
你需要将其复原为通顺的对话记录。

### 技术领域常见术语
- 编程：函数、变量、API、框架、前端、后端、部署、调试、编译
- 架构：微服务、容器、K8s、数据库、缓存、队列、负载均衡
- AI/ML：模型、训练、推理、数据集、参数、token、embedding

### 典型whisper错误模式
- "接口 → 接口"、"部署 → 部署"、"变量 → 变量"

### 输出要求
1. 正确断句加标点
2. 保留技术术语的英文原文
3. 保留口语风格
4. 不改原意，不编造内容

输出JSON格式: {{"corrected": "修正后文本", "confidence": 0.0-1.0}}""",
    },
    "general": {
        "role": "听写速记员",
        "description": "通用内容（兜底）",
        "system_prompt": """你是一个专业的【听写速记员】，正在处理语音识别输出的原始文本。

### 你的核心任务
原始文本来自whisper语音识别，存在大量同音错字、断句错误。
你需要将其复原为通顺的文字记录。

### 输出要求
1. 正确断句加标点（句号、逗号）
2. 如有多人对话，用"甲：... 乙：..."区分角色
3. 保留说话人的口语风格
4. 无法理解的乱码标记为 [unclear]
5. 不改原意，不编造内容

输出JSON格式: {{"corrected": "修正后文本", "confidence": 0.0-1.0}}""",
    },
}

# ── 说话人口头禅/错词包（以up主名或说话人名为key） ──
SPEAKER_CORRECTIONS = {
    "张聚贤": {
        "alias": ["胖杰克", "张聚贤说交易"],
        "corrections": {
            "单位": "单边",
            "单位吃": "单笔",
            "单位之": "单笔",
            "一符": "一笔",
            "衣服": "一笔",
            "大台街": "大台阶",
            "进热": "进取",
            "增热": "境界",
            "三榜": "三宝",  # 杰克三宝
            "三绑": "三宝",
            "结合三宝": "杰克三宝",  # 常见whisper误认
            "结合三宝的": "杰克三宝的",
            "结合三宝形态": "杰克三宝形态",
            "倒水的线": "倒锤线",  # 锤子线/倒锤蜡烛图
            "倒水线": "倒锤线",
        "跌平早": "跌平涨",  # whisper常见误认 涨→早
        "深证指数": "恒生指数",  # whisper常见误认 恒→深
        "主力结构": "阻力结构",  # whisper常见同音误认，精确匹配避免误杀"主力吸筹"等
        "主力位": "阻力位",
        "主力区": "阻力区",
        "主力过": "阻力过",
        "尺寸": "止损",  # whisper常见误认（交易语境"止损"远多于"尺寸"）
        "到死了": "到手了",  # whisper同音误认
        "到了": "到手",
        "二看": "你看",  # whisper常见同音误认（句子开头）
        "牛逼手": "牛逼之处",  # 张聚贤口音+whisper误认
        "排单": "卖单",  # 交易语境阻力区卖单
        "图形之神": "图形止损法",  # 三种止损法之一
        "图形之死扛": "图形止损法",
        "十之间": "时间止损",  # 时间止损法 whisper误认
        "十之间之神": "时间止损法",
        "头单": "爆仓单",
        "头大": "爆仓",
        "死头到底": "死扛到底",
        "换算都做好了": "方法都讲好了",
        "禁止高": "禁止扛",
        "止损之神": "净值止损法",  # 三种止损法之一：净值止损法
            "黄了": "慌了",
            "黄": "慌",
            "红尖": "红线",  # 均线相关
            "运线": "孕线",  # 孕线口音+whisper误认（张聚贤口音偏"韵"）
            "晕线": "孕线",
            "硬线": "孕线",
            "景线": "颈线",  # 颈线/neckline
            "景线位": "颈线位",
            "吞沫": "吞没",  # K线吞噬形态
            "村莫": "吞没",
            "拼帮": "Pinbar",
            "拼霸": "Pinbar",
            "拼罢": "Pinbar",
            "拼盼": "Pinbar",
            "平仓": "Pinbar",
            "线车": "K线",
            "吞摸": "吞没",
            "逆报全法": "逆波全法",
            "云线吞磨": "均线吞没",
            "运线上破": "孕线上破",
            "上一线下一线": "上孕线下孕线",
        },
        "habits": """这是【胖杰克/张聚贤】的交易教学视频，他的口头习惯包括：
- 口语填充词："是不是嘛"、"对吧"、"你懂吧"
- "大量出奇迹"（不是"气体"）
- 强调"一笔一笔"（不是"一符一符"）
- "拼罢"实际是"Pinbar"（针形反转线）
- "拼盼"实际是"Pinbar"（whisper常见误认）
- "线车"实际是"K线"
- "吞摸"实际是"吞没形态"
- "吃吐"实际是"持筹/持股"
- "孕线"发音偏"运线"（口音习惯，实际是孕线/Inside Bar）
- 经常说"单位/单边"、"台阶"（不是"台街"）
- 语调快，略带东北口音
- "杰克三宝"系列：不追高、不重仓、选优质标的（双底颈线位+龙头）""",
    },
    "听风的蚕": {
        "alias": ["听风的蚕"],
        "corrections": {
            # 暂无，待积累
        },
        "habits": """这是【听风的蚕】的时事分析视频，他的特点包括：
- 逻辑严密，语速中等
- 大量引用历史和政治事件""",
    },
    "吴江": {
        "alias": ["BG吴江", "前华为BG吴江"],
        "corrections": {
            "林林后": "00后",
            "林后": "00后",
        },
        "habits": """这是【吴江】的管理方法论视频，前华为企业BG高管，他的特点包括：
- 擅长用真实故事案例讲管理（如带00后爬黄山）
- 口头禅："对不对"、"是吧"
- 核心方法论：目标管理、流程管理、风险控制、团队激励、项目管理
- 风格：场景化训战，先讲故事后提炼方法
- 常讲"00后"（whisper易误识为"林林后"）
- "呼就站起来了"→实际是"嚯就站起来了"（语气词）
- 强调"人性化管理"、"赋能"、"搭舞台"
- 内容对象：中基层管理者、企业培训""",
    },
}


def _guess_domain(video_title: str = "", uploader: str = "") -> str:
    """从视频标题+UP主名猜测领域
    
    同时检查标题和UP主名，解决合集分集标题不含关键词时仍能正确分类
    例如: 标题"20210908 院长专栏"无关键词，但UP主"张聚贤说交易"含"交易"
    """
    texts_to_check = [video_title.lower(), uploader.lower()]
    trading_kw = ["交易", "止损", "K线", "止盈", "盈亏", "仓位", "杠杆",
                  "期货", "外汇", "股票", "黄金", "炒股", "A股", "美股",
                  "行情", "投资", "基金", "量化", "盘面", "做单", "做盘",
                  "亏损", "赚", "跌", "涨", "获利", "卖飞", "买在",
                  "股", "仓", "单", "风险", "大盘", "杰克", "均线", "底",
                  "轻仓", "爆仓", "支撑", "压力"]
    tech_kw = ["编程", "代码", "API", "框架", "前端", "后端", "部署",
               "Python", "Java", "JavaScript", "开发", "架构", "算法"]
    for text in texts_to_check:
        for kw in trading_kw:
            if kw in text:
                return "trading"
        for kw in tech_kw:
            if kw in text:
                return "tech"
    return "general"


def _match_speaker(uploader: str) -> Optional[str]:
    """匹配up主/说话人，返回speaker key"""
    uploader_lower = uploader.lower().replace(" ", "")
    for speaker, data in SPEAKER_CORRECTIONS.items():
        name = uploader_lower
        for alias in data.get("alias", []):
            if alias in name:
                return speaker
        if speaker in name:
            return speaker
    return None


def _select_prompt(domain: str, speaker: Optional[str] = None) -> str:
    """
    选择最终的系统提示词

    组合逻辑：
    1. 领域基础提示词
    2. 叠加说话人口头禅提示
    """
    if domain not in DOMAIN_PROMPTS:
        domain = "general"

    base = DOMAIN_PROMPTS[domain]["system_prompt"]

    # 叠加说话人信息
    if speaker and speaker in SPEAKER_CORRECTIONS:
        habits = SPEAKER_CORRECTIONS[speaker].get("habits", "")
        if habits:
            base += f"\n\n### 说话人信息\n{habits}"

    return base


def _speaker_corrections_text(text: str, speaker: Optional[str] = None) -> str:
    """应用说话人专属纠错"""
    if not speaker or speaker not in SPEAKER_CORRECTIONS:
        return text
    corr = SPEAKER_CORRECTIONS[speaker].get("corrections", {})
    sorted_c = sorted(corr.items(), key=lambda x: len(x[0]), reverse=True)
    for wrong, correct in sorted_c:
        text = text.replace(wrong, correct)
    return text

def _call_llm(messages: List[Dict], model: str = None,
              max_tokens: int = 8192, temperature: float = 0.1,
              timeout: int = 60) -> Optional[str]:
    """
    调用 DeepSeek API

    Args:
        messages: [{"role": "system"/"user", "content": str}, ...]
        model: 模型名（默认LLM_MODEL）
        max_tokens: 最大输出token
        temperature: 温度（修复类任务用0.1，分析类用0.3）

    Returns:
        response text or None
    """
    model = model or LLM_MODEL
    payload = {
        "model": model,
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": temperature,
        "stream": False,
    }

    try:
        import tempfile
        _tmp = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
        json.dump(payload, _tmp, ensure_ascii=True)
        _tmp_path = _tmp.name
        _tmp.close()
        try:
            r = sp.run(
                ["curl", "-s", "--connect-timeout", "15", "--max-time", str(timeout),
                 f"{DEEPSEEK_BASE}/chat/completions",
                 "-H", f"Authorization: Bearer {DEEPSEEK_API_KEY}",
                 "-H", "Content-Type: application/json",
                 "-d", f"@{_tmp_path}"],
                capture_output=True, text=True, timeout=timeout
            )
        finally:
            try:
                os.unlink(_tmp_path)
            except OSError:
                pass
        if r.returncode != 0:
            print(f"    [LLM] ❌ curl退出码={r.returncode}, stderr={r.stderr[:200]}")
            return None

        data = json.loads(r.stdout)
        if "choices" in data and len(data["choices"]) > 0:
            content = data["choices"][0]["message"].get("content", "").strip()
            if not content:
                # reasoning模型的思考消耗了全部token，没留空间给content
                fr = data["choices"][0].get("finish_reason", "?")
                rc_len = len(data["choices"][0]["message"].get("reasoning_content", ""))
                print(f"    [LLM] ⚠️ content为空, finish_reason={fr}, reasoning={rc_len}字")
                print(f"    [LLM]    → max_tokens={max_tokens}不够, 需加大")
            return content if content else None
        else:
            # API返回了有效HTTP响应但无choices → 错误响应
            err_body = r.stdout[:500]
            print(f"    [LLM] ❌ API返回无choices, body={err_body}")
    except json.JSONDecodeError as e:
        _out = r.stdout[:300] if ('r' in dir() and r and r.stdout) else 'N/A'
        print(f"    [LLM] ❌ JSON解析失败: {e}, body={_out}")
    except sp.TimeoutExpired:
        print(f"    [LLM] ❌ curl超时 ({timeout}s)")
    except Exception as e:
        print(f"    [LLM] ❌ 异常: {type(e).__name__}: {e}")
    return None


# ============================================================
# 2. 字幕分段 + LLM修复
# ============================================================

def subtitle_to_segments(subtitle_data: Dict) -> List[Dict]:
    """
    将B站字幕解析为时间戳分段

    输入: bili_subtitle_fetcher.fetch_subtitle() 返回的字典
    输出: [{"start": 0.0, "end": 5.0, "text": "..."}, ...]
    """
    body = subtitle_data.get("body", [])
    if not body:
        return []

    segments = []
    for item in body:
        segments.append({
            "start": item.get("from", 0.0),
            "end": item.get("to", 0.0),
            "text": item.get("content", "").strip(),
        })

    return segments


def llm_fix_segment(segment: Dict, domain: str = "", speaker: Optional[str] = None,
                     ocr_context: str = "") -> Dict:
    """
    LLM修复单个字幕段

    Args:
        segment: {"start": 0, "end": 5, "text": "..."}
        domain: 领域（trading/tech/general），影响提示词
        speaker: 说话人/up主名，叠加口头禅纠错
        ocr_context: 同时间段视频画面 OCR 文字（辅助纠正）

    Returns: segment with "fixed_text", "is_qualified", "fix_log"
    """
    system_prompt = _select_prompt(domain, speaker)
    
    text = segment.get("text", "")
    if not text.strip():
        return {**segment, "fixed_text": "", "is_qualified": False, "confidence": 0.0}

    # 第一步：说话人专属纠错
    pre_cleaned = _speaker_corrections_text(text, speaker)
    # 第二步：全局纠错词典
    pre_cleaned = apply_all_corrections(pre_cleaned)

    # 第三步：如果提供了OCR上下文，加到prompt里
    user_content = pre_cleaned
    if ocr_context:
        user_content = f"""转录文本：{pre_cleaned}

【视频画面OCR文字，用于辅助判断无法听清的内容】
{ocr_context}

请结合OCR文字判断转录中是否有识别错误，特别是画面中明显出现的关键词。"""

    resp = _call_llm([
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_content},
    ], temperature=0.1, max_tokens=500)

    if not resp:
        return {**segment, "fixed_text": text, "is_qualified": False, "confidence": 0.5}

    try:
        result = json.loads(resp)
        fixed = result.get("corrected", text)
        conf = result.get("confidence", 0.5)
    except (json.JSONDecodeError, KeyError):
        fixed = resp.strip()
        conf = 0.5

    # 后纠错（catch domain terms LLM might have missed）
    fixed = apply_all_corrections(fixed)

    is_qualified = conf >= 0.7

    return {**segment, "fixed_text": fixed, "is_qualified": is_qualified, "confidence": conf}


def llm_fix_batch(segments: List[Dict], batch_size: int = None,
                   domain: str = "", speaker: Optional[str] = None) -> List[Dict]:
    """
    批量LLM修复（优化API调用次数）

    将多个段打包成一次API调用

    Args:
        segments: 字幕段列表
        batch_size: 每批数量
        domain: 领域（trading/tech/general）
        speaker: 说话人/up主名

    Returns: 修复后的段列表
    """
    batch_size = batch_size or LLM_BATCH_SIZE
    results = []

    domain_info = DOMAIN_PROMPTS.get(domain, DOMAIN_PROMPTS["general"])
    system_prompt_batch = _select_prompt(domain, speaker)

    # 分组
    for i in range(0, len(segments), batch_size):
        batch = segments[i:i+batch_size]

        texts = [s["text"] for s in batch]
        prompt = f"请逐条修复以下【{domain_info['description']}】字幕。每条字幕独立修复，保持序号对应。\n\n"
        for j, t in enumerate(texts):
            prompt += f"[{j+1}] {t}\n\n"
        prompt += "\n输出JSON数组：[{\"corrected\": \"...\", \"confidence\": 0.9}, ...]"

        resp = _call_llm([
            {"role": "system", "content": system_prompt_batch},
            {"role": "user", "content": prompt},
        ], temperature=0.1, max_tokens=min(batch_size * 200, 4000), timeout=60)

        if not resp:
            # 回退到逐条修复
            for seg in batch:
                results.append(llm_fix_segment(seg, domain=domain, speaker=speaker))
            continue

        try:
            fixes = json.loads(resp)
            for j, fix in enumerate(fixes):
                seg = batch[j]
                corrected = fix.get("corrected", seg["text"])
                conf = fix.get("confidence", 0.5)
                # 应用说话人纠错+全局纠错
                corrected = _speaker_corrections_text(corrected, speaker)
                corrected = apply_all_corrections(corrected)
                results.append({**seg, "fixed_text": corrected,
                                "is_qualified": conf >= 0.7, "confidence": conf})
        except (json.JSONDecodeError, TypeError, IndexError):
            # 回退到逐条修复
            for seg in batch:
                results.append(llm_fix_segment(seg, domain=domain, speaker=speaker))

    return results


def split_by_quality(segments: List[Dict], threshold: float = 0.7) -> Tuple[List[Dict], List[Dict]]:
    """按质量分达标/不达标分流"""
    qualified = [s for s in segments if s.get("is_qualified", False) and s.get("confidence", 0) >= threshold]
    unqualified = [s for s in segments if not (s.get("is_qualified", False) and s.get("confidence", 0) >= threshold)]
    return qualified, unqualified


# ============================================================
# 3. VAD 重点采样（智能抽检）
# ============================================================

def compute_energy_volatility(audio_path: str, start_time: float, end_time: float) -> float:
    """
    计算指定时间范围内音频的能量波动（RMS标准差）

    波动大 → 语速快/音调高/多人对话 → 重点采样
    波动小 → 语速平稳/单人讲述 → 非重点

    Returns: 归一化波动值 (0.0 ~ 1.0)
    """
    duration = end_time - start_time
    if duration <= 0:
        return 0.5

    # 提取音频段为临时文件
    tmp_path = f"/tmp/bili_work/vol_sample_{int(start_time)}.wav"
    r = sp.run(
        ["ffmpeg", "-i", audio_path, "-ss", str(start_time),
         "-t", str(duration), "-ar", "16000", "-ac", "1",
         "-sample_fmt", "s16", "-y", tmp_path],
        capture_output=True, text=True, timeout=30
    )
    if r.returncode != 0 or not os.path.exists(tmp_path):
        return 0.5

    # 用ffprobe取音频RMS统计
    try:
        # 按100ms分帧，计算每帧RMS
        result = sp.run(
            ["ffprobe", "-v", "error", "-f", "wav",
             "-show_entries", "frame=pkt_size",
             "-of", "csv=p=0", tmp_path],
            capture_output=True, text=True, timeout=30
        )
        sizes = [int(x) for x in result.stdout.strip().split("\n") if x.strip().isdigit()]

        import numpy as np
        if len(sizes) > 10:
            # 归一化方差（标准差/均值）
            std = np.std(sizes)
            mean = np.mean(sizes)
            volatility = std / (mean + 1)
            # 限制在 0-1 范围
            volatility = min(1.0, volatility / 1.5)
            return volatility
    except ImportError:
        # 没有numpy，用简单方法
        if len(sizes) > 10:
            avg = sum(sizes) / len(sizes)
            variance = sum((x - avg) ** 2 for x in sizes) / len(sizes)
            std = variance ** 0.5
            volatility = min(1.0, std / (avg + 1) / 2)
            return volatility
    except Exception:
        pass
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)

    return 0.5


def smart_sample(unqualified_segments: List[Dict], audio_path: str,
                 top_pct: float = 0.15, min_samples: int = 3) -> List[Dict]:
    """
    VAD重点采样--按"时长×能量波动"权重抽检

    算法：
      1. 对每个VAD段计算两个指标：duration（时长）、energy_volatility（能量波动）
      2. 权重分 = 0.6 * norm_dur + 0.4 * norm_vol
      3. 按权重从高到低排序
      4. 抽取前 top_pct 段落（至少 min_samples 个）

    Args:
        unqualified_segments: 不达标字幕段列表 [{"start":..., "end":..., "text":...}]
        audio_path: 音频文件路径
        top_pct: 抽检比例（0.15 = 15%）
        min_samples: 最少抽检数

    Returns: 选中的采样段列表（按权重排序）
    """
    if not unqualified_segments:
        return []

    # 为每个段计算得分
    scored = []
    for seg in unqualified_segments:
        dur = seg.get("end", 0) - seg.get("start", 0)
        if dur <= 0:
            continue

        vol = compute_energy_volatility(audio_path, seg["start"], seg["end"])

        # 归一化时长（假设最长段可达到300s）
        norm_dur = min(1.0, dur / 300.0)

        # 权重分
        score = 0.6 * norm_dur + 0.4 * vol
        scored.append({**seg, "sample_score": score, "energy_volatility": vol})

    # 按权重从高到低
    scored.sort(key=lambda x: x["sample_score"], reverse=True)

    # 抽检
    n_samples = max(min_samples, int(len(scored) * top_pct))
    sampled = scored[:n_samples]

    return sampled


# ============================================================
# 4. 逐级放大ASR
# ============================================================

TMP_DIR = "/tmp/bili_work"

def cascade_asr(audio_path: str, start_time: float, end_time: float,
                min_model: str = "tiny") -> str:
    """
    逐级放大ASR：提取音频段 → tiny转录 → 质量检查 → 不行就base

    不跑small/medium（base封顶原则）

    Args:
        audio_path: 音频文件路径
        start_time: 起始秒
        end_time: 结束秒
        min_model: 起始模型（默认tiny）

    Returns: 转录文本，或空字符串
    """
    duration = end_time - start_time
    if duration <= 0:
        return ""

    # 提取音频段
    seg_path = f"{TMP_DIR}/cascade_{int(start_time)}_{int(end_time)}.wav"
    sp.run(
        ["ffmpeg", "-i", audio_path, "-ss", str(start_time),
         "-t", str(duration), "-ar", "16000", "-ac", "1",
         "-sample_fmt", "s16", "-y", seg_path],
        capture_output=True, text=True, timeout=30
    )

    if not os.path.exists(seg_path):
        return ""

    timeouts = {
        "tiny": max(60, int(duration * 0.5)),
        "base": max(120, int(duration * 2)),
    }

    text = ""
    for model in [min_model, "base"]:
        try:
            # 优先faster-whisper
            try:
                from faster_transcriber import transcribe_audio_segment
                text = transcribe_audio_segment(seg_path, language="zh")
                if text and text.strip() and text[0] != "[":
                    break
            except Exception:
                pass
            
            # fallback: 标准whisper CLI
            r = sp.run(
                ["whisper", "--model", model, "--language", "zh",
                 "--output_format", "txt",
                 "--output_dir", TMP_DIR, seg_path],
                capture_output=True, text=True,
                timeout=timeouts.get(model, 120)
            )

            out_txt = os.path.join(TMP_DIR, os.path.basename(seg_path).replace(".wav", ".txt"))
            if os.path.exists(out_txt):
                with open(out_txt) as f:
                    text = f.read()
                if text.strip():
                    break  # 有结果就停
        except sp.TimeoutExpired:
            continue
        except Exception:
            continue

        # 如果tiny质量的文本太短，尝试base
        if model == "tiny" and len(text.strip()) < 5:
            continue

    # 清理
    for f in [seg_path]:
        if os.path.exists(f):
            os.remove(f)

    return text.strip() or ""


# ============================================================
# 5. 结构化分析
# ============================================================

def structured_analysis(full_text: str, max_summary_chars: int = 200) -> Dict:
    """
    对完整转录文本做结构化分析

    Returns:
        {
            "summary": "200字摘要",
            "keywords": ["关键词", ...],
            "chapters": [{"title": "...", "time_range": "00:00-05:30"}],
            "topics": ["主题1", "主题2", ...],
        }
    """
    if not full_text or len(full_text) < 50:
        return {"summary": "(内容太少，无法分析)", "keywords": [], "chapters": []}

    # 截取前8000字符给LLM（API限制）
    text_for_analysis = full_text[:8000]

    system_prompt = f"""分析以下视频转录文本，输出结构化摘要。

要求：
- 摘要：{max_summary_chars}字以内，概括核心内容
- 关键词：提取5个核心关键词
- 章节：如果内容有明显分段，输出章节（每章标题+大致的行号）
- 主题：概括2-3个核心讨论主题

输出JSON格式：
{{"summary":"...","keywords":["kw1","kw2","kw3","kw4","kw5"],"chapters":[{{"title":"...","line_start":10,"line_end":50}}],"topics":["t1","t2"]}}"""

    resp = _call_llm([
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"转录文本：\n{text_for_analysis}"},
    ], model=ANALYSIS_MODEL, max_tokens=8192, temperature=0.3, timeout=120)  # v3: 推理模型

    if not resp:
        return {"summary": "(LLM分析失败)", "keywords": [], "chapters": []}

    try:
        # 尝试提取JSON（可能被markdown包裹）
        json_match = re.search(r'\{[\s\S]*\}', resp)
        if json_match:
            result = json.loads(json_match.group(0))
            return {
                "summary": result.get("summary", ""),
                "keywords": result.get("keywords", []),
                "chapters": result.get("chapters", []),
                "topics": result.get("topics", []),
            }
    except (json.JSONDecodeError, KeyError):
        pass

    return {"summary": resp[:200], "keywords": [], "chapters": []}


# ============================================================
# 5b. 批量结构化分析（多视频合并一次API调用）
# ============================================================

def batch_structured_analysis(videos: List[Dict]) -> Dict[str, Dict]:
    """
    批量分析多个视频的转录文本 → 一次API调用出所有结果

    Args:
        videos: [{"bv": "BV1xxx", "title": "...", "text": "..."}, ...]
    
    Returns:
        {
            "series_summary": "这组视频的整体主题总结",
            "series_keywords": ["kw1", ...],
            "videos": {
                "BV1xxx": {"summary":"...", "keywords":[...], "chapters":[...], "topics":[...]},
                ...
            }
        }
        
    节省: N次独立分析 → 1次，省 (N-1)×30s
    """
    if not videos:
        return {}
    
    # 过滤掉过短的文本
    valid = [v for v in videos if v.get("text", "").strip() and len(v["text"]) >= 30]
    if not valid:
        return {}
    
    # 构建批量prompt
    parts = []
    for v in valid:
        bv = v.get("bv", "?")
        title = v.get("title", "")[:60]
        text = v["text"][:2000]  # 每个视频截取前2000字
        parts.append(f"--- 视频: {bv} - {title} ---\n{text}")
    
    block = "\n\n".join(parts)
    n = len(valid)
    
    system_prompt = f"""你是视频内容分析助手。下面是一组(共{n}个)短视频的转录文本，来自同一个UP主。
    
请为**每个视频**单独生成：
1. 摘要（80字以内）
2. 关键词（3-5个）
3. 章节（如有明显分段，标题+行号）
4. 核心主题（1-2个）

另外，给这组视频的整体总结：概括这组视频的共同主题和UP主的核心观点。

输出JSON格式：
{{
  "series_summary": "整体总结，100字以内",
  "series_keywords": ["整体关键词1", "整体关键词2", "整体关键词3"],
  "videos": {{
    "BV1xxxx": {{
      "summary": "该视频摘要",
      "keywords": ["kw1", "kw2"],
      "chapters": [{{"title": "章节名", "line_start": 1, "line_end": 20}}],
      "topics": ["主题1"]
    }},
    "BV1yyyy": {{...}}
  }}
}}

注意：每个视频的key必须是BV号。只输出纯JSON，不要markdown包裹。"""

    resp = _call_llm([
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"转录文本列表：\n{block}"},
    ], model=ANALYSIS_MODEL, max_tokens=8192, temperature=0.3, timeout=120)
    
    if not resp:
        # fallback: 逐个分析
        result = {}
        for v in valid:
            result[v["bv"]] = structured_analysis(v["text"])
        return {"series_summary": "(批量分析失败，回退逐个)", "series_keywords": [], "videos": result}
    
    try:
        # 提取JSON
        json_match = re.search(r'\{[\s\S]*\}', resp)
        if json_match:
            result = json.loads(json_match.group(0))
            # 确保所有视频都有结果
            for v in valid:
                if v["bv"] not in result.get("videos", {}):
                    result.setdefault("videos", {})[v["bv"]] = structured_analysis(v["text"])
            return result
    except (json.JSONDecodeError, KeyError) as e:
        pass
    
    return {"series_summary": "(批量分析解析失败)", "series_keywords": [], "videos": {}}


def batch_format_analysis_markdown(batch_result: Dict) -> str:
    """格式化批量分析结果为markdown（含整体+每个视频）"""
    lines = []
    lines.append("## 📊 系列内容分析")
    lines.append("")
    
    series_summary = batch_result.get("series_summary", "")
    if series_summary and "批量" not in series_summary:
        lines.append("### 系列总览")
        lines.append(series_summary)
        lines.append("")
    
    series_keywords = batch_result.get("series_keywords", [])
    if series_keywords:
        lines.append("### 系列关键词")
        lines.append("`" + "`, `".join(series_keywords) + "`")
        lines.append("")
    
    videos = batch_result.get("videos", {})
    if not videos:
        lines.append("*（无分析数据）*")
        return "\n".join(lines)
    
    lines.append("### 各视频分析")
    lines.append("")
    
    for bv, vinfo in videos.items():
        title = vinfo.get("title", bv)
        summary = vinfo.get("summary", "")
        keywords = vinfo.get("keywords", [])
        topics = vinfo.get("topics", [])
        chapters = vinfo.get("chapters", [])
        
        lines.append(f"#### [{bv}] {title}")
        if summary:
            lines.append(f"> {summary}")
        if keywords:
            lines.append(f"> **关键词**: `{'`, `'.join(keywords)}`")
        if topics:
            lines.append(f"> **主题**: {' / '.join(topics)}")
        if chapters:
            lines.append(f"> **章节**: {len(chapters)}段")
        lines.append("")
    
    return "\n".join(lines)


# ============================================================
# 6. 分析报告格式化
# ============================================================

def format_analysis_markdown(analysis: Dict) -> str:
    """将结构化分析格式化为markdown"""
    lines = []
    lines.append("## 📊 内容分析")
    lines.append("")

    summary = analysis.get("summary", "")
    if summary:
        lines.append("### 摘要")
        lines.append(summary)
        lines.append("")

    keywords = analysis.get("keywords", [])
    if keywords:
        lines.append("### 关键词")
        lines.append("`" + "`, `".join(keywords) + "`")
        lines.append("")

    topics = analysis.get("topics", [])
    if topics:
        lines.append("### 核心主题")
        for t in topics:
            lines.append(f"- **{t}**")
        lines.append("")

    chapters = analysis.get("chapters", [])
    if chapters:
        lines.append("### 章节分段")
        for ch in chapters:
            title = ch.get("title", f"章节")
            ls = ch.get("line_start", "?")
            le = ch.get("line_end", "?")
            lines.append(f"- **{title}** (行{ls}-{le})")
        lines.append("")

    return "\n".join(lines)


# ============================================================
# 7. 纠错词典（与bili_subtitle_fetcher兼容）
# ============================================================

def llm_enhance_text(raw_text: str, chunk_size: int = 300,
                     domain: str = "", speaker: Optional[str] = None,
                     video_title: str = "") -> str:
    """
    对任意whisper转录文本进行LLM语义增强

    1. 按句号/换行分段
    2. 每chunk_size字一批
    3. 批量送LLM修复
    4. 纠错词典兜底

    Args:
        raw_text: 原始转录文本
        chunk_size: 每批最大字数（默认300字）

    Returns:
        LLM修复后的文本
    """
    if not raw_text or len(raw_text.strip()) < 20:
        return raw_text

    # 按句号/问号/感叹号/换行切分成句
    sentences = re.split(r'(?<=[。！？\n])', raw_text)
    sentences = [s.strip() for s in sentences if s.strip()]

    if not sentences:
        return raw_text

    # 分批：每批不超过 chunk_size 字
    batches = []
    current_batch = []
    current_len = 0

    for s in sentences:
        if current_len + len(s) > chunk_size and current_batch:
            batches.append(current_batch)
            current_batch = [s]
            current_len = len(s)
        else:
            current_batch.append(s)
            current_len += len(s)

    if current_batch:
        batches.append(current_batch)

    # 每批转segments
    all_fixed = []
    for batch_idx, batch_sents in enumerate(batches):
        segments = []
        for i, sent in enumerate(batch_sents):
            idx = batch_idx * len(batch_sents) + i
            segments.append({"start": idx * 2.0, "end": (idx + 1) * 2.0, "text": sent})

        fixed = llm_fix_batch(segments, domain=domain, speaker=speaker)
        for s in fixed:
            txt = apply_all_corrections(s.get("fixed_text", ""))
            if txt:
                all_fixed.append(txt)

    return "\n".join(all_fixed)


def apply_all_corrections(text: str) -> str:
    """应用领域纠错词典 + 正则修复"""
    if not text:
        return text
    # 按长度降序排列（长词先匹配，避免短词误替换）
    sorted_corrections = sorted(CORRECTIONS.items(), key=lambda x: len(x[0]), reverse=True)
    for wrong, correct in sorted_corrections:
        text = text.replace(wrong, correct)
    # 正则修复：行尾"数字+到" → "数字+刀"（交易行话：刀=美元/点）
    text = re.sub(r'(\d+)到([，。  ！？、]|$)', r'\1刀\2', text)
    return text


# ============================================================
# OCR 对齐工具（v2.0）
# ============================================================

def align_ocr_to_segment(
    segment_start: float,
    segment_end: float,
    ocr_timeline: List[Dict],
    persistent_text: str = "",
    window_pad: float = 2.0,
) -> str:
    """
    将 OCR 文字按时间窗口对齐到 Whisper 片段

    Args:
        segment_start: 片段起始时间（秒）
        segment_end: 片段结束时间（秒）
        ocr_timeline: ocr_video_timeline() 返回的 timeline 列表
        persistent_text: 全局持久文字（由 ocr_video_timeline.persistent 拼接）
        window_pad: 前后放宽秒数

    Returns:
        OCR 上下文文本，格式为：
        【全局固定画面】: 一行或多行
        【当前画面(窗口Xs-Ys)】: 该窗口内出现的瞬态文字（如有）
    """
    parts = []
    
    # 全局持久文字
    if persistent_text:
        parts.append(f"【视频全局固定画面】\n{persistent_text}")
    
    # 查找时间窗口内的瞬态 OCR
    window_start = max(0, segment_start - window_pad)
    window_end = segment_end + window_pad
    
    local_texts = []
    for entry in ocr_timeline:
        ts = entry.get("timestamp", 0)
        text = entry.get("text", "").strip()
        if window_start <= ts <= window_end and text:
            local_texts.append(f"  [{ts:.1f}s] {text}")
    
    if local_texts:
        parts.append(
            f"【当前画面(时间窗口{window_start:.0f}s-{window_end:.0f}s)】\n"
            + "\n".join(local_texts)
        )
    
    if not parts:
        return ""
    
    return "\n\n".join(parts)


def get_persistent_text(ocr_result: Dict) -> str:
    """从 ocr_video_timeline 结果中提取持久文字用于 prompt"""
    persistent = ocr_result.get("persistent", [])
    if not persistent:
        return ""
    return "\n".join(f"  {line}" for line in persistent)


def build_ocr_global_section(ocr_result: Dict) -> str:
    """构建 OCR 全局上下文段落（用于 full-text prompt）"""
    if not ocr_result or not ocr_result.get("persistent"):
        return ""
    lines = ocr_result["persistent"]
    return (
        "\n## 视频画面固定文字（OCR提取，贯穿全视频）\n"
        + "\n".join(f"- {line}" for line in lines)
        + "\n"
    )


def build_ocr_aligned_section(
    low_conf_words: List[Tuple[str, float]],
    raw_segments: List[Dict],
    ocr_timeline: List[Dict],
    persistent_text: str,
    full_text: str = "",  # v1.8.1: 完整文本，用于精确位置匹配
) -> str:
    """
    构建时间对齐的 OCR 参考段落（用于 full-text prompt）

    对每个低置信词，找到它所属的 segment，然后找到对应时间窗口的 OCR 文字
    
    v1.8.1: 用字符位置匹配取代文本匹配，避免段内多字误配
    """
    if not low_conf_words or not raw_segments:
        return ""
    
    if not ocr_timeline:
        return ""
    
    # 预处理：构建分段累积位置映射（v1.8.1 精确匹配）
    import re as _re
    seg_ranges = []
    char_pos = 0
    for seg in raw_segments:
        seg_text = seg.get("text", "")
        start_pos = char_pos
        end_pos = char_pos + len(seg_text)
        seg_ranges.append((start_pos, end_pos))
        char_pos = end_pos + 1  # segments join with \n/space
    
    def _find_segment_by_word(word: str) -> Optional[Dict]:
        """用字符位置找 segment（优先）或文本匹配（兜底）"""
        if full_text:
            m = _re.search(_re.escape(word), full_text)
            if m:
                word_pos = m.start()
                for i, seg in enumerate(raw_segments):
                    if not seg_ranges or i >= len(seg_ranges):
                        continue
                    s_start, s_end = seg_ranges[i]
                    if s_start <= word_pos < s_end:
                        return seg
        # 兜底：文本匹配
        for seg in raw_segments:
            if word in seg.get("text", ""):
                return seg
        return None
    
    # 为每个低置信词找所属 segment
    matched_pairs = []
    for word, prob in low_conf_words:
        seg = _find_segment_by_word(word)
        if seg is None:
            continue
        aligned = align_ocr_to_segment(
            seg.get("start", 0),
            seg.get("end", 0),
            ocr_timeline,
            persistent_text,
            window_pad=2.0,
        )
        if aligned:
            matched_pairs.append({
                "word": word,
                "prob": prob,
                "seg_start": seg.get("start", 0),
                "seg_end": seg.get("end", 0),
                "ocr": aligned,
            })
    
    if not matched_pairs:
        return ""
    
    parts = ["\n## 低置信词对应画面参考（时间对齐）\n"]
    for pair in matched_pairs:
        parts.append(
            f"### 低置信词「{pair['word']}」(置信度{pair['prob']}) "
            f"@ {pair['seg_start']:.0f}s-{pair['seg_end']:.0f}s\n"
            f"{pair['ocr']}\n"
        )
    
    return "\n".join(parts)


# ============================================================
# 自测试
# ============================================================

def test_llm():
    """验证LLM API可用"""
    print("[测试] LLM API...")
    resp = _call_llm([
        {"role": "system", "content": "你只说一个字"},
        {"role": "user", "content": "回复：好"}
    ], max_tokens=100)
    print(f"  响应: '{resp}'")
    return bool(resp and resp.strip())


if __name__ == "__main__":
    if "--test" in sys.argv:
        test_llm()
