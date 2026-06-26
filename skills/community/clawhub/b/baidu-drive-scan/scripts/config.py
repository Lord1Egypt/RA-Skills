import os

class Config:
    # 接口基础地址
    API_BASE = "https://pan.baidu.com/apaas/scan/filter"

    # 鉴权
    BDPAN_SPACE_TOKEN = os.getenv("BDPAN_API_KEY")

    # 默认配置
    DEFAULT_TIMEOUT = 60
    MODE_BASE64 = 1
    MODE_NETDISK = 2
    DEFAULT_DIR = "/apps/bdpan-scan"
    DEFAULT_FILENAME = "output.png"
