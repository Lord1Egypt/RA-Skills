import importlib.util
import unittest
from unittest.mock import patch
from pathlib import Path

from bs4 import BeautifulSoup


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("assemble", ROOT / "scripts" / "assemble.py")
assemble = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(assemble)


def article(paragraphs=None, translations=None):
    return {
        "num": 1,
        "title": "Preface",
        "title_dest_language": "序言",
        "section": "Preface",
        "section_dest_language": "序言",
        "paragraphs": paragraphs or ["Source one.", "Source two."],
        "translated_paragraphs": translations or ["译文一。", "译文二。"],
        "summary_dest_language": "摘要。",
    }


class AssembleOrderTest(unittest.TestCase):
    def test_fails_when_payload_article_count_was_truncated(self):
        payload = {
            "total_articles": 2,
            "articles": [article()],
        }

        with self.assertRaisesRegex(RuntimeError, "contains 1 articles but total_articles is 2"):
            assemble.validate_article_inventory(payload)

    def test_fails_when_payload_count_hides_source_epub_article_count(self):
        payload = {
            "input_epub": "/tmp/book.epub",
            "total_articles": 1,
            "articles": [article()],
        }

        with patch.object(assemble, "count_source_articles", return_value=2):
            with self.assertRaisesRegex(RuntimeError, "source EPUB contains 2 translatable articles"):
                assemble.validate_article_inventory(payload)

    def test_translation_css_uses_consistently_smaller_target_text(self):
        self.assertIn("font-size: smaller", assemble.CSS_TEXT)
        self.assertNotIn("font-family", assemble.CSS_TEXT)
        self.assertIn("font-style: normal", assemble.CSS_TEXT)
        self.assertIn("break-inside: auto", assemble.CSS_TEXT)
        self.assertIn("page-break-inside: auto", assemble.CSS_TEXT)
        self.assertIn("overflow: visible", assemble.CSS_TEXT)
        self.assertIn("max-height: none", assemble.CSS_TEXT)

    def test_translation_paragraph_preserves_source_classes_for_alignment_without_inline_font_size(self):
        html = (
            b'<html><body><h1>Preface</h1><p class="calibre1 body" '
            b'style="font-size: 1.1em; text-align: center; margin-left: 2em">Source one.</p></body></html>'
        )

        output = assemble.process_article_html(
            html,
            article(paragraphs=["Source one."], translations=["译文一。"]),
        )
        soup = BeautifulSoup(output.decode("utf-8"), "lxml")
        target = soup.select_one("p.dest_translation")

        self.assertEqual(target.get("style"), "text-align: center; margin-left: 2em")
        self.assertEqual(target.get("class"), ["calibre1", "body", "dest_translation"])

    def test_inserts_translation_after_div_para_source_paragraph(self):
        html = (
            b'<html><body><h2 class="chapter-title">1 Atoms in Motion</h2>'
            b'<div class="para">Source one.</div></body></html>'
        )

        output = assemble.process_article_html(
            html,
            article(paragraphs=["Source one."], translations=["译文一。"]),
        )
        soup = BeautifulSoup(output.decode("utf-8"), "lxml")
        source = soup.select_one("div.para")
        target = source.find_next_sibling("p")

        self.assertEqual(
            assemble.norm_text(soup.select_one("h2.chapter-title").get_text(" ")),
            "Preface | 序言",
        )
        self.assertIn("dest_translation", target.get("class"))
        self.assertEqual(assemble.norm_text(target.get_text(" ")), "译文一。")

    def test_inserts_each_translation_immediately_after_its_source_paragraph(self):
        html = b"<html><body><h1>Preface</h1><p>Source one.</p><p>Source two.</p></body></html>"

        output = assemble.process_article_html(html, article())
        soup = BeautifulSoup(output.decode("utf-8"), "lxml")
        paragraphs = soup.body.find_all("p", recursive=False)

        self.assertEqual(assemble.norm_text(paragraphs[0].get_text(" ")), "Source one.")
        self.assertEqual(assemble.norm_text(paragraphs[1].get_text(" ")), "译文一。")
        self.assertIn("dest_translation", paragraphs[1].get("class"))
        self.assertEqual(assemble.norm_text(paragraphs[2].get_text(" ")), "Source two.")
        self.assertEqual(assemble.norm_text(paragraphs[3].get_text(" ")), "译文二。")
        self.assertIn("dest_translation", paragraphs[3].get("class"))

    def test_math_aware_matching_clones_source_equations_and_normalizes_translation_math(self):
        html = (
            b'<html><body><h1>Preface</h1><div class="para">'
            b'<div class="first-text">The value <span class="eq-inline" title="D_N^2">D</span> is</div>'
            b'<div class="eq-num"><div class="eq-img"><img src="eq/e.svg"/></div>'
            b'<div class="eq-tag">(6.9)</div></div></div></body></html>'
        )

        output = assemble.process_article_html(
            html,
            article(
                paragraphs=["The value D_N^2 is (6.9)"],
                translations=["值 D_N^2、D2N、NH、Drms、Qrms、X_{i+1}^2 和 10^-3。"],
            ),
        )
        soup = BeautifulSoup(output.decode("utf-8"), "lxml")
        source = soup.select_one("div.para")
        target = source.find_next_sibling("p")
        equation = target.find_next_sibling("div")

        self.assertEqual(
            assemble.norm_text(target.get_text(" ")),
            "值 𝐷²ₙ、𝐷²ₙ、𝑁ₕ、𝐷ᵣₘₛ、𝑄ᵣₘₛ、𝑋²ᵢ₊₁ 和 10⁻³。",
        )
        self.assertIn("dest_translation_equation", equation.get("class"))
        self.assertEqual(assemble.norm_text(equation.get_text(" ")), "(6.9)")

    def test_math_variables_are_italicized_in_translated_math_context(self):
        text = "概率 P(k,n) 是：P(k,n) = (n_k)p^kq^{n-k}。令 p 为 W 的概率，q 为 L 的概率。"

        self.assertEqual(
            assemble.normalize_translation_math(text),
            "概率 𝑃(𝑘,𝑛) 是：𝑃(𝑘,𝑛) = (ⁿₖ)𝑝ᵏ𝑞ⁿ⁻ᵏ。令 𝑝 为 𝑊 的概率，𝑞 为 𝐿 的概率。",
        )

    def test_binomial_coefficient_renders_as_stacked_html_in_translation(self):
        html = b"<html><body><h1>Preface</h1><p>Source one.</p></body></html>"

        output = assemble.process_article_html(
            html,
            article(paragraphs=["Source one."], translations=["P(k,n) = (n_k)p^kq^{n-k}."]),
        )
        soup = BeautifulSoup(output.decode("utf-8"), "lxml")
        target = soup.select_one("p.dest_translation")
        binom = target.select_one(".dest_binom")

        self.assertIsNotNone(binom)
        self.assertEqual(binom.get("data-num"), "n")
        self.assertEqual(binom.get("data-den"), "k")
        self.assertEqual([s.get_text() for s in binom.select(".dest_binom_stack span")], ["𝑛", "𝑘"])
        self.assertEqual(
            assemble.translation_text_for_validation(target),
            "𝑃(𝑘,𝑛) = (ⁿₖ)𝑝ᵏ𝑞ⁿ⁻ᵏ.",
        )

    def test_existing_unicode_binomial_coefficient_renders_as_stacked_html(self):
        html = assemble.translation_math_html("方式数是 (ⁿₖ)，且 (ⁿₖ) = n!/[k!(n-k)!]。")
        soup = BeautifulSoup(f"<p>{html}</p>", "lxml")

        self.assertEqual(len(soup.select(".dest_binom")), 2)
        self.assertEqual(
            [s.get_text() for s in soup.select_one(".dest_binom_stack").select("span")],
            ["𝑛", "𝑘"],
        )
        self.assertEqual(
            assemble.translation_text_for_validation(soup.p),
            "方式数是 (ⁿₖ)，且 (ⁿₖ) = 𝑛!/[𝑘!(𝑛-𝑘)!]。",
        )

    def test_fails_when_a_source_paragraph_cannot_be_matched(self):
        html = b"<html><body><h1>Preface</h1><p>Source one.</p></body></html>"

        with self.assertRaisesRegex(RuntimeError, "matched 1 of 2 source paragraphs"):
            assemble.process_article_html(html, article())

    def test_fails_when_translation_count_does_not_match_source_count(self):
        html = b"<html><body><h1>Preface</h1><p>Source one.</p><p>Source two.</p></body></html>"

        with self.assertRaisesRegex(RuntimeError, "has 1 translations for 2 source paragraphs"):
            assemble.process_article_html(html, article(translations=["译文一。"]))


if __name__ == "__main__":
    unittest.main()
