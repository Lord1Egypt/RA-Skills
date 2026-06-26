import json
import os
from engine.core import get_gua_numbers

def load_bagua_data():
    data_path = os.path.join(os.path.dirname(__file__), 'data/bagua.json')
    with open(data_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def perform_divination(question):
    bagua = load_bagua_data()
    upper_idx, lower_idx, yao = get_gua_numbers()
    
    upper = bagua[str(upper_idx)]
    lower = bagua[str(lower_idx)]
    
    gua_name = f"{upper['name']}{lower['name']}"
    
    print(f"--- 易经占卜结果 ---")
    print(f"问题: {question}")
    print(f"上卦: {upper['name']} ({upper['symbol']})")
    print(f"下卦: {lower['name']} ({lower['symbol']})")
    print(f"本卦: {gua_name} 卦")
    print(f"变爻: 第 {yao} 爻")
    print(f"-------------------")
    print(f"接下来请 AI 根据此卦象为您进行针对性解读。")

if __name__ == "__main__":
    import sys
    question = sys.argv[1] if len(sys.argv) > 1 else "今日运势"
    perform_divination(question)
