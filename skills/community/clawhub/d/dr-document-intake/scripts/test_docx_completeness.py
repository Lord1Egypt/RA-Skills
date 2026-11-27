import importlib.util
import io
import pathlib
import tempfile
import unittest
import zipfile

from docx import Document
from PIL import Image

SKILL = pathlib.Path(__file__).resolve().parents[1] / 'scripts' / 'document_intake.py'
spec = importlib.util.spec_from_file_location('draft_intake_docx', SKILL)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


class DocxCompleteness(unittest.TestCase):
    def test_recovers_header_footer_table_comment_and_drawing_text(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            src = root / 'document.docx'
            doc = Document()
            doc.add_paragraph('Body content')
            doc.sections[0].header.paragraphs[0].text = 'Header evidence'
            doc.sections[0].footer.paragraphs[0].text = 'Footer evidence'
            doc.add_table(rows=1, cols=1).cell(0, 0).text = 'Table evidence'
            image = root / 'image.png'
            Image.new('RGB', (40, 30), 'white').save(image)
            doc.add_picture(str(image))
            doc.save(src)
            with zipfile.ZipFile(src) as z:
                entries = {n: z.read(n) for n in z.namelist()}
            entries['word/comments.xml'] = b'<w:comments xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:comment><w:p><w:r><w:t>Comment evidence</w:t></w:r></w:p></w:comment></w:comments>'
            entries['word/charts/chart1.xml'] = b'<c:chart xmlns:c="http://schemas.openxmlformats.org/drawingml/2006/chart" xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"><a:t>Chart label evidence</a:t><c:v>314159</c:v></c:chart>'
            with zipfile.ZipFile(src, 'w', zipfile.ZIP_DEFLATED) as z:
                for name, value in entries.items():
                    z.writestr(name, value)
            manual = root / 'converter.txt'
            manual.write_text('Body content')
            result = mod.ingest(root, str(src), str(manual), mod.digest(src))
            extract = (root / result['extract']).read_text()
            for value in ('Body content', 'Header evidence', 'Footer evidence', 'Table evidence', 'Comment evidence', 'Chart label evidence', '314159'):
                self.assertIn(value, extract)
            self.assertTrue(any('embedded images' in x for x in result['limitations']))
            self.assertTrue(any('charts' in x for x in result['limitations']))
            self.assertEqual(mod.inspect(root, 'document.docx', src)['status'], 'fresh')

    def test_existing_text_is_not_added_twice(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            src = root / 'simple.docx'
            doc = Document()
            doc.add_paragraph('Distinct content is already present')
            doc.save(src)
            extra, limitations = mod.docx_missing_text(src, 'Distinct content is already present')
            self.assertEqual(extra, '')
            self.assertEqual(limitations, [])


if __name__ == '__main__':
    unittest.main()
