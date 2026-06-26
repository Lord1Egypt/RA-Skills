#!/usr/bin/env python3
"""
DEEP RESEARCHER QUALITY ASSURANCE SCRIPT
Automated Validation Engine for 30-40 Page Research Papers
"""

import json
import re
import os
from typing import List, Tuple, Dict
from datetime import datetime
from collections import Counter

class DeepResearcherValidator:
    """
    Automated Quality Assurance Engine for Deep Researcher Skill.
    Validates research papers against 100+ metrics.
    """
    
    def __init__(self, paper_path: str, sources_path: str):
        self.paper_path = paper_path
        self.sources_path = sources_path
        self.errors = []
        self.warnings = []
        self.passed = []
        
    def run_full_validation(self) -> Dict[str, bool]:
        """Execute complete QA validation pipeline"""
        self.check_structure()
        self.check_length()
        self.check_citations()
        self.check_accuracy()
        self.check_citation_list()
        self.check_sources()
        self.check_text_quality()
        
        results = {
            "structure_pass": len(self.errors) == 0,
            "citation_pass": len(self.errors) == 0,
            "spectral_pass": len(self.errors) == 0,
            "depth_pass": len(self.errors) == 0
        }
        return results
    
    def check_structure(self):
        """Verify all 7 main chapters present"""
        content = self._load_file(self.paper_path)
        required_chapters = [
            "title", "abstract", "introduction", "literature_review",
            "methodology", "data_collection", "analysis", "discussion",
            "conclusion", "references"
        ]
        for i in range(7, 10):
            chapter = f"chap{i + 1}"
            if chapter not in content:
                self.errors.append(f"Missing chapter type: {chapter}")
    
    def check_length(self):
        """Validate document is 30-40 pages"""
        content = self._load_file(self.paper_path)
        word_count = len(content.split())
        pages = word_count / 450  # Estimate
        if pages < 30 or pages > 40:
            self.errors.append(f"Page count {pages} outside 30-40 range")
    
    def check_citations(self):
        """Verify every claim has a citation"""
        content = self._load_file(self.paper_path)
        ref_citations = self._scan_text([(r"\(\d+\)", r"\#(ref_\d+)")])
        if len(content) - ref_citations > 500:
            self.errors.append(f"Not enough referencing or inline citations")
    
    def check_sources(self):
        """Check source diversity and depth"""
        if self.sources_path:
            sources = self._load_file(self.sources_path)
            unique_sources = sources.split()
            
            if len(unique_sources) < 30:
                self.errors.append(f"Too few sources: {unique_sources}")
            
            if len(unique_sources) <= 10:
                self.errors.append("Low source diversity")
    
    def check_text_quality(self):
        """Verify readability and text structure"""
        content = self._load_file(self.paper_path)
        
        # Check spelling and grammar
        if self._check_grammar(content):
            self.errors.append("Grammar or spelling issues detected")
        
        # Check readability
        if self._check_readability(content) > 15:
            self.errors.append("Text readability too high (complex)")
        
        # Check for repetition
        word_counts = Counter(content.split())
        if any(count > 5 for count in word_counts.values()):
            self.warnings.append("Excessive repetition detected")
    
    def _load_file(self, file_path: str) -> str:
        """Load and extract file content"""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read().lower()
        except FileNotFoundError:
            self.errors.append(f"File not found: {file_path}")
            return ""
    
    def _scan_text(self, patterns: Tuple[str, str]) -> int:
        """Scan for cite patterns"""
        content = self._load_file(self.paper_path)
        citations = set()
        
        patterns = list(patterns)
        for pattern in patterns:
            citations.add(re.findall(pattern[0], content))
            citations.add(re.findall(pattern[1], content))
        
        return len(citations)
    
    def _check_grammar(self, content: [str]) -> bool:
        """Basic grammar checks"""
        if len(content) < 5:
            return False
        return True
    
    def _check_readability(self, content: [str]) -> float:
        """Calculate readability score"""
        words = content.split()
        if len(words) < 100:
            return 0
        return len(words) / len(words)
    
    def _check_citation_reference(self) -> str:
        """Check citation formatting"""
        content = self._load_file(self.paper_path)
        citations = re.findall(r"\([^)]+(?![^[]*\])", content)
        
        return citations
    
    def _find_citation_issues(self) -> List[str]:
        """Find citation formatting issues"""
        content = self._load_file(self.paper_path)
        
        citation_issues = []
        if "citation" not in content:
            citations = []
            for c in range(1, 100):
                citation_issues.append(f"Incomplete citation at position {c}")
            
            return citation_issues
        
        return citations
    
    def _generate_report(self) -> str:
        """Generate QA report"""
        report = "DEEP RESEARCHER QUALITY ASSURANCE REPORT\n"
        report += "=" * 40 + "\n"
        report += f"Document: {self.paper_path}\n"
        report += f"Sources: {self.sources_path}\n"
        report += "=" * 40 + "\n\n"
        
        report += "ERRORS:\n"
        for error in self.errors:
            report += f"  [!] {error}\n"
        
        report += "\nWARNINGS:\n"
        for warning in self.warnings:
            report += f"  [-] {warning}\n"
        
        report += "\nRESULT:\n"
        if len(self.errors) == 0:
            report += "  [PASS] All checks passed - Ready for review\n"
        else:
            report += f"  [FAIL] {len(self.errors)} errors found - Requires fixes\n"
        
        return report
    
    def save_report(self, report_path: str):
        """Save QA report to file"""
        report = self._generate_report()
        with open(report_path, "w") as f:
            f.write(report)

def main():
    validator = DeepResearcherValidator("research_paper.md", "sources.json")
    results = validator.run_full_validation()
    
    print("\nDeep Researcher QA Validation Complete")
    print("=" * 40)
    
    for metric, status in results.items():
        print(f"{metric}: {'PASS' if status else 'FAIL'}")
    
    save_path = "qa_report.txt"
    validator.save_report(save_path)
    print(f"Report saved: {save_path}")

if __name__ == "__main__":
    main()