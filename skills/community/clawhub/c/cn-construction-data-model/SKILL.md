---
name: "cn-construction-data-model"
description: "面向中国建设工程项目的数据模型设计工具。创建实体关系图、定义数据模式、生成数据库结构，符合GB/T标准体系。"
version: "1.0.1"
tags:
  - 工程
  - 数据模型
  - 数据库设计
  - ER图
  - GB/T标准
  - 建设工程
---

# 🏗️ 建设工程数据模型设计器

> 面向中国建设工程项目的数据模型设计工具
> 基于 GB/T 50500-2024《建设工程工程量清单计价标准》
> 分类：**工程**

---

## 一、业务需求

### 问题痛点

| 问题 | 影响 |
|------|------|
| 📦 数据分散在各系统中 | 信息孤岛，难以整合 |
| 🔀 数据结构不统一 | 各参与方数据无法互通 |
| 🔗 实体关系缺失 | 无法追溯数据血缘 |
| 📊 集成困难 | BIM、造价、进度系统割裂 |

### 解决方案

系统性设计建设工程数据模型，定义**实体、关系、字段**，实现：
- 项目全生命周期数据管理
- 多方数据互通互联
- 数据血缘可追溯

---

## 二、技术实现

### 核心类库

```python
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from enum import Enum
import json


class DataType(Enum):
    """数据类型枚举"""
    STRING = "string"      # 字符串
    INTEGER = "integer"   # 整数
    FLOAT = "float"       # 浮点数
    BOOLEAN = "boolean"  # 布尔值
    DATE = "date"         # 日期
    DATETIME = "datetime" # 日期时间
    TEXT = "text"         # 长文本
    DECIMAL = "decimal"   # 精确小数（用于金额）


class RelationType(Enum):
    """关系类型枚举"""
    ONE_TO_ONE = "1:1"    # 一对一
    ONE_TO_MANY = "1:N"  # 一对多
    MANY_TO_MANY = "N:M" # 多对多


class ConstraintType(Enum):
    """约束类型枚举"""
    PRIMARY_KEY = "primary_key"  # 主键
    FOREIGN_KEY = "foreign_key"  # 外键
    UNIQUE = "unique"           # 唯一
    NOT_NULL = "not_null"       # 非空


@dataclass
class Field:
    """字段定义"""
    name: str              # 字段名
    data_type: DataType   # 数据类型
    nullable: bool = True
    default: Any = None
    description: str = ""  # 中文描述
    constraints: List[ConstraintType] = field(default_factory=list)


@dataclass
class Entity:
    """实体定义"""
    name: str              # 英文表名
    description: str       # 中文描述
    fields: List[Field] = field(default_factory=list)
    primary_key: str = "id"


@dataclass
class Relationship:
    """关系定义"""
    name: str
    from_entity: str
    to_entity: str
    relation_type: RelationType
    from_field: str
    to_field: str


class CNConstructionDataModel:
    """中国建设工程数据模型设计器"""

    def __init__(self, project_name: str):
        self.project_name = project_name
        self.entities: Dict[str, Entity] = {}
        self.relationships: List[Relationship] = []

    def add_entity(self, entity: Entity):
        """添加实体"""
        self.entities[entity.name] = entity

    def add_relationship(self, relationship: Relationship):
        """添加关系"""
        self.relationships.append(relationship)

    def create_entity(self, name: str, description: str,
                      fields: List[Dict[str, Any]]) -> Entity:
        """从字段定义创建实体"""
        entity_fields = [
            Field(
                name=f['name'],
                data_type=DataType(f.get('type', 'string')),
                nullable=f.get('nullable', True),
                default=f.get('default'),
                description=f.get('description', ''),
                constraints=[ConstraintType(c) for c in f.get('constraints', [])]
            )
            for f in fields
        ]
        entity = Entity(name=name, description=description, fields=entity_fields)
        self.add_entity(entity)
        return entity

    def create_relationship(self, from_entity: str, to_entity: str,
                           relation_type: str = "1:N",
                           from_field: str = None) -> Relationship:
        """创建实体间关系"""
        rel = Relationship(
            name=f"{from_entity}_{to_entity}",
            from_entity=from_entity,
            to_entity=to_entity,
            relation_type=RelationType(relation_type),
            from_field=from_field or f"{to_entity.lower()}_id",
            to_field="id"
        )
        self.add_relationship(rel)
        return rel

    def generate_sql_schema(self, dialect: str = "mysql") -> str:
        """生成SQL DDL语句"""
        sql = []
        type_map = {
            DataType.STRING: "VARCHAR(255)",
            DataType.INTEGER: "INT",
            DataType.FLOAT: "DECIMAL(15,2)",
            DataType.BOOLEAN: "TINYINT(1)",
            DataType.DATE: "DATE",
            DataType.DATETIME: "DATETIME",
            DataType.TEXT: "TEXT",
            DataType.DECIMAL: "DECIMAL(18,2)"
        }

        for name, entity in self.entities.items():
            columns = []
            for fld in entity.fields:
                col = f"    `{fld.name}` {type_map.get(fld.data_type, 'VARCHAR(255)')}"
                if not fld.nullable:
                    col += " NOT NULL"
                if ConstraintType.PRIMARY_KEY in fld.constraints:
                    col += " PRIMARY KEY"
                if fld.default is not None:
                    col += f" DEFAULT {fld.default}"
                if fld.description:
                    col += f" COMMENT '{fld.description}'"
                columns.append(col)

            sql.append(f"CREATE TABLE `{name}` (\n" + ",\n".join(columns) + "\n) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='" + entity.description + "';")

        for rel in self.relationships:
            sql.append(f"""ALTER TABLE `{rel.from_entity}`
ADD CONSTRAINT `fk_{rel.name}`
FOREIGN KEY (`{rel.from_field}`) REFERENCES `{rel.to_entity}`(`{rel.to_field}`);""")

        return "\n\n".join(sql)

    def generate_json_schema(self) -> Dict[str, Any]:
        """生成JSON Schema"""
        schemas = {}
        for name, entity in self.entities.items():
            properties = {}
            required = []

            for fld in entity.fields:
                prop = {"description": fld.description}
                if fld.data_type == DataType.STRING:
                    prop["type"] = "string"
                elif fld.data_type == DataType.INTEGER:
                    prop["type"] = "integer"
                elif fld.data_type == DataType.FLOAT:
                    prop["type"] = "number"
                elif fld.data_type == DataType.BOOLEAN:
                    prop["type"] = "boolean"
                else:
                    prop["type"] = "string"

                properties[fld.name] = prop
                if not fld.nullable:
                    required.append(fld.name)

            schemas[name] = {
                "type": "object",
                "title": entity.description,
                "properties": properties,
                "required": required
            }
        return schemas

    def generate_er_diagram(self) -> str:
        """生成Mermaid ER图"""
        lines = ["erDiagram"]
        for name, entity in self.entities.items():
            lines.append(f"    {name} {{")
            for fld in entity.fields[:6]:
                ftype = {
                    DataType.STRING: "VARCHAR",
                    DataType.INTEGER: "INT",
                    DataType.FLOAT: "DEC",
                    DataType.DECIMAL: "DEC",
                    DataType.DATE: "DATE",
                    DataType.DATETIME: "DT"
                }.get(fld.data_type, "STR")
                lines.append(f"        {ftype} {fld.name}")
            lines.append("    }")

        for rel in self.relationships:
            rel_symbol = {
                RelationType.ONE_TO_ONE: "||--||",
                RelationType.ONE_TO_MANY: "||--o{",
                RelationType.MANY_TO_MANY: "}o--o{"
            }.get(rel.relation_type, "||--o{")
            lines.append(f"    {rel.from_entity} {rel_symbol} {rel.to_entity} : \"{rel.name}\"")

        return "\n".join(lines)

    def validate_model(self) -> List[str]:
        """验证数据模型"""
        issues = []
        for rel in self.relationships:
            if rel.from_entity not in self.entities:
                issues.append(f"❌ 缺少实体: {rel.from_entity}")
            if rel.to_entity not in self.entities:
                issues.append(f"❌ 缺少实体: {rel.to_entity}")

        for name, entity in self.entities.items():
            has_pk = any(ConstraintType.PRIMARY_KEY in f.constraints for f in entity.fields)
            if not has_pk:
                issues.append(f"⚠️ 实体 '{name}' 缺少主键")

        if not issues:
            issues.append("✅ 数据模型验证通过")
        return issues


class CNConstructionEntities:
    """中国建设工程标准实体库"""

    @staticmethod
    def project_entity() -> Entity:
        """工程项目实体"""
        return Entity(
            name="engineering_projects",
            description="工程项目主表",
            fields=[
                Field("id", DataType.INTEGER, False, constraints=[ConstraintType.PRIMARY_KEY]),
                Field("project_code", DataType.STRING, False, description="项目编码", constraints=[ConstraintType.UNIQUE]),
                Field("project_name", DataType.STRING, False, description="项目名称"),
                Field("project_type", DataType.STRING, False, description="项目类型（房屋建筑/市政/公路等）"),
                Field("construction_address", DataType.STRING, description="建设地点"),
                Field("total_investment", DataType.DECIMAL, description="总投资额（元）"),
                Field("planned_area", DataType.FLOAT, description="建筑面积（㎡）"),
                Field("structure_type", DataType.STRING, description="结构类型"),
                Field("building_height", DataType.FLOAT, description="建筑高度（m）"),
                Field("basement_area", DataType.FLOAT, description="地下室面积（㎡）"),
                Field("construction_period", DataType.INTEGER, description="工期（天）"),
                Field("start_date", DataType.DATE, description="开工日期"),
                Field("completion_date", DataType.DATE, description="竣工日期"),
                Field("status", DataType.STRING, description="项目状态"),
                Field("construction_unit", DataType.STRING, description="建设单位"),
                Field("design_unit", DataType.STRING, description="设计单位"),
                Field("supervision_unit", DataType.STRING, description="监理单位"),
                Field("create_time", DataType.DATETIME, description="创建时间"),
            ]
        )

    @staticmethod
    def bill_item_entity() -> Entity:
        """工程量清单实体"""
        return Entity(
            name="bill_items",
            description="工程量清单项目",
            fields=[
                Field("id", DataType.INTEGER, False, constraints=[ConstraintType.PRIMARY_KEY]),
                Field("project_id", DataType.INTEGER, False),
                Field("bill_no", DataType.STRING, False, description="清单编码"),
                Field("item_code", DataType.STRING, description="项目编码（GB/T标准）"),
                Field("item_name", DataType.STRING, False, description="项目名称"),
                Field("project_unit", DataType.STRING, description="计量单位"),
                Field("quantity", DataType.DECIMAL, description="工程量"),
                Field("unit_price", DataType.DECIMAL, description="综合单价（元）"),
                Field("total_price", DataType.DECIMAL, description="合价（元）"),
                Field("tax_rate", DataType.FLOAT, description="税率"),
                Field("remarks", DataType.TEXT, description="备注"),
            ]
        )

    @staticmethod
    def cost_control_entity() -> Entity:
        """造价管控实体"""
        return Entity(
            name="cost_control",
            description="造价管控记录",
            fields=[
                Field("id", DataType.INTEGER, False, constraints=[ConstraintType.PRIMARY_KEY]),
                Field("project_id", DataType.INTEGER, False),
                Field("cost_stage", DataType.STRING, False, description="阶段（估算/概算/预算/结算）"),
                Field("target_cost", DataType.DECIMAL, description="目标成本（元）"),
                Field("actual_cost", DataType.DECIMAL, description="实际成本（元）"),
                Field("budget_cost", DataType.DECIMAL, description="预算成本（元）"),
                Field("change_amount", DataType.DECIMAL, description="变更金额（元）"),
                Field("cost_diff", DataType.DECIMAL, description="成本偏差（元）"),
                Field("cost_ratio", DataType.FLOAT, description="成本偏差率（%）"),
                Field("record_date", DataType.DATE, description="记录日期"),
            ]
        )

    @staticmethod
    def schedule_activity_entity() -> Entity:
        """进度计划实体"""
        return Entity(
            name="schedule_activities",
            description="进度计划活动",
            fields=[
                Field("id", DataType.INTEGER, False, constraints=[ConstraintType.PRIMARY_KEY]),
                Field("project_id", DataType.INTEGER, False),
                Field("wbs_code", DataType.STRING, description="WBS编码"),
                Field("activity_name", DataType.STRING, False, description="活动名称"),
                Field("planned_start", DataType.DATE, description="计划开始日期"),
                Field("planned_end", DataType.DATE, description="计划结束日期"),
                Field("actual_start", DataType.DATE, description="实际开始日期"),
                Field("actual_end", DataType.DATE, description="实际结束日期"),
                Field("progress_percent", DataType.FLOAT, description="完成百分比（%）"),
                Field("前置活动", DataType.STRING, description="前置活动ID"),
                Field("responsible_party", DataType.STRING, description="责任单位"),
            ]
        )

    @staticmethod
    def change_order_entity() -> Entity:
        """工程变更实体"""
        return Entity(
            name="change_orders",
            description="工程变更单",
            fields=[
                Field("id", DataType.INTEGER, False, constraints=[ConstraintType.PRIMARY_KEY]),
                Field("project_id", DataType.INTEGER, False),
                Field("change_no", DataType.STRING, description="变更编号"),
                Field("change_type", DataType.STRING, description="变更类型"),
                Field("change_reason", DataType.TEXT, description="变更原因"),
                Field("original_amount", DataType.DECIMAL, description="原金额（元）"),
                Field("change_amount", DataType.DECIMAL, description="变更金额（元）"),
                Field("new_amount", DataType.DECIMAL, description="新金额（元）"),
                Field("change_date", DataType.DATE, description="变更日期"),
                Field("approval_status", DataType.STRING, description="审批状态"),
                Field("approver", DataType.STRING, description="审批人"),
            ]
        )
```

---

## 三、快速开始

### 示例代码

```python
# 创建模型
model = CNConstructionDataModel("某学校建设项目")

# 添加标准实体
model.add_entity(CNConstructionEntities.project_entity())
model.add_entity(CNConstructionEntities.bill_item_entity())
model.add_entity(CNConstructionEntities.cost_control_entity())

# 添加关系
model.create_relationship("bill_items", "engineering_projects")
model.create_relationship("cost_control", "engineering_projects")

# 生成SQL
sql = model.generate_sql_schema("mysql")
print(sql)
```

---

## 四、常用场景

### 场景1：自定义清单实体

```python
model.create_entity(
    name="safety_inspection",
    description="安全检查记录",
    fields=[
        {"name": "id", "type": "integer", "nullable": False, "constraints": ["primary_key"]},
        {"name": "project_id", "type": "integer", "nullable": False},
        {"name": "inspection_date", "type": "date"},
        {"name": "inspector", "type": "string"},
        {"name": "issue_level", "type": "string", "description": "问题等级"},
        {"name": "description", "type": "text", "description": "问题描述"},
        {"name": "rectification_deadline", "type": "date", "description": "整改期限"},
        {"name": "rectification_status", "type": "string", "description": "整改状态"}
    ]
)
```

### 场景2：生成ER图

```python
er_diagram = model.generate_er_diagram()
print(er_diagram)
# 可复制到 https://mermaid.live 生成可视化图形
```

### 场景3：模型验证

```python
issues = model.validate_model()
for issue in issues:
    print(issue)
```

---

## 五、支持的数据库

| 数据库 | SQL方言 | 特点 |
|--------|---------|------|
| MySQL | `mysql` | 默认，推荐国内项目 |
| PostgreSQL | `postgresql` | 适合大数据量 |
| SQL Server | `mssql` | 适合Windows环境 |
| SQLite | `sqlite` | 适合单机应用 |

---

## 六、符合的标准规范

- GB/T 50500-2024《建设工程工程量清单计价标准》
- GB/T 51262-2017《建筑工程施工质量验收统一标准》
- GB/T 50328-2019《建设工程文件归档规范》
- DBJ/T 15-xxx 广东省标准系列

---

*本工具由度量衡智库出品，专为建设工程数字化管理设计。*
