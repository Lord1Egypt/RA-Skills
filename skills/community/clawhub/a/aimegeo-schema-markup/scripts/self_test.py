#!/usr/bin/env python3
"""Business regression tests; standard library only, no network or host configuration."""

import json
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
from pathlib import Path

sys.dont_write_bytecode = True
from schema_tool import CONTEXT, add_context, embed, load_json, validate, read_and_check


ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "scripts" / "schema_tool.py"


def organization(**extra):
    return {"@context": CONTEXT, "@type": "Organization", "name": "演示资料", **extra}


def faq(answer=None):
    question = {"@type": "Question", "name": "如何导出？"}
    if answer is not None:
        question["acceptedAnswer"] = answer
    return {"@context": CONTEXT, "@type": "FAQPage", "mainEntity": [question]}


def codes(report):
    return {entry["code"] for entry in report["errors"]}


class SchemaBusinessTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="schema-skill-test-")
        self.base = Path(self.temp.name)

    def tearDown(self):
        self.temp.cleanup()

    def write_json(self, name, value):
        path = self.base / name
        path.write_text(json.dumps(value, ensure_ascii=False), encoding="utf-8")
        return path

    def cli(self, *args):
        result = subprocess.run([sys.executable, str(TOOL), *map(str, args)],
                                cwd=self.base, capture_output=True, text=True, timeout=15)
        self.assertEqual(result.stderr, "", result.stderr)
        return result.returncode, json.loads(result.stdout)

    def test_sample_delivers_five_faqs_and_matching_html(self):
        sample = ROOT / "examples" / "company-faq"
        target = self.base / "result"
        status, report = self.cli("build", sample / "draft.json", "--visible-text", sample / "visible.txt", "--output-dir", target)
        self.assertEqual(status, 0)
        self.assertTrue(report["local_valid"])
        self.assertEqual(report["content_check"]["matched_fields"], 12)
        self.assertEqual(report["content_check"]["matched_faq_pairs"], 5)
        self.assertEqual(report["counts"], {"typed_nodes": 12, "root_entities": 2})
        schema = load_json(target / "schema.json")
        self.assertEqual(schema, add_context(load_json(sample / "draft.json")))
        raw_html = (target / "嵌入片段.html").read_text(encoding="utf-8")
        payload = raw_html.split(">", 1)[1].rsplit("</script>", 1)[0]
        self.assertEqual(json.loads(payload), schema)
        self.assertEqual(load_json(target / "校验结果.json"), report)
        self.assertEqual(report["google_rich_results"]["status"], "not_run")

    def test_sample_matches_original_facts_and_no_invented_fields(self):
        sample = ROOT / "examples" / "company-faq"
        source = load_json(sample / "source.json")
        draft = load_json(sample / "draft.json")
        org, page = draft["@graph"]
        for field, value in source["organization"].items():
            self.assertEqual(org[field], value)
        actual_pairs = [(q["name"], q["acceptedAnswer"]["text"]) for q in page["mainEntity"]]
        self.assertEqual(actual_pairs, [(q["question"], q["answer"]) for q in source["faqs"]])
        for node in draft["@graph"]:
            self.assertFalse({"offers", "aggregateRating", "datePublished"} & node.keys())

    def test_unknown_product_price_and_rating_are_never_created(self):
        source = self.write_json("product.json", {"@type": "Product", "name": "演示产品"})
        status, report = self.cli("build", source, "--output-dir", self.base / "out")
        self.assertEqual(status, 0)
        self.assertTrue(report["local_valid"])
        self.assertEqual(load_json(self.base / "out" / "schema.json"),
                         {"@context": CONTEXT, "@type": "Product", "name": "演示产品"})

    def test_unknown_article_dates_are_omitted_and_disclosed(self):
        draft = {"@type": "Article", "headline": "资料保存方法"}
        prepared = add_context(draft)
        self.assertEqual(set(prepared) - set(draft), {"@context"})
        self.assertNotIn("datePublished", prepared)
        report = validate(prepared)
        self.assertTrue(report["local_valid"])
        self.assertEqual({w["path"] for w in report["warnings"]}, {"/author", "/datePublished"})

    def test_json_array_multitype_and_reference_are_supported(self):
        report = validate(load_json(ROOT / "examples" / "array.json"))
        self.assertTrue(report["local_valid"])
        self.assertEqual(report["counts"], {"typed_nodes": 2, "root_entities": 2})

    def test_missing_faq_answer_fails_at_exact_nested_path(self):
        source = ROOT / "examples" / "faq-missing-answer" / "input.json"
        status, report = self.cli("build", source, "--output-dir", self.base / "out")
        self.assertEqual(status, 1)
        self.assertIn("/@graph/1/mainEntity/0/acceptedAnswer", {e["path"] for e in report["errors"]})
        self.assertEqual({p.name for p in (self.base / "out").iterdir()}, {"校验结果.json"})

    def test_answer_missing_or_empty_text_fails(self):
        for answer in ({"@type": "Answer"}, {"@type": "Answer", "text": " "}):
            with self.subTest(answer=answer):
                report = validate(faq(answer))
                self.assertFalse(report["local_valid"])
                self.assertIn("required_field", codes(report))

    def test_wrong_relation_shape_fails_without_exception(self):
        for answer in ([], "没有对象", [{"@type": "Answer", "text": "导出"}], {"@type": [{}]}):
            with self.subTest(answer=answer):
                self.assertIn("relation_type", codes(validate(faq(answer))))

    def test_root_and_graph_boundaries_fail(self):
        for data in (None, "text", 3, [], [5], [[organization()]], {"@context": CONTEXT, "@graph": {}},
                     {"@context": CONTEXT, "@graph": []}):
            with self.subTest(data=data):
                self.assertFalse(validate(data)["local_valid"])

    def test_malformed_type_is_a_report_not_a_crash(self):
        for raw_type in (None, {}, [], ["Article", {}], [True], " "):
            with self.subTest(raw_type=raw_type):
                self.assertIn("type_format", codes(validate(organization(**{"@type": raw_type}))))

    def test_references_are_resolved_and_type_checked(self):
        document = {"@context": CONTEXT, "@graph": [
            {"@type": "Organization", "@id": "#org", "name": "演示"},
            {"@type": "Article", "headline": "演示", "publisher": {"@id": "#org"}}]}
        self.assertTrue(validate(document)["local_valid"])
        document["@graph"][0]["@type"] = "Person"
        self.assertTrue(validate(document)["local_valid"])
        document["@graph"][0]["@type"] = "Product"
        self.assertIn("reference_type", codes(validate(document)))
        document["@graph"][1]["publisher"]["@id"] = "#missing"
        self.assertIn("unresolved_local_reference", codes(validate(document)))

    def test_external_reference_is_unchecked_and_not_fetched(self):
        report = validate(organization(parentOrganization={"@id": "https://example.org/other"}))
        self.assertTrue(report["local_valid"])
        self.assertIn("external_reference_unchecked", {w["code"] for w in report["warnings"]})

    def test_duplicate_definitions_fail(self):
        report = validate([organization(**{"@id": "#same"}), organization(**{"@id": "#same"})])
        self.assertIn("duplicate_id", codes(report))

    def test_offer_arrays_allow_confirmed_zero_and_decimal_prices(self):
        offers = [{"@type": "Offer", "price": 0, "priceCurrency": "CNY"},
                  {"@type": "Offer", "price": "9.90", "priceCurrency": "CNY"}]
        self.assertTrue(validate({"@context": CONTEXT, "@type": "Product", "name": "演示", "offers": offers})["local_valid"])

    def test_invalid_price_and_currency_are_rejected(self):
        for price in (-1, "￥99", "unknown", True, None, [], "NaN"):
            with self.subTest(price=price):
                data = {"@context": CONTEXT, "@type": "Offer", "price": price, "priceCurrency": "CNY"}
                self.assertIn("price_number", codes(validate(data)))
        self.assertIn("currency_format", codes(validate({"@context": CONTEXT, "@type": "Offer", "price": 1, "priceCurrency": "元"})))

    def test_rating_requires_real_count_and_valid_scale(self):
        good = {"@context": CONTEXT, "@type": "AggregateRating", "ratingValue": "8.2", "bestRating": 10, "reviewCount": 9}
        self.assertTrue(validate(good)["local_valid"])
        for change in ({"reviewCount": 0}, {"reviewCount": True}, {"ratingValue": 11}, {"reviewCount": "1.5"}):
            with self.subTest(change=change):
                self.assertFalse(validate({**good, **change})["local_valid"])
        del good["reviewCount"]
        self.assertIn("rating_count", codes(validate(good)))

    def test_calendar_dates_and_explicit_dates(self):
        for value in ("2025-02-29", "2026-13-01", "today", 20261019):
            self.assertIn("date_format", codes(validate(organization(foundingDate=value))))
        for value in ("2024-02-29", "2026-10-19T10:30:00+08:00"):
            self.assertTrue(validate(organization(foundingDate=value))["local_valid"])

    def test_check_requires_context_and_build_adds_only_context(self):
        data = {"@type": "Organization", "name": "演示"}
        self.assertIn("missing_context", codes(validate(data)))
        self.assertEqual(add_context(data), {**data, "@context": CONTEXT})
        self.assertNotIn("@context", data)

    def test_context_strings_and_vocab_with_slash_are_supported(self):
        for context in (CONTEXT, CONTEXT + "/", {"@vocab": CONTEXT + "/"}):
            with self.subTest(context=context):
                report = validate(organization(**{"@context": context}))
                self.assertTrue(report["local_valid"], report["errors"])
                self.assertEqual(report["warnings"], [])
        for context in ("http://schema.org", "http://schema.org/"):
            with self.subTest(context=context):
                report = validate(organization(**{"@context": context}))
                self.assertTrue(report["local_valid"])
                self.assertIn("http_context", {w["code"] for w in report["warnings"]})

    def test_vocab_without_trailing_slash_blocks_build(self):
        source = self.write_json("vocab.json", organization(**{"@context": {"@vocab": CONTEXT}}))
        target = self.base / "out"
        status, report = self.cli("build", source, "--output-dir", target)
        self.assertEqual(status, 1)
        self.assertFalse(report["local_valid"])
        self.assertIn("unsupported_context", codes(report))
        self.assertIn(("unsupported_context", "/@context/@vocab"),
                      {(e["code"], e["path"]) for e in report["errors"]})
        self.assertEqual({p.name for p in target.iterdir()}, {"校验结果.json"})
        self.assertEqual(load_json(target / "校验结果.json"), report)

    def test_array_empty_values_fail_at_exact_recursive_paths(self):
        for value in (None, "", " \t", {}, []):
            for wrapped, path in (([value], "/telephone/0"),
                                  ([[value]], "/telephone/0/0"),
                                  ([{"value": [value]}], "/telephone/0/value/0")):
                with self.subTest(value=value, path=path):
                    report = validate(organization(telephone=wrapped))
                    self.assertFalse(report["local_valid"])
                    self.assertIn(("empty_value", path),
                                  {(e["code"], e["path"]) for e in report["errors"]})

    def test_array_nonempty_values_remain_valid(self):
        report = validate(organization(telephone=["+86-010-12345678"],
                                       contactPoint=[{"@type": "ContactPoint", "telephone": "+86-010-87654321"}]))
        self.assertTrue(report["local_valid"], report["errors"])
        # Generic recursion must not mistake JSON zero or false for missing data.
        self.assertTrue(validate(organization(additionalProperty=[0, False]))["local_valid"])

    def test_array_placeholders_block_build(self):
        for index, value in enumerate((None, "", {})):
            with self.subTest(value=value):
                source = self.write_json("array.json", organization(telephone=[value]))
                target = self.base / str(index)
                status, report = self.cli("build", source, "--output-dir", target)
                self.assertEqual(status, 1)
                self.assertFalse(report["local_valid"])
                self.assertIn("empty_value", codes(report))
                self.assertEqual({p.name for p in target.iterdir()}, {"校验结果.json"})

    def test_breadcrumb_graph_references_resolve_in_document_order(self):
        breadcrumb = {"@type": "BreadcrumbList", "itemListElement": [{"@id": "#home"}, {"@id": "#help"}]}
        home = {"@type": "ListItem", "@id": "#home", "position": 1, "name": "首页"}
        help_item = {"@type": "ListItem", "@id": "#help", "position": 2, "name": "帮助"}
        for nodes in ([breadcrumb, help_item, home], [home, help_item, breadcrumb]):
            with self.subTest(nodes=nodes):
                report = validate({"@context": CONTEXT, "@graph": nodes})
                self.assertTrue(report["local_valid"], report["errors"])
                self.assertEqual(report["counts"], {"typed_nodes": 3, "root_entities": 3})
        mixed = {"@context": CONTEXT, "@graph": [
            {**breadcrumb, "itemListElement": [{"@id": "#home"}, {k: v for k, v in help_item.items() if k != "@id"}]}, home]}
        self.assertTrue(validate(mixed)["local_valid"])

    def test_breadcrumb_references_reject_invalid_order_and_type(self):
        for positions in ((2, 1), (1, 3), (1, 1)):
            with self.subTest(positions=positions):
                document = {"@context": CONTEXT, "@graph": [
                    {"@type": "BreadcrumbList", "itemListElement": [{"@id": "#a"}, {"@id": "#b"}]},
                    {"@type": "ListItem", "@id": "#a", "position": positions[0], "name": "首页"},
                    {"@type": "ListItem", "@id": "#b", "position": positions[1], "name": "帮助"}]}
                report = validate(document)
                self.assertFalse(report["local_valid"])
                self.assertIn("breadcrumb_positions", codes(report))
        document = {"@context": CONTEXT, "@graph": [
            {"@type": "BreadcrumbList", "itemListElement": [{"@id": "#a"}]},
            {"@type": "Organization", "@id": "#a", "position": 1, "name": "演示"}]}
        self.assertIn("reference_type", codes(validate(document)))
        document["@graph"].pop()
        self.assertIn("unresolved_local_reference", codes(validate(document)))

    def test_advanced_context_and_keywords_are_explicit_failures(self):
        for context in ([], 7, "https://example.org/context", {"label": "https://schema.org/name"}):
            self.assertIn("unsupported_context", codes(validate(organization(**{"@context": context}))))
        self.assertIn("unsupported_keyword", codes(validate(organization(**{"@reverse": {}}))))

    def test_literal_content_mismatch_fails_with_path(self):
        report = validate(organization(description="支持导出资料。"), "演示资料 支持查询资料。")
        self.assertEqual(report["content_check"]["status"], "mismatch")
        self.assertIn("/description", {e["path"] for e in report["errors"]})

    def test_swapped_faq_answers_fail_even_if_all_text_is_present(self):
        sample = ROOT / "examples" / "company-faq"
        data = add_context(load_json(sample / "draft.json"))
        questions = data["@graph"][1]["mainEntity"]
        questions[0]["acceptedAnswer"], questions[1]["acceptedAnswer"] = questions[1]["acceptedAnswer"], questions[0]["acceptedAnswer"]
        report = validate(data, (sample / "visible.txt").read_text(encoding="utf-8"))
        self.assertEqual(report["content_check"]["matched_fields"], 12)
        self.assertIn("faq_pair_mismatch", codes(report))
        self.assertEqual(report["content_check"]["matched_faq_pairs"], 3)

    def test_faq_pages_share_question_boundaries_across_graph_and_root_array(self):
        body = "如何退款？ 联系人工客服。 如何导出？ 在账单页申请。"
        for layout in ("graph", "array"):
            with self.subTest(layout=layout):
                pages = [{"@type": "FAQPage", "mainEntity": [
                    {"@type": "Question", "name": name,
                     "acceptedAnswer": {"@type": "Answer", "text": "在账单页申请。"}}]}
                    for name in ("如何退款？", "如何导出？")]
                data = ({"@context": CONTEXT, "@graph": pages} if layout == "graph"
                        else [{"@context": CONTEXT, **page} for page in pages])
                report = validate(data, body)
                self.assertFalse(report["local_valid"])
                self.assertEqual(report["content_check"]["checked_faq_pairs"], 2)
                self.assertEqual(report["content_check"]["matched_faq_pairs"], 1)
                prefix = "/@graph/0" if layout == "graph" else "/0"
                self.assertIn(("faq_pair_mismatch", prefix + "/mainEntity/0/acceptedAnswer"),
                              {(error["code"], error["path"]) for error in report["errors"]})
                target = data["@graph"][0] if layout == "graph" else data[0]
                target["mainEntity"][0]["acceptedAnswer"]["text"] = "联系人工客服。"
                report = validate(data, body)
                self.assertTrue(report["local_valid"], report["errors"])
                self.assertEqual(report["content_check"]["matched_faq_pairs"], 2)

    def test_shared_faq_boundaries_resolve_questions_and_answers_defined_later(self):
        data = {"@context": CONTEXT, "@graph": [
            {"@type": "FAQPage", "mainEntity": [{"@id": "#refund"}]},
            {"@type": "FAQPage", "mainEntity": [{"@id": "#export"}]},
            {"@type": "Question", "@id": "#refund", "name": "如何退款？",
             "acceptedAnswer": {"@id": "#refund-answer"}},
            {"@type": "Question", "@id": "#export", "name": "如何导出？",
             "acceptedAnswer": {"@type": "Answer", "text": "在账单页申请。"}},
            {"@type": "Answer", "@id": "#refund-answer", "text": "在账单页申请。"}]}
        body = "如何退款？ 联系人工客服。 如何导出？ 在账单页申请。"
        report = validate(data, body)
        self.assertFalse(report["local_valid"])
        self.assertIn("faq_pair_mismatch", codes(report))
        self.assertEqual(report["content_check"]["matched_faq_pairs"], 1)
        data["@graph"][4]["text"] = "联系人工客服。"
        report = validate(data, body)
        self.assertTrue(report["local_valid"], report["errors"])
        self.assertEqual(report["content_check"]["matched_faq_pairs"], 2)

    def test_separate_faq_pages_keep_quoted_question_inside_its_real_answer(self):
        answer = "关于‘如何退款？’，请联系支持。"
        data = {"@context": CONTEXT, "@graph": [
            {"@type": "FAQPage", "mainEntity": [
                {"@type": "Question", "name": "如何退款？",
                 "acceptedAnswer": {"@type": "Answer", "text": answer}}]},
            {"@type": "FAQPage", "mainEntity": [
                {"@type": "Question", "name": "如何导出？",
                 "acceptedAnswer": {"@type": "Answer", "text": "点击导出。"}}]}]}
        report = validate(data, "如何退款？ " + answer + " 如何导出？ 点击导出。")
        self.assertTrue(report["local_valid"], report["errors"])
        self.assertEqual(report["content_check"]["matched_faq_pairs"], 2)

    def test_answer_html_and_whitespace_are_normalized(self):
        report = validate(faq({"@type": "Answer", "text": "<p>点击 <b>导出</b>。</p>"}), "如何导出？\n点击   导出。")
        self.assertTrue(report["local_valid"])
        self.assertEqual(report["content_check"]["matched_faq_pairs"], 1)

    def test_short_question_cannot_borrow_long_question_answer(self):
        data = {"@context": CONTEXT, "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": "如何退款？", "acceptedAnswer": {"@type": "Answer", "text": "在账单页申请。"}},
            {"@type": "Question", "name": "自动续费如何退款？", "acceptedAnswer": {"@type": "Answer", "text": "在账单页申请。"}}]}
        body = "如何退款？→联系人工客服；自动续费如何退款？→在账单页申请。"
        report = validate(data, body)
        self.assertFalse(report["local_valid"])
        self.assertEqual(report["content_check"]["matched_faq_pairs"], 1)
        self.assertIn(("faq_pair_mismatch", "/mainEntity/0/acceptedAnswer"),
                      {(e["code"], e["path"]) for e in report["errors"]})
        data["mainEntity"][0]["acceptedAnswer"]["text"] = "联系人工客服"
        report = validate(data, body)
        self.assertTrue(report["local_valid"], report["errors"])
        self.assertEqual(report["content_check"]["matched_faq_pairs"], 2)

    def test_internal_question_is_not_independent_even_without_long_name_in_draft(self):
        data = faq({"@type": "Answer", "text": "在账单页申请。"})
        data["mainEntity"][0]["name"] = "如何退款？"
        report = validate(data, "自动续费如何退款？→在账单页申请。")
        self.assertFalse(report["local_valid"])
        self.assertEqual(report["content_check"]["matched_faq_pairs"], 0)
        self.assertIn("faq_pair_mismatch", codes(report))

    def test_question_prefix_overlap_and_marked_independent_headings(self):
        data = {"@context": CONTEXT, "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": "退款", "acceptedAnswer": {"@type": "Answer", "text": "联系人工。"}},
            {"@type": "Question", "name": "退款流程", "acceptedAnswer": {"@type": "Answer", "text": "联系人工。"}}]}
        report = validate(data, "退款流程：联系人工。")
        self.assertFalse(report["local_valid"])
        self.assertEqual(report["content_check"]["matched_faq_pairs"], 1)
        data["mainEntity"][0]["acceptedAnswer"]["text"] = "联系支持。"
        report = validate(data, "问：退款→联系支持。 问：退款流程→联系人工。")
        self.assertTrue(report["local_valid"], report["errors"])
        self.assertEqual(report["content_check"]["matched_faq_pairs"], 2)

    def test_html_only_answer_fails_without_visible_snapshot_and_writes_only_report(self):
        for index, text in enumerate(("<p><br></p>", "<p>&nbsp;<!-- no answer --></p>",
                                      '<img src="https://example.org/a.png">',
                                      "<p>&#8203;&#8205;</p>",
                                      "<script>not visible</script><style>body{}</style>")):
            with self.subTest(text=text):
                data = faq({"@type": "Answer", "text": text})
                source = self.write_json("empty-answer.json", data)
                output = self.base / ("empty-answer-" + str(index))
                status, report = self.cli("build", source, "--output-dir", output)
                self.assertEqual(status, 1)
                self.assertIn(("answer_text_empty", "/mainEntity/0/acceptedAnswer/text"),
                              {(e["code"], e["path"]) for e in report["errors"]})
                self.assertEqual({p.name for p in output.iterdir()}, {"校验结果.json"})
                self.assertEqual(report["content_check"]["status"], "not_run")

    def test_real_html_answer_is_preserved_and_matches_its_own_question(self):
        answer = "<p>请联系<b>人工客服</b>。</p>"
        data = faq({"@type": "Answer", "text": answer})
        source = self.write_json("answer.json", data)
        snapshot = self.base / "answer.txt"
        snapshot.write_text("如何导出？ 请联系人工客服。", encoding="utf-8")
        output = self.base / "real-answer"
        status, report = self.cli("build", source, "--visible-text", snapshot, "--output-dir", output)
        self.assertEqual(status, 0, report)
        self.assertEqual(report["content_check"]["matched_faq_pairs"], 1)
        self.assertEqual(load_json(output / "schema.json")["mainEntity"][0]["acceptedAnswer"]["text"], answer)

    def test_quoted_question_in_its_answer_is_not_a_faq_boundary(self):
        for opening, closing in (("‘", "’"), ("“", "”"), ("'", "'"), ('"', '"'), ("「", "」")):
            with self.subTest(quotes=(opening, closing)):
                answer = f"关于{opening}如何退款？{closing}，请联系支持。"
                data = {"@context": CONTEXT, "@type": "FAQPage", "mainEntity": [
                    {"@type": "Question", "name": "如何退款？", "acceptedAnswer": {"@type": "Answer", "text": answer}}]}
                report = validate(data, "如何退款？\n" + answer)
                self.assertTrue(report["local_valid"], report["errors"])
                self.assertEqual(report["content_check"]["matched_faq_pairs"], 1)
                report = validate(data, f"{opening}如何退款？{closing}\n" + answer)
                self.assertTrue(report["local_valid"], report["errors"])
                self.assertEqual(report["content_check"]["matched_faq_pairs"], 1)
                data["mainEntity"].append({"@type": "Question", "name": "如何导出？",
                                           "acceptedAnswer": {"@type": "Answer", "text": "点击导出。"}})
                report = validate(data, "如何退款？\n" + answer + "\n如何导出？\n点击导出。")
                self.assertTrue(report["local_valid"], report["errors"])
                self.assertEqual(report["content_check"]["matched_faq_pairs"], 2)

    def test_quoted_question_does_not_allow_answer_past_next_question(self):
        data = {"@context": CONTEXT, "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": "如何退款？", "acceptedAnswer": {"@type": "Answer", "text": "点击导出。"}},
            {"@type": "Question", "name": "如何导出？", "acceptedAnswer": {"@type": "Answer", "text": "点击导出。"}}]}
        for heading in ("如何导出？", "‘如何导出？’"):
            with self.subTest(heading=heading):
                report = validate(data, f"如何退款？ 关于‘如何退款？’，请联系支持。 {heading} 点击导出。")
                self.assertFalse(report["local_valid"])
                self.assertIn(("faq_pair_mismatch", "/mainEntity/0/acceptedAnswer"),
                              {(e["code"], e["path"]) for e in report["errors"]})
                self.assertEqual(report["content_check"]["matched_faq_pairs"], 1)

    def test_repeated_question_does_not_allow_crossing_its_next_occurrence(self):
        data = faq({"@type": "Answer", "text": "没有公开。"})
        data["mainEntity"].append({"@type": "Question", "name": "如何导出？",
                                   "acceptedAnswer": {"@type": "Answer", "text": "点击导出。"}})
        report = validate(data, "如何导出？ 点击导出。 如何导出？ 没有公开。")
        # Both pairs have an actual occurrence and are matchable without crossing a question.
        self.assertTrue(report["local_valid"])
        data["mainEntity"][0]["acceptedAnswer"]["text"] = "点击导出。 如何导出？ 没有公开。"
        self.assertIn("faq_pair_mismatch", codes(validate(data, "如何导出？ 点击导出。 如何导出？ 没有公开。")))

    def test_content_absent_empty_and_not_run_are_distinct(self):
        self.assertEqual(validate(organization())["content_check"]["status"], "not_run")
        self.assertIn("visible_text_empty", codes(validate(organization(), " ")))
        self.assertIn("content_not_found", codes(validate(organization(), "其他正文")))

    def test_html_embedding_cannot_break_out_of_script(self):
        data = organization(description='</ScRiPt><script>alert("x")</script> & <tag>\u2028')
        html = embed(data)
        self.assertEqual(html.lower().count("</script>"), 1)
        self.assertEqual(html.lower().count("<script"), 1)
        self.assertEqual(json.loads(html.split(">", 1)[1].rsplit("</script>", 1)[0]), data)

    def test_bad_json_duplicates_and_nonfinite_values_fail_cleanly(self):
        for text in ('{"broken":', '{"@type":"Organization","@type":"Product"}',
                     '{"number":NaN}', '{"number":1e999}'):
            with self.subTest(text=text):
                source = self.base / "bad.json"
                source.write_text(text, encoding="utf-8")
                status, report = self.cli("check", source)
                self.assertEqual(status, 1)
                self.assertIn("input_error", codes(report))

    def test_existing_output_and_input_report_collision_are_preserved(self):
        source = self.write_json("input.json", organization())
        target = self.base / "existing"
        target.mkdir()
        sentinel = target / "schema.json"
        sentinel.write_text("retain", encoding="utf-8")
        self.assertEqual(self.cli("build", source, "--output-dir", target)[0], 2)
        self.assertEqual(sentinel.read_text(encoding="utf-8"), "retain")
        original = source.read_bytes()
        self.assertEqual(self.cli("check", source, "--report", source)[0], 2)
        self.assertEqual(source.read_bytes(), original)

    def test_missing_input_is_an_input_error_and_saved_report(self):
        target = self.base / "out"
        status, report = self.cli("build", self.base / "missing.json", "--output-dir", target)
        self.assertEqual(status, 1)
        self.assertIn("input_error", codes(report))
        self.assertEqual(load_json(target / "校验结果.json"), report)

    def test_mixed_batch_keeps_success_and_failure_separate(self):
        sources = self.base / "sources"
        sources.mkdir()
        (sources / "good.json").write_text(json.dumps(organization()), encoding="utf-8")
        (sources / "good.txt").write_text("演示资料", encoding="utf-8")
        (sources / "bad.json").write_text(json.dumps(faq()), encoding="utf-8")
        status, report = self.cli("batch", sources, "--output-dir", self.base / "batch")
        self.assertEqual(status, 1)
        self.assertEqual((report["total"], report["passed"], report["failed"]), (2, 1, 1))
        self.assertTrue((self.base / "batch/good/schema.json").is_file())
        self.assertFalse((self.base / "batch/bad/schema.json").exists())
        self.assertEqual(load_json(self.base / "batch/good/校验结果.json")["content_check"]["status"], "matched")
        self.assertEqual(load_json(self.base / "batch/bad/校验结果.json")["content_check"]["status"], "not_run")

    def test_empty_batch_is_a_usage_error(self):
        status, report = self.cli("batch", self.base, "--output-dir", self.base / "out")
        self.assertEqual(status, 2)
        self.assertIn("input_error", codes(report))

    def test_html_parser_unsupported_declarations_return_structured_errors(self):
        source = self.write_json("unsupported-html.json", faq({"@type": "Answer", "text": "请填写 <![订单号]> 后联系客服。"}))
        for exception in (NotImplementedError("unsupported declaration"), AssertionError("unknown status keyword")):
            with self.subTest(exception=type(exception).__name__):
                with patch("schema_tool.PlainText.feed", side_effect=exception):
                    data, report = read_and_check(source)
                self.assertIsNone(data)
                self.assertFalse(report["local_valid"])
                self.assertIn("input_error", codes(report))
                self.assertIn("Cannot parse HTML text", report["errors"][0]["message"])

    def test_native_html_declaration_failure_does_not_abort_batch(self):
        from html.parser import HTMLParser
        answer = "请填写 <![订单号]> 后联系客服。"
        try:
            probe = HTMLParser()
            probe.feed(answer)
            probe.close()
            native_failure = False
        except (AssertionError, NotImplementedError):
            native_failure = True
        sources = self.base / "batch-input"
        sources.mkdir()
        self.write_json("batch-input/unsupported.json", faq({"@type": "Answer", "text": answer}))
        self.write_json("batch-input/good.json", organization())
        output = self.base / "batch-output"
        status, summary = self.cli("batch", sources, "--output-dir", output)
        self.assertEqual(status, 1 if native_failure else 0)
        self.assertEqual(summary["total"], 2)
        self.assertTrue((output / "good/schema.json").is_file())
        report = load_json(output / "unsupported/校验结果.json")
        self.assertEqual(report["local_valid"], not native_failure)
        self.assertEqual((output / "unsupported/schema.json").is_file(), not native_failure)
        if native_failure:
            self.assertIn("input_error", codes(report))

    def test_unknown_type_is_partial_coverage_instead_of_certification(self):
        report = validate({"@context": CONTEXT, "@type": "Course", "name": "演示课程"})
        self.assertTrue(report["local_valid"])
        self.assertIn("type_not_covered", {w["code"] for w in report["warnings"]})
        self.assertEqual(report["google_rich_results"]["status"], "not_run")


if __name__ == "__main__":
    unittest.main(verbosity=2)
