#!/usr/bin/env python3
"""
考试系统核心
层次结构: 难度调整层 → 选择题型层 → 考试层

考试层:
  1. 检测生词层 (偶尔混杂语言，双语输出，检测用户不会的生词)
  2. 考考你层 (从生词库抽单词测试用户)

重要：只有 hybrid 模式才调用随机筛子
"""

import random
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "lib"))

from core import NewWordLibrary, load_config

# 难度等级
DIFFICULTY = {
    "rare": {"name": "稀少", "ratio": 0.3},
    "medium": {"name": "中等", "ratio": 0.5},
    "dense": {"name": "密集", "ratio": 0.8}
}

# 选择题类型
QUESTION_TYPE = {
    "pure_l1": {"name": "纯第一层", "order": ["detection"]},
    "pure_l2": {"name": "纯第二层", "order": ["quiz"]},
    "hybrid": {"name": "混合型", "order": ["detection", "quiz"]}  # 需要随机打乱顺序
}

class ExamSystem:
    def __init__(self, difficulty: str = "medium"):
        self.difficulty = difficulty
        self.difficulty_ratio = DIFFICULTY.get(difficulty, DIFFICULTY["medium"])["ratio"]
    
    def should_trigger_exam(self) -> bool:
        """根据难度决定是否触发考试"""
        return random.random() < self.difficulty_ratio
    
    def detection_layer(self) -> dict:
        """检测生词层"""
        new_lib = NewWordLibrary()
        words = new_lib.list_all()
        
        if not words:
            return {"layer": "detection", "type": "info", "content": "生词库为空"}
        
        sample_size = min(len(words), random.randint(1, 3))
        sample_words = random.sample(words, sample_size)
        
        return {
            "layer": "detection",
            "type": "bilingual_check",
            "content": sample_words,
            "message": "请确认你认识以下单词"
        }
    
    def quiz_layer(self, num_questions: int = 3) -> dict:
        """考考你层"""
        new_lib = NewWordLibrary()
        words = new_lib.list_all()
        
        if len(words) < num_questions:
            num_questions = len(words) if words else 0
        
        if num_questions == 0:
            return {"layer": "quiz", "type": "info", "content": "生词库单词不足"}
        
        questions = random.sample(words, num_questions)
        
        return {
            "layer": "quiz",
            "type": "quiz",
            "content": questions,
            "message": f"请拼写以下 {num_questions} 个单词"
        }
    
    def run_exam(self, question_type: str) -> list:
        """
        运行考试流程
        - pure_l1: 直接执行检测生词层
        - pure_l2: 直接执行考考你层
        - hybrid: 调用随机筛子打乱顺序
        """
        if not self.should_trigger_exam():
            return []
        
        qt_info = QUESTION_TYPE.get(question_type, QUESTION_TYPE["hybrid"])
        layers = qt_info["order"].copy()
        
        # 只有 hybrid 模式才随机打乱顺序
        if question_type == "hybrid":
            random.shuffle(layers)
        
        exam_session = []
        for layer in layers:
            if layer == "detection":
                exam_session.append(self.detection_layer())
            elif layer == "quiz":
                exam_session.append(self.quiz_layer())
        
        return exam_session

def main():
    # 优先使用命令行参数，否则读取配置文件
    config = load_config()
    difficulty = sys.argv[1] if len(sys.argv) > 1 else config["difficulty"]
    question_type = sys.argv[2] if len(sys.argv) > 2 else config["question_type"]

    system = ExamSystem(difficulty)
    
    print(f"考试系统启动 | 难度: {DIFFICULTY[difficulty]['name']} | 题型: {QUESTION_TYPE[question_type]['name']}")
    print("-" * 40)
    
    results = system.run_exam(question_type)
    
    if not results:
        print("本次对话未触发考试")
        return
    
    for i, exam in enumerate(results, 1):
        print(f"\n[考试{i}] {exam['layer']}")
        if exam["type"] == "bilingual_check":
            print(exam["message"])
            for w in exam["content"]:
                print(f"  - {w['name']} ({w['pos']})")
        elif exam["type"] == "quiz":
            print(exam["message"])
            for w in exam["content"]:
                print(f"  ? {w['name']}")

if __name__ == "__main__":
    main()
