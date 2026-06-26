#!/usr/bin/env python3
"""
MSD (Mean Squared Displacement) Analysis
Replacement for `gmx msd` which has selection bugs in GROMACS 2026 conda-forge.
Uses MDAnalysis for trajectory reading and numpy for MSD calculation.

Output: msd.xvg (GROMACS-compatible format), diffusion coefficient D (10^-5 cm^2/s)
"""
import numpy as np
import sys, os, argparse

def parse_args():
    p = argparse.ArgumentParser(description='Calculate MSD and diffusion coefficient')
    p.add_argument('-s', '--structure', required=True, help='TPR/GRO structure file')
    p.add_argument('-f', '--trajectory', required=True, help='XTC/TRR trajectory')
    p.add_argument('-o', '--output', default='msd.xvg', help='Output XVG file')
    p.add_argument('--selection', default='name CA', help='Atom selection (default: C-alpha)')
    p.add_argument('-b', '--begin', type=float, default=0, help='Start time (ps)')
    p.add_argument('-e', '--end', type=float, default=-1, help='End time (ps)')
    return p.parse_args()

def main():
    args = parse_args()
    
    # Lazy import
    import MDAnalysis as mda
    from MDAnalysis.analysis import msd as msd_analysis
    
    print(f"[MSD] Loading: {args.structure} + {args.trajectory}")
    u = mda.Universe(args.structure, args.trajectory)
    
    sel = u.select_atoms(args.selection)
    n_atoms = len(sel)
    n_frames = len(u.trajectory)
    dt = u.trajectory.dt  # ps
    
    print(f"[MSD] Atoms: {n_atoms}, Frames: {n_frames}, dt: {dt} ps, total: {n_frames*dt/1000:.2f} ns")
    
    if n_atoms == 0:
        print(f"[ERROR] No atoms selected with '{args.selection}'")
        sys.exit(1)
    
    # Calculate MSD
    msd_calc = msd_analysis.EinsteinMSD(u, select=args.selection, msd_type='xyz', fft=True)
    try:
        msd_calc.run()
    except ImportError:
        print("[MSD] tidynamics not found, using non-FFT MSD (slower)")
        msd_calc = msd_analysis.EinsteinMSD(u, select=args.selection, msd_type='xyz', fft=False)
        msd_calc.run()
    
    times = np.arange(n_frames) * dt  # ps
    msd_array = msd_calc.results.timeseries  # Å^2
    
    # Convert to nm^2
    msd_nm2 = msd_array / 100.0
    
    # Calculate diffusion coefficient from slope of MSD
    # D = MSD / (6 * t) for 3D (in nm^2/ps)
    # Use the linear region: skip first 10%, use up to 80%
    start_idx = max(1, int(n_frames * 0.1))
    end_idx = int(n_frames * 0.8)
    
    if end_idx - start_idx < 3:
        print("[WARNING] Too few frames for reliable D calculation")
        D_cm2_s_5 = 0.0
    else:
        # Linear fit: MSD = 6*D*t (in nm^2/ps)
        t_fit = times[start_idx:end_idx]
        msd_fit = msd_nm2[start_idx:end_idx]
        slope, intercept = np.polyfit(t_fit, msd_fit, 1)
        D_nm2_ps = slope / 6.0  # nm^2/ps
        D_cm2_s = D_nm2_ps * 1e-2  # convert nm^2/ps to 10^-5 cm^2/s
        # Actually: 1 nm^2/ps = 1e-6 cm^2/s, so:
        D_cm2_s_5 = D_nm2_ps * 1e-1  # 10^-5 cm^2/s
        print(f"\n[MSD] Diffusion coefficient D = {D_cm2_s_5:.4f} × 10^-5 cm^2/s")
        print(f"[MSD] R² = {np.corrcoef(t_fit, msd_fit)[0,1]**2:.4f}")
    
    # Write XVG
    with open(args.output, 'w') as f:
        f.write(f"@ title \"Mean Squared Displacement\"\n")
        f.write(f"@ xaxis label \"Time (ps)\"\n")
        f.write(f"@ yaxis label \"MSD (nm\\S2\\N)\"\n")
        f.write(f"@TYPE xy\n")
        f.write(f"@ view 0.15, 0.15, 0.75, 0.85\n")
        f.write(f"@ legend on\n")
        f.write(f"@ legend box on\n")
        f.write(f"@ legend loctype view\n")
        f.write(f"@ legend 0.78, 0.8\n")
        f.write(f"@ legend length 2\n")
        f.write(f"@ s0 legend \"MSD\"\n")
        f.write(f"@ s1 legend \"D = {D_cm2_s_5:.4f} x 10\\S-5\\N cm\\S2\\N/s\"\n")
        for i in range(n_frames):
            f.write(f"{times[i]:12.6f}  {msd_nm2[i]:12.6f}\n")
    
    print(f"[MSD] Output: {args.output}")
    return 0

if __name__ == '__main__':
    sys.exit(main())
