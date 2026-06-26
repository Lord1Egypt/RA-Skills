import argparse
import requests
import json
import re
from Bio import SeqIO
from Bio.Seq import Seq

def fetch_ncbi_sequence(accession, start=None, end=None):
    print(f"Fetching sequence for {accession}...")
    url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nuccore&id={accession}&rettype=fasta&retmode=text"
    if start and end:
        url += f"&seq_start={start}&seq_stop={end}"
    
    response = requests.get(url)
    if response.status_code == 200:
        lines = response.text.split('\n')
        return "".join(lines[1:])
    return None

def score_sgrna(seq):
    """
    Bio-chat Score: Modified Rule Set 2 for high GC.
    Base values + position weights + GC correction.
    """
    seq = seq.upper()
    gc = (seq.count('G') + seq.count('C')) / 20.0
    
    # Base score start
    score = 50.0
    
    # GC Penalty/Reward for high GC context (PRV context)
    if 0.5 <= gc <= 0.8:
        score += 15 # Optimal for strong binding in GC context
    elif gc > 0.8 or gc < 0.4:
        score -= 20 # Structural or stability penalty
        
    # Seed region weighting (Positions 15-20 near PAM)
    seed = seq[14:20]
    score += seed.count('G') * 5
    score += seed.count('C') * 5
    
    # Rule Set 2 simple heuristics
    if seq[19] == 'G': score += 10 # G at pos 20 is good
    if seq[19] == 'C': score -= 5
    
    return min(max(int(score), 0), 100)

def design_sgrnas(target_seq, relative_to=0):
    candidates = []
    # Scan for NGG (SpCas9)
    for i in range(len(target_seq) - 23):
        sub = target_seq[i:i+23]
        if sub.endswith('GG'):
            sg = sub[:20]
            pam = sub[20:]
            score = score_sgrna(sg)
            
            # Cut site is 3bp upstream of PAM
            cut_pos = i + 17
            candidates.append({
                "sgRNA": sg,
                "PAM": pam,
                "Score": score,
                "Relative_Cut_Pos": cut_pos - relative_to
            })
            
    # Reverse Complement Scan
    rc_seq = str(Seq(target_seq).reverse_complement())
    for i in range(len(rc_seq) - 23):
        sub = rc_seq[i:i+23]
        if sub.endswith('GG'):
            sg = sub[:20]
            pam = sub[20:]
            score = score_sgrna(sg)
            candidates.append({
                "sgRNA": sg,
                "PAM": pam,
                "Score": score,
                "Direction": "Reverse"
            })
            
    return sorted(candidates, key=lambda x: x['Score'], reverse=True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--accession", help="NCBI Accession")
    parser.add_argument("--start", type=int)
    parser.add_argument("--end", type=int)
    parser.add_argument("--seq", help="Direct sequence input")
    args = parser.parse_args()
    
    seq = args.seq
    if args.accession:
        seq = fetch_ncbi_sequence(args.accession, args.start, args.end)
        
    if seq:
        results = design_sgrnas(seq)
        print(json.dumps(results[:5], indent=2))
