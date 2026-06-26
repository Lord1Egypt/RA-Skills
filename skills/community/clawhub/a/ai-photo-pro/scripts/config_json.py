import json
import os
#  程序启动地址
ORGPATH = os.path.dirname(os.path.abspath(__file__))
os.chdir(ORGPATH)
config_file = "config.json"
a = input(
    "您需要配置API Key才能使用本工具。\n\n"
    "1. 配置NVID API Key\n"
    "2. 配置硅基流动API Key\n"
    "3. 退出\n"
    "请输入您的选择: 选择指定数字，其他输入退出程序"
)
config_data = {}
if os.path.exists(config_file):
    with open(config_file, "r") as f:
        config_data = json.load(f)

if a == "1":
    TOKEN_KEY = input("请输入您的NVID API Key: ")
    config_data["NVID"] = TOKEN_KEY
    with open(config_file, "w") as f:
        json.dump(config_data, f, indent=2)
    print("配置文件已创建")
elif a == "2":
    TOKEN_KEY = input("请输入您的硅基流动API Key: ")
    config_data["SILICONFLOW"] = TOKEN_KEY
    with open(config_file, "w") as f:
        json.dump(config_data, f, indent=2)
    print("配置文件已创建")
else:
    exit(1)