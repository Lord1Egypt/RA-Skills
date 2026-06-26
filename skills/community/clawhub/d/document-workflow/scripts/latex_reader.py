#!/usr/bin/env python3
"""
Download and parse LaTeX source from arXiv.

arXiv provides source code via: https://arxiv.org/e-print/{id}
This returns a tar.gz file containing .tex, .bib, and figures.

More comprehensive than PDF extraction because:
- Preserves equation structure (not garbled text)
- Gets full bibliography (.bib)
- Extracts structured content (sections, algorithms, tables)
"""

import argparse
import io
import json
import os
import re
import sys
import tarfile
import tempfile
import urllib.request
import zipfile
from pathlib import Path
from typing import Optional


def extract_arxiv_id(url: str) -> Optional[str]:
    """Extract arXiv ID from various URL formats."""
    patterns = [
        r'arxiv\.org/abs/(\d+\.\d+(?:v\d+)?)',
        r'arxiv\.org/pdf/(\d+\.\d+(?:v\d+)?)',
        r'arxiv\.org/e-print/(\d+\.\d+(?:v\d+)?)',
        r'^(\d{4}\.\d{4,5}(?:v\d+)?)$',  # Bare ID
    ]
    for p in patterns:
        m = re.search(p, url, re.I)
        if m:
            return m.group(1)
    return None


def download_latex_source(arxiv_id: str, timeout: int = 120) -> bytes:
    """Download LaTeX source tarball from arXiv."""
    url = f"https://arxiv.org/e-print/{arxiv_id}"
    print(f"Downloading LaTeX source from: {url}", file=sys.stderr)
    
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (research bot)"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
            data = response.read()
            print(f"✓ Downloaded {len(data)/1024:.1f} KB", file=sys.stderr)
            return data
    except Exception as e:
        raise RuntimeError(f"Failed to download source: {e}")


def extract_tarball(data: bytes, extract_dir: str) -> list:
    """Extract tar.gz or zip content to directory."""
    files = []
    
    # Try tar.gz first
    try:
        with tarfile.open(fileobj=io.BytesIO(data), mode='r:gz') as tar:
            tar.extractall(extract_dir)
            files = tar.getnames()
            print(f"✓ Extracted {len(files)} files (tar.gz)", file=sys.stderr)
            return files
    except tarfile.TarError:
        pass
    
    # Try zip
    try:
        with zipfile.ZipFile(io.BytesIO(data)) as zf:
            zf.extractall(extract_dir)
            files = zf.namelist()
            print(f"✓ Extracted {len(files)} files (zip)", file=sys.stderr)
            return files
    except zipfile.BadZipFile:
        pass
    
    # Check if it's a single .tex file
    try:
        text = data.decode('utf-8', errors='ignore')
        if '\\documentclass' in text or '\\begin{document}' in text:
            tex_file = os.path.join(extract_dir, 'main.tex')
            with open(tex_file, 'w', encoding='utf-8') as f:
                f.write(text)
            print(f"✓ Saved as single .tex file", file=sys.stderr)
            return ['main.tex']
    except:
        pass
    
    raise RuntimeError("Could not extract archive (not tar.gz, zip, or .tex)")


def find_main_tex(extract_dir: str) -> Optional[str]:
    """Find the main .tex file (contains \\documentclass)."""
    for root, _, files in os.walk(extract_dir):
        for f in files:
            if f.endswith('.tex'):
                path = os.path.join(root, f)
                try:
                    with open(path, 'r', encoding='utf-8', errors='ignore') as fp:
                        content = fp.read()
                        if r'\documentclass' in content:
                            return path
                except:
                    continue
    # Fallback: return first .tex file
    for root, _, files in os.walk(extract_dir):
        for f in files:
            if f.endswith('.tex'):
                return os.path.join(root, f)
    return None


def find_bib_files(extract_dir: str) -> list:
    """Find all .bib and .bbl files."""
    bib_files = []
    for root, _, files in os.walk(extract_dir):
        for f in files:
            if f.endswith('.bib') or f.endswith('.bbl'):
                bib_files.append(os.path.join(root, f))
    return bib_files


def clean_latex(text: str) -> str:
    """Remove LaTeX commands and extract plain text."""
    # Remove comments
    text = re.sub(r'%.*$', '', text, flags=re.M)
    
    # Remove common commands but keep content
    text = re.sub(r'\\textbf\{([^}]*)\}', r'\1', text)
    text = re.sub(r'\\textit\{([^}]*)\}', r'\1', text)
    text = re.sub(r'\\emph\{([^}]*)\}', r'\1', text)
    text = re.sub(r'\\underline\{([^}]*)\}', r'\1', text)
    text = re.sub(r'\\text\{([^}]*)\}', r'\1', text)
    text = re.sub(r'\\mbox\{([^}]*)\}', r'\1', text)
    
    # Handle citations
    text = re.sub(r'\\cite[pt]?\{[^}]*\}', '[CITATION]', text)
    text = re.sub(r'\\ref\{[^}]*\}', '[REF]', text)
    text = re.sub(r'\\label\{[^}]*\}', '', text)
    
    # Handle equations - keep structure
    text = re.sub(r'\\begin\{equation\}', '\n[EQUATION]\n', text)
    text = re.sub(r'\\end\{equation\}', '\n[/EQUATION]\n', text)
    text = re.sub(r'\\begin\{align\*?\}', '\n[EQUATION]\n', text)
    text = re.sub(r'\\end\{align\*?\}', '\n[/EQUATION]\n', text)
    text = re.sub(r'\$\$', '\n[EQUATION]\n', text)
    text = re.sub(r'\$', '', text)  # Inline math
    
    # Remove other environments but keep content
    for env in ['figure', 'table', 'algorithm', 'algorithmic', 'itemize', 'enumerate', 'description']:
        text = re.sub(rf'\\begin\{{{env}\*?\}}', f'\n[{env.upper()}]\n', text)
        text = re.sub(rf'\\end\{{{env}\*?\}}', f'\n[/{env.upper()}]\n', text)
    
    # Handle sections
    text = re.sub(r'\\section\{([^}]*)\}', r'\n## \1\n', text)
    text = re.sub(r'\\subsection\{([^}]*)\}', r'\n### \1\n', text)
    text = re.sub(r'\\subsubsection\{([^}]*)\}', r'\n#### \1\n', text)
    text = re.sub(r'\\paragraph\{([^}]*)\}', r'\n**\1** ', text)
    
    # Remove remaining commands (keep content in braces)
    text = re.sub(r'\\[a-zA-Z]+\*?\{([^}]*)\}', r'\1', text)
    text = re.sub(r'\\[a-zA-Z]+', '', text)
    
    # Clean up braces
    text = re.sub(r'\{([^}]*)\}', r'\1', text)
    
    # Clean up whitespace
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = re.sub(r' {2,}', ' ', text)
    
    return text.strip()


def extract_metadata(tex_content: str) -> dict:
    """Extract title, authors, abstract from LaTeX."""
    metadata = {
        "title": None,
        "authors": [],
        "abstract": None,
        "keywords": []
    }
    
    # Extract title
    title_match = re.search(r'\\title\{([^}]*(?:\{[^}]*\}[^}]*)*)\}', tex_content, re.DOTALL)
    if title_match:
        metadata["title"] = clean_latex(title_match.group(1)).strip()
    
    # Extract authors
    author_match = re.search(r'\\author\{([^}]*(?:\{[^}]*\}[^}]*)*)\}', tex_content, re.DOTALL)
    if author_match:
        author_text = author_match.group(1)
        # Split by \and or comma
        authors = re.split(r'\\and|,', author_text)
        for a in authors:
            a = clean_latex(a).strip()
            if a and len(a) < 200:  # Filter out institution names
                metadata["authors"].append(a)
    
    # Also try author macro formats
    if not metadata["authors"]:
        author_matches = re.findall(r'\\author\[(?:[^\]]*)\]\{([^}]*)\}', tex_content)
        metadata["authors"] = [clean_latex(a).strip() for a in author_matches if a.strip()]
    
    # Extract abstract
    abstract_match = re.search(r'\\begin\{abstract\}(.*?)\\end\{abstract\}', tex_content, re.DOTALL)
    if abstract_match:
        metadata["abstract"] = clean_latex(abstract_match.group(1)).strip()
    
    # Extract keywords
    keywords_match = re.search(r'\\keywords\{([^}]*)\}', tex_content)
    if keywords_match:
        metadata["keywords"] = [k.strip() for k in keywords_match.group(1).split(',')]
    
    return metadata


def extract_sections(tex_content: str) -> list:
    """Extract section structure."""
    sections = []
    
    # Match \section{...} and \subsection{...}
    pattern = r'\\(section|subsection|subsubsection)\{([^}]*)\}'
    for match in re.finditer(pattern, tex_content):
        level = {"section": 1, "subsection": 2, "subsubsection": 3}.get(match.group(1), 1)
        title = clean_latex(match.group(2)).strip()
        if title:
            sections.append({"level": level, "title": title})
    
    return sections


def extract_equations(tex_content: str) -> list:
    """Extract equations (numbered and display)."""
    equations = []
    
    # Numbered equations
    eq_pattern = r'\\begin\{equation\}(?:\[[^\]]*\])?(.*?)\\end\{equation\}'
    for i, match in enumerate(re.finditer(eq_pattern, tex_content, re.DOTALL), 1):
        eq = match.group(1).strip()
        eq = re.sub(r'\\label\{[^}]*\}', '', eq).strip()
        if eq:
            equations.append({"number": i, "latex": eq})
    
    # Align environments
    align_pattern = r'\\begin\{align\*?\}(.*?)\\end\{align\*?\}'
    for match in re.finditer(align_pattern, tex_content, re.DOTALL):
        lines = match.group(1).strip().split('\\\\')
        for line in lines:
            line = re.sub(r'\\label\{[^}]*\}', '', line).strip()
            line = re.sub(r'\\nonumber', '', line).strip()
            if line and not line.startswith('&'):  # Skip continuation lines
                equations.append({"number": None, "latex": line})
    
    return equations


def extract_tables(tex_content: str) -> list:
    """Extract table structures."""
    tables = []
    
    # Match table environment
    table_pattern = r'\\begin\{table\*?\}(.*?)\\end\{table\*?\}'
    for match in re.finditer(table_pattern, tex_content, re.DOTALL):
        table_tex = match.group(1)
        
        # Extract caption
        caption = None
        caption_match = re.search(r'\\caption\{([^}]*)\}', table_tex)
        if caption_match:
            caption = clean_latex(caption_match.group(1)).strip()
        
        # Extract label
        label = None
        label_match = re.search(r'\\label\{([^}]*)\}', table_tex)
        if label_match:
            label = label_match.group(1).strip()
        
        # Parse tabular content
        tabular_match = re.search(r'\\begin\{tabular\}[^}]*\}(.*?)\\end\{tabular\}', table_tex, re.DOTALL)
        rows = []
        if tabular_match:
            for line in tabular_match.group(1).split('\\\\'):
                line = line.strip()
                if line and not line.startswith('\\'):
                    cells = [clean_latex(c).strip() for c in line.split('&')]
                    if any(cells):
                        rows.append(cells)
        
        tables.append({
            "caption": caption,
            "label": label,
            "rows": rows if rows else None,
            "raw": table_tex[:500] + "..." if len(table_tex) > 500 else table_tex
        })
    
    return tables


def extract_algorithm(tex_content: str) -> list:
    """Extract algorithm pseudo-code."""
    algorithms = []
    
    # algorithmic environment
    alg_pattern = r'\\begin\{algorithm\*?\}(.*?)\\end\{algorithm\*?\}'
    for match in re.finditer(alg_pattern, tex_content, re.DOTALL):
        alg_tex = match.group(1)
        
        # Extract caption
        caption = None
        caption_match = re.search(r'\\caption\{([^}]*)\}', alg_tex)
        if caption_match:
            caption = clean_latex(caption_match.group(1)).strip()
        
        # Parse algorithmic content
        steps = []
        for line in alg_tex.split('\n'):
            line = line.strip()
            if '\\State' in line:
                step = re.sub(r'\\State\s*', '', line)
                step = clean_latex(step).strip()
                if step:
                    steps.append(step)
            elif '\\For' in line or '\\While' in line or '\\If' in line:
                step = clean_latex(re.sub(r'\\(For|While|If|ElsIf|Else|EndFor|EndWhile|EndIf)\s*', '', line)).strip()
                if step:
                    steps.append(step)
        
        algorithms.append({
            "caption": caption,
            "steps": steps,
            "raw": alg_tex[:1000] + "..." if len(alg_tex) > 1000 else alg_tex
        })
    
    return algorithms


def parse_bib_file(bib_path: str) -> list:
    """Parse .bib file to extract references."""
    references = []
    
    try:
        with open(bib_path, 'r', encoding='utf-8', errors='ignore') as f:
            bib_content = f.read()
    except:
        return references
    
    # Match @type{key, ... }
    entry_pattern = r'@(\w+)\s*\{\s*([^,]+)\s*,([^@]*?)(?=@|\Z)'
    
    for match in re.finditer(entry_pattern, bib_content, re.DOTALL):
        entry_type = match.group(1).lower()
        key = match.group(2).strip()
        fields_text = match.group(3)
        
        entry = {"type": entry_type, "key": key}
        
        # Extract fields
        field_pattern = r'(\w+)\s*=\s*\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}'
        for field_match in re.finditer(field_pattern, fields_text):
            field_name = field_match.group(1).lower()
            field_value = field_match.group(2).strip()
            entry[field_name] = field_value
        
        # Also handle quotes
        field_pattern2 = r'(\w+)\s*=\s*"([^"]*)"'
        for field_match in re.finditer(field_pattern2, fields_text):
            field_name = field_match.group(1).lower()
            field_value = field_match.group(2).strip()
            if field_name not in entry:
                entry[field_name] = field_value
        
        if 'title' in entry or 'author' in entry:
            references.append(entry)
    
    return references


def parse_bbl_file(bbl_path: str) -> list:
    """Parse .bbl file (compiled bibliography from BibTeX)."""
    references = []
    
    try:
        with open(bbl_path, 'r', encoding='utf-8', errors='ignore') as f:
            bbl_content = f.read()
    except:
        return references
    
    # Match \bibitem[label]{key} ... content
    # Format: \bibitem[Author(year)]{key} Author names. \newblock Title. \newblock Venue.
    bibitem_pattern = r'\\bibitem(?:\[[^\]]*\])?\{([^}]+)\}(.*?)(?=\\bibitem|\\end\{thebibliography\})'
    
    for match in re.finditer(bibitem_pattern, bbl_content, re.DOTALL):
        key = match.group(1).strip()
        content = match.group(2).strip()
        
        entry = {"type": "article", "key": key, "raw": content[:500]}
        
        # Extract author (usually at the beginning before \newblock)
        author_match = re.match(r'^([^\\]+?)(?=\\newblock|\n\n|$)', content, re.DOTALL)
        if author_match:
            author_text = author_match.group(1).strip()
            author_text = clean_latex(author_text)
            entry["author"] = author_text
        
        # Extract title (after first \newblock)
        title_match = re.search(r'\\newblock\s+([^\\]+?)(?=\\newblock|\\emph|In\s)', content)
        if title_match:
            title_text = title_match.group(1).strip()
            title_text = clean_latex(title_text)
            # Remove trailing punctuation
            title_text = re.sub(r'[.,;:\s]+$', '', title_text)
            entry["title"] = title_text
        
        # Extract venue (usually in \emph{...} or "In ...")
        venue_match = re.search(r'\\emph\{([^}]+)\}', content)
        if venue_match:
            entry["venue"] = venue_match.group(1).strip()
        
        # Extract year
        year_match = re.search(r'\b(19|20)\d{2}\b', content)
        if year_match:
            entry["year"] = year_match.group(0)
        
        # Extract DOI if present
        doi_match = re.search(r'\\doi\{([^}]+)\}|doi[:\s]+([^\s,}]+)', content)
        if doi_match:
            entry["doi"] = (doi_match.group(1) or doi_match.group(2)).strip()
        
        # Extract URL if present
        url_match = re.search(r'\\url\{([^}]+)\}', content)
        if url_match:
            entry["url"] = url_match.group(1).strip()
        
        if entry.get("title") or entry.get("author"):
            references.append(entry)
    
    return references


def parse_latex_source(tex_path: str, bib_files: list = None) -> dict:
    """Parse LaTeX source file and extract structured content."""
    
    with open(tex_path, 'r', encoding='utf-8', errors='ignore') as f:
        tex_content = f.read()
    
    # Handle \input and \include
    tex_dir = os.path.dirname(tex_path)
    def resolve_includes(content):
        def replace_include(m):
            include_file = m.group(1)
            if not include_file.endswith('.tex'):
                include_file += '.tex'
            include_path = os.path.join(tex_dir, include_file)
            try:
                with open(include_path, 'r', encoding='utf-8', errors='ignore') as f:
                    return f.read()
            except:
                return ''
        
        content = re.sub(r'\\input\{([^}]*)\}', replace_include, content)
        content = re.sub(r'\\include\{([^}]*)\}', replace_include, content)
        content = re.sub(r'\\subfile\{([^}]*)\}', replace_include, content)  # Handle subfile package
        return content
    
    tex_content = resolve_includes(tex_content)
    
    result = {
        "source_file": os.path.basename(tex_path),
        "metadata": extract_metadata(tex_content),
        "sections": extract_sections(tex_content),
        "equations": extract_equations(tex_content),
        "tables": extract_tables(tex_content),
        "algorithms": extract_algorithm(tex_content),
        "full_text": clean_latex(tex_content),
        "references": []
    }
    
    # Parse bibliography files
    if bib_files:
        for bib_path in bib_files:
            if bib_path.endswith('.bbl'):
                refs = parse_bbl_file(bib_path)
            else:
                refs = parse_bib_file(bib_path)
            result["references"].extend(refs)
    
    return result


def main():
    parser = argparse.ArgumentParser(description="Download and parse arXiv LaTeX source")
    parser.add_argument("arxiv_id", help="arXiv ID or URL (e.g., 2301.12345 or https://arxiv.org/abs/2301.12345)")
    parser.add_argument("--output", help="Output JSON file")
    parser.add_argument("--keep", action="store_true", help="Keep extracted files")
    parser.add_argument("--timeout", type=int, default=120, help="Download timeout seconds")
    parser.add_argument("--sections-only", action="store_true", help="Only extract sections outline")
    parser.add_argument("--bib-only", action="store_true", help="Only extract bibliography")
    args = parser.parse_args()
    
    # Extract arXiv ID
    arxiv_id = extract_arxiv_id(args.arxiv_id)
    if not arxiv_id:
        print(json.dumps({"error": f"Invalid arXiv ID or URL: {args.arxiv_id}"}))
        sys.exit(1)
    
    # Download and extract
    data = download_latex_source(arxiv_id, args.timeout)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        files = extract_tarball(data, tmpdir)
        
        # Find main .tex file
        main_tex = find_main_tex(tmpdir)
        if not main_tex:
            print(json.dumps({"error": "No .tex file found in archive", "files": files}))
            sys.exit(1)
        
        print(f"Main TeX: {os.path.basename(main_tex)}", file=sys.stderr)
        
        # Find bibliography files
        bib_files = find_bib_files(tmpdir)
        if bib_files:
            print(f"Bibliography: {len(bib_files)} .bib files", file=sys.stderr)
        
        # Parse
        result = parse_latex_source(main_tex, bib_files)
        result["arxiv_id"] = arxiv_id
        result["all_files"] = files
        
        # Keep files if requested
        if args.keep:
            keep_dir = os.path.join(os.path.dirname(args.output) if args.output else ".", f"arxiv_{arxiv_id}")
            import shutil
            shutil.copytree(tmpdir, keep_dir, dirs_exist_ok=True)
            result["source_dir"] = keep_dir
            print(f"✓ Source files saved to: {keep_dir}", file=sys.stderr)
        
        # Filter output if requested
        if args.sections_only:
            result = {"arxiv_id": arxiv_id, "sections": result["sections"]}
        elif args.bib_only:
            result = {"arxiv_id": arxiv_id, "references": result["references"]}
        
        # Output
        if args.output:
            os.makedirs(os.path.dirname(args.output) or ".", exist_ok=True)
            with open(args.output, 'w', encoding='utf-8') as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
            print(f"✓ Output saved to: {args.output}", file=sys.stderr)
        else:
            # Use UTF-8 for Windows console
            import io
            sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
            print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()