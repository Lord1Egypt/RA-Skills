"""
Cognitive Flexibility Skills 测试用例

测试 OODA Reasoner, Pattern Matcher, Self Assessor, Cognitive Controller
"""

import asyncio
import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.chain_reasoner import OODAReasoner
from scripts.pattern_matcher import PatternMatcher
from scripts.self_assessor import SelfAssessor
from scripts.cognitive_controller import CognitiveController


class MockTools:
    """模拟工具接口（用于测试）"""
    
    async def memory_search(self, query: str, maxResults: int = 5) -> dict:
        """模拟 memory_search"""
        return {
            "results": [
                {
                    "task": "分析用户反馈",
                    "solution_approach": "分类整理反馈，识别高频问题",
                    "success_factors": ["系统化分类", "优先级排序"],
                    "pitfalls": ["忽略长尾问题"],
                    "text": query
                }
            ],
            "provider": "mock",
            "count": 1
        }
    
    async def sessions_send(self, sessionKey: str, message: str, timeoutSeconds: int = 60) -> dict:
        """模拟 sessions_send"""
        return {
            "status": "ok",
            "reply": f"收到：{message}"
        }


async def test_ooda_reasoner():
    """测试 OODA Reasoner"""
    print("\n=== 测试 OODA Reasoner ===")
    
    reasoner = OODAReasoner(confidence_threshold=0.7)
    tools = MockTools()
    
    task = "分析用户反馈数据，找出主要问题"
    result = await reasoner.process(task, tools=tools)
    
    # 验证结果
    assert "final_answer" in result, "缺少最终答案"
    assert "confidence" in result, "缺少置信度"
    assert "steps" in result, "缺少推理步骤"
    
    print(f"✅ 测试通过")
    print(f"   置信度：{result.get('confidence', 0):.2f}")
    print(f"   推理步骤：{len(result.get('steps', []))}步")
    
    return result


async def test_pattern_matcher():
    """测试 Pattern Matcher"""
    print("\n=== 测试 Pattern Matcher ===")
    
    matcher = PatternMatcher(similarity_threshold=0.7)
    tools = MockTools()
    
    task = "分析用户反馈"
    result = await matcher.match(task, tools=tools)
    
    # 验证结果
    assert "mode" in result, "缺少模式信息"
    assert result["mode"] == "OOA", "模式应该是 OOA"
    assert "similar_tasks" in result, "缺少相似任务"
    
    print(f"✅ 测试通过")
    print(f"   相似任务数：{len(result.get('similar_tasks', []))}")
    print(f"   匹配度：{result.get('applicability', {}).get('score', 0):.2f}")
    
    return result


async def test_self_assessor():
    """测试 Self Assessor"""
    print("\n=== 测试 Self Assessor ===")
    
    assessor = SelfAssessor()
    
    # 模拟响应
    response = {
        "answer": "基于分析，主要问题是用户体验不佳",
        "reasoning_chain": [
            {"step": "收集用户反馈", "result": "100 条反馈"},
            {"step": "分类问题", "result": "5 类主要问题"},
            {"step": "优先级排序", "result": "用户体验最紧急"}
        ],
        "confidence": 0.8
    }
    
    assessment = await assessor.evaluate(response)
    
    # 验证结果
    assert "overall_score" in assessment, "缺少综合评分"
    assert "needs_improvement" in assessment, "缺少改进标记"
    
    print(f"✅ 测试通过")
    print(f"   综合评分：{assessment.get('overall_score', 0):.2f}")
    print(f"   需要改进：{assessment.get('needs_improvement', False)}")
    
    return assessment


async def test_cognitive_controller():
    """测试 Cognitive Controller"""
    print("\n=== 测试 Cognitive Controller ===")
    
    controller = CognitiveController(confidence_threshold=0.7)
    tools = MockTools()
    
    # 测试任务 1：简单任务
    task1 = "用户反馈加载慢"
    result1 = await controller.process(task1, tools=tools)
    
    print(f"任务 1（简单）：{result1['mode']} - 置信度：{result1.get('assessment', {}).get('overall_score', 0):.2f}")
    
    # 测试任务 2：复杂任务
    task2 = "分析用户反馈数据，找出主要问题并提出改进建议"
    result2 = await controller.process(task2, tools=tools)
    
    print(f"任务 2（复杂）：{result2['mode']} - 置信度：{result2.get('assessment', {}).get('overall_score', 0):.2f}")
    
    # 验证结果
    assert "mode" in result1, "缺少模式信息"
    assert "mode" in result2, "缺少模式信息"
    assert "assessment" in result2, "缺少评估结果"
    
    print(f"✅ 测试通过")
    
    # 查看统计
    stats = controller.get_mode_statistics()
    print(f"   模式统计：{stats}")
    
    return result2


async def run_all_tests():
    """运行所有测试"""
    print("\n" + "="*60)
    print("Cognitive Flexibility Skills 测试套件")
    print("="*60)
    
    results = {}
    
    try:
        results["OODA Reasoner"] = await test_ooda_reasoner()
        results["Pattern Matcher"] = await test_pattern_matcher()
        results["Self Assessor"] = await test_self_assessor()
        results["Cognitive Controller"] = await test_cognitive_controller()
        
        print("\n" + "="*60)
        print("✅ 所有测试通过！")
        print("="*60)
        
        return {"status": "success", "results": results}
    
    except AssertionError as e:
        print(f"\n❌ 测试失败：{e}")
        return {"status": "failed", "error": str(e)}
    
    except Exception as e:
        print(f"\n❌ 测试异常：{e}")
        import traceback
        traceback.print_exc()
        return {"status": "error", "error": str(e)}


if __name__ == "__main__":
    result = asyncio.run(run_all_tests())
    
    # 输出测试结果
    if result["status"] == "success":
        print("\n测试完成，所有功能正常！")
        sys.exit(0)
    else:
        print(f"\n测试失败：{result.get('error', '未知错误')}")
        sys.exit(1)
