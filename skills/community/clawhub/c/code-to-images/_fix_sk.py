with open('SKILL.md', 'r', encoding='utf-8') as f:
    c = f.read()
c = c.replace('<a href="#chinese">\u4e2d\u6587</a> \u00b7 <a href="#english">English</a>', '[\u4e2d\u6587](#chinese)')
c = c.replace('<a href="#chinese">\u4e2d\u6587</a>', '[\u4e2d\u6587](#chinese)')
c = c.replace('<a href="#english">English</a>', '[English](#english)')
with open('SKILL.md', 'w', encoding='utf-8') as f:
    f.write(c)
print('OK')
