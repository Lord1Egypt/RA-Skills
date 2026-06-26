#!/usr/bin/env python3
"""
法大大电子签 - 批量发送示例

适用于HR批量发送劳动合同、销售批量发送客户合同等场景
"""

import json
from pathlib import Path
from fadada_esign import FaDaDaClient, Signer

# 配置信息
CONFIG = {
    "app_id": "your_app_id",
    "app_secret": "your_app_secret",
    "open_corp_id": "your_open_corp_id"
}


def batch_send_from_list(contract_file: str, signers_list: list, output_file: str = None):
    """
    批量发送合同
    
    Args:
        contract_file: 合同文件路径
        signers_list: 签署人列表 [{"name": "张三", "mobile": "13800138000"}, ...]
        output_file: 结果输出文件（可选）
    """
    client = FaDaDaClient(**CONFIG)
    
    results = []
    
    for idx, signer_info in enumerate(signers_list, 1):
        print(f"[{idx}/{len(signers_list)}] 发送给 {signer_info['name']}...")
        
        try:
            result = client.send_to_single_signer(
                file_path=contract_file,
                signer_name=signer_info['name'],
                signer_mobile=signer_info['mobile'],
                task_subject=f"劳动合同-{signer_info['name']}"
            )
            
            results.append({
                "name": signer_info['name'],
                "mobile": signer_info['mobile'],
                "status": "success",
                "sign_task_id": result['sign_task_id'],
                "sign_url": result['sign_url']
            })
            
            print(f"   ✅ 成功 - Task ID: {result['sign_task_id']}")
            
        except Exception as e:
            results.append({
                "name": signer_info['name'],
                "mobile": signer_info['mobile'],
                "status": "failed",
                "error": str(e)
            })
            print(f"   ❌ 失败 - {e}")
    
    # 保存结果
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print(f"\n结果已保存到: {output_file}")
    
    # 统计
    success_count = sum(1 for r in results if r['status'] == 'success')
    print(f"\n发送完成: {success_count}/{len(signers_list)} 成功")
    
    return results


def batch_send_from_excel(contract_file: str, excel_file: str, output_file: str = None):
    """
    从Excel读取签署人信息并批量发送
    
    Excel格式：
    | 姓名 | 手机号 |
    | 张三 | 13800138000 |
    | 李四 | 13900139000 |
    """
    try:
        import pandas as pd
    except ImportError:
        print("请先安装 pandas: pip install pandas openpyxl")
        return
    
    # 读取Excel
    df = pd.read_excel(excel_file)
    
    # 解析签署人列表
    signers_list = []
    for _, row in df.iterrows():
        name = row.get('姓名') or row.get('Name') or row.get('name')
        mobile = row.get('手机号') or row.get('Mobile') or row.get('mobile')
        
        if pd.notna(name) and pd.notna(mobile):
            signers_list.append({
                'name': str(name).strip(),
                'mobile': str(mobile).strip()
            })
    
    print(f"从Excel读取到 {len(signers_list)} 个签署人")
    
    # 批量发送
    return batch_send_from_list(contract_file, signers_list, output_file)


def main():
    """主函数"""
    print("=" * 60)
    print("法大大电子签 - 批量发送工具")
    print("=" * 60)
    print()
    
    # 示例1：从列表批量发送
    signers = [
        {"name": "张三", "mobile": "13800138000"},
        {"name": "李四", "mobile": "13900139000"},
        {"name": "王五", "mobile": "13700137000"}
    ]
    
    # batch_send_from_list(
    #     contract_file="./劳动合同模板.pdf",
    #     signers_list=signers,
    #     output_file="./batch_results.json"
    # )
    
    # 示例2：从Excel批量发送
    # batch_send_from_excel(
    #     contract_file="./劳动合同模板.pdf",
    #     excel_file="./员工名单.xlsx",
    #     output_file="./batch_results.json"
    # )
    
    print("请根据实际需求修改配置和文件路径后运行")


if __name__ == "__main__":
    main()
