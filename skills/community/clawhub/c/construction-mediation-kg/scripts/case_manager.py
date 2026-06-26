# 调解案件管理系统
# 度量衡商事调解智库 - 案件全生命周期管理

import json
import os
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Any
from dataclasses import dataclass, field, asdict
from enum import Enum

# ============================================================
# 枚举定义
# ============================================================

class CaseStatus(Enum):
    """案件状态"""
    PENDING = "待受理"           # 待受理
    ACCEPTED = "已受理"          # 已受理
    PREPARING = "准备中"          # 准备阶段
    MEDIATING = "调解中"          # 调解会议中
    AGREEMENT = "达成协议"        # 已达成调解协议
    CLOSED = "已结案"            # 已结案
    FAILED = "调解失败"          # 调解失败


class DisputeType(Enum):
    """争议类型"""
    ENGINEERING_PAYMENT = "工程款纠纷"
    SCHEDULE_DISPUTE = "工期争议"
    QUALITY_DISPUTE = "质量争议"
    CHANGE_DISPUTE = "变更签证争议"
    CONTRACT_DISPUTE = "合同争议"
    OTHER = "其他"


# ============================================================
# 数据结构
# ============================================================

@dataclass
class Party:
    """当事方"""
    name: str
    role: str          # 发包人/承包人/分包商等
    contact: str       # 联系方式
    representative: str  # 代理人
    is_key_party: bool = True  # 是否关键方


@dataclass
class DisputePoint:
    """争议焦点"""
    id: str
    description: str
    amount: float      # 涉及金额
    status: str        # 待解决/已解决/部分解决
    priority: int      # 优先级 1-5
    notes: str = ""


@dataclass
class MediationEvent:
    """调解事件"""
    event_id: str
    event_type: str    # 受理/访谈/会议/协议等
    date: str
    content: str
    participants: List[str]
    result: str = ""


@dataclass
class CaseDocument:
    """案件文档"""
    doc_id: str
    doc_type: str      # 申请书/答辩状/合同/签证等
    file_path: str
    upload_date: str
    description: str = ""


@dataclass
class MediationCase:
    """调解案件"""
    case_id: str
    case_name: str
    dispute_type: str
    status: str
    created_date: str
    updated_date: str
    
    # 当事方
    parties: List[Party]
    
    # 争议焦点
    dispute_points: List[DisputePoint]
    
    # 调解事件
    events: List[MediationEvent]
    
    # 文档
    documents: List[CaseDocument]
    
    # 金额
    total_amount: float = 0.0
    disputed_amount: float = 0.0
    
    # 备注
    notes: str = ""
    
    # 调解员
    mediator: str = ""
    
    # 截止日期
    deadline: str = ""


# ============================================================
# 案件管理器
# ============================================================

class CaseManager:
    """
    调解案件管理系统
    
    功能：
    1. 案件创建、编辑、查询
    2. 状态流转管理
    3. 争议焦点跟踪
    4. 调解进度记录
    5. 文档管理
    """
    
    def __init__(self, data_dir: str = "./case_data"):
        self.data_dir = data_dir
        self.cases: Dict[str, MediationCase] = {}
        self._ensure_data_dir()
        self._load_cases()
    
    def _ensure_data_dir(self):
        """确保数据目录存在"""
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
    
    def _load_cases(self):
        """加载已存案件"""
        for filename in os.listdir(self.data_dir):
            if filename.endswith('.json'):
                filepath = os.path.join(self.data_dir, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        case = self._deserialize_case(data)
                        self.cases[case.case_id] = case
                except:
                    pass
    
    def _get_case_file(self, case_id: str) -> str:
        return os.path.join(self.data_dir, f"{case_id}.json")
    
    def _save_case(self, case: MediationCase):
        """保存案件到文件"""
        filepath = self._get_case_file(case.case_id)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self._serialize_case(case), f, ensure_ascii=False, indent=2)
    
    def _serialize_case(self, case: MediationCase) -> Dict:
        """序列化案件"""
        return {
            "case_id": case.case_id,
            "case_name": case.case_name,
            "dispute_type": case.dispute_type,
            "status": case.status,
            "created_date": case.created_date,
            "updated_date": case.updated_date,
            "parties": [asdict(p) for p in case.parties],
            "dispute_points": [asdict(d) for d in case.dispute_points],
            "events": [asdict(e) for e in case.events],
            "documents": [asdict(d) for d in case.documents],
            "total_amount": case.total_amount,
            "disputed_amount": case.disputed_amount,
            "notes": case.notes,
            "mediator": case.mediator,
            "deadline": case.deadline
        }
    
    def _deserialize_case(self, data: Dict) -> MediationCase:
        """反序列化案件"""
        return MediationCase(
            case_id=data["case_id"],
            case_name=data["case_name"],
            dispute_type=data["dispute_type"],
            status=data["status"],
            created_date=data["created_date"],
            updated_date=data["updated_date"],
            parties=[Party(**p) for p in data.get("parties", [])],
            dispute_points=[DisputePoint(**d) for d in data.get("dispute_points", [])],
            events=[MediationEvent(**e) for e in data.get("events", [])],
            documents=[CaseDocument(**d) for d in data.get("documents", [])],
            total_amount=data.get("total_amount", 0.0),
            disputed_amount=data.get("disputed_amount", 0.0),
            notes=data.get("notes", ""),
            mediator=data.get("mediator", ""),
            deadline=data.get("deadline", "")
        )
    
    # ========== 案件操作 ==========
    
    def create_case(self, 
                   case_name: str,
                   dispute_type: str,
                   parties: List[Dict],
                   total_amount: float = 0,
                   disputed_amount: float = 0,
                   notes: str = "") -> MediationCase:
        """
        创建新案件
        
        Args:
            case_name: 案件名称
            dispute_type: 争议类型
            parties: 当事方列表 [{"name": "...", "role": "...", "contact": "...", "representative": "..."}]
            total_amount: 总金额
            disputed_amount: 争议金额
            notes: 备注
            
        Returns:
            新创建的案件
        """
        case_id = f"CASE-{datetime.now().strftime('%Y%m%d')}-{len(self.cases)+1:03d}"
        
        case = MediationCase(
            case_id=case_id,
            case_name=case_name,
            dispute_type=dispute_type,
            status=CaseStatus.PENDING.value,
            created_date=datetime.now().strftime("%Y-%m-%d"),
            updated_date=datetime.now().strftime("%Y-%m-%d"),
            parties=[Party(**p) for p in parties],
            dispute_points=[],
            events=[],
            documents=[],
            total_amount=total_amount,
            disputed_amount=disputed_amount,
            notes=notes
        )
        
        self.cases[case_id] = case
        self._save_case(case)
        
        # 添加受理事件
        self.add_event(case_id, "案件受理", f"案件已创建：{case_name}")
        
        return case
    
    def get_case(self, case_id: str) -> Optional[MediationCase]:
        """获取案件"""
        return self.cases.get(case_id)
    
    def update_case_status(self, case_id: str, new_status: str) -> bool:
        """更新案件状态"""
        case = self.cases.get(case_id)
        if not case:
            return False
        
        old_status = case.status
        case.status = new_status
        case.updated_date = datetime.now().strftime("%Y-%m-%d")
        
        self._save_case(case)
        
        # 记录状态变更事件
        self.add_event(
            case_id, 
            "状态变更", 
            f"状态从 {old_status} 变更为 {new_status}"
        )
        
        return True
    
    def list_cases(self, 
                   status: Optional[str] = None,
                   dispute_type: Optional[str] = None,
                   mediator: Optional[str] = None) -> List[MediationCase]:
        """
        列出案件
        
        Args:
            status: 案件状态过滤
            dispute_type: 争议类型过滤
            mediator: 调解员过滤
            
        Returns:
            符合条件的案件列表
        """
        results = list(self.cases.values())
        
        if status:
            results = [c for c in results if c.status == status]
        if dispute_type:
            results = [c for c in results if dispute_type in c.dispute_type]
        if mediator:
            results = [c for c in results if c.mediator == mediator]
        
        # 按更新时间倒序
        results.sort(key=lambda x: x.updated_date, reverse=True)
        
        return results
    
    # ========== 争议焦点操作 ==========
    
    def add_dispute_point(self, 
                         case_id: str,
                         description: str,
                         amount: float,
                         priority: int = 3) -> bool:
        """添加争议焦点"""
        case = self.cases.get(case_id)
        if not case:
            return False
        
        point_id = f"DP-{len(case.dispute_points)+1:02d}"
        point = DisputePoint(
            id=point_id,
            description=description,
            amount=amount,
            status="待解决",
            priority=priority
        )
        
        case.dispute_points.append(point)
        case.disputed_amount += amount
        case.updated_date = datetime.now().strftime("%Y-%m-%d")
        
        self._save_case(case)
        return True
    
    def update_dispute_point_status(self, case_id: str, point_id: str, status: str) -> bool:
        """更新争议焦点状态"""
        case = self.cases.get(case_id)
        if not case:
            return False
        
        for point in case.dispute_points:
            if point.id == point_id:
                point.status = status
                case.updated_date = datetime.now().strftime("%Y-%m-%d")
                self._save_case(case)
                return True
        
        return False
    
    # ========== 事件操作 ==========
    
    def add_event(self, 
                  case_id: str,
                  event_type: str,
                  content: str,
                  participants: Optional[List[str]] = None,
                  result: str = "") -> bool:
        """添加调解事件"""
        case = self.cases.get(case_id)
        if not case:
            return False
        
        event_id = f"EVT-{len(case.events)+1:03d}"
        event = MediationEvent(
            event_id=event_id,
            event_type=event_type,
            date=datetime.now().strftime("%Y-%m-%d %H:%M"),
            content=content,
            participants=participants or [],
            result=result
        )
        
        case.events.append(event)
        case.updated_date = datetime.now().strftime("%Y-%m-%d")
        
        self._save_case(case)
        return True
    
    # ========== 文档操作 ==========
    
    def add_document(self, 
                    case_id: str,
                    doc_type: str,
                    file_path: str,
                    description: str = "") -> bool:
        """添加文档"""
        case = self.cases.get(case_id)
        if not case:
            return False
        
        doc_id = f"DOC-{len(case.documents)+1:03d}"
        doc = CaseDocument(
            doc_id=doc_id,
            doc_type=doc_type,
            file_path=file_path,
            upload_date=datetime.now().strftime("%Y-%m-%d"),
            description=description
        )
        
        case.documents.append(doc)
        case.updated_date = datetime.now().strftime("%Y-%m-%d")
        
        self._save_case(case)
        return True
    
    # ========== 统计与报表 ==========
    
    def get_statistics(self) -> Dict[str, Any]:
        """获取案件统计"""
        total = len(self.cases)
        status_counts = {}
        type_counts = {}
        total_amount = 0
        total_disputed = 0
        
        for case in self.cases.values():
            # 状态统计
            status_counts[case.status] = status_counts.get(case.status, 0) + 1
            # 类型统计
            type_counts[case.dispute_type] = type_counts.get(case.dispute_type, 0) + 1
            # 金额统计
            total_amount += case.total_amount
            total_disputed += case.disputed_amount
        
        return {
            "total_cases": total,
            "status_distribution": status_counts,
            "type_distribution": type_counts,
            "total_amount": total_amount,
            "total_disputed": total_disputed
        }
    
    def get_case_timeline(self, case_id: str) -> List[Dict]:
        """获取案件时间线"""
        case = self.cases.get(case_id)
        if not case:
            return []
        
        timeline = []
        for event in case.events:
            timeline.append({
                "date": event.date,
                "type": event.event_type,
                "content": event.content,
                "result": event.result
            })
        
        timeline.sort(key=lambda x: x["date"])
        return timeline


# ============================================================
# 便捷函数
# ============================================================

def create_new_case(case_name: str, dispute_type: str, parties: List[Dict], 
                   amount: float, notes: str = "") -> MediationCase:
    """快速创建案件"""
    manager = CaseManager()
    return manager.create_case(case_name, dispute_type, parties, amount, amount, notes)


def list_all_cases(status: str = "") -> List[MediationCase]:
    """快速列出案件"""
    manager = CaseManager()
    return manager.list_cases(status=status)


# ============================================================
# 使用示例
# ============================================================

if __name__ == "__main__":
    # 示例1：创建案件
    print("=== 示例1：创建案件 ===")
    manager = CaseManager()
    case = manager.create_case(
        case_name="某房地产项目工程款纠纷",
        dispute_type="工程款纠纷",
        parties=[
            {"name": "A房地产开发公司", "role": "发包人", "contact": "138xxxx", "representative": "张某"},
            {"name": "B建筑工程公司", "role": "承包人", "contact": "139xxxx", "representative": "李某"}
        ],
        total_amount=8000000,
        disputed_amount=3000000,
        notes="涉及工期延误反诉"
    )
    print(f"案件创建成功: {case.case_id}")
    
    # 示例2：添加争议焦点
    print("\n=== 示例2：添加争议焦点 ===")
    manager.add_dispute_point(
        case.case_id,
        "工程款支付金额争议",
        3000000,
        priority=1
    )
    print("争议焦点已添加")
    
    # 示例3：添加调解事件
    print("\n=== 示例3：记录调解事件 ===")
    manager.add_event(
        case.case_id,
        "首次调解会议",
        "双方就工程款金额进行初步协商",
        participants=["张某", "李某", "调解员王"],
        result="双方同意进一步对账"
    )
    print("调解事件已记录")
    
    # 示例4：更新状态
    print("\n=== 示例4：更新案件状态 ===")
    manager.update_case_status(case.case_id, CaseStatus.MEDIATING.value)
    print(f"案件状态已更新为: {CaseStatus.MEDIATING.value}")
    
    # 示例5：统计报表
    print("\n=== 示例5：案件统计 ===")
    stats = manager.get_statistics()
    print(f"总案件数: {stats['total_cases']}")
    print(f"状态分布: {stats['status_distribution']}")
    print(f"类型分布: {stats['type_distribution']}")
    print(f"争议总金额: {stats['total_disputed']/10000}万元")