#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Paper Classification Module
Classifies papers into categories based on title, abstract, and keywords.
"""

from typing import Dict, List, Tuple


class PaperClassifier:
    """
    Classifies research papers into predefined categories.
    Uses keyword matching with scoring system.
    """
    
    def __init__(self, category_keywords: Dict[str, List[str]]):
        """
        Initialize classifier with category keywords.
        
        Args:
            category_keywords: Dict mapping category names to keyword lists
        """
        self.category_keywords = {}
        for cat_name, keywords in category_keywords.items():
            self.category_keywords[cat_name] = [kw.lower() for kw in keywords]
    
    def classify(self, title: str, abstract: str = None) -> Tuple[str, int]:
        """
        Classify a paper based on title and abstract.
        
        Args:
            title: Paper title
            abstract: Paper abstract (optional)
        
        Returns:
            Tuple of (category_name, confidence_score)
        """
        text = f"{title} {abstract or ''}".lower()
        
        scores = {}
        for category, keywords in self.category_keywords.items():
            score = sum(1 for kw in keywords if kw in text)
            scores[category] = score
        
        # Find best match
        if not scores:
            return "OTHER", 0
        
        best_category = max(scores, key=scores.get)
        best_score = scores[best_category]
        
        # Check for tie
        top_scores = [cat for cat, score in scores.items() if score == best_score]
        if len(top_scores) > 1:
            # Tie: return OTHER or first alphabetically
            return "OTHER", best_score
        
        if best_score == 0:
            return "OTHER", 0
        
        return best_category, best_score
    
    def classify_by_filename(self, filename: str) -> Tuple[str, int]:
        """
        Classify based on filename alone.
        
        Args:
            filename: PDF filename
        
        Returns:
            Tuple of (category_name, confidence_score)
        """
        # Clean filename
        name = filename.lower().replace("_", " ").replace("-", " ").replace(".pdf", "")
        
        return self.classify(title=name)


# Default classification keywords (for B-ALL and MM research)
DEFAULT_KEYWORDS = {
    "B-ALL": [
        "b-cell acute lymphoblastic leukemia",
        "b-all",
        "b cell acute lymphoblastic",
        "b lymphoblastic leukemia",
        "acute lymphoblastic leukemia",
        "cd19",
        "cd22",
        "blinatumomab",
        "inotuzumab",
        "car-t",
        "cart",
        "tisagenlecleucel",
        "brexucabtagene",
        "ph-positive",
        "ph-negative",
        "philadelphia chromosome",
    ],
    "MM": [
        "multiple myeloma",
        "myeloma",
        "plasma cell",
        "bcma",
        "gprc5d",
        "fcrh5",
        "elranatamab",
        "teclistamab",
        "talquetamab",
        "daratumumab",
        "isatuximab",
        "pomalidomide",
        "lenalidomide",
    ],
}


def create_default_classifier() -> PaperClassifier:
    """Create classifier with default B-ALL/MM keywords."""
    return PaperClassifier(DEFAULT_KEYWORDS)


def classify_by_keywords(text: str, category: str = None) -> str:
    """
    Simple keyword-based classification function.
    
    Args:
        text: Text to classify (title, abstract, or filename)
        category: Specific category to check (optional)
    
    Returns:
        Category name
    """
    classifier = create_default_classifier()
    
    if category:
        # Check if text matches specific category
        keywords = classifier.category_keywords.get(category, [])
        text_lower = text.lower()
        if any(kw in text_lower for kw in keywords):
            return category
        return "OTHER"
    
    # Full classification
    result_category, _ = classifier.classify(title=text)
    return result_category


if __name__ == "__main__":
    # Test the classifier
    classifier = create_default_classifier()
    
    test_papers = [
        ("CAR-T therapy for B-ALL", "B-cell acute lymphoblastic leukemia treatment"),
        ("Elranatamab in multiple myeloma", "BCMA-targeted therapy"),
        ("Blinatumomab outcomes", "CD19-targeted treatment"),
        ("Talquetamab for myeloma", "GPRC5D bispecific antibody"),
    ]
    
    print("Classification Tests:")
    print("-" * 50)
    
    for title, abstract in test_papers:
        category, score = classifier.classify(title, abstract)
        print(f"Title: {title}")
        print(f"  → Category: {category} (score: {score})")
        print()
