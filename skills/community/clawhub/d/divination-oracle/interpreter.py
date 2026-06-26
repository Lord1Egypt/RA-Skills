import sys
import json
import os
from engine.plum_blossom import PlumBlossomEngine

def get_gua_interpretation(gua_code):
    data_path = os.path.join(os.path.dirname(__file__), 'data/64gua_db.json')
    with open(data_path, 'r', encoding='utf-8') as f:
        db = json.load(f)
    return db.get(gua_code, "未找到对应的卦象解释")

def interpret_divination(question):
    engine = PlumBlossomEngine()
    res = engine.calculate()
    u, l, y = res['upper'], res['lower'], res['yao']
    
    gua_code = f"{u}{l}"
    gua_info = get_gua_interpretation(gua_code)
    
    print(f"--- 智能占卜解读 ---")
    print(f"问题: {question}")
    print(f"卦象: {gua_info.split('：')[0]} (上卦{u}, 下卦{l}, 变爻第{y}爻)")
    print(f"卦辞: {gua_info}")
    print(f"-------------------")
    print(f"[AI 洞察]: 此卦为 {gua_info.split('：')[0]}。结合您的问题“{question}”，建议关注第 {y} 爻的变动。根据易理，应顺势而为，处理好核心变数。")

if __name__ == "__main__":
    question = sys.argv[1] if len(sys.argv) > 1 else "今日运势"
    interpret_divination(question)
