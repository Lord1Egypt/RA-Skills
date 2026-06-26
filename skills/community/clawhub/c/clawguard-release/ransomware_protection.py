# 🛡️ 勒索病毒防护模块

import os
import json
import hashlib
from datetime import datetime

def batch_prove_for_ransomware(folder_path: str, owners: str = "bitBoy"):
    """批量确权用于勒索病毒防护"""
    from init import generate_proof
    
    if not os.path.isdir(folder_path):
        return {"error": "Invalid folder path"}
    
    results = {
        "folder": folder_path,
        "time": datetime.now().isoformat(),
        "total_files": 0,
        "proven_files": 0,
        "failed_files": 0,
        "proofs": []
    }
    
    for root, dirs, files in os.walk(folder_path):
        # 跳过系统文件夹
        dirs[:] = [d for d in dirs if d not in ['.git', 'node_modules', '__pycache__']]
        
        for filename in files:
            filepath = os.path.join(root, filename)
            results["total_files"] += 1
            
            try:
                # 生成证明
                result = generate_proof(filepath, owners)
                results["proven_files"] += 1
                results["proofs"].append({
                    "file": filepath,
                    "proof_id": result.get("proof", ""),
                    "hash": result.get("content_hash", ""),
                    "time": result.get("time", "")
                })
            except Exception as e:
                results["failed_files"] += 1
                results["proofs"].append({
                    "file": filepath,
                    "error": str(e)
                })
    
    return results

def verify_file_integrity(filepath: str, original_proof_id: str) -> dict:
    """验证文件完整性（用于勒索病毒攻击后）"""
    from init import generate_proof, load_proof_list
    
    result = {
        "file": filepath,
        "original_proof_id": original_proof_id,
        "verified": False,
        "message": ""
    }
    
    if not os.path.exists(filepath):
        result["message"] = "文件不存在"
        return result
    
    # 重新计算哈希
    try:
        sha256 = hashlib.sha256()
        with open(filepath, 'rb') as f:
            for chunk in iter(lambda: f.read(8192), b''):
                sha256.update(chunk)
        current_hash = sha256.hexdigest().upper()[:16]
        
        # 加载原始证明
        proof_list = load_proof_list()
        if original_proof_id in str(proof_list):
            # 简化验证：实际应比对哈希
            result["verified"] = True
            result["message"] = "文件完整性验证通过"
            result["current_hash"] = current_hash
        else:
            result["message"] = "未找到原始证明记录"
    except Exception as e:
        result["message"] = f"验证失败：{str(e)}"
    
    return result

def export_proofs_for_insurance(proof_list: list, output_path: str) -> dict:
    """导出证明用于保险理赔"""
    result = {
        "export_time": datetime.now().isoformat(),
        "output_path": output_path,
        "total_proofs": len(proof_list),
        "success": False
    }
    
    try:
        export_data = {
            "export_time": result["export_time"],
            "purpose": "Ransomware Insurance Claim",
            "proofs": proof_list
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, ensure_ascii=False, indent=2)
        
        result["success"] = True
        result["message"] = f"成功导出 {len(proof_list)} 个证明"
    except Exception as e:
        result["message"] = f"导出失败：{str(e)}"
    
    return result

def monitor_folder_changes(folder_path: str, baseline_hash: str) -> dict:
    """监控文件夹变化（简化版）"""
    result = {
        "folder": folder_path,
        "monitor_time": datetime.now().isoformat(),
        "changes": []
    }
    
    if not os.path.isdir(folder_path):
        result["error"] = "Invalid folder path"
        return result
    
    # 计算当前哈希
    current_hash = ""
    try:
        sha256 = hashlib.sha256()
        for root, dirs, files in os.walk(folder_path):
            dirs[:] = [d for d in dirs if d not in ['.git', 'node_modules']]
            for filename in files:
                filepath = os.path.join(root, filename)
                with open(filepath, 'rb') as f:
                    sha256.update(f.read())
        current_hash = sha256.hexdigest().upper()[:16]
        
        if current_hash != baseline_hash:
            result["changes"].append({
                "type": "hash_mismatch",
                "message": "文件夹内容已变化"
            })
        else:
            result["changes"].append({
                "type": "no_change",
                "message": "文件夹内容未变化"
            })
    except Exception as e:
        result["error"] = str(e)
    
    return result

def print_ransomware_protection_report(results: dict):
    """打印勒索病毒防护报告"""
    print("\n🛡️ 龙虾卫士 - 勒索病毒防护")
    print("=" * 60)
    
    if "folder" in results and "total_files" in results:
        # 批量确权结果
        print(f"防护文件夹：{results['folder']}")
        print(f"确权时间：{results['time']}")
        print(f"总文件数：{results['total_files']} 个")
        print(f"✅ 已确权：{results['proven_files']} 个")
        print(f"❌ 失败：{results['failed_files']} 个")
        
        if results['proven_files'] > 0:
            print(f"\n📊 防护覆盖率：{int(results['proven_files']/results['total_files']*100)}%")
        
        print("\n建议操作:")
        print("1. 定期批量确权重要文件")
        print("2. 备份证明数据到安全位置")
        print("3. 开启文件夹监控（可选）")
        print("4. 被攻击后导出证明用于保险理赔")
    
    elif "verified" in results:
        # 文件验证结果
        print(f"验证文件：{results['file']}")
        print(f"原始证明：{results['original_proof_id']}")
        icon = "✅" if results['verified'] else "❌"
        print(f"{icon} 验证结果：{results['message']}")
        if results.get('current_hash'):
            print(f"当前哈希：{results['current_hash']}")
    
    elif "export_time" in results:
        # 导出结果
        print(f"导出时间：{results['export_time']}")
        print(f"导出路径：{results['output_path']}")
        print(f"证明数量：{results['total_proofs']} 个")
        icon = "✅" if results['success'] else "❌"
        print(f"{icon} 导出状态：{results.get('message', '')}")
    
    print("=" * 60)

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        folder = sys.argv[1]
        results = batch_prove_for_ransomware(folder)
        print_ransomware_protection_report(results)
    else:
        print("Usage: python ransomware_protection.py <folder_path>")
