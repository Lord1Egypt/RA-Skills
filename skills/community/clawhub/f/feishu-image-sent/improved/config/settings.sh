# 飞书图片发送配置
# 图片大小阈值配置（单位：MB）

# 最大文件大小限制，超过此大小的图片将进行压缩
MAX_SIZE_MB=10

# 开始压缩的大小阈值，小于此大小的图片直接发送
COMPRESS_SIZE_MB=5

# JPEG压缩质量（1-100），数值越高质量越好，文件越大
COMPRESS_QUALITY=85

# 是否保留原图发送，true表示大图片同时发送原图，false表示只发送压缩版
KEEP_ORIGINAL=true

# 工作空间目录
WORKSPACE_DIR="/Users/bornforthis/.openclaw/workspace"

# 临时文件目录
TEMP_DIR="/tmp"

# 日志级别（0: 无日志, 1: 基本日志, 2: 详细日志）
LOG_LEVEL=1

# 支持的图片格式
SUPPORTED_FORMATS="png,jpg,jpeg,gif,webp,bmp,tiff"

# 压缩格式（输出格式）
OUTPUT_FORMAT="jpg"