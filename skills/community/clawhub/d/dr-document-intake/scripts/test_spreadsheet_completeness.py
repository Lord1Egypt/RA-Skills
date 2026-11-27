import importlib.util
import pathlib
import re
import tempfile
import unittest
import zipfile

from openpyxl import Workbook
from openpyxl.chart import BarChart, Reference
from openpyxl.comments import Comment
from openpyxl.worksheet.formula import ArrayFormula, DataTableFormula

SKILL = pathlib.Path(__file__).resolve().parents[1] / 'scripts' / 'document_intake.py'
spec = importlib.util.spec_from_file_location('draft_intake', SKILL)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


class SpreadsheetCompleteness(unittest.TestCase):
    def test_all_cells_formulas_cached_values_comments_and_hidden_sheets(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            src = root / 'book.xlsx'
            wb = Workbook()
            ws = wb.active
            ws.title = 'Main sheet'
            ws['A1'] = 'first line\nsecond line'
            ws['B1'] = '=1+1'
            ws['C1'] = '=2+2'
            ws['D1'].comment = Comment('audit comment text', 'tester')
            ws['A2'] = 42
            chart = BarChart()
            chart.add_data(Reference(ws, min_col=1, min_row=2, max_row=2))
            ws.add_chart(chart, 'F2')
            hidden = wb.create_sheet('Hidden data')
            hidden.sheet_state = 'hidden'
            hidden['A1'] = 'hidden source value'
            wb.save(src)
            # Give B1 a real cached numeric result; C1 remains uncached.
            with zipfile.ZipFile(src) as z:
                data = {n: z.read(n) for n in z.namelist()}
            xml = data['xl/worksheets/sheet1.xml'].decode()
            xml, count = re.subn(r'(<c r="B1"[^>]*><f>.*?</f><v>).*?(</v></c>)', r'\g<1>2\g<2>', xml, count=1)
            self.assertEqual(count, 1)
            data['xl/worksheets/sheet1.xml'] = xml.encode()
            with zipfile.ZipFile(src, 'w', zipfile.ZIP_DEFLATED) as z:
                for name, value in data.items():
                    z.writestr(name, value)
            result = mod.ingest(root, str(src))
            extract = (root / result['extract']).read_text()
            for value in ('Main sheet', 'first line\nsecond line', '=1+1', 'Cached value: 2', '=2+2', 'audit comment text', 'Hidden data', 'hidden source value'):
                self.assertIn(value, extract)
            self.assertTrue(any('1 formula cells' in x for x in result['limitations']))
            self.assertTrue(any('images or charts' in x for x in result['limitations']))
            self.assertEqual(mod.inspect(root, 'book.xlsx', src)['status'], 'fresh')

    def test_manual_text_retained_and_supplemented(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            src = root / 'book.xlsx'
            wb = Workbook()
            wb.active['A1'] = 'original cell'
            wb.save(src)
            manual = root / 'manual.txt'
            manual.write_text('manual OCR text')
            result = mod.ingest(root, str(src), str(manual), mod.digest(src))
            extract = (root / result['extract']).read_text()
            self.assertIn('manual OCR text', extract)
            self.assertIn('original cell', extract)
            with self.assertRaises(ValueError):
                mod.ingest(root, str(src), str(manual), 'incorrect')

    def test_comment_only_sheet_is_not_lost(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            src = root / 'comments.xlsx'
            wb = Workbook()
            wb.active['A1'].comment = Comment('standalone comment', 'tester')
            wb.save(src)
            result = mod.ingest(root, str(src))
            self.assertIn('standalone comment', (root / result['extract']).read_text())

    def test_array_and_data_table_formulas_are_not_object_reprs(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            src = root / 'arrays.xlsx'
            wb = Workbook()
            wb.active['A1'] = ArrayFormula(ref='A1:A2', text='=B1:B2*2')
            wb.active['C1'] = DataTableFormula(ref='C1:C2', r1='D1')
            wb.save(src)
            result = mod.ingest(root, str(src))
            extract = (root / result['extract']).read_text()
            self.assertIn('Array formula: =B1:B2*2', extract)
            self.assertIn('Formula range: A1:A2', extract)
            self.assertIn('"r1": "D1"', extract)
            self.assertNotIn('object at 0x', extract)

    def test_named_virtual_environments_are_not_document_gaps(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            (root / '.venv-report').mkdir()
            (root / '.venv-report' / 'package.txt').write_text('library file')
            (root / 'work.txt').write_text('actual work document')
            result = mod.audit(root)
            self.assertIn('.venv-report', result['excluded_directories'])
            self.assertEqual([x['source'] for x in result['items']], ['work.txt'])


if __name__ == '__main__':
    unittest.main()
