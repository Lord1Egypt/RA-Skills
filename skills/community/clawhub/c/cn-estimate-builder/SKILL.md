---
name: "cn-estimate-builder"
description: "建设工程项目估算编制系统。生成包含人工费、材料费、机械费、分包费、其他费的详细造价分解表，符合GB/T 50500-2024计价标准。"
homepage: "https://datadrivenconstruction.io"
metadata: {"openclaw":{"emoji":"📊","os":["darwin","linux","win32"],"homepage":"https://datadrivenconstruction.io","requires":{"bins":["python3"]}}}
---

# 📊 建设工程估算编制系统

## 💼 业务背景

### 问题痛点
- 造价构成复杂，人材机管利规税难以厘清
- 多层级费用类别统计困难
- 费率计算逻辑容易出错
- 清单格式要求各地不同

### 解决方案
结构化估算编制器，依据 GB/T 50500-2024《建设工程工程量清单计价标准》生成专业工程造价估算，支持 proper cost categorization, markups, and export capabilities.

## 📐 核心成本类别

| 类别 | 中文名称 | 说明 |
|------|---------|------|
| LABOR | 人工费 | 直接从事施工的生产工人开支的各项费用 |
| MATERIAL | 材料费 | 建筑工程材料、构件、零件、半成品的费用 |
| EQUIPMENT | 机械费 | 工程施工机械使用费 |
| SUBCONTRACTOR | 专业工程暂估价/分包费 | 专业工程分包及暂估价 |
| OTHER | 其他项目费 | 措施费、规费、税金等 |

## 💻 技术实现

```python
import pandas as pd
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from datetime import date
from enum import Enum


class CostCategory(Enum):
    """造价类别枚举（符合GB/T 50500-2024）"""
    人工费 = "labor"
    材料费 = "material"
    机械费 = "equipment"
    专业工程 = "subcontractor"
    其他项目费 = "other"


@dataclass
class 估算清单项:
    """估算清单行项目"""
    行号: int
    工作分解编码: str  # WBS编码
    项目名称: str      # 清单项目名称
    工程量: float
    单位: str
    综合单价: float
    费用类别: CostCategory
    备注: str = ""

    @property
    def 合价(self) -> float:
        return round(self.工程量 * self.综合单价, 2)


@dataclass
class 费用汇总:
    """分部分项工程费用汇总"""
    人工费: float = 0
    材料费: float = 0
    机械费: float = 0
    专业工程费: float = 0
    其他项目费: float = 0

    @property
    def 分部分项费(self) -> float:
        return self.人工费 + self.材料费 + self.机械费 + self.专业工程费 + self.其他项目费


@dataclass
class 费率调整:
    """费率调整项（规费、税金、利润等）"""
    名称: str
    费率: float  # 小数表示 (0.10 = 10%)
    基数: str = "直接费"  # "直接费" 或 "小计"


class 估算编制器:
    """建设工程估算编制器"""

    def __init__(self, 项目名称: str, 项目编号: str = ""):
        self.项目名称 = 项目名称
        self.项目编号 = 项目编号
        self.编制日期 = date.today()
        self.清单项列表: List[估算清单项] = []
        self.费率调整列表: List[费率调整] = []
        self._下一行号 = 1

    def 添加清单项(self,
                   工作分解编码: str,
                   项目名称: str,
                   工程量: float,
                   单位: str,
                   综合单价: float,
                   费用类别: CostCategory = CostCategory.其他项目费,
                   备注: str = "") -> 估算清单项:
        """添加清单行项目"""
        item = 估算清单项(
            行号=self._下一行号,
            工作分解编码=工作分解编码,
            项目名称=项目名称,
            工程量=工程量,
            单位=单位,
            综合单价=综合单价,
            费用类别=费用类别,
            备注=备注
        )
        self.清单项列表.append(item)
        self._下一行号 += 1
        return item

    def 添加费率调整(self, 名称: str, 费率: float, 基数: str = "直接费"):
        """添加费率调整项（规费、利润、税金等）"""
        self.费率调整列表.append(费率调整(名称=名称, 费率=费率, 基数=基数))

    def 设置标准费率(self,
                     管理费: float = 0.10,
                     利润: float = 0.07,
                     规费: float = 0.05,
                     税金: float = 0.09):
        """设置标准建设工程费率（依据建标[2013]44号）"""
        self.费率调整列表 = [
            费率调整("管理费", 管理费, "直接费"),
            费率调整("利润", 利润, "小计"),
            费率调整("规费", 规费, "小计"),
            费率调整("税金", 税金, "小计")
        ]

    def 获取费用汇总(self) -> 费用汇总:
        """按费用类别获取汇总"""
        汇总 = 费用汇总()
        for item in self.清单项列表:
            费用 = item.合价
            if item.费用类别 == CostCategory.人工费:
                汇总.人工费 += 费用
            elif item.费用类别 == CostCategory.材料费:
                汇总.材料费 += 费用
            elif item.费用类别 == CostCategory.机械费:
                汇总.机械费 += 费用
            elif item.费用类别 == CostCategory.专业工程费:
                汇总.专业工程费 += 费用
            else:
                汇总.其他项目费 += 费用
        return 汇总

    def 计算总造价(self) -> Dict[str, Any]:
        """计算含费率调整的估算总造价"""
        汇总 = self.获取费用汇总()
        直接费 = 汇总.分部分项费

        费率明细 = []
        小计 = 直接费

        for 费率项 in self.费率调整列表:
            if 费率项.基数 == "直接费":
                金额 = 直接费 * 费率项.费率
            else:
                金额 = 小计 * 费率项.费率

            费率明细.append({
                '名称': 费率项.名称,
                '费率': f"{费率项.费率 * 100:.1f}%",
                '金额': round(金额, 2)
            })
            小计 += 金额

        return {
            '费用汇总': {
                '人工费': round(汇总.人工费, 2),
                '材料费': round(汇总.材料费, 2),
                '机械费': round(汇总.机械费, 2),
                '专业工程费': round(汇总.专业工程费, 2),
                '其他项目费': round(汇总.其他项目费, 2),
                '分部分项工程费': round(直接费, 2)
            },
            '费率调整': 费率明细,
            '规费+利润+税金合计': round(小计 - 直接费, 2),
            '建筑安装工程费': round(小计, 2)
        }

    def 按WBS分组(self) -> Dict[str, List[估算清单项]]:
        """按WBS编码前缀分组清单项"""
        分组结果 = {}
        for item in self.清单项列表:
            前缀 = item.工作分解编码.split('.')[0] if '.' in item.工作分解编码 else item.工作分解编码
            if 前缀 not in 分组结果:
                分组结果[前缀] = []
            分组结果[前缀].append(item)
        return 分组结果

    def 从DataFrame导入(self, df: pd.DataFrame):
        """从DataFrame导入清单项"""
        for _, row in df.iterrows():
            self.添加清单项(
                工作分解编码=str(row.get('WBS编码', '')),
                项目名称=row['项目名称'],
                工程量=float(row['工程量']),
                单位=row['单位'],
                综合单价=float(row['综合单价']),
                费用类别=CostCategory(row.get('费用类别', 'other').lower()),
                备注=row.get('备注', '')
            )

    def 导出到DataFrame(self) -> pd.DataFrame:
        """导出估算到DataFrame"""
        data = []
        for item in self.清单项列表:
            data.append({
                '行号': item.行号,
                'WBS编码': item.工作分解编码,
                '项目名称': item.项目名称,
                '工程量': item.工程量,
                '单位': item.单位,
                '综合单价': item.综合单价,
                '合价': item.合价,
                '费用类别': item.费用类别.value,
                '备注': item.备注
            })
        return pd.DataFrame(data)

    def 导出到Excel(self, 输出路径: str) -> str:
        """导出估算到Excel（符合清单计价格式）"""
        总造价 = self.计算总造价()

        with pd.ExcelWriter(输出路径, engine='openpyxl') as writer:
            # 封面汇总
            封面数据 = pd.DataFrame([{
                '项目名称': self.项目名称,
                '项目编号': self.项目编号,
                '编制日期': self.编制日期,
                '清单项数量': len(self.清单项列表),
                '分部分项工程费': 总造价['费用汇总']['分部分项工程费'],
                '建筑安装工程费': 总造价['建筑安装工程费']
            }])
            封面数据.to_excel(writer, sheet_name='汇总封面', index=False)

            # 清单明细
            清单df = self.导出到DataFrame()
            清单df.to_excel(writer, sheet_name='清单明细', index=False)

            # 费用构成
            费用df = pd.DataFrame([总造价['费用汇总']])
            费用df.to_excel(writer, sheet_name='费用构成', index=False)

            # 费率调整
            if 总造价['费率调整']:
                费率df = pd.DataFrame(总造价['费率调整'])
                费率df.to_excel(writer, sheet_name='费率调整', index=False)

        return 输出路径

    def 校核(self) -> List[str]:
        """校核估算常见问题"""
        问题列表 = []

        if not self.清单项列表:
            问题列表.append("估算无清单项")

        for item in self.清单项列表:
            if item.工程量 <= 0:
                问题列表.append(f"行{item.行号}: 工程量无效")
            if item.综合单价 < 0:
                问题列表.append(f"行{item.行号}: 综合单价为负")
            if not item.项目名称:
                问题列表.append(f"行{item.行号}: 缺少项目名称")

        if not self.费率调整列表:
            问题列表.append("未定义费率调整（管理费、利润、规费、税金）")

        return 问题列表
```

## 🚀 快速开始

```python
# 创建估算
估算 = 估算编制器("某学校建设项目", "PRJ-2024-001")

# 添加清单项（示例：教学楼土建工程）
估算.添加清单项("01.01", "平整场地", 5000, "m²", 8.50, CostCategory.其他项目费)
估算.添加清单项("02.01", "钢筋混凝土基础", 200, "m³", 680, CostCategory.材料费)
估算.添加清单项("02.02", "基础模板", 1500, "m²", 45, CostCategory.人工费)
估算.添加清单项("02.03", "土方开挖", 3000, "m³", 28, CostCategory.机械费)
估算.添加清单项("03.01", "钢结构工程", 50, "t", 8500, CostCategory.专业工程费)

# 设置标准费率（依据建标[2013]44号）
估算.设置标准费率(管理费=0.10, 利润=0.07, 规费=0.05, 税金=0.09)

# 计算总造价
结果 = 估算.计算总造价()
print(f"分部分项工程费: ¥{结果['费用汇总']['分部分项工程费']:,.2f}")
print(f"建筑安装工程费: ¥{结果['建筑安装工程费']:,.2f}")
```

## 📋 常见用法

### 1. 按费用类别统计
```python
汇总 = 估算.获取费用汇总()
print(f"人工费: ¥{汇总.人工费:,.2f}")
print(f"材料费: ¥{汇总.材料费:,.2f}")
print(f"机械费: ¥{汇总.机械费:,.2f}")
```

### 2. 导出到Excel
```python
估算.导出到Excel("项目估算成果.xlsx")
```

### 3. 估算校核
```python
问题 = 估算.校核()
for p in 问题:
    print(f"⚠️ {p}")
```

## 📚 规范参考

| 标准号 | 标准名称 | 适用范围 |
|--------|---------|---------|
| GB/T 50500-2024 | 建设工程工程量清单计价标准 | 清单编制、计价 |
| 建标[2013]44号 | 建筑安装工程费用项目组成 | 费用构成 |
| GB/T 51262-2017 | 建筑工程施工质量验收统一标准 | 质量验收 |

## 📖 触发场景

- 建设工程估算编制
- 工程量清单编制
- 造价构成分析
- 费率计算与调整
- 估算成果导出
