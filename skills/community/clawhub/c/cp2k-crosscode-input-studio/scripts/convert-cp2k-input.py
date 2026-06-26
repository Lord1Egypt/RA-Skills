#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Dict, List, Tuple


def read_text(path: str) -> str:
    return Path(path).read_text(encoding='utf-8')


def write_text(path: str, text: str) -> None:
    Path(path).write_text(text.rstrip() + '\n', encoding='utf-8')


def parse_cp2k(inp: str) -> Dict:
    lines = inp.splitlines()
    data = {
        'project': 'converted_job',
        'run_type': 'ENERGY',
        'charge': 0,
        'multiplicity': 1,
        'periodicity': 'NONE',
        'kpoints': [1, 1, 1],
        'cell': None,
        'coords': [],
        'warnings': [],
        'xc_functional': 'PBE',
    }
    in_coord = False
    for line in lines:
        s = line.strip()
        if s.startswith('PROJECT '):
            data['project'] = s.split(None, 1)[1]
        elif s.startswith('RUN_TYPE '):
            data['run_type'] = s.split(None, 1)[1]
        elif s.startswith('CHARGE '):
            data['charge'] = int(float(s.split()[1]))
        elif s.startswith('MULTIPLICITY '):
            data['multiplicity'] = int(float(s.split()[1]))
        elif s.startswith('PERIODIC '):
            data['periodicity'] = s.split()[1]
        elif s.startswith('SCHEME MONKHORST-PACK'):
            parts = s.split()[2:5]
            if len(parts) == 3:
                data['kpoints'] = [int(x) for x in parts]
        elif s.startswith('&COORD'):
            in_coord = True
            continue
        elif s.startswith('&END COORD'):
            in_coord = False
            continue
        elif in_coord and s:
            parts = s.split()
            if len(parts) >= 4:
                data['coords'].append((parts[0], float(parts[1]), float(parts[2]), float(parts[3])))
        elif s.startswith('A '):
            m = re.match(r'A\s+([\dEe+\-.]+)\s+([\dEe+\-.]+)\s+([\dEe+\-.]+)', s)
            if m:
                data.setdefault('_cell_rows', {})['A'] = tuple(float(x) for x in m.groups())
        elif s.startswith('B '):
            m = re.match(r'B\s+([\dEe+\-.]+)\s+([\dEe+\-.]+)\s+([\dEe+\-.]+)', s)
            if m:
                data.setdefault('_cell_rows', {})['B'] = tuple(float(x) for x in m.groups())
        elif s.startswith('C '):
            m = re.match(r'C\s+([\dEe+\-.]+)\s+([\dEe+\-.]+)\s+([\dEe+\-.]+)', s)
            if m:
                data.setdefault('_cell_rows', {})['C'] = tuple(float(x) for x in m.groups())
        elif s.startswith('&PBE') or s == '&PBE':
            data['xc_functional'] = 'PBE'
        elif s.startswith('&B3LYP') or s == '&B3LYP':
            data['xc_functional'] = 'B3LYP'
        elif s.startswith('&PBE0') or s == '&PBE0':
            data['xc_functional'] = 'PBE0'
    rows = data.pop('_cell_rows', None)
    if rows and all(k in rows for k in ['A', 'B', 'C']):
        data['cell'] = [rows['A'], rows['B'], rows['C']]
    if not data['coords']:
        data['warnings'].append('No explicit &COORD block was parsed; conversion may be incomplete')
    return data


def gaussian_method(xc: str) -> str:
    mapping = {'PBE': 'PBE1PBE', 'PBE0': 'PBE1PBE', 'B3LYP': 'B3LYP'}
    return mapping.get(xc.upper(), 'PBE1PBE')


def gaussian_route(data: Dict) -> str:
    run_type = data['run_type'].upper()
    parts = [gaussian_method(data['xc_functional']), 'Def2SVP']
    if run_type == 'GEO_OPT':
        parts.append('Opt')
    elif run_type == 'VIBRATIONAL_ANALYSIS':
        parts.append('Freq')
    elif run_type == 'CELL_OPT':
        parts.append('Opt')
        data['warnings'].append('CELL_OPT was downgraded to molecular Opt semantics for Gaussian draft review')
    if data['periodicity'] != 'NONE':
        data['warnings'].append('Periodic CP2K job mapped into Gaussian draft; review whether a molecular cluster model is scientifically appropriate')
    return '#P ' + ' '.join(parts)


def render_gaussian(data: Dict) -> str:
    coords = '\n'.join(f'{el} {x:.8f} {y:.8f} {z:.8f}' for el, x, y, z in data['coords'])
    warnings = '\n'.join(f'! WARNING: {w}' for w in data['warnings'])
    return f"{warnings}\n{gaussian_route(data)}\n\nConverted from CP2K draft: {data['project']}\n\n{data['charge']} {data['multiplicity']}\n{coords}\n\n"


def render_orca(data: Dict) -> str:
    route_parts = [gaussian_method(data['xc_functional']).replace('PBE1PBE', 'PBE0'), 'def2-SVP']
    rt = data['run_type'].upper()
    if rt == 'GEO_OPT':
        route_parts.append('Opt')
    elif rt == 'VIBRATIONAL_ANALYSIS':
        route_parts.append('Freq')
    elif rt == 'CELL_OPT':
        route_parts.append('Opt')
        data['warnings'].append('CELL_OPT was reduced to Opt-like ORCA draft semantics')
    if data['periodicity'] != 'NONE':
        data['warnings'].append('Periodic CP2K job mapped into ORCA draft; confirm a finite cluster model is scientifically appropriate')
    warnings = '\n'.join(f'# WARNING: {w}' for w in data['warnings'])
    coords = '\n'.join(f'  {el} {x:.8f} {y:.8f} {z:.8f}' for el, x, y, z in data['coords'])
    return f"{warnings}\n! {' '.join(route_parts)}\n\n* xyz {data['charge']} {data['multiplicity']}\n{coords}\n*\n"


def vec_to_line(v: Tuple[float, float, float]) -> str:
    return f'{v[0]:.8f} {v[1]:.8f} {v[2]:.8f}'


def grouped_species(coords: List[Tuple[str, float, float, float]]):
    counts = Counter(el for el, *_ in coords)
    order = []
    seen = set()
    for el, *_ in coords:
        if el not in seen:
            order.append(el)
            seen.add(el)
    grouped = [c for el in order for c in coords if c[0] == el]
    return order, [counts[el] for el in order], grouped


def render_poscar(data: Dict) -> str:
    order, counts, grouped = grouped_species(data['coords'])
    if data['cell'] is None:
        data['warnings'].append('No explicit periodic cell found; using a boxed molecular cell for VASP draft review')
        data['cell'] = [(20.0, 0.0, 0.0), (0.0, 20.0, 0.0), (0.0, 0.0, 20.0)]
    lines = [
        f"{data['project']} converted from CP2K",
        '1.0',
        vec_to_line(data['cell'][0]),
        vec_to_line(data['cell'][1]),
        vec_to_line(data['cell'][2]),
        ' '.join(order),
        ' '.join(str(c) for c in counts),
        'Cartesian',
    ]
    lines.extend(f'{x:.8f} {y:.8f} {z:.8f}' for _, x, y, z in grouped)
    return '\n'.join(lines) + '\n'


def render_kpoints(data: Dict) -> str:
    if data['periodicity'] == 'NONE':
        data['warnings'].append('Nonperiodic CP2K job mapped to Gamma-only boxed VASP draft')
        grid = [1, 1, 1]
    else:
        grid = data['kpoints']
    return '\n'.join(['Automatic mesh', '0', 'Monkhorst-Pack', ' '.join(str(x) for x in grid), '0 0 0']) + '\n'


def render_incar(data: Dict) -> str:
    run_type = data['run_type'].upper()
    lines = [
        f'SYSTEM = {data["project"]} converted from CP2K',
        'ENCUT = 520',
        f'ISPIN = {2 if data["multiplicity"] > 1 else 1}',
        f'NELECT = auto  ! review against CP2K charge={data["charge"]}',
        'EDIFF = 1E-6',
    ]
    if run_type in {'GEO_OPT', 'CELL_OPT'}:
        lines += ['IBRION = 2', 'NSW = 200', 'ISIF = 3' if run_type == 'CELL_OPT' else 'ISIF = 2']
    else:
        lines += ['IBRION = -1', 'NSW = 0']
    if run_type == 'VIBRATIONAL_ANALYSIS':
        lines.append('! Vibrational analysis is not directly translated; review finite-difference workflow manually')
    lines.append('! POTCAR must be assembled manually; this converter does not fabricate pseudopotentials')
    return '\n'.join(lines) + '\n'


def qe_calculation(data: Dict) -> str:
    rt = data['run_type'].upper()
    if rt == 'GEO_OPT':
        return 'relax'
    if rt == 'CELL_OPT':
        return 'vc-relax'
    return 'scf'


def qe_kpoints(data: Dict) -> str:
    if data['periodicity'] == 'NONE':
        data['warnings'].append('Nonperiodic CP2K job mapped into boxed Quantum ESPRESSO draft')
        return 'K_POINTS gamma\n'
    return 'K_POINTS automatic\n' + ' '.join(str(x) for x in data['kpoints']) + ' 0 0 0\n'


def render_qe(data: Dict) -> str:
    if data['cell'] is None:
        data['warnings'].append('No explicit periodic cell found; using a boxed molecular cell for Quantum ESPRESSO draft review')
        data['cell'] = [(20.0, 0.0, 0.0), (0.0, 20.0, 0.0), (0.0, 0.0, 20.0)]
    species = []
    seen = set()
    for el, *_ in data['coords']:
        if el not in seen:
            seen.add(el)
            species.append(el)
    nat = len(data['coords'])
    ntyp = len(species)
    pseudo_lines = '\n'.join(f'  {el}  1.0  {el}.UPF  ! placeholder, replace manually' for el in species)
    coord_lines = '\n'.join(f'  {el}  {x:.8f} {y:.8f} {z:.8f}' for el, x, y, z in data['coords'])
    cell_lines = '\n'.join('  ' + vec_to_line(v) for v in data['cell'])
    spinpol = '.true.' if data['multiplicity'] > 1 else '.false.'
    return (
        f"&CONTROL\n  calculation = '{qe_calculation(data)}'\n  prefix = '{data['project']}'\n/\n"
        f"&SYSTEM\n  ibrav = 0\n  nat = {nat}\n  ntyp = {ntyp}\n  ecutwfc = 60\n  nspin = {2 if data['multiplicity'] > 1 else 1}\n  starting_magnetization(1) = {0.5 if data['multiplicity'] > 1 else 0.0}\n/\n"
        f"&ELECTRONS\n  conv_thr = 1.0d-8\n/\n"
        f"ATOMIC_SPECIES\n{pseudo_lines}\n"
        f"ATOMIC_POSITIONS angstrom\n{coord_lines}\n"
        f"CELL_PARAMETERS angstrom\n{cell_lines}\n"
        f"{qe_kpoints(data)}"
    )


def parse_args():
    p = argparse.ArgumentParser(description='Convert a generated CP2K draft into Gaussian, VASP, ORCA, or Quantum ESPRESSO draft inputs')
    p.add_argument('cp2k_input')
    p.add_argument('target', choices=['gaussian', 'vasp', 'orca', 'qe'])
    p.add_argument('-o', '--output', default='converted_out')
    return p.parse_args()


def main() -> None:
    args = parse_args()
    data = parse_cp2k(read_text(args.cp2k_input))
    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=True)
    if args.target == 'gaussian':
        write_text(str(out / f"{data['project']}.gjf"), render_gaussian(data))
        print(out / f"{data['project']}.gjf")
    elif args.target == 'orca':
        write_text(str(out / f"{data['project']}.inp"), render_orca(data))
        print(out / f"{data['project']}.inp")
    elif args.target == 'qe':
        write_text(str(out / 'pw.in'), render_qe(data))
        write_text(str(out / 'WARNINGS.txt'), '\n'.join(data['warnings']) + '\n' if data['warnings'] else 'No extra warnings\n')
        print(out / 'pw.in')
        print(out / 'WARNINGS.txt')
    else:
        write_text(str(out / 'POSCAR'), render_poscar(data))
        write_text(str(out / 'KPOINTS'), render_kpoints(data))
        write_text(str(out / 'INCAR'), render_incar(data))
        write_text(str(out / 'WARNINGS.txt'), '\n'.join(data['warnings']) + '\n' if data['warnings'] else 'No extra warnings\n')
        print(out / 'POSCAR')
        print(out / 'KPOINTS')
        print(out / 'INCAR')
        print(out / 'WARNINGS.txt')


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f'Error: {e}', file=sys.stderr)
        sys.exit(1)
