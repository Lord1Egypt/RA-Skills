#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI 投毒内容过滤助手
检测 GEO 投毒内容，验证信息来源，保护 AI 助手
"""

import argparse
import sys
import re
from datetime import datetime

# 投毒特征库
POISON_PATTERNS = {
    "虚假权威": [
        r"专家强烈推荐",
        r"专家一致认可",
        r"权威机构认证",
        r"医生推荐",
        r"科学家证实",
    ],
    "绝对化用语": [
        r"行业第一",
        r"全网最优",
        r"效果最好",
        r"排名第一",
        r"销量第一",
        r"遥遥领先",
        r"绝无仅有",
    ],
    "从众诱导": [
        r"用户好评如潮",
        r"百万用户选择",
        r"大家都在用",
        r"口碑爆棚",
        r"好评率.*%",
    ],
    "AI操控": [
        r"AI推荐.*首选",
        r"人工智能推荐",
        r"智能算法推荐",
        r"大数据推荐",
    ],
    "虚假评测": [
        r"实测证明",
        r"实验证明",
        r"临床证明",
        r"数据证明",
    ],
}

SUSPICIOUS_KEYWORDS = [
    "限时优惠", "错过再等", "最后机会", "立即抢购",
    "独家", "秘制", "祖传", "特效", "神奇",
]

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def print_header(text):
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'━' * 60}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.CYAN}{text}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'━' * 60}{Colors.RESET}\n")

def detect_poison(text):
    """检测投毒内容"""
    findings = []
    score = 0
    
    for category, patterns in POISON_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, text, re.IGNORECASE):
                findings.append({
                    "category": category,
                    "pattern": pattern,
                    "matched": re.search(pattern, text, re.IGNORECASE).group(),
                })
                score += 15
    
    # 检查可疑关键词
    for keyword in SUSPICIOUS_KEYWORDS:
        if keyword in text:
            findings.append({
                "category": "可疑关键词",
                "pattern": keyword,
                "matched": keyword,
            })
            score += 10
    
    return findings, min(score, 100)

def assess_risk(score):
    """评估风险等级"""
    if score >= 70:
        return "危险", Colors.RED
    elif score >= 40:
        return "可疑", Colors.YELLOW
    else:
        return "安全", Colors.GREEN

def generate_report(text, findings, score):
    """生成检测报告"""
    risk_level, color = assess_risk(score)
    
    print_header("🛡️ AI 投毒内容检测报告")
    
    print(f"{Colors.BOLD}📋 检测内容：{Colors.RESET}")
    print(f"  {text[:100]}{'...' if len(text) > 100 else ''}")
    print()
    
    print(f"{Colors.BOLD}🔍 检测结果：{Colors.RESET}", end="")
    print(f"{color}{risk_level}{Colors.RESET}")
    print()
    
    print(f"{Colors.BOLD}📊 风险评分：{Colors.RESET}", end="")
    if score >= 70:
        print(f"{Colors.RED}{score}/100（高风险）{Colors.RESET}")
    elif score >= 40:
        print(f"{Colors.YELLOW}{score}/100（中风险）{Colors.RESET}")
    else:
        print(f"{Colors.GREEN}{score}/100（低风险）{Colors.RESET}")
    print()
    
    if findings:
        print(f"{Colors.BOLD}🚩 发现的投毒特征（{len(findings)} 个）：{Colors.RESET}")
        for i, finding in enumerate(findings, 1):
            print(f"  {i}. {Colors.YELLOW}⚠️ {finding['category']}{Colors.RESET}")
            print(f"     匹配：「{finding['matched']}」")
        print()
    else:
        print(f"{Colors.GREEN}✅ 未发现明显投毒特征{Colors.RESET}")
        print()
    
    print(f"{Colors.BOLD}💡 建议：{Colors.RESET}")
    if score >= 70:
        print(f"  {Colors.RED}❌ 不建议信任此内容{Colors.RESET}")
        print(f"  {Colors.YELLOW}⚠️ 可能是 GEO 投毒内容{Colors.RESET}")
        print(f"  ✅ 请通过官方渠道核实")
        print(f"  ✅ 查看多个独立来源")
    elif score >= 40:
        print(f"  {Colors.YELLOW}⚠️ 需要谨慎对待{Colors.RESET}")
        print(f"  ✅ 建议进一步核实")
        print(f"  ✅ 对比多个信息源")
    else:
        print(f"  {Colors.GREEN}✅ 内容相对安全{Colors.RESET}")
        print(f"  ✅ 但仍建议保持警惕")
    print()
    
    print(f"{Colors.BOLD}📖 参考：{Colors.RESET}")
    print(f"  央视3·15晚会曝光 GEO 投毒案例")
    print(f"  https://clawhub.ai/testmtcode/ai-poison-guard")

def main():
    parser = argparse.ArgumentParser(
        description="AI 投毒内容过滤助手",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    
    parser.add_argument("--detect-text", type=str, metavar="TEXT",
                        help="检测文本内容")
    parser.add_argument("--detect-file", type=str, metavar="FILE",
                        help="检测文件内容")
    parser.add_argument("--json", action="store_true",
                        help="输出 JSON 格式")
    
    args = parser.parse_args()
    
    if args.detect_text:
        text = args.detect_text
        findings, score = detect_poison(text)
        
        if args.json:
            import json
            result = {
                "text": text,
                "findings": findings,
                "score": score,
                "risk_level": assess_risk(score)[0],
                "timestamp": datetime.now().isoformat(),
            }
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            generate_report(text, findings, score)
    
    elif args.detect_file:
        try:
            with open(args.detect_file, 'r', encoding='utf-8') as f:
                text = f.read()
            findings, score = detect_poison(text)
            generate_report(text, findings, score)
        except FileNotFoundError:
            print(f"{Colors.RED}❌ 文件不存在：{args.detect_file}{Colors.RESET}")
            sys.exit(1)
    
    else:
        # 交互模式
        print_header("🛡️ AI 投毒内容过滤助手")
        print("输入要检测的内容（直接回车退出）：")
        print()
        
        while True:
            try:
                text = input(f"{Colors.CYAN}> {Colors.RESET}").strip()
                if not text:
                    break
                
                findings, score = detect_poison(text)
                generate_report(text, findings, score)
                
                print("\n" + "━" * 60 + "\n")
            
            except KeyboardInterrupt:
                print(f"\n\n{Colors.GREEN}再见！{Colors.RESET}")
                break

if __name__ == "__main__":
    main()
