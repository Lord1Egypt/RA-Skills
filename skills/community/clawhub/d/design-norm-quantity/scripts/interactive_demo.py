"""
Design Norm Quantity Estimation System - Interactive Demo
设计规范配比工程量估算系统 - 交互式演示

This script demonstrates the complete AI-user interaction flow:
1. Welcome & Initiation
2. Mandatory Parameter Collection
3. Optional Parameter Collection
4. Validation
5. Calculation Execution
6. Report Generation
"""

import json
import sys
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional
from datetime import datetime

# Force UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')


class SessionState:
    """Session states"""
    INIT = "INIT"
    COLLECTING_MANDATORY = "COLLECTING_MANDATORY"
    COLLECTING_OPTIONAL = "COLLECTING_OPTIONAL"
    VALIDATING = "VALIDATING"
    CALCULATING = "CALCULATING"
    GENERATING_REPORT = "GENERATING_REPORT"
    COMPLETED = "COMPLETED"
    ERROR = "ERROR"


@dataclass
class EstimationParams:
    """Estimation Parameters"""
    # Mandatory
    building_type: Optional[str] = None
    structure_type: Optional[str] = None
    total_area: Optional[float] = None
    city: Optional[str] = None
    estimation_year: int = 2026
    
    # Optional
    basement_area: float = 0
    seismic_grade: str = "二级"
    decoration_level: str = "精装"
    floor_count: int = 0
    basement_floors: int = 0
    has_pile: bool = False
    pile_type: Optional[str] = None
    reinforcement_factor: float = 1.0
    concrete_factor: float = 1.0
    labor_factor: float = 1.0
    
    def get_mandatory_missing(self) -> List[str]:
        """Get missing mandatory parameters"""
        missing = []
        if not self.building_type:
            missing.append("building_type")
        if not self.structure_type:
            missing.append("structure_type")
        if not self.total_area or self.total_area <= 0:
            missing.append("total_area")
        if not self.city:
            missing.append("city")
        return missing


class InteractionFlow:
    """Interaction Flow Manager"""
    
    BUILDING_TYPES = [
        ("A", "住宅", "高层住宅、公寓等居住建筑"),
        ("B", "办公", "写字楼、政府办公楼等"),
        ("C", "商业", "商场、综合体等"),
        ("D", "医院", "医院、医疗建筑"),
        ("E", "学校", "教学楼、图书馆等教育建筑"),
    ]
    
    STRUCTURE_TYPES = {
        "住宅": [
            ("A", "框架结构", "梁柱承重，室内空间灵活"),
            ("B", "剪力墙结构", "抗震性能好，高层住宅首选"),
            ("C", "框架-剪力墙", "综合优势，中高层住宅"),
        ],
        "办公": [
            ("A", "框架结构", "空间灵活，易于分割"),
            ("B", "框架-核心筒", "超高层写字楼首选"),
        ],
        "default": [
            ("A", "框架结构", "最常见的结构形式"),
            ("B", "框架-剪力墙", "中高层建筑"),
        ]
    }
    
    CITIES = [
        ("A", "汕尾", {"building": 1.03, "installation": 1.05}),
        ("B", "广州", {"building": 1.15, "installation": 1.18}),
        ("C", "深圳", {"building": 1.22, "installation": 1.25}),
        ("D", "东莞", {"building": 1.08, "installation": 1.10}),
    ]
    
    DECORATION_LEVELS = [
        ("A", "毛坯", 0.80, "基础装修"),
        ("B", "简装", 1.00, "普通装修"),
        ("C", "精装", 1.20, "精装修 (推荐)"),
        ("D", "豪装", 1.50, "高端装修"),
    ]
    
    def __init__(self):
        self.state = SessionState.INIT
        self.params = EstimationParams()
        self.current_question: Optional[str] = None
        
    def show_welcome(self) -> str:
        """Show welcome message"""
        welcome = """
================================================================================
         DESIGN NORM QUANTITY ESTIMATION SYSTEM
         Based on GB50010/GB50011/GB50003 Design Standards
================================================================================

 Welcome to the Design Norm Quantity Estimation System!

 This system provides precise quantity estimation based on:
   - National design codes (GB50010, GB50011, GB50003)
   - Quantity ratio coefficients
   - Regional adjustment factors

 Core Capabilities:
   [Y] Civil engineering quantity estimation
   [Y] MEP (Mechanical/Electrical/Plumbing) estimation
   [Y] Multi-city regional coefficient adjustment
   [Y] Time-based price index updates
   [Y] Intelligent validation & risk warnings
   [Y] Structured report generation

================================================================================
"""
        return welcome
    
    def show_progress(self) -> str:
        """Show parameter collection progress"""
        missing = self.params.get_mandatory_missing()
        total_mandatory = 5
        collected = 5 - len(missing)
        
        progress_bar = "=" * collected + "-" * (total_mandatory - collected)
        percentage = int(collected / total_mandatory * 100)
        
        progress = f"""
+------------------------------------------------------------------------------+
|  Progress: [{progress_bar}] {percentage}%                                     |
+------------------------------------------------------------------------------+
|  Collected Parameters:                                                       |
|    Building Type:     {self.params.building_type or 'Not set':<15}                  |
|    Structure Type:   {self.params.structure_type or 'Not set':<15}                  |
|    Total Area:        {str(round(self.params.total_area, 0)) + ' sqm' if self.params.total_area else 'Not set':<15}            |
|    City:              {self.params.city or 'Not set':<15}                          |
|    Estimation Year:   {self.params.estimation_year:<15}                             |
+------------------------------------------------------------------------------+
"""
        return progress
    
    def question_building_type(self) -> str:
        """Q1: Building type"""
        options = "\n".join([f"  {opt[0]}. {opt[1]} - {opt[2]}" for opt in self.BUILDING_TYPES])
        
        question = f"""
+------------------------------------------------------------------------------+
|  Step 1: Building Type                                                     |
+------------------------------------------------------------------------------+
|  Please select the building type:                                           |
|                                                                              |
|{options}
|                                                                              |
|  Enter option letter (e.g., A) or name:                                      |
+------------------------------------------------------------------------------+
"""
        self.current_question = "building_type"
        return question
    
    def question_structure_type(self, building_type: str) -> str:
        """Q2: Structure type"""
        options = self.STRUCTURE_TYPES.get(building_type, self.STRUCTURE_TYPES["default"])
        options_text = "\n".join([f"  {opt[0]}. {opt[1]} - {opt[2]}" for opt in options])
        
        question = f"""
+------------------------------------------------------------------------------+
|  Step 2: Structure Type                                                     |
+------------------------------------------------------------------------------+
|  Selected: [{building_type}]                                                 |
|  Please select the structure type:                                           |
|                                                                              |
|{options_text}
|                                                                              |
|  Enter option letter:                                                       |
+------------------------------------------------------------------------------+
"""
        self.current_question = "structure_type"
        return question
    
    def question_total_area(self) -> str:
        """Q3: Total area"""
        question = """
+------------------------------------------------------------------------------+
|  Step 3: Total Floor Area                                                   |
+------------------------------------------------------------------------------+
|  Please enter the total floor area (above ground):                           |
|                                                                              |
|  Reference:                                                                 |
|    - High-rise residential: 8,000 - 20,000 sqm per building                 |
|    - Office building: 10,000 - 100,000 sqm                                  |
|    - School/Hospital: 5,000 - 80,000 sqm                                    |
|                                                                              |
|  Enter area (in sqm): _______ sqm                                            |
+------------------------------------------------------------------------------+
"""
        self.current_question = "total_area"
        return question
    
    def question_city(self) -> str:
        """Q4: City"""
        options = "\n".join([f"  {opt[0]}. {opt[1]} (coef: {opt[2]['building']:.2f})" for opt in self.CITIES])
        
        question = f"""
+------------------------------------------------------------------------------+
|  Step 4: Project Location                                                   |
+------------------------------------------------------------------------------+
|  Select the city (regional coefficient will be applied):                     |
|                                                                              |
|{options}
|                                                                              |
|  Enter option letter:                                                       |
+------------------------------------------------------------------------------+
"""
        self.current_question = "city"
        return question
    
    def question_basement(self) -> str:
        """Q5: Basement (optional)"""
        question = """
+------------------------------------------------------------------------------+
|  Optional: Basement Configuration                                            |
+------------------------------------------------------------------------------+
|  Does the project have basement?                                             |
|                                                                              |
|  A. No basement                                                             |
|  B. Yes, approx 5,000 sqm                                                   |
|  C. Yes, approx 10,000 sqm                                                  |
|  D. Yes, approx 20,000 sqm                                                  |
|  E. Custom area: _______ sqm                                                |
|                                                                              |
|  Enter option (or press Enter to skip):                                     |
+------------------------------------------------------------------------------+
"""
        self.current_question = "basement"
        return question
    
    def question_decoration(self) -> str:
        """Q6: Decoration level (optional)"""
        options = "\n".join([f"  {opt[0]}. {opt[1]} (coef: {opt[2]:.2f}) - {opt[3]}" for opt in self.DECORATION_LEVELS])
        
        question = f"""
+------------------------------------------------------------------------------+
|  Optional: Decoration Standard                                               |
+------------------------------------------------------------------------------+
|  Select the decoration level:                                               |
|                                                                              |
|{options}
|                                                                              |
|  Enter option (or press Enter to skip):                                     |
+------------------------------------------------------------------------------+
"""
        self.current_question = "decoration"
        return question
    
    def process_input(self, user_input: str) -> tuple:
        """Process user input"""
        user_input = user_input.strip()
        
        if user_input.lower() in ["skip", "s", ""]:
            return (True, "Skipped", "next")
        
        if self.current_question == "building_type":
            for opt in self.BUILDING_TYPES:
                if user_input.upper() == opt[0] or user_input == opt[1]:
                    self.params.building_type = opt[1]
                    return (True, f"[OK] Building Type = [{opt[1]}]", "next")
            return (False, "[ERROR] Invalid selection", "retry")
        
        elif self.current_question == "structure_type":
            options = self.STRUCTURE_TYPES.get(self.params.building_type, self.STRUCTURE_TYPES["default"])
            for opt in options:
                if user_input.upper() == opt[0] or user_input == opt[1]:
                    self.params.structure_type = opt[1]
                    return (True, f"[OK] Structure Type = [{opt[1]}]", "next")
            return (False, "[ERROR] Invalid selection", "retry")
        
        elif self.current_question == "total_area":
            try:
                area = float(user_input.replace(",", "").replace(",", ""))
                if area > 0 and area <= 500000:
                    self.params.total_area = area
                    self.params.floor_count = int(area / 1500) if self.params.building_type == "住宅" else int(area / 2000)
                    return (True, f"[OK] Area = {area:,.0f} sqm (est. {self.params.floor_count} floors)", "next")
                return (False, "[ERROR] Area out of range", "retry")
            except ValueError:
                return (False, "[ERROR] Invalid number", "retry")
        
        elif self.current_question == "city":
            for opt in self.CITIES:
                if user_input.upper() == opt[0] or user_input == opt[1]:
                    self.params.city = opt[1]
                    return (True, f"[OK] City = [{opt[1]}] (coef: {opt[2]['building']:.2f})", "next")
            return (False, "[ERROR] Invalid selection", "retry")
        
        elif self.current_question == "basement":
            area_map = {"A": 0, "B": 5000, "C": 10000, "D": 20000}
            if user_input.upper() in area_map:
                self.params.basement_area = area_map[user_input.upper()]
                return (True, f"[OK] Basement = {self.params.basement_area:,.0f} sqm", "next")
            try:
                area = float(user_input)
                self.params.basement_area = area
                return (True, f"[OK] Basement = {area:,.0f} sqm", "next")
            except ValueError:
                return (False, "[ERROR] Invalid input", "retry")
        
        elif self.current_question == "decoration":
            for opt in self.DECORATION_LEVELS:
                if user_input.upper() == opt[0] or user_input == opt[1]:
                    self.params.decoration_level = opt[1]
                    return (True, f"[OK] Decoration = [{opt[1]}] (coef: {opt[2]:.2f})", "next")
            return (False, "[ERROR] Invalid selection", "retry")
        
        return (False, "[ERROR] Unknown question", "retry")


class QuantityCalculator:
    """Quantity Calculator based on Design Norms"""
    
    REINFORCEMENT_RATIOS = {
        "框架结构": {"三级": (80, 95, 110), "二级": (95, 110, 130), "一级": (110, 130, 150)},
        "框架-剪力墙": {"三级": (100, 120, 140), "二级": (115, 135, 160), "一级": (130, 150, 175)},
        "剪力墙结构": {"三级": (120, 140, 165), "二级": (140, 160, 185), "一级": (155, 180, 210)},
        "框架-核心筒": {"二级": (145, 170, 200), "一级": (165, 190, 225)},
    }
    
    CONCRETE_RATIOS = {
        "住宅": (0.38, 0.45, 0.55),
        "办公": (0.32, 0.38, 0.45),
        "商业": (0.40, 0.48, 0.58),
        "医院": (0.42, 0.50, 0.60),
        "学校": (0.32, 0.38, 0.45),
    }
    
    FORMWORK_RATIO = (8.0, 12.0, 18.0)
    
    MASONRY_RATIOS = {
        "剪力墙结构": (0.05, 0.08, 0.12),
        "框架结构": (0.20, 0.25, 0.35),
        "框架-剪力墙": (0.15, 0.20, 0.28),
        "框架-核心筒": (0.12, 0.18, 0.25),
    }
    
    def __init__(self, params: EstimationParams):
        self.params = params
        
    def get_city_coefficient(self) -> Dict[str, float]:
        city_coefs = {
            "汕尾": {"building": 1.03, "installation": 1.05},
            "广州": {"building": 1.15, "installation": 1.18},
            "深圳": {"building": 1.22, "installation": 1.25},
            "东莞": {"building": 1.08, "installation": 1.10},
        }
        return city_coefs.get(self.params.city, city_coefs["汕尾"])
    
    def get_time_coefficient(self) -> float:
        return 1.0 + (self.params.estimation_year - 2022) * 0.04
    
    def get_decoration_coefficient(self) -> float:
        return {"毛坯": 0.80, "简装": 1.00, "精装": 1.20, "豪装": 1.50}.get(self.params.decoration_level, 1.0)
    
    def calculate(self) -> Dict:
        p = self.params
        
        city_coef = self.get_city_coefficient()
        time_coef = self.get_time_coefficient()
        decor_coef = self.get_decoration_coefficient()
        
        reinf_ratio = self.REINFORCEMENT_RATIOS.get(p.structure_type, {}).get(
            p.seismic_grade, (100, 120, 150))
        concrete_ratio = self.CONCRETE_RATIOS.get(p.building_type, (0.35, 0.42, 0.50))
        formwork_ratio = self.FORMWORK_RATIO
        masonry_ratio = self.MASONRY_RATIOS.get(p.structure_type, (0.15, 0.20, 0.28))
        
        # Concrete volume
        concrete_above = [p.total_area * concrete_ratio[i] for i in range(3)]
        concrete_below = [p.basement_area * (1.5 if i < 2 else 1.8) for i in range(3)] if p.basement_area > 0 else [0,0,0]
        concrete_total = [concrete_above[i] + concrete_below[i] for i in range(3)]
        
        # Reinforcement (tons)
        reinf_vol = [concrete_total[i] * reinf_ratio[i] / 1000 * p.reinforcement_factor for i in range(3)]
        
        # Formwork
        formwork_vol = [concrete_total[i] * formwork_ratio[1] for i in range(3)]
        
        # Masonry
        masonry_vol = [p.total_area * masonry_ratio[i] for i in range(3)]
        
        # Electrical
        elec_low = [p.total_area * 3.5 for _ in range(3)]
        elec_light = [p.total_area * 8.0 for _ in range(3)]
        
        # Plumbing
        plum_supply = [p.total_area * 2.5 for _ in range(3)]
        plum_drain = [p.total_area * 2.0 for _ in range(3)]
        
        # Cost
        base_cost = 3500
        total_cost = [
            base_cost * city_coef["building"] * time_coef * decor_coef * 0.9,
            base_cost * city_coef["building"] * time_coef * decor_coef,
            base_cost * city_coef["building"] * time_coef * decor_coef * 1.25,
        ]
        total_price = [total_cost[i] * (p.total_area + p.basement_area) / 10000 for i in range(3)]
        
        reinf_check = reinf_vol[1] / concrete_total[1] * 1000 if concrete_total[1] > 0 else 0
        
        return {
            "params": asdict(p),
            "coefficients": {
                "city": city_coef,
                "time": time_coef,
                "decoration": decor_coef,
            },
            "quantities": {
                "concrete": {"above": concrete_above, "below": concrete_below, "total": concrete_total},
                "reinforcement": reinf_vol,
                "formwork": formwork_vol,
                "masonry": masonry_vol,
                "electrical": {"low_voltage": elec_low, "lighting": elec_light},
                "plumbing": {"supply": plum_supply, "drainage": plum_drain},
            },
            "cost": {
                "unit_price": total_cost,
                "total_price": total_price,
            },
            "verification": {
                "reinforcement_ratio": reinf_check,
                "is_valid": 80 <= reinf_check <= 225,
            }
        }


def run_demo():
    """Run interactive demo"""
    print("\n" + "="*80)
    print("    DESIGN NORM QUANTITY ESTIMATION SYSTEM - INTERACTIVE DEMO")
    print("="*80 + "\n")
    
    flow = InteractionFlow()
    
    # Welcome
    print(flow.show_welcome())
    input("\nPress ENTER to start parameter collection...")
    
    # Mandatory parameters
    flow.state = "COLLECTING_MANDATORY"
    
    # Q1: Building type
    print(flow.show_progress())
    print(flow.question_building_type())
    while True:
        user_input = input("\n> Enter: ").strip()
        success, msg, action = flow.process_input(user_input)
        print(f"\nAI: {msg}")
        if success:
            break
    
    # Q2: Structure type
    print(flow.show_progress())
    print(flow.question_structure_type(flow.params.building_type))
    while True:
        user_input = input("\n> Enter: ").strip()
        success, msg, action = flow.process_input(user_input)
        print(f"\nAI: {msg}")
        if success:
            break
    
    # Q3: Total area
    print(flow.show_progress())
    print(flow.question_total_area())
    while True:
        user_input = input("\n> Enter: ").strip()
        success, msg, action = flow.process_input(user_input)
        print(f"\nAI: {msg}")
        if success:
            break
    
    # Q4: City
    print(flow.show_progress())
    print(flow.question_city())
    while True:
        user_input = input("\n> Enter: ").strip()
        success, msg, action = flow.process_input(user_input)
        print(f"\nAI: {msg}")
        if success:
            break
    
    # Optional parameters
    flow.state = "COLLECTING_OPTIONAL"
    print(flow.show_progress())
    print("\n" + "="*80)
    print("    MANDATORY PARAMETERS COMPLETE!")
    print("="*80)
    
    # Q5: Basement
    print(flow.question_basement())
    user_input = input("\n> Enter (or ENTER to skip): ").strip()
    success, msg, action = flow.process_input(user_input)
    if "Skipped" in msg or not user_input:
        flow.params.basement_area = 0
        print("\nAI: [OK] Using default: No basement")
    else:
        print(f"\nAI: {msg}")
    
    # Q6: Decoration
    print(flow.question_decoration())
    user_input = input("\n> Enter (or ENTER to skip): ").strip()
    success, msg, action = flow.process_input(user_input)
    if "Skipped" in msg or not user_input:
        flow.params.decoration_level = "精装"
        print("\nAI: [OK] Using default: 精装")
    else:
        print(f"\nAI: {msg}")
    
    # Calculate
    print("\n" + "="*80)
    print("    CALCULATING QUANTITIES...")
    print("="*80)
    
    calc = QuantityCalculator(flow.params)
    result = calc.calculate()
    
    # Generate report
    print("\n" + "="*80)
    print("    GENERATING ESTIMATION REPORT")
    print("="*80 + "\n")
    
    r = result
    p = r["params"]
    c = r["coefficients"]
    q = r["quantities"]
    cost = r["cost"]
    v = r["verification"]
    
    report = f"""
================================================================================
                         ESTIMATION REPORT
           Based on Design Norm Quantity Ratios (GB50010/GB50011)
================================================================================

[1] PROJECT INFORMATION
+------------------------------------------------------------------------------+
|  Building Type:     {p['building_type']:<15} |  Total Area:      {p['total_area']:>12,.0f} sqm     |
|  Structure Type:    {p['structure_type']:<15} |  Basement Area:  {p['basement_area']:>12,.0f} sqm     |
|  City:              {p['city']:<15} |  Decoration:    {p['decoration_level']:<15}     |
|  Seismic Grade:     {p['seismic_grade']:<15} |  Year:           {p['estimation_year']:<15}     |
+------------------------------------------------------------------------------+

[2] ADJUSTMENT COEFFICIENTS
+------------------------------------------------------------------------------+
|  City Coef (Build): {c['city']['building']:.2f}   City Coef (Install): {c['city']['installation']:.2f}   |
|  Time Coef: {c['time']:.2f}   Decoration Coef: {c['decoration']:.2f}                                      |
+------------------------------------------------------------------------------+

[3] CIVIL ENGINEERING QUANTITIES
+------------------------------------------------------------------------------+
|  Item           |     Low    |   Median   |    High   |      Unit       |
+------------------------------------------------------------------------------+
|  Concrete       | {q['concrete']['total'][0]:>10,.0f} | {q['concrete']['total'][1]:>10,.0f} | {q['concrete']['total'][2]:>10,.0f} |       m3        |
|    - Above      | {q['concrete']['above'][0]:>10,.0f} | {q['concrete']['above'][1]:>10,.0f} | {q['concrete']['above'][2]:>10,.0f} |       m3        |
|    - Below      | {q['concrete']['below'][0]:>10,.0f} | {q['concrete']['below'][1]:>10,.0f} | {q['concrete']['below'][2]:>10,.0f} |       m3        |
|  Reinforcement  | {q['reinforcement'][0]:>10,.1f} | {q['reinforcement'][1]:>10,.1f} | {q['reinforcement'][2]:>10,.1f} |        t         |
|  Formwork       | {q['formwork'][0]:>10,.0f} | {q['formwork'][1]:>10,.0f} | {q['formwork'][2]:>10,.0f} |       m2        |
|  Masonry        | {q['masonry'][0]:>10,.0f} | {q['masonry'][1]:>10,.0f} | {q['masonry'][2]:>10,.0f} |       m3        |
+------------------------------------------------------------------------------+

[4] MEP (MECHANICAL/ELECTRICAL/PLUMBING) QUANTITIES
+------------------------------------------------------------------------------+
|  Item           |     Low    |   Median   |    High   |      Unit       |
+------------------------------------------------------------------------------+
|  Power Cable    | {q['electrical']['low_voltage'][0]:>10,.0f} | {q['electrical']['low_voltage'][1]:>10,.0f} | {q['electrical']['low_voltage'][2]:>10,.0f} |        m         |
|  Lighting Wire | {q['electrical']['lighting'][0]:>10,.0f} | {q['electrical']['lighting'][1]:>10,.0f} | {q['electrical']['lighting'][2]:>10,.0f} |        m         |
|  Water Supply   | {q['plumbing']['supply'][0]:>10,.0f} | {q['plumbing']['supply'][1]:>10,.0f} | {q['plumbing']['supply'][2]:>10,.0f} |        m         |
|  Drainage       | {q['plumbing']['drainage'][0]:>10,.0f} | {q['plumbing']['drainage'][1]:>10,.0f} | {q['plumbing']['drainage'][2]:>10,.0f} |        m         |
+------------------------------------------------------------------------------+

[5] COST ESTIMATION
+------------------------------------------------------------------------------+
|                                                                              |
|                         TOTAL PROJECT COST ESTIMATE                          |
|                                                                              |
|            +======================================+                          |
|            |                                      |                          |
|            |  LOW:      {cost['total_price'][0]:>10,.2f} x10,000 CNY      |                          |
|            |                                      |                          |
|            |  MEDIAN:   {cost['total_price'][1]:>10,.2f} x10,000 CNY      |                          |
|            |                                      |                          |
|            |  HIGH:     {cost['total_price'][2]:>10,.2f} x10,000 CNY      |                          |
|            |                                      |                          |
|            |  Unit Price: {cost['unit_price'][1]:>8,.0f} CNY/sqm        |                          |
|            +======================================+                          |
|                                                                              |
+------------------------------------------------------------------------------+

[6] VERIFICATION
+------------------------------------------------------------------------------+
|  Reinforcement/Concrete Ratio: {v['reinforcement_ratio']:>7.1f} kg/m3                        |
|  Valid Range: 80-225 kg/m3                                                    |
|  Status: {"PASS" if v['is_valid'] else "WARN"}                                                          |
+------------------------------------------------------------------------------+

[7] REFERENCE STANDARDS
  - GB 50010-2010: Code for Design of Concrete Structures
  - GB 50011-2010: Code for Seismic Design of Buildings
  - GB 50003-2011: Code for Design of Masonry Structures
  - GB/T 50353-2013: Code for Measuring Building Area

================================================================================
                    Design Norm Quantity Estimation System
                           MEDIATION WISDOM LAB
================================================================================
"""
    print(report)
    
    # JSON output
    print("\n[8] JSON OUTPUT (for programmatic processing)")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    run_demo()
