import re
from collections import Counter


class VoiceAnalyzer:
    """
    Calculates linguistic density, sentence complexity, and
    lexical variety to define a Brand Voice baseline.
    """

    STOP_WORDS = {
        'the', 'and', 'is', 'to', 'in', 'of', 'a', 'with', 'for',
        'on', 'at', 'by', 'an', 'be', 'as', 'it', 'its', 'or', 'are',
        'was', 'were', 'this', 'that', 'from', 'we', 'our', 'you', 'your',
        'they', 'their', 'but', 'not', 'have', 'has', 'had', 'do', 'does',
    }

    def __init__(self, text: str):
        self.text = text
        self.words = re.findall(r"\w+", text.lower())
        self.sentences = [s.strip() for s in re.split(r"[.!?]+", text) if s.strip()]

    # ------------------------------------------------------------------
    # Core metrics
    # ------------------------------------------------------------------

    def get_lexical_density(self) -> float:
        """Unique words / total words × 100."""
        if not self.words:
            return 0.0
        return round(len(set(self.words)) / len(self.words) * 100, 2)

    def get_avg_sentence_length(self) -> float:
        """Mean word count per sentence."""
        if not self.sentences:
            return 0.0
        lengths = [len(s.split()) for s in self.sentences]
        return round(sum(lengths) / len(lengths), 2)

    def get_cadence_variance(self) -> float:
        """
        Standard deviation of sentence lengths.
        Low  → clinical / authoritative precision
        High → conversational / narrative energy
        """
        if len(self.sentences) < 2:
            return 0.0
        lengths = [len(s.split()) for s in self.sentences]
        mean = sum(lengths) / len(lengths)
        variance = sum((x - mean) ** 2 for x in lengths) / len(lengths)
        return round(variance ** 0.5, 2)

    def get_sentiment_temperature(self) -> float:
        """
        Rough 0.0–1.0 emotional temperature based on
        positive / negative word ratio in the corpus.
        0.0 = cold/clinical, 1.0 = warm/enthusiastic
        """
        positive = {
            'great', 'excellent', 'innovative', 'powerful', 'leading', 'best',
            'easy', 'simple', 'amazing', 'love', 'fantastic', 'brilliant',
        }
        negative = {
            'bad', 'poor', 'fail', 'broken', 'slow', 'complex', 'difficult',
            'hard', 'issue', 'problem', 'error', 'wrong', 'lost', 'down',
        }
        pos = sum(1 for w in self.words if w in positive)
        neg = sum(1 for w in self.words if w in negative)
        total = pos + neg
        if total == 0:
            return 0.5  # neutral default
        return round(pos / total, 2)

    def top_n_keywords(self, n: int = 10) -> list[tuple[str, int]]:
        """Most frequent non-stop-word tokens."""
        filtered = [w for w in self.words if w not in self.STOP_WORDS and len(w) > 2]
        return Counter(filtered).most_common(n)

    # ------------------------------------------------------------------
    # Aggregate report
    # ------------------------------------------------------------------

    def generate_report(self) -> dict:
        return {
            "lexical_density_percent": self.get_lexical_density(),
            "avg_sentence_length": self.get_avg_sentence_length(),
            "cadence_variance": self.get_cadence_variance(),
            "sentiment_temperature": self.get_sentiment_temperature(),
            "core_keywords": self.top_n_keywords(),
            "total_words": len(self.words),
            "total_sentences": len(self.sentences),
        }

    def print_report(self) -> None:
        report = self.generate_report()
        print("=" * 50)
        print("  BRAND VOICE LINGUISTIC AUDIT")
        print("=" * 50)
        print(f"  Total words       : {report['total_words']}")
        print(f"  Total sentences   : {report['total_sentences']}")
        print(f"  Lexical density   : {report['lexical_density_percent']}%")
        print(f"  Avg sentence len  : {report['avg_sentence_length']} words")
        print(f"  Cadence variance  : {report['cadence_variance']} (σ)")
        print(f"  Sentiment temp.   : {report['sentiment_temperature']} / 1.0")
        print("\n  TOP KEYWORDS:")
        for word, count in report["core_keywords"]:
            print(f"    {word:<20} {count}")
        print("=" * 50)


# ------------------------------------------------------------------
# CLI usage
# ------------------------------------------------------------------
if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        # Accept a file path or inline text
        arg = sys.argv[1]
        try:
            with open(arg, "r", encoding="utf-8") as f:
                corpus = f.read()
        except FileNotFoundError:
            corpus = arg  # treat as raw text
    else:
        corpus = input("Paste corpus text and press Enter:\n> ")

    analyzer = VoiceAnalyzer(corpus)
    analyzer.print_report()
