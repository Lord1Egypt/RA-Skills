#!/usr/bin/env python3
"""Render 付忠明 2026-01 report under scheme v2."""

from __future__ import annotations

import re
from pathlib import Path


GREEN = "#2e7d32"
YELLOW = "#b26a00"
RED = "#d32f2f"
BLACK = "#111111"
COLOR = {"🟢": GREEN, "🟡": YELLOW, "🔴": RED, "⚫": BLACK}


def judgment_block(light: str, reason: str) -> str:
    color = COLOR[light]
    lines = [
        f"- <span style=\"color:{color}; font-weight:700;\">灯色判断：{light}</span>",
        f"  <span style=\"color:{color}; font-weight:700;\">判断理由：{reason}</span>",
        f"  <span style=\"color:{color}; font-weight:700;\">人工判断：待确认（请填写：同意 / 不同意）</span>",
        f"  <span style=\"color:{color}; font-weight:700;\">若同意：请明确填写“同意”。</span>",
        f"  <span style=\"color:{color}; font-weight:700;\">若不同意：请填写理由类别（BP不清晰 / 举证材料不足 / AI判断错误 / 其他）及具体说明。</span>",
    ]
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
    if light in {"🟡", "🔴", "⚫"}:
        lines.extend(
            [
                f"  <span style=\"color:{color}; font-weight:700;\">整改方案：待补充</span>",
                f"  <span style=\"color:{color}; font-weight:700;\">承诺完成时间：待补充</span>",
                f"  <span style=\"color:{color}; font-weight:700;\">下周期具体举措：待补充</span>",
            ]
        )
        if light == "⚫":
            lines.append(
                f"  <span style=\"color:{color}; font-weight:700;\">持续提醒至下周期：是</span>"
            )
    return "\n".join(lines)


def replace_range(text: str, start_marker: str, end_marker: str, replacement: str) -> str:
    start = text.index(start_marker)
    end = text.index(end_marker, start)
    return text[:start] + replacement + text[end:]


def replace_first_judgment_block(section_text: str, new_block: str) -> str:
    pattern = re.compile(
        r"- <span style=.*?>灯色判断：[🟢🟡🔴⚫]</span>\n(?:  <span style=.*?>.*?</span>\n?)+",
        re.S,
    )
    return pattern.sub(new_block + "\n", section_text, count=1)


def replace_section_block(text: str, heading: str, next_heading: str, new_block: str) -> str:
    start = text.index(heading)
    end = text.index(next_heading, start)
    section = text[start:end]
    section = replace_first_judgment_block(section, new_block)
    return text[:start] + section + text[end:]


def replace_result_judgment_line(
    text: str, heading: str, next_heading: str, new_line: str
) -> str:
    start = text.index(heading)
    end = text.index(next_heading, start)
    section = text[start:end]
    pattern = re.compile(
        r"- 结果判断：\n  - <span style=.*?>.*?</span>",
        re.S,
    )
    section = pattern.sub(f"- 结果判断：\n  - {new_line}", section, count=1)
    return text[:start] + section + text[end:]


def replace_nth_judgment_between(
    text: str, start_marker: str, end_marker: str, new_block: str, occurrence: int
) -> str:
    start = text.index(start_marker)
    end = text.index(end_marker, start)
    section = text[start:end]
    pattern = re.compile(
        r"- <span style=.*?>灯色判断：[🟢🟡🔴⚫]</span>\n(?:  <span style=.*?>.*?</span>\n?)+",
        re.S,
    )
    matches = list(pattern.finditer(section))
    if occurrence >= len(matches):
        raise ValueError(f"judgment block occurrence {occurrence} not found between markers")
    match = matches[occurrence]
    section = section[: match.start()] + new_block + "\n" + section[match.end() :]
    return text[:start] + section + text[end:]


def apply_scheme_v2(base_text: str) -> str:
    mapping = {
        "summary": (
            "🟡",
            "1 月已在调薪、组织规划和市场准入部风险处置三条线上形成真实推进，但大量关键成果仍缺少本人主证据或有效留痕，整体判断仍需保持黄灯关注。",
        ),
        "next": (
            "🟡",
            "2 月如果不能同步补强关键人才、核心团队和数字化条线的留痕，当前“少数事项推进、整体可判断性偏弱”的状态会继续拖累整条 BP 的管理判断。",
        ),
        "2.1": (
            "🟡",
            "调薪与制度设计已明确启动，但 1 月内已经暴露规则执行不一致问题，且 3 月 31 日前审核放行仍存在实质压力，因此保留黄灯。",
        ),
        "2.2": (
            "⚫",
            "1 月没有关键岗位供给、保留机制或专项攻坚的有效汇报，当前无法判断这一关键成果是否真实推进，应判黑灯。",
        ),
        "2.3.1": (
            "🟢",
            "多个组织的组织结构与编制规划已经进入请示审批，市场准入部问题也已启动专项处置；虽然还未稳定运行，但按年度节奏看当前仍大概率可以继续推进。",
        ),
        "2.3.2": (
            "⚫",
            "1 月没有流程线上化率、数据准确率或标签体系建设的有效证据，当前无法判断该关键成果是否推进，应判黑灯。",
        ),
        "2.4": (
            "⚫",
            "1 月没有总监级岗位攻坚、团队融入或继任计划的有效汇报，当前无法判断核心管理团队建设是否真实推进，应判黑灯。",
        ),
        "2.5": (
            "🟢",
            "市场准入部相关风险事项已经被及时响应并形成处理建议和后续动作安排，虽然机制化尚未完成，但按当前节奏看年度目标仍大概率可达。",
        ),
        "3.1": (
            "🟡",
            "调薪与制度框架已经启动，但规则一致性问题在启动阶段就已出现，若不继续纠偏会直接影响后续落地，因此结果层面仍为黄灯。",
        ),
        "3.2": (
            "🟢",
            "组织结构与编制调整已形成多份正式请示并进入审批，当前虽还在启动期，但偏差尚未实质影响年度达成信心，可判绿灯。",
        ),
        "3.3": (
            "🟢",
            "风险事项已被及时识别并启动处置，付忠明本人也已给出责任判断和补位方向，当前属于正常推进中的个案响应。",
        ),
        "4.1.1": (
            "🟡",
            "调薪审核放行工作已明确启动并连续推进，但 1 月内已出现规则执行不一致问题，当前对后续放行节奏形成实质压力，故保留黄灯。",
        ),
        "4.1.2": (
            "⚫",
            "当前没有检索到绩效系统数据质量攻坚的有效汇报，无法判断该举措在 1 月是否真实推进，应判黑灯。",
        ),
        "4.1.3": (
            "⚫",
            "当前没有检索到年度激励方案评审会的有效汇报，无法判断该举措在 1 月是否真实推进，应判黑灯。",
        ),
        "4.2.1": (
            "⚫",
            "当前没有检索到关键岗位风险预警机制的有效汇报，无法判断该举措在 1 月是否真实推进，应判黑灯。",
        ),
        "4.2.2": (
            "⚫",
            "当前没有检索到稀缺关键岗位专项攻坚的有效汇报，无法判断该举措在 1 月是否真实推进，应判黑灯。",
        ),
        "4.2.3": (
            "⚫",
            "当前没有检索到人才质量回溯机制的有效汇报，无法判断该举措在 1 月是否真实推进，应判黑灯。",
        ),
        "4.3.1": (
            "🟢",
            "多个组织架构与编制方案已经形成正式请示并进入审批，当前虽未闭环，但整体仍处于可按计划推进的正常区间。",
        ),
        "4.3.2": (
            "🟢",
            "市场准入部问题的专项诊断、处理建议和后续补位动作已经形成，当前个案处置节奏正常，尚未出现失控信号。",
        ),
        "4.3.3": (
            "⚫",
            "当前没有检索到组织健康度诊断报告解读会的有效汇报，无法判断该举措在 1 月是否真实推进，应判黑灯。",
        ),
        "4.3.4": (
            "⚫",
            "当前没有检索到 HR 与业务系统数据打通的有效汇报，无法判断该举措在 1 月是否真实推进，应判黑灯。",
        ),
        "4.3.5": (
            "⚫",
            "当前没有检索到线上流程体验优化机制的有效汇报，无法判断该举措在 1 月是否真实推进，应判黑灯。",
        ),
        "4.3.6": (
            "⚫",
            "当前没有检索到员工数据标签体系建设的有效汇报，无法判断该举措在 1 月是否真实推进，应判黑灯。",
        ),
        "4.4.1": (
            "⚫",
            "当前没有检索到总监级岗位招聘攻坚的有效汇报，无法判断该举措在 1 月是否真实推进，应判黑灯。",
        ),
        "4.4.2": (
            "⚫",
            "当前没有检索到核心团队融入与融合计划的有效汇报，无法判断该举措在 1 月是否真实推进，应判黑灯。",
        ),
        "4.4.3": (
            "⚫",
            "当前没有检索到核心团队定期复盘与反馈机制的有效汇报，无法判断该举措在 1 月是否真实推进，应判黑灯。",
        ),
        "4.4.4": (
            "⚫",
            "当前没有检索到团队专业能力提升与继任计划的有效汇报，无法判断该举措在 1 月是否真实推进，应判黑灯。",
        ),
        "4.4.5": (
            "⚫",
            "当前没有检索到团队作战效能评估的有效汇报，无法判断该举措在 1 月是否真实推进，应判黑灯。",
        ),
        "4.5.1": (
            "⚫",
            "当前没有检索到重大劳资纠纷与合规隐患汇报触发条件建设的有效汇报，无法判断该举措在 1 月是否真实推进，应判黑灯。",
        ),
        "4.5.2": (
            "⚫",
            "当前没有检索到牵头跨部门应急协同机制的有效汇报，无法判断该举措在 1 月是否真实推进，应判黑灯。",
        ),
        "4.5.3": (
            "⚫",
            "当前没有检索到制度根因修订与风控手册修订版的有效汇报，无法判断该举措在 1 月是否真实推进，应判黑灯。",
        ),
        "5.1": (
            "🟡",
            "调薪规则执行不一致已经被清晰识别，若不及时拍板纠偏会直接影响后续制度落地和公平性感知，因此按版本二仍需黄灯整改。",
        ),
        "5.2": (
            "⚫",
            "多数关键成果已经出现无法判断进展的情况，不是简单的证据偏弱，而是当月缺少有效汇报，应判黑灯。",
        ),
        "5.3": (
            "🟡",
            "个案处置动作真实存在，但如果后续不能沉淀为机制，年度目标会持续承压，因此仍需黄灯整改。",
        ),
        "6.1": (
            "🟡",
            "调薪制度公信力风险已经形成实质威胁，若不继续处理会直接影响后续执行，因此保持黄灯。",
        ),
        "6.2": (
            "⚫",
            "关键人才、核心团队和数字化条线已出现无法判断进展的情况，这一风险本身来源于黑灯状态，因此仍按黑灯提示处理。",
        ),
    }

    text = base_text
    first_line = text.splitlines()[0]
    text = text.replace(first_line, f"{first_line}（版本二对比版）", 1)
    text = text.replace(
        "> 证据说明：当前接口暂未返回 `reportId`，所以本稿先以“R编号 + 汇报标题 + 作者/证据等级”引用原始汇报",
        "> 证据说明：当前接口暂未返回 `reportId`，所以本稿先以“R编号 + 汇报标题 + 作者/证据等级”引用原始汇报\n"
        "> 灯规则版本：`版本二（黄灯必须整改，但绿灯和黄灯标准均放宽）`\n"
        "> 解释口径：绿灯允许本月存在部分节点未完成或 1-2 周滞后，只要不实质影响最终按时达成信心；黄灯只用于已对最终达成构成实质威胁的事项。",
        1,
    )

    summary_block = (
        "- **本月总体判断：**\n"
        "  🟡 1 月已经能看到几条年度主线的实质启动：调薪与制度框架启动、多个组织架构与编制方案进入审批、市场准入部风险事项开始进入处置闭环。按版本二的放宽标准，组织调整和风险响应两条线仍可视为大概率能按年内节奏推进；但调薪规则一致性问题和多条黑灯项，使整体仍需保持黄灯关注。\n"
        + "\n".join("  " + line for line in judgment_block(*mapping["summary"]).splitlines())
        + "\n\n"
    )
    text = replace_range(text, "- **本月总体判断：**", "\n- **本月最关键的进展：**", summary_block)

    next_block = (
        "- **对下月的总体判断：**\n"
        "  🟡 如果 2 月能尽快拍板调薪规则、推进组织调整审批结果落地，并补齐关键人才、核心团队和数字化条线的有效留痕，这条 BP 才会从“事项启动”过渡到“机制运行”。\n"
        + "\n".join("  " + line for line in judgment_block(*mapping["next"]).splitlines())
        + "\n\n"
    )
    text = replace_range(text, "- **对下月的总体判断：**", "\n## 2. BP目标承接与对齐情况", next_block)

    section_map = {
        "### 2.1 \"战略-绩效-分配\"一体化闭环处于有效运行状态，评价与激励实现统一": ("### 2.2 集团关键人才供应链质量与风险处于可控状态", "2.1"),
        "### 2.2 集团关键人才供应链质量与风险处于可控状态": ("### 2.3 组织变革与关键机制处于稳定运行状态，制度已转化为管理行为", "2.2"),
        "### 2.4 人力资源核心管理团队处于高质量、高战力状态，组织能力建设内部根基稳固": ("### 2.5 集团重大人员风险与合规事件处于可控状态", "2.4"),
        "### 2.5 集团重大人员风险与合规事件处于可控状态": ("## 3. 核心结果与经营表现", "2.5"),
        "### 3.1 2026年1月调薪与制度框架启动": ("### 3.2 组织结构与编制调整进入请示审批", "3.1"),
        "### 3.2 组织结构与编制调整进入请示审批": ("### 3.3 市场准入部风险事项开始进入闭环处置", "3.2"),
        "### 3.3 市场准入部风险事项开始进入闭环处置": ("## 4. 关键举措推进情况", "3.3"),
        "### 5.1 调薪规则执行一致性不足": ("### 5.2 多数关键成果缺少本人主证据", "5.1"),
        "### 5.2 多数关键成果缺少本人主证据": ("### 5.3 组织问题处置仍偏个案化", "5.2"),
        "### 5.3 组织问题处置仍偏个案化": ("## 6. 风险预警与资源需求", "5.3"),
        "### 6.1 调薪制度公信力风险": ("### 6.2 组织与人才条线留痕不足风险", "6.1"),
        "### 6.2 组织与人才条线留痕不足风险": ("## 7. 下月重点安排", "6.2"),
    }
    for heading, (next_heading, key) in section_map.items():
        text = replace_section_block(text, heading, next_heading, judgment_block(*mapping[key]))

    result_replacements = {
        '<span style="color:#b26a00; font-weight:700;">🟡 启动明确，但成果未成立。</span>':
            '<span style="color:#b26a00; font-weight:700;">🟡 启动明确，但规则一致性问题已对后续落地形成实质压力。</span>',
        '<span style="color:#b26a00; font-weight:700;">🟡 组织变革已启动，但机制稳定性尚未形成。</span>':
            '<span style="color:#2e7d32; font-weight:700;">🟢 已形成多项正式请示，当前整体仍处于可按计划推进的正常区间。</span>',
        '<span style="color:#b26a00; font-weight:700;">🟡 响应及时，但机制未成型。</span>':
            '<span style="color:#2e7d32; font-weight:700;">🟢 响应及时，个案处置节奏正常，当前尚未出现明显失控信号。</span>',
    }
    for old, new in result_replacements.items():
        text = text.replace(old, new, 1)

    text = replace_nth_judgment_between(
        text,
        "### 2.3 组织变革与关键机制处于稳定运行状态，制度已转化为管理行为",
        "### 2.4 人力资源核心管理团队处于高质量、高战力状态，组织能力建设内部根基稳固",
        judgment_block(*mapping["2.3.1"]),
        0,
    )
    text = replace_nth_judgment_between(
        text,
        "### 2.3 组织变革与关键机制处于稳定运行状态，制度已转化为管理行为",
        "### 2.4 人力资源核心管理团队处于高质量、高战力状态，组织能力建设内部根基稳固",
        judgment_block(*mapping["2.3.2"]),
        1,
    )

    action_map = {
        "#### 4.1.1 负责集团总部2026年调薪方案的审核放行，对于存在疑问的核心组织参与会议沟通和研讨，确认解决方案": ("#### 4.1.2 推动绩效系统数据质量攻坚，输出《系统数据校验及治理规范》", "4.1.1"),
        "#### 4.1.2 推动绩效系统数据质量攻坚，输出《系统数据校验及治理规范》": ("#### 4.1.3 主持年度激励方案评审会", "4.1.2"),
        "#### 4.1.3 主持年度激励方案评审会": ("### 4.2 集团关键人才供应链质量与风险处于可控状态", "4.1.3"),
        "#### 4.2.1 亲自主导关键岗位风险预警机制": ("#### 4.2.2 推动稀缺关键岗位专项攻坚", "4.2.1"),
        "#### 4.2.2 推动稀缺关键岗位专项攻坚": ("#### 4.2.3 建立人才质量回溯机制", "4.2.2"),
        "#### 4.2.3 建立人才质量回溯机制": ("### 4.3 组织变革与关键机制处于稳定运行状态，制度已转化为管理行为", "4.2.3"),
        "#### 4.3.1 负责集团总部编制及组织架构方案的最终审批": ("#### 4.3.2 针对重大个别组织问题开展专项诊断并放行最终方案", "4.3.1"),
        "#### 4.3.2 针对重大个别组织问题开展专项诊断并放行最终方案": ("#### 4.3.3 主持组织健康度诊断报告解读会并跟进落地", "4.3.2"),
        "#### 4.3.3 主持组织健康度诊断报告解读会并跟进落地": ("#### 4.3.4 推动 HR 与业务系统数据打通", "4.3.3"),
        "#### 4.3.4 推动 HR 与业务系统数据打通": ("#### 4.3.5 建立线上流程体验优化机制", "4.3.4"),
        "#### 4.3.5 建立线上流程体验优化机制": ("#### 4.3.6 主导构建员工数据标签体系", "4.3.5"),
        "#### 4.3.6 主导构建员工数据标签体系": ("### 4.4 人力资源核心管理团队处于高质量、高战力状态，组织能力建设内部根基稳固", "4.3.6"),
        "#### 4.4.1 亲自主导总监级岗位招聘攻坚": ("#### 4.4.2 实施核心团队融入与融合计划", "4.4.1"),
        "#### 4.4.2 实施核心团队融入与融合计划": ("#### 4.4.3 建立核心团队定期复盘与反馈机制", "4.4.2"),
        "#### 4.4.3 建立核心团队定期复盘与反馈机制": ("#### 4.4.4 推动人力资源团队专业能力提升与继任计划", "4.4.3"),
        "#### 4.4.4 推动人力资源团队专业能力提升与继任计划": ("#### 4.4.5 评估团队作战效能", "4.4.4"),
        "#### 4.4.5 评估团队作战效能": ("### 4.5 集团重大人员风险与合规事件处于可控状态", "4.4.5"),
        "#### 4.5.1 升级重大劳资纠纷与合规隐患的汇报触发条件与时限": ("#### 4.5.2 牵头跨部门应急协同", "4.5.1"),
        "#### 4.5.2 牵头跨部门应急协同": ("#### 4.5.3 推动制度根因修订并发布风控手册修订版", "4.5.2"),
        "#### 4.5.3 推动制度根因修订并发布风控手册修订版": ("## 5. 问题、偏差与原因分析", "4.5.3"),
    }
    for heading, (next_heading, key) in action_map.items():
        text = replace_section_block(text, heading, next_heading, judgment_block(*mapping[key]))

    return text


def main() -> None:
    run_dir = Path("/Users/hou/Documents/UGit/BP- writer/report-runs/2026年度计划BP_付忠明/2026-01")
    base_path = run_dir / "05_ai_baseline_report.md"
    out_path = run_dir / "05_ai_baseline_report_scheme_v2.md"
    out_path.write_text(apply_scheme_v2(base_path.read_text(encoding="utf-8")), encoding="utf-8")
    print(out_path)


if __name__ == "__main__":
    main()
