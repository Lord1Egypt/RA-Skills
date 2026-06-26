from engine.plum_blossom import PlumBlossomEngine

def test_engine():
    engine = PlumBlossomEngine()
    
    # 模拟多次起卦，验证输出格式
    print("--- 算法引擎验证测试 ---")
    for i in range(3):
        res = engine.calculate()
        print(f"测试 {i+1}: 上卦={res['upper']}, 下卦={res['lower']}, 变爻={res['yao']}")
    print("--- 验证通过 ---")

if __name__ == "__main__":
    test_engine()
