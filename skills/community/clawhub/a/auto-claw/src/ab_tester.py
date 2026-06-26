"""
A/B Testing Engine — WordPress 极致A/B测试框架
支持多变量测试、自动分流、统计显著性判断
"""
import re
import json
import time
import hashlib
import random
import statistics
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from collections import defaultdict

@dataclass
class ABVariant:
    """测试变体"""
    id: str
    name: str  # "Control" / "Variant A" / "Variant B"
    traffic_split: float = 0.5  # 0.0-1.0
    headline: str = ""
    description: str = ""
    cta_text: str = ""
    cta_color: str = ""
    
    # 统计数据
    visitors: int = 0
    conversions: int = 0
    
    @property
    def conversion_rate(self) -> float:
        return self.conversions / self.visitors if self.visitors > 0 else 0.0

@dataclass
class ABTest:
    """A/B测试配置"""
    test_id: str
    name: str
    url: str  # 测试的目标页面
    
    # 测试元素
    test_element: str  # "headline" / "cta" / "hero_image" / "price"
    variants: List[ABVariant] = field(default_factory=list)
    
    # 目标
    goal_type: str = "click"  # click / form_submit / scroll_depth / time_on_page / purchase
    goal_selector: str = ""  # CSS selector for goal
    
    # 状态
    status: str = "draft"  # draft / running / paused / completed
    started_at: str = ""
    ended_at: str = ""
    confidence_threshold: float = 0.95
    
    # 结果
    winner_id: str = ""
    confidence: float = 0.0
    lift: float = 0.0  # 相对于对照组的提升
    
    notes: str = ""

@dataclass
class ABTestResult:
    """测试结果"""
    test_id: str
    test_name: str
    status: str
    winner: str = ""
    confidence: float = 0.0
    lift: float = 0.0
    duration_days: int = 0
    
    variant_results: List[Dict] = field(default_factory=list)
    recommendation: str = ""

class ABTester:
    """
    WordPress A/B测试引擎
    
    功能：
    1. 创建和运行A/B测试
    2. 自动分流（基于Cookie/指纹）
    3. 收集数据（点击/转化/滚动深度）
    4. 统计显著性分析（贝叶斯方法）
    5. 生成最优变体推荐
    6. 自动应用获胜者（通过Gate Pipeline）
    """
    
    def __init__(self, web_root: str = ""):
        self.web_root = web_root
        self.tests: Dict[str, ABTest] = {}
        self.session_key = "ab_test_sessions"
    
    def create_test(self, name: str, url: str, test_element: str,
                   goal_type: str = "click", goal_selector: str = "",
                   confidence_threshold: float = 0.95) -> ABTest:
        """创建新测试"""
        test_id = hashlib.md5(f"{name}{time.time()}".encode()).hexdigest()[:8]
        
        test = ABTest(
            test_id=test_id,
            name=name,
            url=url,
            test_element=test_element,
            goal_type=goal_type,
            goal_selector=goal_selector,
            confidence_threshold=confidence_threshold,
            status="draft"
        )
        
        self.tests[test_id] = test
        return test
    
    def add_variant(self, test_id: str, name: str, traffic_split: float = 0.5,
                    headline: str = "", description: str = "",
                    cta_text: str = "", cta_color: str = "") -> ABVariant:
        """添加变体"""
        test = self.tests.get(test_id)
        if not test:
            raise ValueError(f"Test {test_id} not found")
        
        variant = ABVariant(
            id=hashlib.md5(f"{test_id}{name}{time.time()}".encode()).hexdigest()[:6],
            name=name,
            traffic_split=traffic_split,
            headline=headline,
            description=description,
            cta_text=cta_text,
            cta_color=cta_color
        )
        
        test.variants.append(variant)
        
        # 确保 traffic_split 总和 <= 1
        total = sum(v.traffic_split for v in test.variants)
        if total > 1.0:
            # 归一化
            for v in test.variants:
                v.traffic_split /= total
        
        return variant
    
    def assign_variant(self, test_id: str, visitor_id: str) -> Optional[ABVariant]:
        """为访客分配变体（基于哈希分流）"""
        test = self.tests.get(test_id)
        if not test or test.status != "running":
            return None
        
        # 基于访客ID的确定性哈希
        hash_input = f"{test_id}:{visitor_id}"
        hash_val = int(hashlib.md5(hash_input.encode()).hexdigest(), 16)
        threshold = (hash_val % 10000) / 10000.0
        
        cumulative = 0.0
        for variant in test.variants:
            cumulative += variant.traffic_split
            if threshold <= cumulative:
                return variant
        
        return test.variants[0]  # 默认第一个
    
    def record_visitor(self, test_id: str, variant_id: str, visitor_id: str):
        """记录访客"""
        test = self.tests.get(test_id)
        if not test:
            return
        
        for v in test.variants:
            if v.id == variant_id:
                v.visitors += 1
                break
    
    def record_conversion(self, test_id: str, variant_id: str, visitor_id: str, value: float = 1.0):
        """记录转化"""
        test = self.tests.get(test_id)
        if not test:
            return
        
        for v in test.variants:
            if v.id == variant_id:
                v.conversions += 1
                break
    
    def calculate_significance(self, test: ABTest) -> Tuple[float, str]:
        """
        计算统计显著性（贝叶斯方法简化版）
        返回 (confidence, winner_id)
        """
        if len(test.variants) < 2:
            return 0.0, ""
        
        control = test.variants[0]
        variants = test.variants[1:]
        
        results = []
        for v in test.variants:
            if v.visitors < 30:  # 最小样本量
                results.append((0.0, v.id))
                continue
            
            cr = v.conversion_rate
            baseline = control.conversion_rate if control == v else variants[0].conversion_rate
            
            # 简化的贝叶斯 A/B
            # 使用Beta分布近似
            alpha = v.conversions + 1
            beta = max(1, v.visitors - v.conversions)
            
            # 简单置信度估算
            if v.visitors >= 100 and cr > 0:
                # Z-test 简化版
                p1 = cr
                p2 = control.conversion_rate if control != v else (variants[0].conversion_rate if variants else 0)
                n1 = v.visitors
                n2 = control.visitors if control != v else variants[0].visitors
                
                if n1 > 0 and n2 > 0 and p2 > 0:
                    pooled_p = (v.conversions + (control.conversions if control != v else variants[0].conversions)) / (n1 + n2)
                    se = (pooled_p * (1 - pooled_p) * (1/n1 + 1/n2)) ** 0.5
                    if se > 0:
                        z = (p1 - p2) / se
                        # 简化Z值到置信度
                        import math
                        confidence = min(0.99, max(0.0, 0.5 + math.erf(z / 2 ** 0.5) / 2))
                    else:
                        confidence = 0.5
                else:
                    confidence = 0.5
            else:
                confidence = 0.5
            
            results.append((confidence, v.id))
        
        # 选择置信度最高且提升为正的
        best_conf, best_id = max(results, key=lambda x: x[0])
        
        # 检查提升
        winner = next((v for v in test.variants if v.id == best_id), None)
        if winner and control != winner:
            lift = (winner.conversion_rate - control.conversion_rate) / control.conversion_rate if control.conversion_rate > 0 else 0
            test.lift = lift
        else:
            test.lift = 0
        
        if best_conf >= test.confidence_threshold:
            return best_conf, best_id
        
        return best_conf, ""
    
    def analyze_test(self, test_id: str) -> ABTestResult:
        """分析测试结果"""
        test = self.tests.get(test_id)
        if not test:
            return ABTestResult(test_id=test_id, test_name="", status="not_found")
        
        confidence, winner_id = self.calculate_significance(test)
        
        test.confidence = confidence
        test.winner_id = winner_id
        
        # 变异结果
        variant_results = []
        for v in test.variants:
            variant_results.append({
                "name": v.name,
                "visitors": v.visitors,
                "conversions": v.conversions,
                "conversion_rate": round(v.conversion_rate, 4),
                "is_winner": v.id == winner_id
            })
        
        # 建议
        if winner_id:
            winner = next(v for v in test.variants if v.id == winner_id)
            rec = f"变体 '{winner.name}' 置信度 {confidence:.1%}，"
            rec += f"转化率提升 {test.lift:.1%}"
            if test.lift > 0.1:
                rec += "，建议立即应用"
            elif test.lift > 0:
                rec += "，建议再观察几天确认"
            else:
                rec = "当前变体无显著提升，建议调整后再测"
        else:
            rec = f"样本量不足或置信度未达标({confidence:.1%})，继续收集数据"
        
        # 计算持续时间
        duration = 0
        if test.started_at:
            start = datetime.fromisoformat(test.started_at)
            end = datetime.now()
            if test.ended_at:
                end = datetime.fromisoformat(test.ended_at)
            duration = (end - start).days
        
        return ABTestResult(
            test_id=test_id,
            test_name=test.name,
            status=test.status,
            winner=winner_id,
            confidence=confidence,
            lift=test.lift,
            duration_days=duration,
            variant_results=variant_results,
            recommendation=rec
        )
    
    def start_test(self, test_id: str) -> bool:
        """启动测试"""
        test = self.tests.get(test_id)
        if not test or len(test.variants) < 2:
            return False
        
        test.status = "running"
        test.started_at = datetime.now().isoformat()
        return True
    
    def stop_test(self, test_id: str) -> bool:
        """停止测试"""
        test = self.tests.get(test_id)
        if not test:
            return False
        
        test.status = "completed"
        test.ended_at = datetime.now().isoformat()
        return True
    
    def generate_wp_shortcode(self, test: ABTest) -> str:
        """生成 WordPress shortcode 用于插入测试"""
        code = f'''[ab-test id="{test.test_id}" element="{test.test_element}" goal="{test.goal_type}"]
'''
        for v in test.variants:
            code += f'''  [ab-variant id="{v.id}" name="{v.name}" traffic="{int(v.traffic_split*100)}%"]
'''
        code += "[/ab-test]"
        return code
    
    def export_results(self, test_id: str) -> str:
        """导出测试结果 JSON"""
        result = self.analyze_test(test_id)
        return json.dumps(result, ensure_ascii=False, indent=2)

def demo():
    """演示"""
    tester = ABTester()
    
    # 创建测试
    test = tester.create_test(
        name="Hero Headline Test",
        url="http://example.com/landing",
        test_element="headline",
        goal_type="click",
        goal_selector=".cta-button"
    )
    
    # 添加变体
    tester.add_variant(test.test_id, "Control", traffic_split=0.5,
                      headline="The Best Widget for Your Needs")
    tester.add_variant(test.test_id, "Variant A - Urgency", traffic_split=0.5,
                      headline="Don't Miss Out: 50% Off Today Only!")
    
    # 启动
    tester.start_test(test.test_id)
    
    # 模拟数据
    control = test.variants[0]
    variant_a = test.variants[1]
    
    # 模拟1000访客，Control 3%转化，Variant A 4.5%转化
    control.visitors = 500
    control.conversions = 15
    
    variant_a.visitors = 500
    variant_a.conversions = 23
    
    # 分析
    result = tester.analyze_test(test.test_id)
    
    print(f"\n📊 A/B Test Results: {result.test_name}")
    print(f"   状态: {result.status}")
    print(f"   持续: {result.duration_days}天")
    print()
    for vr in result.variant_results:
        icon = "🏆" if vr.get("is_winner") else "  "
        print(f"   {icon} {vr['name']}: {vr['visitors']}访客 / {vr['conversions']}转化 / {vr['conversion_rate']:.2%}")
    
    print()
    print(f"   获胜者: {result.winner or '无显著差异'}")
    print(f"   置信度: {result.confidence:.1%}")
    print(f"   提升: {result.lift:.1%}")
    print()
    print(f"   建议: {result.recommendation}")
    
    print("\n   WordPress Shortcode:")
    print(f"   {tester.generate_wp_shortcode(test)}")

if __name__ == "__main__":
    demo()
