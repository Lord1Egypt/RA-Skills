#!/usr/bin/env python3
"""Render two scheme-based comparison reports for 陈舒婷 2026-03."""

from __future__ import annotations

import re
from pathlib import Path


GREEN = "#2e7d32"
YELLOW = "#b26a00"
RED = "#d32f2f"
BLACK = "#111111"
COLOR = {"🟢": GREEN, "🟡": YELLOW, "🔴": RED, "⚫": BLACK}


def judgment_block(light: str, reason: str, scheme: str) -> str:
    color = COLOR[light]
    lines = [
        f"- <span style=\"color:{color}; font-weight:700;\">三灯判断：{light}</span>",
        f"  <span style=\"color:{color}; font-weight:700;\">判断理由：{reason}</span>",
    ]
    if light == "🟢":
        lines.extend(
            [
                f"  <span style=\"color:{color}; font-weight:700;\">人工判断：待确认（请填写：同意 / 不同意）</span>",
                f"  <span style=\"color:{color}; font-weight:700;\">若同意：请明确填写“同意”。</span>",
                f"  <span style=\"color:{color}; font-weight:700;\">若不同意：请填写理由类别（BP不清晰 / 举证材料不足 / AI判断错误 / 其他）及具体说明。</span>",
            ]
        )
    elif light == "🟡" and scheme == "v1":
        lines.extend(
            [
                f"  <span style=\"color:{color}; font-weight:700;\">复核判断：待确认（请填写：认可黄灯原因 / 不认可黄灯原因）</span>",
                f"  <span style=\"color:{color}; font-weight:700;\">若认可：请说明准备采取的应对预案，并明确预计转为绿灯的时间。</span>",
                f"  <span style=\"color:{color}; font-weight:700;\">若不认可：请说明为什么不认可（例如实际应标绿灯/红灯，或黄灯原因不成立）。</span>",
            ]
        )
    else:
        lines.extend(
            [
                f"  <span style=\"color:{color}; font-weight:700;\">人工判断：待确认（请填写：同意 / 不同意）</span>",
                f"  <span style=\"color:{color}; font-weight:700;\">若同意：请明确填写“同意”。</span>",
                f"  <span style=\"color:{color}; font-weight:700;\">若不同意：请填写理由类别（BP不清晰 / 举证材料不足 / AI判断错误 / 其他）及具体说明。</span>",
            ]
        )
        if light == "⚫":
            lines.extend(
                [
                    f"  <span style=\"color:{color}; font-weight:700;\">黑灯类型：需人工复核后选择（未开展/未执行 / 已开展但未关联 / 体外开展但体系内无留痕）</span>",
                    f"  <span style=\"color:{color}; font-weight:700;\">请人工回答：当前属于哪一种黑灯类型？</span>",
                    f"  <span style=\"color:{color}; font-weight:700;\">若未开展：请回答下月/下周期准备怎么做。</span>",
                    f"  <span style=\"color:{color}; font-weight:700;\">若已开展但未关联：请回答需补关联的材料/汇报是什么。</span>",
                    f"  <span style=\"color:{color}; font-weight:700;\">若体外开展但无留痕：请回答需补什么留痕、何时补齐。</span>",
                ]
            )
        lines.extend(
            [
                f"  <span style=\"color:{color}; font-weight:700;\">整改方案：待补充</span>",
                f"  <span style=\"color:{color}; font-weight:700;\">承诺完成时间：待补充</span>",
                f"  <span style=\"color:{color}; font-weight:700;\">下周期具体举措：待补充</span>",
            ]
        )
    return "\n".join(lines)


def replace_range(text: str, start_marker: str, end_marker: str, replacement: str) -> str:
    start = text.index(start_marker)
    end = text.index(end_marker, start)
    return text[:start] + replacement + text[end:]


def replace_first_judgment_block(section_text: str, new_block: str) -> str:
    pattern = re.compile(
        r"- <span style=.*?>三灯判断：[🟢🟡🔴⚫]</span>\n(?:  <span style=.*?>.*?</span>\n?)+",
        re.S,
    )
    return pattern.sub(new_block + "\n", section_text, count=1)


def replace_section_block(text: str, heading: str, next_heading: str, new_block: str) -> str:
    start = text.index(heading)
    end = text.index(next_heading, start)
    section = text[start:end]
    section = replace_first_judgment_block(section, new_block)
    return text[:start] + section + text[end:]


def insert_ch4_block(text: str, heading: str, next_heading: str, block: str) -> str:
    start = text.index(heading)
    end = text.index(next_heading, start)
    section = text[start:end].rstrip() + "\n" + block + "\n\n"
    return text[:start] + section + text[end:]


def apply_scheme(base_text: str, scheme: str) -> str:
    if scheme == "v1":
        title_suffix = "对比版-版本一"
        scheme_note = (
            "> 灯规则版本：`版本一（黄灯不强制整改，仅需上级认可/补充说明）`\n"
            "> 解释口径：绿灯从严、黄灯偏关注、红灯/黑灯进入整改。"
        )
        mapping = {
            "summary": ("🟡", "3 月虽然有充分推进证据，但战略绩效、长期激励和流程线上化条线仍有本月关键节点未闭环或仅部分完成，按版本一的从严绿灯标准仍不能判绿。"),
            "next": ("🟡", "4 月若要转绿，必须把系统稳定性、调薪拍板执行和流程条线留痕这几项关键节点真正收口，否则仍会维持黄灯。"),
            "2.1": ("🟡", "试点运行、问题修复和系数评议都已推进，但 3 月 31 日前应完成的人机协同评定模型开发测试与首批系数校准尚未形成完整闭环证据，按版本一应判黄。"),
            "2.2": ("🟡", "终稿请示、征询和修订已完成，但“业务激励方案已生效”及 3 月发布实施的证据尚未完全闭环，按版本一从严标准应判黄。"),
            "2.3": ("🟡", "专项方案请示已形成，但法务/财务会签、审批通过和执行规则书面化尚未全部完成，本月关键节点只算部分完成。"),
            "2.4": ("🟡", "流程和预算确有推进，但当前主要停留在需求评审和方案拆解阶段，且本人主证据不足，按版本一只能判黄。"),
            "3.1": ("🟡", "机制已经跑起来，但 3 月的开发测试、首批系数校准和稳定运行证据仍未完全闭环，因此结果层面仍为黄灯。"),
            "3.2": ("🟡", "调薪终稿、系数评议和业务激励修订都有推进，但“已全面生效并完成适配性评估”仍未完全成立，按版本一应判黄。"),
            "3.3": ("🟡", "已有正式方案文本，但离会签、审批和授予到位仍有距离，当前只能视作阶段性推进。"),
            "5.1": ("🟡", "系统问题已经暴露并需要持续关注，但尚未造成明确失效，按版本一属于关注级黄灯。"),
            "5.2": ("🟡", "流程线上化和预算平台存在真实推进，但主责人留痕不足会持续影响判断可靠性，需上级关注并补充说明。"),
            "6.1": ("🟡", "系统稳定性风险真实存在，但尚未形成不可逆后果，当前属于需要持续关注的黄灯。"),
            "6.2": ("🟡", "调薪拍板与执行风险已对 4 月节奏形成压力，但尚未到明确失控阶段。"),
            "4.1": ("🟡", "个人BP闭环管理已进入试点运行，但 3 月末模型测试、问题收口和校准闭环尚未全部完成，按版本一应判黄。"),
            "4.2": ("🟡", "调薪和制度修订已推进到终稿与评议，但正式发布实施和执行闭环尚未全部完成，按版本一应判黄。"),
            "4.3": ("🟡", "长期激励举措已形成请示稿，但会签、审批和执行规则尚未全部完成，本月仅完成部分关键节点。"),
        }
    else:
        title_suffix = "对比版-版本二"
        scheme_note = (
            "> 灯规则版本：`版本二（黄灯必须整改，但绿灯和黄灯标准均放宽）`\n"
            "> 解释口径：绿灯可容忍部分节点未完成或 1-2 周滞后；黄灯只用于已对最终达成构成实质威胁的事项。"
        )
        mapping = {
            "summary": ("🟡", "3 月多数条线基于当前进展仍大概率可以按年内节奏达成，但战略绩效主线在 3 月末仍存在系统稳定性和校准闭环压力，所以整体暂不转绿。"),
            "next": ("🟡", "4 月若系统问题继续拖延或调薪拍板执行反复，当前压力会进一步放大，因此下月整体仍需保持黄灯关注。"),
            "2.1": ("🟡", "虽然个人BP机制已进入运行，但 3 月 31 日节点上的模型开发测试和首批系数校准仍未形成足够闭环，已对阶段性达成构成实质压力。"),
            "2.2": ("🟢", "调薪终稿请示、广泛征询、V3.0 确认和业务激励修订已经连续发生，虽仍待正式执行，但基于当前进展大概率可按计划达成后续标准。"),
            "2.3": ("🟢", "德镁专项股权激励方案已形成正式请示稿，而关键签批节点在 5 月前，按当前节奏看仍大概率可以按时推进。"),
            "2.4": ("🟢", "流程线上化和预算平台已完成需求评审与方案拆解，关键时间节点主要在 6 月及以后，当前虽留痕偏辅证，但整体进展仍属正常。"),
            "3.1": ("🟡", "战略绩效结果条线仍压在 3 月末开发测试与校准闭环节点上，若不继续干预，后续达成会承压，因此保留黄灯。"),
            "3.2": ("🟢", "从终稿请示到业务激励修订的关键动作已经落地，当前偏差尚未实质影响年度目标达成信心。"),
            "3.3": ("🟢", "长期激励方案虽未闭环，但当前处于合理的前置推进阶段，尚未构成实质性失败风险。"),
            "5.1": ("🟡", "系统问题已在运行中暴露，若不处理将持续威胁后续稳定运行，因此按版本二仍需进入黄灯整改。"),
            "5.2": ("🟡", "本人留痕不足本身不会直接证明目标失败，但它已对后续判断和复盘可靠性构成实质威胁，仍需以黄灯处理。"),
            "6.1": ("🟡", "系统稳定性风险若不继续干预，将直接影响 4 月规模化运行，因此仍属黄灯。"),
            "6.2": ("🟡", "调薪拍板未落地已对 4 月执行节奏形成实质性威胁，在版本二下仍应保持黄灯整改。"),
            "4.1": ("🟡", "个人BP闭环举措虽已启动并运行，但 3 月末关键测试与校准闭环仍有实质压力，因此仍为黄灯。"),
            "4.2": ("🟢", "调薪与制度修订举措已完成终稿、征询与评议等核心动作，虽待执行，但当前大概率可按计划推进到位。"),
            "4.3": ("🟢", "长期激励举措已形成正式方案请示，而关键签批窗口在后续月份，当前进展仍属正常区间。"),
        }

    text = base_text
    first_line = text.splitlines()[0]
    text = text.replace(first_line, f"{first_line}（{title_suffix}）", 1)
    text = text.replace(
        "> 证据说明：本稿按最新版 skill 重跑。当前接口暂未返回 `reportId`，因此本月先以“汇报标题 + 作者 + taskId + 证据等级”引用原始汇报，不再引用本地 json 快照。",
        "> 证据说明：本稿按最新版 skill 重跑。当前接口暂未返回 `reportId`，因此本月先以“汇报标题 + 作者 + taskId + 证据等级”引用原始汇报，不再引用本地 json 快照。\n"
        f"{scheme_note}",
        1,
    )

    summary_block = (
        "- **本月总体判断：**\n"
        f"  {mapping['summary'][0]} 3 月最大的变化不是“又有证据了”，而是个人BP机制已经真正开始跑起来了：部署、试点、问题暴露、自动审查、关键岗位系数评议都在本月出现；薪酬与业务激励主线继续保持强推进；长期激励首次出现较完整方案请示；流程线上化和预算平台仍偏辅证。\n"
        + "\n".join("  " + line for line in judgment_block(mapping["summary"][0], mapping["summary"][1], scheme).splitlines())
        + "\n\n"
    )
    text = replace_range(text, "- **本月总体判断：**", "\n- **本月最关键的进展：**", summary_block)

    next_block = (
        "- **对下月的总体判断：**\n"
        f"  {mapping['next'][0]} 如果 4 月能把系统问题进一步收口、把调薪和系数评议结果落实、并补强流程线上化条线本人留痕，这条主线会从“试点推进”走向“稳态执行”。\n"
        + "\n".join("  " + line for line in judgment_block(mapping["next"][0], mapping["next"][1], scheme).splitlines())
        + "\n\n"
    )
    text = replace_range(text, "- **对下月的总体判断：**", "\n## 2. BP目标承接与对齐情况", next_block)

    sec_map = {
        "### 2.1 集团战略绩效管理体系已高效运行，质量与效果评估达标": ("### 2.2 薪酬体系与业务激励方案已全面生效并完成业务适配性评估", "2.1"),
        "### 2.2 薪酬体系与业务激励方案已全面生效并完成业务适配性评估": ("### 2.3 长期激励与福利体系已完成升级，薪酬竞争力处于对标合理区间", "2.2"),
        "### 2.3 长期激励与福利体系已完成升级，薪酬竞争力处于对标合理区间": ("### 2.4 核心人事与预算流程已实现线上化运行", "2.3"),
        "### 2.4 核心人事与预算流程已实现线上化运行": ("## 3. 核心结果与经营表现", "2.4"),
        "### 3.1 个人BP闭环管理进入试点运行": ("### 3.2 调薪终稿与业务激励修订推进", "3.1"),
        "### 3.2 调薪终稿与业务激励修订推进": ("### 3.3 长期激励方案形成正式文本", "3.2"),
        "### 3.3 长期激励方案形成正式文本": ("## 4. 关键举措推进情况", "3.3"),
        "### 5.1 系统运行问题暴露": ("### 5.2 流程线上化与预算平台仍以辅证为主", "5.1"),
        "### 5.2 流程线上化与预算平台仍以辅证为主": ("## 6. 风险预警与资源需求", "5.2"),
        "### 6.1 系统稳定性风险": ("### 6.2 调薪拍板与执行风险", "6.1"),
        "### 6.2 调薪拍板与执行风险": ("## 7. 下月重点安排", "6.2"),
    }
    for heading, (next_heading, key) in sec_map.items():
        text = replace_section_block(text, heading, next_heading, judgment_block(mapping[key][0], mapping[key][1], scheme))

    ch4_map = {
        "### 4.1 个人BP闭环管理举措推进": ("### 4.2 调薪与制度修订举措推进", "4.1"),
        "### 4.2 调薪与制度修订举措推进": ("### 4.3 长期激励方案举措推进", "4.2"),
        "### 4.3 长期激励方案举措推进": ("## 5. 问题、偏差与原因分析", "4.3"),
    }
    for heading, (next_heading, key) in ch4_map.items():
        text = insert_ch4_block(text, heading, next_heading, judgment_block(mapping[key][0], mapping[key][1], scheme))

    return text


def main() -> None:
    run_dir = Path("/Users/hou/Documents/UGit/BP- writer/report-runs/2026年度计划BP_陈舒婷/2026-03")
    base_path = run_dir / "05_report.md"
    base_text = base_path.read_text(encoding="utf-8")

    out_v1 = run_dir / "05_report_scheme_v1.md"
    out_v2 = run_dir / "05_report_scheme_v2.md"
    out_v1.write_text(apply_scheme(base_text, "v1"), encoding="utf-8")
    out_v2.write_text(apply_scheme(base_text, "v2"), encoding="utf-8")
    print(out_v1)
    print(out_v2)


if __name__ == "__main__":
    main()
