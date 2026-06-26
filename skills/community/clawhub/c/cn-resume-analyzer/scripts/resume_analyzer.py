#!/usr/bin/env python3
"""cn-resume-analyzer - AI简历分析优化工具"""
import sys, re

def analyze_resume(text):
    """分析简历内容
    
    提供结构化评分、关键词匹配、格式建议和改进方案。
    使用规则分析，不依赖外部AI API。
    
    Args:
        text: 简历文本内容
    
    Returns:
        dict: 分析结果
    """
    if not text or len(text.strip()) < 50:
        return {"error": "简历内容太短，请提供更完整的简历"}
    
    score = 0
    suggestions = []
    keywords_found = []
    
    # 基础检查
    checks = {
        "contact": (r"(手机|电话|微信|邮箱|@|\d{11})", "联系方式"),
        "education": (r"(本科|硕士|博士|学士|大学|学院|专业|985|211|QS)", "教育背景"),
        "experience": (r"(工作|实习|项目|负责|参与|担任)", "工作/项目经验"),
        "skills": (r"(Python|Java|JS|React|Vue|SQL|Linux|AWS|Docker|K8s|AI|ML|Deep Learning)", "技术技能"),
        "achievement": (r"(增长|提升|优化|完成|获得|产出|业绩|指标)", "成果描述"),
    }
    
    results = {}
    for key, (pattern, label) in checks.items():
        found = bool(re.search(pattern, text))
        results[key] = found
        if found:
            score += 20
            keywords_found.append(label)
        else:
            suggestions.append(f"缺少{label}部分")
    
    # 格式检查
    lines = text.split('\n')
    if len(lines) > 10:
        score += 5
    else:
        suggestions.append("简历结构偏简单，建议增加详细内容")
    
    # 关键词密度
    skill_pattern = r"(Python|Java|JS|React|SQL|AWS|AI|ML|产品|运营|市场|设计)"
    skills_count = len(re.findall(skill_pattern, text))
    if skills_count >= 5:
        score += 10
        keywords_found.append(f"核心技能({skills_count}项)")
    
    # 评分
    score = min(100, score)
    grade = "优秀" if score >= 80 else "良好" if score >= 60 else "一般" if score >= 40 else "待完善"
    
    # 改进建议
    if score < 80:
        suggestions.extend([
            "建议量化工作成果（如：提升效率30%）",
            "确保联系方式完整",
            "突出与目标岗位相关的核心技能",
        ])
    
    return {
        "score": score,
        "grade": grade,
        "keywords_found": keywords_found,
        "checks": results,
        "suggestions": list(set(suggestions)),
        "summary": f"简历得分为{score}分({grade})，{'基本合格，建议优化细节' if score >= 60 else '需要大幅改进'}"
    }

def generate_improvement(text, target_role=None):
    """生成简历优化建议"""
    analysis = analyze_resume(text)
    
    suggestions = [
        "📝 结构优化：按「基本信息→求职意向→教育背景→工作经历→项目经验→技能特长」排列",
        "💡 量化成果：将「负责XX工作」改为「负责XX，实现XX%增长/提升」",
        "🎯 关键词匹配：根据目标岗位JD提取关键词，确保简历中包含核心技能词",
        "📊 数据支撑：用具体数字展示成果（如：管理10人团队、日活提升40%）",
    ]
    
    if analysis["score"] >= 80:
        suggestions = ["✨ 简历质量已经很好，主要关注关键词匹配和面试准备"]
    
    return {
        "analysis": analysis,
        "improvements": suggestions,
        "target_role": target_role
    }

if __name__ == '__main__':
    if len(sys.argv) > 1:
        text = sys.argv[1]
    else:
        text = sys.stdin.read()
    
    result = analyze_resume(text)
    print(f"\n📊 简历分析报告")
    print(f"{'='*40}")
    print(f"得分: {result['score']}/100 ({result['grade']})")
    print(f"\n✅ 已包含: {', '.join(result['keywords_found'])}")
    print(f"\n💡 改进建议:")
    for s in result['suggestions']:
        print(f"   • {s}")
