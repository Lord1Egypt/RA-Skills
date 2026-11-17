# Cover-letter DOCX builder with approved letter spacing.
# Résumés use resume_layout.py's explicit blocks; letters use make_letter.
# Expected lines: name, contact lines..., date, recipient, salutation, body/headings..., closing, signature.
import zipfile,re,xml.etree.ElementTree as E
W='http://schemas.openxmlformats.org/wordprocessingml/2006/main'
R='http://schemas.openxmlformats.org/officeDocument/2006/relationships'
E.register_namespace('w',W);E.register_namespace('r',R)
def q(s):return '{'+W+'}'+s
from resume_layout import inline_link_runs, validate_xml_text
# twentieths of a point; body 11pt Calibri, 1.1 line spacing, 1-inch side and 0.75-inch top/bottom margins
STYLE={'name':(0,60,'32',True),'contact':(0,60,'21',False),'date':(280,0,'22',False),'recipient':(160,0,'22',False),
 'salutation':(280,200,'22',False),'heading':(160,120,'22',True),'body':(0,200,'22',False),
 'closing':(60,360,'22',False),'signature':(0,0,'22',False)}
MARGIN='1440';VMARGIN='1080'
def validate_letter(lines,contact_lines):
 if isinstance(contact_lines,bool) or not isinstance(contact_lines,int) or contact_lines<0:
  raise ValueError('Set contact_lines_count explicitly to the actual number of contact paragraphs')
 if not isinstance(lines,list) or len(lines)<contact_lines+7:
  raise ValueError('Complete letter paragraphs required')
 for text in lines:
  validate_xml_text(text)
  if '\n' in text or '\r' in text:raise ValueError('Use one letter paragraph per entry; paragraph spacing supplies the gaps')

def roles(lines,contact_lines):
 validate_letter(lines,contact_lines)
 out=['name']+['contact']*contact_lines+['date','recipient','salutation']
 for t in lines[len(out):-2]:out.append('heading' if t.startswith('• ') else 'body')
 return out+['closing','signature']
# Compact gaps retain visible paragraph separation.
# Font sizes, line spacing and margins remain the canonical values above.
COMPACT_SPACING={'name':(0,0),'date':(240,0),'recipient':(120,0),'salutation':(200,120),
                 'body':(0,120),'closing':(0,300)}
def make_letter(lines,path,contact_lines=None,scale=1.0,spacing='standard'):
 if spacing not in ('standard','compact'):raise ValueError('Unknown letter spacing profile')
 vertical_margin=VMARGIN
 rl=roles(lines,contact_lines)
 root=E.Element(q('document'));body=E.SubElement(root,q('body'))
 rels=E.Element('Relationships',xmlns='http://schemas.openxmlformats.org/package/2006/relationships')
 for i,(text,role) in enumerate(zip(lines,rl)):
  before,after,size,bold=STYLE[role]
  if spacing=='compact':before,after=COMPACT_SPACING.get(role,(before,after))
  p=E.SubElement(body,q('p'));pp=E.SubElement(p,q('pPr'))
  E.SubElement(pp,q('spacing'),{q('before'):str(round(before*scale)),q('after'):str(round(after*scale)),q('line'):'264' if role in('body','heading') else '252',q('lineRule'):'auto'})
  if role in('name','contact','date','recipient','heading','closing'):E.SubElement(pp,q('keepNext'))
  E.SubElement(pp,q('keepLines'))
  for part,target in inline_link_runs(text):
   if not part:continue
   container=p
   if target:
    rid='rId'+str(len(rels)+1)
    E.SubElement(rels,'Relationship',Id=rid,Type=R+'/hyperlink',Target=target,TargetMode='External')
    container=E.SubElement(p,q('hyperlink'),{'{'+R+'}id':rid})
   run=E.SubElement(container,q('r'));rp=E.SubElement(run,q('rPr'))
   E.SubElement(rp,q('rFonts'),{q('ascii'):'Calibri',q('hAnsi'):'Calibri'})
   if bold:E.SubElement(rp,q('b'))
   E.SubElement(rp,q('sz'),{q('val'):size})
   t=E.SubElement(run,q('t'));t.text=part;t.set('{http://www.w3.org/XML/1998/namespace}space','preserve')
 sect=E.SubElement(body,q('sectPr'))
 E.SubElement(sect,q('pgSz'),{q('w'):'12240',q('h'):'15840'})
 E.SubElement(sect,q('pgMar'),{q('top'):vertical_margin,q('bottom'):vertical_margin,q('left'):MARGIN,q('right'):MARGIN,q('header'):'0',q('footer'):'0',q('gutter'):'0'})
 ctypes='<?xml version="1.0"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/></Types>'
 package='<?xml version="1.0"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/></Relationships>'
 with zipfile.ZipFile(path,'w',zipfile.ZIP_DEFLATED) as z:
  z.writestr('[Content_Types].xml',ctypes);z.writestr('_rels/.rels',package)
  z.writestr('word/document.xml',E.tostring(root,encoding='utf-8',xml_declaration=True))
  z.writestr('word/_rels/document.xml.rels',E.tostring(rels,encoding='utf-8',xml_declaration=True))
 return rl
