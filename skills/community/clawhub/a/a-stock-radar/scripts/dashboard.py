"""
A股雷达仪表盘：一键汇总主要指数 + 宏观快照 + 核心企业 + 板块涨跌
用法: python dashboard.py
"""
import subprocess
import sys
import os

base = os.path.dirname(os.path.abspath(__file__))

print("=" * 50)
print("  🦞 A股雷达仪表盘")
print("=" * 50)

# 1. 主要指数
print("\n>>> 主要指数")
subprocess.run([sys.executable, os.path.join(base, "index_spot.py")])

# 2. 宏观快照
print("\n>>> 宏观快照")
subprocess.run([sys.executable, os.path.join(base, "macro_snapshot.py")])

# 3. 核心企业
print("\n>>> A股核心企业")
subprocess.run([sys.executable, os.path.join(base, "core_companies.py")])

# 4. 行业板块
print("\n>>> 行业涨幅榜TOP10")
result = subprocess.run([sys.executable, os.path.join(base, "sector_ranking.py"), "行业板块"], capture_output=True, text=True)
if "暂时不可用" in result.stdout:
    print("（行业板块数据暂时不可用，请稍后重试）")
else:
    print(result.stdout, end="")

# 5. 短线情绪
print("\n>>> 短线情绪")
result2 = subprocess.run([sys.executable, os.path.join(base, "sentiment_snapshot.py")], capture_output=True, text=True)
print(result2.stdout, end="")
