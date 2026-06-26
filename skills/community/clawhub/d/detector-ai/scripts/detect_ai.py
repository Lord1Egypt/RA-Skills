#!/usr/bin/env python3
"""
AI Content Detector
Analyzes text to detect AI-generated content using multiple methods.
"""

import re
import math
import sys
import io
from collections import Counter
from typing import Dict, List, Tuple

# Ensure UTF-8 output on Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')


class AIDetector:
    """Main AI detection class with multiple analysis methods."""
    
    # Common AI transition words and phrases
    AI_TRANSITIONS = [
        'furthermore', 'moreover', 'additionally', 'consequently', 'therefore',
        'thus', 'hence', 'in conclusion', 'to summarize', 'in summary',
        'on the other hand', 'in contrast', 'similarly', 'likewise',
        'firstly', 'secondly', 'thirdly', 'finally', 'lastly',
        'it is important to note', 'it should be noted', 'it is worth noting',
        'in today\'s world', 'in the modern world', 'in recent years',
        'with the advent of', 'due to the fact that', 'in order to'
    ]
    
    # Generic AI openers
    AI_OPENERS = [
        'in today\'s', 'in the modern', 'in recent years', 'with the development',
        'as we all know', 'it is widely known', 'it is universally accepted',
        'in this essay', 'this essay will', 'this paper will'
    ]
    
    def __init__(self, text: str):
        self.text = text
        self.sentences = self._split_sentences(text)
        self.words = self._extract_words(text)
        
    def _split_sentences(self, text: str) -> List[str]:
        """Split text into sentences (supports English and Chinese)."""
        # Split by English sentence endings and Chinese punctuation
        sentences = re.split(r'[.!?。！？]+', text)
        return [s.strip() for s in sentences if s.strip()]
    
    def _extract_words(self, text: str) -> List[str]:
        """Extract words from text (supports English and Chinese)."""
        # Extract English words
        english_words = re.findall(r'\b[a-zA-Z]+\b', text.lower())
        # Extract Chinese characters/words (treat each char as a word for simplicity)
        chinese_chars = re.findall(r'[\u4e00-\u9fff]', text)
        return english_words + chinese_chars
    
    def calculate_perplexity(self) -> Dict:
        """
        Calculate perplexity using n-gram analysis.
        Lower perplexity = more predictable = likely AI.
        """
        if len(self.words) < 3:
            return {"score": 0, "interpretation": "Insufficient text"}
        
        # Calculate bigram probabilities
        bigrams = [(self.words[i], self.words[i+1]) for i in range(len(self.words)-1)]
        bigram_counts = Counter(bigrams)
        word_counts = Counter(self.words)
        
        # Calculate perplexity
        total_log_prob = 0
        for bigram in bigrams:
            # Laplace smoothing
            prob = (bigram_counts[bigram] + 1) / (word_counts[bigram[0]] + len(word_counts))
            total_log_prob += math.log2(prob)
        
        avg_log_prob = total_log_prob / len(bigrams)
        perplexity = 2 ** (-avg_log_prob)
        
        # Normalize to 0-100 scale (typical range: 50-300)
        normalized = max(0, min(100, (300 - perplexity) / 2.5))
        
        interpretation = ""
        if normalized > 70:
            interpretation = "Low perplexity - highly predictable text (AI-like)"
        elif normalized > 40:
            interpretation = "Medium perplexity - some predictability"
        else:
            interpretation = "High perplexity - varied and surprising (Human-like)"
        
        return {
            "score": round(normalized, 1),
            "raw_perplexity": round(perplexity, 2),
            "interpretation": interpretation
        }
    
    def calculate_burstiness(self) -> Dict:
        """
        Calculate sentence length variation (burstiness).
        Higher burstiness = more varied = likely human.
        """
        if len(self.sentences) < 2:
            return {"score": 0, "interpretation": "Insufficient sentences"}
        
        sentence_lengths = [len(s.split()) for s in self.sentences]
        
        if len(set(sentence_lengths)) == 1:
            return {"score": 0, "interpretation": "Uniform sentence lengths (Highly AI-like)"}
        
        mean_length = sum(sentence_lengths) / len(sentence_lengths)
        variance = sum((x - mean_length) ** 2 for x in sentence_lengths) / len(sentence_lengths)
        std_dev = math.sqrt(variance)
        
        # Coefficient of variation (burstiness measure)
        if mean_length > 0:
            cv = (std_dev / mean_length) * 100
        else:
            cv = 0
        
        # Normalize to 0-100
        normalized = min(100, cv * 2)
        
        interpretation = ""
        if normalized > 70:
            interpretation = "High burstiness - varied sentence lengths (Human-like)"
        elif normalized > 40:
            interpretation = "Medium burstiness - some variation"
        else:
            interpretation = "Low burstiness - uniform patterns (AI-like)"
        
        return {
            "score": round(normalized, 1),
            "coefficient_of_variation": round(cv, 2),
            "avg_sentence_length": round(mean_length, 1),
            "interpretation": interpretation
        }
    
    def calculate_readability(self) -> Dict:
        """
        Calculate Flesch-Kincaid readability score.
        AI text often clusters in Grade 8-10 range.
        """
        if len(self.sentences) == 0 or len(self.words) == 0:
            return {"score": 0, "flesch_kincaid_grade": 0, "interpretation": "Insufficient text"}
        
        # Count syllables (approximation)
        def count_syllables(word: str) -> int:
            word = word.lower()
            vowels = 'aeiouy'
            syllables = 0
            prev_was_vowel = False
            for char in word:
                is_vowel = char in vowels
                if is_vowel and not prev_was_vowel:
                    syllables += 1
                prev_was_vowel = is_vowel
            if word.endswith('e'):
                syllables -= 1
            return max(1, syllables)
        
        total_syllables = sum(count_syllables(w) for w in self.words)
        
        # Flesch-Kincaid Grade Level
        avg_sentence_length = len(self.words) / len(self.sentences)
        avg_syllables_per_word = total_syllables / len(self.words)
        
        fk_grade = (0.39 * avg_sentence_length) + (11.8 * avg_syllables_per_word) - 15.59
        fk_grade = max(0, fk_grade)
        
        # Check if in suspicious AI range (Grade 6-12 is common for AI)
        in_ai_range = 6 <= fk_grade <= 12
        
        # Score based on how "suspiciously" typical the readability is
        if in_ai_range:
            # Closer to 8-10 is more suspicious
            if 8 <= fk_grade <= 10:
                score = 80  # Highly suspicious
                interpretation = f"Grade {fk_grade:.1f} - Suspiciously typical AI readability range"
            else:
                score = 60  # Moderately suspicious
                interpretation = f"Grade {fk_grade:.1f} - Within common AI readability range"
        else:
            score = 30  # Less suspicious
            interpretation = f"Grade {fk_grade:.1f} - Outside typical AI readability range"
        
        return {
            "score": score,
            "flesch_kincaid_grade": round(fk_grade, 1),
            "avg_sentence_length": round(avg_sentence_length, 1),
            "avg_syllables_per_word": round(avg_syllables_per_word, 2),
            "interpretation": interpretation
        }
    
    def detect_ai_fingerprints(self) -> Dict:
        """
        Detect specific AI writing patterns and fingerprints.
        """
        text_lower = self.text.lower()
        
        # Count AI transitions
        transition_count = 0
        found_transitions = []
        for transition in self.AI_TRANSITIONS:
            count = text_lower.count(transition)
            if count > 0:
                transition_count += count
                found_transitions.append(f"'{transition}' ({count}x)")
        
        # Count generic openers
        opener_count = 0
        found_openers = []
        for opener in self.AI_OPENERS:
            if text_lower.startswith(opener) or f". {opener}" in text_lower:
                opener_count += 1
                found_openers.append(opener)
        
        # Check for repetitive n-grams (3-grams)
        trigrams = [tuple(self.words[i:i+3]) for i in range(len(self.words)-2)]
        trigram_counts = Counter(trigrams)
        repetitive_trigrams = [(tg, count) for tg, count in trigram_counts.items() if count > 2]
        
        # Calculate score
        score = 0
        details = []
        
        # Transition word density
        if len(self.words) > 0:
            transition_density = transition_count / len(self.words) * 100
            if transition_density > 2:
                score += 30
                details.append(f"High transition word density ({transition_density:.1f}%)")
            elif transition_density > 1:
                score += 15
                details.append(f"Moderate transition word density ({transition_density:.1f}%)")
        
        # Generic openers
        if opener_count > 0:
            score += min(25, opener_count * 10)
            details.append(f"Found {opener_count} generic AI opener(s)")
        
        # Repetitive patterns
        if repetitive_trigrams:
            score += min(20, len(repetitive_trigrams) * 5)
            details.append(f"Found {len(repetitive_trigrams)} repetitive 3-gram pattern(s)")
        
        # Check for formulaic structure
        paragraph_starts = [p.strip()[:30].lower() for p in self.text.split('\n\n') if p.strip()]
        formulaic_starts = sum(1 for p in paragraph_starts if any(
            p.startswith(w) for w in ['the', 'this', 'in', 'it', 'there']
        ))
        if len(paragraph_starts) > 2 and formulaic_starts / len(paragraph_starts) > 0.7:
            score += 15
            details.append("Formulaic paragraph structure detected")
        
        interpretation = ""
        if score > 60:
            interpretation = "Strong AI fingerprints detected"
        elif score > 30:
            interpretation = "Some AI patterns detected"
        else:
            interpretation = "Few or no AI fingerprints"
        
        return {
            "score": min(100, score),
            "transition_count": transition_count,
            "found_transitions": found_transitions[:5],  # Top 5
            "opener_count": opener_count,
            "found_openers": found_openers,
            "repetitive_patterns": len(repetitive_trigrams),
            "details": details,
            "interpretation": interpretation
        }
    
    def analyze(self) -> Dict:
        """Run all analyses and return comprehensive results."""
        perplexity = self.calculate_perplexity()
        burstiness = self.calculate_burstiness()
        readability = self.calculate_readability()
        fingerprints = self.detect_ai_fingerprints()
        
        # Calculate overall AI probability
        # Weight: perplexity (30%), burstiness (20%), readability (20%), fingerprints (30%)
        # Note: For perplexity, lower is more AI-like, so we invert
        perplexity_contribution = perplexity["score"] * 0.30
        burstiness_contribution = (100 - burstiness["score"]) * 0.20  # Invert: low burstiness = AI
        readability_contribution = readability["score"] * 0.20
        fingerprint_contribution = fingerprints["score"] * 0.30
        
        overall_score = perplexity_contribution + burstiness_contribution + readability_contribution + fingerprint_contribution
        
        # Determine verdict
        if overall_score > 60:
            verdict = "Likely AI-generated"
            confidence = "High" if overall_score > 75 else "Medium"
        elif overall_score > 35:
            verdict = "Uncertain - Mixed signals"
            confidence = "Low"
        else:
            verdict = "Likely human-written"
            confidence = "High" if overall_score < 20 else "Medium"
        
        return {
            "overall_ai_probability": round(overall_score, 1),
            "verdict": verdict,
            "confidence": confidence,
            "text_stats": {
                "word_count": len(self.words),
                "sentence_count": len(self.sentences),
                "avg_word_length": round(sum(len(w) for w in self.words) / max(1, len(self.words)), 1)
            },
            "perplexity": perplexity,
            "burstiness": burstiness,
            "readability": readability,
            "ai_fingerprints": fingerprints
        }


def print_results(results: Dict):
    """Print analysis results in a formatted way."""
    print("=" * 60)
    print("AI CONTENT DETECTION RESULTS")
    print("=" * 60)
    print()
    
    # Overall verdict
    prob = results["overall_ai_probability"]
    verdict = results["verdict"]
    confidence = results["confidence"]
    
    print(f"[STATS] OVERALL AI PROBABILITY: {prob}%")
    print(f"[TEXT] VERDICT: {verdict}")
    print(f"[TARGET] CONFIDENCE: {confidence}")
    print()
    
    # Text stats
    stats = results["text_stats"]
    print(f"[TREND] TEXT STATISTICS:")
    print(f"   Words: {stats['word_count']}")
    print(f"   Sentences: {stats['sentence_count']}")
    print(f"   Avg word length: {stats['avg_word_length']} chars")
    print()
    
    # Perplexity
    p = results["perplexity"]
    print(f"[CALC] PERPLEXITY ANALYSIS:")
    print(f"   Score: {p['score']}/100")
    if p.get('raw_perplexity') is not None:
        print(f"   Raw perplexity: {p['raw_perplexity']}")
    else:
        print(f"   Raw perplexity: N/A")
    print(f"   -> {p['interpretation']}")
    print()
    
    # Burstiness
    b = results["burstiness"]
    print(f"[RULE] BURSTINESS DETECTION:")
    print(f"   Score: {b['score']}/100")
    if b.get('coefficient_of_variation') is not None:
        print(f"   Variation coefficient: {b['coefficient_of_variation']}%")
        print(f"   Avg sentence length: {b['avg_sentence_length']} words")
    else:
        print(f"   Variation coefficient: N/A")
        print(f"   Avg sentence length: N/A")
    print(f"   -> {b['interpretation']}")
    print()
    
    # Readability
    r = results["readability"]
    print(f"[BOOK] READABILITY SCORING:")
    print(f"   AI-suspicion score: {r['score']}/100")
    print(f"   Flesch-Kincaid Grade: {r['flesch_kincaid_grade']}")
    print(f"   -> {r['interpretation']}")
    print()
    
    # AI Fingerprints
    f = results["ai_fingerprints"]
    print(f"[SEARCH] AI FINGERPRINT DETECTION:")
    print(f"   Score: {f['score']}/100")
    print(f"   Transition words found: {f['transition_count']}")
    print(f"   Generic openers found: {f['opener_count']}")
    print(f"   Repetitive patterns: {f['repetitive_patterns']}")
    if f.get('found_transitions'):
        print(f"   Top transitions: {', '.join(f['found_transitions'][:3])}")
    else:
        print(f"   Top transitions: (none detected)")
    if f.get('details'):
        print(f"   Details: {'; '.join(f['details'])}")
    else:
        print(f"   Details: (none)")
    print(f"   -> {f['interpretation']}")
    print()
    
    print("=" * 60)
    print("[!] DISCLAIMER: AI detection is not 100% accurate.")
    print("   Results should be used as guidance, not definitive proof.")
    print("=" * 60)


def main():
    """Main entry point."""
    import json
    
    # Check for output format argument
    output_json = '--json' in sys.argv
    if output_json:
        sys.argv.remove('--json')
    
    # Read text from stdin or command line argument
    if len(sys.argv) > 1:
        # Read from file
        file_path = sys.argv[1]
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
        except Exception as e:
            print(f"Error reading file: {e}")
            sys.exit(1)
    else:
        # Read from stdin
        print("Enter text to analyze (Ctrl+D/Ctrl+Z when done):", file=sys.stderr)
        text = sys.stdin.read()
    
    if not text.strip():
        print("Error: No text provided.")
        print("Usage: python detect_ai.py [file_path] [--json]", file=sys.stderr)
        sys.exit(1)
    
    # Run analysis
    detector = AIDetector(text)
    results = detector.analyze()
    
    # Print results - use JSON if requested
    if output_json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        print_results(results)


if __name__ == "__main__":
    main()
