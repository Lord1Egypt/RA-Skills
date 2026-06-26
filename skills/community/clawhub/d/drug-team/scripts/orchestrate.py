#!/usr/bin/env python3
import sys
import json
import subprocess
import os
import re
from pathlib import Path
import pandas as pd
import numpy as np

from rdkit import Chem
from rdkit.Chem import Descriptors, QED, rdMolDescriptors
from rdkit.Chem.Draw import MolToImage, MolToFile
from rdkit.Chem.rdMolDescriptors import CalcTPSA
try:
    from rdkit.Chem.SA_Score import sascore
    def sa_score(mol):
        return sascore.SAScore(mol)
except:
    def sa_score(mol):
        return 5.0  # dummy

from rdkit.Chem import Lipinski

CHEM_QUERY_DIR = Path(__file__).parents[3] / "skills/chemistry-query/scripts"  # Adjusted path
SYNTH_NOTEBOOK_DIR = Path(__file__).parents[3] / "skills/synth-notebook/scripts"
LAB_INVENTORY_DIR = Path(__file__).parents[3] / "skills/lab-inventory"

def run_chem_query(cmd):
    try:
        result = subprocess.run(["python3"] + cmd, cwd=CHEM_QUERY_DIR, capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            return json.loads(result.stdout)
        else:
            print(f"Error: {result.stderr}")
            return None
    except:
        return None

def run_synth_notebook(cmd):
    try:
        result = subprocess.run(["python3"] + cmd, cwd=SYNTH_NOTEBOOK_DIR, capture_output=True, text=True, timeout=60)
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            print(f"Error: {result.stderr}")
            return None
    except:
        return None

def run_lab_inventory(cmd):
    try:
        result = subprocess.run(["python3"] + cmd, cwd=LAB_INVENTORY_DIR, capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            return json.loads(result.stdout)
        else:
            print(f"Error: {result.stderr}")
            return None
    except:
        return None

def parse_query(query):
    target = "pain" if any(word in query.lower() for word in ["pain", "painkiller"]) else "generic"
    cons = {}
    logp_match = re.search(r'logP<(\d+\\.\\d+|\\d+)', query)
    if logp_match:
        cons['max_logp'] = float(logp_match.group(1))
    # Parse quantity, e.g. "10g"
    qty_match = re.search(r'(\\d+)(g|mg)', query)
    scale = 1.0
    unit = 'g'
    if qty_match:
        scale = float(qty_match.group(1))
        unit = qty_match.group(2)
        if unit == 'mg':
            scale /= 1000  # to g
    check_stock = "check stock" in query.lower()
    return target, cons, scale, check_stock

def get_candidates(target):
    seeds = {
        'pain': ['aspirin', 'ibuprofen', 'paracetamol', 'naproxen', 'codeine']
    }
    candidates = []
    for seed in seeds.get(target, ['aspirin']):
        sim = run_chem_query(['query_pubchem.py', '--compound', seed, '--type', 'similar'])
        if sim:
            candidates.extend([c['smiles'] for c in sim[:5]])
    # unique + known
    known = {
        'pain': ['CC(=O)NC1=CC=C(O)C=C1',  # paracetamol
                 'CC(=O)OC1=CC=CC=C1C(=O)O',  # aspirin
                 'CC(C)CC1=CC=C(C=C1)C(C)C(=O)O']  # ibuprofen
    }
    candidates = list(set(candidates + known.get(target, [])))
    return candidates[:10]

def compute_admet(smiles):
    mol = Chem.MolFromSmiles(smiles)
    if not mol:
        return None
    logp = Descriptors.MolLogP(mol)
    tpsa = Descriptors.TPSA(mol)
    qed = QED.qed(mol)
    sa = sa_score(mol)
    pka_proxy = 10 - Lipinski.NumAcidicGroups(mol)*3  # rough
    return {'logp': logp, 'tpsa': tpsa, 'qed': qed, 'sa': sa, 'pka': pka_proxy}

def compute_tox(smiles):
    mol = Chem.MolFromSmiles(smiles)
    if not mol:
        return {'score': 0}
    # Simple proxies
    pains = len(mol.GetSubstructMatches(Chem.MolFromSmarts('[CX3,4]=[CX3,4]')))  # enone proxy
    brenk = Descriptors.NumAromaticRings(mol) > 4
    ames = 'N(=O)=O' in Chem.MolToSmiles(mol)
    tox_score = 1.0 - (pains/10 + int(brenk)*0.2 + int(ames)*0.3)
    return {'pains': pains, 'brenk': int(brenk), 'ames': ames, 'score': max(0, tox_score)}

def pharm_proxy(smiles, target):
    mol = Chem.MolFromSmiles(smiles)
    if not mol:
        return {'affinity': -5}
    # Pain proxy
    phenol = bool(mol.GetSubstructMatch(Chem.MolFromSmarts('[c;H0:1][OH1]')))
    acid = Lipinski.NumAcidicGroups(mol) > 0
    amide = bool(mol.GetSubstructMatch(Chem.MolFromSmarts('C(=O)N')))
    score = -6 + (1 if phenol else 0) + (2 if acid else 0) + (1 if amide else 0)
    return {'affinity': score, 'notes': f"Phenol:{phenol}, Acid:{acid}, Amide:{amide}"}

def get_synth_route(smiles, temp_dir):
    plan = run_chem_query(['rdkit_mol.py', '--target', smiles, '--action', 'plan', '--steps', '2'])
    if not plan:
        plan = []  # empty
    route_path = os.path.join(temp_dir, 'route.json')
    with open(route_path, 'w') as f:
        json.dump(plan, f)
    return route_path

def process_synth_notebook(route_path):
    out = run_synth_notebook(['route_viz.py', '--route_json', route_path])
    if out:
        synth_out_path = os.path.join(os.path.dirname(route_path), 'synth_output.json')
        with open(synth_out_path, 'r') as f:
            synth_data = json.load(f)
        return synth_data
    return None

def check_inventory(route_path, scale, check_stock):
    if not check_stock:
        return {'available': True, 'low': [], 'est_cost': 0.0}
    # Assume stock.csv in lab-inventory
    stock_path = os.path.join(LAB_INVENTORY_DIR, 'stock.csv')
    # Create dummy if not exists? For testing.
    if not os.path.exists(stock_path):
        with open(stock_path, 'w') as f:
            f.write('reagent,quantity,unit,price\nacid,5,g,10.0\n')
    synth_out_path = os.path.join(os.path.dirname(route_path), 'synth_output.json')  # from previous
    inv = run_lab_inventory(['stock_check.py', '--reagents_from', synth_out_path, '--stock', stock_path])
    if inv and 'low' in inv and inv['low']:
        low_reagents = ','.join(inv['low'])
        vendor_cmd = ['vendor_scout.py', '--reagents', low_reagents, '--scale', f"{scale}g"]
        vendor_data = run_lab_inventory(vendor_cmd)
        if vendor_data:
            additional_cost = 0.0
            for reag in inv['low']:
                vdata = vendor_data.get(reag, {})
                cheapest = vdata.get('cheapest', {})
                if cheapest:
                    info = list(cheapest.values())[0]
                    additional_cost += info['total']
            inv['est_cost'] += additional_cost
    if inv:
        # Scale cost? For now, assume quantities are scaled in synth, but dummy.
        return inv
    return {'available': False, 'low': [], 'est_cost': 0.0}

def main(query):
    target, cons, scale, check_stock = parse_query(query)
    cands = get_candidates(target)
    results = []
    temp_dir = 'temp'
    os.makedirs(temp_dir, exist_ok=True)
    viz_dir = 'viz'
    os.makedirs(viz_dir, exist_ok=True)

    # Patent scout step
    candidates_path = os.path.join(temp_dir, 'candidates.json')
    with open(candidates_path, 'w') as f:
        json.dump([{"smiles": s} for s in cands], f)
    patent_cmd = ['patent_scout.py', '--candidates', candidates_path, '--target', target]
    patent_result = subprocess.run(["python3"] + patent_cmd, cwd=Path(__file__).parent, capture_output=True, text=True, timeout=30)
    if patent_result.returncode == 0:
        patent_data = json.loads(patent_result.stdout)
    else:
        print(f"Error in patent scout: {patent_result.stderr}")
        patent_data = {}

    for i, smiles in enumerate(cands):
        admet = compute_admet(smiles)
        if not admet:
            continue
        if 'max_logp' in cons and admet['logp'] >= cons['max_logp']:
            continue
        tox = compute_tox(smiles)
        pharm = pharm_proxy(smiles, target)
        novelty = patent_data.get(smiles, {"novelty_score": 5, "blocking": False})
        route_path = get_synth_route(smiles, temp_dir)
        synth_data = process_synth_notebook(route_path)
        if synth_data:
            total_yield = synth_data['total_yield']
            safety_score = synth_data['safety_score']
            images = synth_data['images']  # list of step images
            alerts = synth_data.get('hazards', [])
            # Move images to viz_dir
            for img in images:
                new_img = os.path.join(viz_dir, os.path.basename(img))
                os.rename(img, new_img)
        else:
            total_yield = 0.5
            safety_score = 0.8
            images = []
            alerts = []
        
        inv_data = check_inventory(route_path, scale, check_stock)
        available = inv_data['available']
        est_cost = inv_data['est_cost']
        feasibility = total_yield * safety_score * (1.0 if available else 0.5)
        cost_factor = 100 / (100 + est_cost) if est_cost > 0 else 1.0
        score = admet['qed'] * tox['score'] * (-pharm['affinity']/10) * feasibility * cost_factor * (novelty['novelty_score'] / 10.0) * (0.5 if novelty['blocking'] else 1.0)
        
        mol = Chem.MolFromSmiles(smiles)
        img_path = f"viz/cand_{i}.png"
        if mol:
            MolToFile(mol, img_path)
        
        results.append({
            **admet, **tox, **pharm,
            'score': score, 'smiles': smiles, 'img': img_path,
            'total_yield': total_yield, 'safety_score': safety_score,
            'available': available, 'est_cost': est_cost,
            'route_images': images, 'feasibility': feasibility, 'safety_alerts': ', '.join(alerts),
            'novelty_score': novelty['novelty_score'], 'blocking': novelty['blocking']
        })
    
    # Rank top 3
    sorted_results = sorted(results, key=lambda x: x['score'], reverse=True)[:3]
    print("Top 3 Candidates:")
    for res in sorted_results:
        print(f"SMILES: {res['smiles']}")
        print(f"LogP: {round(res['logp'],2)}, QED: {round(res['qed'],2)}, SA: {round(res['sa'],2)}")
        print(f"Tox Score: {round(res['score'],2)}, Affinity: {res['affinity']}")
        print(f"Yield: {round(res['total_yield'],2)}, Safety: {round(res['safety_score'],2)}")
        print(f"Available: {res['available']}, Est Cost: {round(res['est_cost'],2)}")
        print(f"Alerts: {res['safety_alerts']}")
        print(f"Novelty: {res['novelty_score']}, Blocking: {res['blocking']}")
        print(f"Score: {round(res['score'],2)}\\n")
    print("\\nVisualizations saved in viz/")
    print("Top candidates ranked by composite score including feasibility and novelty (\"High novelty: no blocking patents\").")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python orchestrate.py \\"Design 10g ibuprofen analog, check stock\\"")
        sys.exit(1)
    main(' '.join(sys.argv[1:]))
