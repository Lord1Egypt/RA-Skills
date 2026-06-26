#!/usr/bin/env python3
"""PDB file parser for extracting ligand info and computing docking pocket parameters.

Mirrors the logic from utils/pdb_parser.js, providing:
  - Ligand enumeration (excluding water and ions)
  - Automatic largest-ligand selection
  - Pocket center / size / radius calculation
  - site / site_label derivation
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Tuple

IONS = frozenset([
    "CL", "NA", "MG", "ZN", "CA", "FE", "MN", "CO", "CU", "NI", "K",
    "CD", "HG", "CS", "SR", "BA", "TL", "PB", "AU", "AG", "IR", "RU",
    "PT", "RH", "OS", "RE", "TC", "MO", "W", "V", "CR", "Y", "X",
    "ZR", "NB", "PD", "IN", "SN", "SB", "TE", "I", "XE", "LA", "CE",
    "PR", "ND", "PM", "SM", "EU", "GD", "TB", "DY", "HO", "ER", "TM",
    "YB", "LU", "HF", "TA", "BI", "PO", "AT", "RN", "FR", "RA", "AC",
    "TH", "PA", "U", "NP", "PU", "AM", "CM", "BK", "CF", "ES", "FM",
    "MD", "NO", "LR", "RF", "DB", "SG", "BH", "HS", "MT", "DS", "RG",
    "CN", "NH", "FL", "MC", "LV", "TS", "OG",
])


@dataclass
class LigandInfo:
    """A single ligand instance identified by (chain, residue_name, residue_id)."""
    chain: str
    residue_name: str
    residue_id: str
    coords: List[Tuple[float, float, float]] = field(default_factory=list)

    @property
    def atom_count(self) -> int:
        return len(self.coords)

    @property
    def key(self) -> str:
        """e.g. 'A:KY9:601'"""
        return f"{self.chain}:{self.residue_name}:{self.residue_id}"

    @property
    def site(self) -> str:
        """e.g. 'A:KY9'"""
        return f"{self.chain}:{self.residue_name}"

    @property
    def site_label(self) -> str:
        """e.g. 'A:KY9:601'"""
        return self.key


@dataclass
class PocketParams:
    """Docking pocket parameters derived from a ligand's bounding box."""
    site: str
    site_label: str
    center: Tuple[float, float, float]
    size: Tuple[float, float, float]
    radius: float


def parse_hetatm_line(line: str) -> Optional[Dict]:
    """Parse a single HETATM line from a PDB file.

    PDB fixed-width format:
      cols  1-6   record type
      cols 13-16  atom name
      cols 18-20  residue name
      col  22     chain ID
      cols 23-26  residue sequence number (+ insertion code at col 27)
      cols 31-38  x coordinate
      cols 39-46  y coordinate
      cols 47-54  z coordinate
    """
    if not line.startswith("HETATM"):
        return None
    try:
        residue_name = line[17:20].strip()
        chain = line[21:22].strip()
        residue_id = line[22:27].strip()
        x = float(line[30:38].strip())
        y = float(line[38:46].strip())
        z = float(line[46:54].strip())
    except (ValueError, IndexError):
        return None
    return {
        "residue_name": residue_name,
        "chain": chain,
        "residue_id": residue_id,
        "x": x, "y": y, "z": z,
    }


def parse_ligands(pdb_text: str) -> List[LigandInfo]:
    """Extract all non-water, non-ion ligands grouped by (chain, name, residue_id)."""
    ligand_map: Dict[str, LigandInfo] = {}
    for line in pdb_text.splitlines():
        parsed = parse_hetatm_line(line)
        if parsed is None:
            continue
        rname = parsed["residue_name"]
        if rname == "HOH" or rname in IONS:
            continue
        key = f"{parsed['chain']}:{rname}:{parsed['residue_id']}"
        if key not in ligand_map:
            ligand_map[key] = LigandInfo(
                chain=parsed["chain"],
                residue_name=rname,
                residue_id=parsed["residue_id"],
            )
        ligand_map[key].coords.append((parsed["x"], parsed["y"], parsed["z"]))
    return list(ligand_map.values())


def find_largest_ligand(ligands: List[LigandInfo], min_atoms: int = 6) -> Optional[LigandInfo]:
    """Return the ligand with the most atoms (>= min_atoms) as the default binding site."""
    candidates = [lig for lig in ligands if lig.atom_count >= min_atoms]
    if not candidates:
        return None
    return max(candidates, key=lambda l: l.atom_count)


def find_ligand_by_site(
    ligands: List[LigandInfo],
    site_selector: str,
    min_atoms: int = 1,
) -> Optional[LigandInfo]:
    """Find ligand by site selector.

    Accepted selector formats:
      - chain:resname         (e.g. A:OQ4)
      - chain:resname:resid   (e.g. A:OQ4:601)
    """
    selector = (site_selector or "").strip()
    if not selector:
        return None

    parts = selector.split(":")
    if len(parts) not in (2, 3):
        return None

    chain = parts[0].strip()
    residue_name = parts[1].strip()
    residue_id = parts[2].strip() if len(parts) == 3 else None

    candidates = [
        lig
        for lig in ligands
        if lig.chain == chain
        and lig.residue_name == residue_name
        and lig.atom_count >= min_atoms
        and (residue_id is None or lig.residue_id == residue_id)
    ]
    if not candidates:
        return None

    # If only site (without residue id) is provided, choose the largest instance.
    return max(candidates, key=lambda l: l.atom_count)


def compute_pocket(ligand: LigandInfo, expand: float = 10.0) -> PocketParams:
    """Derive docking pocket center / size / radius from a ligand's atom coordinates.

    Args:
        ligand: The ligand whose bounding box defines the pocket.
        expand: Extra padding (Angstroms) added to each dimension of the bounding box.
                Default 10 Å is a common choice for molecular docking.
    """
    xs = [c[0] for c in ligand.coords]
    ys = [c[1] for c in ligand.coords]
    zs = [c[2] for c in ligand.coords]

    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)
    min_z, max_z = min(zs), max(zs)

    cx = (max_x + min_x) / 2.0
    cy = (max_y + min_y) / 2.0
    cz = (max_z + min_z) / 2.0

    sx = (max_x - min_x) + expand
    sy = (max_y - min_y) + expand
    sz = (max_z - min_z) + expand

    radius = max(
        math.sqrt((x - cx) ** 2 + (y - cy) ** 2 + (z - cz) ** 2)
        for x, y, z in ligand.coords
    ) + expand / 2.0

    return PocketParams(
        site=ligand.site,
        site_label=ligand.site_label,
        center=(round(cx, 3), round(cy, 3), round(cz, 3)),
        size=(round(sx, 3), round(sy, 3), round(sz, 3)),
        radius=round(radius, 4),
    )


def auto_pocket_from_pdb(pdb_text: str, expand: float = 10.0) -> Optional[PocketParams]:
    """One-shot: parse PDB text -> find largest ligand -> compute pocket params."""
    ligands = parse_ligands(pdb_text)
    largest = find_largest_ligand(ligands)
    if largest is None:
        return None
    return compute_pocket(largest, expand=expand)


def auto_pocket_from_pdb_with_site(
    pdb_text: str,
    site_selector: str,
    expand: float = 10.0,
) -> Optional[PocketParams]:
    """Parse PDB text and compute pocket for a specific site selector."""
    ligands = parse_ligands(pdb_text)
    selected = find_ligand_by_site(ligands, site_selector=site_selector, min_atoms=1)
    if selected is None:
        return None
    return compute_pocket(selected, expand=expand)


def auto_pocket_from_file(pdb_path: str, expand: float = 10.0) -> Optional[PocketParams]:
    """Convenience wrapper that reads a PDB file from disk."""
    text = Path(pdb_path).read_text(encoding="utf-8", errors="replace")
    return auto_pocket_from_pdb(text, expand=expand)


def auto_pocket_from_file_with_site(
    pdb_path: str,
    site_selector: str,
    expand: float = 10.0,
) -> Optional[PocketParams]:
    """Read a PDB file and compute pocket params for a specific site selector."""
    text = Path(pdb_path).read_text(encoding="utf-8", errors="replace")
    return auto_pocket_from_pdb_with_site(text, site_selector=site_selector, expand=expand)


# ---------------------------------------------------------------------------
# CLI: quick inspection of a local PDB file
# ---------------------------------------------------------------------------
def main() -> None:
    import argparse, json  # noqa: E401

    parser = argparse.ArgumentParser(description="Parse PDB and print pocket params for the largest ligand.")
    parser.add_argument("pdb_file", help="Path to a .pdb file")
    parser.add_argument("--expand", type=float, default=10.0, help="Bounding-box padding in Angstroms (default: 10)")
    parser.add_argument("--site", default=None, help="Optional site selector: chain:resname or chain:resname:resid")
    parser.add_argument("--list-ligands", action="store_true", help="List all ligands found")
    args = parser.parse_args()

    text = Path(args.pdb_file).read_text(encoding="utf-8", errors="replace")
    ligands = parse_ligands(text)

    if args.list_ligands:
        print(f"Found {len(ligands)} ligand(s):")
        for lig in sorted(ligands, key=lambda l: -l.atom_count):
            print(f"  {lig.key}  atoms={lig.atom_count}")

    selected = None
    if args.site:
        selected = find_ligand_by_site(ligands, args.site, min_atoms=1)
    if selected is None:
        selected = find_largest_ligand(ligands)
    if selected is None:
        print("No ligand with >= 6 atoms found.")
        return

    pocket = compute_pocket(selected, expand=args.expand)
    print(json.dumps({
        "selected_ligand": selected.key,
        "atom_count": selected.atom_count,
        "site": pocket.site,
        "site_label": pocket.site_label,
        "center": list(pocket.center),
        "size": list(pocket.size),
        "radius": pocket.radius,
    }, indent=2))


if __name__ == "__main__":
    main()
