import zipfile, shutil, os, re, tempfile

desktop = os.path.join(os.environ['USERPROFILE'], 'Desktop')
target_size = 15914
matching = [(f, os.path.getsize(os.path.join(desktop, f))) for f in os.listdir(desktop)
            if f.endswith('.xlsx') and os.path.getsize(os.path.join(desktop, f)) == target_size]
filename, _ = matching[0]
filepath = os.path.join(desktop, filename)
print('Fixing:', filepath)

# Read all files from the xlsx
with zipfile.ZipFile(filepath, 'r') as z:
    names = z.namelist()
    files = {}
    for name in names:
        with z.open(name) as f:
            files[name] = f.read()

# Fix sharedStrings.xml: the bytes are GBK but XML declares UTF-8
# Re-decode as GBK and re-encode as UTF-8
shared = files['xl/sharedStrings.xml']
# Decode the raw bytes as GBK, then encode as UTF-8
content_str = shared.decode('gbk', errors='replace')
# Remove the encoding declaration and save as UTF-8
content_str = content_str.replace('encoding="UTF-8"', 'encoding="UTF-8"')
# Re-encode only the content (t tags) as proper UTF-8
def fix_t(content):
    # For each <t> element, get the text, decode from GBK bytes (the bytes we have are GBK), 
    # then the string is already decoded - but we need to re-encode properly
    def replacer(m):
        return m.group(0)
    return content

# Actually, let's take a different approach: rebuild the strings correctly
# The sharedStrings.xml stores raw UTF-8 bytes but labeled as such - the issue is the underlying storage
# Let's just re-save the strings by reading them correctly (as GBK) and writing as UTF-8

new_shared = shared.decode('gbk', errors='replace').encode('utf-8', errors='replace')
files['xl/sharedStrings.xml'] = new_shared

# Also fix worksheet and other XMLs that may have inline strings
for name in ['xl/worksheets/sheet1.xml', 'xl/workbook.xml']:
    if name in files:
        content = files[name]
        try:
            s = content.decode('gbk', errors='replace')
            files[name] = s.encode('utf-8', errors='replace')
        except:
            pass

# Save fixed xlsx
fixed_path = os.path.join(desktop, 'fixed_' + filename)
with zipfile.ZipFile(fixed_path, 'w', zipfile.ZIP_DEFLATED) as zout:
    for name in names:
        zout.writestr(name, files[name])

print('Fixed file saved to:', fixed_path)
print('Original size:', os.path.getsize(filepath))
print('Fixed size:', os.path.getsize(fixed_path))
