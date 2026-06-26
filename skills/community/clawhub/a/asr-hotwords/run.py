#!/usr/bin/env python3
"""
run.py — ASR 热词挖掘主控制器

Pipeline: 提取 OpenClaw 对话 → 本地 build_words 挖掘 → 输出歧义词表 → 导出 hotwords.md
"""

import argparse
import csv
import io
import json
import glob
import os
import sys
import tempfile
import logging
from datetime import datetime, timezone, timedelta
from pathlib import Path

import yaml

from extract_sessions import extract_sessions, format_chat_data
from build_words import build_pipeline

logger = logging.getLogger(__name__)

CST = timezone(timedelta(hours=8))
SCRIPT_DIR = Path(__file__).parent


def load_config() -> dict:
    """加载 config.yaml"""
    config_path = SCRIPT_DIR / "config.yaml"
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_openclaw_llm_config() -> dict:
    """从 ~/.openclaw/openclaw.json 自动读取 LLM 配置"""
    config_path = os.path.expanduser("~/.openclaw/openclaw.json")
    with open(config_path, "r", encoding="utf-8") as f:
        oc_config = json.load(f)

    primary = (
        oc_config.get("agents", {})
        .get("defaults", {})
        .get("model", {})
        .get("primary", "")
    )
    if "/" not in primary:
        raise ValueError(f"Cannot parse primary model: '{primary}', expected 'provider/model_id'")

    provider_name, model_id = primary.split("/", 1)

    providers = oc_config.get("models", {}).get("providers", {})
    if provider_name not in providers:
        providers = oc_config.get("providers", {})
    if provider_name not in providers:
        raise ValueError(f"Provider '{provider_name}' not found in openclaw.json")

    p = providers[provider_name]

    api_raw = p.get("api", "anthropic-messages")
    api_format = "anthropic" if "anthropic" in api_raw else "openai"

    return {
        "api_key": p.get("apiKey", ""),
        "base_url": p.get("baseUrl", ""),
        "model": model_id,
        "api_format": api_format,
    }


# ============================================================
# 导出模块
# ============================================================

def load_all_vocabs(output_dir: Path) -> list:
    """加载所有 vocab 文件，合并去重，过滤无效词条"""
    vocab_files = sorted(glob.glob(str(output_dir / "vocab_*.json")))
    vocab_files = [f for f in vocab_files if ".bak." not in f]

    merged = {}
    for fpath in vocab_files:
        try:
            with open(fpath, "r", encoding="utf-8") as f:
                data = json.load(f)
            for item in data.get("vocab", []):
                term = item["term"]
                if term in merged:
                    merged[term]["frequency"] = max(
                        merged[term].get("frequency", 0),
                        item.get("frequency", 0),
                    )
                    existing = set(merged[term].get("possible_asr_errors", []))
                    existing.update(item.get("possible_asr_errors", []))
                    merged[term]["possible_asr_errors"] = sorted(existing)
                    if len(item.get("desc", "")) > len(merged[term].get("desc", "")):
                        merged[term]["desc"] = item["desc"]
                else:
                    merged[term] = item.copy()
        except Exception as e:
            logger.warning(f"加载失败 {fpath}: {e}")

    result = sorted(merged.values(), key=lambda x: x.get("frequency", 0), reverse=True)
    return [
        v for v in result
        if v.get("desc", "").strip() or v.get("possible_asr_errors", [])
    ]


def load_anchors(output_dir: Path) -> list:
    """从 output 目录加载所有历史 vocab 结果，合并去重后作为 anchors"""
    vocab = load_all_vocabs(output_dir)
    if not vocab:
        logger.info("无历史 vocab 文件，anchors 为空")
        return []

    anchors = [
        {"term": v["term"], "category": v.get("category", "unknown"), "desc": v.get("desc", "")}
        for v in vocab
    ]
    logger.info(f"加载 {len(anchors)} 个 anchors（去重后）")
    return anchors


def export_txt(vocab: list) -> str:
    return "\n".join(item["term"] for item in vocab)


def export_json(vocab: list) -> str:
    output = []
    for item in vocab:
        output.append({
            "term": item["term"],
            "possible_asr_errors": item.get("possible_asr_errors", []),
            "category": item.get("category", ""),
            "desc": item.get("desc", ""),
        })
    return json.dumps(output, indent=2, ensure_ascii=False)


def export_csv(vocab: list) -> str:
    buf = io.StringIO()
    writer = csv.writer(buf)
    writer.writerow(["热词", "类别", "说明", "常见误识别", "词频"])
    for item in vocab:
        writer.writerow([
            item["term"],
            item.get("category", ""),
            item.get("desc", ""),
            "、".join(item.get("possible_asr_errors", [])),
            item.get("frequency", 0),
        ])
    return buf.getvalue()


def export_prompt(vocab: list) -> str:
    """按类别分组的 Markdown 热词表格式"""
    # 按 category 分组，unknown 归入 other
    groups = {}
    for item in vocab:
        cat = item.get("category", "other") or "other"
        if cat == "unknown":
            cat = "other"
        if cat not in groups:
            groups[cat] = []
        groups[cat].append(item)

    # category 中文映射
    cat_names = {
        "product": "产品术语",
        "tech_term": "技术术语",
        "person": "人名",
        "company": "企业/公司名",
        "ambiguous": "易混淆词",
        "other": "其他",
    }

    # 固定输出顺序
    order = ["product", "tech_term", "person", "company", "ambiguous", "other"]
    sections = []
    for cat in order:
        if cat not in groups:
            continue
        items = groups.pop(cat)
        label = cat_names.get(cat, cat)
        section_lines = [f"## {label}"]
        if cat == "ambiguous":
            # 易混淆词：用 ≠ 格式展示
            for item in items:
                errors = item.get("possible_asr_errors", [])
                if errors:
                    section_lines.append(f"- {item['term']} ≠ {'、'.join(errors)}")
                else:
                    section_lines.append(f"- {item['term']}")
        else:
            # 其他类别：词条 + 描述（如有）
            for item in items:
                desc = item.get("desc", "").strip()
                if desc:
                    section_lines.append(f"- {item['term']}（{desc}）")
                else:
                    section_lines.append(f"- {item['term']}")
        sections.append("\n".join(section_lines))

    # 剩余未知类别
    for cat, items in groups.items():
        label = cat_names.get(cat, cat)
        section_lines = [f"## {label}"]
        for item in items:
            desc = item.get("desc", "").strip()
            if desc:
                section_lines.append(f"- {item['term']}（{desc}）")
            else:
                section_lines.append(f"- {item['term']}")
        sections.append("\n".join(section_lines))

    return "# 语音纠错上下文\n\n" + "\n\n".join(sections) + "\n"



EXPORT_FORMATTERS = {
    "txt": export_txt,
    "json": export_json,
    "csv": export_csv,
    "prompt": export_prompt,
}


def export_hotwords(output_dir: Path, fmt: str = "prompt", output_file: Path = None, min_freq: int = 1):
    """从所有 vocab 文件导出热词表"""
    vocab = load_all_vocabs(output_dir)
    logger.info(f"导出热词表: {len(vocab)} 个热词")

    if min_freq > 1:
        vocab = [v for v in vocab if v.get("frequency", 0) >= min_freq]
        logger.info(f"词频 >= {min_freq} 过滤后: {len(vocab)} 个")

    result = EXPORT_FORMATTERS[fmt](vocab)

    if output_file:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(result)
        logger.info(f"热词表已导出到: {output_file}")
    return result


# ============================================================
# DMWork 注入通知
# ============================================================

def notify_agent_inject_dmwork(hotwords_path: Path, max_retries: int = 2):
    """
    通过 openclaw gateway call agent 通知 agent 将 hotwords.md 注入 DMWork 语音纠错上下文。
    发送结构化消息，agent 收到后调用 dmwork_management(voice-context-update)。
    """
    import subprocess
    import uuid

    if not hotwords_path.exists():
        logger.warning(f"hotwords.md 不存在: {hotwords_path}，跳过 DMWork 注入")
        return

    content = hotwords_path.read_text(encoding="utf-8").strip()
    if not content:
        logger.warning("hotwords.md 为空，跳过 DMWork 注入")
        return

    message = (
        "[asr-hotwords 自动任务] 热词挖掘已完成，请立即执行以下操作：\n"
        "1. 读取文件: {path}\n"
        "2. 调用 dmwork_management(action=\"voice-context-update\", content=文件内容)\n"
        "3. 调用 dmwork_management(action=\"voice-context-read\") 验证注入成功\n"
        "注意：这是自动化任务，无需通知用户，直接执行即可。"
    ).format(path=hotwords_path)

    for attempt in range(1, max_retries + 1):
        idempotency_key = f"asr-hotwords-dmwork-inject-{uuid.uuid4().hex[:8]}"
        params = json.dumps({
            "sessionKey": "agent:main:main",
            "message": message,
            "idempotencyKey": idempotency_key,
        })

        try:
            result = subprocess.run(
                ["openclaw", "gateway", "call", "agent", "--params", params, "--json"],
                capture_output=True, text=True, timeout=30,
            )
            if result.returncode == 0 and '"accepted"' in result.stdout:
                logger.info(f"DMWork 注入通知已发送 (第{attempt}次)")
                return
            else:
                logger.warning(f"DMWork 注入通知发送失败 (第{attempt}次): {result.stdout} {result.stderr}")
        except Exception as e:
            logger.warning(f"DMWork 注入通知异常 (第{attempt}次): {e}")

    logger.error(f"DMWork 注入通知失败，已重试 {max_retries} 次")


# ============================================================
# 主流程
# ============================================================

def run(target_date: str, end_date: str = None):
    """主流程：提取对话 → 本地挖掘 → 保存 → 导出"""
    config = load_config()
    extract_cfg = config["extract"]
    output_dir = SCRIPT_DIR / config.get("output_dir", "output")
    output_dir.mkdir(exist_ok=True)

    # 1. 加载 LLM 配置
    logger.info("从 openclaw.json 自动读取 LLM 配置...")
    llm_config = load_openclaw_llm_config()
    logger.info(f"  Model: {llm_config['model']}, Format: {llm_config['api_format']}")

    # 2. 提取对话
    agents = extract_cfg.get("agents", ["*"])
    logger.info(f"提取对话: {target_date}" + (f" ~ {end_date}" if end_date else "") + f" (agents: {agents})")
    messages = extract_sessions(
        target_date=target_date,
        agents=agents,
        max_content_len=extract_cfg.get("max_content_len", 300),
        end_date=end_date,
    )

    if not messages:
        logger.warning("未提取到任何消息，退出")
        print(json.dumps({"status": "empty", "message": "无可用对话数据"}, ensure_ascii=False))
        return

    logger.info(f"提取到 {len(messages)} 条消息")

    # 3. 准备临时文件
    chat_data = format_chat_data(messages)
    chat_tmp = tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False, encoding="utf-8")
    chat_tmp.write(chat_data)
    chat_tmp.close()

    # 4. 准备 anchors 文件
    anchors = load_anchors(output_dir)
    anchors_tmp = None
    if anchors:
        anchors_tmp = tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False, encoding="utf-8")
        json.dump(anchors, anchors_tmp)
        anchors_tmp.close()

    # 5. 保存路径
    date_label = target_date if not end_date or end_date == target_date else f"{target_date}_{end_date}"
    output_path = output_dir / f"vocab_{date_label}.json"

    # 如果同日期结果已存在，备份
    if output_path.exists():
        ts_suffix = datetime.now(CST).strftime("%H%M%S")
        backup_path = output_dir / f"vocab_{date_label}.{ts_suffix}.bak.json"
        output_path.rename(backup_path)
        logger.info(f"已备份旧结果: {backup_path.name}")

    # 6. 执行本地 build_pipeline
    logger.info("开始本地热词挖掘...")
    try:
        success, error = build_pipeline(
            chat_path=chat_tmp.name,
            anchor_path=anchors_tmp.name if anchors_tmp else None,
            output_path=str(output_path),
            api_key=llm_config["api_key"],
            base_url=llm_config["base_url"],
            model=llm_config["model"],
            api_format=llm_config["api_format"],
            min_freq=extract_cfg.get("min_freq", 3),
            validate=False,
        )
    finally:
        # 清理临时文件
        os.unlink(chat_tmp.name)
        if anchors_tmp:
            os.unlink(anchors_tmp.name)

    if not success:
        logger.error(f"热词挖掘失败: {error}")
        print(json.dumps({"status": "error", "message": error}, ensure_ascii=False))
        return

    # 7. 读取结果
    with open(output_path, "r", encoding="utf-8") as f:
        result_data = json.load(f)

    # 补充 meta 信息
    result_data["meta"] = {
        "source": "asr-hotwords",
        "target_date": target_date,
        "end_date": end_date or target_date,
        "built_at": datetime.now(CST).isoformat(),
        "messages_count": len(messages),
    }
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result_data, f, indent=2, ensure_ascii=False)

    vocab = result_data.get("vocab", [])
    logger.info(f"挖掘完成: {len(vocab)} 条热词")

    # 8. 导出 hotwords.md
    hotwords_path = SCRIPT_DIR / "hotwords.md"
    export_hotwords(output_dir, fmt="prompt", output_file=hotwords_path)

    # 9. 通知 agent 注入 DMWork 语音纠错上下文
    notify_agent_inject_dmwork(hotwords_path)

    # 10. 输出摘要
    summary = {
        "status": "success",
        "date": date_label,
        "messages_count": len(messages),
        "vocab_count": len(vocab),
        "output_file": str(output_path),
        "top_terms": [
            {
                "term": v["term"],
                "freq": v.get("frequency", 0),
                "asr_errors": v.get("possible_asr_errors", []),
            }
            for v in vocab[:10]
        ],
    }
    print(json.dumps(summary, indent=2, ensure_ascii=False))


def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
        datefmt="%H:%M:%S",
    )

    parser = argparse.ArgumentParser(description="ASR 热词挖掘")
    parser.add_argument("--date", default=None, help="目标日期 YYYY-MM-DD（默认前一天）")
    parser.add_argument("--start", default=None, help="起始日期")
    parser.add_argument("--end", default=None, help="结束日期")
    parser.add_argument("--export-only", action="store_true", help="仅导出热词表，不执行挖掘")
    parser.add_argument("--format", "-f", choices=["txt", "json", "csv", "prompt"], default="prompt", help="导出格式")
    parser.add_argument("--output", "-o", default=None, help="导出文件路径")
    parser.add_argument("--min-freq", type=int, default=1, help="导出时最低词频过滤")
    args = parser.parse_args()

    # 仅导出模式
    if args.export_only:
        output_dir = SCRIPT_DIR / "output"
        output_file = Path(args.output) if args.output else None
        result = export_hotwords(output_dir, fmt=args.format, output_file=output_file, min_freq=args.min_freq)
        if not args.output:
            print(result)
        return

    if args.start:
        target_date = args.start
        end_date = args.end or args.start
    elif args.date:
        target_date = args.date
        end_date = args.date
    else:
        yesterday = datetime.now(CST) - timedelta(days=1)
        target_date = yesterday.strftime("%Y-%m-%d")
        end_date = target_date

    run(target_date=target_date, end_date=end_date)


if __name__ == "__main__":
    main()
