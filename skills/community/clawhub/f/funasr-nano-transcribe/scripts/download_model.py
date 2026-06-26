#!/usr/bin/env python3
"""
Fun-ASR-Nano-2512 模型下载/复制脚本
支持从 ModelScope、HuggingFace 下载或本地复制
"""

import os
import sys
import argparse
import shutil
from pathlib import Path
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def copy_local_model(source_dir: str, output_dir: str):
    """
    从本地目录复制模型文件
    
    Args:
        source_dir: 源模型目录
        output_dir: 目标目录（会自动创建 Fun-ASR-Nano-2512 子目录）
    """
    source_path = Path(source_dir)
    
    # 在输出目录下创建 Fun-ASR-Nano-2512 子目录
    output_path = Path(output_dir) / "Fun-ASR-Nano-2512"
    
    if not source_path.exists():
        logger.error(f"❌ 源目录不存在: {source_path}")
        sys.exit(1)
    
    logger.info(f"📂 从本地复制模型")
    logger.info(f"   源: {source_path}")
    logger.info(f"   目标: {output_path}")
    
    # 创建目标目录
    output_path.mkdir(parents=True, exist_ok=True)
    
    # 复制文件
    copied_files = []
    total_size = 0
    
    for item in source_path.rglob("*"):
        if item.is_file():
            # 计算相对路径
            rel_path = item.relative_to(source_path)
            target_file = output_path / rel_path
            
            # 创建父目录
            target_file.parent.mkdir(parents=True, exist_ok=True)
            
            # 复制文件
            shutil.copy2(item, target_file)
            
            size = item.stat().st_size
            total_size += size
            copied_files.append((rel_path, size))
    
    logger.info(f"✅ 复制完成！共 {len(copied_files)} 个文件")
    logger.info(f"📊 总大小: {total_size / (1024**3):.2f} GB")
    
    # 清理临时文件夹（如 ._____temp）
    _cleanup_temp_dirs(output_path)
    
    return output_path

def _cleanup_temp_dirs(directory: Path):
    """清理临时文件夹"""
    temp_dirs = []
    for item in directory.rglob("*"):
        if item.is_dir() and item.name.startswith(".") and "temp" in item.name.lower():
            temp_dirs.append(item)
    
    for temp_dir in temp_dirs:
        try:
            # 检查是否为空文件夹
            if temp_dir.exists() and not any(temp_dir.iterdir()):
                temp_dir.rmdir()
                logger.info(f"🧹 清理临时文件夹: {temp_dir.name}")
        except Exception as e:
            logger.warning(f"⚠️ 无法删除临时文件夹 {temp_dir}: {e}")

def download_from_modelscope(model_id: str, output_dir: str, cache_dir: str = None):
    """从 ModelScope 下载模型"""
    try:
        from modelscope import snapshot_download
    except ImportError:
        logger.error("❌ 请先安装 modelscope: pip install modelscope")
        sys.exit(1)
    
    if cache_dir is None:
        cache_dir = Path.home() / ".cache" / "modelscope"
    
    # 自动创建 Fun-ASR-Nano-2512 子目录
    output_path = Path(output_dir) / "Fun-ASR-Nano-2512"
    output_path.mkdir(parents=True, exist_ok=True)
    
    logger.info(f"🚀 从 ModelScope 下载: {model_id}")
    logger.info(f"📁 输出目录: {output_path}")
    
    try:
        local_dir = snapshot_download(
            model_id,
            cache_dir=str(cache_dir),
            local_dir=str(output_path)
        )
        logger.info(f"✅ 下载完成: {local_dir}")
        return local_dir
    except Exception as e:
        logger.error(f"❌ 下载失败: {e}")
        raise

def check_model_exists(model_dir: str):
    """检查模型是否已存在且完整"""
    model_path = Path(model_dir)
    
    if not model_path.exists():
        return False, "目录不存在"
    
    # 检查关键文件
    required_files = ["model.pt", "config.yaml"]
    missing = []
    
    for f in required_files:
        if not (model_path / f).exists():
            missing.append(f)
    
    if missing:
        return False, f"缺少文件: {', '.join(missing)}"
    
    # 计算大小
    total_size = sum(f.stat().st_size for f in model_path.rglob("*") if f.is_file())
    size_gb = total_size / (1024 ** 3)
    
    return True, f"大小: {size_gb:.2f} GB"

def get_model_info(model_dir: str):
    """获取模型信息"""
    model_path = Path(model_dir)
    
    if not model_path.exists():
        return None
    
    info = {
        "path": str(model_path),
        "exists": True,
        "files": [],
        "total_size_gb": 0
    }
    
    total_size = 0
    for f in sorted(model_path.rglob("*")):
        if f.is_file():
            size = f.stat().st_size
            total_size += size
            size_mb = size / (1024 * 1024)
            info["files"].append({
                "name": str(f.relative_to(model_path)),
                "size_mb": round(size_mb, 2)
            })
    
    info["total_size_gb"] = round(total_size / (1024 ** 3), 2)
    info["file_count"] = len(info["files"])
    
    return info

def main():
    parser = argparse.ArgumentParser(
        description='下载/复制 Fun-ASR-Nano-2512 模型',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 下载到默认位置（models/Fun-ASR-Nano-2512）
  python download_model.py
  
  # 复制模型到指定目录（会自动创建 Fun-ASR-Nano-2512 子目录）
  python download_model.py --copy -o /path/to/parent_dir
  # 结果: /path/to/parent_dir/Fun-ASR-Nano-2512/
  
  # 检查模型是否完整
  python download_model.py --check
  
  # 查看模型信息
  python download_model.py --info
  
  # 从 ModelScope 下载（如果可用）
  python download_model.py --modelscope -o models/Fun-ASR-Nano-2512
"""
    )
    
    parser.add_argument(
        '--model-id',
        default='FunAudioLLM/Fun-ASR-Nano-2512',
        help='ModelScope 模型 ID（默认：FunAudioLLM/Fun-ASR-Nano-2512）'
    )
    parser.add_argument(
        '-o', '--output-dir',
        help='模型保存目录（默认：models/Fun-ASR-Nano-2512）'
    )
    parser.add_argument(
        '--source',
        help='源模型目录（用于 --copy）'
    )
    parser.add_argument(
        '--copy',
        action='store_true',
        help='从本地目录复制模型'
    )
    parser.add_argument(
        '--modelscope',
        action='store_true',
        help='从 ModelScope 下载'
    )
    parser.add_argument(
        '--check',
        action='store_true',
        help='检查模型是否完整'
    )
    parser.add_argument(
        '--info',
        action='store_true',
        help='显示模型详细信息'
    )
    parser.add_argument(
        '--force',
        action='store_true',
        help='强制重新复制/下载'
    )
    
    parser.add_argument(
        '--cleanup',
        action='store_true',
        help='清理模型目录中的临时文件夹'
    )
    
    args = parser.parse_args()
    
    # 确定脚本和技能目录
    script_dir = Path(__file__).parent
    skill_dir = script_dir.parent
    
    # 默认输出目录
    if args.output_dir:
        output_dir = args.output_dir
    else:
        output_dir = skill_dir / "models" / "Fun-ASR-Nano-2512"
    
    # 检查模式
    if args.check:
        exists, msg = check_model_exists(output_dir)
        if exists:
            print(f"✅ 模型完整")
            print(f"📂 位置: {output_dir}")
            print(f"📊 {msg}")
        else:
            print(f"❌ 模型不完整")
            print(f"📂 位置: {output_dir}")
            print(f"⚠️ {msg}")
        sys.exit(0 if exists else 1)
    
    # 信息模式
    if args.info:
        info = get_model_info(output_dir)
        if info:
            print(f"📊 模型信息")
            print(f"   路径: {info['path']}")
            print(f"   文件数: {info['file_count']}")
            print(f"   总大小: {info['total_size_gb']:.2f} GB")
            print(f"\n📋 文件列表:")
            for f in info['files'][:10]:  # 只显示前10个
                print(f"   - {f['name']}: {f['size_mb']:.1f} MB")
            if len(info['files']) > 10:
                print(f"   ... 还有 {len(info['files']) - 10} 个文件")
        else:
            print(f"❌ 模型不存在: {output_dir}")
        sys.exit(0)
    
    # 清理临时文件夹模式
    if args.cleanup:
        print(f"🧹 清理临时文件夹: {output_dir}")
        _cleanup_temp_dirs(Path(output_dir))
        print(f"✅ 清理完成")
        sys.exit(0)
    
    # 确定源目录（用于复制）
    if args.copy:
        if args.source:
            source_dir = args.source
        else:
            # 默认从 models 目录复制
            source_dir = skill_dir / "models" / "Fun-ASR-Nano-2512"
        
        # 检查源目录
        if not Path(source_dir).exists():
            logger.error(f"❌ 源目录不存在: {source_dir}")
            sys.exit(1)
        
        # 检查目标是否已存在
        exists, msg = check_model_exists(output_dir)
        if exists and not args.force:
            print(f"✅ 目标已存在（{msg}），跳过复制")
            print(f"💡 使用 --force 强制重新复制")
            sys.exit(0)
        
        # 执行复制
        copy_local_model(source_dir, output_dir)
    
    elif args.modelscope:
        # 从 ModelScope 下载
        try:
            download_from_modelscope(args.model_id, output_dir)
        except Exception as e:
            logger.error(f"❌ 下载失败: {e}")
            logger.info("💡 尝试使用本地模型: python download_model.py --copy")
            sys.exit(1)
    
    else:
        # 默认行为：检查本地模型
        exists, msg = check_model_exists(output_dir)
        if exists:
            print(f"✅ 本地模型已存在")
            print(f"📂 位置: {output_dir}")
            print(f"📊 {msg}")
            print(f"\n💡 如需复制到其他地方，使用: python download_model.py --copy -o <目标目录>")
        else:
            print(f"❌ 本地模型不存在")
            print(f"📂 预期位置: {output_dir}")
            print(f"⚠️ {msg}")
            print(f"\n💡 如需从其他位置复制，使用: python download_model.py --copy --source <源目录> -o <目标目录>")

if __name__ == '__main__':
    main()
