"""Offline regression tests for evidence, eligibility and safe editing."""
import json
import tempfile
import unittest
from dataclasses import asdict, replace
from pathlib import Path
from unittest.mock import patch
import verify_references as v
from generate_html_report import report_category, build_report_payload
from verifier_prior_results import _result_keys, prior_result_for_entry, load_prior_results

class Boundaries(unittest.TestCase):
    def setUp(self):
        self.entry=v.ReferenceEntry(1,'Smith JA. DNA methylation in human embryos. Journal A. 2024. doi:10.1234/example','ama','DNA methylation in human embryos',['Smith JA'],'Journal A','2024','10.1234/example','','','',volume='12',issue='3',pages='101-112')
        self.record=v.CanonicalRecord(source='Crossref',title=self.entry.title,authors=['Smith, John A'],journal='Journal A',year='2024',doi=self.entry.doi,volume='12',issue='3',pages='101-112')
    def classify(self,entry=None,record=None):
        return v.first_round_classification(entry or self.entry,record or self.record,'ama','report-only',False)
    def test_wrong_author_blocked_and_retained(self):
        r=self.classify(record=replace(self.record,authors=['Wrong, Alice']))
        self.assertEqual(r.status,'partial_attribute_corruption');self.assertEqual(r.fixed_reference,self.entry.original)
    def test_wrong_journal_not_normalized(self):
        r=self.classify(record=replace(self.record,journal='Unrelated Journal'))
        self.assertEqual(r.status,'partial_attribute_corruption')
        self.assertEqual(r.field_differences[0]['field'],'journal')
    def test_explicit_journal_alias(self):
        r=self.classify(record=replace(self.record,journal='Journal Alpha',journal_abbreviation='Journal A'))
        self.assertEqual(r.status,'minor_fix')
    def test_missing_author_or_year_cannot_pass(self):
        for e in (replace(self.entry,authors=[]),replace(self.entry,year='')):
            self.assertEqual(self.classify(e).status,'partial_attribute_corruption')
    def test_date_drift_needs_evidence(self):
        self.assertEqual(self.classify(record=replace(self.record,year='2023')).status,'partial_attribute_corruption')
    def test_identifier_only_not_usable(self):
        e=replace(self.entry,title_reliable=False);r=self.classify(e)
        v.describe_result(r,e,'verify','strict',['Crossref'])
        self.assertFalse(r.usable);self.assertEqual(report_category(r.status),'blocked')
        self.assertEqual(r.fixed_reference,e.original)
    def test_pmid_conflict_detected(self):
        e=replace(self.entry,pmid='12345678');r=self.classify(e,replace(self.record,pmid='87654321'))
        self.assertEqual(r.status,'partial_attribute_corruption')
    def test_empty_search_is_not_usable(self):
        e=replace(self.entry,doi='');r=v.first_round_classification(e,None,'ama','report-only',False)
        class Empty:
            def crossref_search(self,*a,**k):return []
            def openalex_search(self,*a,**k):return []
            def pubmed_search(self,*a,**k):return []
        v.recover_by_title([e],[r],Empty(),'ama','corroborate','corroborate','report-only',False)
        v.describe_result(r,e,'verify','strict',['Crossref'])
        self.assertEqual(r.status,'total_fabrication');self.assertFalse(r.usable)
    def test_no_title_similarity_based_record_merge(self):
        a=replace(self.record,pmid='');b=replace(self.record,doi='10.9999/other',pmid='12345678')
        self.assertEqual(v.merge_equivalent(a,[b]).pmid,'')
    def test_format_only_keeps_identifiers_and_details(self):
        for style in ('ama','vancouver','apa','gbt7714'):
            r=v.format_only_results([self.entry],style)[0]
            v.describe_result(r,self.entry,'format-only','balanced',[])
            for text in ('12','(3)','101-112','10.1234/example'):
                self.assertIn(text,r.fixed_reference)
            self.assertFalse(r.usable);self.assertEqual(r.status,'formatted_only')
    def test_recovered_doi_requires_append(self):
        e=replace(self.entry,doi=self.record.doi,recovered_doi=self.record.doi)
        self.assertNotIn('doi:',v.build_fixed_reference(e,self.record,'verified','ama','report-only'))
        self.assertIn('doi:',v.build_fixed_reference(e,self.record,'verified','ama','append'))
    def test_author_names(self):
        self.assertEqual(v.format_ama_author('Smith JA'),'Smith JA')
        self.assertEqual(v.format_ama_author('Smith, John A'),'Smith JA')
        self.assertEqual(v.format_ama_author('John Smith'),'Smith J')
        self.assertEqual(v.format_ama_author('Genome Research Consortium'),'Genome Research Consortium')
        self.assertEqual(len(v.normalize_authors(['Author']*25)),25)
    def test_et_al_is_a_verified_prefix(self):
        self.assertTrue(v.authors_agree(['Smith JA','et al'],['Smith, John A','Jones, Amy']))
        self.assertFalse(v.authors_agree(['Wrong A','et al'],['Smith, John A','Jones, Amy']))
        self.assertTrue(v.authors_agree(["O'Connell BL",'et al'],['O’Connell, Brendan L','Jones, Amy']))
    def test_title_with_commas_is_not_an_author_list(self):
        e=replace(self.entry,title='Epigenetics, fragmentomics, and topology of cell-free DNA in liquid biopsies')
        self.assertTrue(v.finalize_entry_quality(e).title_reliable)
    def test_page_range_equivalence(self):
        self.assertEqual(v.normalized_pages('E5503-E5512'),v.normalized_pages('E5503-12'))
        self.assertEqual(v.normalized_pages('e136'),v.normalized_pages('e136-e136'))
        self.assertNotEqual(v.normalized_pages('e2412660'),v.normalized_pages('e12660'))
    def test_pubmed_collective_author(self):
        xml=v.ET.fromstring('<PubmedArticle><MedlineCitation><PMID>12345678</PMID><Article><ArticleTitle>Title</ArticleTitle><AuthorList><Author><CollectiveName>Practice Committee</CollectiveName></Author></AuthorList></Article></MedlineCitation></PubmedArticle>')
        self.assertEqual(v.pubmed_record(xml).authors,['Practice Committee'])
        self.assertEqual(v.author_parts('Practice Committees. Electronic address: info@example.org')[0],'Practice Committees')
    def test_pubmed_issue_year_is_dated_evidence(self):
        best=replace(self.record,year='2020',publication_years=['2020'])
        issue=replace(self.record,source='PubMed',year='2021')
        merged=v.merge_equivalent(best,[issue])
        self.assertIn('2021',merged.publication_years)
    def test_placeholder_does_not_imply_hijacking(self):
        self.assertEqual(self.classify(record=replace(self.record,title='OUP accepted manuscript')).status,'unresolved')
    def test_same_doi_secondary_title_replaces_placeholder(self):
        primary=replace(self.record,title='OUP accepted manuscript')
        secondary=replace(self.record,source='PubMed')
        with patch.object(v,'run_identifier_queries',return_value=({self.entry.doi:primary},{},{self.entry.doi:secondary},{},{})):
            r=v.classify_entries([self.entry],object())[0]
        self.assertIn(r.status,{'verified','minor_fix'});self.assertEqual(r.canonical.source,'PubMed')
        self.assertEqual(len(r.provider_records),2)
    def test_source_records_preserve_locations_and_urls(self):
        entry=v.machine_record_to_entry({'source':{'original_text':'raw','title':self.entry.title,'source_lines':[12,15],'identifiers':{'urls':['https://example.org/paper']}}},1)
        self.assertEqual(entry.source_lines,[12,15]);self.assertEqual(entry.urls,['https://example.org/paper'])
    def saved(self):
        r=self.classify();v.describe_result(r,self.entry,'verify','balanced',['Crossref']);return asdict(r)
    def test_same_original_changed_fields_not_reused(self):
        row=self.saved();rows={k:row for k in _result_keys(row)}
        self.assertIsNotNone(prior_result_for_entry(rows,self.entry))
        for field,value in [('title','Another title'),('doi','10.1/other'),('authors',['Wrong Author']),('pmid','12345678'),('pages','200-210')]:
            self.assertIsNone(prior_result_for_entry(rows,replace(self.entry,**{field:value})))
    def test_reuse_checks_mode_pipeline_and_malformed_evidence(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/'audit.json';row=self.saved();p.write_text(json.dumps({'results':[row]}))
            self.assertTrue(load_prior_results(str(p),pipeline='verify',mode='balanced',channels=['Crossref'],policy_version=v.POLICY_VERSION))
            self.assertFalse(load_prior_results(str(p),pipeline='verify',mode='strict',channels=['Crossref'],policy_version=v.POLICY_VERSION))
            self.assertFalse(load_prior_results(str(p),pipeline='format-only',policy_version=v.POLICY_VERSION))
            row['canonical']['authors']='broken';p.write_text(json.dumps({'results':[row]}))
            self.assertFalse(load_prior_results(str(p)))
    def test_all_disabled_recovery_channels_stay_off(self):
        e=replace(self.entry,doi='')
        class Client:
            crossref_workers=1
            def crossref_search(self,*a,**k): return []
            def openalex_search(self,*a,**k): raise AssertionError('disabled')
            def pubmed_search(self,*a,**k): raise AssertionError('disabled')
        v.recover_missing_dois_early([e],Client(),v.RuntimeMetrics(mode='balanced'),'balanced','off','off')

if __name__=='__main__':unittest.main()
