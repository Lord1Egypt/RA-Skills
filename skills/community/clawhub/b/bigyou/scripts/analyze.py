#!/usr/bin/env python3
"""
bigyou · 比优 — 选项比较与决策工具 v2
用法: python3 analyze.py <用户问题>
"""
import sys
import re
from typing import List, Dict, Optional


# ─────────────────────────────────────────────
# 维度配置：不同场景的底线/加分维度
# ─────────────────────────────────────────────

SCENE_CONFIGS = {
    "职业选择": {
        "场景关键词": ["工作", "offer", "跳槽", "职业", "公司", "岗位", "辞职", "创业", "职场"],
        "底线": [
            ("业务方向匹配度", "不满足直接淘汰，方向不匹配是长期消耗"),
        ],
        "加分": [
            ("薪资/经济回报", 4, "比当前提升多少，关注5年总回报而非月薪"),
            ("成长空间", 4, "3年后回头看，这段经历值不值"),
            ("团队/直属领导", 3, "直接影响工作体验和质量"),
            ("通勤/工作地点", 3, "每天2小时 vs 15分钟，差距很大"),
            ("工作生活平衡", 3, "加班频率、假期制度"),
        ],
    },
    "工具软件": {
        "场景关键词": ["软件", "工具", "平台", "系统", "app", "服务", "选型"],
        "底线": [
            ("满足核心需求", 5, "不满足核心需求直接淘汰"),
        ],
        "加分": [
            ("成本（费用/学习成本）", 4, "总持有成本"),
            ("易用性/体验", 3, "上手难度、界面体验"),
            ("扩展性/生态", 3, "能否满足未来需求"),
            ("稳定性/可靠性", 4, "故障率、数据安全"),
        ],
    },
    "房产": {
        "场景关键词": ["房", "买房", "租", "房子", "住宅"],
        "底线": [
            ("预算/价格", 5, "超出预算直接淘汰"),
            ("地段/交通", 4, "地铁、上下班时间"),
        ],
        "加分": [
            ("采光/朝向/户型", 3, "居住舒适度"),
            ("周边配套", 3, "学校/医院/商业"),
            ("小区品质/物业", 2, "长期居住体验"),
        ],
    },
    "默认": {
        "场景关键词": [],
        "底线": [
            ("满足核心需求", 5, "不满足核心需求直接淘汰"),
        ],
        "加分": [
            ("长期价值", 4, "3-5年维度的价值"),
            ("短期收益", 3, "立即获得的好处"),
            ("风险/隐患", 4, "潜在风险有多大"),
            ("执行难度", 2, "落地需要多少资源"),
        ],
    },
}


def detect_scene(problem: str) -> str:
    """识别问题场景"""
    p = problem.lower()
    for scene, cfg in SCENE_CONFIGS.items():
        if any(k in p for k in cfg["场景关键词"]):
            return scene
    return "默认"


def extract_options_v2(problem: str) -> List[str]:
    """从问题文本中提取选项名（精准版）"""
    # 预处理
    text = problem.strip().rstrip('?？.。!！')
    
    # 找 A... B... 模式
    # 目标："A薪资高但业务方向我不喜欢，B方向喜欢但薪资低20%"
    # 要提取出 ["A薪资高但业务方向我不喜欢", "B方向喜欢但薪资低20%"]
    
    # 找到所有 "A开头到逗号" 和 "B开头到逗号或结尾" 的片段
    options_raw = []
    
    # 找到所有A和B出现的位置
    a_positions = [(m.start(), m.group()) for m in re.finditer(r'\bA\b', text)]
    b_positions = [(m.start(), m.group()) for m in re.finditer(r'\bB\b', text)]
    
    # 提取A选项：从 "A" 位置到下一个逗号之间
    for pos, _ in a_positions:
        # 从A的位置往后找内容
        rest = text[pos+1:]  # 跳过A
        # 找第一个逗号作为结束
        comma_match = re.search(r'[,，]', rest)
        if comma_match:
            segment = rest[:comma_match.start()].strip()
        else:
            # 如果A后面没有逗号（如在句尾），取到问号或结尾
            end_match = re.search(r'[?？]', rest)
            segment = rest[:end_match.start() if end_match else len(rest)].strip()
        if len(segment) >= 2:
            options_raw.append(("A", segment))
    
    # 提取B选项
    for pos, _ in b_positions:
        rest = text[pos+1:]  # 跳过B
        comma_match = re.search(r'[,，]', rest)
        if comma_match:
            segment = rest[:comma_match.start()].strip()
        else:
            end_match = re.search(r'[?？]', rest)
            segment = rest[:end_match.start() if end_match else len(rest)].strip()
        if len(segment) >= 2:
            options_raw.append(("B", segment))
    
    # 去重并组合（去掉原始前缀如"薪资高但业务方向"）
    result = []
    seen = set()
    for label, segment in options_raw:
        # 清理：去掉开头的标点和空白
        clean = segment.strip().lstrip('，,、:：.。')
        if clean and clean not in seen and len(clean) > 2:
            seen.add(clean)
            result.append(clean)
    
    # 如果提取失败，尝试备选方案：直接按逗号分割
    if not result:
        parts = re.split(r'[,，]', text)
        for part in parts:
            p = part.strip()
            # 跳过问题句本身
            if any(k in p for k in ['怎么选', '哪个好', '帮我', '请问', '选哪个', '哪个更好']):
                continue
            if len(p) > 3:
                result.append(p[:40])
    
    return result[:4]  # 最多4个选项


def extract_option_features(option: str, dims: List[Dict]) -> Dict[str, int]:
    """根据选项文本特征推断各维度得分"""
    o = option.lower()
    scores = {}
    
    for dim in dims:
        dname = dim["维度"]
        dtype = dim.get("类型", "加分")
        weight = dim.get("权重", 3)
        
        if dtype == "底线":
            # 底线维度：匹配关键词给5分，否则给1分
            if any(k in o for k in ["方向喜欢", "匹配", "感兴趣", "喜欢", "符合"]):
                scores[dname] = 5
            elif any(k in o for k in ["方向不喜欢", "不匹配", "不喜欢", "排斥", "抵触"]):
                scores[dname] = 1
            elif any(k in o for k in ["不确定", "未知", "模糊"]):
                scores[dname] = 2
            else:
                scores[dname] = 3  # 信息不足，给中性分
        else:
            # 加分维度：基于关键词打分
            score = 3  # 默认中等
            
            # 薪资相关
            if "薪" in dname or "工资" in dname or "收入" in dname or "回报" in dname:
                if any(k in o for k in ["薪资高", "薪资高", "工资高", "收入高", "薪资高", "高薪", "高薪"]):
                    score = 5
                elif any(k in o for k in ["薪资低", "工资低", "收入低", "薪资低20%", "低20%"]):
                    score = 2
                elif any(k in o for k in ["薪资一般", "工资一般", "持平"]):
                    score = 3
            
            # 方向/匹配相关
            elif "方向" in dname or "匹配" in dname or "业务" in dname:
                if any(k in o for k in ["方向喜欢", "匹配", "感兴趣", "喜欢", "方向对"]):
                    score = 5
                elif any(k in o for k in ["方向不喜欢", "不喜欢", "方向不喜欢"]):
                    score = 1
            
            # 成长相关
            elif "成长" in dname or "发展" in dname or "空间" in dname:
                if any(k in o for k in ["成长", "发展", "空间", "潜力", "前景"]):
                    score = 4
                elif any(k in o for k in ["瓶颈", "天花板"]):
                    score = 2
            
            # 通勤相关
            elif "通勤" in dname or "距离" in dname or "地点" in dname:
                if any(k in o for k in ["近", "15分钟", "30分钟"]):
                    score = 5
                elif any(k in o for k in ["远", "2小时", "1小时", "通勤长"]):
                    score = 1
            
            # 团队相关
            elif "团队" in dname or "领导" in dname:
                if any(k in o for k in ["团队好", "领导好", "大厂", "团队强"]):
                    score = 5
                elif any(k in o for k in ["团队差", "领导差"]):
                    score = 1
            
            # 工作生活平衡
            elif "平衡" in dname or "加班" in dname or "生活" in dname:
                if any(k in o for k in ["加班", "996", "卷", "强度大"]):
                    score = 1
                elif any(k in o for k in ["965", "轻松", "wlb", "work life"]):
                    score = 5
            
            scores[dname] = score
        
        scores.setdefault(dname, 3)
    
    return scores


def compute_composite(scores: Dict[str, int], dims: List[Dict]) -> float:
    """计算加权综合分"""
    total_weight = sum(d.get("权重", 3) for d in dims)
    weighted = sum(scores.get(d["维度"], 3) * d.get("权重", 3) for d in dims)
    return round(weighted / total_weight, 1) if total_weight > 0 else 0


def analyze(problem: str) -> str:
    """完整分析，输出 Markdown 报告"""
    
    # 1. 识别场景和维度
    scene = detect_scene(problem)
    cfg = SCENE_CONFIGS[scene]
    
    dims = []
    for name, desc in cfg["底线"]:
        dims.append({"维度": name, "类型": "底线", "权重": 5, "说明": desc})
    for name, weight, desc in cfg["加分"]:
        dims.append({"维度": name, "类型": "加分", "权重": weight, "说明": desc})
    
    # 2. 提取选项
    options = extract_options_v2(problem)
    
    # 3. 对每个选项打分
    scored = []
    for opt in options:
        scores = extract_option_features(opt, dims)
        composite = compute_composite(scores, dims)
        
        # 找最大优势和最大风险（得分最高和最低的维度）
        if scores:
            max_dim = max(scores, key=scores.get)
            min_dim = min(scores, key=scores.get)
            
            # 只有当最高/最低分有明显差异时才标注
            if scores[max_dim] >= 4 and scores[max_dim] - scores[min_dim] >= 1.5:
                advantage = f"{max_dim}突出"
                risk = f"{min_dim}是短板"
            elif scores[min_dim] <= 2:
                advantage = "综合均衡"
                risk = f"{min_dim}明显不足"
            else:
                advantage = "综合表现均衡"
                risk = "各维度无明显短板"
        else:
            advantage = "—"
            risk = "—"
        
        # 底线维度是否通过
        baseline_pass = all(
            scores.get(d["维度"], 3) >= 3 for d in dims
            if d.get("类型") == "底线"
        )
        
        scored.append({
            "选项": opt,
            "综合得分": composite,
            "维度得分": scores,
            "最大优势": advantage,
            "最大风险": risk,
            "底线通过": baseline_pass,
        })
    
    # 按底线通过 + 综合得分排序
    scored.sort(key=lambda x: (x["底线通过"], x["综合得分"]), reverse=True)
    
    # 4. 生成分析文字
    scene_tips = {
        "职业选择": "薪资差异超过20%时，长期复利效应显著——建议量化5年总回报而非仅看月薪差。",
        "工具软件": "选工具的核心是「不满足核心需求」直接淘汰，其余按性价比排序。",
        "默认": "先明确底线（什么情况下绝对不考虑），再在通过底线的选项中打分排序。",
    }
    
    # 5. 输出报告
    lines = []
    lines.append(f"# 比优 · 选项分析报告\n")
    lines.append(f"**决策问题**：{problem}\n")
    
    if options:
        lines.append(f"**识别到 {len(options)} 个选项**：{', '.join(options)}\n")
    else:
        lines.append(f"**未识别到具体选项**，以下按通用框架分析：\n")
    
    lines.append(f"\n---\n")
    
    # 一、问题定性
    lines.append(f"\n## 一、问题定性\n")
    lines.append(f"**场景判断**：{scene}\n")
    lines.append(f"**关键洞察**：{scene_tips.get(scene, scene_tips['默认'])}\n")
    
    # 二、目标画像
    lines.append(f"\n## 二、目标画像\n")
    lines.append(f"**🔴 底线维度**（一项不满足 → 直接淘汰）：\n")
    for dim in dims:
        if dim.get("类型") == "底线":
            lines.append(f"- **{dim['维度']}**：{dim.get('说明', '')}\n")
    
    lines.append(f"\n**🟡 加分维度**（满足越多得分越高）：\n")
    for dim in dims:
        if dim.get("类型") == "加分":
            lines.append(f"- **{dim['维度']}**（权重×{dim.get('权重', 3)}）：{dim.get('说明', '')}\n")
    
    # 三、选项打分
    if scored:
        lines.append(f"\n## 三、选项打分\n")
        
        # 表头：选项 + 各维度
        dim_names = [d["维度"] for d in dims]
        header = "| 选项 | 综合 | " + " | ".join(dim_names[:6]) + " |"
        sep = "|------|------|" + "|------" * len(dim_names[:6]) + "|"
        lines.append(header)
        lines.append(sep)
        
        for item in scored:
            row = f"| **{item['选项'][:18]}** | **{item['综合得分']}**"
            for dname in dim_names[:6]:
                score = item["维度得分"].get(dname, 3)
                icon = "🟢" if score >= 4 else "🟡" if score >= 3 else "🔴"
                row += f" | {icon}{score}"
            row += " |"
            lines.append(row)
        
        lines.append(f"\n**推荐选项**：{scored[0]['选项']}（综合得分 {scored[0]['综合得分']}/5）\n")
        lines.append(f"- ✅ 优势：{scored[0]['最大优势']}\n")
        lines.append(f"- ⚠️ 风险：{scored[0]['最大风险']}\n")
        lines.append(f"- {'✅ 底线全部通过' if scored[0]['底线通过'] else '❌ 存在底线未通过项'}\n")
        
        # 决策建议
        if len(scored) >= 2:
            top, second = scored[0], scored[1]
            diff = top["综合得分"] - second["综合得分"]
            if diff >= 0.5:
                lines.append(f"\n**决策建议**：{top['选项']} 领先第二名 {diff} 分，优势明显，推荐优先考虑。\n")
            elif diff < 0.3:
                lines.append(f"\n**决策建议**：两者得分接近（差距 {diff} 分），建议以底线维度为首要过滤条件。\n")
    
    # 四、最坏情况推演
    lines.append(f"\n## 四、最坏情况推演（底线思维）\n")
    if scored:
        for item in scored:
            o = item["选项"]
            worst_case = f"选了「{o[:20]}」后，发现实际体验与预期差距大，且已产生沉没成本"
            lines.append(f"- **{o[:25]}**：{worst_case}\n")
            lines.append(f"  → 自问：这种情况我能接受吗？有没有预防机制？\n")
    else:
        lines.append(f"（请明确选项后，系统将生成针对每个选项的最坏情况推演）\n")
    
    # 五、决策检查清单
    lines.append(f"\n## 五、决策检查清单\n")
    lines.append(f"在最终决定前，逐项确认：\n")
    lines.append(f"- [ ] **底线通过**：所有🔴底线维度都满足了吗？\n")
    lines.append(f"- [ ] **信息验证**：各维度得分有事实依据，还是仅凭猜测？\n")
    lines.append(f"- [ ] **最坏可接受**：最坏情况发生，仍在你的承受范围内？\n")
    lines.append(f"- [ ] **验证节点**：设定了后续复盘/验证的时间点？\n")
    lines.append(f"- [ ] **理性决策**：这是分析后的选择，而非因为焦虑或压力？\n")
    
    # 六、维度权重记录（可复用）
    lines.append(f"\n## 六、本次画像记录\n")
    for dim in dims:
        icon = "🔴" if dim.get("类型") == "底线" else "🟡"
        lines.append(f"- {icon} {dim['维度']}（权重×{dim.get('权重', 3)}）\n")
    lines.append(f"\n*下次遇到类似选择，可直接复用这套维度*\n")
    
    lines.append(f"\n---\n")
    lines.append(f"*比优 · 先画标准，再量选项*\n")
    
    return '\n'.join(lines)


# ─────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────

def main():
    if len(sys.argv) < 2:
        print("用法: python3 analyze.py <问题描述>", file=sys.stderr)
        print("示例: python3 analyze.py '两个工作，A薪资高但方向不喜欢，B方向喜欢但薪资低20%怎么选'", file=sys.stderr)
        sys.exit(1)
    
    problem = ' '.join(sys.argv[1:])
    print(analyze(problem))


if __name__ == "__main__":
    main()
