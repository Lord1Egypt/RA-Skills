# -*- coding: utf-8 -*-
"""
度量衡智库 · 度量衡测不准系统 - 交互式计算器
Uncertainty Calculator - Interactive Interface
===============================================

使用方法:
    python uncertainty_calculator.py

作者：度量衡智库
版本：3.0.0
日期：2026-04-03
"""

import sys
import os

# 添加脚本目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from uncertainty_estimator import (
    UncertaintyEstimator, ProjectParams, BuildingType, StructureType, Region,
    quick_estimate
)

# ============================================================
# 颜色定义（ANSI格式）
# ============================================================

class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_header(text: str):
    print(f"\n{Colors.CYAN}{Colors.BOLD}{'='*60}{Colors.ENDC}")
    print(f"{Colors.CYAN}{Colors.BOLD}  {text}{Colors.ENDC}")
    print(f"{Colors.CYAN}{Colors.BOLD}{'='*60}{Colors.ENDC}\n")

def print_section(text: str):
    print(f"\n{Colors.YELLOW}{Colors.BOLD}▶ {text}{Colors.ENDC}")

def print_success(text: str):
    print(f"{Colors.GREEN}✓ {text}{Colors.ENDC}")

def print_warning(text: str):
    print(f"{Colors.YELLOW}⚠ {text}{Colors.ENDC}")

def print_error(text: str):
    print(f"{Colors.RED}✗ {text}{Colors.ENDC}")

def print_info(label: str, value: str):
    print(f"  {Colors.BLUE}{label}:{Colors.ENDC} {value}")

# ============================================================
# 交互式输入函数
# ============================================================

def input_choice(prompt: str, options: dict, default: str = None) -> str:
    """显示选项并获取用户选择"""
    print(f"\n{Colors.BOLD}{prompt}{Colors.ENDC}")
    for key, value in options.items():
        marker = " [默认]" if key == default else ""
        print(f"  {Colors.CYAN}{key}{Colors.ENDC}. {value}{marker}")
    
    while True:
        choice = input(f"\n请选择 ({'/'.join(options.keys())}) [{default}]: ").strip()
        if not choice and default:
            return default
        if choice.upper() in options.keys():
            return choice.upper()
        if choice.upper() in [v.upper() for v in options.values()]:
            for k, v in options.items():
                if v.upper() == choice.upper():
                    return k.upper()
        print_warning(f"无效选择，请重新输入")

def input_int(prompt: str, default: int = None, min_val: int = None, max_val: int = None) -> int:
    """获取整数输入"""
    while True:
        default_str = f" [{default}]" if default is not None else ""
        value_str = input(f"{prompt}{default_str}: ").strip()
        
        if not value_str and default is not None:
            return default
        
        try:
            value = int(value_str)
            if min_val is not None and value < min_val:
                print_warning(f"值不能小于 {min_val}")
                continue
            if max_val is not None and value > max_val:
                print_warning(f"值不能大于 {max_val}")
                continue
            return value
        except ValueError:
            print_error("请输入有效整数")

def input_float(prompt: str, default: float = None, min_val: float = None) -> float:
    """获取浮点数输入"""
    while True:
        default_str = f" [{default}]" if default is not None else ""
        value_str = input(f"{prompt}{default_str}: ").strip()
        
        if not value_str and default is not None:
            return default
        
        try:
            value = float(value_str)
            if min_val is not None and value < min_val:
                print_warning(f"值不能小于 {min_val}")
                continue
            return value
        except ValueError:
            print_error("请输入有效数字")

def input_yes_no(prompt: str, default: bool = None) -> bool:
    """获取是/否输入"""
    default_str = ""
    if default is True:
        default_str = " [Y]"
    elif default is False:
        default_str = " [N]"
    
    while True:
        value = input(f"{prompt} (Y/N){default_str}: ").strip().upper()
        if not value and default is not None:
            return default
        if value in ['Y', 'YES', '是', '有']:
            return True
        if value in ['N', 'NO', '否', '无']:
            return False
        print_warning("请输入 Y 或 N")

# ============================================================
# 菜单系统
# ============================================================

class MenuSystem:
    """交互式菜单系统"""
    
    def __init__(self):
        self.estimator = UncertaintyEstimator()
        self.current_project = None
        
    def run(self):
        """运行主循环"""
        while True:
            self.show_main_menu()
            choice = input("\n请选择操作: ").strip()
            
            if choice == '1':
                self.create_project()
            elif choice == '2':
                self.quick_estimate_demo()
            elif choice == '3':
                self.show_system_info()
            elif choice == '4':
                self.show_material_factors()
            elif choice == '5':
                self.run_monte_carlo_demo()
            elif choice == '0':
                print("\n感谢使用！再见~ 👋")
                break
            else:
                print_warning("无效选择，请重新输入")
    
    def show_main_menu(self):
        """显示主菜单"""
        print_header("度量衡测不准关键因子配比估量估价系统 v3.0")
        print(f"{Colors.BOLD}主菜单:{Colors.ENDC}")
        print(f"  {Colors.CYAN}1{Colors.ENDC}. 📊 新建项目估算")
        print(f"  {Colors.CYAN}2{Colors.ENDC}. ⚡ 快速示例演示")
        print(f"  {Colors.CYAN}3{Colors.ENDC}. 📖 系统创新说明")
        print(f"  {Colors.CYAN}4{Colors.ENDC}. 🔧 材料因子查询")
        print(f"  {Colors.CYAN}5{Colors.ENDC}. 🎲 蒙特卡洛模拟演示")
        print(f"  {Colors.CYAN}0{Colors.ENDC}. 🚪 退出系统")
    
    def create_project(self):
        """创建新项目估算"""
        print_header("新建项目估算")
        
        # 1. 选择建筑类型
        building_types = {
            'R': '住宅', 'O': '办公', 'C': '商业',
            'H': '酒店', 'M': '医疗', 'E': '教育', 'I': '工业'
        }
        bt_choice = input_choice("请选择建筑类型:", building_types, 'O')
        bt_map = {
            'R': BuildingType.RESIDENTIAL, 'O': BuildingType.OFFICE,
            'C': BuildingType.COMMERCIAL, 'H': BuildingType.HOTEL,
            'M': BuildingType.HOSPITAL, 'E': BuildingType.EDUCATION,
            'I': BuildingType.INDUSTRIAL
        }
        building_type = bt_map[bt_choice]
        
        # 2. 选择结构类型
        structure_types = {
            'F': '框架', 'S': '剪力墙', 'FS': '框架-剪力墙',
            'FC': '框架-核心筒', 'ST': '钢结构'
        }
        st_choice = input_choice("请选择结构类型:", structure_types, 'FS')
        st_map = {
            'F': StructureType.FRAME, 'S': StructureType.SHEAR_WALL,
            'FS': StructureType.FRAME_SHEAR_WALL, 'FC': StructureType.FRAME_CORE_TUBE,
            'ST': StructureType.STEEL
        }
        structure_type = st_map[st_choice]
        
        # 3. 输入建筑面积
        total_area = input_int("总建筑面积 (㎡)", default=50000, min_val=100)
        
        # 4. 输入层数
        floor_count = input_int("地上层数", default=33, min_val=1, max_val=200)
        
        # 5. 地下室
        has_basement = input_yes_no("是否有地下室", default=True)
        basement_area = 0
        basement_floors = 0
        if has_basement:
            basement_ratio = input_float("地下室面积占地上面积比例", default=0.20, min_val=0)
            basement_area = total_area * basement_ratio
            basement_floors = input_int("地下室层数", default=2, min_val=1, max_val=5)
        
        # 6. 装修标准
        decoration_levels = {'1': '毛坯', '2': '简装', '3': '精装', '4': '豪装'}
        dl_choice = input_choice("装修标准:", decoration_levels, '3')
        decoration_level = decoration_levels[dl_choice]
        
        # 7. 是否有中央空调
        has_central_ac = input_yes_no("是否有中央空调", default=True)
        
        # 8. 是否有桩基
        has_pile = input_yes_no("是否有桩基工程", default=True)
        
        # 9. 地区选择
        regions = {
            'GZ': '广州', 'SZ': '深圳', 'ZH': '珠海',
            'ST': '汕头', 'SW': '汕尾', 'FS': '佛山', 'DG': '东莞'
        }
        region_choice = input_choice("请选择工程地区:", regions, 'SW')
        region_map = {
            'GZ': Region.GUANGZHOU, 'SZ': Region.SHENZHEN, 'ZH': Region.ZHUHAI,
            'ST': Region.SHANTOU, 'SW': Region.SHANWEI, 'FS': Region.FOSHAN,
            'DG': Region.DONGGUAN
        }
        region = region_map[region_choice]
        
        # 10. 年份
        year = input_int("造价基准年份", default=2026, min_val=2019, max_val=2030)
        
        # 构建项目参数
        self.current_project = ProjectParams(
            building_type=building_type,
            structure_type=structure_type,
            total_area=total_area,
            floor_count=floor_count,
            basement_area=basement_area,
            basement_floors=basement_floors,
            decoration_level=decoration_level,
            has_central_ac=has_central_ac,
            has_pile=has_pile,
            seismic_level="二级",
            region=region,
            year=year
        )
        
        # 执行估算
        print_section("正在执行估算...")
        result = self.estimator.estimate(self.current_project)
        
        # 显示结果
        self.display_result(result)
        
        # 保存项目
        self.save_project(result)
    
    def display_result(self, result: dict):
        """显示估算结果"""
        print_header("📊 估算结果报告")
        
        cost = result["造价估算"]
        
        print_section("项目基本信息")
        params = result["项目参数"]
        print_info("建筑类型", f"{params['building_type']['value']} ({params['structure_type']['value']})")
        print_info("总建筑面积", f"{params['total_area']:,.0f} ㎡")
        print_info("地上层数", f"{params['floor_count']} 层")
        print_info("地下室", f"{params['basement_area']:,.0f} ㎡ ({params['basement_floors']}层)")
        print_info("装修标准", params['decoration_level'])
        print_info("工程地区", f"{params['region']} (系数: {cost['地区系数']})")
        print_info("基准年份", cost['时间系数'])
        
        print_section("💰 造价估算")
        print(f"\n  {Colors.BOLD}单方造价区间:{Colors.ENDC}")
        print(f"    {Colors.GREEN}低限: {cost['单方造价区间']['低限']}{Colors.ENDC}")
        print(f"    {Colors.CYAN}中值: {cost['单方造价区间']['中值']}{Colors.ENDC}")
        print(f"    {Colors.YELLOW}高限: {cost['单方造价区间']['高限']}{Colors.ENDC}")
        
        print(f"\n  {Colors.BOLD}总造价区间:{Colors.ENDC}")
        print(f"    {Colors.GREEN}低限: {cost['总造价区间']['低限']}{Colors.ENDC}")
        print(f"    {Colors.CYAN}中值: {cost['总造价区间']['中值']}{Colors.ENDC}")
        print(f"    {Colors.YELLOW}高限: {cost['总造价区间']['高限']}{Colors.ENDC}")
        
        print(f"\n  {Colors.BOLD}地下室附加: {cost['地下室附加']}{Colors.ENDC}")
        
        # 配比参数亮点
        print_section("📐 关键配比参数")
        
        mep = result["配比参数"]["第三族_机电安装交叉配比"]
        print_info("风管展开面积", f"{mep['风管展开比']['展开面积']:,.0f} ㎡")
        print_info("弱电管线总长", f"{mep['弱电管线密度']['总长度']:,.0f} m")
        
        rebar = result["配比参数"]["第四族_钢筋智能配比"]["钢筋混凝土比"]
        print_info("钢筋混凝土比", f"{rebar['value']:.0f} kg/m³ ({rebar['range']})")
        print_info("估算钢筋总量", f"{rebar['估算钢筋量']:,.1f} 吨")
        
        foundation = result["配比参数"]["第五族_地基基础配比"]["桩长密度"]
        print_info("桩长密度", f"{foundation['value']:.1f} m/㎡ ({foundation['range']})")
        
        # 材料因子影响
        print_section("🔧 材料因子影响")
        impact = result["材料因子影响"]["_summary"]
        print_info("价格波动影响", impact['总影响幅度'])
        print_info("核心驱动", impact['核心驱动因子'])
        
        # 蒙特卡洛模拟
        mc = result["不确定性分析"]["蒙特卡洛模拟"]
        print_section("🎲 不确定性分析 (蒙特卡洛 10,000次)")
        print_info("P10(乐观)", f"{mc['P10']:,.0f} 元/㎡")
        print_info("P50(中性)", f"{mc['P50']:,.0f} 元/㎡")
        print_info("P90(保守)", f"{mc['P90']:,.0f} 元/㎡")
        print_info("估算精度", result["不确定性分析"]["估算精度等级"])
        
        print()
        print_success("估算完成！")
    
    def save_project(self, result: dict):
        """保存项目结果"""
        try:
            import json
            from datetime import datetime
            
            # 创建输出目录
            output_dir = os.path.join(os.path.dirname(__file__), '..', 'outputs')
            os.makedirs(output_dir, exist_ok=True)
            
            # 生成文件名
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"estimate_{timestamp}.json"
            filepath = os.path.join(output_dir, filename)
            
            # 保存结果
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(result, f, ensure_ascii=False, indent=2, default=str)
            
            print_success(f"结果已保存至: {filepath}")
        except Exception as e:
            print_warning(f"保存失败: {e}")
    
    def quick_estimate_demo(self):
        """快速示例演示"""
        print_header("⚡ 快速示例演示")
        
        examples = {
            '1': ('高层办公楼', {'building_type': '办公', 'structure_type': '框架-剪力墙',
                               'total_area': 50000, 'floor_count': 33, 'basement_area': 10000,
                               'decoration_level': '精装', 'has_central_ac': True}),
            '2': ('住宅小区', {'building_type': '住宅', 'structure_type': '剪力墙',
                              'total_area': 80000, 'floor_count': 26, 'basement_area': 20000,
                              'decoration_level': '精装', 'has_central_ac': False}),
            '3': ('商业综合体', {'building_type': '商业', 'structure_type': '框架-核心筒',
                               'total_area': 150000, 'floor_count': 8, 'basement_area': 50000,
                               'decoration_level': '精装', 'has_central_ac': True}),
        }
        
        print("请选择示例项目:")
        for key, (name, _) in examples.items():
            print(f"  {Colors.CYAN}{key}{Colors.ENDC}. {name}")
        
        choice = input("\n选择 [1-3]: ").strip()
        if choice not in examples:
            return
        
        name, params = examples[choice]
        print(f"\n正在执行 {name} 估算...")
        
        result = quick_estimate(**params)
        self.display_result(result)
    
    def show_system_info(self):
        """显示系统创新说明"""
        print_header("📖 度量衡测不准系统创新说明")
        
        info = self.estimator.get_innovation_summary()
        
        print(f"{Colors.BOLD}系统名称:{Colors.ENDC} {info['系统名称']}")
        print(f"{Colors.BOLD}版本:{Colors.ENDC} {info['版本']}")
        
        print_section("核心创新")
        for item in info['核心创新']:
            print(f"  • {item}")
        
        print_section("测不准三公理")
        for i, axiom in enumerate(info['测不准三公理'], 1):
            print(f"  {Colors.CYAN}{i}.{Colors.ENDC} {axiom}")
        
        print_section("精度等级")
        for level, desc in info['精度等级'].items():
            print(f"  {Colors.CYAN}{level}:{Colors.ENDC} {desc}")
        
        print_section("7族创新配比参数体系")
        families = [
            ("第一族", "结构构件交叉配比", "构件间体积守恒"),
            ("第二族", "建筑围护配比", "物理-成本关联"),
            ("第三族", "机电安装交叉配比", "跨系统关联"),
            ("第四族", "钢筋智能配比", "精细化控制"),
            ("第五族", "地基基础配比", "最大不确定性"),
            ("第六族", "装饰装修配比", "成本弹性最大"),
            ("第七族", "跨域综合配比", "系统共振"),
        ]
        for family, name, feature in families:
            print(f"  {Colors.CYAN}{family}:{Colors.ENDC} {name} - {feature}")
        
        print_section("6大关键材料因子")
        for code, factor in self.estimator.materials_db.FACTORS.items():
            print(f"  {Colors.CYAN}{code}:{Colors.ENDC} {factor.name}")
            print(f"      造价占比: {factor.cost_ratio:.0%} | 年波动率: ±{factor.annual_volatility:.0%}")
    
    def show_material_factors(self):
        """显示材料因子详情"""
        print_header("🔧 6大关键材料因子详情")
        
        for code, factor in self.estimator.materials_db.FACTORS.items():
            print(f"\n{Colors.BOLD}{Colors.CYAN}{code} {factor.name}{Colors.ENDC}")
            print(f"  规格: {factor.specification}")
            print(f"  当前价格: {Colors.YELLOW}{factor.current_price:,} 元/{factor.unit}{Colors.ENDC}")
            print(f"  造价占比: {factor.cost_ratio:.0%}")
            print(f"  年波动率: ±{factor.annual_volatility:.0%}")
            print(f"  价格趋势: {factor.price_trend}")
    
    def run_monte_carlo_demo(self):
        """蒙特卡洛模拟演示"""
        print_header("🎲 蒙特卡洛模拟演示")
        
        base_cost = input_float("请输入基准单方造价 (元/㎡)", default=4200, min_val=1000)
        n_simulations = input_int("模拟次数", default=10000, min_val=1000, max_val=100000)
        
        print(f"\n正在执行 {n_simulations:,} 次蒙特卡洛模拟...")
        
        result = self.estimator.monte_carlo_simulation(base_cost, n_simulations)
        
        print_section("模拟结果")
        print_info("模拟次数", f"{result['n_simulations']:,} 次")
        print_info("均值", f"{result['mean']:,.0f} 元/㎡")
        print_info("标准差", f"{result['std']:,.0f} 元/㎡")
        print()
        print(f"  {Colors.GREEN}P10 (乐观):{Colors.ENDC} {result['P10']:,.0f} 元/㎡")
        print(f"  {Colors.CYAN}P50 (中性):{Colors.ENDC} {result['P50']:,.0f} 元/㎡")
        print(f"  {Colors.YELLOW}P90 (保守):{Colors.ENDC} {result['P90']:,.0f} 元/㎡")
        
        # 计算置信区间
        print_section("置信区间")
        print_info("80%置信区间", f"{result['P10']:,.0f} ~ {result['P90']:,.0f} 元/㎡")
        print_info("波动幅度", f"+{(result['P90']-result['P50'])/result['P50']:.1%} / -{abs(result['P10']-result['P50'])/result['P50']:.1%}")


# ============================================================
# 主入口
# ============================================================

def main():
    """主入口函数"""
    try:
        menu = MenuSystem()
        menu.run()
        
    except KeyboardInterrupt:
        print("\n\n已退出系统。再见！")
    except Exception as e:
        print_error(f"发生错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
