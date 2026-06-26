#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
首次配置工具
- 交互式输入 COS 桶名、Region、SecretId、SecretKey 等
- 通过 COS SDK 验证桶连通性
- 加密保存所有配置到文件
"""

import sys
import os
import getpass

# 将脚本所在目录加入 Python 路径
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

from config import (
    save_cos_config,
    load_cos_config,
    ENCRYPTED_CONFIG_FILE,
    STORAGE_CLASS_OPTIONS,
    DEFAULT_STORAGE_CLASS,
)


def _validate_bucket_name(bucket):
    """
    校验桶名格式
    腾讯云 COS 桶名格式：<自定义名称>-<APPID>
    """
    if not bucket:
        return False, "桶名不能为空"
    if '-' not in bucket:
        return False, "桶名格式不正确，应为 <名称>-<APPID>（如 my-bucket-1250000000）"
    parts = bucket.rsplit('-', 1)
    if not parts[1].isdigit():
        return False, "桶名末尾的 APPID 应为纯数字（如 my-bucket-1250000000）"
    return True, ""


def _validate_region(region):
    """校验 Region 格式"""
    if not region:
        return False, "Region 不能为空"
    if not region.startswith("ap-"):
        return False, "Region 格式不正确，应以 'ap-' 开头（如 ap-guangzhou、ap-beijing）"
    return True, ""


def _verify_cos_connection(config_data):
    """
    通过 COS SDK 验证桶连通性

    Args:
        config_data: 完整的配置字典

    Returns:
        tuple: (success, message)
    """
    try:
        from qcloud_cos import CosConfig, CosS3Client

        region = config_data["region"]
        use_internal = config_data.get("use_internal", True)

        cos_config = CosConfig(
            Region=region,
            SecretId=config_data["secret_id"],
            SecretKey=config_data["secret_key"],
            Scheme='https',
            EnableInternalDomain=use_internal,  # SDK 自动处理内网/外网域名
        )
        client = CosS3Client(cos_config)

        # 尝试 head_bucket 验证桶是否存在且有权限
        client.head_bucket(Bucket=config_data["bucket"])
        return True, "桶连通性验证成功"

    except ImportError:
        return False, "cos-python-sdk-v5 未安装，跳过连通性验证"
    except Exception as e:
        error_str = str(e)
        if "NoSuchBucket" in error_str:
            return False, f"桶 {config_data['bucket']} 不存在，请检查桶名和 Region"
        elif "AccessDenied" in error_str:
            return False, "访问被拒绝，请检查 SecretId/SecretKey 权限"
        elif "ConnectTimeout" in error_str or "ConnectionError" in error_str:
            if use_internal:
                return False, "内网连接超时，请确认服务器在腾讯云内网环境中"
            else:
                return False, "连接超时，请检查网络"
        else:
            return False, f"验证失败: {error_str}"


def setup():
    """交互式配置 COS 全部参数"""
    print("=" * 56)
    print("  腾讯云 COS 配置工具（桶信息 + 密钥 一站式配置）")
    print("=" * 56)
    print()

    # 检查是否已有配置
    if os.path.exists(ENCRYPTED_CONFIG_FILE):
        print("⚠️  检测到已有加密配置文件")
        confirm = input("是否覆盖？(y/N): ").strip().lower()
        if confirm != 'y':
            print("已取消")
            return

    # ==================== 第一步：COS 桶信息 ====================
    print()
    print("━" * 56)
    print("  📦 第一步：COS 桶信息")
    print("━" * 56)
    print()
    print("  💡 提示：桶名和 Region 可在 COS 控制台查看")
    print("     https://console.cloud.tencent.com/cos/bucket")
    print()

    # 桶名
    while True:
        bucket = input("  请输入 COS 桶名（如 my-bucket-1250000000）: ").strip()
        valid, msg = _validate_bucket_name(bucket)
        if valid:
            break
        print(f"  ❌ {msg}")

    # Region
    print()
    print("  常用 Region：")
    print("    ap-guangzhou（广州）  ap-beijing（北京）  ap-shanghai（上海）")
    print("    ap-chengdu（成都）    ap-chongqing（重庆）ap-nanjing（南京）")
    print("    ap-hongkong（香港）   ap-singapore（新加坡）")
    print()
    while True:
        region = input("  请输入 COS Region（如 ap-guangzhou）: ").strip()
        valid, msg = _validate_region(region)
        if valid:
            break
        print(f"  ❌ {msg}")

    # 存储类型
    print()
    print("  存储类型选择：")
    for key, (cls, desc) in STORAGE_CLASS_OPTIONS.items():
        marker = " 👈 推荐" if cls == DEFAULT_STORAGE_CLASS else ""
        print(f"    {key}. {desc}{marker}")
    print()
    while True:
        storage_choice = input(f"  请选择存储类型 [1/2/3]（默认 2-低频存储）: ").strip()
        if not storage_choice:
            storage_choice = "2"
        if storage_choice in STORAGE_CLASS_OPTIONS:
            storage_class = STORAGE_CLASS_OPTIONS[storage_choice][0]
            storage_desc = STORAGE_CLASS_OPTIONS[storage_choice][1]
            break
        print("  ❌ 请输入 1、2 或 3")

    # 网络模式
    print()
    print("  网络模式：")
    print("    1. 内网上传（服务器在腾讯云同区域内网，免流量费，推荐）")
    print("    2. 外网上传（服务器不在腾讯云内网）")
    print()
    while True:
        net_choice = input("  请选择网络模式 [1/2]（默认 1-内网）: ").strip()
        if not net_choice:
            net_choice = "1"
        if net_choice in ("1", "2"):
            use_internal = (net_choice == "1")
            break
        print("  ❌ 请输入 1 或 2")

    # ==================== 第二步：API 密钥 ====================
    print()
    print("━" * 56)
    print("  🔑 第二步：腾讯云 API 密钥")
    print("━" * 56)
    print()
    print("  💡 提示：建议使用子账号密钥，仅授予 COS 读写权限")
    print("     https://console.cloud.tencent.com/cam/capi")
    print()

    secret_id = input("  请输入 SecretId: ").strip()
    if not secret_id:
        print("  ❌ SecretId 不能为空")
        sys.exit(1)

    secret_key = getpass.getpass("  请输入 SecretKey（输入不可见）: ").strip()
    if not secret_key:
        print("  ❌ SecretKey 不能为空")
        sys.exit(1)

    # ==================== 第三步：确认配置 ====================
    print()
    print("━" * 56)
    print("  📋 第三步：确认配置信息")
    print("━" * 56)
    print()
    print(f"  桶名称:     {bucket}")
    print(f"  Region:     {region}")
    print(f"  存储类型:   {storage_desc}")
    print(f"  网络模式:   {'内网上传' if use_internal else '外网上传'}")
    # 对 SecretId 做脱敏显示
    if len(secret_id) > 10:
        masked_id = f"{secret_id[:6]}...{secret_id[-4:]}"
    else:
        masked_id = f"{secret_id[:2]}****"
    print(f"  SecretId:   {masked_id}")
    print(f"  SecretKey:  ****（已隐藏）")
    print()

    confirm = input("  以上信息是否正确？(Y/n): ").strip().lower()
    if confirm == 'n':
        print("  已取消，请重新运行配置工具")
        sys.exit(0)

    # ==================== 第四步：保存并验证 ====================
    print()
    print("━" * 56)
    print("  💾 第四步：保存并验证")
    print("━" * 56)
    print()

    # 构建配置数据
    config_data = {
        "secret_id": secret_id,
        "secret_key": secret_key,
        "bucket": bucket,
        "region": region,
        "storage_class": storage_class,
        "use_internal": use_internal,
    }

    # 保存加密配置
    print("  正在加密保存配置...")
    save_cos_config(config_data)

    # 验证配置是否可以正常读取
    print("  正在验证配置文件读取...")
    try:
        loaded_config = load_cos_config()
        if (loaded_config["secret_id"] == secret_id and
                loaded_config["secret_key"] == secret_key and
                loaded_config["bucket"] == bucket and
                loaded_config["region"] == region):
            print("  ✅ 配置文件读取验证成功")
        else:
            print("  ❌ 配置验证失败：读取的配置与输入不一致")
            sys.exit(1)
    except Exception as e:
        print(f"  ❌ 配置验证失败: {e}")
        sys.exit(1)

    # 验证 COS 桶连通性
    print("  正在验证 COS 桶连通性...")
    success, message = _verify_cos_connection(config_data)
    if success:
        print(f"  ✅ {message}")
    else:
        print(f"  ⚠️  {message}")
        print("  （配置已保存，但连通性验证未通过，请检查后重试）")

    # ==================== 完成 ====================
    print()
    print("━" * 56)
    print("  🎉 配置完成！")
    print("━" * 56)
    print()
    print(f"  加密配置文件: {ENCRYPTED_CONFIG_FILE}")
    print()
    print("  现在可以通过以下方式测试上传：")
    print(f"    ./run.sh --file /path/to/test.jpg")
    print()


if __name__ == "__main__":
    setup()
