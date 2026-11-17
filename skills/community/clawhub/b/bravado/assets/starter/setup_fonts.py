"""Download and verify the typefaces used by the sample renderer."""
from pathlib import Path
from urllib.request import urlopen
import hashlib

ROOT=Path(__file__).resolve().parent/'fonts'
FONTS={
 'IBMPlexMono-400.ttf':('https://fonts.gstatic.com/s/ibmplexmono/v20/-F63fjptAgt5VM-kVkqdyU8n5ig.ttf','a7fdc993f9f0387caedba4e42521136fa97e4c0837ae6239bf0413ccf8af00c2'),
 'IBMPlexMono-500.ttf':('https://fonts.gstatic.com/s/ibmplexmono/v20/-F6qfjptAgt5VM-kVkqdyU8n3twJ8lc.ttf','4fc14a73ca53ba9d32fd759ae1ca1a3133326035d0dd337862b3ee1633cc156e'),
 'Inter-400.ttf':('https://fonts.gstatic.com/s/inter/v20/UcCO3FwrK3iLTeHuS_nVMrMxCp50SjIw2boKoduKmMEVuLyfMZg.ttf','1b08e7fc267a5c7e1d614100f604b83e7e8a0be241f0f288faa2b3ac93a683ba'),
 'Inter-700.ttf':('https://fonts.gstatic.com/s/inter/v20/UcCO3FwrK3iLTeHuS_nVMrMxCp50SjIw2boKoduKmMEVuFuYMZg.ttf','b37284b5701b6b168dfc770aa1a4ac492106422fd3ba76bc7641e37434e8019c'),
 'Inter-800.ttf':('https://fonts.gstatic.com/s/inter/v20/UcCO3FwrK3iLTeHuS_nVMrMxCp50SjIw2boKoduKmMEVuDyYMZg.ttf','eec66af7f2337bd34fe6e801cf92ededcb57a20c0d7bc40a61d4eefcbe3dd40c'),
 'PlayfairDisplay-700.ttf':('https://fonts.gstatic.com/s/playfairdisplay/v40/nuFvD-vYSZviVYUb_rj3ij__anPXJzDwcbmjWBN2PKeiukDQ.ttf','adefc53e7b3d483f1fa5e85edd82b7689ca79db25a1f6786bd7949cdcfeec601')
}

def main():
    ROOT.mkdir(exist_ok=True)
    for name,(url,digest) in FONTS.items():
        path=ROOT/name
        if path.exists() and hashlib.sha256(path.read_bytes()).hexdigest()==digest:continue
        with urlopen(url,timeout=30) as response:data=response.read()
        if hashlib.sha256(data).hexdigest()!=digest:raise ValueError(f'Font hash mismatch: {name}')
        path.write_bytes(data)
        print(f'Downloaded {name}')
if __name__=='__main__':main()
