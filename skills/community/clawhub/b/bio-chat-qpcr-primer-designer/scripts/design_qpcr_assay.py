import argparse
import requests
import json
import time

def get_transcript(accession):
    if not accession: return None
    print(f"Fetching sequence for {accession}...")
    url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nuccore&id={accession}&rettype=fasta&retmode=text"
    for _ in range(3):
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                lines = response.text.strip().split('\n')
                return "".join(lines[1:])
        except:
            time.sleep(1)
    return None

def get_exon_junctions(accession):
    """获取外显子拼接点坐标"""
    print(f"Fetching exon annotation for {accession}...")
    url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nuccore&id={accession}&rettype=gb&retmode=text"
    junctions = []
    for _ in range(3):
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                lines = response.text.split('\n')
                current_end = 0
                for line in lines:
                    if line.strip().startswith('exon'):
                        parts = line.split()
                        if len(parts) > 1:
                            coords = parts[1].replace('<', '').replace('>', '')
                            if '..' in coords:
                                try:
                                    start, end = coords.split('..')
                                    if current_end > 0:
                                        junctions.append(int(current_end))
                                    current_end = int(end)
                                except: pass
                return junctions
        except:
            time.sleep(1)
    return junctions

def map_homolog_junctions(target_seq, homolog_acc):
    """硬核解法：利用同源物种(如Human)的外显子边界映射到目标序列"""
    print(f"Mapping homolog junctions from {homolog_acc} to target...")
    homolog_seq = get_transcript(homolog_acc)
    homolog_gb = ""
    url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nuccore&id={homolog_acc}&rettype=gb&retmode=text"
    for _ in range(3):
        try:
            res = requests.get(url, timeout=10)
            if res.status_code == 200:
                homolog_gb = res.text
                break
        except: time.sleep(1)
    
    if not homolog_seq or not homolog_gb:
        print("Failed to retrieve homolog data.")
        return []
    
    h_juncs = get_exon_junctions(homolog_acc)
    target_juncs = []
    
    for j in h_juncs:
        if 15 < j < len(homolog_seq) - 15:
            anchor = homolog_seq[j-15 : j+15]
            idx = target_seq.find(anchor)
            if idx != -1:
                target_juncs.append(idx + 15)
            else:
                anchor_left = homolog_seq[j-15 : j]
                idx_left = target_seq.find(anchor_left)
                if idx_left != -1:
                    target_juncs.append(idx_left + 15)
    
    print(f"Successfully mapped {len(target_juncs)} junctions using homology.")
    return target_juncs

def calculate_tm_nn(seq):
    """使用基础算法计算 Tm"""
    if len(seq) == 0: return 0
    gc = seq.count('G') + seq.count('C')
    at = len(seq) - gc
    return float(at * 2 + gc * 4)

def rev_comp(seq):
    complement = {'A': 'T', 'C': 'G', 'G': 'C', 'T': 'A', 'N': 'N'}
    return "".join([complement.get(b, 'N') for b in seq[::-1]])

def check_self_dimer(seq):
    rc = rev_comp(seq)
    for length in range(4, min(8, len(seq))):
        for i in range(len(seq) - length + 1):
            if seq[i:i+length] in rc:
                return True
    return False

def check_3prime_quality(seq):
    last_5 = seq[-5:]
    gc_count = last_5.count('G') + last_5.count('C')
    return gc_count <= 4 # 针对高GC物种放宽到4

def check_3prime_mismatch(primer_seq, off_target_seq):
    if not off_target_seq: return True
    prefix = primer_seq[:-3]
    idx = off_target_seq.find(prefix)
    if idx != -1:
        match_region = off_target_seq[idx : idx+len(primer_seq)]
        if match_region[-3:] == primer_seq[-3:]:
            return False
    return True

def spans_exon_junction(start, end, junctions):
    for j in junctions:
        if start + 3 <= j <= end - 3:
            return True
    return False

def check_intron_spanning(f_start, f_end, r_start, r_end, junctions):
    for j in junctions:
        if f_end < j < r_start:
            return True
    return False

def design_assay(target_seq, offtarget_seq=None, junctions=None, amplicon_range=(70, 150)):
    candidates = []
    seq_len = len(target_seq)
    if not junctions: junctions = []
    
    for f in range(20, seq_len - amplicon_range[1] - 50):
        for length in range(16, 23):
            f_seq = target_seq[f : f+length]
            f_tm = calculate_tm_nn(f_seq)
            f_gc = (f_seq.count('G') + f_seq.count('C')) / float(length)
            
            if 58 <= f_tm <= 68 and 0.40 <= f_gc <= 0.90:
                if check_3prime_quality(f_seq) and not check_self_dimer(f_seq):
                    if check_3prime_mismatch(f_seq, offtarget_seq):
                        for r_len in range(16, 23):
                            for r in range(f + amplicon_range[0], f + amplicon_range[1]):
                                if r + r_len > seq_len: break
                                r_seq_plus = target_seq[r : r+r_len]
                                r_seq = rev_comp(r_seq_plus)
                                r_tm = calculate_tm_nn(r_seq)
                                r_gc = (r_seq.count('G') + r_seq.count('C')) / float(r_len)
                                
                                if 58 <= r_tm <= 68 and 0.40 <= r_gc <= 0.90 and abs(f_tm - r_tm) <= 4.0:
                                    if check_3prime_quality(r_seq) and not check_self_dimer(r_seq):
                                        if check_3prime_mismatch(r_seq, offtarget_seq):
                                            
                                            is_gdna_safe = False
                                            if junctions:
                                                if spans_exon_junction(f, f+length, junctions) or spans_exon_junction(r, r+r_len, junctions):
                                                    is_gdna_safe = True
                                                elif check_intron_spanning(f, f+length, r, r+r_len, junctions):
                                                    is_gdna_safe = True
                                            else:
                                                is_gdna_safe = True

                                            if is_gdna_safe:
                                                candidates.append({
                                                    "Amplicon_Size": r + r_len - f,
                                                    "gDNA_Safe": "Yes" if junctions else "Unknown",
                                                    "F_Primer": {"seq": f_seq, "tm": f_tm, "len": length},
                                                    "R_Primer": {"seq": r_seq, "tm": r_tm, "len": r_len},
                                                    "Probe": None
                                                })
                                                
                                                for p_len in range(18, 30):
                                                    for p in range(f + length + 5, r - 5):
                                                        if p + p_len > r: break
                                                        p_seq = target_seq[p : p+p_len]
                                                        p_tm = calculate_tm_nn(p_seq)
                                                        p_gc = (p_seq.count('G') + p_seq.count('C')) / float(p_len)
                                                        if f_tm + 3 <= p_tm <= 75 and 0.30 <= p_gc <= 0.85:
                                                            if p_seq[0] != 'G' and 'GGGG' not in p_seq:
                                                                candidates[-1]["Probe"] = {"seq": p_seq, "tm": p_tm, "len": p_len}
                                                                break
                                                    if candidates[-1]["Probe"]: break
                                                
                                                if len(candidates) >= 5: return candidates
                        break
    return candidates

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Advanced RT-qPCR Assay Designer v5.0 (Hardcore Mode)")
    parser.add_argument("--target", required=False, help="Target Accession (e.g. NM_001356)")
    parser.add_argument("--file", required=False, help="Local FASTA file")
    parser.add_argument("--offtarget", required=False, help="Off-target Accession for 3' mismatch check")
    parser.add_argument("--homolog", required=False, help="Homolog Accession (e.g. Human NM_) to map junctions")
    parser.add_argument("--no-gdna-check", action="store_true", help="Disable exon junction check")
    args = parser.parse_args()
    
    if args.file:
        with open(args.file, "r") as f:
            lines = f.read().strip().split("\n")
            target_seq = "".join(lines[1:])
    else:
        target_seq = get_transcript(args.target)
    
    offtarget_seq = get_transcript(args.offtarget) if args.offtarget else None
    
    junctions = []
    if target_seq and not args.no_gdna_check:
        junctions = get_exon_junctions(args.target)
        if not junctions and args.homolog:
            print(f"Target lacks exon data. Activating HARDCORE MODE with {args.homolog}...")
            junctions = map_homolog_junctions(target_seq, args.homolog)
            
        if junctions:
            print(f"Found {len(junctions)} exon junctions.")
        else:
            print("No exon junctions found.")

    if target_seq:
        print("Searching for highly specific primer/probe sets...")
        results = design_assay(target_seq, offtarget_seq, junctions)
        if results:
            print(f"Found {len(results)} valid assay designs. Showing top 3:")
            print(json.dumps(results[:3], indent=2))
        else:
            print("No valid primer/probe sets found matching all strict criteria.")
    else:
        print("Failed to retrieve target sequence.")
