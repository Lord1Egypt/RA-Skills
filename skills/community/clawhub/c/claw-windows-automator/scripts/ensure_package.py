#!/usr/bin/env python3
# -*- coding: utf-8, -*-

"""
Skill Name: claw-windows-automator
Author: 王岷瑞/https://github.com/wangminrui2022
License: Apache License
Description: 智能的 Python 包安装工具函数，支持多种安装方式（普通包、指定版本、git 仓库、本地 zip 包等），并具备完善的已安装检测和失败回退机制
功能特点：
    支持 git+https:// 方式安装 GitHub 仓库
    支持本地 .zip 包作为回退方案（git 下载失败时自动尝试）
    加强版已安装检测（import + importlib.metadata 双重检查）
    支持强制重新安装（force=True）
    对 git+ 安装失败提供友好提示和本地 zip 回退，不轻易抛出异常
    自动区分是否使用清华镜像加速（git+ 和本地 zip 不使用镜像）
    
"""

import subprocess
import sys
import os
import importlib.metadata
from packaging import version as pkg_version
from logger_manager import LoggerManager
logger = LoggerManager.setup_logger(logger_name="claw-windows-automator")

def fix_setuptools_for_legacy_packages():
    """专门为老项目（使用 pkg_resources 的 setup.py）修复 setuptools 版本"""
    logger.info("🔧 正在修复 setuptools 版本（兼容旧 GitHub 包构建）...")
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install",
            "--quiet", "--force-reinstall", "setuptools<=81.2.0", "wheel"
        ])
        logger.info("✅ setuptools 已切换到兼容版本 (<=81.2.0)")
    except Exception as e:
        logger.info(f"⚠️ setuptools 修复失败: {e}（可忽略，继续尝试安装）")

# ==================== 在文件最开头调用 ====================
fix_setuptools_for_legacy_packages()
import pkg_resources  # 用于更鲁棒的版本比较
from config import SKILL_ROOT

"""
参数,类型,默认值,说明
spec,str,无,安装规格，支持普通包名、包==版本、git+https://...、本地.zip 等
import_name,str,None,用于 import 检查的名称。若不传则自动使用包名（git 包建议显式传入）
sub_import,str,None,需要检查的子模块（较少使用）
min_version,str,None,最低版本要求
force,bool,False,是否强制重新安装（忽略已安装版本）
fallback_zip,str,None,"当 git+ 安装失败时，用于回退的本地 zip 包路径（如 ""versatile_audio_super_resolution-main.zip""）"
"""
def pip(spec: str, 
        import_name: str = None, 
        sub_import: str = None, 
        min_version: str = None,
        force: bool = False,
        fallback_zip: str = None):
    """
    智能安装函数 - 加强版 import + metadata 双重检测
    """
    # 从 spec 中尝试提取包名（对 git+ 更友好）
    check_name = parse_spec(spec)[0] if hasattr(parse_spec, '__call__') else spec.split('/')[-1].replace('.git', '')
    
    if import_name is None:
        import_name = check_name

    # ==================== 强制安装直接跳过检查 ====================
    if force:
        logger.warning(f"🔄 强制安装 {spec} ...")
        _install_package(spec, check_name, fallback_zip)
        return

    # ==================== 加强版已安装检测 ====================
    installed = False
    installed_version = None

    # 第一步：尝试 import 检查（最快）
    try:
        parts = import_name.split('.')
        mod = __import__(parts[0])
        for part in parts[1:]:
            mod = getattr(mod, part)
        if sub_import:
            getattr(mod, sub_import)
        logger.debug(f"✅ 通过 import 检测到 {import_name} 已安装")
        installed = True
    except Exception:
        pass

    # 第二步：用 importlib.metadata / pkg_resources 更可靠地检查（推荐方式）
    if not installed:
        try:
            import importlib.metadata
            installed_version = importlib.metadata.version(check_name)
            installed = True
            logger.debug(f"✅ 通过 metadata 检测到 {check_name} 已安装，版本 {installed_version}")
        except (importlib.metadata.PackageNotFoundError, Exception):
            pass

    # 第三步：兼容旧的 get_installed_version 函数（如果你已有）
    if not installed and 'get_installed_version' in globals():
        installed_version = get_installed_version(check_name)
        if installed_version:
            installed = True
            logger.debug(f"✅ 通过 get_installed_version 检测到 {check_name} 已安装")

    # 第四步：判断是否需要安装
    need_install = not installed

    # 如果有版本要求，再额外判断（git+ 包通常没有固定版本，这里可根据需要调整）
    if installed and (min_version or parse_spec(spec)[1]):
        target_ver = min_version or parse_spec(spec)[1]
        if not is_version_satisfied(installed_version, target_ver):
            logger.info(f"📦 {check_name} 当前版本 {installed_version}，需要升级到 {target_ver}")
            need_install = True

    if not need_install:
        logger.info(f"✅ {spec} 已满足要求，跳过安装")
        return

    # 执行安装
    _install_package(spec, check_name, fallback_zip)


def _install_package(spec: str, check_name: str, fallback_zip: str = None):
    """实际执行安装的内部函数（新增 git+ 失败 fallback 支持）"""
    logger.warning(f"🔧 正在安装 {spec} ...（首次运行会较慢）")
    
    cmd = [
        sys.executable, "-m", "pip", "install",
        "--upgrade",
        spec,
        "--quiet"
    ]
    
    # git+、http、zip 等特殊安装方式不使用清华镜像，避免冲突
    # if any(keyword in spec for keyword in ["git+", "://", ".zip", ".whl"]):
    #     cmd = [c for c in cmd if c != "-i" and not str(c).startswith("https://pypi.tuna")]
    # else:
    #     cmd.extend(["-i", "https://pypi.tuna.tsinghua.edu.cn/simple"])

    # git+、http、.zip、.whl 等特殊安装方式不使用清华镜像，避免源冲突或构建问题
    if any(keyword in spec.lower() for keyword in ["git+", "://", ".zip", ".whl"]):
        # 过滤掉所有 -i 和 tuna 镜像参数
        cmd = [c for c in cmd if c != "-i" and not str(c).startswith("https://pypi.tuna")]
        
        # 额外建议：为这类包添加常见构建修复参数（强烈推荐加上）
        extra_flags = ["--no-build-isolation", "--no-deps", "--use-pep517"]
        # 插入到合适位置（通常在 install 之后）
        try:
            install_idx = cmd.index("install")
            cmd[install_idx+1:install_idx+1] = extra_flags
        except ValueError:
            cmd.extend(extra_flags)
    else:
        # 普通包使用清华镜像加速
        cmd.extend(["-i", "https://pypi.tuna.tsinghua.edu.cn/simple"])

    try:
        subprocess.check_call(cmd)
        logger.info(f"✅ {spec} 安装/升级完成！")
        
    except subprocess.CalledProcessError as e:
        logger.error(f"❌ 安装 {spec} 失败！错误信息：{e}")
        # === git+ 失败后的回退逻辑 ===
        if fallback_zip and "git+" in spec:
            if os.path.exists(fallback_zip):
                logger.warning(f"⚠️ 尝试使用本地回退包: {fallback_zip}")
                try:
                    cmd_fallback = [
                        sys.executable, "-m", "pip", "install",
                        "--upgrade", fallback_zip, "--quiet"
                    ]
                    subprocess.check_call(cmd_fallback)
                    logger.info(f"✅ 使用本地包 {fallback_zip} 安装成功！")
                    return
                except subprocess.CalledProcessError as e2:
                    logger.error(f"❌ 本地回退包安装也失败！")
                    # 这里可以选择继续抛出或不抛出，根据你的需求
                    raise
            else:
                logger.warning(f"⚠️ 本地回退包不存在: {fallback_zip}")
                logger.warning(f"💡 请将 {fallback_zip}  放到 {SKILL_ROOT} 目录，重新启动安装")
                # 【关键修改】：不抛出异常，让程序继续往下运行
                return
        
        # 如果不是 git+ 失败，或者没有设置 fallback_zip，才真正报错
        logger.error(f"❌ 安装 {spec} 最终失败！")
        raise        


def parse_spec(spec: str):
    """解析安装规格"""
    if "==" in spec:
        name, ver = spec.split("==", 1)
        return name.strip(), ver.strip()
    
    if spec.startswith("git+"):
        if "#egg=" in spec:
            name = spec.split("#egg=")[-1].split("&")[0]
        else:
            name = spec.rstrip("/").split("/")[-1].replace(".git", "")
            # 特殊处理常见包名
            name = name.replace("torchlibrosa-master", "torchlibrosa")
            name = name.replace("voicefixer-main", "voicefixer")
        return name, None
    
    if spec.endswith((".zip", ".whl")):
        name = spec.split("/")[-1].split("-")[0].split("_")[0]
        name = name.replace("master", "").replace("main", "")
        if "torchlibrosa" in name:
            name = "torchlibrosa"
        elif "voicefixer" in name:
            name = "voicefixer"
        return name.strip(), None
    
    return spec, None


def get_installed_version(package_name: str):
    """获取已安装版本（双保险）"""
    try:
        return importlib.metadata.version(package_name)
    except Exception:
        try:
            return pkg_resources.get_distribution(package_name).version
        except Exception:
            return None


def is_version_satisfied(installed_ver: str | None, required: str | None):
    """版本比较"""
    if not installed_ver or not required:
        return bool(installed_ver)
    
    try:
        installed = pkg_version.parse(installed_ver)
        
        if required.startswith("=="):
            req_ver = pkg_version.parse(required[2:].strip())
            return installed == req_ver
        else:
            # 默认视为最低版本要求
            req_ver = pkg_version.parse(required.lstrip(">="))
            return installed >= req_ver
    except Exception:
        return False
"""
一个轻量级的包安装函数，主要用于快速安装普通 PyPI 包并支持简单的版本约束（如 <2、>=1.26 等）。
"""
def pip_v(pkg: str, version: str = None):
    """
    智能安装函数，支持版本约束
    示例：
        pip_v("urllib3", version="<2")
        pip_v("numpy", version=">=1.26.0")
    """
    import_name = pkg   # 默认相同，可后续扩展传参

    # ==================== 1. 检查是否已安装 + 版本是否满足 ====================
    try:
        __import__(import_name)
        
        # 尝试获取当前版本
        try:
            import importlib.metadata
            current_version = importlib.metadata.version(pkg)
            
            if version and not is_version_satisfied(current_version, version):  # 需要你已有这个函数
                logger.info(f"📦 {pkg} 当前版本 {current_version}，不满足 {version}，准备重新安装...")
            else:
                logger.info(f"✅ {pkg} 已安装（版本 {current_version}），跳过")
                return
        except:
            logger.info(f"✅ {pkg} 已通过 import 检测，跳过安装")
            return
            
    except ImportError:
        logger.debug(f"{pkg} 未通过 import 检测，准备安装...")

    # ==================== 2. 执行安装 ====================
    install_str = pkg
    if version:
        install_str = f"{pkg}{version}"   # 正确拼接方式

    logger.warning(f"🔧 正在安装 {install_str} ...")

    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install",
            install_str,
            "-i", "https://pypi.tuna.tsinghua.edu.cn/simple",
            "--quiet"
        ])
        logger.info(f"✅ {pkg} 安装完成！")
        
    except subprocess.CalledProcessError as e:
        logger.error(f"❌ {pkg} 安装失败！")
        raise