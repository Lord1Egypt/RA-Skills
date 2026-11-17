"""Regression tests for opt-in email and bilingual offline reports."""
import json
import os
import re
import sys
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from urllib.parse import urlparse, parse_qs
import verify_references as v
import generate_html_report as h

class PrivacyLanguage(unittest.TestCase):
    def test_cli_ignores_ambient_email(self):
        with tempfile.TemporaryDirectory() as td:
            source=Path(td)/'input.json'
            source.write_text(json.dumps({'records':[{'index':1,'source':{'original_text':'Smith JA. DNA methylation in human embryos. 2024.','title':'DNA methylation in human embryos','authors':['Smith JA'],'year':'2024'}}]}))
            entries=v.build_entries(source.read_text(),None,'records')
            results=v.format_only_results(entries,'ama')
            with patch.dict(os.environ,{'USER_EMAIL':'private@example.org','CLAWDBOT_EMAIL':'other@example.org'}), patch.object(sys,'argv',['verify',str(source),'--output-dir',str(Path(td)/'out')]), patch.object(v,'ApiClient') as client, patch.object(v,'recover_missing_dois_early'), patch.object(v,'classify_entries',return_value=results), patch.object(v,'write_outputs'):
                self.assertEqual(v.main(),0)
                self.assertEqual(client.call_args.kwargs['email'],'')

    def test_provider_queries_only_include_explicit_email(self):
        for email in ('','contact@example.org'):
            with self.subTest(email=email):
                c=v.ApiClient(email=email); urls=[]
                def json_response(url):
                    urls.append(url)
                    return {'message':{'items':[]},'esearchresult':{'idlist':[]},'results':[]}
                def bytes_response(url):urls.append(url); return b'<PubmedArticleSet/>'
                with patch.object(c,'get_json',side_effect=json_response),patch.object(c,'get_bytes',side_effect=bytes_response):
                    c.crossref_by_doi('10.1234/example'); c.crossref_search('DNA methylation')
                    c.pubmed_search('DNA methylation');c.fetch_pubmed_pmids(['123']);c._pubmed_by_doi_batch_once(['10.1234/example'])
                    c.openalex_by_doi('10.1234/example');c.openalex_by_pmid('123');c.openalex_search('DNA methylation')
                self.assertGreaterEqual(len(urls),8)
                for url in urls:
                    query=parse_qs(urlparse(url).query,keep_blank_values=True)
                    values=query.get('email',query.get('mailto',[]))
                    self.assertEqual(values,[email] if email else [])

    def test_user_agent_omits_email_by_default(self):
        for email in ('','contact@example.org'):
            with self.subTest(email=email),patch.object(v.urllib.request,'urlopen') as request:
                request.return_value.__enter__.return_value.read.return_value=b'{}'
                v.ApiClient(email=email).get_bytes('https://api.crossref.org/works')
                header=request.call_args.args[0].get_header('User-agent')
                self.assertEqual('mailto:' in header,bool(email))
                if email:self.assertIn(email,header)

    def test_english_template_translates_ui_without_mutating_evidence(self):
        row={'index':1,'status':'unresolved','original':'原始文献','fixed_reference':'原始文献  [不可用：unresolved，未自动修复]','suggested_action':'不可用：当前证据未通过核查。保留原文供复核，不纳入可用引用。 Retry.','field_differences':[{'after':'未取得对应证据'}]}
        payload=h.build_report_payload(input_path='refs',results=[row]);before=json.dumps(payload)
        html=h.render_html(payload,language='en')
        self.assertIn('lang="en"',html);self.assertIn('Copy filtered results',html)
        self.assertIn('Not eligible:',html);self.assertIn('原始文献',html)
        self.assertEqual(json.dumps(payload),before)
        template=h.TEMPLATE_PATH.with_name('reference-audit-report-template.en.html').read_text()
        self.assertIsNone(re.search(r'[\u4e00-\u9fff]',template))
        self.assertIn('参考文献核查',h.render_html(payload))

    def test_both_cli_entrypoints_select_english(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);source=root/'input.json'
            source.write_text(json.dumps({'records':[{'index':1,'source':{'original_text':'Smith JA. DNA methylation in human embryos. 2024.','title':'DNA methylation in human embryos','authors':['Smith JA'],'year':'2024'}}]}))
            result=subprocess.run([sys.executable,str(Path(v.__file__)),str(source),'--pipeline','format-only','--report-language','en','--output-dir',str(root/'out'),'--keep-process-json'],capture_output=True,text=True)
            self.assertEqual(result.returncode,0,result.stderr)
            self.assertIn('lang="en"',(root/'out/reference-audit-report.html').read_text())
            result=subprocess.run([sys.executable,str(Path(h.__file__)),str(root/'out/reference-audit.json'),'--language','en','--output',str(root/'standalone.html')],capture_output=True,text=True)
            self.assertEqual(result.returncode,0,result.stderr)
            self.assertIn('lang="en"',(root/'standalone.html').read_text())

    def test_both_templates_escape_payload(self):
        for lang in ('zh','en'):
            html=h.render_html({'results':[{'original':'</script><img src=x onerror=alert(1)>'}]},language=lang)
            self.assertNotIn('</script><img',html)
            self.assertIn('\\u003c/script',html)

if __name__=='__main__':unittest.main()
