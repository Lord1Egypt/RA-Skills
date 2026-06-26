# 🔍 文件安全扫描模块

import os
import stat
from datetime import datetime, timedelta

# 风险文件扩展名定义
HIGH_RISK_EXTENSIONS = {
    '.exe', '.dll', '.com', '.scr', '.pif', '.msp', '.bat', '.cmd'
}

MEDIUM_RISK_EXTENSIONS = {
    '.ps1', '.vbs', '.js', '.jse', '.wsf', '.wsh', '.msi', '.jar'
}

MACRO_EXTENSIONS = {
    '.doc', '.docm', '.xls', '.xlsm', '.ppt', '.pptm', '.dotm', '.xltm'
}

SUSPICIOUS_EXTENSIONS = {
    '.lnk', '.hta', '.cpl', '.msc', '.diagcab'
}

# 大文件阈值 (100MB)
LARGE_FILE_THRESHOLD = 100 * 1024 * 1024

def load_proof_list(proof_list_path: str) -> dict:
    """加载确权文件列表"""
    if proof_list_path is None:
        proof_list_path = os.path.join(os.path.dirname(__file__), 'bh_data', 'proof_list.txt')
    
    proof_map = {}  # filename -> proof_id
    
    if os.path.exists(proof_list_path):
        try:
            with open(proof_list_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    # 跳过标题行
                    if line.startswith('BH_PROOF_LIST') or not line:
                        continue
                    # 解析格式：time | proof_id | type | time_source | owners | size
                    if '|' in line:
                        parts = [p.strip() for p in line.split('|')]
                        if len(parts) >= 3:
                            proof_id = parts[1].strip()
                            file_info = parts[2].strip()
                            # 提取文件名 (格式：file:filename 或直接文件名)
                            if file_info.startswith('file:'):
                                filename = file_info[5:]
                            else:
                                filename = file_info
                            proof_map[filename] = proof_id
        except Exception as e:
            pass
    
    return proof_map

def get_file_hash(filepath: str) -> str:
    """计算文件 SHA256 哈希"""
    import hashlib
    sha256 = hashlib.sha256()
    try:
        with open(filepath, 'rb') as f:
            for chunk in iter(lambda: f.read(8192), b''):
                sha256.update(chunk)
        return sha256.hexdigest().upper()[:16]  # 返回前 16 位
    except:
        return ""

def scan_files(folder_path: str, proof_list_path: str = None):
    """扫描文件夹中的可疑文件"""
    if not os.path.isdir(folder_path):
        return {"error": "Invalid folder path"}
    
    # 加载确权列表
    proof_list = load_proof_list(proof_list_path)
    
    results = {
        "scan_path": folder_path,
        "scan_time": datetime.now().isoformat(),
        "total_files": 0,
        "safe_files": 0,
        "proven_files": [],  # 已确权文件
        "high_risk": [],
        "medium_risk": [],
        "low_risk": [],
        "large_files": []
    }
    
    for root, dirs, files in os.walk(folder_path):
        # 跳过系统文件夹
        dirs[:] = [d for d in dirs if d not in ['.git', 'node_modules', '__pycache__', '.venv']]
        
        for filename in files:
            filepath = os.path.join(root, filename)
            ext = os.path.splitext(filename)[1].lower()
            
            results["total_files"] += 1
            
            try:
                file_size = os.path.getsize(filepath)
            except:
                file_size = 0
            
            # 检查是否已确权 (按文件名匹配)
            filename = os.path.basename(filepath)
            is_proven = filename in proof_list
            proof_id = proof_list.get(filename, "")
            
            # 已确权文件（可信）
            if is_proven:
                results["proven_files"].append({
                    "path": filepath,
                    "type": get_file_type(ext),
                    "size": format_size(file_size),
                    "proof_id": proof_id,
                    "status": "proven"
                })
                results["safe_files"] += 1
            # 高风险文件
            elif ext in HIGH_RISK_EXTENSIONS:
                results["high_risk"].append({
                    "path": filepath,
                    "type": get_file_type(ext),
                    "size": format_size(file_size),
                    "risk": "high"
                })
            
            # 中风险文件
            elif ext in MEDIUM_RISK_EXTENSIONS:
                results["medium_risk"].append({
                    "path": filepath,
                    "type": get_file_type(ext),
                    "size": format_size(file_size),
                    "risk": "medium"
                })
            
            # 宏文档
            elif ext in MACRO_EXTENSIONS:
                results["medium_risk"].append({
                    "path": filepath,
                    "type": "Macro Document",
                    "size": format_size(file_size),
                    "risk": "medium"
                })
            
            # 可疑扩展名
            elif ext in SUSPICIOUS_EXTENSIONS:
                results["low_risk"].append({
                    "path": filepath,
                    "type": get_file_type(ext),
                    "size": format_size(file_size),
                    "risk": "low"
                })
            
            # 大文件
            elif file_size > LARGE_FILE_THRESHOLD:
                results["large_files"].append({
                    "path": filepath,
                    "size": format_size(file_size),
                    "type": "Large File"
                })
            
            else:
                results["safe_files"] += 1
    
    return results

def get_file_type(ext: str) -> str:
    """获取文件类型描述"""
    type_map = {
        '.exe': 'Executable',
        '.dll': 'Dynamic Library',
        '.com': 'Command File',
        '.scr': 'Screen Saver',
        '.pif': 'Program Information',
        '.msp': 'Windows Installer Patch',
        '.bat': 'Batch File',
        '.cmd': 'Command Script',
        '.ps1': 'PowerShell Script',
        '.vbs': 'VBScript',
        '.js': 'JavaScript',
        '.jse': 'JScript Encoded',
        '.wsf': 'Windows Script File',
        '.wsh': 'Windows Script Host',
        '.msi': 'Windows Installer',
        '.jar': 'Java Archive',
        '.doc': 'Word Document',
        '.docm': 'Word Macro-Enabled',
        '.xls': 'Excel Spreadsheet',
        '.xlsm': 'Excel Macro-Enabled',
        '.ppt': 'PowerPoint Presentation',
        '.pptm': 'PowerPoint Macro-Enabled',
        '.lnk': 'Shortcut',
        '.hta': 'HTML Application',
        '.cpl': 'Control Panel',
        '.msc': 'Microsoft Management Console'
    }
    return type_map.get(ext, f'{ext.upper()} File')

def format_size(size_bytes: int) -> str:
    """格式化文件大小"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024:
            return f"{size_bytes:.1f}{unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f}TB"

def print_scan_report(results: dict):
    """打印扫描报告"""
    print("\n🦞 龙虾卫士 - 文件安全扫描")
    print("=" * 60)
    print(f"扫描路径：{results['scan_path']}")
    print(f"扫描时间：{results['scan_time']}")
    print(f"扫描文件：{results['total_files']} 个")
    print(f"安全文件：{results['safe_files']} 个")
    
    # 已确权文件（优先显示）
    if results['proven_files']:
        print(f"\n✅ 已确权文件：{len(results['proven_files'])} 个")
        for f in results['proven_files'][:10]:
            print(f"  - {f['path']} ({f['type']}, {f['size']}) [确权：{f['proof_id']}]")
    
    if results['high_risk']:
        print(f"\n❌ 高风险文件：{len(results['high_risk'])} 个")
        for f in results['high_risk'][:10]:
            print(f"  - {f['path']} ({f['type']}, {f['size']})")
    
    if results['medium_risk']:
        print(f"\n⚠️  中风险文件：{len(results['medium_risk'])} 个")
        for f in results['medium_risk'][:10]:
            print(f"  - {f['path']} ({f['type']}, {f['size']})")
    
    if results['low_risk']:
        print(f"\n🟢 低风险文件：{len(results['low_risk'])} 个")
        for f in results['low_risk'][:10]:
            print(f"  - {f['path']} ({f['type']}, {f['size']})")
    
    if results['large_files']:
        print(f"\n📦 大文件：{len(results['large_files'])} 个")
        for f in results['large_files'][:10]:
            print(f"  - {f['path']} ({f['size']})")
    
    # 安全评分（已确权文件加分）
    total_risky = len(results['high_risk']) * 3 + len(results['medium_risk']) * 2 + len(results['low_risk'])
    proven_bonus = len(results['proven_files']) * 2  # 每个已确权文件加 2 分
    if results['total_files'] > 0:
        risk_ratio = max(0, total_risky - proven_bonus) / results['total_files']
        score = max(0, 100 - int(risk_ratio * 100))
        print(f"\n📊 安全评分：{score}/100", end="")
        if score >= 90:
            print(" (优秀)")
        elif score >= 70:
            print(" (良好)")
        elif score >= 50:
            print(" (中等)")
        else:
            print(" (需改进)")
    
    print("\n建议操作:")
    if results['proven_files']:
        print("✅ 已确权文件可信，可安全使用")
    if results['high_risk']:
        print("1. 审查高风险文件，确认来源")
        print("2. 使用杀毒软件扫描高风险文件")
    if results['medium_risk']:
        print("3. 谨慎打开宏文档和脚本文件")
    print("4. 定期备份重要文件")
    print("=" * 60)

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        folder = sys.argv[1]
    else:
        folder = "."
    
    results = scan_files(folder)
    print_scan_report(results)
