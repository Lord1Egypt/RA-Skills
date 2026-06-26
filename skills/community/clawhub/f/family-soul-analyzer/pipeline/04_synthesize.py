"""
阶段4：合成 soul.md + 三个 persona
=====================================
初次生成：
  python3 pipeline/04_synthesize.py

版本更新（每季度/半年）：
  python3 pipeline/04_synthesize.py --update
    --previous-soul outputs/soul_v1.0.md   # 上一版本路径
    --since 2025-10-01                      # 只取这个日期之后的新观察
    --include-moments                       # 是否合并朋友圈观察

输入：data/observations/observations.jsonl
      prompts/synthesize_soul.md（首次）
      prompts/synthesize_soul_update.md（更新）
      prompts/synthesize_persona.md
输出：outputs/soul.md（以及带版本号的备份 soul_vX.Y.md）
      outputs/persona_dad.md
      outputs/persona_mom.md
      outputs/persona_son.md

使用 claude-opus-4-5 + streaming
"""

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import anthropic
from config import (
    ANTHROPIC_API_KEY, DATA_DIR, FAMILY_CONTEXT,
    OUTPUTS_DIR, PROMPTS_DIR, SON_CONTEXT, SYNTHESIZE_MODEL,
)
from utils import load_jsonl, print_step, save_text


ROLE_INFO = {
    "dad": {
        "display": "爸爸",
        "description": "父亲，倾向于理性/结构化思维，通过行动和建议表达爱",
    },
    "mom": {
        "display": "妈妈",
        "description": "母亲，情感导向，关注关系和日常细节，直接表达关怀",
    },
    "son": {
        "display": "孩子",
        "description": "家庭中的孩子，处于人生重要成长阶段",
    },
    "child": {
        "display": "孩子",
        "description": "家庭中的孩子，处于人生重要成长阶段",
    },
}


def observations_to_text(obs_list: list[dict], max_obs: int = 200) -> str:
    """把观察数据格式化成 LLM 可读的文本摘要"""
    # 按 context_tags 聚合，取最有信号的观察
    high_signal = [o for o in obs_list if o.get("has_signal", True)]
    # 采样（如果太多）
    if len(high_signal) > max_obs:
        import random
        random.seed(42)
        high_signal = random.sample(high_signal, max_obs)

    lines = []
    for i, obs in enumerate(high_signal):
        lines.append(f"\n--- 观察 {i+1} ({obs.get('time_range', '')}) ---")
        o = obs.get("observations", {})

        # 语言特征
        lang = o.get("language", {})
        if isinstance(lang, dict):
            for role, desc in lang.items():
                if desc and desc != "无明显信号":
                    lines.append(f"  语言[{role}]: {desc}")
        elif lang and lang != "无明显信号":
            lines.append(f"  语言: {lang}")

        # 其他维度
        for key, label in [
            ("emotional_patterns", "情感模式"),
            ("values", "价值观"),
            ("relational_dynamics", "关系动态"),
            ("collective_identity", "集体人格"),
        ]:
            val = o.get(key, "")
            if val and val != "无明显信号":
                lines.append(f"  {label}: {val}")

        # 代表性引用
        quotes = obs.get("notable_quotes", [])
        if quotes:
            for q in quotes[:2]:  # 每个观察最多取 2 条引用
                role = q.get("role", "")
                quote = q.get("quote", "")
                why = q.get("why_notable", "")
                if quote:
                    lines.append(f"  引用[{role}]: 「{quote}」 → {why}")

    return "\n".join(lines)


def role_observations_to_text(obs_list: list[dict], role: str) -> str:
    """聚焦某个角色的观察"""
    lines = []
    for obs in obs_list:
        if not obs.get("has_signal", True):
            continue
        o = obs.get("observations", {})
        role_parts = []

        # 语言特征（该角色）
        lang = o.get("language", {})
        if isinstance(lang, dict) and role in lang:
            val = lang[role]
            if val and val != "无明显信号":
                role_parts.append(f"语言习惯: {val}")

        # 该角色的引用
        quotes = obs.get("notable_quotes", [])
        role_quotes = [q for q in quotes if q.get("role") == role]
        for q in role_quotes[:2]:
            role_parts.append(f"说过: 「{q.get('quote', '')}」（{q.get('why_notable', '')}）")

        if role_parts:
            lines.append(f"\n[{obs.get('time_range', '')}]")
            lines.extend(f"  · {p}" for p in role_parts)

    # 还要加上关系动态和情感模式里涉及该角色的信息
    for obs in obs_list:
        if not obs.get("has_signal", True):
            continue
        o = obs.get("observations", {})
        for key in ("emotional_patterns", "relational_dynamics"):
            val = o.get(key, "")
            if val and val != "无明显信号" and role in val:
                # 只有提到这个角色的段落才收录
                lines.append(f"  [{key}] {val}")

    return "\n".join(lines) if lines else "（未提取到足够的角色特定信息，请参考集体观察）"


def stream_synthesis(client: anthropic.Anthropic, prompt: str, label: str) -> str:
    """流式调用 Claude，边生成边打印，返回完整文本。遇到速率限制自动等待重试。"""
    import time

    max_retries = 5
    base_wait = 60  # 秒

    for attempt in range(max_retries):
        try:
            print(f"\n  🔄 正在生成 {label}…\n")
            full_text = []

            with client.messages.stream(
                model=SYNTHESIZE_MODEL,
                max_tokens=4096,
                messages=[{"role": "user", "content": prompt}],
            ) as stream:
                for event in stream:
                    if event.type == "content_block_delta":
                        if event.delta.type == "text_delta":
                            chunk = event.delta.text
                            print(chunk, end="", flush=True)
                            full_text.append(chunk)

            final = stream.get_final_message()
            print(f"\n\n  ✓ 完成（输入 {final.usage.input_tokens} tokens，输出 {final.usage.output_tokens} tokens）")
            return "".join(full_text)

        except anthropic.RateLimitError as e:
            if attempt == max_retries - 1:
                raise
            wait = base_wait * (attempt + 1)
            print(f"\n  ⏳ 速率限制，等待 {wait} 秒后重试（第 {attempt + 1}/{max_retries} 次）…")
            time.sleep(wait)

    raise RuntimeError("stream_synthesis: 超过最大重试次数")


def compute_time_span(obs_list: list[dict]) -> str:
    ranges = [o.get("time_range", "") for o in obs_list if o.get("time_range")]
    if not ranges:
        return "未知时间范围"
    all_times = []
    for r in ranges:
        parts = r.split("~")
        all_times.extend(p.strip() for p in parts if p.strip())
    all_times.sort()
    if len(all_times) >= 2:
        return f"{all_times[0][:7]} ～ {all_times[-1][:7]}"
    return all_times[0][:7] if all_times else "未知"


def parse_version(soul_content: str) -> tuple[str, str]:
    """从 soul.md 内容中提取版本号和生成日期"""
    version_match = re.search(r'版本：(v[\d.]+)', soul_content)
    date_match = re.search(r'生成于：(\d{4}-\d{2}-\d{2})', soul_content)
    version = version_match.group(1) if version_match else "v1.0"
    date = date_match.group(1) if date_match else "未知"
    return version, date


def increment_version(version: str) -> str:
    """v1.0 → v1.1，v1.9 → v2.0"""
    match = re.match(r'v(\d+)\.(\d+)', version)
    if not match:
        return "v1.1"
    major, minor = int(match.group(1)), int(match.group(2))
    if minor >= 9:
        return f"v{major + 1}.0"
    return f"v{major}.{minor + 1}"


def filter_observations_since(obs_list: list, since_date: str) -> list:
    """只保留 since_date 之后的观察"""
    result = []
    for obs in obs_list:
        time_range = obs.get("time_range", "")
        # 取结束时间（time_range 格式: "2025-01-01 12:00 ~ 2025-01-01 13:00"）
        end_time = time_range.split("~")[-1].strip() if "~" in time_range else time_range
        if end_time >= since_date:
            result.append(obs)
    return result


def load_all_observations(include_moments: bool = False) -> list:
    """加载所有 observations，可选合并朋友圈和图片"""
    obs_path = DATA_DIR / "observations" / "observations.jsonl"
    all_obs = load_jsonl(obs_path) if obs_path.exists() else []

    if include_moments:
        # 合并朋友圈观察
        for moments_file in (DATA_DIR / "observations").glob("moments_*.jsonl"):
            all_obs.extend(load_jsonl(moments_file))
            print(f"  合并朋友圈观察：{moments_file.name}")

        # 合并图片观察
        img_path = DATA_DIR / "observations" / "image_observations.jsonl"
        if img_path.exists():
            img_obs = load_jsonl(img_path)
            # 只取有信号的图片观察
            img_obs = [o for o in img_obs if o.get("has_signal", True)]
            all_obs.extend(img_obs)
            print(f"  合并图片观察：{len(img_obs)} 条")

    return all_obs


def main():
    parser = argparse.ArgumentParser(description="阶段4：合成 soul.md + persona")
    parser.add_argument("--update", action="store_true",
                        help="更新模式：基于上一版本做增量更新")
    parser.add_argument("--previous-soul", type=str,
                        help="上一版 soul.md 的路径（更新模式必填）")
    parser.add_argument("--since", type=str,
                        help="只使用此日期之后的新观察（格式：YYYY-MM-DD）")
    parser.add_argument("--include-moments", action="store_true",
                        help="是否合并朋友圈和图片观察")
    parser.add_argument("--soul-only", action="store_true",
                        help="只生成 soul.md，跳过 persona（更新模式常用）")
    args = parser.parse_args()

    mode = "更新" if args.update else "首次生成"
    print_step(4, f"合成 soul.md + 三个 persona（{mode}）")

    if not ANTHROPIC_API_KEY:
        print("✗ 请设置 ANTHROPIC_API_KEY 环境变量")
        sys.exit(1)

    import httpx
    client = anthropic.Anthropic(
        api_key=ANTHROPIC_API_KEY,
        http_client=httpx.Client(proxy=None),
    )

    # ── 加载观察数据 ───────────────────────────────────────────────────────────
    all_obs = load_all_observations(include_moments=args.include_moments)
    print(f"  读入 {len(all_obs):,} 条观察记录")

    persona_prompt_template = (PROMPTS_DIR / "synthesize_persona.md").read_text(encoding="utf-8")

    # ══════════════════════════════════════════════════════════════════════════
    # 首次生成模式
    # ══════════════════════════════════════════════════════════════════════════
    if not args.update:
        soul_prompt_template = (PROMPTS_DIR / "synthesize_soul.md").read_text(encoding="utf-8")
        time_span = compute_time_span(all_obs)
        obs_text = observations_to_text(all_obs)

        soul_prompt = (
            soul_prompt_template
            .replace("{{OBSERVATION_COUNT}}", str(len(all_obs)))
            .replace("{{TIME_SPAN}}", time_span)
            .replace("{{OBSERVATIONS_TEXT}}", obs_text)
        )

        soul_content = stream_synthesis(client, soul_prompt, "soul.md（集体人格）")

        # 注入版本元数据（首次为 v1.0）
        today = datetime.now().strftime("%Y-%m-%d")
        version_header = f"<!-- 版本：v1.0 | 生成于：{today} | 数据时段：{time_span} -->\n"
        soul_content = version_header + soul_content

        save_text(soul_content, OUTPUTS_DIR / "soul.md")
        # 同时保存带版本号的备份
        save_text(soul_content, OUTPUTS_DIR / "soul_v1.0.md")

    # ══════════════════════════════════════════════════════════════════════════
    # 更新模式
    # ══════════════════════════════════════════════════════════════════════════
    else:
        # 加载上一版本 soul
        prev_soul_path = Path(args.previous_soul) if args.previous_soul else OUTPUTS_DIR / "soul.md"
        if not prev_soul_path.exists():
            print(f"✗ 找不到上一版 soul.md：{prev_soul_path}")
            sys.exit(1)

        prev_soul_content = prev_soul_path.read_text(encoding="utf-8")
        prev_version, prev_date = parse_version(prev_soul_content)
        new_version = increment_version(prev_version)
        today = datetime.now().strftime("%Y-%m-%d")

        print(f"  上一版本：{prev_version}（{prev_date}）→ 新版本：{new_version}")

        # 筛选新观察
        if args.since:
            new_obs = filter_observations_since(all_obs, args.since)
            period_start = args.since
            print(f"  筛选 {args.since} 之后的观察：{len(new_obs)} 条（共 {len(all_obs)} 条）")
        else:
            new_obs = all_obs
            period_start = compute_time_span(all_obs).split("～")[0].strip()

        period_end = today
        new_obs_text = observations_to_text(new_obs, max_obs=150)

        # 统计各来源数量
        moments_count = sum(1 for o in new_obs if o.get("source") == "wechat_moments")
        image_count = sum(1 for o in new_obs if o.get("source") == "image")
        chat_count = len(new_obs) - moments_count - image_count

        update_prompt_template = (PROMPTS_DIR / "synthesize_soul_update.md").read_text(encoding="utf-8")
        soul_prompt = (
            update_prompt_template
            .replace("{{PREVIOUS_SOUL}}", prev_soul_content)
            .replace("{{PERIOD_START}}", period_start)
            .replace("{{PERIOD_END}}", period_end)
            .replace("{{NEW_OBS_COUNT}}", str(chat_count))
            .replace("{{MOMENTS_COUNT}}", str(moments_count))
            .replace("{{IMAGE_COUNT}}", str(image_count))
            .replace("{{NEW_OBSERVATIONS_TEXT}}", new_obs_text)
            .replace("{{NEW_VERSION}}", new_version)
            .replace("{{PREV_VERSION}}", prev_version)
            .replace("{{PREV_DATE}}", prev_date)
            .replace("{{GENERATION_DATE}}", today)
            .replace("{{FAMILY_NAME}}", "三头怪")  # 可从 config 读取
            .replace("{{CURRENT_CHAPTER_TITLE}}", f"{today[:7]} 当前章节")
        )

        soul_content = stream_synthesis(client, soul_prompt, f"soul.md（{new_version} 更新）")

        # 备份旧版本
        backup_path = OUTPUTS_DIR / f"soul_{prev_version}.md"
        if not backup_path.exists():
            save_text(prev_soul_content, backup_path)
            print(f"  已备份旧版本 → {backup_path.name}")

        save_text(soul_content, OUTPUTS_DIR / "soul.md")
        save_text(soul_content, OUTPUTS_DIR / f"soul_{new_version}.md")
        print(f"  新版本已保存：soul.md + soul_{new_version}.md")

    # ── 从这里开始两种模式共用：生成 persona ──────────────────────────────────
    if args.soul_only:
        print("\n  ⏭ --soul-only 模式，跳过 persona 生成")
    else:
        soul_content_for_persona = (OUTPUTS_DIR / "soul.md").read_text(encoding="utf-8")

        import time
        roles = list(ROLE_INFO.items())
        for idx, (role_key, info) in enumerate(roles):
            # persona 之间等待，避免 Opus 速率限制（30k tokens/min）
            if idx > 0:
                print("\n  ⏳ 等待 65 秒，避免速率限制…")
                time.sleep(65)

            role_obs_text = role_observations_to_text(all_obs, role_key)

            family_ctx = FAMILY_CONTEXT
            if role_key == "son":
                family_ctx = FAMILY_CONTEXT + "\n\n" + SON_CONTEXT

            persona_prompt = (
                persona_prompt_template
                .replace("{{ROLE_DISPLAY}}", info["display"])
                .replace("{{SOUL_CONTENT}}", soul_content_for_persona)
                .replace("{{ROLE_OBSERVATIONS}}", role_obs_text)
                .replace("{{FAMILY_CONTEXT}}", family_ctx)
            )

            persona_content = stream_synthesis(
                client, persona_prompt, f"persona_{role_key}.md（{info['display']}）"
            )
            save_text(persona_content, OUTPUTS_DIR / f"persona_{role_key}.md")

    print("\n" + "─" * 60)
    print("  ✅ 所有文件生成完毕！")
    print(f"  📁 {OUTPUTS_DIR}")
    for f in sorted(OUTPUTS_DIR.iterdir()):
        size = f.stat().st_size
        print(f"     {f.name:30s}  {size:,} bytes")


if __name__ == "__main__":
    main()
