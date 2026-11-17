"""Copy the Bravado starter into a new directory without replacing existing work."""
from pathlib import Path
import argparse, shutil

parser=argparse.ArgumentParser()
parser.add_argument('destination',type=Path)
args=parser.parse_args()
source=Path(__file__).resolve().parent.parent/'assets'/'starter'
dest=args.destination.resolve()
if dest.exists() and any(dest.iterdir()):
    parser.error(f'Destination is not empty: {dest}')
dest.mkdir(parents=True,exist_ok=True)
shutil.copytree(source,dest,dirs_exist_ok=True)
print(dest)
