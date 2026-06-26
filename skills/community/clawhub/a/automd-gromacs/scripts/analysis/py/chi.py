#!/usr/bin/env python3
"""
Chi Angle Analysis
Replacement for `gmx chi` which has selection bugs in GROMACS 2026 conda-forge.
Calculates chi1 (N-CA-CB-CG) and chi2 (CA-CB-CG-CD) angles for specified residues.

Output: chi_angles.xvg (time series), chi_summary.txt (mean ± std)
"""
import numpy as np
import sys, os, argparse

def calc_dihedral(p1, p2, p3, p4):
    """Calculate dihedral angle between four points (in degrees)"""
    b1 = p2 - p1
    b2 = p3 - p2
    b3 = p4 - p3
    
    n1 = np.cross(b1, b2)
    n2 = np.cross(b2, b3)
    
    n1_norm = np.linalg.norm(n1)
    n2_norm = np.linalg.norm(n2)
    
    if n1_norm < 1e-10 or n2_norm < 1e-10:
        return 0.0
    
    n1 = n1 / n1_norm
    n2 = n2 / n2_norm
    
    cos_phi = np.clip(np.dot(n1, n2), -1.0, 1.0)
    phi = np.arccos(cos_phi)
    
    # Determine sign
    sign = np.sign(np.dot(np.cross(n1, n2), b2 / np.linalg.norm(b2)))
    if sign == 0:
        sign = 1
    
    return np.degrees(sign * phi)

def parse_args():
    p = argparse.ArgumentParser(description='Chi angle analysis for protein residues')
    p.add_argument('-s', '--structure', required=True, help='TPR/GRO structure file')
    p.add_argument('-f', '--trajectory', required=True, help='XTC/TRR trajectory')
    p.add_argument('-o', '--output', default='chi_angles', help='Output prefix')
    p.add_argument('-r', '--residues', default='all', help='Residue selection (e.g., "160,206,237" or "all")')
    p.add_argument('-b', '--begin', type=float, default=0, help='Start time (ps)')
    p.add_argument('-e', '--end', type=float, default=-1, help='End time (ps)')
    return p.parse_args()

def main():
    args = parse_args()
    
    import MDAnalysis as mda
    
    print(f"[CHI] Loading: {args.structure} + {args.trajectory}")
    u = mda.Universe(args.structure, args.trajectory)
    
    protein = u.select_atoms("protein")
    
    # Determine which residues to analyze
    if args.residues == 'all':
        residues = sorted(set(protein.residues.resids))
    else:
        residues = [int(x.strip()) for x in args.residues.split(',')]
    
    chi_atoms = {
        'chi1': ['N', 'CA', 'CB', 'CG'],
        'chi2': ['CA', 'CB', 'CG', 'CD'],
    }
    
    n_frames = len(u.trajectory)
    dt = u.trajectory.dt
    
    print(f"[CHI] Analyzing {len(residues)} residues over {n_frames} frames")
    
    # Store results: {chi_type: {resid: [angles...]}}
    chi_results = {}
    for chi_name in chi_atoms:
        chi_results[chi_name] = {}
    
    for ts in u.trajectory:
        for res in protein.residues:
            if res.resid not in residues:
                continue
            
            for chi_name, atom_names in chi_atoms.items():
                positions = []
                for aname in atom_names:
                    atom = res.atoms.select_atoms(f"name {aname}")
                    if len(atom) == 0:
                        positions.append(None)
                    else:
                        positions.append(atom[0].position)
                
                if any(p is None for p in positions):
                    continue
                
                angle = calc_dihedral(*positions)
                
                if res.resid not in chi_results[chi_name]:
                    chi_results[chi_name][res.resid] = []
                chi_results[chi_name][res.resid].append(angle)
    
    # Write results
    times = np.array([ts.time for ts in u.trajectory])
    
    for chi_name in chi_atoms:
        outfile = f"{args.output}_{chi_name}.xvg"
        with open(outfile, 'w') as f:
            f.write(f"@ title \"{chi_name} Angles\"\n")
            f.write(f"@ xaxis label \"Time (ps)\"\n")
            f.write(f"@ yaxis label \"Angle (degrees)\"\n")
            f.write(f"@TYPE xy\n")
            
            legend_num = 0
            header = f"{'Time(ps)':>12s}"
            active_residues = []
            
            for resid in sorted(chi_results[chi_name].keys()):
                if len(chi_results[chi_name][resid]) == n_frames:
                    active_residues.append(resid)
                    header += f"  {chi_name}({resid:>4d})"
                    f.write(f"@ s{legend_num} legend \"{chi_name} {resid}\"\n")
                    legend_num += 1
            
            f.write(f"{header}\n")
            
            for i in range(n_frames):
                line = f"{times[i]:12.4f}"
                for resid in active_residues:
                    line += f"  {chi_results[chi_name][resid][i]:12.4f}"
                f.write(f"{line}\n")
        
        print(f"[CHI] → {outfile} ({len(active_residues)} residues)")
        
        # Statistics
        for resid in active_residues:
            angles = np.array(chi_results[chi_name][resid])
            
            # Handle circular statistics for angles
            mean_rad = np.arctan2(np.mean(np.sin(np.radians(angles))),
                                  np.mean(np.cos(np.radians(angles))))
            mean_deg = np.degrees(mean_rad)
            
            # Circular std
            r = np.sqrt(np.mean(np.sin(np.radians(angles)))**2 + 
                       np.mean(np.cos(np.radians(angles)))**2)
            std_circ = np.degrees(np.sqrt(-2 * np.log(max(r, 1e-10))))
            
            if resid in [160, 206, 237]:  # Catalytic triad
                print(f"  {chi_name}({resid}): {mean_deg:.1f}° ± {std_circ:.1f}°")
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
