import csv,io,json,pathlib,tempfile,unittest,zipfile,importlib.util
spec=importlib.util.spec_from_file_location('parser',pathlib.Path(__file__).resolve().parent.parent/'summarize_chat_export.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class ExportTests(unittest.TestCase):
 def test_nested_quotes_and_malformed_tail(self):
  with tempfile.TemporaryDirectory() as d:
   p=pathlib.Path(d)/'log.csv';details=[{'value':[{'text':{'content':'hi'}}]},{'value':[{'file':{'name':'x.jpg'}}]}]
   s=io.StringIO();w=csv.writer(s);w.writerow(['最后对话时间','对话详情','状态']);w.writerow(['2026-11-01', '"'+json.dumps(details).replace('"','""')+'"','{}','extra']);p.write_text(s.getvalue(),encoding='utf-8-sig',newline='');r=m.summarize(p)['sheets'][0]
   self.assertEqual(r['parsed_sessions'],1);self.assertEqual(r['messages'],2);self.assertEqual(r['attachments'],1);self.assertEqual(r['column_mismatch_rows'],[2]);self.assertFalse(r['unparsed_rows'])
 def test_bad_details_not_silently_dropped(self):
  with tempfile.TemporaryDirectory() as d:
   p=pathlib.Path(d)/'log.csv';p.write_text('对话详情\nbad\n',encoding='utf-8');self.assertEqual(m.summarize(p)['sheets'][0]['unparsed_rows'],[2])
 def test_xlsx_two_sheets_without_execution(self):
  with tempfile.TemporaryDirectory() as d:
   p=pathlib.Path(d)/'a.xlsx'
   ns='http://schemas.openxmlformats.org/spreadsheetml/2006/main'
   with zipfile.ZipFile(p,'w') as z:
    z.writestr('xl/workbook.xml',f'<workbook xmlns="{ns}" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"><sheets><sheet name="一" r:id="r1"/><sheet name="二" r:id="r2"/></sheets></workbook>')
    z.writestr('xl/_rels/workbook.xml.rels','<Relationships><Relationship Id="r1" Target="worksheets/s1.xml"/><Relationship Id="r2" Target="/xl/worksheets/s2.xml"/></Relationships>')
    for n in [1,2]:z.writestr(f'xl/worksheets/s{n}.xml',f'<worksheet xmlns="{ns}"><sheetData><row><c r="A1" t="inlineStr"><is><t>对话详情</t></is></c></row><row><c r="A2" t="inlineStr"><is><t>[]</t></is></c></row></sheetData></worksheet>')
   r=m.summarize(p);self.assertEqual(len(r['sheets']),2);self.assertTrue(all(s['parsed_sessions']==1 for s in r['sheets']))
if __name__=='__main__':unittest.main()
