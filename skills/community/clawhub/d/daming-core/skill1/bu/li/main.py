"""
礼部 - 规范制定与礼仪管理
负责制定系统规范、礼仪标准、文档管理
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

from ....config import LOCAL_LOGS_DIR


class LiBu:
    """礼部 - 规范与礼仪管理"""
    
    def __init__(self):
        self.standards_file = LOCAL_LOGS_DIR / "standards.json"
        self.protocols_file = LOCAL_LOGS_DIR / "protocols.json"
        self._ensure_files_exist()
    
    def _ensure_files_exist(self):
        """确保配置文件存在"""
        if not self.standards_file.exists():
            with open(self.standards_file, 'w', encoding='utf-8') as f:
                json.dump({
                    "created_at": datetime.now().isoformat(),
                    "standards": [],
                    "revisions": []
                }, f, ensure_ascii=False, indent=2)
        
        if not self.protocols_file.exists():
            with open(self.protocols_file, 'w', encoding='utf-8') as f:
                json.dump({
                    "created_at": datetime.now().isoformat(),
                    "protocols": [],
                    "active_protocols": []
                }, f, ensure_ascii=False, indent=2)
    
    def create_standard(self, name: str, description: str, content: str) -> Dict:
        """创建规范"""
        with open(self.standards_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        standard_id = f"STD-{datetime.now().strftime('%Y%m%d')}-{len(data['standards']) + 1:04d}"
        
        standard = {
            "id": standard_id,
            "name": name,
            "description": description,
            "content": content,
            "created_at": datetime.now().isoformat(),
            "status": "draft",
            "version": "1.0.0"
        }
        
        data["standards"].append(standard)
        
        with open(self.standards_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        return standard
    
    def approve_standard(self, standard_id: str) -> Dict:
        """批准规范"""
        with open(self.standards_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        for standard in data["standards"]:
            if standard["id"] == standard_id:
                standard["status"] = "approved"
                standard["approved_at"] = datetime.now().isoformat()
                
                # 记录修订
                revision = {
                    "standard_id": standard_id,
                    "action": "approved",
                    "timestamp": datetime.now().isoformat(),
                    "version": standard["version"]
                }
                data["revisions"].append(revision)
                
                with open(self.standards_file, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                
                return standard
        
        raise ValueError(f"规范 {standard_id} 不存在")
    
    def create_protocol(self, name: str, description: str, steps: List[str]) -> Dict:
        """创建协议"""
        with open(self.protocols_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        protocol_id = f"PROT-{datetime.now().strftime('%Y%m%d')}-{len(data['protocols']) + 1:04d}"
        
        protocol = {
            "id": protocol_id,
            "name": name,
            "description": description,
            "steps": steps,
            "created_at": datetime.now().isoformat(),
            "status": "draft"
        }
        
        data["protocols"].append(protocol)
        
        with open(self.protocols_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        return protocol
    
    def activate_protocol(self, protocol_id: str) -> Dict:
        """激活协议"""
        with open(self.protocols_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        for protocol in data["protocols"]:
            if protocol["id"] == protocol_id:
                protocol["status"] = "active"
                protocol["activated_at"] = datetime.now().isoformat()
                
                # 添加到活跃协议列表
                if protocol_id not in data["active_protocols"]:
                    data["active_protocols"].append(protocol_id)
                
                with open(self.protocols_file, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                
                return protocol
        
        raise ValueError(f"协议 {protocol_id} 不存在")
    
    def get_active_protocols(self) -> List[Dict]:
        """获取活跃协议"""
        with open(self.protocols_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        active_protocols = []
        for protocol_id in data["active_protocols"]:
            for protocol in data["protocols"]:
                if protocol["id"] == protocol_id:
                    active_protocols.append(protocol)
        
        return active_protocols
    
    def get_all_standards(self) -> List[Dict]:
        """获取所有规范"""
        with open(self.standards_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        return data["standards"]
    
    def get_standard_by_id(self, standard_id: str) -> Optional[Dict]:
        """根据ID获取规范"""
        with open(self.standards_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        for standard in data["standards"]:
            if standard["id"] == standard_id:
                return standard
        
        return None


def create_libu() -> LiBu:
    """创建礼部实例"""
    return LiBu()


def list_standards() -> List[Dict]:
    """列出所有规范"""
    libu = LiBu()
    return libu.get_all_standards()


def list_active_protocols() -> List[Dict]:
    """列出活跃协议"""
    libu = LiBu()
    return libu.get_active_protocols()


if __name__ == "__main__":
    print("🏛️ 礼部功能测试")
    libu = LiBu()
    
    # 测试创建规范
    standard = libu.create_standard(
        name="代码规范",
        description="系统代码编写规范",
        content="1. 使用PEP8规范\n2. 添加类型注解\n3. 编写文档字符串"
    )
    print(f"✅ 创建规范: {standard['id']}")
    
    # 测试创建协议
    protocol = libu.create_protocol(
        name="任务处理协议",
        description="标准任务处理流程",
        steps=[
            "1. 接收任务",
            "2. 审核任务",
            "3. 分配资源",
            "4. 执行任务",
            "5. 记录结果"
        ]
    )
    print(f"✅ 创建协议: {protocol['id']}")
    
    # 测试激活协议
    activated = libu.activate_protocol(protocol["id"])
    print(f"✅ 激活协议: {activated['id']}")
    
    print("🎉 礼部功能测试完成")