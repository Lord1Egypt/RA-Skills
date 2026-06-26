#!/usr/bin/env python3
"""
Residue Pair Distance Analysis
Replacement for `gmx distance` which has -select bugs in GROMACS 2026 conda-forge.
Tracks distances between specified residue pairs over the trajectory.

Output: distance_<pair>.xvg (GROMACS-compatible format)
"""
import numpy as np
import sys, os, argparse

def parse_args():
    p = argparse.ArgumentParser(description='Track residue pair distances')
    p.add_argument('-s', '--structure', required=True, help='TPR/GRO structure file')
    p.add_argument('-f', '--trajectory', required=True, help='XTC/TRR trajectory')
    p.add_argument('-o', '--output', default='distance', help='Output prefix')
    p.add_argument('-p', '--pairs', required=True, nargs='+', 
                   help='Residue pairs: "160-206" "206-237" (multiple allowed)')
    p.add_argument('-b', '--begin', type=float, default=0, help='Start time (ps)')
    p.add_argument('-e', '--end', type=float, default=-1, help='End time (ps)')
    return p.parse_args()

def main():
    args = parse_args()
    
    import MDAnalysis as mda
    
    print(f"[DIST] Loading: {args.structure} + {args.trajectory}")
    u = mda.Universe(args.structure, args.trajectory)
    dt = u.trajectory.dt
    n_frames = len(u.trajectory)
    
    print(f"[DIST] Trajectory: {n_frames} frames, dt={dt} ps, total={n_frames*dt/1000:.2f} ns")
    
    all_results = {}
    
    for pair_str in args.pairs:
        parts = pair_str.replace('-', ' ').split()
        if len(parts) != 2:
            print(f"[WARNING] Invalid pair format: {pair_str}, skip")
            continue
        
        r1, r2 = parts
        
        # Select atoms for each residue (use CA for protein)
        sel1 = u.select_atoms(f"resid {r1} and name CA")
        sel2 = u.select_atoms(f"resid {r2} and name CA")
        
        if len(sel1) == 0 or len(sel2) == 0:
            print(f"[WARNING] Residue pair {r1}-{r2}: no CA atoms found, using all heavy atoms")
            sel1 = u.select_atoms(f"resid {r1} and not name H*")
            sel2 = u.select_atoms(f"resid {r2} and not name H*")
        
        if len(sel1) == 0 or len(sel2) == 0:
            print(f"[ERROR] Residue {r1} or {r2} not found")
            continue
        
        # Calculate COM distance over trajectory
        distances = np.zeros(n_frames)
        times = np.zeros(n_frames)
        
        for ts in u.trajectory:
            i = ts.frame
            times[i] = ts.time
            com1 = sel1.center_of_mass()
            com2 = sel2.center_of_mass()
            distances[i] = np.linalg.norm(com1 - com2) / 10.0  # Å to nm
        
        # Statistics
        mean_d = np.mean(distances)
        std_d = np.std(distances)
        min_d = np.min(distances)
        max_d = np.max(distances)
        
        print(f"\n[DIST] {r1}-{r2}: mean={mean_d:.3f} nm, std={std_d:.3f}, min={min_d:.3f}, max={max_d:.3f}")
        
        # Write XVG
        outfile = f"{args.output}_{r1}_{r2}.xvg"
        with open(outfile, 'w') as f:
            f.write(f"@ title \"Distance: Residues {r1}-{r2}\"\n")
            f.write(f"@ xaxis label \"Time (ps)\"\n")
            f.write(f"@ yaxis label \"Distance (nm)\"\n")
            f.write(f"@TYPE xy\n")
            f.write(f"@ s0 legend \"d({r1}-{r2})\"\n")
            for i in range(n_frames):
                f.write(f"{times[i]:12.6f}  {distances[i]:12.6f}\n")
        
        all_results[pair_str] = {'mean': mean_d, 'std': std_d, 'file': outfile}
        print(f"[DIST] → {outfile}")
    
    # Summary
    print("\n[DIST] Summary:")
    for k, v in all_results.items():
        print(f"  {k}: {v['mean']:.3f} ± {v['std']:.3f} nm → {v['file']}")
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
