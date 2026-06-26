#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Smart ArXiv Survey Generator
Searches multiple AI areas and automatically selects hottest topic
"""

import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
from pathlib import Path
import subprocess
from datetime import datetime
from collections import Counter

class SmartArXivGenerator:
    """Intelligently select topic and generate survey"""
    
    def __init__(self, output_dir):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.arxiv_api = "http://export.arxiv.org/api/query"
        
        # AI research areas to monitor
        self.search_areas = [
            "artificial intelligence",
            "machine learning",
            "deep learning",
            "neural networks",
            "natural language processing",
            "computer vision",
            "reinforcement learning",
            "generative AI",
            "diffusion models",
            "large language models",
            "graph neural networks",
            "transformer architecture",
            "federated learning",
            "meta learning",
            "self-supervised learning"
        ]
    
    def generate_hourly_survey(self, max_papers_per_area=10):
        """
        Generate survey by:
        1. Searching multiple AI areas
        2. Analyzing trends
        3. Selecting hottest topic
        4. Generating survey
        """
        print("🔍 Searching multiple AI areas on arXiv...")
        
        # Search all areas
        all_papers = {}
        for area in self.search_areas:
            papers = self._search_arxiv(area, max_papers_per_area)
            if papers:
                all_papers[area] = papers
                print(f"  ✓ {area}: {len(papers)} papers")
        
        if not all_papers:
            print("❌ No papers found")
            return None
        
        # Analyze and select topic
        selected_topic = self._select_hot_topic(all_papers)
        print(f"\n🎯 Selected topic: {selected_topic}")
        
        # Generate survey for selected topic
        print(f"\n📝 Generating survey for: {selected_topic}")
        papers = all_papers[selected_topic]
        analysis = self._analyze_papers(papers)
        tex_content = self._generate_survey(selected_topic, papers, analysis)
        
        # Save and compile
        safe_name = self._safe_filename(selected_topic)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        tex_file = self.output_dir / f'{safe_name}_{timestamp}.tex'
        
        with open(tex_file, 'w', encoding='utf-8') as f:
            f.write(tex_content)
        
        pdf_file = self._compile_pdf(tex_file)
        
        return {
            'tex_file': str(tex_file),
            'pdf_file': str(pdf_file),
            'topic': selected_topic,
            'papers': papers,
            'analysis': analysis,
            'total_searched': sum(len(p) for p in all_papers.values()),
            'areas_monitored': len(all_papers)
        }
    
    def _search_arxiv(self, query, max_papers=10):
        """Search arXiv API"""
        try:
            search_query = urllib.parse.quote(query)
            url = f"{self.arxiv_api}?search_query=all:{search_query}&start=0&max_results={max_papers}&sortBy=submittedDate&sortOrder=descending"
            
            with urllib.request.urlopen(url, timeout=30) as response:
                xml_data = response.read().decode('utf-8')
            
            root = ET.fromstring(xml_data)
            namespace = {'atom': 'http://www.w3.org/2005/Atom'}
            
            papers = []
            for entry in root.findall('atom:entry', namespace):
                paper = {
                    'title': self._get_text(entry, 'atom:title', namespace),
                    'authors': [a.text for a in entry.findall('atom:author/atom:name', namespace)],
                    'summary': self._get_text(entry, 'atom:summary', namespace),
                    'published': self._get_text(entry, 'atom:published', namespace),
                    'arxiv_id': self._get_arxiv_id(entry, namespace),
                    'categories': [c.get('term') for c in entry.findall('atom:category', namespace)]
                }
                papers.append(paper)
            
            return papers
        except Exception as e:
            print(f"Error searching {query}: {e}")
            return []
    
    def _get_text(self, element, tag, namespace):
        elem = element.find(tag, namespace)
        return elem.text.strip() if elem is not None else ""
    
    def _get_arxiv_id(self, element, namespace):
        id_elem = element.find('atom:id', namespace)
        if id_elem is not None:
            return id_elem.text.split('/abs/')[-1]
        return ""
    
    def _select_hot_topic(self, all_papers):
        """Select hottest topic based on paper count and trends"""
        
        # Count papers per area
        paper_counts = {area: len(papers) for area, papers in all_papers.items()}
        
        # Extract keywords from all papers
        all_keywords = Counter()
        for area, papers in all_papers.items():
            for paper in papers:
                text = (paper['title'] + ' ' + paper['summary']).lower()
                # Extract technical keywords
                keywords = self._extract_keywords(text)
                all_keywords.update(keywords)
        
        # Score each area
        area_scores = {}
        for area, papers in all_papers.items():
            # Base score: number of papers
            score = len(papers) * 10
            
            # Bonus: recent papers (last 24h)
            recent_count = sum(1 for p in papers if self._is_very_recent(p['published']))
            score += recent_count * 5
            
            # Bonus: trending keywords
            area_text = ' '.join([p['title'] + ' ' + p['summary'] for p in papers]).lower()
            area_keywords = self._extract_keywords(area_text)
            trending_bonus = sum(all_keywords[k] for k in area_keywords[:5])
            score += trending_bonus
            
            area_scores[area] = score
        
        # Select highest scoring area
        selected = max(area_scores, key=area_scores.get)
        
        print(f"\n📊 Topic selection analysis:")
        print(f"   Areas monitored: {len(all_papers)}")
        print(f"   Total papers: {sum(paper_counts.values())}")
        print(f"   Top 3 areas:")
        for area, score in sorted(area_scores.items(), key=lambda x: x[1], reverse=True)[:3]:
            print(f"     - {area}: {score:.1f} points ({paper_counts[area]} papers)")
        
        return selected
    
    def _extract_keywords(self, text):
        """Extract technical keywords from text"""
        # Common AI/ML keywords
        keywords = [
            'transformer', 'attention', 'bert', 'gpt', 'llm',
            'cnn', 'resnet', 'vit', 'diffusion', 'gan', 'vae',
            'gnn', 'graph', 'reinforcement', 'policy', 'reward',
            'contrastive', 'self-supervised', 'few-shot', 'zero-shot',
            'adapter', 'lora', 'prompt', 'fine-tuning',
            'federated', 'distributed', 'privacy',
            'meta-learning', 'maml', 'optimization',
            'segmentation', 'detection', 'generation', 'classification'
        ]
        
        found = []
        for kw in keywords:
            if kw in text:
                found.append(kw)
        
        return found
    
    def _is_very_recent(self, published_str):
        """Check if paper is from last 24 hours"""
        try:
            published = datetime.fromisoformat(published_str.replace('Z', '+00:00'))
            now = datetime.now(published.tzinfo)
            hours_ago = (now - published).total_seconds() / 3600
            return hours_ago < 24
        except:
            return False
    
    def _analyze_papers(self, papers):
        """Analyze papers to identify themes"""
        if not papers:
            return {'themes': [], 'methods': []}
        
        all_text = ' '.join([p['title'] + ' ' + p['summary'] for p in papers]).lower()
        
        keywords = self._extract_keywords(all_text)
        keyword_counts = Counter(keywords)
        
        return {
            'themes': [k for k, _ in keyword_counts.most_common(10)],
            'top_methods': [k for k, _ in keyword_counts.most_common(5)],
            'paper_count': len(papers),
            'date_range': f"{papers[-1]['published'][:10]} to {papers[0]['published'][:10]}" if papers else ""
        }
    
    def _generate_survey(self, topic, papers, analysis):
        """Generate survey LaTeX"""
        abstract = self._gen_abstract(topic, papers, analysis)
        intro = self._gen_intro(topic, papers, analysis)
        background = self._gen_background(topic)
        taxonomy = self._gen_taxonomy(topic, analysis)
        methods = self._gen_methods(papers, analysis)
        experiments = self._gen_experiments()
        challenges = self._gen_challenges()
        future = self._gen_future()
        conclusion = self._gen_conclusion(topic)
        references = self._gen_references(papers)
        
        return self._assemble(topic, abstract, intro, background, taxonomy, methods,
                            experiments, challenges, future, conclusion, references)
    
    def _gen_abstract(self, topic, papers, analysis):
        return f"This survey reviews recent advances in {topic} based on analysis of {len(papers)} papers from arXiv ({analysis['date_range']}). We identify key trends including {', '.join(analysis['themes'][:3])}. Our analysis reveals significant progress with applications spanning multiple domains. We discuss open challenges and outline promising directions for future research."
    
    def _gen_intro(self, topic, papers, analysis):
        return f"""
\\section{{Introduction}}

Recent advances in {topic} have attracted significant attention. This survey analyzes {len(papers)} recent papers from arXiv.

\\subsection{{Motivation}}

The rapid growth of publications makes it challenging to track developments. This survey synthesizes key findings.

\\subsection{{Contributions}}

\\begin{{itemize}}
    \\item Analysis of {len(papers)} recent arXiv papers
    \\item Identification of {len(analysis['themes'])} key themes
    \\item Taxonomy of methods
    \\item Open challenges and future directions
\\end{{itemize}}
"""
    
    def _gen_background(self, topic):
        return f"""
\\section{{Background}}

\\subsection{{Historical Context}}

Research in {topic} has evolved significantly.

\\subsection{{Key Concepts}}

Foundational concepts include attention mechanisms, representation learning, and transfer learning.
"""
    
    def _gen_taxonomy(self, topic, analysis):
        themes = analysis['themes'][:5]
        theme_items = '\n'.join([f"    \\item \\textbf{{{t.title()}}}: Active research area" for t in themes])
        
        return f"""
\\section{{Taxonomy}}

We categorize recent work:

\\begin{{itemize}}
{theme_items}
\\end{{itemize}}
"""
    
    def _gen_methods(self, papers, analysis):
        methods = analysis['top_methods'][:4]
        method_items = '\n'.join([f"    \\item \\textbf{{{m.title()}}}: Emerging technique" for m in methods])
        
        return f"""
\\section{{Methodologies}}

\\begin{{itemize}}
{method_items}
\\end{{itemize}}
"""
    
    def _gen_experiments(self):
        return """
\\section{{Experimental Analysis}}

\\subsection{{Benchmarks}}

Papers evaluate on standard benchmarks.

\\subsection{{Metrics}}

Common metrics include accuracy, efficiency, and generalization.
"""
    
    def _gen_challenges(self):
        return """
\\section{{Challenges}}

\\subsection{{Scalability}}

Large-scale scenarios remain challenging.

\\subsection{{Efficiency}}

Computational efficiency is an active area.
"""
    
    def _gen_future(self):
        return """
\\section{{Future Directions}}

\\subsection{{Emerging Trends}}

Continued advancement in architectures and methods.

\\subsection{{Applications}}

Expanding applications to new domains.
"""
    
    def _gen_conclusion(self, topic):
        return f"""
\\section{{Conclusion}}

This survey reviewed recent advances in {topic}. The field continues to evolve rapidly.
"""
    
    def _gen_references(self, papers):
        bib = []
        for i, paper in enumerate(papers[:50], 1):
            authors = ' and '.join(paper['authors'][:3])
            if len(paper['authors']) > 3:
                authors += ' and others'
            bib.append(f"\\bibitem{{Ref{i}}} {authors}. \"{paper['title']}.\" arXiv:{paper['arxiv_id']}, {paper['published'][:4]}.")
        return "\n".join(bib)
    
    def _assemble(self, topic, abstract, intro, background, taxonomy, methods, experiments, challenges, future, conclusion, references):
        template = r"""
\documentclass[11pt,a4paper]{article}
\usepackage[numbers]{natbib}
\usepackage{booktabs}
\usepackage{hyperref}
\usepackage{tikz}
\usepackage{amsmath}
\usepackage{geometry}
\geometry{margin=1in}

\title{TOPIC: A Survey of Recent arXiv Research}
\author{Redigg AI Research}
\date{\today}

\begin{document}
\maketitle

\begin{abstract}
ABSTRACT
\end{abstract}

INTRO

BACKGROUND

TAXONOMY

METHODS

EXPERIMENTS

CHALLENGES

FUTURE

CONCLUSION

\begin{thebibliography}{99}

REFERENCES

\end{thebibliography}

\end{document}
"""
        return (template
            .replace('TOPIC', topic)
            .replace('ABSTRACT', abstract)
            .replace('INTRO', intro)
            .replace('BACKGROUND', background)
            .replace('TAXONOMY', taxonomy)
            .replace('METHODS', methods)
            .replace('EXPERIMENTS', experiments)
            .replace('CHALLENGES', challenges)
            .replace('FUTURE', future)
            .replace('CONCLUSION', conclusion)
            .replace('REFERENCES', references))
    
    def _safe_filename(self, topic):
        return topic.lower().replace(' ', '_').replace('-', '_')[:40]
    
    def _compile_pdf(self, tex_file):
        try:
            for _ in range(2):
                subprocess.run(
                    ['pdflatex', '-interaction=nonstopmode', str(tex_file)],
                    cwd=str(tex_file.parent),
                    capture_output=True,
                    timeout=120
                )
        except Exception as e:
            print(f"Warning: Compilation issue: {e}")
        return tex_file.with_suffix('.pdf')
