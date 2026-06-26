#!/usr/bin/env python3
"""
CP2K输入文件生成工具

这个脚本根据计算要求和结构文件生成CP2K输入文件。
支持从多种格式读取结构,并根据计算类型自动设置参数。
"""

import os
import sys
import argparse
from pathlib import Path
from typing import Dict, List, Tuple, Optional


class CP2KInputGenerator:
    """CP2K输入文件生成器"""
    
    def __init__(self):
        self.input_params = {}
        self.structure = None
        
    def parse_structure_file(self, filepath: str) -> Dict:
        """
        解析结构文件
        
        支持的格式: xyz, cif, pdb, gaussian
        """
        file_ext = Path(filepath).suffix.lower()
        
        if file_ext == '.xyz':
            return self._parse_xyz(filepath)
        elif file_ext == '.cif':
            return self._parse_cif(filepath)
        elif file_ext == '.pdb':
            return self._parse_pdb(filepath)
        elif file_ext == '.gjf' or file_ext == '.com':
            return self._parse_gaussian(filepath)
        else:
            raise ValueError(f"不支持的文件格式: {file_ext}")
    
    def _parse_xyz(self, filepath: str) -> Dict:
        """解析XYZ格式"""
        atoms = []
        coords = []
        
        with open(filepath, 'r') as f:
            lines = f.readlines()
        
        num_atoms = int(lines[0].strip())
        comment = lines[1].strip() if len(lines) > 1 else ""
        
        for line in lines[2:2+num_atoms]:
            parts = line.strip().split()
            atoms.append(parts[0])
            coords.append([float(x) for x in parts[1:4]])
        
        return {
            'num_atoms': num_atoms,
            'comment': comment,
            'atoms': atoms,
            'coords': coords,
            'format': 'xyz'
        }
    
    def _parse_cif(self, filepath: str) -> Dict:
        """解析CIF格式"""
        import re
        
        atoms = []
        coords = []
        cell = None
        
        with open(filepath, 'r') as f:
            content = f.read()
        
        # 解析晶胞参数
        cell_pattern = r'_cell_length_[abc]\s+([\d.]+)'
        cell_matches = re.findall(cell_pattern, content)
        if len(cell_matches) == 3:
            cell = [float(x) for x in cell_matches]
        
        # 解析原子坐标
        atom_pattern = r'([A-Z][a-z]?)\s+([\d\.-]+)\s+([\d\.-]+)\s+([\d\.-]+)'
        matches = re.findall(atom_pattern, content)
        
        for match in matches:
            atoms.append(match[0])
            coords.append([float(match[1]), float(match[2]), float(match[3])])
        
        return {
            'num_atoms': len(atoms),
            'atoms': atoms,
            'coords': coords,
            'cell': cell,
            'format': 'cif'
        }
    
    def _parse_pdb(self, filepath: str) -> Dict:
        """解析PDB格式"""
        atoms = []
        coords = []
        
        with open(filepath, 'r') as f:
            for line in f:
                if line.startswith('ATOM') or line.startswith('HETATM'):
                    atom_name = line[12:16].strip()
                    x = float(line[30:38].strip())
                    y = float(line[38:46].strip())
                    z = float(line[46:54].strip())
                    
                    # 提取元素符号
                    elem = atom_name[0]
                    if atom_name[0].isdigit():
                        elem = atom_name[1]
                    
                    atoms.append(elem)
                    coords.append([x, y, z])
        
        return {
            'num_atoms': len(atoms),
            'atoms': atoms,
            'coords': coords,
            'format': 'pdb'
        }
    
    def _parse_gaussian(self, filepath: str) -> Dict:
        """解析Gaussian格式"""
        atoms = []
        coords = []
        
        with open(filepath, 'r') as f:
            lines = f.readlines()
        
        # 跳过前两行
        started = False
        for line in lines[2:]:
            parts = line.strip().split()
            if len(parts) >= 4:
                if parts[0].isdigit() and not started:
                    continue
                started = True
                atoms.append(parts[0])
                coords.append([float(x) for x in parts[1:4]])
        
        return {
            'num_atoms': len(atoms),
            'atoms': atoms,
            'coords': coords,
            'format': 'gaussian'
        }
    
    def _guess_basis_set(self, element: str, system_size: int) -> str:
        """
        根据元素和体系大小推荐基组
        
        Args:
            element: 元素符号
            system_size: 体系大小
        """
        # 大体系使用DZVP,小体系使用TZVP
        if system_size > 200:
            return 'DZVP-MOLOPT-SR-GTH'
        else:
            return 'TZVP-MOLOPT-GTH'
    
    def _guess_potential(self, functional: str) -> str:
        """根据泛函推荐赝势"""
        if 'PBE' in functional.upper():
            return 'GTH-PBE'
        elif 'BLYP' in functional.upper():
            return 'GTH-BLYP'
        else:
            return 'GTH-PBE'
    
    def _determine_cutoff(self, system_size: int, basis_type: str) -> int:
        """确定CUTOFF值"""
        if system_size > 200:
            return 500
        elif system_size > 50:
            return 400
        else:
            return 350
    
    def _determine_kpoints(self, periodicity: str, cell_size: List[float]) -> List[int]:
        """
        根据周期性和晶胞大小确定k点
        
        Args:
            periodicity: 周期性方向 (XYZ/XY/Y/Z/NONE)
            cell_size: 晶胞向量长度 [a, b, c]
        """
        if periodicity == 'NONE':
            return [1, 1, 1]
        
        # 简单策略: 反比于晶胞大小
        kpoints = []
        for i, size in enumerate(cell_size[:3]):
            if periodicity[i] in ['X', 'Y', 'Z']:
                # 如果该方向是周期性的
                k = max(1, int(20.0 / size))
                kpoints.append(k)
            else:
                kpoints.append(1)
        
        return kpoints
    
    def generate_energy_input(
        self,
        structure_file: str,
        project_name: str = "energy",
        charge: int = 0,
        multiplicity: int = 1,
        functional: str = "PBE",
        method: str = "Quickstep",
        spin_polarized: bool = False,
        periodicity: str = "XYZ",
        **kwargs
    ) -> str:
        """
        生成单点能量计算输入文件
        
        Args:
            structure_file: 结构文件路径
            project_name: 项目名称
            charge: 净电荷
            multiplicity: 自旋多重度
            functional: 交换关联泛函
            method: 计算方法
            spin_polarized: 是否自旋极化
            periodicity: 周期性方向
        """
        # 解析结构
        struct = self.parse_structure_file(structure_file)
        
        # 确定参数
        system_size = struct['num_atoms']
        basis_type = self._guess_basis_set(struct['atoms'][0], system_size)
        potential = self._guess_potential(functional)
        cutoff = self._determine_cutoff(system_size, basis_type)
        
        # 确定k点
        kpoints = [1, 1, 1]
        if periodicity != 'NONE' and struct.get('cell'):
            kpoints = self._determine_kpoints(periodicity, struct['cell'])
        
        # 生成输入文件
        inp_lines = []
        inp_lines.append(f"#Generated from {Path(structure_file).name}")
        inp_lines.append("&GLOBAL")
        inp_lines.append(f"  PROJECT {project_name}")
        inp_lines.append("  PRINT_LEVEL LOW")
        inp_lines.append("  RUN_TYPE ENERGY")
        inp_lines.append("&END GLOBAL")
        inp_lines.append("")
        
        inp_lines.append("&FORCE_EVAL")
        inp_lines.append(f"  METHOD {method}")
        inp_lines.append("  &SUBSYS")
        
        # CELL部分
        if struct.get('cell'):
            inp_lines.append("    &CELL")
            inp_lines.append(f"      A     {struct['cell'][0]:.8f}     0.00000000     0.00000000")
            inp_lines.append(f"      B     0.00000000     {struct['cell'][1]:.8f}     0.00000000")
            inp_lines.append(f"      C     0.00000000     0.00000000     {struct['cell'][2]:.8f}")
            inp_lines.append(f"      PERIODIC {periodicity} #Direction of applied PBC")
            inp_lines.append("    &END CELL")
        
        # COORD部分
        inp_lines.append("    &COORD")
        for atom, coord in zip(struct['atoms'], struct['coords']):
            inp_lines.append(f"      {atom:<6}   {coord[0]:12.8f}   {coord[1]:12.8f}   {coord[2]:12.8f}")
        inp_lines.append("    &END COORD")
        
        # KIND部分
        unique_atoms = list(set(struct['atoms']))
        for atom in unique_atoms:
            inp_lines.append(f"    &KIND {atom}")
            inp_lines.append(f"      ELEMENT {atom}")
            inp_lines.append(f"      BASIS_SET {basis_type}")
            inp_lines.append(f"      POTENTIAL {potential}")
            inp_lines.append("    &END KIND")
        
        inp_lines.append("  &END SUBSYS")
        inp_lines.append("")
        
        # DFT部分
        inp_lines.append("  &DFT")
        inp_lines.append("    BASIS_SET_FILE_NAME  BASIS_MOLOPT")
        inp_lines.append("    POTENTIAL_FILE_NAME  POTENTIAL")
        inp_lines.append(f"    CHARGE    {charge} #Net charge")
        inp_lines.append(f"    MULTIPLICITY    {multiplicity} #Spin multiplicity")
        
        if spin_polarized:
            inp_lines.append("    UKS")
        
        # KPOINTS
        if periodicity != 'NONE' and sum(kpoints) > 3:
            inp_lines.append("    &KPOINTS")
            inp_lines.append(f"      SCHEME MONKHORST-PACK  {kpoints[0]}  {kpoints[1]}  {kpoints[2]}")
            inp_lines.append("      SYMMETRY F")
            inp_lines.append("    &END KPOINTS")
        
        inp_lines.append("    &QS")
        inp_lines.append("      EPS_DEFAULT 1E-10")
        inp_lines.append("    &END QS")
        
        # POISSON
        inp_lines.append("    &POISSON")
        if periodicity == 'NONE':
            inp_lines.append("      PERIODIC NONE")
            inp_lines.append("      PSOLVER MT")
        else:
            inp_lines.append(f"      PERIODIC {periodicity}")
            inp_lines.append("      PSOLVER PERIODIC")
        inp_lines.append("    &END POISSON")
        
        # XC
        inp_lines.append("    &XC")
        inp_lines.append(f"      &XC_FUNCTIONAL {functional}")
        inp_lines.append("      &END XC_FUNCTIONAL")
        inp_lines.append("    &END XC")
        
        # MGRID
        inp_lines.append("    &MGRID")
        inp_lines.append(f"      CUTOFF {cutoff}")
        inp_lines.append("      REL_CUTOFF 50")
        if 'TZVP' in basis_type:
            inp_lines.append("      NGRIDS 5")
        inp_lines.append("    &END MGRID")
        
        # SCF
        inp_lines.append("    &SCF")
        inp_lines.append("      MAX_SCF 128")
        inp_lines.append("      EPS_SCF 5.0E-06")
        inp_lines.append("      &DIAGONALIZATION")
        inp_lines.append("        ALGORITHM STANDARD")
        inp_lines.append("      &END DIAGONALIZATION")
        inp_lines.append("      &MIXING")
        inp_lines.append("        METHOD BROYDEN_MIXING")
        inp_lines.append("        ALPHA 0.4")
        inp_lines.append("        NBROYDEN 8")
        inp_lines.append("      &END MIXING")
        inp_lines.append("    &END SCF")
        inp_lines.append("  &END DFT")
        inp_lines.append("&END FORCE_EVAL")
        
        return "\n".join(inp_lines)
    
    def generate_geo_opt_input(
        self,
        structure_file: str,
        project_name: str = "opt",
        charge: int = 0,
        multiplicity: int = 1,
        functional: str = "PBE",
        optimizer: str = "BFGS",
        max_iter: int = 500,
        **kwargs
    ) -> str:
        """
        生成几何优化输入文件
        
        Args:
            structure_file: 结构文件路径
            project_name: 项目名称
            charge: 净电荷
            multiplicity: 自旋多重度
            functional: 交换关联泛函
            optimizer: 优化器 (BFGS/CG/LBFGS)
            max_iter: 最大迭代次数
        """
        # 先生成能量计算的基础部分
        inp = self.generate_energy_input(
            structure_file=structure_file,
            project_name=project_name,
            charge=charge,
            multiplicity=multiplicity,
            functional=functional,
            **kwargs
        )
        
        # 替换RUN_TYPE
        inp = inp.replace("RUN_TYPE ENERGY", "RUN_TYPE GEO_OPT")
        
        # 添加MOTION部分
        motion_section = f"""
&MOTION
  &GEO_OPT
    TYPE MINIMIZATION
    OPTIMIZER {optimizer}
    &{optimizer}
      TRUST_RADIUS 0.2
    &END {optimizer}
    MAX_ITER {max_iter}
    MAX_DR 3E-3
    RMS_DR 1.5E-3
    MAX_FORCE 4.5E-4
    RMS_FORCE 3E-4
  &END GEO_OPT
  &PRINT
    &TRAJECTORY
      FORMAT xyz
    &END TRAJECTORY
  &END PRINT
&END MOTION"""
        
        inp += motion_section
        
        return inp
    
    def generate_md_input(
        self,
        structure_file: str,
        project_name: str = "md",
        charge: int = 0,
        multiplicity: int = 1,
        functional: str = "PBE",
        ensemble: str = "NVT",
        steps: int = 50000,
        timestep: float = 0.5,
        temperature: float = 300.0,
        thermostat: str = "CSVR",
        timecon: float = 100.0,
        **kwargs
    ) -> str:
        """
        生成分子动力学输入文件
        
        Args:
            structure_file: 结构文件路径
            project_name: 项目名称
            charge: 净电荷
            multiplicity: 自旋多重度
            functional: 交换关联泛函
            ensemble: 系综 (NVT/NVE/NPT)
            steps: 步数
            timestep: 时间步长(fs)
            temperature: 温度(K)
            thermostat: 热浴类型
            timecon: 热浴时间常数(fs)
        """
        # 先生成基础部分
        inp = self.generate_energy_input(
            structure_file=structure_file,
            project_name=project_name,
            charge=charge,
            multiplicity=multiplicity,
            functional=functional,
            periodicity="XYZ",  # MD通常需要周期性
            **kwargs
        )
        
        # 替换RUN_TYPE
        inp = inp.replace("RUN_TYPE ENERGY", "RUN_TYPE MD")
        
        # 添加MOTION部分
        motion_section = f"""
&MOTION
  &MD
    ENSEMBLE {ensemble}
    STEPS {steps}
    TIMESTEP {timestep}
    TEMPERATURE {temperature}
    &THERMOSTAT
      TYPE {thermostat}
      &{thermostat}
        TIMECON {timecon}
      &END {thermostat}
    &END THERMOSTAT
  &END MD
  &PRINT
    &TRAJECTORY
      &EACH
        MD     10
      &END EACH
      FORMAT xyz
    &END TRAJECTORY
    &RESTART
      BACKUP_COPIES 0
      &EACH
        MD 10
      &END EACH
    &END RESTART
    &RESTART_HISTORY OFF
    &END RESTART_HISTORY
  &END PRINT
&END MOTION"""
        
        inp += motion_section
        
        return inp


def main():
    """命令行接口"""
    parser = argparse.ArgumentParser(description='CP2K输入文件生成工具')
    
    # 必需参数
    parser.add_argument('calculation_type', type=str,
                       choices=['energy', 'opt', 'md', 'freq'],
                       help='计算类型')
    parser.add_argument('structure_file', type=str,
                       help='结构文件路径')
    
    # 可选参数
    parser.add_argument('-o', '--output', type=str, default='function.inp',
                       help='输出文件名 (默认: function.inp)')
    parser.add_argument('-p', '--project', type=str, default='calculation',
                       help='项目名称')
    parser.add_argument('-c', '--charge', type=int, default=0,
                       help='净电荷 (默认: 0)')
    parser.add_argument('-m', '--multiplicity', type=int, default=1,
                       help='自旋多重度 (默认: 1)')
    parser.add_argument('-f', '--functional', type=str, default='PBE',
                       help='交换关联泛函 (默认: PBE)')
    
    # MD参数
    parser.add_argument('--ensemble', type=str, default='NVT',
                       help='系综 (默认: NVT)')
    parser.add_argument('--steps', type=int, default=50000,
                       help='MD步数 (默认: 50000)')
    parser.add_argument('--timestep', type=float, default=0.5,
                       help='时间步长 fs (默认: 0.5)')
    parser.add_argument('--temperature', type=float, default=300.0,
                       help='温度 K (默认: 300)')
    
    # 几何优化参数
    parser.add_argument('--optimizer', type=str, default='BFGS',
                       help='优化器 (默认: BFGS)')
    parser.add_argument('--max-iter', type=int, default=500,
                       help='最大迭代次数 (默认: 500)')
    
    args = parser.parse_args()
    
    # 检查结构文件
    if not os.path.exists(args.structure_file):
        print(f"错误: 结构文件不存在: {args.structure_file}")
        sys.exit(1)
    
    # 生成输入文件
    generator = CP2KInputGenerator()
    
    if args.calculation_type == 'energy':
        inp_content = generator.generate_energy_input(
            structure_file=args.structure_file,
            project_name=args.project,
            charge=args.charge,
            multiplicity=args.multiplicity,
            functional=args.functional
        )
    elif args.calculation_type == 'opt':
        inp_content = generator.generate_geo_opt_input(
            structure_file=args.structure_file,
            project_name=args.project,
            charge=args.charge,
            multiplicity=args.multiplicity,
            functional=args.functional,
            optimizer=args.optimizer,
            max_iter=args.max_iter
        )
    elif args.calculation_type == 'md':
        inp_content = generator.generate_md_input(
            structure_file=args.structure_file,
            project_name=args.project,
            charge=args.charge,
            multiplicity=args.multiplicity,
            functional=args.functional,
            ensemble=args.ensemble,
            steps=args.steps,
            timestep=args.timestep,
            temperature=args.temperature
        )
    else:
        print(f"错误: 不支持的计算类型: {args.calculation_type}")
        sys.exit(1)
    
    # 写入输出文件
    with open(args.output, 'w') as f:
        f.write(inp_content)
    
    print(f"✅ 成功生成CP2K输入文件: {args.output}")
    print(f"   计算类型: {args.calculation_type}")
    print(f"   结构文件: {args.structure_file}")


if __name__ == '__main__':
    main()
