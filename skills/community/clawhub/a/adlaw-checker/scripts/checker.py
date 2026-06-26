#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
广告法违禁词检测器
Author: 咪咪
Version: 1.0.0
"""

import json
import re
from typing import Dict, List, Optional
from datetime import datetime


class AdLawChecker:
    """广告法违禁词检测器"""
    
    def __init__(self, lang: str = "zh"):
        """初始化检测器"""
        self.lang = lang
        self.violation_words = self._load_violation_words()
        self.platform_rules = self._load_platform_rules()
        self.suggestions = self._load_suggestions()
    
    def _load_violation_words(self) -> Dict[str, List[str]]:
        """加载违禁词库"""
        return {
            "high": [
                # 绝对化用语
                "最", "最好", "最佳", "最优", "最强", "顶级", "顶尖",
                "第一", "首个", "唯一", "独家", "首家", "第一品牌",
                "绝对", "绝对好", "100%", "百分百", "完全", "彻底",
                "永久", "万能", "所有", "任何", "一切", "每个",
                "史无前例", "前无古人", "绝无仅有", "世界第一",
                # 虚假宣传
                "根治", "根除", "永不", "永不反弹", "一天见效",
                "三天见效", "立即见效", "零风险", "无风险", "稳赚",
                "稳赚不赔", "包过", "保过", "无效退款", "包治百病",
                "延年益寿", "长生不老"
            ],
            "medium": [
                # 夸大用语
                "领先", "领先品牌", "领导者", "领袖品牌", "旗舰",
                "王牌", "金牌", "名牌", "著名", "知名", "顶级体验",
                "极致", "完美", "完美体验", "卓越", "非凡", "震撼",
                "颠覆", "革命性", "突破性", "重大突破"
            ],
            "low": [
                # 推荐用语 (需注意上下文)
                "推荐", "值得", "值得拥有", "必买", "必备", "神器",
                "种草", "必入", "必囤", "断货王", "爆款", "热卖",
                "热销", "畅销", "人气", "受欢迎", "好评如潮"
            ],
            "platform_xiaohongshu": [
                # 小红书特定
                "全网最低", "最低价", "史上最低", "点击领取",
                "立即抢购", "限时秒杀", "秒杀价", "跳楼价"
            ],
            "platform_wechat": [
                # 微信公众号特定
                "关注领取", "转发获取", "分享得", "邀请好友",
                "点击阅读原文", "点击下方链接"
            ]
        }
    
    def _load_platform_rules(self) -> Dict:
        """加载平台规则"""
        return {
            "xiaohongshu": {
                "name": "小红书",
                "strict_level": "high",
                "special_rules": [
                    "不能直接引导购买",
                    "不能使用诱导性用语",
                    "需要标注广告/合作"
                ]
            },
            "wechat": {
                "name": "微信公众号",
                "strict_level": "medium",
                "special_rules": [
                    "不能诱导分享",
                    "不能诱导关注",
                    "不能使用夸张标题"
                ]
            },
            "douyin": {
                "name": "抖音",
                "strict_level": "high",
                "special_rules": [
                    "不能虚假宣传",
                    "不能引导私下交易",
                    "需要标注广告"
                ]
            }
        }
    
    def _load_suggestions(self) -> Dict[str, str]:
        """加载替换建议"""
        return {
            # 绝对化用语替换
            "最": "很/非常",
            "最好": "优秀/出色",
            "最佳": "良好/不错",
            "第一": "领先/前列",
            "顶级": "高端/优质",
            "唯一": "独特/特别",
            "绝对": "非常/相当",
            "100%": "几乎/大部分",
            "永久": "长期/持久",
            "万能": "多功能/多种用途",
            # 虚假宣传替换
            "根治": "改善/缓解",
            "永不反弹": "效果持久",
            "一天见效": "持续使用可见效果",
            "零风险": "低风险",
            "稳赚不赔": "投资有风险",
            # 平台特定替换
            "种草": "推荐/分享",
            "必买": "值得入手",
            "断货王": "热门/受欢迎",
            "全网最低": "优惠/划算"
        }
    
    def check(self, text: str, platform: Optional[str] = None) -> Dict:
        """
        检查文案合规性
        
        Args:
            text: 待检查的文案
            platform: 平台 (xiaohongshu, wechat, douyin)
            
        Returns:
            检查结果
        """
        violations = []
        
        # 检查高风险词
        for word in self.violation_words.get("high", []):
            positions = self._find_all_positions(text, word)
            for pos in positions:
                violations.append({
                    "word": word,
                    "position": pos,
                    "risk_level": "high",
                    "category": "绝对化用语/虚假宣传",
                    "suggestion": self.suggestions.get(word, "建议删除或替换")
                })
        
        # 检查中风险词
        for word in self.violation_words.get("medium", []):
            positions = self._find_all_positions(text, word)
            for pos in positions:
                violations.append({
                    "word": word,
                    "position": pos,
                    "risk_level": "medium",
                    "category": "夸大用语",
                    "suggestion": self.suggestions.get(word, "建议谨慎使用")
                })
        
        # 检查低风险词
        for word in self.violation_words.get("low", []):
            positions = self._find_all_positions(text, word)
            for pos in positions:
                violations.append({
                    "word": word,
                    "position": pos,
                    "risk_level": "low",
                    "category": "推荐用语",
                    "suggestion": self.suggestions.get(word, "注意上下文")
                })
        
        # 检查平台特定规则
        if platform and platform in self.violation_words:
            for word in self.violation_words[platform]:
                positions = self._find_all_positions(text, word)
                for pos in positions:
                    violations.append({
                        "word": word,
                        "position": pos,
                        "risk_level": "high",
                        "category": f"{platform}平台规则",
                        "suggestion": self.suggestions.get(word, "建议删除")
                    })
        
        # 计算风险等级和合规分数
        risk_level = self._calculate_risk_level(violations)
        compliance_score = self._calculate_compliance_score(violations, len(text))
        
        # 生成修改建议
        suggestions = self._generate_suggestions(violations)
        
        # 生成合规版本
        compliant_version = self._generate_compliant_version(text, violations)
        
        return {
            "text": text,
            "violations": violations,
            "risk_level": risk_level,
            "compliance_score": compliance_score,
            "suggestions": suggestions,
            "compliant_version": compliant_version,
            "checked_at": datetime.now().isoformat()
        }
    
    def _find_all_positions(self, text: str, word: str) -> List[int]:
        """查找词汇在文本中的所有位置"""
        positions = []
        start = 0
        while True:
            pos = text.find(word, start)
            if pos == -1:
                break
            positions.append(pos)
            start = pos + 1
        return positions
    
    def _calculate_risk_level(self, violations: List[Dict]) -> str:
        """计算风险等级"""
        if not violations:
            return "low"
        
        high_count = sum(1 for v in violations if v["risk_level"] == "high")
        medium_count = sum(1 for v in violations if v["risk_level"] == "medium")
        
        if high_count > 0:
            return "high"
        elif medium_count > 2:
            return "medium"
        else:
            return "low"
    
    def _calculate_compliance_score(self, violations: List[Dict], text_length: int) -> int:
        """计算合规分数 (0-100)"""
        if not violations:
            return 100
        
        # 扣分规则
        high_penalty = 15
        medium_penalty = 8
        low_penalty = 3
        
        total_penalty = sum(
            high_penalty if v["risk_level"] == "high" else
            medium_penalty if v["risk_level"] == "medium" else
            low_penalty
            for v in violations
        )
        
        score = max(0, 100 - total_penalty)
        return score
    
    def _generate_suggestions(self, violations: List[Dict]) -> List[str]:
        """生成修改建议"""
        suggestions = []
        
        if not violations:
            return ["文案合规，无需修改"]
        
        # 按风险等级排序
        sorted_violations = sorted(violations, key=lambda x: x["risk_level"], reverse=True)
        
        for v in sorted_violations[:5]:  # 最多显示 5 条建议
            suggestions.append(f"将'{v['word']}'替换为'{v['suggestion']}'")
        
        return suggestions
    
    def _generate_compliant_version(self, text: str, violations: List[Dict]) -> str:
        """生成合规版本"""
        compliant_text = text
        
        # 按位置倒序替换，避免位置偏移
        sorted_violations = sorted(violations, key=lambda x: x["position"], reverse=True)
        
        for v in sorted_violations:
            replacement = v["suggestion"].split("/")[0]  # 取第一个建议
            compliant_text = (
                compliant_text[:v["position"]] +
                replacement +
                compliant_text[v["position"] + len(v["word"]):]
            )
        
        return compliant_text
    
    def batch_check(self, texts: List[str], platform: Optional[str] = None) -> List[Dict]:
        """批量检查"""
        return [self.check(text, platform) for text in texts]
    
    def add_violation_words(self, words: List[str], risk_level: str = "medium"):
        """添加自定义违禁词"""
        if risk_level not in self.violation_words:
            self.violation_words[risk_level] = []
        self.violation_words[risk_level].extend(words)
    
    def add_suggestion(self, word: str, suggestion: str):
        """添加自定义替换建议"""
        self.suggestions[word] = suggestion
    
    def set_industry(self, industry: str):
        """设置行业特定规则"""
        industry_words = {
            "cosmetics": ["美白", "祛斑", "祛痘", "抗衰老", "年轻化"],
            "food": ["纯天然", "无添加", "有机", "绿色", "健康"],
            "education": ["保过", "包过", "提分", "名师", "一对一"],
            "finance": ["保本", "高收益", "稳赚", "无风险", "理财"]
        }
        
        if industry in industry_words:
            self.add_violation_words(industry_words[industry], "high")


def main():
    """主函数 - 命令行入口"""
    import argparse
    
    parser = argparse.ArgumentParser(description="广告法违禁词检测器")
    parser.add_argument("command", choices=["check", "batch"], help="命令类型")
    parser.add_argument("--text", help="待检查的文案")
    parser.add_argument("--file", help="待检查的文件")
    parser.add_argument("--platform", choices=["xiaohongshu", "wechat", "douyin"], help="平台")
    parser.add_argument("--report", help="报告输出路径")
    
    args = parser.parse_args()
    
    checker = AdLawChecker()
    
    if args.command == "check":
        if args.file:
            with open(args.file, 'r', encoding='utf-8') as f:
                text = f.read()
        elif args.text:
            text = args.text
        else:
            print("错误：请提供文案 (--text 或 --file)")
            return
        
        result = checker.check(text, args.platform)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        
        if args.report:
            with open(args.report, 'w', encoding='utf-8') as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
            print(f"报告已保存到：{args.report}")


if __name__ == "__main__":
    main()
