"""Local Tesseract execution with verified private model snapshots."""
from dataclasses import asdict, dataclass
import hashlib, math, os, re, shutil, tempfile
from pathlib import Path
from .base import OCRProvider
from .errors import OCRError
from .models import OCRPage, OCRProviderCapabilities, OCRProviderMetadata, OCRProvenance, OCREvidence
from .process import ProcessRunner
from .validation import validate_provider, validate_request

_VERSION = re.compile(r"^tesseract\s+(\d+)\.(\d+)(?:\.(\d+))?(?=\s|$|[-+])", re.I | re.M)
_HEADER = "level page_num block_num par_num line_num word_num left top width height conf text".split()

def parse_tesseract_version(output):
    m = _VERSION.search(output or "")
    if not m: raise OCRError("could not determine Tesseract version", "OCR_PROVIDER_VERSION_UNAVAILABLE")
    if m.group(1) != "5": raise OCRError("unsupported Tesseract major version", "OCR_PROVIDER_VERSION_UNSUPPORTED")
    return ".".join(x for x in m.groups() if x is not None)

@dataclass(frozen=True)
class Traineddata:
    model_id: str
    model_digest: str
    model_source: str

def _languages(value):
    names = value.split("+") if isinstance(value, str) else value
    if not isinstance(names, (tuple, list)) or not names or len(set(names)) != len(names):
        raise OCRError("invalid language configuration", "OCR_LANGUAGE_UNSUPPORTED")
    if any(not isinstance(n, str) or not re.fullmatch(r"[A-Za-z0-9_]+", n) for n in names):
        raise OCRError("invalid language configuration", "OCR_LANGUAGE_UNSUPPORTED")
    return tuple(names)

def _read(path):
    try: return path.read_bytes()
    except OSError as exc: raise OCRError("required traineddata unavailable", "OCR_MODEL_UNAVAILABLE") from exc

class TesseractProvider(OCRProvider):
    provider_id = "tesseract"
    provider_version = "phase15.1"
    capabilities = OCRProviderCapabilities(True, True, "local", False, bounding_boxes=True, confidence=True, word_boxes=True)

    def __init__(self, executable=None, *, runner=None, tessdata_dir=None, model_sources=None):
        self.executable = executable; self.runner = runner or ProcessRunner()
        self.tessdata_dir = Path(tessdata_dir).resolve() if tessdata_dir else None
        self.model_sources = dict(model_sources or {})

    def resolve_executable(self):
        try: path = self.executable or shutil.which("tesseract")
        except (OSError, ValueError) as exc: raise OCRError("Tesseract unavailable", "OCR_PROVIDER_UNAVAILABLE") from exc
        if not isinstance(path, str) or not path or "\\0" in path: raise OCRError("Tesseract unavailable", "OCR_PROVIDER_UNAVAILABLE")
        return path

    def _version(self, exe):
        result = self.runner.run([exe, "--version"])
        if result.returncode: raise OCRError("version probe failed", "OCR_PROVIDER_VERSION_UNAVAILABLE")
        return parse_tesseract_version(result.stdout)

    def detect_version(self): return self._version(self.resolve_executable())

    def discover_traineddata(self, languages):
        names = _languages(languages)
        if self.tessdata_dir is None: raise OCRError("traineddata directory unavailable", "OCR_MODEL_UNAVAILABLE")
        found=[]
        for name in names:
            data = _read(self.tessdata_dir / (name + ".traineddata")); source = self.model_sources.get(name)
            if source is None:
                source = "sha256:" + hashlib.sha256(data).hexdigest()
            if not isinstance(source, str) or not source or source.lower() == "unknown" or source.startswith(("/", "file:", "~")):
                raise OCRError("portable model source attribution required", "OCR_PROVIDER_CONTRACT_INVALID")
            found.append(Traineddata(name, hashlib.sha256(data).hexdigest(), source))
        return tuple(sorted(found, key=lambda m:(m.model_id,m.model_digest,m.model_source)))

    def recognize(self, request, *, expected_models=None):
        validate_request(request); validate_provider(self)
        names = _languages(request.language_config.get("languages", ("eng",)))
        models = self.discover_traineddata(names)
        if expected_models is not None and tuple(expected_models) != models: raise OCRError("traineddata changed", "OCR_MODEL_CHANGED")
        with tempfile.TemporaryDirectory(prefix="agy-ocr-") as temp:
            root=Path(temp); snap=root/"tessdata"; snap.mkdir(mode=0o700)
            for model in models:
                data=_read(self.tessdata_dir/(model.model_id+".traineddata"))
                if hashlib.sha256(data).hexdigest()!=model.model_digest: raise OCRError("traineddata changed", "OCR_MODEL_CHANGED")
                dest=snap/(model.model_id+".traineddata"); dest.write_bytes(data); dest.chmod(0o400)
                if hashlib.sha256(_read(dest)).hexdigest()!=model.model_digest: raise OCRError("snapshot digest mismatch", "OCR_MODEL_CHANGED")
            exe=self.resolve_executable(); version=self._version(exe); image=root/"input"; image.write_bytes(request.image_bytes); output=root/"result"
            argv=[exe,str(image),str(output),"--tessdata-dir",str(snap),"-l","+".join(names),"--psm","3","-c","tessedit_create_txt=1","-c","tessedit_create_tsv=1"]
            result=self.runner.run(argv)
            if result.returncode: raise OCRError("Tesseract recognition failed", "OCR_PROVIDER_FAILED")
            try:
                raw=output.with_suffix(".txt").read_bytes().decode("utf-8",errors="strict")
                tsv=output.with_suffix(".tsv").read_bytes().decode("utf-8",errors="strict")
            except (OSError, UnicodeError) as exc: raise OCRError("invalid recognition output", "OCR_PROVIDER_OUTPUT_INVALID") from exc
            regions=parse_tsv(tsv)
        evidence=OCREvidence("1.0",request.source_id,request.source_digest,(OCRPage(request.locator,raw,tuple(regions)),),self.capabilities,OCRProviderMetadata(self.provider_id,self.provider_version,"tesseract",version),OCRProvenance(self.provider_id,self.provider_id,"local",False),model_manifest=tuple(asdict(m) for m in models),language_config={"languages":names},execution_config={"page_segmentation_mode":3,"text_output":True,"tsv_output":True})
        evidence.validate(); return evidence

def parse_tsv(text):
    lines=text.splitlines();
    if not lines or lines[0].split("\t")!=_HEADER: raise OCRError("invalid TSV header", "OCR_PROVIDER_OUTPUT_INVALID")
    regions=[]
    for line in lines[1:]:
        f=line.split("\t")
        try:
            if len(f)!=12 or any(not re.fullmatch(r"[0-9]+",x) for x in f[:10]): raise ValueError
            level,page,block,par,row,word,x,y,w,h=map(int,f[:10]); conf=float(f[10])
            if not math.isfinite(conf) or conf < -1 or conf > 100 or any(v<0 for v in (x,y,w,h)): raise ValueError
            if level!=5: continue
            region={"region_id":"w-"+"-".join(f[:6]),"text":f[11]}
            if conf!=-1: region["confidence"]={"raw_confidence":conf,"confidence_scale":"0-100","confidence_source":"tesseract_word"}
            regions.append(((page,block,par,row,word),region,(x,y,w,h)))
        except (ValueError,TypeError): raise OCRError("malformed TSV evidence", "OCR_PROVIDER_OUTPUT_INVALID")
    # Pixel geometry is retained only when a page row supplies dimensions.
    page_rows=[line.split("\t") for line in lines[1:] if line.split("\t")[0]=="1"]
    if page_rows:
        try: iw,ih=int(page_rows[0][8]),int(page_rows[0][9])
        except (IndexError,ValueError): raise OCRError("invalid TSV page geometry", "OCR_PROVIDER_OUTPUT_INVALID")
        if iw<=0 or ih<=0: raise OCRError("invalid TSV page geometry", "OCR_PROVIDER_OUTPUT_INVALID")
        for _,region,(x,y,w,h) in regions:
            if x+w>iw or y+h>ih: raise OCRError("TSV geometry exceeds page", "OCR_PROVIDER_OUTPUT_INVALID")
            region["bounding_box"]={"x":x/iw,"y":y/ih,"width":w/iw,"height":h/ih}
    return [r for _,r,_ in sorted(regions,key=lambda i:i[0])]
