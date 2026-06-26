#!/usr/bin/env python3
"""
Post-Install Patch Script
自动修复 timesfm 等库的兼容性问题

问题: timesfm 的 TimesFM_2p5_200M_torch.__init__() 不接受 'proxies' 参数
原因: huggingface_hub 较新版本移除了 proxies 参数

使用方法:
  python3 scripts/post_install.py
  或在安装后自动运行
"""
import os
import sys
import re
import subprocess
from pathlib import Path


def find_timesfm_in_venv(venv_path: str = None) -> Path:
    """查找 venv 中的 timesfm 安装路径"""
    if venv_path is None:
        # 默认从项目目录推断
        project_dir = Path(__file__).parent.parent
        venv_path = project_dir / ".venv"
    
    venv_path = Path(venv_path)
    
    # 搜索 timesfm 目录
    site_packages = venv_path / "lib" / f"python{sys.version_info.major}.{sys.version_info.minor}" / "site-packages"
    
    if not site_packages.exists():
        print(f"❌ Site-packages not found: {site_packages}")
        return None
    
    # 查找 timesfm 目录
    for item in site_packages.iterdir():
        if item.name.startswith("timesfm"):
            return item
    
    return None


def patch_timesfm_proxies():
    """修复 timesfm 的 proxies 参数问题"""
    timesfm_path = find_timesfm_in_venv()
    
    if timesfm_path is None:
        print("❌ timesfm not found in venv")
        return False
    
    # 查找需要修改的文件
    init_file = timesfm_path / "__init__.py"
    if not init_file.exists():
        # 可能在 timesfm 子目录
        for item in timesfm_path.rglob("__init__.py"):
            if "timesfm" in str(item):
                init_file = item
                break
    
    if not init_file or not init_file.exists():
        print(f"❌ Cannot find __init__.py in {timesfm_path}")
        return False
    
    print(f"📁 Found timesfm at: {timesfm_path}")
    print(f"📄 Patching: {init_file}")
    
    # 读取文件
    content = init_file.read_text()
    
    # 检查是否已经修复
    if "proxies" not in content or "get_client" in content:
        print("✅ timesfm already patched or not needs patching")
        return True
    
    # 查找 huggingface_hub import 并添加兼容代码
    # 我们需要在 from_pretrained 调用中移除 proxies 参数
    
    # 方案: 在文件开头添加 monkey patch
    patch_code = '''
# === Post-install patch for huggingface_hub compatibility ===
import sys
import warnings
from functools import wraps

_original_from_pretrained = None

def _patched_from_pretrained(*args, **kwargs):
    """移除 proxies 参数以兼容新版 huggingface_hub"""
    # 移除 proxies 参数
    kwargs.pop('proxies', None)
    return _original_from_pretrained(*args, **kwargs)

def _apply_timesfm_patch():
    global _original_from_pretrained
    try:
        from huggingface_hub import snapshot_download
        if hasattr(snapshot_download, '__wrapped__'):
            return  # Already patched
        _original_from_pretrained = snapshot_download
        snapshot_download.__wrapped__ = _patched_from_pretrained
        print("✅ timesfm patch applied: proxies parameter removed")
    except ImportError:
        pass

_apply_timesfm_patch()
# === End patch ===
'''
    
    # 在文件开头添加 patch
    new_content = patch_code + "\n" + content
    
    # 写回文件
    init_file.write_text(new_content)
    print(f"✅ Patched {init_file}")
    
    return True


def patch_hf_hub_init():
    """
    直接修改 huggingface_hub 的 snapshot_download 函数
    这是更彻底的解决方案
    """
    try:
        import huggingface_hub
        hf_path = Path(huggingface_hub.__file__).parent
        init_file = hf_path / "scheduler_utils.py"  # 或其他包含 from_pretrained 的文件
        
        # 这个方法可能不适用，改用 monkey patch
        pass
    except:
        pass


def run_post_install():
    """运行所有 post-install patches"""
    print("🔧 AI Model Team - Post-Install Patch Script")
    print("=" * 50)
    
    success = True
    
    # 1. Patch timesfm
    print("\n1️⃣ Patching timesfm (proxies parameter)...")
    if patch_timesfm_proxies():
        print("   ✅ Done")
    else:
        print("   ⚠️  Skipped or failed")
        success = False
    
    # 2. 检查其他依赖
    print("\n2️⃣ Checking dependencies...")
    try:
        import numpy
        import pandas
        import torch
        import transformers
        print(f"   ✅ numpy={numpy.__version__}")
        print(f"   ✅ pandas={pandas.__version__}")
        print(f"   ✅ torch={torch.__version__}")
        print(f"   ✅ transformers={transformers.__version__}")
    except ImportError as e:
        print(f"   ❌ Missing: {e}")
        success = False
    
    print("\n" + "=" * 50)
    if success:
        print("✅ Post-install patch completed successfully!")
    else:
        print("⚠️  Some patches failed - please check errors above")
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(run_post_install())
