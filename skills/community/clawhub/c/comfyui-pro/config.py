# ComfyUI 配置 - 机械之神专用
# 最后更新：2026-03-15

# ComfyUI 服务器配置
COMFYUI_HOST = "127.0.0.1"
COMFYUI_PORT = 8000  # ComfyUI 桌面版默认端口
COMFYUI_URL = f"http://{COMFYUI_HOST}:{COMFYUI_PORT}"

# ComfyUI 安装路径
COMFYUI_BASE = "G:\\comfyui\\resources\\ComfyUI"
COMFYUI_PYTHON = "F:\\comcyui 模型\\.venv\\Scripts\\python.exe"

# 模型路径
MODELS_DIR = "F:\\comcyui 模型\\models"
OUTPUT_DIR = "F:\\comcyui 模型\\output"
INPUT_DIR = "F:\\comcyui 模型\\input"
USER_DIR = "F:\\comcyui 模型\\user"

# 预设模型
DEFAULT_MODEL = {
    "checkpoint": "z_image_turbo_bf16.safetensors",
    "clip": "qwen_3_4b.safetensors",
    "vae": "ae.safetensors",
    "controlnet": "Z-Image-Turbo-Fun-Controlnet-Union.safetensors"
}

# 默认参数
DEFAULT_PARAMS = {
    "width": 1024,
    "height": 1024,
    "steps": 4,
    "cfg": 1.0,
    "sampler": "res_multistep",
    "scheduler": "simple",
    "seed": -1  # 随机种子
}
