"""Build a completed application as Word files, PDFs or both. No API calls."""
import argparse,hashlib,json,os,tempfile
from pathlib import Path
from resume_layout import build, validate_blocks
from letter_layout import make_letter, validate_letter


def verify_receipt(path, expected, label, document=None, hash_field='docx_sha256'):
 try:
  receipt=json.loads(path.read_text(encoding='utf-8'))
  if not isinstance(receipt,dict) or any(receipt.get(k)!=v for k,v in expected.items()):
   raise ValueError('Source metadata differs')
  if document is not None and receipt.get(hash_field)!=hashlib.sha256(document.read_bytes()).hexdigest():
   raise ValueError('Document differs')
 except (ValueError,TypeError) as exc:
  raise ValueError(f'Existing {label} differs from its saved receipt; preserve it and choose a new revision directory') from exc
 return receipt


def publish(source, destination):
 try:
  os.link(source,destination)
 except OSError as exc:
  raise OSError(exc.errno,'Document publication needs filesystem hard-link support and write permission. '
                'Saved files and pending receipts are preserved; resume on supported storage or use another document tool.') from exc


def render(packet,destination,resume=False,format='docx'):
 if format not in ('docx','pdf','both'):
  raise ValueError('format must be docx, pdf or both')
 out=Path(destination)
 lines=packet['cover_letter_lines'];contacts=packet.get('contact_lines_count')
 validate_letter(lines,contacts)
 validate_blocks(packet['resume_blocks'])
 if packet.get('letter_spacing','standard') not in ['standard','compact']:
  raise ValueError('letter_spacing must be standard or compact')
 packet_text=json.dumps(packet,indent=2,ensure_ascii=False)+'\n'
 packet_file=out/'packet.json'
 names=['Resume.docx','Resume.layout.json','Letter.docx','Letter.layout.json','packet.json','.Resume.pending.json','.Letter.pending.json']
 if format in ('pdf','both'):
  names += ['Resume.pdf','Letter.pdf','Resume.pdf.json','Letter.pdf.json','.Resume.pdf.pending.json','.Letter.pdf.pending.json']
 if not resume and any((out/name).exists() for name in names):
  raise ValueError('Preserve existing files; choose a new revision directory')
 if resume and (not packet_file.is_file() or json.loads(packet_file.read_text(encoding='utf-8'))!=packet):
  raise ValueError('Resume requires the same saved packet; choose a new revision directory for changed wording or layout')
 documents=[('Resume',{'source_blocks':packet['resume_blocks']}),
            ('Letter',{'source_lines':lines,'contact_lines_count':contacts,
                       'letter_spacing':packet.get('letter_spacing','standard')})]
 # Validate every existing file before repairing either document.
 for name,expected in documents:
  document=out/(name+'.docx');receipt=out/(name+'.layout.json');pending=out/('.'+name+'.pending.json')
  if pending.exists():verify_receipt(pending,expected,name.lower(),document if document.exists() else None)
  if document.exists():
   saved=receipt if receipt.is_file() else pending
   if not saved.is_file():raise ValueError(f'Existing {name.lower()} has no receipt; preserve it and choose a new revision directory')
   verify_receipt(saved,expected,name.lower(),document)
  elif receipt.exists():
   raise ValueError(f'An existing {name.lower()} receipt needs a separate revision directory')
 out.mkdir(parents=True,exist_ok=True)
 if not resume:
  with packet_file.open('x',encoding='utf-8') as f:f.write(packet_text)
 # Save the receipt before publishing its document; it survives staging cleanup.
 with tempfile.TemporaryDirectory(prefix='.get-hired-pro-build-',dir=out) as temporary:
  staging=Path(temporary)
  for name,expected in documents:
   document=out/(name+'.docx');receipt=out/(name+'.layout.json');pending=out/('.'+name+'.pending.json')
   if not document.exists():
    staged=staging/(name+'.docx');staged_receipt=staging/(name+'.layout.json')
    if name=='Resume':
     build({'blocks':packet['resume_blocks']},staged)
    else:
     make_letter(lines,staged,contact_lines=contacts,spacing=packet.get('letter_spacing','standard'))
     data={**expected,'docx_sha256':hashlib.sha256(staged.read_bytes()).hexdigest()}
     staged_receipt.write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    os.replace(staged_receipt,pending)
    publish(staged,document)
   if not receipt.exists():publish(pending,receipt)
   if pending.exists():pending.unlink()
 if format in ('pdf','both'):
  from pdf_layout import export_pdfs
  export_pdfs(out,resume=resume,publish=publish,verify=verify_receipt)
 return json.loads((out/'Resume.layout.json').read_text(encoding='utf-8'))

if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('packet');p.add_argument('destination');p.add_argument('--resume',action='store_true',help='Complete missing files for the identical saved packet; preserve existing documents');p.add_argument('--format',choices=['docx','pdf','both'],default='docx');a=p.parse_args()
 render(json.loads(Path(a.packet).read_text(encoding='utf-8')),a.destination,resume=a.resume,format=a.format)
 print('Built '+('Resume.docx and Letter.docx' if a.format=='docx' else 'Resume.pdf and Letter.pdf'+(' plus Word copies' if a.format=='both' else ''))+'.')
