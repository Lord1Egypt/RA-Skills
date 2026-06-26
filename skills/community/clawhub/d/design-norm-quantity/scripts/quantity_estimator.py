"""
基于设计规范配比的工程量精确估算计算器
Design-Norm-Quantity Estimator v1.0

使用方法:
    python quantity_estimator.py [建筑类型] [结构形式] [建筑面积] [地区] [选项]
    
示例:
    python quantity_estimator.py 住宅 剪力墙 50000 汕尾 --basement 10000 --seismic 二级
"""

import json
import sys
from typing import Dict, List, Optional
from dataclasses import dataclass
from pathlib import Path

@dataclass
class BuildingParams:
    """建筑参数"""
    building_type: str          # 建筑类型：住宅/办公/商业/医院/学校
    structure_type: str         # 结构形式：框架/剪力墙/框架-剪力墙/框架-核心筒
    area: float                 # 建筑面积（㎡）
    basement_area: float = 0    # 地下室面积（㎡）
    seismic_grade: str = "二级" # 抗震等级：一级/二级/三级
    decoration: str = "精装"     # 装修标准：毛坯/简装/精装/豪装
    floors: int = 0             # 地上层数
    basement_floors: int = 0    # 地下层数
    city: str = "汕尾"          # 城市
    year: int = 2026            # 估算年份

class QuantityEstimator:
    """工程量估算器"""
    
    def __init__(self, base_path: Optional[str] = None):
        """初始化估算器"""
        if base_path is None:
            base_path = Path(__file__).parent.parent / "references"
        else:
            base_path = Path(base_path)
        
        # 加载配比数据库
        with open(base_path / "design-quantity-ratios.json", "r", encoding="utf-8") as f:
            self.ratios = json.load(f)
        
        # 加载地区系数
        with open(base_path / "region-adjustments.json", "r", encoding="utf-8") as f:
            self.region = json.load(f)
    
    def get_city_coefficient(self, city: str) -> Dict[str, float]:
        """获取城市系数"""
        for city_data in self.region["data"]["city_coefficients"]["categories"]:
            if city_data["city"] == city:
                return {"building": city_data["building"], "installation": city_data["installation"]}
        # 默认返回汕尾系数
        return {"building": 1.03, "installation": 1.05}
    
    def get_time_coefficient(self, year: int) -> float:
        """获取时间系数"""
        for time_data in self.region["data"]["time_coefficients"]["categories"]:
            if time_data["year"] == year:
                return time_data["coefficient"]
        # 线性外推
        return 1.00 + (year - 2022) * 0.03
    
    def get_decoration_coefficient(self, decoration: str) -> float:
        """获取装修标准系数"""
        for dec_data in self.region["data"]["decoration_standards"]["categories"]:
            if dec_data["standard"] == decoration:
                return dec_data["coefficient"]
        return 1.00
    
    def get_reinforcement_ratio(self, structure_type: str, seismic_grade: str) -> Dict[str, float]:
        """获取钢筋含量配比"""
        for category in self.ratios["data"]["reinforcement_ratios"]["categories"]:
            if category["structure_type"] == structure_type:
                for grade in category["grades"]:
                    if grade["grade"] == seismic_grade:
                        return {"low": grade["low"], "median": grade["median"], "high": grade["high"]}
        # 默认值
        return {"low": 100, "median": 120, "high": 150}
    
    def get_concrete_ratio(self, building_type: str) -> Dict[str, float]:
        """获取混凝土含量配比"""
        for item in self.ratios["data"]["concrete_ratios"]["categories"]:
            if building_type in item["type"]:
                return {"low": item["low"], "median": item["median"], "high": item["high"]}
        # 默认值
        return {"low": 0.38, "median": 0.45, "high": 0.55}
    
    def get_masonry_ratio(self, building_type: str, structure_type: str) -> Dict[str, float]:
        """获取砌体含量配比"""
        # 剪力墙结构砌体含量较低
        if "剪力墙" in structure_type:
            return {"low": 0.05, "median": 0.08, "high": 0.12}
        
        for item in self.ratios["data"]["masonry_ratios"]["categories"]:
            if building_type in item["type"]:
                return {"low": item["low"], "median": item["median"], "high": item["high"]}
        
        return {"low": 0.25, "median": 0.32, "high": 0.40}
    
    def get_formwork_ratio(self) -> Dict[str, float]:
        """获取模板综合配比"""
        # 取各构件的加权平均
        components = self.ratios["data"]["formwork_ratios"]["components"]
        avg_median = sum(c["median"] for c in components) / len(components)
        avg_low = sum(c["low"] for c in components) / len(components)
        avg_high = sum(c["high"] for c in components) / len(components)
        return {"low": avg_low, "median": avg_median, "high": avg_high}
    
    def get_electrical_ratio(self, building_type: str) -> Dict:
        """获取电气安装配比"""
        for item in self.ratios["data"]["electrical_ratios"]["categories"]:
            if item["building_type"] == building_type:
                return item
        # 默认住宅
        for item in self.ratios["data"]["electrical_ratios"]["categories"]:
            if "住宅" in item["building_type"]:
                return item
        return {}
    
    def get_plumbing_ratio(self, building_type: str) -> Dict:
        """获取给排水配比"""
        for item in self.ratios["data"]["plumbing_ratios"]["categories"]:
            if item["building_type"] == building_type:
                return item
        return {}
    
    def get_hvac_ratio(self, building_type: str) -> Dict:
        """获取通风空调配比"""
        for item in self.ratios["data"]["hvac_ratios"]["categories"]:
            if item["building_type"] == building_type:
                return {"low": item["low"], "median": item["median"], "high": item["high"]}
        return {"low": 1.5, "median": 2.0, "high": 2.8}
    
    def calculate(self, params: BuildingParams) -> Dict:
        """执行工程量估算"""
        
        # 获取各类系数
        city_coef = self.get_city_coefficient(params.city)
        time_coef = self.get_time_coefficient(params.year)
        decor_coef = self.get_decoration_coefficient(params.decoration)
        
        # 获取配比
        reinf_ratio = self.get_reinforcement_ratio(params.structure_type, params.seismic_grade)
        concrete_ratio = self.get_concrete_ratio(params.building_type)
        masonry_ratio = self.get_masonry_ratio(params.building_type, params.structure_type)
        formwork_ratio = self.get_formwork_ratio()
        elec_ratio = self.get_electrical_ratio(params.building_type)
        plum_ratio = self.get_plumbing_ratio(params.building_type)
        hvac_ratio = self.get_hvac_ratio(params.building_type)
        
        # 计算混凝土工程量
        concrete_vol = {
            "low": params.area * concrete_ratio["low"] + params.basement_area * 1.5,
            "median": params.area * concrete_ratio["median"] + params.basement_area * 1.5,
            "high": params.area * concrete_ratio["high"] + params.basement_area * 1.8
        }
        
        # 计算钢筋工程量（吨）
        reinf_vol = {
            level: vol * reinf_ratio[level] / 1000  # kg转吨
            for level, vol in concrete_vol.items()
        }
        
        # 计算模板工程量
        formwork_vol = {
            level: vol * formwork_ratio[level]
            for level, vol in concrete_vol.items()
        }
        
        # 计算砌体工程量
        masonry_vol = {
            level: params.area * masonry_ratio[level]
            for level in ["low", "median", "high"]
        }
        
        # 计算电气工程量
        electrical = {
            "low_voltage": {
                level: params.area * elec_ratio["low_voltage"][level]
                for level in ["low", "median", "high"]
            } if elec_ratio else {"low": 0, "median": 0, "high": 0},
            "lighting": {
                level: params.area * elec_ratio["lighting"][level]
                for level in ["low", "median", "high"]
            } if elec_ratio else {"low": 0, "median": 0, "high": 0}
        }
        
        # 计算给排水工程量
        plumbing = {
            "supply": {
                level: params.area * plum_ratio["supply"][level]
                for level in ["low", "median", "high"]
            } if plum_ratio else {"low": 0, "median": 0, "high": 0},
            "drainage": {
                level: params.area * plum_ratio["drainage"][level]
                for level in ["low", "median", "high"]
            } if plum_ratio else {"low": 0, "median": 0, "high": 0}
        }
        
        # 计算通风空调工程量
        hvac = {
            level: params.area * hvac_ratio[level]
            for level in ["low", "median", "high"]
        }
        
        # 校验计算
        verification = {}
        if concrete_vol["median"] > 0:
            reinf_check = reinf_vol["median"] / concrete_vol["median"] * 1000  # 吨转kg
            verification["reinforcement_ratio"] = {
                "value": reinf_check,
                "min": 80,
                "max": 225,
                "valid": 80 <= reinf_check <= 225
            }
            
            formwork_check = formwork_vol["median"] / concrete_vol["median"]
            verification["formwork_ratio"] = {
                "value": formwork_check,
                "min": 8,
                "max": 25,
                "valid": 8 <= formwork_check <= 25
            }
        
        # 造价估算（元/㎡）
        base_cost = {
            "building": 3500,  # 基础建安单价
            "installation": 800,
            "decoration": 500
        }
        
        total_cost = {
            "low": (base_cost["building"] + base_cost["installation"] + base_cost["decoration"] * decor_coef) * city_coef["building"] * time_coef,
            "median": (base_cost["building"] * 1.15 + base_cost["installation"] * 1.1 + base_cost["decoration"] * decor_coef * 1.1) * city_coef["building"] * time_coef,
            "high": (base_cost["building"] * 1.3 + base_cost["installation"] * 1.2 + base_cost["decoration"] * decor_coef * 1.2) * city_coef["building"] * time_coef
        }
        
        total_price = {
            level: total_cost[level] * params.area
            for level in ["low", "median", "high"]
        }
        
        return {
            "params": {
                "building_type": params.building_type,
                "structure_type": params.structure_type,
                "area": params.area,
                "basement_area": params.basement_area,
                "seismic_grade": params.seismic_grade,
                "decoration": params.decoration,
                "city": params.city,
                "year": params.year
            },
            "coefficients": {
                "city": city_coef,
                "time": time_coef,
                "decoration": decor_coef
            },
            "quantities": {
                "concrete": concrete_vol,
                "reinforcement": reinf_vol,
                "formwork": formwork_vol,
                "masonry": masonry_vol,
                "electrical": electrical,
                "plumbing": plumbing,
                "hvac": hvac
            },
            "verification": verification,
            "cost_estimate": {
                "unit_price": total_cost,
                "total_price": {k: v/10000 for k, v in total_price.items()}  # 万元
            }
        }
    
    def format_report(self, result: Dict) -> str:
        """格式化输出报告"""
        params = result["params"]
        coeffs = result["coefficients"]
        qty = result["quantities"]
        cost = result["cost_estimate"]
        verify = result["verification"]
        
        report = f"""
================================================================================
                   [ DESIGN-NORM-QUANTITY ESTIMATION REPORT ]               
================================================================================

[1] Project Basic Information
+------------------------------------------------------------------------------+
|  Building Type: {params['building_type']:<12}   Structure: {params['structure_type']:<15}    |
|  Floor Area: {params['area']:>10,.0f} sqm    Basement: {params['basement_area']:>10,.0f} sqm        |
|  Seismic Grade: {params['seismic_grade']:<12}   Decoration: {params['decoration']:<15}    |
|  City: {params['city']:<12}         Year: {params['year']:<15}         |
+------------------------------------------------------------------------------+

[2] Adjustment Coefficients
+------------------------------------------------------------------------------+
|  City Coefficient: Building {coeffs['city']['building']:.2f}  | Installation {coeffs['city']['installation']:.2f}            |
|  Time Coefficient: {coeffs['time']:.2f} (Base Year 2022)                                         |
|  Decoration Coefficient: {coeffs['decoration']:.2f}                                                         |
+------------------------------------------------------------------------------+

[3] Civil Engineering Quantity Estimation
+------------------------------------------------------------------------------+
|  Item           |    Low     |   Median   |    High    |       Unit        |
+------------------------------------------------------------------------------+
|  Concrete       | {qty['concrete']['low']:>10,.0f} | {qty['concrete']['median']:>10,.0f} | {qty['concrete']['high']:>10,.0f} |       m3          |
|  Reinforcement | {qty['reinforcement']['low']:>10,.1f} | {qty['reinforcement']['median']:>10,.1f} | {qty['reinforcement']['high']:>10,.1f} |       t           |
|  Formwork       | {qty['formwork']['low']:>10,.0f} | {qty['formwork']['median']:>10,.0f} | {qty['formwork']['high']:>10,.0f} |       m2          |
|  Masonry        | {qty['masonry']['low']:>10,.0f} | {qty['masonry']['median']:>10,.0f} | {qty['masonry']['high']:>10,.0f} |       m3          |
+------------------------------------------------------------------------------+

[4] MEP (Mechanical/Electrical/Plumbing) Quantity Estimation
+------------------------------------------------------------------------------+
|  Item           |    Low     |   Median   |    High    |       Unit        |
+------------------------------------------------------------------------------+
|  Power Cable    | {qty['electrical']['low_voltage']['low']:>10,.0f} | {qty['electrical']['low_voltage']['median']:>10,.0f} | {qty['electrical']['low_voltage']['high']:>10,.0f} |       m           |
|  Lighting Wire  | {qty['electrical']['lighting']['low']:>10,.0f} | {qty['electrical']['lighting']['median']:>10,.0f} | {qty['electrical']['lighting']['high']:>10,.0f} |       m           |
|  Water Supply   | {qty['plumbing']['supply']['low']:>10,.0f} | {qty['plumbing']['supply']['median']:>10,.0f} | {qty['plumbing']['supply']['high']:>10,.0f} |       m           |
|  Drainage       | {qty['plumbing']['drainage']['low']:>10,.0f} | {qty['plumbing']['drainage']['median']:>10,.0f} | {qty['plumbing']['drainage']['high']:>10,.0f} |       m           |
|  HVAC Duct      | {qty['hvac']['low']:>10,.0f} | {qty['hvac']['median']:>10,.0f} | {qty['hvac']['high']:>10,.0f} |       m           |
+------------------------------------------------------------------------------+

[5] Cost Estimation
+------------------------------------------------------------------------------+
|  Unit Price    |    Low     |   Median   |    High    |       Unit        |
+------------------------------------------------------------------------------+
|  Total Cost    | {cost['unit_price']['low']:>8,.0f} | {cost['unit_price']['median']:>8,.0f} | {cost['unit_price']['high']:>8,.0f} |     CNY/sqm      |
+------------------------------------------------------------------------------+
                              TOTAL PROJECT COST
              +==================================+
              |  Low:    {cost['total_price']['low']:>12,.2f} x10,000 CNY     |
              |  Median: {cost['total_price']['median']:>12,.2f} x10,000 CNY     |
              |  High:   {cost['total_price']['high']:>12,.2f} x10,000 CNY     |
              +==================================+

[6] Verification Check
+------------------------------------------------------------------------------+
|  Check Item                |   Value    |   Range    |   Result   |
+------------------------------------------------------------------------------+
|  Reinf/Concrete Ratio     | {verify['reinforcement_ratio']['value']:>8.0f} |  {verify['reinforcement_ratio']['min']:>3.0f}-{verify['reinforcement_ratio']['max']:>3.0f} kg/m3  | {'PASS' if verify['reinforcement_ratio']['valid'] else 'WARN'}  |
|  Formwork/Concrete Ratio  | {verify['formwork_ratio']['value']:>8.1f} |   {verify['formwork_ratio']['min']:>2.0f}-{verify['formwork_ratio']['max']:>2.0f} m2/m3  | {'PASS' if verify['formwork_ratio']['valid'] else 'WARN'}  |
+------------------------------------------------------------------------------+

[7] Reference Standards
  - GB50010: Code for Design of Concrete Structures
  - GB50003: Code for Design of Masonry Structures
  - GB50210: Code for Acceptance of Construction Quality of Decoration
  - Guangdong Province Construction Engineering Valuation Standard
  - Shanwei Government Investment Project Cost Index

================================================================================
                              Report Generated
================================================================================
"""
        return report


def main():
    """主函数"""
    # 示例：高层住宅工程量估算
    params = BuildingParams(
        building_type="住宅",
        structure_type="剪力墙结构",
        area=50000,
        basement_area=10000,
        seismic_grade="二级",
        decoration="精装",
        floors=33,
        basement_floors=2,
        city="汕尾",
        year=2026
    )
    
    estimator = QuantityEstimator()
    result = estimator.calculate(params)
    report = estimator.format_report(result)
    print(report)
    
    # 输出JSON格式结果（便于程序处理）
    print("\n[JSON输出]")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
