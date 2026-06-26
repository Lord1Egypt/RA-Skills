"""
Document Agent - 工艺文档智能体

专注领域：截图填表、文档生成、PLM系统对接、工艺文件管理

角色定位：专业智能体，负责企业文档全生命周期管理
"""

from __future__ import annotations

import asyncio
import logging
import uuid
from dataclasses import dataclass, field, asdict
from datetime import datetime
from enum import Enum
from typing import Any, Optional

from safety.audit_logger import AuditLogger, EventType, LogLevel, traced
from safety.permission_manager import PermissionManager, PermissionContext, PermissionResult

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# =============================================================================
# 数据模型
# =============================================================================

class DocumentType(Enum):
    """文档类型"""
    PROCESS_SHEET = "process_sheet"       # 工艺卡
    INSPECTION_REPORT = "inspection_report"  # 检验报告
    BOM = "bom"                           # 物料清单
    WORK_ORDER = "work_order"             # 作业指导书
    QUALITY_REPORT = "quality_report"     # 质量报告
    PURCHASE_REQUEST = "purchase_request"  # 采购申请单


class DocumentStatus(Enum):
    """文档状态"""
    DRAFT = "draft"
    PENDING_REVIEW = "pending_review"
    APPROVED = "approved"
    RELEASED = "released"
    OBSOLETE = "obsolete"


@dataclass
class FormField:
    """表单字段"""
    name: str
    value: Any
    source: str  # manual/auto/erp/wms/plm
    confidence: float = 1.0


@dataclass
class GeneratedDocument:
    """生成的文档"""
    doc_id: str
    doc_type: str
    title: str
    content: dict
    file_path: str
    status: str
    metadata: dict

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class PLMData:
    """PLM数据"""
    item_id: str
    name: str
    version: str
    category: str
    specifications: dict
    process_routes: list[dict]
    materials: list[dict]
    quality_standards: list[str]

    def to_dict(self) -> dict:
        return asdict(self)


# =============================================================================
# PLM服务（模拟）
# =============================================================================

class PLMService:
    """PLM（产品生命周期管理）服务"""

    ITEMS = {
        "BOM-ASSY-001": {
            "item_id": "BOM-ASSY-001",
            "name": "电机总成",
            "version": "V2.1",
            "category": "assembly",
            "specifications": {
                "power": "2.2kW",
                "voltage": "380V",
                "speed": "1450rpm",
                "efficiency": "IE3",
                "protection": "IP55",
            },
            "process_routes": [
                {"step": 1, "name": "来料检验", "station": "IQC-01", "cycle_time": 30},
                {"step": 2, "name": "轴加工", "station": "CNC-01", "cycle_time": 120},
                {"step": 3, "name": "定子装配", "station": "ASM-01", "cycle_time": 90},
                {"step": 4, "name": "总装", "station": "ASM-02", "cycle_time": 150},
                {"step": 5, "name": "测试", "station": "TEST-01", "cycle_time": 60},
                {"step": 6, "name": "包装", "station": "PKG-01", "cycle_time": 20},
            ],
            "materials": [
                {"sku": "RAW-ST-001", "name": "硅钢片", "qty": 120, "unit": "片"},
                {"sku": "RAW-CU-001", "name": "漆包线", "qty": 2.5, "unit": "kg"},
                {"sku": "SKU001", "name": "轴承", "qty": 2, "unit": "套"},
                {"sku": "RAW-AL-001", "name": "铝合金端盖", "qty": 2, "unit": "件"},
            ],
            "quality_standards": [
                "GB/T 28575-2012 电机能效限定值",
                "IEC 60034-30 电机效率等级",
                "ISO 9001:2015 过程检验",
            ],
        },
        "BOM-PUMP-002": {
            "item_id": "BOM-PUMP-002",
            "name": "工业水泵",
            "version": "V1.5",
            "category": "pump",
            "specifications": {
                "flow": "50m³/h",
                "head": "32m",
                "power": "7.5kW",
                "impeller": "closed type",
            },
            "process_routes": [
                {"step": 1, "name": "铸造", "station": "CAST-01", "cycle_time": 180},
                {"step": 2, "name": "机加工", "station": "MC-01", "cycle_time": 240},
                {"step": 3, "name": "装配", "station": "ASM-03", "cycle_time": 120},
                {"step": 4, "name": "测试", "station": "TEST-02", "cycle_time": 90},
            ],
            "materials": [
                {"sku": "RAW-HT-001", "name": "铸铁泵体", "qty": 1, "unit": "件"},
                {"sku": "SKU004", "name": "叶轮", "qty": 1, "unit": "件"},
                {"sku": "RAW-SEAL-001", "name": "机械密封", "qty": 1, "unit": "套"},
            ],
            "quality_standards": [
                "GB/T 5657-2013 离心泵技术条件",
                "ISO 5199 离心泵设计标准",
            ],
        },
    }

    async def get_item(self, item_id: str) -> dict[str, Any]:
        """查询PLM物料"""
        await asyncio.sleep(0.08)
        item = self.ITEMS.get(item_id)
        if not item:
            return {"success": False, "error": f"PLM物料不存在: {item_id}"}
        return {"success": True, "data": item}

    async def search_items(
        self,
        keyword: str = "",
        category: str = "",
    ) -> dict[str, Any]:
        """搜索PLM物料"""
        await asyncio.sleep(0.05)
        results = []
        for item_id, item in self.ITEMS.items():
            if keyword and keyword.lower() not in item["name"].lower():
                continue
            if category and item["category"] != category:
                continue
            results.append(item)

        return {
            "success": True,
            "count": len(results),
            "data": results,
        }


# =============================================================================
# 文档智能体
# =============================================================================

class DocumentAgent:
    """
    工艺文档智能体

    核心能力：
    1. 截图填表：从图像中提取信息并填入表单
    2. 文档生成：根据模板和数据生成各类文档
    3. PLM集成：从PLM系统获取工艺数据
    4. PDF导出：生成标准格式文档

    支持的文档类型：
    - 工艺卡（Process Sheet）
    - 检验报告（Inspection Report）
    - BOM表（Bill of Materials）
    - 采购申请单（Purchase Request）
    - 质量报告（Quality Report）
    """

    def __init__(
        self,
        agent_id: str = "doc_agent",
        user_id: str = "system",
        user_role: str = "viewer",
    ):
        self.agent_id = agent_id
        self.user_id = user_id
        self.user_role = user_role

        self._plm = PLMService()
        self._audit = AuditLogger(log_dir=f"./logs/{agent_id}")
        self._permission = PermissionManager()

        self.capabilities = [
            "screenshot_to_form",
            "generate_document",
            "plm_lookup",
            "pdf_export",
            "batch_process",
        ]

        logger.info(f"工艺文档智能体初始化: {agent_id}, role={user_role}")

    @traced(agent_name="doc_agent", action="screenshot_to_form")
    async def screenshot_to_form(
        self,
        screenshot_path: str,
        form_template: str,
        auto_fill: bool = True,
    ) -> dict[str, Any]:
        """
        截图填表

        从截图/图像中提取字段信息，填入指定表单模板

        Args:
            screenshot_path: 截图路径
            form_template: 表单模板类型
            auto_fill: 是否自动填充

        Returns:
            表单数据
        """
        ctx = PermissionContext(
            user_id=self.user_id,
            user_role=self.user_role,
            agent_id=self.agent_id,
            action="screenshot_to_form",
            parameters={"template": form_template},
        )
        decision = self._permission.check_permission(ctx)
        if decision.result == PermissionResult.DENIED:
            return {"success": False, "error": decision.reason, "fields": []}

        # 模拟OCR和字段提取
        await asyncio.sleep(0.15)

        # 模拟从截图提取的字段
        mock_fields = [
            FormField(name="产品名称", value="电机总成", source="ocr", confidence=0.95),
            FormField(name="型号规格", value="YE2-132S-4 2.2kW", source="ocr", confidence=0.88),
            FormField(name="数量", value="100", source="ocr", confidence=0.92),
            FormField(name="单位", value="台", source="auto", confidence=1.0),
            FormField(name="申请人", value="生产部-张工", source="ocr", confidence=0.99),
            FormField(name="申请日期", value=datetime.now().strftime("%Y-%m-%d"), source="auto", confidence=1.0),
            FormField(name="用途", value="库存补货", source="manual", confidence=1.0),
        ]

        fields_dict = {f.name: {"value": f.value, "source": f.source, "confidence": f.confidence}
                       for f in mock_fields}

        result = {
            "success": True,
            "form_template": form_template,
            "fields": fields_dict,
            "summary": {
                "total_fields": len(mock_fields),
                "auto_filled": sum(1 for f in mock_fields if f.source == "auto"),
                "ocr_confidence_avg": round(
                    sum(f.confidence for f in mock_fields if f.source == "ocr") /
                    max(sum(1 for f in mock_fields if f.source == "ocr"), 1), 2
                ),
            },
            "alerts": [
                f"⚠️ {f.name}置信度较低({f.confidence:.0%})，请人工核对"
                for f in mock_fields if f.confidence < 0.9
            ],
        }

        await self._audit.log(
            event_type=EventType.AGENT_CALL,
            action="screenshot_to_form",
            agent_name=self.agent_id,
            actor_id=self.user_id,
            level=LogLevel.INFO,
            input_data={"screenshot": screenshot_path, "template": form_template},
            output_data={"fields_extracted": len(mock_fields)},
        )

        return result

    @traced(agent_name="doc_agent", action="generate_document")
    async def generate_document(
        self,
        doc_type: str,
        title: str,
        data: dict,
        output_format: str = "json",
        template: Optional[str] = None,
    ) -> GeneratedDocument:
        """
        生成文档

        根据文档类型和传入数据生成标准格式文档

        Args:
            doc_type: 文档类型
            title: 文档标题
            data: 文档数据
            output_format: 输出格式 json/pdf/docx
            template: 可选模板ID

        Returns:
            生成的文档对象
        """
        ctx = PermissionContext(
            user_id=self.user_id,
            user_role=self.user_role,
            agent_id=self.agent_id,
            action="generate_document",
            parameters={"doc_type": doc_type, "title": title},
        )
        decision = self._permission.check_permission(ctx)

        doc_id = f"DOC-{datetime.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:6].upper()}"

        # 根据文档类型生成内容
        content = self._generate_content(doc_type, title, data)
        file_path = f"./output/{doc_id}.{output_format}"

        doc = GeneratedDocument(
            doc_id=doc_id,
            doc_type=doc_type,
            title=title,
            content=content,
            file_path=file_path,
            status="generated",
            metadata={
                "generated_by": self.agent_id,
                "generated_at": datetime.now().isoformat(),
                "user_id": self.user_id,
                "user_role": self.user_role,
                "output_format": output_format,
                "template": template,
            },
        )

        await self._audit.log(
            event_type=EventType.AGENT_CALL,
            action="generate_document",
            agent_name=self.agent_id,
            actor_id=self.user_id,
            actor_role=self.user_role,
            input_data={"doc_type": doc_type, "title": title},
            output_data={"doc_id": doc_id, "file_path": file_path},
        )

        return doc

    @traced(agent_name="doc_agent", action="plm_lookup")
    async def plm_lookup(
        self,
        item_id: Optional[str] = None,
        keyword: Optional[str] = None,
        include_process: bool = True,
        include_materials: bool = True,
    ) -> dict[str, Any]:
        """
        查询PLM系统

        Args:
            item_id: PLM物料编码
            keyword: 搜索关键词
            include_process: 包含工艺路线
            include_materials: 包含物料清单

        Returns:
            PLM数据
        """
        ctx = PermissionContext(
            user_id=self.user_id,
            user_role=self.user_role,
            agent_id=self.agent_id,
            action="plm_integration",
            parameters={"item_id": item_id, "keyword": keyword},
        )
        decision = self._permission.check_permission(ctx)
        if decision.result == PermissionResult.DENIED:
            return {"success": False, "error": decision.reason}

        if item_id:
            result = await self._plm.get_item(item_id)
        else:
            result = await self._plm.search_items(keyword=keyword or "")

        if result.get("success"):
            data = result["data"]
            if isinstance(data, dict) and include_process:
                # 添加辅助分析
                if "process_routes" in data:
                    total_cycle_time = sum(p["cycle_time"] for p in data["process_routes"])
                    data["_analysis"] = {
                        "total_steps": len(data["process_routes"]),
                        "total_cycle_time_minutes": total_cycle_time,
                        "critical_path": data["process_routes"][-1]["name"],
                        "bottleneck": max(data["process_routes"], key=lambda x: x["cycle_time"])["name"],
                    }

        return result

    async def generate_process_sheet(
        self,
        item_id: str,
        order_no: Optional[str] = None,
    ) -> GeneratedDocument:
        """生成工艺卡（快速入口）"""
        # 从PLM获取数据
        plm_data = await self.plm_lookup(item_id=item_id)
        if not plm_data.get("success"):
            return GeneratedDocument(
                doc_id="ERROR",
                doc_type="process_sheet",
                title="工艺卡-错误",
                content={"error": plm_data.get("error", "未知错误")},
                file_path="",
                status="error",
                metadata={},
            )

        data = plm_data["data"]
        return await self.generate_document(
            doc_type="process_sheet",
            title=f"工艺卡 - {data['name']} ({data['version']})",
            data={
                "item": data,
                "order_no": order_no or f"WO-{datetime.now().strftime('%Y%m%d%H%M')}",
                "workshop": "装配车间A线",
            },
        )

    def _generate_content(
        self,
        doc_type: str,
        title: str,
        data: dict,
    ) -> dict[str, Any]:
        """根据文档类型生成内容结构"""
        if doc_type == "process_sheet":
            item = data.get("item", {})
            return {
                "header": {
                    "title": title,
                    "document_no": f"PS-{datetime.now().strftime('%Y%m%d')}",
                    "version": item.get("version", "V1.0"),
                    "effective_date": datetime.now().strftime("%Y-%m-%d"),
                },
                "product_info": {
                    "name": item.get("name", ""),
                    "specifications": item.get("specifications", {}),
                },
                "process_routes": item.get("process_routes", []),
                "materials": item.get("materials", []),
                "quality_standards": item.get("quality_standards", []),
                "footer": {
                    "prepared_by": self.user_id,
                    "approved_by": "",
                    "approved_date": "",
                },
            }
        elif doc_type == "purchase_request":
            return {
                "header": {
                    "pr_no": f"PR-{datetime.now().strftime('%Y%m%d%H%M')}",
                    "date": datetime.now().strftime("%Y-%m-%d"),
                    "department": data.get("department", ""),
                    "applicant": data.get("applicant", ""),
                },
                "items": data.get("items", []),
                "total_amount": data.get("total_amount", 0),
                "purpose": data.get("purpose", ""),
                "urgency": data.get("urgency", "normal"),
            }
        else:
            return {
                "title": title,
                "content": data,
                "generated_at": datetime.now().isoformat(),
            }


# =============================================================================
# 入口
# =============================================================================

if __name__ == "__main__":
    async def demo():
        print("=" * 60)
        print("  工艺文档智能体演示")
        print("=" * 60)

        agent = DocumentAgent(user_role="procurement_manager")

        # PLM查询
        print("\n[1] 查询PLM物料")
        plm = await agent.plm_lookup(item_id="BOM-ASSY-001")
        data = plm["data"]
        print(f"  物料: {data['name']} ({data['version']})")
        print(f"  规格: {data['specifications']}")
        print(f"  工艺路线: {data['_analysis']['total_steps']}步, "
              f"总工时{data['_analysis']['total_cycle_time_minutes']}min")
        print(f"  瓶颈: {data['_analysis']['bottleneck']}")

        # 截图填表
        print("\n[2] 截图填表")
        form = await agent.screenshot_to_form(
            screenshot_path="./uploads/invoice_001.png",
            form_template="purchase_request",
        )
        print(f"  提取字段: {form['summary']['total_fields']}个")
        print(f"  自动填充: {form['summary']['auto_filled']}个")
        print(f"  OCR平均置信度: {form['summary']['ocr_confidence_avg']}")
        print(f"  告警: {form.get('alerts', [])}")

        # 生成工艺卡
        print("\n[3] 生成工艺卡")
        doc = await agent.generate_process_sheet(item_id="BOM-PUMP-002")
        print(f"  文档ID: {doc.doc_id}")
        print(f"  状态: {doc.status}")
        print(f"  工序数: {len(doc.content.get('process_routes', []))}")
        print(f"  物料项: {len(doc.content.get('materials', []))}")

        # 生成采购申请单
        print("\n[4] 生成采购申请单")
        pr = await agent.generate_document(
            doc_type="purchase_request",
            title="紧急采购申请-电机配件",
            data={
                "department": "生产部",
                "applicant": "李工",
                "items": [
                    {"sku": "SKU001", "name": "轴承", "qty": 500, "unit_price": 50},
                    {"sku": "SKU003", "name": "液压油", "qty": 50, "unit_price": 120},
                ],
                "total_amount": 31000,
                "purpose": "补货",
                "urgency": "high",
            },
        )
        print(f"  申请单号: {pr.content['header']['pr_no']}")
        print(f"  总金额: ¥{pr.content['total_amount']}")
        print(f"  物料明细: {len(pr.content['items'])}项")

    asyncio.run(demo())
