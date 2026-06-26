import glob, os
for path in ['README.md', '../skills/code-to-images/SKILL.md']:
    with open(path, 'r', encoding='utf-8') as f:
        c = f.read()
    # Remove raw HTML anchor tags
    c = c.replace('| <a href="#chinese">\u4e2d\u6587</a> \u00b7 <a href="#english">English</a>', '| [\u4e2d\u6587](#chinese)')
    c = c.replace('\u00b7 <a href="#chinese">\u4e2d\u6587</a>', '| [\u4e2d\u6587](#chinese)')
    c = c.replace('<a href="#chinese">\u4e2d\u6587</a> \u00b7 <a href="#english">English</a>', '[\u4e2d\u6587](#chinese)')
    c = c.replace('<a href="#chinese">\u4e2d\u6587</a>', '[\u4e2d\u6587](#chinese)')
    c = c.replace('<a href="#english">English</a>', '[English](#english)')

    with open(path, 'w', encoding='utf-8') as f:
        f.write(c)
    print(f'Fixed: {path}')
