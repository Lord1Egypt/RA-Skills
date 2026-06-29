import importlib.util
import unittest
from pathlib import Path

from bs4 import BeautifulSoup


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("extract", ROOT / "scripts" / "extract.py")
extract = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(extract)


class ExtractFeynmanStyleTest(unittest.TestCase):
    def test_extracts_div_para_book_chapters(self):
        html = """
        <html>
          <head><title>FLP Vol. 1, Ch. 1</title></head>
          <body>
            <div class="chapter">
              <h2 class="title chapter-title">1 Atoms in Motion</h2>
              <div class="section">
                <h3 class="title section-title">1-1 Introduction</h3>
                <div class="para"><div class="first-text">First source paragraph with enough content.</div></div>
                <div class="para"><div class="first-text">Second source paragraph with enough content.</div></div>
              </div>
            </div>
          </body>
        </html>
        """
        soup = BeautifulSoup(html, "lxml")

        self.assertEqual(extract.classify_page(soup, "OEBPS/I_01.xhtml"), "article")
        self.assertEqual(extract.extract_title(soup), "1 Atoms in Motion")
        self.assertEqual(
            extract.get_translatable_paragraphs(soup),
            [
                "First source paragraph with enough content.",
                "Second source paragraph with enough content.",
            ],
        )

    def test_extracts_inline_math_titles_into_paragraph_text(self):
        html = """
        <html><body>
          <h2 class="title chapter-title">6 Probability</h2>
          <div class="para">
            The value <span class="eq-inline" title="D_N^2"><span>D</span></span>
            equals <span class="svg-inline" title="\\tfrac{1}{7}"><img src="eq/x.svg"/></span>.
          </div>
        </body></html>
        """
        soup = BeautifulSoup(html, "lxml")

        self.assertEqual(
            extract.get_translatable_paragraphs(soup),
            ["The value 𝐷²ₙ equals 1/7."],
        )


if __name__ == "__main__":
    unittest.main()
