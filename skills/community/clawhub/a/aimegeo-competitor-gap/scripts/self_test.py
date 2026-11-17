#!/usr/bin/env python3
"""Offline business regressions, including a loopback-only HTTP acquisition test."""

import copy
import csv
import importlib.util
import json
import subprocess
import sys
import tempfile
import threading
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("comparison", ROOT / "scripts/compare_pages.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


class BusinessTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads((ROOT / "examples/comparison.json").read_text(encoding="utf-8"))

    def report(self, data=None):
        return mod.build_report(data or self.data, mod.Loader(ROOT / "examples"))

    def test_supplied_page_gaps_and_no_ai_ranking(self):
        result = self.report()
        pages = [s["pages"][0]["signals"]["metrics"] for s in result["sites"]]
        self.assertEqual([p["faq_visible_pairs"] for p in pages], [0, 2, 1])
        self.assertEqual([p["explicit_source_links"] for p in pages], [0, 2, 1])
        self.assertEqual([p["brand_entity_field_count"] for p in pages], [2, 4, 3])
        self.assertEqual(result["comparisons"][0]["competitor_minus_brand"]["faq_visible_pairs"], 2)
        self.assertEqual(result["comparisons"][0]["kind"], "simulated")
        self.assertEqual(result["ai_observations"]["observed_answer_denominator"], 0)
        self.assertIsNone(result["ai_observations"]["native_citation_total"])
        self.assertNotIn("ranking", result["ai_observations"])
        self.assertNotIn("score", result["sites"][0])

    def test_nested_schema_and_invalid_json(self):
        html = '''<h1>Test</h1><script data-x="1" TYPE='application/ld+json'>
        [{"@context":"https://schema.org","@graph":[{"@type":["WebPage","FAQPage"],
        "publisher":{"@type":"Organization","name":"青禾","description":"工具"}}]}]</script>
        <script type="application/ld+json">{bad}</script>'''
        parsed = mod.extract_page(html, "https://qinghe.example/p", self.data["sites"][0])
        self.assertEqual(parsed["metrics"]["schema_types"], ["FAQPage", "Organization", "WebPage"])
        self.assertEqual(parsed["metrics"]["brand_organizations"], 1)
        self.assertEqual(parsed["metrics"]["jsonld_invalid_blocks"], 1)

    def test_foreign_entity_context_and_keyword_do_not_count(self):
        html = '''<h1>FAQ</h1><p>Frequently asked questions</p>
        <script type="application/ld+json">{"@context":"https://other.example", "@type":"Organization","name":"青禾"}</script>
        <script type="application/ld+json">{"@context":"https://schema.org","@type":"Organization","name":"别家"}</script>
        <a href="https://social.example/a">社交账号</a>'''
        parsed = mod.extract_page(html, "https://qinghe.example/p", self.data["sites"][0])
        self.assertEqual(parsed["metrics"]["faq_visible_pairs"], 0)
        self.assertEqual(parsed["metrics"]["brand_organizations"], 0)
        self.assertEqual(parsed["metrics"]["external_link_candidates"], 1)
        self.assertEqual(parsed["metrics"]["explicit_source_links"], 0)

    def test_schema_context_inherits_language_but_respects_vocab_order_and_reset(self):
        publisher = {"@context": {"@language": "zh-CN"}, "@type": "Organization", "name": "青禾"}
        parent = {"@context": "https://schema.org", "@type": "WebPage", "publisher": publisher}
        bodies = [
            (parent, 1),
            ({"@context": [{"@vocab": "https://schema.org/"}, {"@vocab": "https://other.example/"}],
              "@type": "Organization", "name": "青禾"}, 0),
            ({"@context": [{"@vocab": "https://other.example/"}, {"@vocab": "https://schema.org/"}],
              "@type": "Organization", "name": "青禾"}, 1),
            ({**parent, "publisher": {**publisher, "@context": None}}, 0),
            ({**parent, "publisher": {**publisher, "@context": {"@vocab": None}}}, 0),
            ({**parent, "publisher": {**publisher, "@context": [{"@language": "zh-CN"}]}}, 1),
        ]
        for body, expected in bodies:
            with self.subTest(body=body):
                html = '<h1>Product</h1><script type="application/ld+json">' + json.dumps(body) + '</script>'
                parsed = mod.extract_page(html, "https://qinghe.example/p", self.data["sites"][0])
                self.assertEqual(parsed["metrics"]["brand_organizations"], expected)
                self.assertEqual("Organization" in parsed["metrics"]["schema_types"], bool(expected))

    def test_hidden_faq_is_excluded(self):
        html = '<h1>产品</h1><div hidden><h2>能用吗？</h2><p>可以</p></div><details><summary>未回答？</summary></details>'
        self.assertEqual(mod.extract_page(html, "https://a.example/", self.data["sites"][0])["metrics"]["faq_visible_pairs"], 0)

    def test_hidden_headings_do_not_end_visible_faq_and_source_contexts(self):
        hidden_headings = [
            '<h2 hidden>隐藏导航</h2>',
            '<h2 aria-hidden="true">隐藏导航</h2>',
            '<h2 style="display:none">隐藏导航</h2>',
            '<div hidden><h2>隐藏导航</h2></div>',
            '<template><h2>隐藏导航</h2></template>',
        ]
        for hidden in hidden_headings:
            with self.subTest(hidden=hidden):
                body = ('<section><h2>常见问题</h2>' + hidden
                        + '<h3>导入方式</h3><div><p>上传CSV。</p></div></section>'
                        + '<section><h2>参考资料</h2>' + hidden
                        + '<a href="https://sources.example/manual">资料</a></section>')
                parsed = mod.extract_page(body, 'https://a.example/', self.data['sites'][0])
                self.assertEqual(parsed['faq_evidence'], [{'question': '导入方式', 'answer': '上传CSV。'}])
                self.assertEqual(parsed['metrics']['explicit_source_links'], 1)

    def test_faq_answers_stay_in_the_question_structural_region(self):
        unrelated = [
            '<section><h2>如何导入？</h2></section><footer><p>版权所有，联系我们。</p></footer>',
            '<section><h2>如何导入？</h2></section><section><p>另一个区域的介绍。</p></section>',
            '<main><h2>如何导入？</h2></main><aside><p>侧栏信息。</p></aside>',
            '<section><h2>如何导入？</h2></section><p>区域外的介绍。</p>',
            '<h2>如何导入？</h2><footer><p>版权所有，联系我们。</p></footer>',
        ]
        for body in unrelated:
            with self.subTest(body=body):
                self.assertEqual(mod.extract_page(body, 'https://a.example/', self.data['sites'][0])['faq_evidence'], [])
        for body in ('<h2>如何导入？</h2><div><p>上传CSV。</p></div>',
                     '<section><h2>如何导入？</h2><div><p>上传CSV。</p></div></section>'):
            with self.subTest(body=body):
                self.assertEqual(mod.extract_page(body, 'https://a.example/', self.data['sites'][0])['faq_evidence'],
                                 [{'question': '如何导入？', 'answer': '上传CSV。'}])

    def test_heading_contexts_end_with_plain_div_and_keep_inner_wrappers(self):
        for tag in ('section', 'div'):
            with self.subTest(tag=tag):
                body = ('<html><body><' + tag + '><h2>References</h2>'
                        + '<div><a href="https://sources.example/manual">资料</a></div></' + tag + '>'
                        + '<a href="https://products.example/related">相关产品</a>'
                        + '<' + tag + '><h2>常见问题</h2><div><details><summary>导入方式</summary>'
                        + '<p>上传CSV。</p></details></div></' + tag + '>'
                        + '<details><summary>产品参数</summary><p>重量100克</p></details></body></html>')
                parsed = mod.extract_page(body, 'https://a.example/', self.data['sites'][0])
                self.assertEqual(parsed['faq_evidence'], [{'question': '导入方式', 'answer': '上传CSV。'}])
                self.assertEqual(parsed['metrics']['explicit_source_links'], 1)
                self.assertEqual([link['explicit_source'] for link in parsed['external_links']], [True, False])
                body = '<div><h2>常见问题</h2><div><h3>导入方式</h3><div><p>上传CSV。</p></div></div></div>'
                self.assertEqual(mod.extract_page(body, 'https://a.example/', self.data['sites'][0])['faq_evidence'],
                                 [{'question': '导入方式', 'answer': '上传CSV。'}])

    def test_question_container_must_remain_an_answer_ancestor(self):
        for tag in ('div', 'section'):
            with self.subTest(tag=tag):
                body = ('<main><' + tag + ' class="questions"><h2>如何导入？</h2></' + tag + '>'
                        + '<' + tag + ' class="promotion"><p>本周新品促销，欢迎订阅。</p></' + tag + '></main>')
                self.assertEqual(mod.extract_page(body, 'https://a.example/', self.data['sites'][0])['faq_evidence'], [])
        for body in ('<section><h2>如何导入？</h2><div><div><p>上传CSV。</p></div></div></section>',
                     '<main><div><h2>如何导入？</h2><div><p>上传CSV。</p></div></div></main>'):
            with self.subTest(body=body):
                self.assertEqual(mod.extract_page(body, 'https://a.example/', self.data['sites'][0])['faq_evidence'],
                                 [{'question': '如何导入？', 'answer': '上传CSV。'}])

    def test_details_specs_and_real_faq_match_equivalent_heading_markup(self):
        fragments = [
            '<h2>产品参数</h2><p>重量100克</p><h2>如何导入？</h2><p>上传CSV。</p>',
            '<details><summary>产品参数</summary><p>重量100克</p></details>'
            '<details><summary>如何导入？</summary><p>上传CSV。</p></details>',
        ]
        for body in fragments:
            with self.subTest(body=body):
                parsed = mod.extract_page(body, 'https://a.example/product', self.data['sites'][0])
                self.assertEqual(parsed['metrics']['faq_visible_pairs'], 1)
                self.assertEqual(parsed['faq_evidence'], [{'question': '如何导入？', 'answer': '上传CSV。'}])

    def test_details_answer_headings_do_not_duplicate_the_summary_question(self):
        answers = ['<p>上传 CSV。</p>', '<h3>导入步骤</h3><p>上传 CSV。</p>',
                   '<section><h3>导入步骤</h3><div><p>上传 CSV。</p></div></section>',
                   '<h3>上传完成了吗？</h3><p>上传 CSV。</p>']
        for marker in ('', ' id="faq"'):
            for answer in answers:
                with self.subTest(marker=marker, answer=answer):
                    body = '<section' + marker + '><details><summary>如何导入？</summary>' + answer + '</details></section>'
                    parsed = mod.extract_page(body, 'https://a.example/', self.data['sites'][0])
                    self.assertEqual(parsed['metrics']['faq_visible_pairs'], 1)
                    self.assertEqual(parsed['faq_evidence'][0]['question'], '如何导入？')
                    self.assertIn('上传 CSV。', parsed['faq_evidence'][0]['answer'])
        # A non-question disclosure without a summary pair can contain a real Q/A.
        body = '<details><summary>说明</summary><h3>如何导入？</h3><p>上传 CSV。</p></details>'
        self.assertEqual(mod.extract_page(body, 'https://a.example/', self.data['sites'][0])['faq_evidence'],
                         [{'question': '如何导入？', 'answer': '上传 CSV。'}])

    def test_explicit_faq_context_without_question_mark_and_missing_answers(self):
        fragments = [
            '<section id="faq"><h3>导入方式</h3><p>上传CSV。</p></section>',
            '<section class="faq"><details><summary>导入方式</summary><p>上传CSV。</p></details></section>',
            '<section><h2>常见问题</h2><h3>导入方式</h3><p>上传CSV。</p></section>',
            '<section><h2>Frequently asked questions</h2><details><summary>导入方式</summary><p>上传CSV。</p></details></section>',
        ]
        for body in fragments:
            with self.subTest(body=body):
                parsed = mod.extract_page(body, 'https://a.example/product', self.data['sites'][0])
                self.assertEqual(parsed['faq_evidence'], [{'question': '导入方式', 'answer': '上传CSV。'}])
        body = '<h2>常见问题</h2><details><summary>未回答</summary></details><h2>产品参数</h2><details><summary>重量</summary><p>100克</p></details>'
        self.assertEqual(mod.extract_page(body, 'https://a.example/', self.data['sites'][0])['faq_evidence'], [])

    def test_visible_source_headings_equal_source_id_without_counting_related_products(self):
        link = '<ul><li><a href="https://www.rfc-editor.org/rfc/rfc9309.html">RFC</a></li></ul>'
        for heading in ('参考资料', '来源', 'References', 'Sources'):
            for marker in ('', ' id="references"'):
                with self.subTest(heading=heading, marker=marker):
                    body = f'<section{marker}><h2><span>{heading}</span></h2>{link}</section>'
                    body += '<a href="https://products.example/other">相关产品</a>'
                    parsed = mod.extract_page(body, 'https://a.example/', self.data['sites'][0])
                    self.assertEqual(parsed['metrics']['explicit_source_links'], 1)
                    self.assertEqual(parsed['metrics']['external_link_candidates'], 2)
                    self.assertEqual([link['explicit_source'] for link in parsed['external_links']], [True, False])
        body = '<h2>References</h2>' + link + '<h2>Related products</h2><a href="https://products.example/other">产品</a>'
        parsed = mod.extract_page(body, 'https://a.example/', self.data['sites'][0])
        self.assertEqual(parsed['metrics']['explicit_source_links'], 1)
        self.assertEqual([link['explicit_source'] for link in parsed['external_links']], [True, False])
        for body in ('<h2 hidden>参考资料</h2>' + link, '<h2>相关产品</h2>' + link):
            self.assertEqual(mod.extract_page(body, 'https://a.example/', self.data['sites'][0])['metrics']['explicit_source_links'], 0)

    def test_identical_business_content_markup_does_not_manufacture_comparison_gaps(self):
        with tempfile.TemporaryDirectory() as tmp:
            data = copy.deepcopy(self.data)
            data['sites'] = data['sites'][:2]
            ref = '<h2>参考资料</h2><a href="https://www.rfc-editor.org/rfc/rfc9309.html">RFC</a>'
            bodies = ['<h2>产品参数</h2><p>重量100克</p><h2>如何导入？</h2><p>上传CSV。</p><section>' + ref + '</section>',
                '<details><summary>产品参数</summary><p>重量100克</p></details>'
                '<details><summary>如何导入？</summary><p>上传CSV。</p></details><section id="references">' + ref + '</section>']
            for i, (site, body) in enumerate(zip(data['sites'], bodies)):
                site.pop('robots', None)
                (Path(tmp) / f'page-{i}.html').write_text(body, encoding='utf-8')
                site['pages'][0]['snapshot']['path'] = f'page-{i}.html'
            report = mod.build_report(data, mod.Loader(tmp))
            gap = report['comparisons'][0]['competitor_minus_brand']
            self.assertEqual(gap['faq_visible_pairs'], 0)
            self.assertEqual(gap['explicit_source_links'], 0)

    def test_hidden_descendant_text_stays_out_of_visible_ancestors(self):
        hidden_answers = [
            '<p hidden>隐藏答案</p>',
            '<p aria-hidden="true"><span>隐藏答案</span></p>',
            '<p style="display: none">隐藏答案</p>',
            '<p style="visibility: hidden">隐藏答案</p>',
            '<template><p>隐藏答案</p></template>',
            '<script>隐藏答案</script><style>隐藏答案</style>',
        ]
        for answer in hidden_answers:
            with self.subTest(answer=answer):
                html = '<details><summary>问题？</summary>' + answer + '</details>'
                parsed = mod.extract_page(html, "https://a.example/", self.data["sites"][0])
                self.assertEqual(parsed["faq_evidence"], [])
                self.assertEqual(parsed["metrics"]["faq_visible_pairs"], 0)
                self.assertEqual(parsed["visible_blocks"], [
                    {"tag": "summary", "text": "问题？"}, {"tag": "details", "text": "问题？"}])
        html = '''<details><summary>问题？</summary><p>可见<span hidden>隐藏答案</span>回答</p>
        <script type="application/ld+json">{"@context":"https://schema.org","@type":"FAQPage"}</script></details>
        <p>青禾<span hidden>隐藏答案</span>介绍</p>
        <a href="https://source.example/">资料<span hidden>隐藏答案</span></a>'''
        parsed = mod.extract_page(html, "https://a.example/", self.data["sites"][0])
        self.assertEqual(parsed["faq_evidence"], [{"question": "问题？", "answer": "可见回答"}])
        self.assertEqual(parsed["first_paragraph"], "可见回答")
        self.assertEqual(parsed["external_links"][0]["text"], "资料")
        self.assertEqual(parsed["metrics"]["schema_types"], ["FAQPage"])
        html = '<p>可见<template><h2>隐藏问题？</h2><p>隐藏答案</p></template>回答</p>'
        parsed = mod.extract_page(html, "https://a.example/", self.data["sites"][0])
        self.assertEqual(parsed["visible_blocks"], [{"tag": "p", "text": "可见回答"}])
        self.assertEqual(parsed["metrics"]["faq_visible_pairs"], 0)

    def test_optional_paragraph_ends_match_explicit_answers(self):
        explicit = '<h2>如何导入？</h2><p>上传 <strong>CSV</strong>。</p><h2>失败怎么办？</h2><p>修正后重试。</p>'
        omitted = '<h2>如何导入？</h2><p>上传 <strong>CSV</strong>。<h2>失败怎么办？</h2><p>修正后重试。'
        expected = mod.extract_page(explicit, "https://a.example/", self.data["sites"][0])
        for html in (omitted, '<div>' + omitted + '</div>', '<html><body>' + omitted):
            with self.subTest(html=html):
                parsed = mod.extract_page(html, "https://a.example/", self.data["sites"][0])
                self.assertEqual(parsed["faq_evidence"], [
                    {"question": "如何导入？", "answer": "上传 CSV。"},
                    {"question": "失败怎么办？", "answer": "修正后重试。"}])
                self.assertEqual(parsed["visible_blocks"], expected["visible_blocks"])
                self.assertEqual(parsed["metrics"], expected["metrics"])
        parser = mod.PageHTML()
        parser.feed('<p>首段<p>次段')
        parser.close()
        parser.close()
        self.assertEqual(parser.blocks, [{"tag": "p", "text": "首段"}, {"tag": "p", "text": "次段"}])
        self.assertEqual(parser.stack, [])

    def test_optional_paragraphs_and_hidden_answers_do_not_create_gaps(self):
        with tempfile.TemporaryDirectory() as tmp:
            pages = [
                '<h2>一问？</h2><p>一答</p><h2>二问？</h2><p>二答</p>',
                '<h2>一问？</h2><p>一答<h2>二问？</h2><p>二答',
                '<details><summary>问题？</summary><p hidden>隐藏答案</p></details>',
            ]
            for index, (site, html) in enumerate(zip(self.data["sites"], pages)):
                site.pop("robots", None)
                name = f"page-{index}.html"
                (Path(tmp) / name).write_text(html, encoding="utf-8")
                site["pages"][0]["snapshot"]["path"] = name
            result = mod.build_report(self.data, mod.Loader(tmp))
        self.assertEqual([s["pages"][0]["analysis_status"] for s in result["sites"]], ["observed"] * 3)
        self.assertEqual([s["pages"][0]["signals"]["metrics"]["faq_visible_pairs"] for s in result["sites"]], [2, 2, 0])
        self.assertEqual([c["competitor_minus_brand"]["faq_visible_pairs"] for c in result["comparisons"]], [0, -2])

    def test_malformed_attributes_links_and_foreign_types(self):
        html = '''<h1 class>产品</h1><p style aria-hidden>可读段落</p><script type>noop</script>
        <script type="application/ld+json">{"@context":"https://schema.org","@type":42}</script>
        <script type="application/ld+json">{"@context":"https://schema.org","@type":"https://other.example/Organization","name":"青禾"}</script>
        <a href="http://[broken">坏链接</a><a href>空链接</a>'''
        parsed = mod.extract_page(html, "https://qinghe.example/p", self.data["sites"][0])
        self.assertEqual(parsed["first_paragraph"], "可读段落")
        self.assertEqual(parsed["metrics"]["schema_types"], [])
        self.assertEqual(parsed["metrics"]["brand_organizations"], 0)
        self.assertEqual(parsed["external_links"], [])

    def test_html_robots_response_does_not_imply_allowed(self):
        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / "page.html").write_text("<h1>Product</h1><p>Body</p>")
            data = copy.deepcopy(self.data)
            for site in data["sites"]:
                site["pages"][0]["snapshot"]["path"] = "page.html"
                if "robots" in site:
                    site["robots"]["snapshot"]["path"] = "page.html"
            result = mod.build_report(data, mod.Loader(tmp))
            self.assertTrue(all(p["robots"]["GPTBot"]["state"] == "unverified" for site in result["sites"] for p in site["pages"]))

    def test_robots_specific_groups_path_and_allow_tie(self):
        body = 'User-agent: *\nDisallow: /\nUser-agent: GPTBot\nDisallow: /private/\nAllow: /private/open$\n'
        check = lambda path: mod.robots_decision(body, "GPTBot", "https://a.example" + path)["state"]
        self.assertEqual(check("/products/a"), "allowed")
        self.assertEqual(check("/private/a"), "blocked")
        self.assertEqual(check("/private/open"), "allowed")
        self.assertEqual(check("/private/open?x=1"), "blocked")
        self.assertEqual(mod.robots_decision(body, "ClaudeBot", "https://a.example/")["state"], "blocked")
        tie = 'User-agent: GPTBot\nDisallow: /p\nAllow: /p\n'
        self.assertEqual(mod.robots_decision(tie, "GPTBot", "https://a.example/p")["state"], "allowed")

    def test_robots_merge_wildcards_empty_and_octets(self):
        body = 'User-agent: GPTBot\nDisallow: /*.pdf$\nUser-agent: GPTBot\nDisallow: /caf%C3%A9\nAllow: /~public\nDisallow:\n'
        self.assertEqual(mod.robots_decision(body, "GPTBot", "https://a.example/x.pdf")["state"], "blocked")
        self.assertEqual(mod.robots_decision(body, "GPTBot", "https://a.example/café")["state"], "blocked")
        self.assertEqual(mod.robots_decision(body, "GPTBot", "https://a.example/%7Epublic")["state"], "allowed")
        encoded = 'User-agent: *\nDisallow: /a%2Fb\n'
        self.assertEqual(mod.robots_decision(encoded, "GPTBot", "https://a.example/a/b")["state"], "allowed")
        self.assertEqual(mod.robots_decision(encoded, "GPTBot", "https://a.example/a%2fb")["state"], "blocked")

    def test_robots_all_google_rule_precedence_examples(self):
        # Primary reference: Google's robots-txt-spec rule-precedence table.
        cases = [
            ('/page', '/p', '/', 'allowed', 'allow: /p'),
            ('/folder/page', '/folder', '/folder', 'allowed', 'allow: /folder'),
            ('/page.htm', '/page', '/*.htm', 'blocked', 'disallow: /*.htm'),
            ('/page.php5', '/page', '/*.ph', 'allowed', 'allow: /page'),
            ('/', '/$', '/', 'allowed', 'allow: /$'),
            ('/page.htm', '/$', '/', 'blocked', 'disallow: /'),
        ]
        for path, allow, disallow, state, winner in cases:
            for reverse in (False, True):
                with self.subTest(path=path, allow=allow, disallow=disallow, reverse=reverse):
                    rules = [f'Allow: {allow}', f'Disallow: {disallow}']
                    if reverse:
                        rules.reverse()
                    body = 'User-agent: *\n' + '\n'.join(rules) + '\n'
                    decision = mod.robots_decision(body, 'GPTBot', 'https://example.com' + path)
                    self.assertEqual(decision['state'], state)
                    self.assertEqual(decision['rule'], winner)

    def test_robots_anchor_and_percent_normalization_keep_full_rule_length(self):
        cases = [
            ('/', '/', '/$', 'blocked', 'disallow: /$'),
            ('/page', '/page', '/page$', 'blocked', 'disallow: /page$'),
            ('/%7Epublic', '/%7Epublic', '/~public', 'allowed', 'allow: /%7Epublic'),
            ('/café', '/café', '/caf%C3%A9', 'allowed', 'allow: /café'),
            ('/caf%C3%A9', '/caf***', '/café', 'blocked', 'disallow: /café'),
            ('/x%2A', '/x', '/x%2A$', 'blocked', 'disallow: /x%2A$'),
            ('/x%24suffix', '/x', '/x%24', 'blocked', 'disallow: /x%24'),
        ]
        for path, allow, disallow, state, winner in cases:
            with self.subTest(path=path, allow=allow, disallow=disallow):
                body = f'User-agent: *\nAllow: {allow}\nDisallow: {disallow}\n'
                decision = mod.robots_decision(body, 'GPTBot', 'https://example.com' + path)
                self.assertEqual(decision['state'], state)
                self.assertEqual(decision['rule'], winner)

    def test_cli_robot_precedence_blocks_html_and_keeps_equal_length_allow(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'page.html').write_text('<h1>合成产品页</h1><p>明确提供的页面内容。</p>', encoding='utf-8')
            (root / 'robots.txt').write_text('User-agent: *\nAllow: /page\nDisallow: /*.htm\nDisallow: /*.ph\n', encoding='utf-8')
            def snapshot(file):
                return {'path': file, 'status': 'ok', 'http_status': 200, 'kind': 'simulated',
                        'captured_at': '2026-10-19T15:00:00+08:00'}
            sites = []
            for name, role, path in [('brand', 'brand', '/page.htm'), ('other', 'competitor', '/page.php5')]:
                origin = f'https://{name}.example'
                sites.append({'id': name, 'name': name, 'role': role,
                    'pages': [{'slot': 'product', 'url': origin + path, 'snapshot': snapshot('page.html')}],
                    'robots': {'url': origin + '/robots.txt', 'snapshot': snapshot('robots.txt')}})
            source = root / 'input.json'
            source.write_text(json.dumps({'comparison': {'question': '合成产品页的抓取规则比较',
                'page_slots': ['product']}, 'sites': sites, 'ai_samples': []}), encoding='utf-8')
            result = subprocess.run([sys.executable, str(ROOT / 'scripts/compare_pages.py'),
                '--input', str(source), '--out', str(root / 'out')], capture_output=True, text=True, timeout=15)
            self.assertEqual(result.returncode, 0, result.stderr)
            report = json.loads((root / 'out/evidence.json').read_text())
            self.assertEqual(report['cache']['network_requests'], 0)
            for bot in mod.CRAWLERS:
                self.assertEqual(report['sites'][0]['pages'][0]['robots'][bot]['state'], 'blocked')
                self.assertEqual(report['sites'][1]['pages'][0]['robots'][bot]['state'], 'allowed')
            with (root / 'out/竞品差距矩阵.csv').open(encoding='utf-8-sig', newline='') as handle:
                rows = list(csv.reader(handle))
            row = next(row for row in rows if row[2] == 'robots:GPTBot')
            self.assertEqual((row[3], row[5]), ('[模拟] blocked', '[模拟] allowed'))
            self.assertEqual(json.loads(row[4])['decision']['rule'], 'disallow: /*.htm')

    def test_failed_page_is_not_zero_or_advantage(self):
        data = json.loads((ROOT / "examples/failure-input.json").read_text(encoding="utf-8"))
        result = self.report(data)
        failed = result["sites"][1]["pages"][0]
        self.assertEqual(failed["analysis_status"], "unverified")
        self.assertIsNone(failed["signals"])
        self.assertEqual(result["comparisons"][0]["status"], "unverified")
        self.assertIsNone(result["comparisons"][0]["competitor_minus_brand"])
        ai = result["ai_observations"]
        self.assertEqual([s["status"] for s in ai["samples"]], ["query_failed", "not_run", "simulated"])
        self.assertIsNone(ai["samples"][0]["native_citation_count"])
        self.assertIsNone(ai["samples"][2]["native_citation_count"])
        self.assertIsNone(ai["native_citation_total"])
        self.assertEqual(ai["native_citation_denominator"], 0)

    def test_missing_slot_or_snapshot_is_unverified(self):
        self.data["sites"][1]["pages"] = []
        del self.data["sites"][2]["pages"][0]["snapshot"]
        result = self.report()
        self.assertTrue(all(c["status"] == "unverified" for c in result["comparisons"]))
        self.assertEqual(result["cache"]["network_requests"], 0)

    def test_repeated_url_and_local_path_are_cached(self):
        self.data["comparison"]["page_slots"].append("same-page-review")
        for site in self.data["sites"]:
            duplicate = copy.deepcopy(site["pages"][0])
            duplicate["slot"] = "same-page-review"
            site["pages"].append(duplicate)
        result = self.report()
        self.assertEqual(result["cache"], {"unique_urls": 5, "cache_hits": 3, "unique_snapshot_reads": 4, "network_requests": 0})

    def test_conflicting_same_url_records_rejected(self):
        self.data["comparison"]["page_slots"].append("duplicate")
        duplicate = copy.deepcopy(self.data["sites"][0]["pages"][0])
        duplicate["slot"] = "duplicate"
        duplicate["snapshot"]["captured_at"] = "2026-10-19T13:00:00+08:00"
        self.data["sites"][0]["pages"].append(duplicate)
        with self.assertRaises(mod.InputError):
            self.report()

    def test_missing_file_and_js_shell_are_unverified(self):
        self.data["sites"][1]["pages"][0]["snapshot"]["path"] = "pages/missing.html"
        self.assertIsNone(self.report()["comparisons"][0]["competitor_minus_brand"])
        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / "shell.html").write_text('<html><body><div id="app"></div><script>app()</script></body></html>')
            data = copy.deepcopy(self.data)
            for site in data["sites"]:
                site.pop("robots", None)
                site["pages"][0]["snapshot"]["path"] = "shell.html"
            result = mod.build_report(data, mod.Loader(tmp))
            self.assertTrue(all(c["status"] == "unverified" for c in result["comparisons"]))

    def test_origin_mismatch_and_missing_robots_are_unknown(self):
        self.data["sites"][0]["pages"][0]["snapshot"]["final_url"] = "https://other.example/product"
        result = self.report()
        self.assertEqual(result["sites"][0]["pages"][0]["robots"]["GPTBot"]["state"], "unverified")
        self.assertEqual(result["sites"][2]["pages"][0]["robots"]["GPTBot"]["state"], "unverified")

    def test_simulated_and_observed_pages_do_not_form_a_gap(self):
        self.data["sites"][0]["pages"][0]["snapshot"]["kind"] = "observed"
        self.assertTrue(all(c["competitor_minus_brand"] is None for c in self.report()["comparisons"]))

    def test_ai_denominators_native_sources_and_literal_mentions(self):
        base = {"id": "actual-input", "status": "observed", "platform": "controlled-test", "query": "客户工具？",
                "captured_at": "2026-10-19T12:00:00+08:00", "answer": "青禾提供客户管理，参考 https://plain.example/。",
                "evidence": "controlled-test-record", "native_citations": []}
        missing = dict(base, id="uncollected", native_citations=None)
        simulated = dict(base, id="simulation", status="simulated", native_citations=[{"url": "https://native.example/"}])
        self.data["ai_samples"] = [base, missing, simulated]
        ai = self.report()["ai_observations"]
        self.assertEqual(ai["observed_answer_denominator"], 2)
        self.assertEqual(ai["native_citation_denominator"], 1)
        self.assertEqual(ai["native_citation_total"], 0)
        self.assertTrue(ai["samples"][0]["mentions"]["qinghe"])
        self.assertFalse(ai["samples"][0]["mentions"]["cedar"])
        self.assertEqual(ai["samples"][0]["native_citation_count"], 0)
        self.assertIsNone(ai["samples"][1]["native_citation_count"])

    def test_bad_scope_timestamp_and_failed_citations_rejected(self):
        variants = []
        bad = copy.deepcopy(self.data)
        bad["sites"][1]["pages"][0]["slot"] = "unmatched-scope"
        variants.append(bad)
        bad = copy.deepcopy(self.data)
        bad["sites"][0]["pages"][0]["snapshot"]["captured_at"] = "2026-10-19"
        variants.append(bad)
        bad = copy.deepcopy(self.data)
        bad["ai_samples"] = [{"id": "fail", "status": "query_failed", "platform": "test", "query": "q", "reason": "timeout", "native_citations": []}]
        variants.append(bad)
        for data in variants:
            with self.subTest(data=data):
                with self.assertRaises(mod.InputError):
                    self.report(data)

    def test_snapshot_escape_rejected(self):
        self.data["sites"][0]["pages"][0]["snapshot"]["path"] = "../outside.html"
        with self.assertRaises(mod.InputError):
            self.report()

    def test_invalid_enum_types_are_cli_input_errors(self):
        fields = [
            (("sites", 0, "role"), "Invalid site role"),
            (("sites", 0, "pages", 0, "snapshot", "status"), "Invalid snapshot status"),
            (("sites", 0, "pages", 0, "snapshot", "kind"), "snapshot.kind is required"),
            (("ai_samples", 0, "status"), "Invalid AI sample status"),
        ]
        self.data["ai_samples"] = [{
            "id": "enum-test", "status": "simulated", "platform": "offline-fixture", "query": "问题？",
            "captured_at": "2026-10-19T12:00:00+08:00", "answer": "构造回答", "evidence": "enum-fixture",
            "native_citations": None,
        }]
        with tempfile.TemporaryDirectory() as tmp:
            path, out = Path(tmp) / "bad.json", Path(tmp) / "report"
            for keys, message in fields:
                for value in ([], {}, ["ok"], {"status": "ok"}, None, 0, False, "invalid"):
                    with self.subTest(field=keys, value=value):
                        data = copy.deepcopy(self.data)
                        target = data
                        for key in keys[:-1]:
                            target = target[key]
                        target[keys[-1]] = value
                        with self.assertRaisesRegex(mod.InputError, message):
                            mod.validate(data)
                        path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
                        run = subprocess.run([sys.executable, str(ROOT / "scripts/compare_pages.py"),
                                              "--input", str(path), "--out", str(out)],
                                             cwd=tmp, capture_output=True, text=True, check=False)
                        self.assertEqual(run.returncode, 2, run.stderr)
                        self.assertIn("Input/output error: " + message, run.stderr)
                        self.assertNotIn("Traceback", run.stderr)
                        self.assertEqual(run.stdout, "")
                        self.assertFalse(out.exists())

    def test_truncated_chunked_http_keeps_other_pages_and_cli_report(self):
        requests = []

        class Handler(BaseHTTPRequestHandler):
            def do_GET(self):
                requests.append(self.path)
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Connection", "close")
                if self.path == "/truncated":
                    self.send_header("Transfer-Encoding", "chunked")
                    self.end_headers()
                    # Declare 64 bytes, send only a partial chunk, then disconnect.
                    self.wfile.write(b"40\r\n<h1>Partial</h1>")
                else:
                    self.end_headers()
                    self.wfile.write(b"<h1>Readable</h1><p>Complete body</p>")
                self.close_connection = True

            def log_message(self, *args):
                pass

        server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            url = f"http://127.0.0.1:{server.server_port}"
            with tempfile.TemporaryDirectory() as tmp:
                for site, path in zip(self.data["sites"], ("/brand", "/truncated", "/healthy")):
                    site.pop("robots", None)
                    site["pages"] = [{"slot": "product", "url": url + path}]
                path = Path(tmp) / "input.json"
                path.write_text(json.dumps(self.data, ensure_ascii=False), encoding="utf-8")
                run = subprocess.run([sys.executable, str(ROOT / "scripts/compare_pages.py"),
                                      "--input", str(path), "--out", tmp, "--fetch"],
                                     cwd=tmp, capture_output=True, text=True, check=False)
                self.assertEqual(run.returncode, 0, run.stderr)
                self.assertEqual(json.loads(run.stdout)["pages_unverified"], 1)
                result = json.loads((Path(tmp) / "evidence.json").read_text(encoding="utf-8"))
                failed = result["sites"][1]["pages"][0]
                self.assertEqual(failed["analysis_status"], "unverified")
                self.assertIsNone(failed["signals"])
                self.assertEqual(failed["acquisition"]["reason"], "fetch_failed:IncompleteRead")
                self.assertIsNone(failed["acquisition"]["sha256"])
                self.assertEqual(result["comparisons"][0]["status"], "unverified")
                self.assertIsNone(result["comparisons"][0]["competitor_minus_brand"])
                self.assertEqual(result["comparisons"][1]["status"], "comparable")
                self.assertEqual(result["sites"][2]["pages"][0]["signals"]["first_paragraph"], "Complete body")
                with (Path(tmp) / "竞品差距矩阵.csv").open(encoding="utf-8-sig", newline="") as handle:
                    faq = next(row for row in csv.reader(handle) if row[2] == "faq_visible_pairs")
                self.assertEqual([faq[3], faq[5], faq[7]], ["0", "未验证", "0"])
                self.assertEqual(requests, ["/brand", "/truncated", "/healthy"])
                loader = mod.Loader(tmp, fetch=True)
                first = loader.load({"url": url + "/truncated"})
                self.assertEqual(first, loader.load({"url": url + "/truncated#again"}))
                self.assertEqual(first["status"], "unverified")
                self.assertEqual(first["text"], "")
                self.assertEqual((loader.network_requests, loader.hits), (1, 1))
                self.assertEqual(requests.count("/truncated"), 2)
        finally:
            server.shutdown()
            server.server_close()
            thread.join()

    def test_oversize_http_page_is_unverified_and_healthy_cli_delivery_continues(self):
        requests = []
        class Handler(BaseHTTPRequestHandler):
            def do_GET(self):
                requests.append(self.path)
                raw = b'x' * (mod.LIMIT + 1) if self.path == '/oversize' else b'<h1>Readable</h1><p>Complete body</p>'
                self.send_response(200)
                self.send_header('Content-Type', 'text/html; charset=utf-8')
                self.send_header('Content-Length', str(len(raw)))
                self.end_headers()
                self.wfile.write(raw)
            def log_message(self, *args):
                pass
        server = ThreadingHTTPServer(('127.0.0.1', 0), Handler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            origin = f'http://127.0.0.1:{server.server_port}'
            with tempfile.TemporaryDirectory() as tmp:
                for site, path in zip(self.data['sites'], ('/brand', '/oversize', '/healthy')):
                    site.pop('robots', None)
                    site['pages'] = [{'slot': 'product', 'url': origin + path}]
                source, out = Path(tmp) / 'input.json', Path(tmp) / 'out'
                source.write_text(json.dumps(self.data), encoding='utf-8')
                run = subprocess.run([sys.executable, str(ROOT / 'scripts/compare_pages.py'), '--input', str(source),
                    '--out', str(out), '--fetch'], capture_output=True, text=True, timeout=20)
                self.assertEqual(run.returncode, 0, run.stderr)
                self.assertEqual(run.stderr, '')
                self.assertEqual(json.loads(run.stdout)['pages_unverified'], 1)
                report = json.loads((out / 'evidence.json').read_text())
                large = report['sites'][1]['pages'][0]
                self.assertEqual(large['analysis_status'], 'unverified')
                self.assertIsNone(large['signals'])
                self.assertIsNone(large['acquisition']['sha256'])
                self.assertEqual(large['acquisition']['reason'], 'fetch_failed:response_too_large')
                self.assertIsNone(report['comparisons'][0]['competitor_minus_brand'])
                self.assertEqual(report['comparisons'][1]['status'], 'comparable')
                self.assertEqual(requests, ['/brand', '/oversize', '/healthy'])
                with (out / '竞品差距矩阵.csv').open(encoding='utf-8-sig', newline='') as stream:
                    row = next(row for row in csv.reader(stream) if row[2] == 'faq_visible_pairs')
                self.assertEqual((row[3], row[5], row[7]), ('0', '未验证', '0'))
                loader = mod.Loader(tmp, fetch=True)
                first = loader.load({'url': origin + '/oversize'})
                self.assertEqual(first, loader.load({'url': origin + '/oversize#again'}))
                self.assertEqual((loader.network_requests, loader.hits), (1, 1))
        finally:
            server.shutdown()
            server.server_close()
            thread.join()

    def test_fixed_length_truncation_and_html_robots_from_http(self):
        requests = []
        html_robots = {
            "/comment-robots": "<!-- error --><html><body>Error</body></html>",
            "/bom-robots": "\ufeff<html><body>Error</body></html>",
            "/bom-comment-robots": "\ufeff<!-- error --><html><body>Error</body></html>",
        }

        class Handler(BaseHTTPRequestHandler):
            def do_GET(self):
                requests.append(self.path)
                body = html_robots.get(self.path, "<h1>Product</h1><details><summary>Question?</summary><p>Answer</p></details>")
                if self.path == "/truncated":
                    body = "<h1>Partial</h1>"
                elif self.path == "/valid-robots":
                    body = "# <html> is a comment, not an HTML response\nUser-agent: *\nDisallow: /private/\n"
                elif self.path == "/bom-rules":
                    body = "\ufeffUser-agent: GPTBot\nDisallow: /\n"
                raw = body.encode("utf-8")
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", "999" if self.path == "/truncated" else str(len(raw)))
                self.send_header("Connection", "close")
                self.end_headers()
                self.wfile.write(raw)
                self.close_connection = True

            def log_message(self, *args):
                pass

        server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            url = f"http://127.0.0.1:{server.server_port}"
            with tempfile.TemporaryDirectory() as tmp:
                for site, path in zip(self.data["sites"], ("/brand", "/truncated", "/healthy")):
                    site.pop("robots", None)
                    site["pages"] = [{"slot": "product", "url": url + path}]
                result = mod.build_report(self.data, mod.Loader(tmp, fetch=True))
                failed = result["sites"][1]["pages"][0]
                self.assertEqual(failed["analysis_status"], "unverified")
                self.assertEqual(failed["acquisition"]["reason"], "fetch_failed:IncompleteRead")
                self.assertIsNone(failed["acquisition"]["sha256"])
                self.assertIsNone(failed["signals"])
                self.assertIsNone(result["comparisons"][0]["competitor_minus_brand"])
                self.assertEqual(result["comparisons"][1]["status"], "comparable")
                self.assertEqual(requests, ["/brand", "/truncated", "/healthy"])
                loader = mod.Loader(tmp, fetch=True)
                first = loader.load({"url": url + "/truncated"})
                self.assertEqual(first, loader.load({"url": url + "/truncated#again"}))
                self.assertEqual(first["text"], "")
                self.assertEqual((loader.network_requests, loader.hits), (1, 1))

                for path in list(html_robots) + ["/valid-robots", "/bom-rules"]:
                    with self.subTest(robots=path):
                        data = copy.deepcopy(self.data)
                        data["sites"][1]["pages"][0]["url"] = url + "/competitor"
                        data["sites"][0]["robots"] = {"url": url + path}
                        report = mod.build_report(data, mod.Loader(tmp, fetch=True))
                        bots = report["sites"][0]["pages"][0]["robots"]
                        self.assertEqual(set(bots), set(mod.CRAWLERS))
                        for bot, decision in bots.items():
                            if path == "/bom-rules":
                                self.assertEqual(decision["state"], "blocked" if bot == "GPTBot" else "allowed")
                                if bot == "GPTBot":
                                    self.assertEqual(decision["groups"], [["gptbot"]])
                                    self.assertEqual(decision["rule"], "disallow: /")
                            elif path == "/valid-robots":
                                self.assertEqual(decision["state"], "allowed")
                            else:
                                self.assertEqual(decision["state"], "unverified")
                                self.assertEqual(decision["reason"], "robots_returned_html")
                        self.assertEqual(requests.count(path), 1)
        finally:
            server.shutdown()
            server.server_close()
            thread.join()

    def test_http_get_cache_failure_and_no_guessed_paths(self):
        requests = []
        class Handler(BaseHTTPRequestHandler):
            def do_GET(self):
                requests.append(self.path)
                if self.path == "/chosen":
                    self.send_response(200)
                    self.send_header("Content-Type", "text/html; charset=utf-8")
                    self.end_headers()
                    self.wfile.write(b"<h1>Specified page</h1><p>Body</p>")
                else:
                    self.send_error(404)

            def log_message(self, *args):
                pass

        server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            url = f"http://127.0.0.1:{server.server_port}"
            loader = mod.Loader(ROOT / "examples", fetch=True)
            first = loader.load({"url": url + "/chosen"})
            second = loader.load({"url": url + "/chosen#again"})
            failed = loader.load({"url": url + "/missing"})
            self.assertEqual(first["sha256"], second["sha256"])
            self.assertEqual(failed["status"], "unverified")
            self.assertEqual(failed["http_status"], 404)
            self.assertEqual(requests, ["/chosen", "/missing"])
            self.assertEqual(loader.hits, 1)
        finally:
            server.shutdown()
            server.server_close()
            thread.join()

    def test_cli_csv_json_from_arbitrary_working_directory(self):
        with tempfile.TemporaryDirectory() as tmp:
            run = subprocess.run([sys.executable, str(ROOT / "scripts/compare_pages.py"),
                                  "--input", str(ROOT / "examples/comparison.json"), "--out", tmp],
                                 cwd=tmp, capture_output=True, text=True, check=False)
            self.assertEqual(run.returncode, 0, run.stderr)
            result = json.loads((Path(tmp) / "evidence.json").read_text(encoding="utf-8"))
            with (Path(tmp) / "竞品差距矩阵.csv").open(encoding="utf-8-sig", newline="") as handle:
                rows = list(csv.reader(handle))
            faq = next(row for row in rows if row[2] == "faq_visible_pairs")
            self.assertEqual([faq[3], faq[5], faq[7]], ["[模拟] 0", "[模拟] 2", "[模拟] 1"])
            self.assertEqual(result["sites"][1]["pages"][0]["signals"]["metrics"]["explicit_source_links"], 2)

    def test_cli_failure_is_explicit(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "bad.json"
            path.write_text('{"sites": []}', encoding="utf-8")
            run = subprocess.run([sys.executable, str(ROOT / "scripts/compare_pages.py"), "--input", str(path), "--out", tmp],
                                 cwd=tmp, capture_output=True, text=True, check=False)
            self.assertEqual(run.returncode, 2)
            self.assertIn("comparison.question", run.stderr)
            self.assertFalse((Path(tmp) / "evidence.json").exists())


if __name__ == "__main__":
    unittest.main(verbosity=2)
