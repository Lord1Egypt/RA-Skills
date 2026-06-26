import os, shutil, sys
from pathlib import Path

HOME = Path(os.environ.get('USERPROFILE','~')).expanduser()
DESKTOP = HOME / 'Desktop'

# extensions map
EXT_MAP = {
    'PDFs': {'.pdf'},
    'Images': {'.jpg', '.jpeg', '.png', '.gif'},
    'Archives': {'.zip', '.rar', '.7z'},
    'Documents': {'.docx', '.xlsx'},
    'Presentations': {'.pptx'},
}

if not DESKTOP.exists():
    print('ERROR: Desktop not found:', DESKTOP)
    sys.exit(1)

moved = {k: 0 for k in EXT_MAP}

for item in DESKTOP.iterdir():
    if not item.is_file():
        continue
    if item.suffix.lower() in {'.lnk', '.ini'}:
        continue
    ext = item.suffix.lower()
    target_folder = None
    for folder, exts in EXT_MAP.items():
        if ext in exts:
            target_folder = folder
            break
    if not target_folder:
        continue
    dest_dir = DESKTOP / target_folder
    dest_dir.mkdir(exist_ok=True)
    dest = dest_dir / item.name
    try:
        shutil.move(str(item), str(dest))
        moved[target_folder] += 1
    except Exception:
        # skip locked or move errors
        pass

print('RESULT')
for folder in EXT_MAP:
    print(f"{folder}: {moved[folder]}")
