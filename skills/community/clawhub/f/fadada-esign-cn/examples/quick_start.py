#!/usr/bin/env python3
"""
法大大电子签 - 快速开始示例

最简单的使用方式：一键发送合同
"""

from fadada_esign import FaDaDaClient, Signer

# 配置信息（实际使用时建议从环境变量或配置文件读取）
CONFIG = {
    "app_id": "your_app_id",
    "app_secret": "your_app_secret",
    "open_corp_id": "your_open_corp_id"
}


def example_single_signer():
    """示例1：发送给单个签署人"""
    print("=" * 50)
    print("示例1：发送给单个签署人")
    print("=" * 50)
    
    # 创建客户端
    client = FaDaDaClient(**CONFIG)
    
    # 一键发送（最简单的方式）
    result = client.send_to_single_signer(
        file_path="./contract.pdf",
        signer_name="张三",
        signer_mobile="13800138000",
        task_subject="劳动合同签署"
    )
    
    print(f"✅ 任务创建成功！")
    print(f"任务 ID: {result['sign_task_id']}")
    print(f"签署链接: {result['sign_url']}")
    print()
    
    return result['sign_task_id']


def example_multiple_signers():
    """示例2：发送给多个签署人"""
    print("=" * 50)
    print("示例2：发送给多个签署人")
    print("=" * 50)
    
    client = FaDaDaClient(**CONFIG)
    
    # 创建多个签署人
    signers = [
        Signer(name="张三", mobile="13800138000", actor_id="signer1"),
        Signer(name="李四", mobile="13900139000", actor_id="signer2")
    ]
    
    # 发送合同
    result = client.send_document(
        file_path="./contract.pdf",
        signers=signers,
        task_subject="多方合作协议"
    )
    
    print(f"✅ 任务创建成功！")
    print(f"任务 ID: {result['sign_task_id']}")
    print(f"签署链接（第一个签署人）: {result['sign_url']}")
    print()
    
    return result['sign_task_id']


def example_step_by_step():
    """示例3：分步操作（更灵活的控制）"""
    print("=" * 50)
    print("示例3：分步操作")
    print("=" * 50)
    
    client = FaDaDaClient(**CONFIG)
    
    # 步骤1：上传文件
    print("1. 上传文件...")
    file_id = client.upload_file("./contract.pdf")
    print(f"   File ID: {file_id}")
    
    # 步骤2：创建签署任务
    print("2. 创建签署任务...")
    signer = Signer(name="张三", mobile="13800138000")
    sign_task_id = client.create_sign_task(
        task_subject="分步操作示例",
        file_id=file_id,
        signers=[signer]
    )
    print(f"   Task ID: {sign_task_id}")
    
    # 步骤3：获取签署链接
    print("3. 获取签署链接...")
    sign_url = client.get_sign_url(sign_task_id)
    print(f"   Sign URL: {sign_url}")
    
    print("✅ 完成！")
    print()
    
    return sign_task_id


def example_query_and_download():
    """示例4：查询状态和下载"""
    print("=" * 50)
    print("示例4：查询状态和下载")
    print("=" * 50)
    
    client = FaDaDaClient(**CONFIG)
    
    # 假设已知任务ID
    sign_task_id = "your_task_id"
    
    # 查询任务详情
    print("1. 查询任务详情...")
    detail = client.query_task_detail(sign_task_id)
    print(f"   状态: {detail.get('signTaskStatus')}")
    print(f"   主题: {detail.get('signTaskSubject')}")
    
    # 如果已完成，获取下载链接
    if detail.get('signTaskStatus') == 'finished':
        print("2. 获取下载链接...")
        download_url = client.get_download_url(sign_task_id)
        print(f"   下载链接: {download_url}")
    
    print()


if __name__ == "__main__":
    print("法大大电子签 - 快速开始示例")
    print()
    
    # 运行示例（请根据实际情况取消注释）
    # example_single_signer()
    # example_multiple_signers()
    # example_step_by_step()
    # example_query_and_download()
    
    print("请根据实际需求修改 CONFIG 和文件路径后运行示例")
