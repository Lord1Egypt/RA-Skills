# Python 脚本写入配置文件
import subprocess

config_content = '''
model1: doubao-seed-2-0-lite-260215
model2: doubao-seed-2-0-pro-260215
model3: doubao-seed-2-0-mini-260215
model4: doubao-seedance-2-0-260215
model5: doubao-seedance-2-0-fast-260215
model6: doubao-seedance-1-5-pro-251215
model7: doubao-seedream-5-0-260128
model8: doubao-embedding-vision-251215
model9: kimi-k2-250905
model10: glm-4-7-251222
model11: deepseek-v3-2-251201
model12: minimax-m2.7
'''

with open('/path/to/config/file', 'w') as f:
    f.write(config_content)

subprocess.run(['exec', 'cat', '/path/to/config/file'])