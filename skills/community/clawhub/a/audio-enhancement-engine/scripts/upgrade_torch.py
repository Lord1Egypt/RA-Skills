import os
import subprocess
import sys
import platform
from pathlib import Path
from logger_manager import LoggerManager
import ensure_package
ensure_package.pip("requests")
ensure_package.pip("tqdm","tqdm")
import requests
from tqdm import tqdm

# ==================== 下载配置 ====================
WHEELS_DIR = Path("./pytorch_wheels")
WHEELS_DIR.mkdir(exist_ok=True)

logger = LoggerManager.setup_logger(logger_name="universal-voice-cloner")

# ==================== 动态生成 wheel（支持 Windows / Linux + cu129） ====================

python_tag = f"cp{sys.version_info.major}{sys.version_info.minor}"

if platform.system() == "Windows":
    platform_tag = "win_amd64"
elif platform.system() == "Linux":
    platform_tag = "manylinux_2_28_x86_64"
else:
    raise RuntimeError(f"暂不支持的系统: {platform.system()}")

WHEELS = {
    "torch": {
        "url": f"https://download.pytorch.org/whl/cu129/torch-2.9.1%2Bcu129-{python_tag}-{python_tag}-{platform_tag}.whl",
        "filename": f"torch-2.9.1+cu129-{python_tag}-{python_tag}-{platform_tag}.whl"
    },
    "torchvision": {
        "url": f"https://download.pytorch.org/whl/cu129/torchvision-0.24.1%2Bcu129-{python_tag}-{python_tag}-{platform_tag}.whl",
        "filename": f"torchvision-0.24.1+cu129-{python_tag}-{python_tag}-{platform_tag}.whl"
    },
    "torchaudio": {
        "url": f"https://download.pytorch.org/whl/cu129/torchaudio-2.9.1%2Bcu129-{python_tag}-{python_tag}-{platform_tag}.whl",
        "filename": f"torchaudio-2.9.1+cu129-{python_tag}-{python_tag}-{platform_tag}.whl"
    }
}

def download_file(url, filename, desc):
    filepath = WHEELS_DIR / filename
    if filepath.exists():
        logger.info(f"✅ {desc} 已存在，跳过下载")
        return
    
    logger.info(f"正在下载 {desc}（约 2.5GB，总共需要耐心等待）...")
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    
    with open(filepath, "wb") as f, tqdm(
        total=total_size, 
        unit="B", 
        unit_scale=True, 
        unit_divisor=1024,
        desc=desc,
        ncols=100
    ) as bar:
        for chunk in response.iter_content(chunk_size=1024*1024):  # 1MB 块
            if chunk:
                f.write(chunk)
                bar.update(len(chunk))

def get_venv_pip() -> Path:
    """自动查找当前项目中的 venv/pip，支持任意深度的子文件夹（你的 universal-voice-cloner 结构也完美支持）"""
    
    # 1. 如果当前已经在 venv 中运行，直接使用当前 python 对应的 pip（最快最准）
    if hasattr(sys, "base_prefix") and sys.prefix != sys.base_prefix:
        return Path(sys.executable).parent / ("pip.exe" if sys.platform.startswith("win") else "pip")
    
    # 2. 不在 venv 时，自动往上查找项目里的 venv（支持你的多级目录结构）
    current = Path(__file__).resolve().parent   # 从当前脚本目录开始
    while current != current.parent:            # 一直往上直到根目录
        candidate = current / "venv"
        if candidate.is_dir():
            # 根据操作系统自动选择正确的 pip 路径
            pip_name = "pip.exe" if sys.platform.startswith("win") else "pip"
            pip_dir = "Scripts" if sys.platform.startswith("win") else "bin"
            pip_path = candidate / pip_dir / pip_name
            if pip_path.exists():
                return pip_path
        current = current.parent
    
    # 如果实在找不到，抛出明确错误
    raise FileNotFoundError(
        "❌ 找不到 venv 文件夹！\n"
        f"当前脚本路径: {Path(__file__).resolve()}\n"
        "请确认项目中存在 skills/venv 文件夹"
    )

def upgrade_torch():
    logger.info("=== PyTorch 2.11.0 CUDA 13.0 下载脚本（带真实进度条）===\n")
    logger.info(f"当前系统: {platform.system()} | Python: {sys.version_info.major}.{sys.version_info.minor} ({python_tag}) | 平台: {platform_tag}")
    
    for name, info in WHEELS.items():
        download_file(info["url"], info["filename"], name.capitalize())
    
    logger.info("\n✅ 全部下载完成！文件保存在 ./pytorch_wheels 文件夹")
    logger.info("\n现在开始本地安装（速度会快很多）...")

    #先卸载旧版本
    uninstall_old_torch()
    #修改 Python 进程的环境变量
    setup_cusparselt_env()
    setup_nvshmem_env()
    # 自动安装
    venv_pip = get_venv_pip()

    # 动态生成 wheel 路径
    wheel_paths = [str(WHEELS_DIR / info["filename"]) for info in WHEELS.values()]
    
    install_cmd = [
        str(venv_pip),
        "install",
        "--force-reinstall",
        "--no-deps",
        *wheel_paths
    ]
    
    logger.info("正在安装（这步通常很快）...")
    subprocess.run(install_cmd, check=True)
    
    # 验证（跨平台兼容）
    pip_str = str(venv_pip)
    if platform.system() == "Windows":
        python_exe = pip_str.replace("pip.exe", "python.exe")
    else:
        python_exe = pip_str.replace("pip", "python")   # Ubuntu venv 下 pip → python
    
    subprocess.run([python_exe, "-c", 
                   "import torch; print('✅ 成功！新版本:', torch.__version__); print('CUDA 可用:', torch.cuda.is_available())"])
    
    logger.info("\n🎉 全部完成！现在可以关闭这个窗口了。")

def setup_cusparselt_env():
    """
    查找 libcusparseLt.so 并将其目录加入 LD_LIBRARY_PATH，
    保证 PyTorch GPU 可以找到库。
    """
    try:
        # 查找 libcusparseLt.so 文件
        result = subprocess.run(
            ['find', '/usr/local', '-name', 'libcusparseLt.so*'],
            capture_output=True, text=True, check=True
        )
        paths = result.stdout.strip().split('\n')
        if not paths or paths == ['']:
            logger.info("⚠️ 未找到 libcusparseLt.so 文件")
            return False
        # 取第一个路径
        lib_dir = os.path.dirname(paths[0])
        logger.info(f"✅ 找到库目录: {lib_dir}")
        # 更新 LD_LIBRARY_PATH
        ld_path = os.environ.get("LD_LIBRARY_PATH", "")
        if lib_dir not in ld_path:
            os.environ["LD_LIBRARY_PATH"] = f"{lib_dir}:{ld_path}"
            logger.info(f"✅ 更新 LD_LIBRARY_PATH: {os.environ['LD_LIBRARY_PATH']}")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"❌ 查找库文件出错: {e}")
        return False

def setup_nvshmem_env():
    """
    查找 libnvshmem_host.so* 并加入 LD_LIBRARY_PATH，保证 PyTorch GPU 可以找到库
    """
    try:
        result = subprocess.run(
            ['find', '/usr/local', '-name', 'libnvshmem_host.so*'],
            capture_output=True, text=True, check=True
        )
        paths = result.stdout.strip().split('\n')
        if not paths or paths == ['']:
            logger.info("⚠️ 未找到 libnvshmem_host.so 文件")
            return False

        lib_dir = os.path.dirname(paths[0])
        logger.info(f"✅ 找到 NVSHMEM 库目录: {lib_dir}")

        ld_path = os.environ.get("LD_LIBRARY_PATH", "")
        if lib_dir not in ld_path:
            os.environ["LD_LIBRARY_PATH"] = f"{lib_dir}:{ld_path}"
            logger.info(f"✅ 更新 LD_LIBRARY_PATH: {os.environ['LD_LIBRARY_PATH']}")

        return True

    except subprocess.CalledProcessError as e:
        logger.error(f"❌ 查找 NVSHMEM 库文件出错: {e}")
        return False

def uninstall_old_torch():
    """在升级前彻底卸载旧版 torch 相关包（可被其他函数调用）"""
    logger.info("=== 开始卸载旧版 PyTorch 包（torch / torchvision / torchaudio）===")
    
    venv_pip = get_venv_pip()          # 使用你脚本里已有的函数，自动适配 ../venv/bin/pip
    
    uninstall_cmd = [
        str(venv_pip),
        "uninstall",
        "-y",                          # 自动确认，不询问
        "torch",
        "torchvision",
        "torchaudio"
    ]
    
    try:
        result = subprocess.run(uninstall_cmd, check=True, capture_output=True, text=True)
        logger.info("✅ 旧版 PyTorch 包已全部卸载")
        if result.stdout:
            logger.debug(result.stdout.strip())   # 如果想看详细输出可以打开
    except subprocess.CalledProcessError as e:
        # 包不存在时 pip 也会返回非0，但我们希望继续升级
        logger.warning("卸载时出现警告（可能是部分包本来就不存在），继续执行升级...")
        logger.debug(e.stderr.strip() if e.stderr else "无错误输出")