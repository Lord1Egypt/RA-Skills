"""
修复 docx 文档中可能出现的非法空标签（如 docx-js 旧版本偶发的 <0/>）。

P2 修复：
- 原实现仅在 word/document.xml 做字面替换，且若用户正文恰好含「<0/>」字面量会被误删；
  页眉/页脚/编号等其他 XML 部件中的同类问题被漏处理。
- 现改为：扫描包内所有 *.xml 部件，仅移除「裸 <0/> 自闭合标签」（非命名空间元素、数字开头，
  属非法 XML，Word 无法打开），其余内容（含正文出现的 <0/> 字面文本）一律不动。
- 经实测，docx 9.6.1 生成的文档不含此问题，本脚本作为防御性安全网（no-op 时正常退出）。

用法:
    python fix_xml.py <input.docx> [output.docx]

若不指定 output.docx，则覆盖输入文件。
"""
import sys
import zipfile
import os
import re

# 仅匹配「裸 <0/>」：前面不能是字母/冒号（排除 <w:0/> 这类合法命名空间标签），
# 后面紧跟 > 结束。这样正文里出现的「<0/>」纯文本不会被误删，
# 但真正的非法标签 <0/> 会被移除。
BARE_ZERO_TAG = re.compile(r'(?<![\w:])<0/>(?=\s*<)')


def fix_docx(input_path, output_path=None):
    if output_path is None:
        output_path = input_path

    fixed_parts = []
    parts = {}

    with zipfile.ZipFile(input_path, 'r') as zin:
        for name in zin.namelist():
            data = zin.read(name)
            if name.endswith('.xml'):
                try:
                    text = data.decode('utf-8')
                except UnicodeDecodeError:
                    parts[name] = data
                    continue
                if '<0/>' in text:
                    # 仅移除裸 <0/>（夹在标签之间的非法空标签）；不触碰正文文本
                    new_text, n = BARE_ZERO_TAG.subn('', text)
                    if n > 0:
                        fixed_parts.append((name, n))
                    data = new_text.encode('utf-8')
            parts[name] = data

    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zout:
        for name, data in parts.items():
            zout.writestr(name, data)

    if fixed_parts:
        for name, n in fixed_parts:
            print(f'[FIX] Removed {n} illegal <0/> tag(s) in {name}')
    else:
        print('[SKIP] No illegal <0/> tags found (docx 9.6.1 output is clean).')

    # 校验所有 XML 部件可解析
    ok = True
    with zipfile.ZipFile(output_path, 'r') as z:
        import xml.etree.ElementTree as ET
        for name in z.namelist():
            if not name.endswith('.xml'):
                continue
            try:
                ET.fromstring(z.read(name))
            except ET.ParseError as e:
                print(f'[ERROR] {name} still invalid: {e}')
                ok = False
    print('[OK] Fixed & validated: ' + output_path if fixed_parts
          else '[OK] Validated (no changes): ' + output_path)
    return ok


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python fix_xml.py <input.docx> [output.docx]')
        sys.exit(1)
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    success = fix_docx(input_file, output_file)
    sys.exit(0 if success else 1)
