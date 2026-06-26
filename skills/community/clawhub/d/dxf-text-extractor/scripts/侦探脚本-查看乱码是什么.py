# 侦探脚本：查看乱码到底是什么
test_str = "410"  # 粘贴一条你提取出的乱码
for char in test_str:
    print(f"字符: {char} | Unicode 编码: {hex(ord(char))}")