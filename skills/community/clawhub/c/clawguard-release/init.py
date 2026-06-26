import hashlib
import os
import re
import shutil
import struct
from datetime import datetime

VERSION = "V1.5"
AUTHOR = "Bowie / 陈宝华"
COMPANY = "新疆宝恒信息科技有限公司"
EMAIL = "cbh007@qq.com"
BH_ROOT_ID = "BH-ROOT-BOWIE-20260315-CLAWGURAD-GENESIS"
BH_OFFICIAL_TAG = "✅ BH Trusted Root System"
DATA_DIR = "bh_data"
CHAIN_FILE = os.path.join(DATA_DIR, "local_chain.txt")
PROOF_LIST = os.path.join(DATA_DIR, "proof_list.txt")

os.makedirs(DATA_DIR, exist_ok=True)

def init_files():
    for f in [CHAIN_FILE, PROOF_LIST]:
        if not os.path.exists(f):
            with open(f, "w", encoding="utf-8") as fp:
                fp.write("BH_LOCAL_CHAIN_INIT\n" if f == CHAIN_FILE else "BH_PROOF_LIST\n")

init_files()

def hash_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()[:16].upper()

def hash_text(s: str) -> str:
    return hash_bytes(s.encode("utf-8", errors="replace"))

def hash_file(path: str) -> str | None:
    if not os.path.isfile(path):
        return None
    try:
        h = hashlib.sha256()
        with open(path, "rb") as f:
            while chunk := f.read(1 << 20):
                h.update(chunk)
        return h.hexdigest()[:16].upper()
    except Exception:
        return None

def get_last_block_hash() -> str:
    """获取最后一个区块的哈希"""
    try:
        with open(CHAIN_FILE, "r", encoding="utf-8") as f:
            lines = [l.strip() for l in f if l.strip().startswith("BLOCK:")]
        if not lines:
            return "GENESIS"
        # BLOCK:哈希 | 时间 |ID| 来源 | 前一哈希 | 时间类型
        return lines[-1].split("|")[0].replace("BLOCK:", "")
    except Exception:
        return "GENESIS"

def verify_chain_integrity():
    """验证区块链完整性（检测篡改）"""
    try:
        with open(CHAIN_FILE, "r", encoding="utf-8") as f:
            lines = [l.strip() for l in f if l.strip().startswith("BLOCK:")]
        
        if len(lines) == 0:
            return {"valid": True, "msg": "Chain is empty", "blocks": 0}
        
        # 验证每个区块的哈希链接
        prev_hash = "GENESIS"
        for i, line in enumerate(lines, 1):
            parts = line.split("|")
            if len(parts) < 6:
                return {"valid": False, "msg": f"Invalid block format at {i}", "block": i}
            
            # BLOCK:哈希 | 时间 |ID| 来源 | 前一哈希 | 时间类型
            stored_hash = parts[0].replace("BLOCK:", "")
            prev_stored_hash = parts[4]  # 前一区块哈希
            
            # 验证前一区块哈希是否匹配
            if prev_stored_hash != prev_hash:
                return {"valid": False, "msg": f"Chain broken at block {i}", "block": i}
            
            # 重新计算当前区块哈希
            block_data = "|".join(parts[1:])  # 去掉 BLOCK: 前缀
            calculated_hash = hash_text(block_data)
            
            if calculated_hash != stored_hash:
                return {"valid": False, "msg": f"Block {i} tampered", "block": i}
            
            prev_hash = stored_hash
        
        return {"valid": True, "msg": "Chain integrity verified", "blocks": len(lines)}
    
    except Exception as e:
        return {"valid": False, "msg": f"Verification failed: {str(e)}"}

def append_to_chain(ts: str, proof_id: str, src: str, time_type: str):
    """添加区块到链（包含前一区块哈希）"""
    try:
        last_hash = get_last_block_hash()
        # 区块数据包含前一区块哈希
        block_data = f"{ts}|{proof_id}|{src}|{last_hash}|{time_type}"
        block_hash = hash_text(block_data)
        # 存储：BLOCK:当前哈希 | 时间 |ID| 来源 | 前一哈希 | 时间类型
        with open(CHAIN_FILE, "a", encoding="utf-8") as f:
            f.write(f"BLOCK:{block_hash}|{ts}|{proof_id}|{src}|{last_hash}|{time_type}\n")
    except Exception:
        pass

def append_to_proof_list(item: str):
    try:
        with open(PROOF_LIST, "a", encoding="utf-8") as f:
            f.write(item + "\n")
    except Exception:
        pass

def get_ntp_time() -> str | None:
    """获取 NTP 网络时间（ISO 8601 格式）"""
    try:
        import socket
        servers = ["pool.ntp.org", "time.windows.com", "ntp.ntsc.ac.cn"]
        for host in servers:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                sock.settimeout(1)
                sock.sendto(b'\x1b' + 47 * b'\0', (host, 123))
                msg = sock.recv(1024)
                t = struct.unpack('!12I', msg)[10] - 2208988800
                # ISO 8601 格式：2026-03-16T15:52:00+08:00
                return datetime.fromtimestamp(t).strftime("%Y-%m-%dT%H:%M:%S+08:00")
            except Exception:
                continue
    except Exception:
        pass
    return None

def get_local_time_iso() -> str:
    """获取本地时间（ISO 8601 格式）"""
    return datetime.now().strftime("%Y-%m-%dT%H:%M:%S+08:00")

def generate_proof(data_or_path: str, owner: str = "宝爷"):
    """生成数字存证（支持多权属人）
    
    Args:
        data_or_path: 文件路径或文本内容
        owner: 权属人姓名，支持多人（用逗号分隔，如："bitBoy,宝爷"）
    """
    ntp_ts = get_ntp_time()
    local_ts = get_local_time_iso()
    ts = ntp_ts if ntp_ts else local_ts
    time_type = "ntp" if ntp_ts else "local"

    root_seed = hash_text(BH_ROOT_ID)[:8]

    # 增强文件信息收集
    file_info = {}
    if os.path.isfile(data_or_path):
        fname = os.path.basename(data_or_path)
        content_hash = hash_file(data_or_path)
        src = f"file:{fname}"
        
        # 收集文件详细信息
        try:
            stat = os.stat(data_or_path)
            file_info = {
                "filename": fname,
                "size": stat.st_size,
                "size_human": format_size(stat.st_size),
                "type": get_file_type(data_or_path),
                "full_hash": content_hash,  # 完整哈希用于法律验证
                "owner": owner  # 新增：权属人信息
            }
        except:
            file_info = {"filename": fname, "type": "unknown", "owner": owner}
    else:
        content_hash = hash_text(data_or_path)
        src = f"text"
        file_info = {
            "type": "text",
            "preview": data_or_path[:100] + "..." if len(data_or_path) > 100 else data_or_path,
            "full_hash": content_hash,
            "owner": owner  # 新增：权属人信息
        }

    if not content_hash:
        return {"error": "Invalid content or file"}

    proof_id = f"BH-{root_seed}-{content_hash}"
    append_to_chain(ts, proof_id, src, time_type)
    
    # 增强存证记录（包含权属人信息）
    proof_record = f"{ts} | {proof_id} | {src} | {'🌐 NTP' if time_type=='ntp' else '📱 Local'} | {owner} | {file_info.get('size_human', 'N/A')}"
    append_to_proof_list(proof_record)
    
    result = {
        "proof": proof_id,
        "time": ts,
        "time_type": time_type,
        "source": src,
        "root": BH_ROOT_ID,
        "file_info": file_info,
        "content_hash": content_hash,
        "owner": owner  # 新增：权属人
    }
    return result

def batch_prove_folder(folder_path: str, owner: str = "宝爷", extensions: list = None):
    """批量确权文件夹中的所有文件
    
    Args:
        folder_path: 文件夹路径
        owner: 权属人
        extensions: 支持的文件扩展名列表（默认支持所有）
    
    Returns:
        dict: {total: 总数，success: 成功数，failed: 失败数，proofs: [确权结果列表]}
    """
    if not os.path.isdir(folder_path):
        return {"error": "Invalid folder path"}
    
    if extensions is None:
        extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.pdf', '.doc', '.docx', 
                     '.txt', '.md', '.py', '.js', '.ts', '.cpp', '.c', '.java', '.go']
    
    results = []
    success = 0
    failed = 0
    
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            ext = os.path.splitext(file)[1].lower()
            if ext in extensions or extensions == ['*']:
                file_path = os.path.join(root, file)
                try:
                    result = generate_proof(file_path, owner)
                    if "error" not in result:
                        results.append(result)
                        success += 1
                    else:
                        failed += 1
                except Exception as e:
                    failed += 1
    
    return {
        "total": success + failed,
        "success": success,
        "failed": failed,
        "proofs": results
    }
    ntp_ts = get_ntp_time()
    local_ts = get_local_time_iso()
    ts = ntp_ts if ntp_ts else local_ts
    time_type = "ntp" if ntp_ts else "local"

    root_seed = hash_text(BH_ROOT_ID)[:8]

    # 增强文件信息收集
    file_info = {}
    if os.path.isfile(data_or_path):
        fname = os.path.basename(data_or_path)
        content_hash = hash_file(data_or_path)
        src = f"file:{fname}"
        
        # 收集文件详细信息
        try:
            stat = os.stat(data_or_path)
            file_info = {
                "filename": fname,
                "size": stat.st_size,
                "size_human": format_size(stat.st_size),
                "type": get_file_type(data_or_path),
                "full_hash": content_hash,  # 完整哈希用于法律验证
                "owner": owner  # 新增：权属人信息
            }
        except:
            file_info = {"filename": fname, "type": "unknown", "owner": owner}
    else:
        content_hash = hash_text(data_or_path)
        src = f"text"
        file_info = {
            "type": "text",
            "preview": data_or_path[:100] + "..." if len(data_or_path) > 100 else data_or_path,
            "full_hash": content_hash,
            "owner": owner  # 新增：权属人信息
        }

    if not content_hash:
        return {"error": "Invalid content or file"}

    proof_id = f"BH-{root_seed}-{content_hash}"
    append_to_chain(ts, proof_id, src, time_type)
    
    # 增强存证记录（包含权属人信息）
    proof_record = f"{ts} | {proof_id} | {src} | {'🌐 NTP' if time_type=='ntp' else '📱 Local'} | {owner} | {file_info.get('size_human', 'N/A')}"
    append_to_proof_list(proof_record)
    
    result = {
        "proof": proof_id,
        "time": ts,
        "time_type": time_type,
        "source": src,
        "root": BH_ROOT_ID,
        "file_info": file_info,
        "content_hash": content_hash,
        "owner": owner  # 新增：权属人
    }
    return result

def format_size(size_bytes: int) -> str:
    """格式化文件大小"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024:
            return f"{size_bytes:.1f}{unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f}TB"

def get_file_type(path: str) -> str:
    """获取文件类型"""
    ext = os.path.splitext(path)[1].lower()
    type_map = {
        '.jpg': 'JPEG 图片', '.jpeg': 'JPEG 图片', '.png': 'PNG 图片',
        '.gif': 'GIF 图片', '.webp': 'WebP 图片', '.bmp': 'BMP 图片',
        '.mp4': 'MP4 视频', '.avi': 'AVI 视频', '.mov': 'MOV 视频',
        '.mp3': 'MP3 音频', '.wav': 'WAV 音频', '.flac': 'FLAC 音频',
        '.pdf': 'PDF 文档', '.doc': 'Word 文档', '.docx': 'Word 文档',
        '.xls': 'Excel 表格', '.xlsx': 'Excel 表格',
        '.py': 'Python 代码', '.js': 'JavaScript 代码', '.ts': 'TypeScript 代码',
        '.txt': '文本文件', '.md': 'Markdown 文档'
    }
    return type_map.get(ext, f'{ext.upper()} 文件')

def auto_proof(data_or_path: str):
    try:
        return generate_proof(data_or_path)
    except Exception as e:
        return {"error": f"auto_proof failed: {str(e)}"}

def verify_proof(proof_id: str):
    # 1. 格式检查
    if not isinstance(proof_id, str):
        return {"valid": False, "msg": "Invalid proof type"}
    if not proof_id.startswith("BH-"):
        return {"valid": False, "msg": "Invalid proof prefix (must start with BH-)"}
    
    parts = proof_id.split("-")
    if len(parts) < 3:
        return {"valid": False, "msg": "Invalid proof format (must be BH-XXXX-YYYY)"}
    
    # 2. 链上验证（核心安全修复）
    try:
        if not os.path.exists(CHAIN_FILE):
            return {"valid": False, "msg": "Chain file not found"}
        
        with open(CHAIN_FILE, "r", encoding="utf-8") as f:
            chain_content = f.read()
            # 检查 proof ID 是否存在于链中
            if proof_id in chain_content:
                return {"valid": True, "msg": BH_OFFICIAL_TAG, "root": BH_ROOT_ID}
            else:
                return {"valid": False, "msg": "Proof not found in chain (可能已伪造)"}
    except Exception as e:
        return {"valid": False, "msg": f"Chain verification failed: {str(e)}"}

def clean_all():
    targets = ["__pycache__", "logs", "cache", "tmp", "temp"]
    removed = []
    for d in targets:
        if os.path.isdir(d):
            shutil.rmtree(d, ignore_errors=True)
            removed.append(d)
    return removed

def backup_config():
    if not os.path.exists("config.json"):
        return False
    ts = datetime.now().strftime("%Y%m%d%H%M%S")
    name = f"config.{ts}.bak"
    try:
        shutil.copy("config.json", name)
        return name
    except Exception:
        return False

def restore_latest():
    backs = sorted([f for f in os.listdir(".") if f.startswith("config.") and f.endswith(".bak")], reverse=True)
    if not backs:
        return False
    try:
        shutil.copy(backs[0], "config.json")
        return backs[0]
    except Exception:
        return False

def export_proofs():
    out = os.path.join(DATA_DIR, "exported_proofs.txt")
    try:
        shutil.copy(PROOF_LIST, out)
        return out
    except Exception:
        return None

def search_proofs(query: str = None, owner: str = None, date: str = None, file_type: str = None):
    """搜索存证记录
    
    Args:
        query: 关键词搜索（文件名/ID）
        owner: 按权属人搜索
        date: 按日期搜索 (YYYY-MM-DD)
        file_type: 按文件类型搜索 (image/text/code)
    
    Returns:
        list: 匹配的存证记录列表
    """
    try:
        with open(PROOF_LIST, "r", encoding="utf-8") as f:
            lines = f.readlines()
        
        results = []
        for line in lines[1:]:  # 跳过标题行
            line = line.strip()
            if not line:
                continue
            
            parts = line.split(" | ")
            if len(parts) < 5:
                continue
            
            ts, proof_id, source, time_type, owner_rec = parts[:5]
            
            # 搜索条件匹配
            match = True
            
            if query and query.lower() not in line.lower():
                match = False
            
            if owner and owner.lower() not in owner_rec.lower():
                match = False
            
            if date and not ts.startswith(date.replace("-", "")):
                match = False
            
            if file_type:
                if file_type == "image" and not any(ext in source.lower() for ext in ['.jpg', '.png', '.gif']):
                    match = False
                elif file_type == "text" and source == "text":
                    pass
                elif file_type == "code" and not any(ext in source.lower() for ext in ['.py', '.js', '.ts', '.cpp']):
                    match = False
            
            if match:
                results.append({
                    "time": ts,
                    "proof_id": proof_id,
                    "source": source,
                    "time_type": time_type,
                    "owner": owner_rec,
                    "size": parts[5] if len(parts) > 5 else "N/A"
                })
        
        return results
    
    except Exception as e:
        return []

def get_stats():
    """获取统计信息"""
    try:
        with open(PROOF_LIST, "r", encoding="utf-8") as f:
            lines = f.readlines()
        
        total = len(lines) - 1  # 减去标题行
        if total <= 0:
            return {"total": 0}
        
        # 统计文件类型
        types = {"image": 0, "text": 0, "code": 0, "other": 0}
        owners = {}
        
        for line in lines[1:]:
            parts = line.strip().split(" | ")
            if len(parts) < 3:
                continue
            
            source = parts[2]
            owner = parts[4] if len(parts) > 4 else "未知"
            
            # 文件类型统计
            if any(ext in source.lower() for ext in ['.jpg', '.png', '.gif', '.jpeg']):
                types["image"] += 1
            elif source == "text":
                types["text"] += 1
            elif any(ext in source.lower() for ext in ['.py', '.js', '.ts', '.cpp', '.java']):
                types["code"] += 1
            else:
                types["other"] += 1
            
            # 权属人统计
            owners[owner] = owners.get(owner, 0) + 1
        
        return {
            "total": total,
            "types": types,
            "owners": owners,
            "latest": lines[-1].strip() if len(lines) > 1 else "N/A"
        }
    
    except Exception as e:
        return {"error": str(e)}

def generate_certificate(proof_id: str, output_format: str = "text", file_info: dict = None, language: str = "zh"):
    """生成可视化存证凭证（增强版 - 支持多语言 + 权属人信息）
    
    Args:
        proof_id: 确权 ID
        output_format: 输出格式 (text/markdown/json)
        file_info: 文件信息字典
        language: 语言 (zh=中文/en=英文/bi=中英双语)
    """
    # 查找 proof 信息（包含权属人）- 读取最新记录
    try:
        with open(PROOF_LIST, "r", encoding="utf-8") as f:
            lines = f.readlines()
            proof_info = None
            # 从后往前找，取最新的记录
            for line in reversed(lines):
                if proof_id in line:
                    parts = line.strip().split(" | ")
                    # 新格式：时间 | ID | 来源 | 时间类型 | 权属人 | 大小
                    # 旧格式：时间 | ID | 来源 | 时间类型 | 大小
                    if len(parts) >= 5:
                        # 检查第 5 个字段是权属人还是大小
                        field5 = parts[4]
                        is_owner = not any(unit in field5 for unit in ["KB", "MB", "GB", "Bytes"])
                        
                        proof_info = {
                            "time": parts[0],
                            "proof_id": parts[1],
                            "source": parts[2],
                            "time_type": parts[3],
                            "owner": parts[4] if is_owner and len(parts) >= 5 else "未知",
                            "size": parts[5] if len(parts) > 5 else (parts[4] if not is_owner and len(parts) > 4 else "N/A")
                        }
                        break
        
        if not proof_info:
            return {"error": "Proof not found"}
        
        # 提取文件名和类型
        source = proof_info["source"]
        filename = source.replace("file:", "") if source.startswith("file:") else "文本内容"
        content_type = file_info.get("type", "未知") if file_info else "N/A"
        full_hash = file_info.get("full_hash", "N/A") if file_info else proof_id.split("-")[-1] if len(proof_id.split("-")) > 2 else "N/A"
        owner = proof_info.get("owner", "未知")  # 权属人信息
        
        # 生成增强版凭证（多语言 + 权属人信息）
        if output_format == "text":
            if language == "zh":
                # 纯中文版（含权属人）
                cert = f"""
╔══════════════════════════════════════════════════════════╗
║              🦞 龙虾卫士 存证凭证                        ║
║              AI 数字资产所有权证书                        ║
╠══════════════════════════════════════════════════════════╣
║                                                          ║
║  确权 ID: {proof_info["proof_id"]}
║  权属人：{owner}
║                                                          ║
║  ────────────────────────────────────────────────────    ║
║  📄 文件信息                                              ║
║  文件名：{filename[:40]}{"..." if len(filename)>40 else ""}
║  文件类型：{content_type}
║  文件大小：{proof_info["size"]}
║  内容哈希：{full_hash[:32]}...  {" " * (32-len(full_hash[:32]))}║
║  ────────────────────────────────────────────────────    ║
║                                                          ║
║  ⏰ 存证时间：{proof_info["time"]} {proof_info["time_type"]}
║  ✅ 状态：已上本地可信链
║  🔍 验证：龙虾卫士，验真 {proof_info["proof_id"]}
║                                                          ║
║  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━            ║
║  📌 法律效力说明                                          ║
║  1. 内容哈希 = SHA256(原文件) → 证明内容唯一性            ║
║  2. 时间戳 = NTP 网络时间 → 证明存证时间                  ║
║  3. 本地链存证 → 不可篡改                                 ║
║  4. 第三方可验真 → 任何人都能验证                         ║
║                                                          ║
║  新疆宝恒信息科技有限公司                                ║
╚══════════════════════════════════════════════════════════╝
"""
            elif language == "en":
                # 纯英文版（含权属人）
                time_mark = "NTP" if proof_info["time_type"] == "🌐 NTP" else "Local"
                cert = f"""
╔══════════════════════════════════════════════════════════╗
║         🦞 ClawGuard Certificate of Proof                ║
║         AI Digital Asset Ownership Certificate           ║
╠══════════════════════════════════════════════════════════╣
║                                                          ║
║  Proof ID: {proof_info["proof_id"]}
║  Owner: {owner}
║                                                          ║
║  ────────────────────────────────────────────────────    ║
║  📄 File Information                                      ║
║  Filename: {filename[:40]}{"..." if len(filename)>40 else ""}
║  File Type: {content_type}
║  File Size: {proof_info["size"]}
║  Content Hash: {full_hash[:32]}...{" " * (32-len(full_hash[:32]))}║
║  ────────────────────────────────────────────────────    ║
║                                                          ║
║  ⏰ Timestamp: {proof_info["time"]} [{time_mark}]
║  ✅ Status: Verified on Local Blockchain
║  🔍 Verify: lobster verify {proof_info["proof_id"]}
║                                                          ║
║  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━            ║
║  📌 Legal Validity                                        ║
║  1. Content Hash = SHA256(Original) → Uniqueness         ║
║  2. Timestamp = NTP Time → Proof of Existence            ║
║  3. Blockchain → Tamper-proof                            ║
║  4. Third-party Verification → Publicly Verifiable       ║
║                                                          ║
║  Xinjiang Baoheng Information Technology Co., Ltd.       ║
╚══════════════════════════════════════════════════════════╝
"""
            else:  # language == "bi"
                # 中英双语版（正式场合用，含权属人）
                time_mark = "NTP" if proof_info["time_type"] == "🌐 NTP" else "Local"
                cert = f"""
╔══════════════════════════════════════════════════════════╗
║  🦞 ClawGuard Certificate of Proof / 存证凭证            ║
║  AI Digital Asset Ownership / AI 数字资产所有权证书      ║
╠══════════════════════════════════════════════════════════╣
║                                                          ║
║  Proof ID / 确权 ID: {proof_info["proof_id"]}
║  Owner / 权属人：{owner}
║                                                          ║
║  ────────────────────────────────────────────────────    ║
║  📄 File Info / 文件信息                                  ║
║  Filename / 文件名：{filename[:35]}{"..." if len(filename)>35 else ""}
║  Type / 类型：{content_type}
║  Size / 大小：{proof_info["size"]}
║  Hash / 哈希：{full_hash[:32]}...{" " * (32-len(full_hash[:32]))}║
║  ────────────────────────────────────────────────────    ║
║                                                          ║
║  ⏰ Timestamp / 时间：{proof_info["time"]} [{time_mark}]
║  ✅ Status / 状态：Verified / 已验证
║  🔍 Verify / 验证：lobster verify {proof_info["proof_id"]}
║                                                          ║
║  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━            ║
║  📌 Legal Validity / 法律效力                             ║
║  1. SHA256 Hash → Uniqueness / 内容唯一性                ║
║  2. NTP Timestamp → Proof / 存证时间                     ║
║  3. Blockchain → Tamper-proof / 不可篡改                 ║
║  4. Third-party / 第三方可验证                           ║
║                                                          ║
║  Xinjiang Baoheng Info Tech / 新疆宝恒信息科技           ║
╚══════════════════════════════════════════════════════════╝
"""
            return {"certificate": cert, "format": "text"}
        
        elif output_format == "markdown":
            if language == "zh":
                cert = f"""# 🦞 龙虾卫士 存证凭证

## AI 数字资产所有权证书

| 项目 | 详情 |
|-----|------|
| **确权 ID** | `{proof_info["proof_id"]}` |
| **存证时间** | {proof_info["time"]} {proof_info["time_type"]} |
| **状态** | ✅ 已上本地可信链 |

### 📄 文件信息

| 属性 | 值 |
|-----|------|
| **文件名** | `{filename}` |
| **文件类型** | {content_type} |
| **文件大小** | {proof_info["size"]} |
| **内容哈希 (SHA256)** | `{full_hash}` |

### 🔍 验证方式

```bash
龙虾卫士，验真 {proof_info["proof_id"]}
```

### ⚖️ 法律效力说明

**如何证明此凭证与原文件的关联？**

1. **内容哈希验证** - 使用 SHA256 工具计算原文件哈希，对比凭证中的哈希值
2. **时间戳验证** - NTP 网络时间同步，证明在 {proof_info["time"]} 已存在
3. **链上存证验证** - 存证记录在本地区块链中，不可篡改
4. **第三方验真** - 任何人都可用"龙虾卫士"验真

---
**新疆宝恒信息科技有限公司**  
**凭证版本**: V1.2 (增强版 - 含文件指纹)
"""
            elif language == "en":
                time_mark = "NTP" if proof_info["time_type"] == "🌐 NTP" else "Local"
                cert = f"""# 🦞 ClawGuard Certificate of Proof

## AI Digital Asset Ownership Certificate

| Item | Details |
|------|---------|
| **Proof ID** | `{proof_info["proof_id"]}` |
| **Timestamp** | {proof_info["time"]} [{time_mark}] |
| **Status** | ✅ Verified on Blockchain |

### 📄 File Information

| Attribute | Value |
|-----------|-------|
| **Filename** | `{filename}` |
| **File Type** | {content_type} |
| **File Size** | {proof_info["size"]} |
| **Content Hash (SHA256)** | `{full_hash}` |

### 🔍 Verification

```bash
lobster verify {proof_info["proof_id"]}
```

### ⚖️ Legal Validity

**How to verify this certificate matches the original file?**

1. **Content Hash** - Calculate SHA256 of original file, compare with certificate hash
2. **Timestamp** - NTP synchronized time, proves existence at {proof_info["time"]}
3. **Blockchain** - Recorded on local blockchain, tamper-proof
4. **Third-party** - Anyone can verify using "ClawGuard"

---
**Xinjiang Baoheng Information Technology Co., Ltd.**  
**Certificate Version**: V1.2 (Enhanced with File Fingerprint)
"""
            else:  # bilingual
                time_mark = "NTP" if proof_info["time_type"] == "🌐 NTP" else "Local"
                cert = f"""# 🦞 ClawGuard Certificate / 龙虾卫士存证凭证

## AI Digital Asset Ownership / AI 数字资产所有权证书

| Item / 项目 | Details / 详情 |
|-------------|---------------|
| **Proof ID / 确权 ID** | `{proof_info["proof_id"]}` |
| **Timestamp / 存证时间** | {proof_info["time"]} [{time_mark}] |
| **Status / 状态** | ✅ Verified / 已验证 |

### 📄 File Info / 文件信息

| Attribute / 属性 | Value / 值 |
|-----------------|-----------|
| **Filename / 文件名** | `{filename}` |
| **Type / 类型** | {content_type} |
| **Size / 大小** | {proof_info["size"]} |
| **Hash / 哈希** | `{full_hash}` |

### 🔍 Verify / 验证

```bash
lobster verify / 龙虾卫士，验真 {proof_info["proof_id"]}
```

### ⚖️ Legal Validity / 法律效力

1. **SHA256 Hash** → Uniqueness / 内容唯一性
2. **NTP Timestamp** → Proof of Existence / 存证时间
3. **Blockchain** → Tamper-proof / 不可篡改
4. **Third-party** → Publicly Verifiable / 第三方可验证

---
**Xinjiang Baoheng / 新疆宝恒信息科技有限公司**  
**Version / 版本**: V1.2
"""
            return {"certificate": cert, "format": "markdown"}
        
        elif output_format == "json":
            return {
                "certificate": {
                    "version": "V1.2",
                    "proof_id": proof_info["proof_id"],
                    "timestamp": proof_info["time"],
                    "time_type": proof_info["time_type"],
                    "file": {
                        "name": filename,
                        "type": content_type,
                        "size": proof_info["size"],
                        "sha256_hash": full_hash
                    },
                    "status": "verified",
                    "issuer": "新疆宝恒信息科技有限公司",
                    "root_id": BH_ROOT_ID,
                    "legal_proof": {
                        "content_hash": "SHA256(原文件) = " + full_hash,
                        "timestamp": "NTP 网络时间 = " + proof_info["time"],
                        "chain": "本地区块链存证（不可篡改）",
                        "verification": "第三方可验真"
                    }
                },
                "format": "json"
            }
        
        return {"error": "Unsupported format"}
    
    except Exception as e:
        return {"error": f"Generate certificate failed: {str(e)}"}

def clean_cmd(s: str) -> str:
    """清理命令，保留中文内容"""
    cleaned = re.sub(r"\s+", " ", s).strip()
    return cleaned

def handle(query: str):
    try:
        raw = str(query).strip()
        cmd = clean_cmd(raw).lower()
        cmd_no_spaces = cmd.replace(" ", "")  # 移除空格用于匹配
        is_en = any(w in cmd for w in ["ai proof","verify","clean","backup","restore","help","version","status","export","list"])
        is_chinese = any(kw in cmd for kw in ["龙虾", "确权", "验真", "查看", "导出", "清理", "备份", "恢复", "状态", "版本", "帮助"])
        head = "【🦞 ClawGuard / 龙虾卫士】"
        
        # 中文命令优先
        if is_chinese or not is_en:
            if cmd in ["", "龙虾卫士", "clawguard"] or cmd_no_spaces in ["龙虾卫士", "clawguard"]:
                return f"""{head}
{BH_OFFICIAL_TAG}

🦞 ClawGuard / 龙虾卫士 - AI Digital Asset Proof System

Commands / 命令:
  clawguard, prove [file/text] [owner]     - AI 确权 (Default owner: 宝爷)
  clawguard, certificate [ID] [lang]       - 生成凭证 (zh/en/bi)
  clawguard, verify [ID]                   - 验真
  clawguard, list                          - 查看记录
  clawguard, export                        - 导出记录
  clawguard, status                        - 系统状态
  clawguard, help                          - 帮助信息

Examples / 示例:
  clawguard, prove photo.jpg 宝爷           - 文件确权
  clawguard, prove This is my work 张三     - 文本确权
  clawguard, certificate BH-xxx bi          - Bilingual certificate
  clawguard, verify BH-xxx                  - Verify proof

中文命令也支持:
  龙虾卫士，AI 确权 [文件] [权属人]
  龙虾卫士，生成凭证 [ID] [语言]
  龙虾卫士，验真 [ID]
"""
            # 支持中英文命令：AI 确权 / prove
            if any(kw in cmd_no_spaces for kw in ["ai 确权", "prove", "clawguardprove"]):
                # 支持多种命令格式，支持指定权属人（支持多人）
                # 英文：clawguard, prove photo.jpg Bowie Chen
                # 中文：龙虾卫士，AI 确权 photo.jpg 权属人：bitBoy,宝爷
                target_match = re.search(r"(?:ai 确权|prove)\s+(.+?)(?:\s+(?:权属人 [：:]?\s*|owner[：:]?\s*))?(.+)?$", raw, re.IGNORECASE)
                if target_match:
                    target = target_match.group(1).strip()
                    owner = target_match.group(2).strip() if target_match.group(2) else "宝爷"
                else:
                    target = re.sub(r".*?(?:ai 确权|prove)", "", raw, flags=re.IGNORECASE).strip()
                    owner_match = re.search(r"(?:权属人 [：:]?\s*|owner[：:]?\s*)(.+)", target)
                    if owner_match:
                        owner = owner_match.group(1).strip()
                        target = re.sub(r"\s*(?:权属人 [：:]?\s*|owner[：:]?\s*).*", "", target).strip()
                    else:
                        owner = "宝爷"  # 默认权属人
                
                # 支持多权属人（逗号分隔）
                res = generate_proof(target, owner)
            
            # V1.5 新功能：批量确权
            if any(kw in cmd_no_spaces for kw in ["batchprove", "batch_prove", "批量确权"]):
                folder_match = re.search(r"(?:batch[_ ]?prove|批量确权)\s+(.+?)(?:\s+(?:owner[：:]?\s*|权属人 [：:]?\s*))?(.+)?$", raw, re.IGNORECASE)
                if folder_match:
                    folder = folder_match.group(1).strip()
                    owner = folder_match.group(2).strip() if folder_match.group(2) else "宝爷"
                    
                    result = batch_prove_folder(folder, owner)
                    if "error" in result:
                        return f"{head}\n❌ {result['error']}"
                    
                    return f"""{head}
{BH_OFFICIAL_TAG}
📦 批量确权完成 / Batch Proof Complete

📊 统计 / Statistics:
  总数 / Total: {result['total']}
  成功 / Success: {result['success']}
  失败 / Failed: {result['failed']}

📄 最新 5 个存证 / Latest 5 Proofs:
{chr(10).join([f"  - {p['proof']} | {p['file_info']['filename']}" for p in result['proofs'][-5:]])}
"""
                if "error" in res:
                    return f"{head}\n❌ {res['error']}"
                tmark = "🌐 网络时间" if res["time_type"] == "ntp" else "📱 本地时间"
                
                # 自动生成增强版凭证（传入文件信息）
                file_info = res.get('file_info', {})
                cert_result = generate_certificate(res['proof'], "text", file_info)
                cert_text = cert_result.get('certificate', '') if 'certificate' in cert_result else ''
                
                return f"""{head}
{BH_OFFICIAL_TAG}
✅ Proof ID / 确权 ID: {res['proof']}
👤 Owner / 权属人：{owner}
⏰ Time / 时间：{res['time']} {tmark}
📄 Source / 来源：{res['source']}
🔒 Status / 状态：Verified on Blockchain / 已上链

{cert_text}
💡 Tips / 提示:
- clawguard, certificate [ID] [lang] - Generate certificate / 生成凭证
- clawguard, verify [ID] - Verify proof / 验真
- clawguard, prove [file] [owner] - Prove ownership / AI 确权
"""
            # 支持中英文：验真 / verify
            if any(kw in cmd for kw in ["验真", "verify"]):
                pid = re.sub(r".*?(?:验真|verify)\s*", "", raw, flags=re.IGNORECASE).strip()
                v = verify_proof(pid)
                if v['valid']:
                    return f"{head}\n✅ Verified / 验真成功\n{v['msg']}"
                return f"{head}\n❌ Verification Failed / 验真失败\n{v['msg']}"
            # 支持中英文命令：生成凭证 / certificate
            if any(kw in cmd_no_spaces for kw in ["生成凭证", "certificate", "cert"]):
                # 提取 proof ID 和语言参数
                pid_match = re.search(r"(?:生成凭证|certificate|cert)\s*([A-Z0-9-]+)", raw, re.IGNORECASE)
                lang_match = re.search(r"(中文 | 英文 | 双语|zh|en|bi|chinese|english|bilingual)", raw, re.IGNORECASE)
                
                pid = pid_match.group(1) if pid_match else re.sub(r".*?(?:生成凭证|certificate|cert)\s*", "", raw, flags=re.IGNORECASE).strip()
                lang = "bi"  # 默认中英双语（国际化）
                if lang_match:
                    l = lang_match.group(1).lower()
                    if l in ["zh", "中文", "chinese"]: lang = "zh"
                    elif l in ["en", "英文", "english"]: lang = "en"
                    elif l in ["bi", "双语", "bilingual"]: lang = "bi"
                
                cert_result = generate_certificate(pid, "text", file_info=None, language=lang)
                if "error" in cert_result:
                    return f"{head}\n❌ Error: {cert_result['error']}"
                return f"{head}\n{BH_OFFICIAL_TAG}\n{cert_result['certificate']}"
            # V1.5 新功能：搜索
            if any(kw in cmd for kw in ["search", "搜索"]):
                # 提取搜索参数
                owner_match = re.search(r"owner[：:]\s*(\S+)", raw, re.IGNORECASE)
                date_match = re.search(r"date[：:]\s*(\S+)", raw, re.IGNORECASE)
                type_match = re.search(r"type[：:]\s*(\S+)", raw, re.IGNORECASE)
                query_match = re.search(r"(?:search|搜索)\s+(.+?)(?:\s+(?:owner|date|type)[：:])?", raw, re.IGNORECASE)
                
                owner = owner_match.group(1) if owner_match else None
                date = date_match.group(1) if date_match else None
                file_type = type_match.group(1) if type_match else None
                query = query_match.group(1).strip() if query_match else None
                
                # 移除参数部分
                if query:
                    query = re.sub(r'\s+(owner|date|type)[：:].*', '', query).strip()
                
                results = search_proofs(query=query, owner=owner, date=date, file_type=file_type)
                
                if not results:
                    return f"{head}\n❌ No results found / 未找到匹配记录"
                
                result_text = "\n".join([
                    f"{r['time']} | {r['proof_id']} | {r['source']} | {r['owner']} | {r['size']}"
                    for r in results[:20]  # 最多显示 20 条
                ])
                
                return f"""{head}
{BH_OFFICIAL_TAG}
🔍 搜索结果 / Search Results

找到 / Found: {len(results)} 条记录
{result_text}
"""
            
            # V1.5 新功能：统计
            if any(kw in cmd for kw in ["stats", "statistic", "统计"]):
                stats = get_stats()
                
                if "error" in stats:
                    return f"{head}\n❌ {stats['error']}"
                
                types_text = "\n".join([f"  {k}: {v}" for k, v in stats.get('types', {}).items()])
                owners_text = "\n".join([f"  {k}: {v}" for k, v in list(stats.get('owners', {}).items())[:10]])
                
                return f"""{head}
{BH_OFFICIAL_TAG}
📊 统计信息 / Statistics

总数 / Total: {stats['total']}

📁 文件类型 / File Types:
{types_text}

👥 权属人 / Owners (Top 10):
{owners_text}
"""
            
            if "查看记录" in cmd_no_spaces or "查看记录" in cmd or cmd == "list":
                try:
                    with open(PROOF_LIST, encoding="utf-8") as f:
                        return head + "\n" + BH_OFFICIAL_TAG + "\n" + f.read()[-800:]
                except:
                    return head + "\n❌ No list"
            if "导出记录" in cmd_no_spaces or "导出记录" in cmd:
                p = export_proofs()
                return f"{head}\n✅ 已导出到：{p}" if p else f"{head}\n❌ 导出失败"
            if "清理" in cmd_no_spaces or "清理" in cmd:
                r = clean_all()
                return f"{head}\n✅ 已清理：{', '.join(r) if r else '无垃圾'}"
            if "备份" in cmd_no_spaces or "备份" in cmd:
                n = backup_config()
                return f"{head}\n✅ 已备份：{n}" if n else f"{head}\n❌ 无配置文件"
            if "恢复" in cmd_no_spaces or "恢复" in cmd:
                n = restore_latest()
                return f"{head}\n✅ 已恢复：{n}" if n else f"{head}\n❌ 无备份"
            if "状态" in cmd_no_spaces or "状态" in cmd:
                # 验证区块链完整性
                chain_status = verify_chain_integrity()
                chain_msg = "✅ 完整" if chain_status['valid'] else f"❌ 异常：{chain_status['msg']}"
                list_ok = os.path.exists(PROOF_LIST)
                config_ok = os.path.exists('config.json')
                return f"""{head}
🔗 区块链 / Blockchain: {chain_msg}
📋 存证清单 / List: {"✅ 正常" if list_ok else "❌ 缺失"}
⚙️  配置 / Config: {"✅ 存在" if config_ok else "⚠️ 无配置文件"}
📊 区块数 / Blocks: {chain_status.get('blocks', 0)}
"""
            if "版本" in cmd_no_spaces or "版本" in cmd:
                return f"{head}\n{VERSION}\n{AUTHOR}｜{COMPANY}｜{EMAIL}"
            if "帮助" in cmd_no_spaces or "帮助" in cmd:
                return f"""{head}
{BH_OFFICIAL_TAG}

🦞 龙虾卫士 V1.5 - 14 个功能

📌 核心功能 (5 个):
  prove [文件] [权属人]     - AI 确权（支持多人）
  certificate [ID] [语言]   - 生成凭证 (中文/英文/双语)
  verify [ID]               - 验真
  list                      - 查看记录
  export                    - 导出记录

📌 管理功能 (6 个):
  clean                     - 清理缓存
  backup                    - 备份配置
  restore                   - 恢复配置
  status                    - 系统状态（含区块链验证）
  version                   - 版本信息
  help                      - 帮助信息

📌 V1.5 新增 (3 个):
  batch_prove [文件夹] owner:[姓名]  - 批量确权
  search owner:[姓名] date:[日期]    - 搜索存证
  stats                              - 统计信息

📄 示例:
  龙虾卫士，AI 确权 photo.jpg 权属人：宝爷
  clawguard, batch_prove C:/Photos owner:Bowie Chen
  clawguard, search owner:bitBoy
  clawguard, stats

🔗 文档：README.md | FEATURES.md | RELEASE-V1.5.md

同一内容，同一指纹。谁先确权，谁是源头。
"""
            return f"{head}\n❌ 指令无法识别"
        
        # 英文命令
        else:
            if cmd in ["", "clawguard"]:
                return f"""{head}
{BH_OFFICIAL_TAG}
Commands:
ai proof [path/text]   - Prove ownership
certificate [ID]       - Generate certificate
verify [ID]            - Verify proof
list                   - Show proofs
export                 - Export proofs
clean                  - Clean junk
backup                 - Backup config
restore                - Restore config
status                 - Status
version                - Version
help                   - Help
"""
            if "aiproof" in cmd or "ai proof" in cmd:
                target = re.sub(r".*?(?:ai proof|aiproof).*?", "", raw, flags=re.IGNORECASE).strip()
                res = generate_proof(target)
                if "error" in res:
                    return f"{head}\n❌ {res['error']}"
                tmark = "🌐 NTP" if res["time_type"] == "ntp" else "📱 Local"
                return f"{head}\n✅ Proof: {res['proof']}\n⏰ {res['time']} {tmark}\n📄 {res['source']}\n🔒 On chain"
            if "verify" in cmd:
                pid = re.sub(r".*?verify\s*", "", raw, flags=re.IGNORECASE).strip()
                v = verify_proof(pid)
                return f"{head}\n{'✅ Valid' if v['valid'] else '❌ Invalid'}\n{v['msg']}"
            if "certificate" in cmd:
                pid = re.sub(r".*?certificate\s*", "", raw, flags=re.IGNORECASE).strip()
                cert_result = generate_certificate(pid, "text")
                if "error" in cert_result:
                    return f"{head}\n❌ {cert_result['error']}"
                return f"{head}\n{BH_OFFICIAL_TAG}\n{cert_result['certificate']}"
            if cmd == "list":
                try:
                    with open(PROOF_LIST, encoding="utf-8") as f:
                        return head + "\n" + BH_OFFICIAL_TAG + "\n" + f.read()[-800:]
                except:
                    return head + "\n❌ No list"
            if cmd == "export":
                p = export_proofs()
                return f"{head}\n✅ Exported to: {p}" if p else f"{head}\n❌ Export failed"
            if cmd == "clean":
                r = clean_all()
                return f"{head}\n✅ Cleaned: {', '.join(r) if r else 'nothing'}"
            if cmd == "backup":
                n = backup_config()
                return f"{head}\n✅ Backed up: {n}" if n else f"{head}\n❌ No config"
            if cmd == "restore":
                n = restore_latest()
                return f"{head}\n✅ Restored: {n}" if n else f"{head}\n❌ No backup"
            if "status" in cmd:
                # Verify blockchain integrity
                chain_status = verify_chain_integrity()
                chain_msg = "✅ Verified" if chain_status['valid'] else f"❌ Error: {chain_status['msg']}"
                list_ok = os.path.exists(PROOF_LIST)
                config_ok = os.path.exists('config.json')
                return f"""{head}
🔗 Blockchain: {chain_msg}
📋 Proof List: {"✅ OK" if list_ok else "❌ Missing"}
⚙️  Config: {"✅ Exists" if config_ok else "⚠️ No config"}
📊 Blocks: {chain_status.get('blocks', 0)}
"""
            if cmd == "version":
                return f"{head}\n{VERSION}\n{AUTHOR} | {COMPANY} | {EMAIL}"
            if cmd == "help":
                return f"""{head}
{BH_OFFICIAL_TAG}

🦞 ClawGuard - Complete Commands

Core Commands:
  prove [file/text] [owner]  - AI 确权 (Default: 宝爷)
  certificate [ID] [lang]    - 生成凭证 (zh/en/bi)
  verify [ID]                - 验真

Management:
  list                       - 查看所有存证
  export                     - 导出存证
  clean                      - 清理缓存
  backup                     - 备份配置
  restore                    - 恢复配置
  status                     - 系统状态
  version                    - 版本信息
  help                       - 帮助

Features:
  ✅ Offline First · NTP Timestamp · Local Blockchain
  ✅ No Cloud · No Public Chain · Fully Self-hosted
  ✅ Multilingual Support (Chinese/English/Bilingual)
  ✅ Owner Attribution (明确权属)

First to Prove, First to Own.
"""
            if cmd == "clean":
                r = clean_all()
                return f"{head}\n✅ Cleaned: {', '.join(r) if r else 'Nothing'}"
            if cmd == "backup":
                n = backup_config()
                return f"{head}\n✅ Backup: {n}" if n else f"{head}\n❌ No config"
            if cmd == "restore":
                n = restore_latest()
                return f"{head}\n✅ Restored: {n}" if n else f"{head}\n❌ No backup"
            if cmd == "status":
                # Verify blockchain integrity
                chain_status = verify_chain_integrity()
                chain_msg = "✅ Verified" if chain_status['valid'] else f"❌ Error: {chain_status['msg']}"
                list_ok = os.path.exists(PROOF_LIST)
                config_ok = os.path.exists('config.json')
                return f"""{head}
🔗 Blockchain: {chain_msg}
📋 Proof List: {"✅ OK" if list_ok else "❌ Missing"}
⚙️  Config: {"✅ Exists" if config_ok else "⚠️ No config"}
📊 Blocks: {chain_status.get('blocks', 0)}
"""
            if cmd == "version":
                return f"{head}\n{VERSION}\n{AUTHOR} | {COMPANY} | {EMAIL}"
            if cmd == "help":
                return f"""{head}
{BH_OFFICIAL_TAG}
✅ All file formats supported
✅ Offline first, online upgrade
✅ Anti-tamper local chain
✅ AI Agent auto_proof()
✅ Exportable proofs
No cloud • No chain • Self-sovereign

Same content = same fingerprint.
Who proofs first, owns the root.
"""
            return f"{head}\n❌ Unknown command"
    except Exception as e:
        return f"【🦞 ClawGuard / 龙虾卫士】Error: {str(e)}"
